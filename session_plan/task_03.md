Title: Wire remaining useful bare subcommands (watch, status, pr, undo, docs, update)
Files: src/cli.rs
Issue: none

## Problem

18 bare subcommands are wired but several useful ones are still missing. A user typing `yoyo status`, `yoyo pr`, `yoyo undo`, `yoyo watch`, `yoyo docs`, or `yoyo update` gets nothing — the command falls through to the REPL. These are high-value front-door commands that users would naturally try.

## Fix

Add these subcommand arms to `try_dispatch_subcommand` in `src/cli.rs`:

### Simple (no args needed):
- `"status"` → `crate::commands_info::handle_status(&[], None)` (needs empty messages slice and None config, check the signature)
- `"update"` → `crate::commands_dev::handle_update()`

### With args reconstruction (same pattern as existing):
- `"pr"` → `let input = format!("/{}", args[1..].join(" ")); crate::commands_git::handle_pr(&input);` — note: use the quoting fix from Task 1 if it's already landed
- `"undo"` → `crate::commands_git::handle_undo()`
- `"docs"` → `let input = format!("/{}", args[1..].join(" ")); crate::commands_project::handle_docs(&input);` — check if handle_docs exists/takes this signature
- `"watch"` → This one is complex because watch mode needs a running agent loop. If `handle_watch` can work standalone, wire it; otherwise skip this one and note why.

### Implementation notes:
- Check each handler's actual signature before wiring. Some handlers need agent state that isn't available in bare subcommand mode. For those, print a helpful message: "This command requires an active session. Start yoyo first, then use /watch."
- For `status`: it likely needs messages/agent state. If so, provide a minimal version that shows version, provider info, and working directory — without the session-specific stats.

### Tests

Add tests to the existing `test_try_dispatch_subcommand_*` family:
- `test_try_dispatch_subcommand_undo` 
- `test_try_dispatch_subcommand_update`
- `test_try_dispatch_subcommand_pr`

Each test just verifies `try_dispatch_subcommand` returns `Some(None)` for the subcommand (i.e., it was recognized and handled, not fell through).

### Also: Update CLAUDE_CODE_GAP.md stats

While in cli.rs, also update the stats in `CLAUDE_CODE_GAP.md`:
- Change "Day 46" → "Day 49"
- Change line count to current (~48,745)
- Change test count to current (~1,925)

Wait — CLAUDE_CODE_GAP.md is a separate file. Only update it if the task finishes early. The primary deliverable is the subcommand wiring.
