Title: Remove hardcoded execution limits — make turns/tokens configurable or unlimited
Files: src/main.rs, src/cli.rs
Issue: #278

## Problem

yoyo has hardcoded execution limits that constrain agent autonomy:

1. `max_turns` defaults to 200 (line 360 in main.rs), but help text says "default: 50" (line 153 in cli.rs) — documentation inconsistency.
2. `max_total_tokens` is hardcoded to 1,000,000 (line 361 in main.rs) and NOT configurable via any flag or config file.

These limits mean the agent silently stops mid-task when hitting them. Claude Code has no such limits. Issue #278 requests `/extended` mode for long tasks, and the maintainer's response is clear: "We shouldn't limit the agent with budget. Extend / without limit should be the default."

## Fix

### 1. Fix help text inconsistency (cli.rs)

Line 153 says `"default: 50"` but the actual default is 200. Fix to match reality OR remove the default from help text since we're making it unlimited:

Change help text to:
```
"  --max-turns <n>   Maximum agent turns per prompt (default: unlimited)"
```

### 2. Make max_total_tokens configurable (main.rs + cli.rs)

Currently `max_total_tokens: 1_000_000` is hardcoded. Add a `--max-session-tokens` flag:

In `cli.rs`:
- Add `pub max_session_tokens: Option<usize>` to the Config struct (near line 73 where `max_turns` is)
- Add it to the flag list (near line 518)
- Parse it with `parse_numeric_flag` (near line 1082)
- Add help text: `"  --max-session-tokens <n>  Maximum total tokens per session (default: unlimited)"`

In `main.rs`:
- Change the `ExecutionLimits` block (line 359-363) to:
```rust
let limits = ExecutionLimits {
    max_turns: self.max_turns.unwrap_or(usize::MAX),
    max_total_tokens: self.max_session_tokens.unwrap_or(usize::MAX),
    ..ExecutionLimits::default()
};
if limits.max_turns < usize::MAX || limits.max_total_tokens < usize::MAX {
    agent = agent.with_execution_limits(limits);
}
```

This makes both limits unlimited by default. Users who want limits can set `--max-turns 200` or `--max-session-tokens 1000000`.

### 3. Update AgentConfig (main.rs)

Add `max_session_tokens` to the `AgentConfig` struct (near line 299) and thread it through `build_agent`.

### 4. Wire through existing config file support

In the config file example (cli.rs line 392-393), update:
```
max_turns = 200      # optional, unlimited by default
max_session_tokens = 1000000  # optional, unlimited by default
```

## Verification

```bash
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```

Also verify the help text:
```bash
cargo run -- --help 2>&1 | grep -i "max-turns\|max-session-tokens"
```

## Notes

This addresses the SPIRIT of #278 without building a separate `/extended` command. The maintainer explicitly said unlimited should be the default. By removing the hardcoded limits, every session is effectively "extended" by default. Users who want guardrails can set explicit limits.

Don't add an `/extended` slash command — that's unnecessary complexity when the fix is just removing artificial caps. The `/extended` idea from the issue can be deferred or closed with "unlimited is now the default."
