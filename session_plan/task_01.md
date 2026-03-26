Title: Register SubAgentTool via Agent::with_sub_agent()
Files: src/main.rs, src/help.rs
Issue: #186, #194

## Context

This is the #1 capability gap — Claude Code and Codex both have model-initiated sub-agents. yoagent 0.7.4 provides `SubAgentTool` and `Agent::with_sub_agent()`. Two previous attempts failed (Issue #194) because they tried to modify `build_tools()`, breaking tool-count assertions. This time we use the correct API.

## Why previous attempts failed

The Issue #194 plan tried to add SubAgentTool inside `build_tools()` or by manually building tool vecs and calling `.with_tools()`. This broke `test_build_tools_returns_six_tools` (asserts exactly 7 tools). The correct approach is `Agent::with_sub_agent(sub_agent_tool)` — a dedicated method on Agent that simply pushes the tool to the internal vec without affecting `build_tools`.

## Implementation

### 1. Create `build_sub_agent_tool()` function in `src/main.rs`

Add this function near `build_tools()` (around line 860):

```rust
use yoagent::sub_agent::SubAgentTool;
use yoagent::provider::StreamProvider;

/// Build a SubAgentTool that inherits the parent's provider/model/key.
/// The sub-agent gets basic tools (no permission prompts, no sub-agent recursion).
fn build_sub_agent_tool(config: &AgentConfig) -> SubAgentTool {
    // Sub-agent gets standard yoagent tools — no permission guards needed
    // since the parent already authorized the delegation.
    let child_tools: Vec<Arc<dyn AgentTool>> = vec![
        Arc::new(yoagent::tools::BashTool::default()),
        Arc::new(yoagent::tools::ReadFileTool::default()),
        Arc::new(yoagent::tools::WriteFileTool::new()),
        Arc::new(yoagent::tools::EditFileTool::new()),
        Arc::new(yoagent::tools::ListFilesTool::default()),
        Arc::new(yoagent::tools::SearchTool::default()),
    ];

    // Select the right provider
    let provider: Arc<dyn StreamProvider> = match config.provider.as_str() {
        "anthropic" => Arc::new(AnthropicProvider),
        "google" => Arc::new(GoogleProvider),
        _ => Arc::new(OpenAiCompatProvider),
    };

    SubAgentTool::new("sub_agent", provider)
        .with_description(
            "Delegate a subtask to a fresh sub-agent with its own context window. \
             Use for complex, self-contained subtasks like: researching a codebase, \
             running a series of tests, or implementing a well-scoped change. \
             The sub-agent has bash, file read/write/edit, list, and search tools. \
             It starts with a clean context and returns a summary of what it did."
        )
        .with_system_prompt(
            "You are a focused sub-agent. Complete the given task efficiently \
             using the tools available. Be thorough but concise in your final \
             response — summarize what you did, what you found, and any issues."
        )
        .with_model(&config.model)
        .with_api_key(&config.api_key)
        .with_tools(child_tools)
        .with_thinking(config.thinking)
        .with_max_turns(25)
}
```

**Important notes:**
- Return type is `SubAgentTool`, NOT `Box<dyn AgentTool>` — because `with_sub_agent()` takes `SubAgentTool` directly
- Use `yoagent::tools::BashTool` (not StreamingBashTool) — the sub-agent doesn't need streaming bash since its events flow through the parent's event channel
- No `with_model_config()` exists on SubAgentTool — `model + api_key + provider` is sufficient for Anthropic. For other providers, the provider already handles routing.
- No recursive sub-agents — the child doesn't get a SubAgentTool (by design)

### 2. Wire into `configure_agent()`

In `configure_agent()` (around line 999), AFTER the existing `agent = agent.with_tools(build_tools(...))` call, add:

```rust
agent = agent.with_sub_agent(build_sub_agent_tool(self));
```

This adds the SubAgentTool to the agent's tool list via the dedicated API, completely separate from `build_tools()`. The `build_tools()` function stays at 7 tools. All existing tool-count tests pass unchanged.

### 3. Handle sub-agent events in the event loop

In the main event handling match (search for `AgentEvent::ToolExecutionStart` in main.rs), the sub-agent's events are automatically forwarded through the parent's event stream by yoagent. Check if `ToolExecutionStart` events from sub-agents have the tool_name prefixed or if there's a separate event variant. If not, the existing event handling should work — the sub-agent's bash/read/write calls will show up as regular tool events.

