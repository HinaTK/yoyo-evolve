Title: Add terminal bell notification when agent completes a long operation
Files: src/repl.rs, src/format.rs
Issue: #167

## Context

Issue #167 was a previous attempt that reverted due to build failure. The mistake was trying to add a `bell` field to `AgentConfig` and wire it through cli.rs config parsing — too many moving parts at once. This time, use the same pattern as `disable_color()` — a simple global static.

## Implementation

1. **In `src/format.rs`**: Add a bell notification system using the same `OnceLock` pattern as color:

   ```rust
   /// Whether bell notification has been disabled (via --no-bell flag or YOYO_NO_BELL env).
   static BELL_DISABLED: OnceLock<bool> = OnceLock::new();

   /// Disable bell notifications. Call from CLI arg parsing.
   pub fn disable_bell() {
       let _ = BELL_DISABLED.set(true);
   }

   /// Check if bell is enabled. Respects YOYO_NO_BELL env var.
   pub fn bell_enabled() -> bool {
       !*BELL_DISABLED.get_or_init(|| std::env::var("YOYO_NO_BELL").is_ok())
   }

   /// Ring the terminal bell if enabled and elapsed time exceeds threshold.
   /// The bell character (\x07) causes most terminal emulators to flash the tab
   /// or play a sound, alerting multitasking developers.
   pub fn maybe_ring_bell(elapsed: std::time::Duration) {
       if bell_enabled() && elapsed.as_secs() >= 3 {
           let _ = std::io::Write::write_all(&mut std::io::stdout(), b"\x07");
           let _ = std::io::Write::flush(&mut std::io::stdout());
       }
   }
   ```

2. **In `src/repl.rs`**: After `run_prompt()` returns in the REPL loop, call `maybe_ring_bell(elapsed)` using the already-tracked duration. Look for where `run_prompt()` is called and the elapsed time is computed — it should already be measured for cost tracking. Just add the bell call.

3. **In `src/cli.rs` (parse_args only)**: Add `--no-bell` flag parsing. When encountered, call `format::disable_bell()`. Also check for `YOYO_NO_BELL` env var. Do NOT add to AgentConfig — this is a display concern like color, not an agent concern.

4. **Tests** (in `src/format.rs` test module):
   - `test_bell_enabled_default` — bell_enabled() returns true when env var not set (careful: use a unique env var name or test in isolation)
   - `test_maybe_ring_bell_short_duration_no_bell` — durations under 3s don't ring
   - `test_disable_bell_function` — after disable_bell(), bell_enabled() returns false

   **Integration test** (in `tests/integration.rs`):
   - `test_no_bell_flag_accepted` — `--no-bell` doesn't cause an error

5. **In help.rs**: Add `--no-bell` to the CLI flags section of help text.

Keep it minimal. No config file support, no AgentConfig changes. Just the flag, the env var, and the bell on long completions.
