Title: Fix hardcoded 200K context window — derive from model config, add --context-window override
Files: src/main.rs, src/cli.rs, src/help.rs, docs/src/configuration/models.md
Issue: #195, #197

## Problem

`src/main.rs` line ~1277 hardcodes `max_context_tokens: 200_000` for ALL providers via `with_context_config()`. This overrides yoagent's built-in auto-derivation from `ModelConfig.context_window`:

- Anthropic: 200K ✓ (correct by coincidence)
- Google: 1M → compacts at 200K = 80% wasted
- MiniMax: 1M → compacts at 200K = 80% wasted
- OpenAI: 128K → compacts at 200K = never compacts until too late
- xAI: 131K → same problem
- Ollama/local: 128K default but user may configure differently

Issue #197 documents a previous revert due to build failure. This attempt must be clean.

## Implementation

### Step 1: Add `context_window: Option<u32>` to Config in cli.rs

In `src/cli.rs`, add `pub context_window: Option<u32>` to the `Config` struct. Parse it from:
- CLI: `--context-window <N>` (similar to `--max-turns`)
- Config file: `context_window = 1000000` in `[agent]` section of `.yoyo.toml`

In the argument parsing loop, add a case:
```rust
"--context-window" => {
    context_window = args.get(i + 1).and_then(|v| v.parse().ok());
    if context_window.is_some() { i += 1; }
}
```

Initialize `let mut context_window: Option<u32> = None;` with the other arg variables.

Add `context_window` to the Config struct construction at the end of `parse_args`.

### Step 2: Thread context_window into AgentConfig in main.rs

Add `pub context_window: Option<u32>` to the `AgentConfig` struct.

When constructing `AgentConfig` (search for `AgentConfig {`), add:
```rust
context_window: config.context_window,
```

### Step 3: Fix configure_agent to derive from model config

In `configure_agent()`, the ModelConfig has already been set on the agent via `with_model_config()` before `configure_agent` is called. But `configure_agent` doesn't receive the ModelConfig directly.

**Better approach:** Pass the model's context_window into `configure_agent` or compute it in `build_agent` where we have the ModelConfig:

In `build_agent()`, capture the context_window from the model config before passing to configure_agent:

```rust
pub fn build_agent(&self) -> Agent {
    let base_url = self.base_url.as_deref();

    if self.provider == "anthropic" && base_url.is_none() {
        let mut model_config = ModelConfig::anthropic(&self.model, &self.model);
        insert_client_headers(&mut model_config);
        let cw = model_config.context_window;
        let agent = Agent::new(AnthropicProvider).with_model_config(model_config);
        self.configure_agent(agent, cw)
    } else if self.provider == "google" {
        let model_config = create_model_config(&self.provider, &self.model, base_url);
        let cw = model_config.context_window;
        let agent = Agent::new(GoogleProvider).with_model_config(model_config);
        self.configure_agent(agent, cw)
    } else {
        let model_config = create_model_config(&self.provider, &self.model, base_url);
        let cw = model_config.context_window;
        let agent = Agent::new(OpenAiCompatProvider).with_model_config(model_config);
        self.configure_agent(agent, cw)
    }
}
```

Change `configure_agent` signature to:
```rust
fn configure_agent(&self, mut agent: Agent, model_context_window: u32) -> Agent {
```

Then replace the hardcoded ContextConfig with:
```rust
// Derive context window: user override > model config default
let effective_cw = self.context_window.unwrap_or(model_context_window);
agent = agent.with_context_config(ContextConfig {
    max_context_tokens: (effective_cw as usize) * 80 / 100,
    system_prompt_tokens: 4_000,
    keep_recent: 10,
    keep_first: 2,
    tool_output_max_lines: 50,
});
```

This preserves our custom `keep_recent`, `keep_first`, and `tool_output_max_lines` values while using the correct context window per provider.

### Step 4: Update /tokens display

If `/tokens` or any status display shows the context window, update it to show the effective value. Search for the token display code in `commands.rs` and `prompt.rs`.

### Step 5: Update help text

In `src/help.rs`, add `--context-window` to the help page under options/configuration.

In `src/cli.rs`, add to `print_help()` output.

### Step 6: Tests

Add to `src/cli.rs` tests:
- `test_context_window_default_is_none` — no flag → None
- `test_context_window_parses_value` — `--context-window 32000` → Some(32000)
- `test_context_window_from_toml` — config file sets it

Add to `src/main.rs` tests:
- `test_model_config_context_windows_vary_by_provider` — verify that `create_model_config` for different providers returns different context_window values (e.g., google = 1M, openai = 128K)

### Step 7: Update docs

Update `docs/src/configuration/models.md`:
- Document that yoyo now auto-derives context window per provider
- Document the `--context-window` override flag
- List when to use it (custom Ollama setups, non-standard deployments)

### Important notes

- The previous attempt (#197) failed at build time. Be extremely careful with the `configure_agent` signature change — update ALL call sites.
- `ModelConfig.context_window` is a `pub u32` field — it's directly accessible.
- Keep `with_context_config()` call unconditional — we always want our custom keep_recent/keep_first values, just with the right max_context_tokens.
- Run `cargo build` before running tests to catch any signature mismatches early.
