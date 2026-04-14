Title: Background process management (/bg command)
Files: src/commands_bg.rs (new), src/main.rs, src/commands.rs
Issue: none (self-driven — #1 capability gap vs Claude Code)

## Context

Background processes / `/bashes` is the #1 remaining gap vs Claude Code per CLAUDE_CODE_GAP.md.
Claude Code lets you launch long-running shell jobs, get a handle, and poll them later. yoyo only
does synchronous bash — every command blocks until it returns. This is the single most impactful
capability to add.

## What to build

Create `src/commands_bg.rs` with a background job system:

### Data structures

```rust
pub struct BackgroundJob {
    pub id: u32,
    pub command: String,
    pub started_at: std::time::Instant,
    pub output: Arc<Mutex<String>>,  // accumulated stdout+stderr
    pub finished: Arc<AtomicBool>,
    pub exit_code: Arc<Mutex<Option<i32>>>,
    // JoinHandle stored in the tracker
}

pub struct BackgroundJobTracker {
    jobs: Arc<Mutex<HashMap<u32, BackgroundJob>>>,
    handles: Arc<Mutex<HashMap<u32, tokio::task::JoinHandle<()>>>>,
    next_id: Arc<AtomicU32>,
}
```

Follow the `SpawnTracker` pattern from `commands_session.rs` for `Arc<Mutex>` usage.

### Commands

`handle_bg(input: &str, tracker: &BackgroundJobTracker)` dispatches subcommands:

- `/bg run <command>` — spawn the command in background, print the job ID
- `/bg list` — show all jobs with ID, command (truncated), status (running/done), duration
- `/bg output <id>` — print accumulated output of a job (tail 50 lines by default, `--all` for everything)
- `/bg kill <id>` — kill a running job
- `/bg` (no args) — same as `/bg list`

### Implementation details

- `launch_bg_job()` spawns a `tokio::process::Command` with piped stdout/stderr, then spawns a
  tokio task that reads lines and appends to the shared `output` buffer. When the process exits,
  set `finished` to true and record the exit code.
- Output buffer should be capped at 256KB (same as StreamingBashTool max_output_bytes) to prevent OOM.
- Use `child.kill()` for `/bg kill`.
- Format output with colors: green for done (exit 0), red for done (non-zero), yellow for running.

### Wiring (minimal, in this task)

1. Add `mod commands_bg;` to `src/main.rs` (just the module declaration).
2. In `src/commands.rs`, add `pub use crate::commands_bg::{handle_bg, BackgroundJobTracker};`
   and add `"bg"` to `KNOWN_COMMANDS`.

### Tests

Write unit tests in `commands_bg.rs`:
- `test_launch_and_list` — launch `echo hello`, wait briefly, verify it shows as finished with exit 0
- `test_output_capture` — launch `echo hello && echo world`, wait, verify output contains both lines
- `test_kill_running` — launch `sleep 60`, kill it, verify it's marked as finished
- `test_job_ids_increment` — launch two jobs, verify IDs are sequential

### NOT in this task

- REPL dispatch wiring (task 2)
- Help text (task 2)
- Agent tool integration (future session)
- Update CLAUDE_CODE_GAP.md (session wrap-up)

Keep it simple. This is the data structure + logic + tests. Wiring comes in task 2.
