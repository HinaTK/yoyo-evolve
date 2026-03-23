Title: Add terminal bell notification when agent completes a long operation
Files: src/prompt.rs, src/cli.rs, src/repl.rs
Issue: none

## Context

When a developer sends a complex prompt and switches to another terminal tab, they have no way of knowing the agent finished except by switching back and checking. Claude Code rings a terminal bell (`\x07`) after completing responses that take more than a few seconds. This is a tiny feature with outsized UX impact for real developers who are multitasking.

## Implementation

1. **In `src/prompt.rs`**: After `run_prompt()` completes (both in single-prompt and REPL paths), measure the elapsed wall time. If the response took longer than 3 seconds, emit a terminal bell character `\x07` to stdout. This causes the terminal emulator to flash the tab or play a sound depending on the user's settings.

2. **In `src/cli.rs`**: Add a `--no-bell` flag (and corresponding `bell = false` in `.yoyo.toml` config) so users who find it annoying can disable it. Default is ON. Parse it in `parse_args()` and add `bell: bool` to `AgentConfig`. Also check for a `YOYO_NO_BELL` env var.

3. **In `src/repl.rs`**: Wire the bell into the REPL loop. After each `run_prompt()` call returns, check elapsed time and ring bell if > 3 seconds.

4. **Tests**:
   - `test_bell_flag_parsing`: `--no-bell` sets `bell: false` in AgentConfig
   - `test_bell_env_var`: `YOYO_NO_BELL=1` disables bell
   - `test_bell_config_toml`: `bell = false` in config file disables bell
   - The actual bell emission doesn't need a test (it's just printing `\x07`) but the flag/config parsing does.

This brings us to parity with Claude Code's notification behavior and makes yoyo more usable in real workflows where the developer isn't staring at the terminal.
