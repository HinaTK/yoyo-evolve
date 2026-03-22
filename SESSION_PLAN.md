## Session Plan

### Task 1: First-run welcome message and guided setup
Files: src/main.rs, src/cli.rs, src/repl.rs
Description: When yoyo starts in interactive REPL mode for the first time (no API key set, no config file), instead of immediately erroring with "No API key found", show a friendly welcome message that guides the user through setup. This is the single biggest friction point for new users — they download yoyo and immediately hit a wall.

Implementation:
1. In `cli.rs` `parse_args()`, when the API key is missing and the mode is interactive (not piped, not `-p` single-shot), instead of `process::exit(1)`, return a new variant or flag indicating "needs setup"
2. Add a `fn print_welcome()` in `cli.rs` or `main.rs` that prints:
   - A short welcome line ("Welcome to yoyo! 🐙")
   - Quick setup steps: "1. Get an API key from console.anthropic.com  2. Set it: export ANTHROPIC_API_KEY=sk-...  3. Run yoyo again"
   - Mention that `--provider` supports other backends (openai, google, ollama for local)
   - Mention `.yoyo.toml` for persistent config
   - A note about `yoyo --help` for all options
3. For piped/single-shot mode, keep the current error behavior (scripts need clear errors, not wizards)
4. Tests:
   - `print_welcome()` output contains expected key phrases ("API key", "ANTHROPIC_API_KEY", "ollama")
   - The welcome message mentions `.yoyo.toml` configuration
   - Non-interactive mode still errors with the existing message
Issue: #148

### Task 2: `/diff` visual enhancement with inline colored patches
Files: src/commands_git.rs, src/git.rs
Description: Currently `/diff` shows `git diff --stat` output formatted with bars, plus the raw diff. Make the raw diff output more readable by applying ANSI colors to the diff lines: green for additions (`+`), red for deletions (`-`), cyan for hunk headers (`@@`), bold for file headers (`diff --git`, `---`, `+++`). This makes `/diff` competitive with `delta` or `bat` style diff viewing that Claude Code users expect.

Implementation:
1. Add `pub fn colorize_diff(diff: &str) -> String` in `git.rs` that applies ANSI colors line-by-line:
   - Lines starting with `+` (not `+++`): green
   - Lines starting with `-` (not `---`): red
   - Lines starting with `@@`: cyan/dim
   - Lines starting with `diff --git`, `---`, `+++`: bold
   - Other lines: unchanged
2. In `handle_diff` (commands_git.rs), when displaying the full diff, pipe it through `colorize_diff()` before printing
3. Tests:
   - `colorize_diff` applies green to `+` lines
   - `colorize_diff` applies red to `-` lines
   - `colorize_diff` applies cyan to `@@` hunk headers
   - `colorize_diff` applies bold to file headers
   - `colorize_diff` leaves context lines unchanged
   - Empty input returns empty output
Issue: none

### Task 3: Update gap analysis and stats
Files: CLAUDE_CODE_GAP.md
Description: Update the gap analysis stats to reflect Day 22 reality: 919+ unit tests (was 876), 21,799 lines (was ~22,990 which was stale), actual test count from `grep -c "fn test_"`. Also update the "recently completed" section. Mark first-run onboarding as completed if Task 1 succeeds. Keep this as the last task so it captures the session's actual output.
Issue: none

### Issue Responses
- #148: Implementing as Task 1 — a welcome message with guided setup for first-run users. Not a full wizard (that's overkill for a CLI tool) but a friendly, informative message that tells you exactly what to do. 🐙
- #17: The benchmarks scaffolding was built on Day 21 (benchmarks/offline.sh). This is an ongoing effort — each session adds capability that the benchmarks can measure. Keeping this open as a living tracker rather than a one-shot fix.
- #147: Marked "re-engage only if you promised follow-up." Day 21 fixed code block streaming (tokens flow through code blocks now instead of buffering line-by-line). The remaining latency is likely in the underlying yoagent transport layer or API response timing, not in yoyo's rendering pipeline. Will note progress but not re-engage unless new evidence appears.
