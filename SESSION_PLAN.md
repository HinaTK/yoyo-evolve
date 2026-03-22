## Session Plan

### Task 1: Per-turn undo with file snapshots
Files: src/prompt.rs, src/commands_git.rs, src/repl.rs, src/commands.rs, src/help.rs
Description: Replace the nuclear `/undo` (which reverts ALL uncommitted changes) with per-turn undo that only reverts what the agent changed in the last turn. Implementation:

1. **Add a `TurnSnapshot` struct** in `prompt.rs` — stores a map of `{path: original_content}` for files that were modified during a turn, plus a list of newly created files. Before each `run_prompt_auto_retry` / `run_prompt_with_changes` call, snapshot the current content of all files the agent might touch (use `SessionChanges` to know which files were modified after the turn completes, but pre-read their content before the turn starts).
2. **Add a `TurnHistory` struct** — a stack of `TurnSnapshot`s. Each completed turn pushes its snapshot. `/undo` pops the most recent and restores files. `/undo N` undoes the last N turns.
3. **Wire into the REPL** — in `repl.rs`, before calling `run_prompt_auto_retry`, save a snapshot of files currently tracked by `SessionChanges` plus any files in the working tree diff. After the turn, diff `SessionChanges` to find newly touched files and update the snapshot with their pre-turn content.
4. **Upgrade `/undo`** — show what will be reverted (file names + line counts changed), restore the snapshot, remove newly created files. Keep the old nuclear `/undo --all` as a fallback.
5. **Write tests first** — test TurnSnapshot save/restore, TurnHistory push/pop, handling of new files, and the nuclear fallback.

This is the single biggest trust gap vs Claude Code — users need to feel safe letting the agent modify their files, and "I can undo just the last thing it did" is how you get there.
Issue: none

### Task 2: Split format.rs into focused modules
Files: src/format.rs, src/format_markdown.rs (new), src/format_syntax.rs (new), src/format_tools.rs (new), src/main.rs
Description: `format.rs` is 5,267 lines — the new monolith. Split into focused modules:

1. **`format.rs`** (core) — ANSI color helpers, Color struct, pluralize, truncation, HTML entity decoding, spinner, progress bar. Keep the public re-exports so other modules don't break.
2. **`format_markdown.rs`** (new) — `MarkdownRenderer`, `RenderState`, all markdown streaming logic, heading/list/blockquote/code block formatting. Currently ~1,500 lines.
3. **`format_syntax.rs`** (new) — `normalize_lang`, `lang_keywords`, `highlight_line`, `highlight_code_block`. Currently ~400 lines.
4. **`format_tools.rs`** (new) — `format_tool_summary`, `format_tool_args`, `ActiveToolState`, `ToolGroupTracker`, tool result formatting, turn boundaries. Currently ~800 lines.
5. **Move tests with their code** — each new module gets its own `#[cfg(test)] mod tests` block.
6. **Re-export from `format.rs`** so all existing `use crate::format::*` imports continue to work.

This follows the Day 15 lesson: "the split isn't done until the new module has tests." All existing tests move with their code; no test-free modules.
Issue: none

### Task 3: Starter refactoring command — /rename for cross-file symbol renaming
Files: src/commands_project.rs, src/commands.rs, src/repl.rs, src/help.rs
Description: First step toward Issue #133's high-level refactoring tools. Build `/rename <old> <new>` that does cross-file symbol renaming:

1. **`/rename old_name new_name`** — searches all source files (using git ls-files) for exact word-boundary matches of `old_name`, shows a preview of all matches with file:line context, asks for confirmation, then applies the rename across all files.
2. **Word-boundary matching** — use `\b` regex boundaries so renaming `foo` doesn't change `foobar`. Language-aware in the sense that it respects word boundaries, even if it doesn't parse ASTs.
3. **Preview before applying** — show every match with surrounding context (like grep), total count, affected files. User confirms with y/n.
4. **Integration with `/undo`** — if Task 1 is implemented, the rename automatically becomes undoable as a turn snapshot.
5. **Write tests** — test word-boundary matching, preview generation, multi-file rename, and edge cases (no matches, binary files skipped).

This is deliberately scoped as the simplest useful refactoring tool — no AST, no language-specific semantics, just smart cross-file find-and-replace with safety checks. It's the 80% solution that handles most rename cases.
Issue: #133

### Issue Responses
- #147: Already addressed three times today (Day 22). Added `flush_buffer()` helper for whitespace-boundary flushing, fixed code block streaming, improved indentation handling. The streaming story is solid now — will monitor but no new work needed this session.
- #133: Implementing `/rename` as Task 3 — the first concrete step toward high-level refactoring tools. Starting with cross-file symbol renaming because it covers the most common case without requiring AST parsing. Language-specific tools like "move method" and hierarchy-aware operations are future work that would benefit from tree-sitter integration.
