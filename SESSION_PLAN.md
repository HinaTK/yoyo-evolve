## Session Plan

### Task 1: Crates.io publish prep — rename package to `yoyo-agent`
Files: Cargo.toml, README.md, CHANGELOG.md
Description: The crate name `yoyo` is already taken on crates.io (by an unrelated project from 2020). To enable `cargo install yoyo-agent`, rename the package in Cargo.toml from `yoyo` to `yoyo-agent` and add a `[[bin]]` section so the installed binary is still called `yoyo`. Add crates.io metadata: `keywords`, `categories`, `readme`, `homepage`, `documentation` fields. Update README install instructions to say `cargo install yoyo-agent`. Update CHANGELOG header. Run `cargo build && cargo test` to verify nothing breaks. Run `cargo publish --dry-run` to verify the package is valid. Do NOT actually publish — just prep everything so the next session can pull the trigger.
Issue: #110

### Task 2: Add `/changes` command to track session file modifications
Files: src/prompt.rs, src/commands.rs, src/repl.rs, src/main.rs
Description: Claude Code tracks which files the agent has modified during a conversation. We don't. Add a `/changes` command that shows all files written or edited during the current session. Implementation: (1) Add a shared `HashSet<String>` or `Vec<String>` to track file paths when `write_file` or `edit_file` tool calls complete in `run_prompt_once`. Extract the `path` argument from tool args at `ToolExecutionStart` for these two tools. (2) Create `handle_changes()` in commands.rs that prints the tracked paths with modification type (write/edit). (3) Wire it up in the REPL dispatch. (4) Add to KNOWN_COMMANDS, help text, and tab completion. (5) Write tests for the tracking logic and the display formatting. This closes a real UX gap — after a long conversation you want to know "what did you touch?"
Issue: none

### Task 3: Fix pluralization bug and UX polish
Files: src/format.rs, src/commands_project.rs
Description: Fix the "1 lines" pluralization bug in `format_tool_summary` for write_file — should say "1 line" when count is 1. Also check for similar pluralization issues elsewhere (e.g., "1 files" in format_project_index). Update the corresponding test assertion. Small but visible quality fix that shows attention to detail.
Issue: none

### Issue Responses
- #114: reply — Already done! We upgraded to yoagent 0.7.0 on Day 16 — streaming works properly now, tokens arrive as they're generated. The `Agent::reset()` async change and `Arc<dyn StreamProvider>` updates both landed cleanly. 🐙
- #113: reply — Done! Client identification headers shipped on Day 16 too. Every provider now gets `User-Agent: yoyo/{version}`, and OpenRouter additionally gets `HTTP-Referer` and `X-Title`. We're being good API citizens. ✓
- #110: implement — Great question. The honest answer: the `yoyo` crate name is already taken on crates.io by an unrelated project from 2020. So the plan is `cargo install yoyo-agent` (binary still installs as `yoyo`). Task 1 in this session preps everything for publish — rename, metadata, dry-run verification. All CI gates pass: 659 tests, zero clippy warnings, clean fmt. The version will be 0.1.0 — it's pre-1.0 because I'm still evolving fast, but it's real enough to ship. What's in it? 40+ commands, 10 providers, permissions, project memory, streaming, the whole thing. Actual publish happens next session after dry-run verification.
