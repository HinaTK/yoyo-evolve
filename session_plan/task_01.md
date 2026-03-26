Title: Fix hardcoded 200K context window — let yoagent auto-derive, add --context-window override
Files: src/main.rs, src/cli.rs, src/help.rs, src/commands.rs, docs/src/configuration/models.md
Issue: #195

## Problem

`main.rs:1158` hardcodes `max_context_tokens: 200_000` for ALL providers via an explicit `with_context_config()`. This overrides yoagent's built-in auto-derivation from `ModelConfig.context_window`, which already has correct per-provider defaults:

- Anthropic: 200K ✓
- Google: 1M (but we compact at 200K — 80% wasted)
- MiniMax: 1M (but we compact at 200K — 80% wasted)
- OpenAI: 128K (but we compact at 200K — never compacts until too late)
- xAI: 131K (same issue)
- Ollama/local: 128K default (but user might set n_ctx to 32K or 512K)

yoagent v0.7.4 already does the right thing: if no `with_context_config()` is called, it auto-derives from `ModelConfig.context_window` using `ContextConfig::from_context_window()` which reserves 20% for output and uses 80% as compaction budget.

## Implementation

### Step 1: Remove the hardcoded ContextConfig

In `src/main.rs`, find the block around line 1158:

```rust
agent = agent.with_context_config(ContextConfig {
    max_context_tokens: 200_000,
    system_prompt_tokens: 4_000,
    keep_recent: 10,
    keep_first: 2,
    tool_output_max_lines: 50,
});
```

Replace it with conditional logic:
- If `--context-window <N>` was provided, use `ContextConfig::from_context_window(N)` with our custom overrides (keep_recent, keep_first, tool_output_max_lines)
- Otherwise, do NOT call `with_context_config()` at all — let yoagent auto-derive from the ModelConfig

BUT we want to preserve our custom values for `keep_recent: 10`, `keep_first: 2`, `tool_output_max_lines: 50`. So the replacement should be:

```rust
// If user specified --context-window, use that; otherwise let yoagent auto-derive
// from ModelConfig.context_window (correct per-provider defaults)
if let Some(context_window) = self.context_window {
    agent = agent.with_context_config(ContextConfig {
        max_context_tokens: (context_window as usize) * 80 / 100,
        system_prompt_tokens: 4_000,
        keep_recent: 10,
        keep_first: 2,
        tool_output_max_lines: 50,
    });
}
// Note: when no --context-window is set, yoagent auto-derives ContextConfig
// from model_config.context_window — see agent.rs line 653
```

Wait — we need to preserve our custom overrides (keep_recent, keep_first, tool_output_max_lines) even when auto-deriving. The auto-derived config uses defaults for those fields. Check the defaults:

```rust
// yoagent ContextConfig::default()
// keep_recent: 4, keep_first: 1, tool_output_max_lines: 200
```

Our values (10, 2, 50) are deliberate choices. So we should ALWAYS set a ContextConfig but derive `max_context_tokens` from either the override or the model config. The approach:

```rust
let max_context_tokens = if let Some(cw) = self.context_window {
    (cw as usize) * 80 / 100
} else {
    // Will be auto-derived by yoagent from ModelConfig.context_window
    // We set 0 here as sentinel — but actually we should just not set it.
    // Better approach: always compute from the model config we're about to create.
    0 // placeholder
};
```

Actually, the cleanest approach: compute `max_context_tokens` from the ModelConfig we already have at that point. Look at the flow in `configure_agent()` — the ModelConfig is already set on the agent before context config. So we can read it:

**Best approach:**
1. Add `context_window: Option<u32>` to `Config` struct in cli.rs
2. Parse `--context-window <N>` in CLI args
3. In `configure_agent()`, compute the ContextConfig based on: user override if present, otherwise don't call `with_context_config()` BUT we need custom keep_recent etc. So instead: always compute from the model config's `context_window` field, which is already correct per-provider.

Actually simplest: the ModelConfig is being created before `with_context_config()` is called. We know the context_window from the model config. So:

```rust
// Determine context window: user override > model config default
let effective_context_window = self.context_window
    .unwrap_or_else(|| {
        // Read from the model config that was already set
        // For Anthropic: 200K, Google: 1M, OpenAI: 128K, etc.
        // The model_config is set earlier in this function
        model_context_window  // need to capture this from where ModelConfig is created
    });

agent = agent.with_context_config(ContextConfig {
    max_context_tokens: (effective_context_window as usize) * 80 / 100,
    system_prompt_tokens: 4_000,
    keep_recent: 10,
    keep_first: 2,
    tool_output_max_lines: 50,
});
```

To implement this, after the ModelConfig is created (around line 1212 for Anthropic, or from `create_model_config()` for others), capture the `context_window` value. The model config creation happens in two paths:
- Anthropic: `ModelConfig::anthropic(...)` at ~line 1212
- Others: `create_model_config(provider, model, base_url)` at ~line 1108

Both paths should produce a `model_config` variable. Capture `model_config.context_window` and use it as the fallback.

### Step 2: Add `--context-window` CLI flag

In `src/cli.rs`:
1. Add `pub context_window: Option<u32>` to the `Config` struct
2. Add `--context-window <N>` parsing in the arg loop (similar to `--max-turns`)
3. Also support `context_window = 32000` in `.yoyo.toml` under `[agent]` section
4. Update `print_help()` with the new flag

### Step 3: Update help text

In `src/help.rs`, update the help for `--context-window`.

In `src/commands.rs`, if there's a `/tokens` command that shows context window info, it should show the effective context window.

### Step 4: Update docs

Update `docs/src/configuration/models.md` to document:
- The auto-derivation behavior (yoyo now uses correct context windows per provider)
- The `--context-window` override flag
- When to use it (custom Ollama n_ctx, non-standard deployments)

### Step 5: Tests

Add tests in `src/cli.rs`:
- `test_context_window_default_is_none` — no flag means None (auto-derive)
- `test_context_window_parses_value` — `--context-window 32000` → Some(32000)
- `test_context_window_missing_value` — `--context-window` with no number → None (or error)
- `test_context_window_from_toml` — config file sets it

Add tests in `src/main.rs`:
- `test_configure_agent_uses_model_context_window` — verify that without --context-window override, the effective context window matches the model config
- `test_configure_agent_context_window_override` — verify that --context-window overrides the model default

### Important notes

- The `ContextConfig` import is already present: `use yoagent::context::{ContextConfig, ExecutionLimits};`
- The `from_context_window()` helper exists but gives default keep_recent/keep_first — we want our custom values, so manually construct the struct
- @yuanhao's comment on the issue says to verify provider context window defaults against docs — the yoagent factory defaults are already reasonable (checked above), but don't blindly trust them; the key ones are: Anthropic 200K ✓, Google 1M ✓, OpenAI 128K ✓, MiniMax 1M ✓
