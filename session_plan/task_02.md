Title: Make /run stream output line-by-line instead of buffering
Files: src/commands_dev.rs
Issue: none

## What

Replace the buffered `Command::new("sh").output()` in `run_shell_command()` (used by `/run`, `/test`, `/lint`) with a streaming approach that prints stdout and stderr line-by-line as the subprocess produces them.

## Why

Currently, `/run cargo build`, `/test`, and `/lint` all call `run_shell_command()` which buffers the entire output and prints it only after the process exits. For long-running commands (build, test suite, lint), the user sees nothing for seconds or minutes, then a wall of text. Claude Code streams subprocess output in real-time. This is competitive gap #3 from CLAUDE_CODE_GAP.md.

This is a direct UX improvement that makes yoyo feel more responsive and professional.

## Implementation

1. Modify `run_shell_command()` in `src/commands_dev.rs` (around line 1127) to:
   - Spawn the process with `Command::new("sh").args(["-c", cmd]).stdout(Stdio::piped()).stderr(Stdio::piped()).spawn()`
   - Read stdout and stderr in real-time using `BufRead::lines()` on piped handles
   - Print each line as it arrives (stdout normal, stderr in red)
   - Use threads or `select` to interleave stdout and stderr (a simple approach: spawn a thread for stderr that prints lines as they come, read stdout on the main thread)
   - Still track the exit code and elapsed time for the summary line

2. A simple and robust approach:
   ```rust
   use std::process::{Command, Stdio};
   use std::io::{BufRead, BufReader};
   
   let mut child = Command::new("sh")
       .args(["-c", cmd])
       .stdout(Stdio::piped())
       .stderr(Stdio::piped())
       .spawn()
       .map_err(|e| format!("error running command: {e}"))?;
   
   // Spawn thread for stderr
   let stderr = child.stderr.take().unwrap();
   let stderr_handle = std::thread::spawn(move || {
       let reader = BufReader::new(stderr);
       for line in reader.lines().flatten() {
           eprintln!("{RED}{line}{RESET}");
       }
   });
   
   // Read stdout on main thread
   let stdout = child.stdout.take().unwrap();
   let reader = BufReader::new(stdout);
   for line in reader.lines().flatten() {
       println!("{line}");
   }
   
   stderr_handle.join().ok();
   let status = child.wait();
   ```

3. Keep the existing exit code + elapsed time summary at the end.

4. Add tests:
   - Test that `run_shell_command` with a simple echo works (output appears)
   - Test that a failing command shows the exit code
   - Since streaming is hard to test directly, focus on correctness of the final state (exit code, that the function doesn't panic)

5. The functions `handle_test`, `handle_lint`, and `handle_run` all delegate to `run_shell_command`, so they all benefit automatically.

## Key Decisions

- Use `Stdio::piped()` + `BufReader::lines()` for line-by-line streaming
- Use a thread for stderr to avoid blocking on either pipe
- Keep the summary line at the end for consistency with current behavior
- Don't change the function signature — it's `fn run_shell_command(cmd: &str)` and callers don't need to change
