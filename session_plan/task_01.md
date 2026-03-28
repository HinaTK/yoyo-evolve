Title: Add --fallback CLI flag for mid-session provider failover
Files: src/main.rs, src/cli.rs, tests/integration.rs
Issue: #205

## Description

Build a `FallbackProvider` wrapper that implements yoagent's `StreamProvider` trait and enables automatic mid-session failover when the primary provider fails. This is the hardest task — it goes first.

### Architecture

yoagent does NOT have built-in fallback/failover. It has:
- `RetryConfig` — retries the SAME provider with exponential backoff (handles transient errors)
- `ProviderError::is_retryable()` — only true for `RateLimited` and `Network` variants

We need a NEW layer: a `FallbackProvider` that wraps two `StreamProvider` instances and catches non-retryable errors to try the second provider.

### Implementation Plan

1. **CLI parsing** in `cli.rs`:
   - Add `--fallback <provider:model>` option to `CliArgs`
   - Parse the `provider:model` format (e.g., `openai:gpt-4o`, `anthropic:claude-sonnet-4-20250514`)
   - Store as `fallback_provider: Option<String>` and `fallback_model: Option<String>`
   - Also support config file: `fallback = "openai:gpt-4o"` in `.yoyo.toml`

2. **FallbackProvider** in `src/main.rs` (or a new section within it):
   - Struct holding `primary: Arc<dyn StreamProvider>` and `fallback: Arc<dyn StreamProvider>` with their respective `ModelConfig`s
   - Implement `StreamProvider` for `FallbackProvider`:
     - Try `primary.stream()` first
     - If it returns a non-retryable `ProviderError` (Auth, Api, ContextOverflow, Other — NOT RateLimited or Network since those are handled by yoagent's retry), construct a new `StreamConfig` with the fallback's model/config and call `fallback.stream()`
     - Log the failover to stderr so the user knows it happened
   - Note: `ProviderError::Cancelled` should NOT trigger failover (user explicitly cancelled)

3. **Wire into `AgentConfig::build_agent()`**:
   - If `--fallback` is set, construct both the primary and fallback providers
   - Wrap them in `FallbackProvider`
   - Pass `FallbackProvider` as the agent's provider

4. **Tests**:
   - Unit test: parse `--fallback openai:gpt-4o` correctly
   - Unit test: parse `--fallback` with invalid format gives error
   - Integration test: verify `--fallback` appears in help output
   - Unit test: `FallbackProvider` delegates to primary on success (mock or simple test)

### Key considerations
- The fallback provider needs its own API key. Check env vars for the fallback provider (e.g., if fallback is `openai:gpt-4o`, look for `OPENAI_API_KEY`).
- Don't fail at startup if fallback key is missing — warn and disable fallback.
- The `StreamConfig` sent to the fallback needs the fallback's model name and model_config, but the same messages/tools/system_prompt.
- Update help text and docs to mention the new flag.

### Docs to update
- `src/help.rs` — add `--fallback` to CLI flags section
- `docs/src/configuration/models.md` — mention fallback configuration
- `CLAUDE.md` — add to recently changed files if needed
