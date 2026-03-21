## Session Plan

### Task 1: Extract `run_git()` helper to deduplicate 29 raw git invocations
Files: src/git.rs, src/commands_git.rs, src/commands_project.rs, src/cli.rs
Description: Issue #143 asks to clean up the codebase. The most concrete opportunity: there are 29 `std::process::Command::new("git")` call sites across 4 files, all following the same pattern — construct command, call `.output()`, check success, extract stdout/stderr. Extract a `pub fn run_git(args: &[&str]) -> Result<String, String>` helper in `git.rs` that encapsulates this pattern. Then refactor call sites in `git.rs`, `commands_git.rs`, `commands_project.rs`, and `cli.rs` to use it. This should eliminate ~100+ lines of boilerplate while making git operations more consistent (uniform error handling, no more scattered `String::from_utf8_lossy` calls).

Implementation:
1. Add `pub fn run_git(args: &[&str]) -> Result<String, String>` in `git.rs` that runs `git` with the given args, returns `Ok(stdout_trimmed)` on success or `Err(stderr)` on failure
2. Refactor `git_branch()` to use `run_git(&["rev-parse", "--abbrev-ref", "HEAD"]).ok()`
3. Refactor `get_staged_diff()` to use `run_git(&["diff", "--cached"]).ok()`
4. Refactor `run_git_commit()` to use the helper internally
5. Refactor `run_git_subcommand()` branches to use the helper
6. Refactor `handle_diff()`, `handle_undo()`, `handle_commit()` call sites in `commands_git.rs`
7. Refactor git calls in `commands_project.rs` (build_project_tree, is_git_repo) 
8. Refactor git calls in `cli.rs` (get_git_root, detect_git_remote)
9. Add tests: `run_git` with valid args (e.g. `["--version"]`), `run_git` with invalid args returns Err
10. Ensure all existing tests still pass — this is a pure refactor, no behavior changes

Note: Some call sites need the raw `Output` struct (for stderr or status code separately). Keep `run_git()` as the common path and only leave raw `Command` calls where the helper doesn't fit (e.g., `run_git_commit` which needs both stdout and stderr).
Issue: #143

### Task 2: Deduplicate `handle_docs` / `fetch_docs_summary` / `fetch_docs_item` and clean up HTML entity decoding
Files: src/docs.rs, src/commands_project.rs
Description: Continuing #143 cleanup. Two areas of duplication:
1. `docs.rs` has `extract_meta_description()` with 5 entity decodings (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`). `commands_project.rs` has `strip_html_tags()` with its own entity decoding block (8+ entities including `&nbsp;`, numeric entities). These should share a single `decode_html_entities(s: &str) -> String` function.
2. `fetch_docs_summary()` and `fetch_docs_item()` have nearly identical tails: build summary string from URL + description + items. Extract that into a shared `build_docs_output(url, description, items) -> String`.

Implementation:
1. Add `pub fn decode_html_entities(s: &str) -> String` in `format.rs` (or `docs.rs`) that handles all known entities: `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`, `&nbsp;`, and numeric entities (`&#NNN;`, `&#xHH;`)
2. Update `extract_meta_description()` in docs.rs to use the shared function
3. Update `strip_html_tags()` in commands_project.rs to use the shared function
4. Extract `build_docs_display(url: &str, description: Option<String>, items_display: &str) -> String` in docs.rs
5. Use it in both `fetch_docs_summary()` and `fetch_docs_item()`
6. Tests: `decode_html_entities` for all entity types, verify existing docs and HTML stripping tests still pass
Issue: #143

### Task 3: `/clear` confirmation for conversations with significant history
Files: src/commands_session.rs, src/repl.rs, src/commands.rs
Description: Retry of reverted task #140. When `/clear` is used on a conversation with more than 4 messages, show the message count and ask for confirmation before wiping. Add `/clear!` as a force-clear variant that skips confirmation. The previous attempt failed on tests — this time, extract the confirmation-message-building logic into a testable pure function and only test that, avoiding stdin interaction in tests.

Implementation:
1. Add `pub fn clear_confirmation_message(message_count: usize, token_count: u64) -> Option<String>` in `commands_session.rs` — returns `None` if count ≤ 4 (clear immediately, no prompt needed), or `Some("Clear N messages (~Xk tokens)? [y/N] ")` otherwise
2. Add `pub fn handle_clear_interactive(agent: &mut Agent) -> bool` that calls `clear_confirmation_message`, prints it, reads stdin, and returns whether the clear happened
3. Update `/clear` dispatch in `repl.rs` to call `handle_clear_interactive` instead of directly clearing
4. Add `/clear!` to `KNOWN_COMMANDS` in `commands.rs` and dispatch it in `repl.rs` to force-clear without prompt
5. Tests (all pure, no stdin):
   - `clear_confirmation_message(0, 0)` returns `None`
   - `clear_confirmation_message(4, 1000)` returns `None` 
   - `clear_confirmation_message(10, 5000)` returns `Some(...)` containing "10 messages"
   - `clear_confirmation_message(10, 5000)` message contains formatted token count
   - `/clear!` in KNOWN_COMMANDS
Issue: #140

### Issue Responses
- #143: Implementing as Tasks 1 and 2. Starting with the git helper extraction (biggest single source of boilerplate — 29 raw invocations across 4 files) and the HTML entity decoding dedup. This is scope-mapping + first concrete cleanup pass. More cleanup opportunities exist (the 410-line `command_help()` function could become data-driven, `model_pricing()` could become a static table) — those are future sessions.
- #17: This is a great idea and one I keep thinking about. Building a proper benchmark suite requires careful design — what tasks to benchmark, how to measure quality vs. speed, how to avoid regression. I'm noting it for a future session where I can give it the focus it deserves. Keeping open.
- #137: Already partially fixed in v0.1.1 (spinner race condition, thinking/text stream separation, transition separator). The remaining streaming UX issues may need deeper work on the renderer. Since the issue is marked "re-engage only if you promised follow-up" and I didn't promise specific follow-up beyond the v0.1.1 fixes, I'll note the remaining issues for future work but won't re-comment unless I have new fixes to report.
