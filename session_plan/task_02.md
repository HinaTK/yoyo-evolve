Title: Wire /bg command into REPL and help system
Files: src/repl.rs, src/help.rs, src/commands.rs
Issue: none (continuation of Task 1)

## Context

Task 1 creates `commands_bg.rs` with the background job tracker and handlers. This task
wires it into the REPL so users can actually use it.

## What to do

### 1. Create and store the BackgroundJobTracker

In `src/repl.rs`, in the `run_repl` function, create a `BackgroundJobTracker::new()` at the
start of the REPL loop (similar to how other state like `turn_history` is created). It needs
to live for the duration of the REPL session.

### 2. Add REPL dispatch

In the main match block in `run_repl` (where `/run`, `/watch`, `/test` etc. are dispatched),
add:

```rust
s if s.starts_with("/bg") => {
    commands::handle_bg(input, &bg_tracker);
}
```

Place it near the other dev/tool commands (`/run`, `/test`, `/lint`, `/watch`).

### 3. Add help text

In `src/help.rs`, add `/bg` to the command help:
- Short description: "Manage background shell processes"
- In `command_help`, add a section for "bg" with usage examples:
  ```
  /bg run <command>  — launch a command in the background
  /bg list           — show all background jobs
  /bg output <id>    — show output from a job
  /bg kill <id>      — kill a running job
  ```

### 4. Add to command completions

In `src/commands.rs`, if not already done in Task 1, ensure "bg" is in `KNOWN_COMMANDS`.
Also add subcommand completions in `command_arg_completions` for "bg": `["run", "list", "output", "kill"]`.

### 5. Verify

After wiring, the following should work in the REPL:
- `/bg` shows empty job list
- `/bg run echo hello` launches a background job and prints the ID
- `/bg list` shows the job
- `/bg output 1` shows the output
- Tab completion shows `/bg` and its subcommands

Ensure `cargo build && cargo test` passes.
