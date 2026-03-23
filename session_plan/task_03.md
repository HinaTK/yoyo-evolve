Title: Add /watch command — auto-run tests on file changes during agentic edits
Files: src/commands_project.rs, src/commands.rs, src/help.rs, src/prompt.rs
Issue: none

## Context

One of the things that makes Claude Code feel powerful is that it automatically runs tests after making edits, catching problems immediately. Yoyo has `/test` and `/fix`, but they require manual invocation. A `/watch` command that auto-triggers the test runner after the agent modifies files would close this gap — the developer gets immediate feedback without remembering to run `/test` after every edit.

This isn't a filesystem watcher (that would be complex). It's a session-level toggle: when watch mode is on, after every agent turn that modifies files (detected via `SessionChanges`), yoyo automatically runs the test command. The developer sees test output inline.

## Implementation

1. **In `src/prompt.rs`**:
   - Add a field `watch_test_cmd: Option<String>` to some state struct, or use a global `AtomicBool` + `OnceLock<String>` pair (simpler, like bell_enabled).
   - Add `pub fn set_watch_command(cmd: &str)` and `pub fn get_watch_command() -> Option<String>` and `pub fn clear_watch_command()`.
   - At the end of `run_prompt()`, after the agent turn completes, check if watch mode is active AND if `SessionChanges` has new entries since the last check. If so, run the watch command via `std::process::Command` and display the output (abbreviated — show pass/fail summary, show full output only on failure).

2. **In `src/commands_project.rs`**:
   - Add `pub fn handle_watch(input: &str)` — parse `/watch [command]`:
     - `/watch` with no args: auto-detect test command (check for Cargo.toml → `cargo test`, package.json → `npm test`, etc.) and toggle on
     - `/watch cargo test -- --lib`: set a specific watch command
     - `/watch off`: disable watch mode
     - `/watch status`: show current watch state
   - Add `pub fn detect_test_command() -> Option<String>` — reuse or share logic from `/test` handler.

3. **In `src/commands.rs`**: Add `/watch` to `KNOWN_COMMANDS`.

4. **In `src/help.rs`**: Add help entry:
   ```
   /watch [command|off|status] — Auto-run tests after agent edits
   
   Usage:
     /watch              Auto-detect and enable test watching
     /watch cargo test   Watch with a specific command
     /watch off          Disable watching
     /watch status       Show current watch state
   ```

5. **Tests**:
   - `test_detect_test_command_cargo` — detects `cargo test` when Cargo.toml present
   - `test_handle_watch_off` — disabling watch mode works
   - `test_handle_watch_status` — status shows current state
   - `test_watch_in_known_commands`
   - `test_watch_in_help_text`
   - `test_set_and_get_watch_command` — round-trip the global state
   - `test_clear_watch_command` — clearing works

This makes yoyo behave more like an autonomous agent — it catches its own mistakes immediately instead of waiting for the developer to remember to run tests.
