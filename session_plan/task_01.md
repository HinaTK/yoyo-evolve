Title: Add --fallback CLI flag for mid-session provider failover (retry)
Files: src/main.rs, src/cli.rs, src/help.rs, tests/integration.rs, docs/src/configuration/models.md
Issue: #205

## Context

This was attempted on Day 28 (04:07) and reverted because tests failed (Issue #207). The architecture was sound — a `FallbackProvider` wrapping two `StreamProvider` instances — but the implementation had test failures. This retry takes a more careful, test-first approach.

## Strategy: Minimal first, test early

The previous attempt tried to do everything at once. This time:
1. Write CLI parsing + tests FIRST, verify they pass
2. Write FallbackProvider struct + trait impl, verify build
3. Wire into agent construction, verify full test suite
4. Update help text and docs last

## Step-by-step implementation

### 1. CLI parsing in `cli.rs`

Add to `CliArgs` struct:
```
--fallback <PROVIDER:MODEL>   Fallback provider:model for automatic failover (e.g., openai:gpt-4o)
```

Parse the `provider:model` format. Store as `fallback: Option<String>` in CliArgs. In the config resolution, split on `:` to get provider and model.

Also support in `.yoyo.toml`:
```toml
fallback = "openai:gpt-4o"
```

Add a helper function `parse_fallback(s: &str) -> Result<(String, String), String>` that validates the format. Write tests for this function immediately:
- `parse_fallback("openai:gpt-4o")` → Ok(("openai", "gpt-4o"))
- `parse_fallback("anthropic:claude-sonnet-4-20250514")` → Ok(...)
- `parse_fallback("invalid")` → Err (no colon)
- `parse_fallback(":model")` → Err (empty provider)
- `parse_fallback("provider:")` → Err (empty model)

Run `cargo test` after this step before proceeding.

### 2. FallbackProvider in `src/main.rs`

Create a `FallbackProvider` struct:
```rust
struct FallbackProvider {
    primary: Arc<dyn StreamProvider>,
    fallback: Arc<dyn StreamProvider>,
    fallback_model: String,
    fallback_model_config: Option<ModelConfig>,
}
```

Implement `StreamProvider` for `FallbackProvider`:
- `async fn stream(&self, config: StreamConfig) -> Result<EventStream, ProviderError>`
- Try `self.primary.stream(config.clone())` first
- On error, check if the error is a failover candidate:
  - YES failover: `ProviderError::Auth`, `ProviderError::Api`, `ProviderError::Other`
  - NO failover: `ProviderError::RateLimited` (yoagent retry handles this), `ProviderError::Network` (transient), `ProviderError::Cancelled` (user intent), `ProviderError::ContextOverflow` (won't help to switch)
- On failover: log to stderr with `eprintln!`, construct new `StreamConfig` with fallback's model/model_config but same messages/tools/system_prompt, call `self.fallback.stream(new_config)`

**IMPORTANT**: Check what `StreamConfig` fields exist in yoagent. Read the yoagent source to understand the exact struct fields:
```bash
find ~/.cargo/registry/src -path "*/yoagent-*/src/*" -name "*.rs" | xargs grep -l "StreamConfig" | head -5
```
Then read the struct definition to know exactly what fields to modify for failover.

Also check if `StreamConfig` implements `Clone`. If not, you'll need to reconstruct it field by field.

Also check the exact variants of `ProviderError` — don't assume, read the actual enum.

Run `cargo build` after this step. Don't worry about the wiring yet — just make sure the struct compiles.

### 3. Wire into AgentConfig::build_agent()

In `AgentConfig` struct, add:
```rust
pub fallback: Option<String>,  // "provider:model" format
```

In the `build_agent()` method:
- If `fallback` is set, parse it
- Look up the API key env var for the fallback provider (e.g., `OPENAI_API_KEY` for openai)
- If key is missing, warn and disable fallback (don't fail)
- Construct the fallback provider using the same `create_provider()` helper
- Wrap primary + fallback in `FallbackProvider`
- Pass `FallbackProvider` as the agent's provider

The key function is `create_provider()` or however the provider is currently constructed — read the existing code to find where `AnthropicProvider::new()` or similar is called.

### 4. Integration test

Add to `tests/integration.rs`:
```rust
#[test]
fn test_fallback_in_help() {
    let output = Command::new(env!("CARGO_BIN_EXE_yoyo"))
        .arg("--help")
        .output()
        .expect("failed to run yoyo");
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("--fallback"), "help should mention --fallback");
}
```

### 5. Update help text

In `src/help.rs`, add `--fallback` to the CLI flags section with a brief description.

### 6. Update docs

In `docs/src/configuration/models.md`, add a section about fallback configuration:
- CLI usage: `--fallback openai:gpt-4o`
- Config file: `fallback = "openai:gpt-4o"` in `.yoyo.toml`
- Behavior: automatic failover on API errors, preserves conversation context
- Which errors trigger failover and which don't

## Key gotchas from the first attempt

- Don't assume `StreamConfig` is `Clone` — check first
- Don't assume `ProviderError` variants — read the actual enum  
- The fallback provider needs its own API key from env vars
- Keep the test surface small — CLI parsing tests + help test + build passing is enough
- DO NOT try to write mock provider tests — that's what caused the first failure. Real integration testing of failover requires actual API calls. Just test the CLI parsing and wiring.

## Verification

After each step, run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings`. If any step fails, fix it before moving to the next. If the FallbackProvider implementation proves too complex for yoagent's current trait requirements, fall back to just the CLI parsing + a TODO comment — shipping partial progress is better than another revert.