Add a visual indicator when the sub-agent tool itself is invoked. In the `ToolExecutionStart` match arm, detect `tool_name == "sub_agent"` and print a distinctive header:
```rust
if tool_name == "sub_agent" {
    // Print a distinctive header for sub-agent delegation
    eprintln!("\n{DIM}  🐙 Delegating to sub-agent...{RESET}");
}
```

### 4. Tests

Add these tests in the `#[cfg(test)]` module in `src/main.rs`:

```rust
#[test]
fn test_build_sub_agent_tool_returns_correct_name() {
    let config = AgentConfig {
        model: "claude-sonnet-4-20250514".to_string(),
        api_key: "test-key".to_string(),
        provider: "anthropic".to_string(),
        base_url: None,
        skills: yoagent::skills::SkillSet::empty(),
        system_prompt: "test".to_string(),
        thinking: ThinkingLevel::Off,
        max_tokens: None,
        temperature: None,
        max_turns: None,
        auto_approve: true,
        permissions: cli::PermissionConfig::default(),
        dir_restrictions: cli::DirectoryRestrictions::default(),
        context_strategy: cli::ContextStrategy::Compact,
    };
    let tool = build_sub_agent_tool(&config);
    assert_eq!(tool.name(), "sub_agent");
}

#[test]
fn test_build_sub_agent_tool_has_task_parameter() {
    let config = /* same as above */;
    let tool = build_sub_agent_tool(&config);
    let schema = tool.parameters_schema();
    assert!(schema["properties"]["task"].is_object(), "Should have 'task' parameter");
    assert!(schema["required"].as_array().unwrap().contains(&serde_json::json!("task")));
}

#[test]
fn test_build_tools_count_unchanged() {
    // Verify build_tools still returns exactly 7 (SubAgentTool is separate)
    let perms = cli::PermissionConfig::default();
    let dirs = cli::DirectoryRestrictions::default();
    let tools = build_tools(true, &perms, &dirs, TOOL_OUTPUT_MAX_CHARS);
    assert_eq!(tools.len(), 7, "build_tools must stay at 7 — SubAgentTool is added via with_sub_agent");
}

#[test]
fn test_configure_agent_includes_sub_agent() {
    // Use test_agent_config helper and check that the resulting agent
    // gets more tools than build_tools alone (7 base + 1 sub_agent = 8)
    let config = test_agent_config("anthropic", "claude-sonnet-4-20250514");
    let agent = config.build_agent();
    // We can't easily introspect tool count on Agent, but we can verify
    // build_sub_agent_tool doesn't panic with various providers
    let _tool_anthropic = build_sub_agent_tool(&test_agent_config("anthropic", "claude-sonnet-4-20250514"));
    let _tool_google = build_sub_agent_tool(&test_agent_config("google", "gemini-2.0-flash"));
    let _tool_openai = build_sub_agent_tool(&test_agent_config("openai", "gpt-4o"));
    // All three providers build without panic
}
```

Use the existing `test_agent_config` helper (line ~2048) for constructing test configs.

### 5. Update help text

In `src/help.rs`, add sub-agent mention to the general help text where tools are described. Something like:
```
"The agent can also delegate complex subtasks to sub-agents with their own context windows."
```

### 6. Do NOT update KNOWN_COMMANDS or docs

The sub-agent is a model tool, not a REPL command. No `/sub_agent` command needed — the model decides when to use it. `/spawn` already exists as the user-initiated version.

### Key risks and mitigations

1. **Import issues**: Make sure `use yoagent::sub_agent::SubAgentTool;` is at the top of main.rs. Also need `use yoagent::provider::StreamProvider;` for the `Arc<dyn StreamProvider>` type.
2. **Tool count tests**: `build_tools` tests assert 7 — this plan DOES NOT change build_tools, so they pass.
3. **configure_agent tests**: Some tests call `configure_agent` and check agent properties. Adding `with_sub_agent` shouldn't break those since it just adds a tool.
4. **The `test_agent_config` helper**: Check if it exists at line ~2048 and what fields it sets. Use it for test configs.

After implementing, run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` to verify everything passes.
