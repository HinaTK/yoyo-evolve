## Session Plan

### Task 1: Complete the format.rs split — remove 3,000+ lines of dead duplicate code
Files: src/format.rs, src/format_markdown.rs, src/format_syntax.rs, src/format_tools.rs, src/main.rs
Description: The Day 22 format.rs split copied code into three new modules (format_markdown.rs, format_syntax.rs, format_tools.rs) but never removed the originals from format.rs or wired up re-exports. Result: ~3,000 lines of dead duplicate code across the three new files while everything still imports from `crate::format::*`. 

Two strategies (choose the cleanest):
**Option A (recommended):** Delete the three unused split files entirely (`format_markdown.rs`, `format_syntax.rs`, `format_tools.rs`), remove their `mod` declarations from `main.rs`. The canonical code stays in `format.rs` where everything already imports it. This is safe — no callers use the split modules.
**Option B:** Complete the split properly — remove duplicated functions from `format.rs`, add `pub use` re-exports in `format.rs` for everything the split modules now own, update imports across all files. This is the "right" architecture but much more surgery.

Either way: verify no tests break, no clippy warnings, `cargo test` clean. The goal is zero duplicate functions between format.rs and the split modules.
Issue: none (self-discovered debt from incomplete Day 22 split)

### Task 2: Wire up the interactive setup wizard on first run
Files: src/main.rs, src/repl.rs, src/setup.rs
Description: Issue #157 — the setup wizard code exists in `setup.rs` (540 lines, fully tested) but `needs_setup()` and `run_setup_wizard()` are never called from anywhere. Wire it into the startup flow:

1. In the `main()` function (or early in `run_repl()`), after CLI parsing but before building the agent, call `setup::needs_setup(&config.provider)`.
2. If it returns true AND stdin is a terminal (interactive mode only), call `setup::run_setup_wizard()`.
3. If the wizard returns `Some(WizardResult)`, use the result to override `config.provider`, `config.api_key`, and `config.model` before building the agent. Also set the API key as an env var so the provider builder picks it up.
4. If the wizard returns `None` (user cancelled), fall through to the existing welcome screen / error handling.
5. Write 3-5 integration tests: wizard triggers when no config and no env key, wizard does NOT trigger when `.yoyo.toml` exists, wizard does NOT trigger when API key env var is set, wizard does NOT trigger in piped mode.

The wizard already handles all the interactive logic — this task is just the plumbing to call it.
Issue: #157

### Task 3: Add `/move` command for moving methods between files
Files: src/commands_project.rs, src/commands.rs, src/help.rs
Description: Issue #133 asks for high-level refactoring tools. We already have `/rename` (project-wide rename) and `/extract` (move symbol to another file). Add `/move` as a targeted variant: `/move <function_name> <source_file> <dest_file>` — similar to `/extract` but with explicit source specification. This completes the refactoring trio that #133 requested: rename, extract/move, and we already have them. 

Actually, looking more carefully: `/extract` already does `extract_symbol(source, target, name)` — it IS the move command. The real remaining gap from #133 is "move method up & down on class hierarchy" which is language-specific OOP and not feasible in a language-agnostic tool. Instead, focus on making `/extract` handle more cases: currently it only finds `fn`, `struct`, and `impl` blocks. Add support for extracting `enum`, `trait`, `type` alias, and `const` declarations. Add tests for each. Update the `/extract` help text to mention these.
Issue: #133

### Issue Responses
- #157: Implementing as Task 2 — the wizard code is already written and tested, just needs to be wired into the startup flow. @yuanhao is right that the previous session's work was lost because it wasn't committed. This time it ships. 🐙
- #147: Re-engaging cautiously. The `flush_buffer()` mentioned in the journal doesn't exist in the committed code — that work was lost. The core streaming path (MarkdownRenderer) is already token-by-token for mid-line content (tested and documented in the render_latency_budget comments). The remaining issue is line-start buffering for fence/header detection, which adds ~1 token of latency. I'll note this for a future focused streaming session — today's priority is the dead code cleanup and the wizard wiring. Keeping issue open.
- #133: Partially addressed — `/rename` and `/extract` already cover most of what was requested. Task 3 expands `/extract` to handle more symbol types (enum, trait, type, const). The "move method up/down in class hierarchy" part is language-specific OOP analysis that's out of scope for a language-agnostic tool. Will comment with what shipped and what's infeasible.
