Title: Add AskUserTool — let the model ask the user directed questions
Files: src/main.rs, src/help.rs, src/commands.rs
Issue: #187

## Context

Issue #187 challenges yoyo to match Claude Code's `ask_question` tool. The model should be able to ask the user directed questions mid-task instead of guessing. This is the second biggest capability gap after SubAgentTool (which is task_01).

## Implementation

### 1. Create `AskUserTool` struct in `src/main.rs`

This is an internal tool (like TodoTool would be) that reads from stdin. It should be placed near the other custom tools (StreamingBashTool, RenameSymbolTool, etc.).

```rust
/// Tool that lets the model ask the user directed questions.
/// The user types their answer, which is returned as the tool result.
pub struct AskUserTool;

#[async_trait::async_trait]
impl AgentTool for AskUserTool {
    fn name(&self) -> &str { "ask_user" }
    fn label(&self) -> &str { "ask_user" }
    fn description(&self) -> &str {
        "Ask the user a question to get clarification or input. Use this when you need \
         specific information to proceed, like a preference, a decision, or context that \
         isn't available in the codebase. The user sees your question and types a response."
    }
    fn parameters_schema(&self) -> serde_json::Value {
        serde_json::json!({
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the user. Be specific and concise."
                }
            },
            "required": ["question"]
        })
    }
    async fn execute(
        &self,
        params: serde_json::Value,
        _ctx: ToolContext,
    ) -> Result<ToolResult, ToolError> {
        let question = params.get("question")
            .and_then(|v| v.as_str())
            .ok_or_else(|| ToolError::InvalidArgs("Missing 'question' parameter".into()))?;

        // Display the question with visual distinction
        eprintln!("\n{YELLOW}  ❓ {question}{RESET}");
        eprint!("{GREEN}  → {RESET}");
        io::stderr().flush().ok();

        // Read the user's response
        use std::io::BufRead;
        let mut response = String::new();
        let stdin = io::stdin();
        match stdin.lock().read_line(&mut response) {
            Ok(0) | Err(_) => {
                return Ok(ToolResult {
                    content: vec![Content::Text {
                        text: "(user provided no response)".to_string(),
                    }],
                    details: serde_json::Value::Null,
                });
            }
            _ => {}
        }

        let response = response.trim().to_string();
        if response.is_empty() {
            return Ok(ToolResult {
                content: vec![Content::Text {
                    text: "(user provided empty response)".to_string(),
                }],
                details: serde_json::Value::Null,
            });
        }

        Ok(ToolResult {
            content: vec![Content::Text { text: response }],
            details: serde_json::Value::Null,
        })
    }
}
```

### 2. Register in `build_tools()`

Add `AskUserTool` to the tools vec returned by `build_tools()`. It does NOT need permission guarding (it doesn't touch the filesystem). It does NOT need truncation wrapping (user responses are short). But it should ONLY be included when stdin is a terminal (not in piped mode).

Add a parameter to `build_tools()` or check `io::stdin().is_terminal()` inside the function. Since `build_tools` already receives `max_tool_output` (which varies by piped vs terminal mode), the simplest approach is to check `io::stdin().is_terminal()` inside `build_tools`:

```rust
// Only add ask_user in interactive mode
if std::io::stdin().is_terminal() {
    tools.push(Box::new(AskUserTool));
}
```

**CRITICAL**: This changes the tool count. Update ALL tests that assert `tools.len() == 7`:
- `test_build_tools_returns_six_tools` (line ~1444) — update assertion based on terminal detection. Since tests run without a terminal, `is_terminal()` returns false, so the count stays 7 in tests. Add a comment explaining this.
- `test_build_tools_auto_approve_skips_confirmation` (line ~1789) — same
- `test_build_tools_no_approve_includes_confirmation` (line ~1803) — same
- `test_build_tools_with_piped_limit` (line ~2457) — same

Actually, since tests don't have a terminal, `is_terminal()` returns false, so AskUserTool won't be added in tests, and the count stays 7. This means existing tests pass without changes. But we should add a dedicated test that verifies the behavior:

```rust
#[test]
fn test_ask_user_tool_schema() {
    let tool = AskUserTool;
    assert_eq!(tool.name(), "ask_user");
    let schema = tool.parameters_schema();
    assert!(schema["properties"]["question"].is_object());
    assert!(schema["required"].as_array().unwrap().contains(&serde_json::json!("question")));
}

#[test]
fn test_ask_user_tool_not_in_piped_mode() {
    // In test environment (no terminal), ask_user should NOT be included
    let perms = cli::PermissionConfig::default();
    let dirs = cli::DirectoryRestrictions::default();
    let tools = build_tools(true, &perms, &dirs, TOOL_OUTPUT_MAX_CHARS);
    let names: Vec<&str> = tools.iter().map(|t| t.name()).collect();
    assert!(!names.contains(&"ask_user"), "ask_user should not be in non-terminal mode");
}
```

### 3. Update help text

In `src/help.rs`, mention that the model can ask questions:
```
"The agent can ask you questions mid-task using the ask_user tool."
```

### 4. Update KNOWN_COMMANDS description if relevant

This is a model tool, not a REPL command. No slash command needed. But mention it in the `/help` output under a "Model capabilities" section or similar.

### 5. Edge cases

- **Piped mode**: Don't register the tool (stdin isn't interactive)
- **EOF on stdin**: Return "(user provided no response)"
- **Empty response**: Return "(user provided empty response)"
- **Auto-approve mode**: The tool doesn't need approval — it's asking FOR user input, not performing a dangerous action

After implementing, run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings`.
