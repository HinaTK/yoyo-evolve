Title: Make run_watch_command stream output and show partial results during /watch fix loop
Files: src/prompt.rs
Issue: none

## What

Replace the buffered `Command::new("sh").output()` in `run_watch_command()` (line 58 of `src/prompt.rs`) with a streaming approach that captures output line-by-line AND prints a live tail while the command runs, while still returning the full output string for the agent to analyze.

## Why

The `/watch` command runs a test/build command repeatedly in a fix loop. Currently `run_watch_command()` buffers all output and returns it silently — the user sees nothing while `cargo test` runs (which can take 30-60+ seconds for this project). This is especially painful during the evolution pipeline where watch-mode fix loops run for minutes with no visible progress.

This is the same class of improvement as Task 2 (streaming `/run`), applied to the watch/fix loop path. Together they close the "real-time subprocess streaming" competitive gap.

## Implementation

1. Modify `run_watch_command()` in `src/prompt.rs` (around line 58) to:
   - Spawn the process with `Stdio::piped()` for stdout and stderr
   - Read lines in real-time, collecting them into a Vec<String> for the return value
   - Print a compact live tail (last 3-5 lines) to stderr using cursor-up/overwrite, similar to how `ToolProgressTimer` shows partial output — BUT only if stdout is a terminal (check `atty::is(atty::Stream::Stderr)` or equivalent)
   - In non-terminal (piped/CI) mode, just collect silently as before
   - Return the same `(bool, String)` tuple

2. A simpler alternative (lower risk): Just print each line to stderr with a dim prefix as it arrives, without cursor tricks. Something like:
   ```rust
   // During line collection:
   if atty::is(atty::Stream::Stderr) {
       eprint!("\r{DIM}  ⟳ {line_count} lines...{RESET}");
   }
   ```
   This gives the user a progress indicator without complex terminal manipulation.

3. The function signature stays the same: `fn run_watch_command(cmd: &str) -> (bool, String)` — the full output is still collected and returned for the agent to analyze.

4. Use threads for stderr/stdout interleaving, same pattern as Task 2.

5. Add tests:
   - Test that `run_watch_command("echo hello")` returns `(true, "hello")`
   - Test that `run_watch_command("exit 1")` returns `(false, ...)` 
   - Test that output is fully captured (not lost to streaming)

## Key Decisions

- The function must still return full output — the agent needs the complete test/build output to diagnose failures
- Start with the simpler "line count progress" approach rather than full live tail (lower risk, still a big UX improvement)
- Only show progress indicator when stderr is a terminal — CI/piped mode stays clean
- Check if `std::io::stderr().is_terminal()` is available (Rust 1.70+ has `IsTerminal` trait) to avoid adding the `atty` dependency. If not, use `atty` crate or just always show the progress.
