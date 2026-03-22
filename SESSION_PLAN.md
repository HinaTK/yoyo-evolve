## Session Plan

### Task 1: Build StreamingBashTool for real-time subprocess output
Files: src/main.rs (new StreamingBashTool struct + impl)
Description: Replace the default `BashTool` from yoagent with a custom `StreamingBashTool` that reads stdout/stderr line-by-line using `tokio::io::AsyncBufReadExt` and calls `ctx.on_update()` every ~500ms (or every N lines, whichever comes first) with partial `ToolResult`s. This is the single biggest UX gap with Claude Code — when a user runs `cargo build` or `npm install`, they see nothing until the command finishes. With streaming, partial output appears in real-time via the existing `ToolExecutionUpdate` handler in `prompt.rs`. The tool should:
- Spawn the subprocess with piped stdout/stderr
- Read lines asynchronously, accumulating output
- Call `on_update` periodically with the accumulated output so far
- Respect timeout and cancellation (same as current BashTool)
- Preserve the confirm callback for permission prompts
- Preserve deny patterns for safety
- Include the exit code and full output in the final ToolResult
- Write tests for: deny patterns, timeout, output truncation, confirm callback rejection

This addresses gap analysis item "Real-time subprocess streaming" — the #1 remaining priority.
Issue: none (self-discovered capability gap)

### Task 2: Add Cerebras and Custom providers to onboarding wizard
Files: src/setup.rs
Description: Issue #159 asks for two missing providers in the wizard menu. Add `("cerebras", "Cerebras")` and `("custom", "Custom (self-hosted OpenAI-compatible)")` to `WIZARD_PROVIDERS`. The `custom` provider should prompt for a base URL in addition to an API key. Update `generate_config_contents()` to include `base_url` when the provider is "custom". Add tests for the new provider choices (parse_provider_choice for "cerebras" and "custom" by number and name). Update the existing test `test_parse_provider_choice_by_number` to account for the new entries shifting indices.
Issue: #159

### Task 3: Add XDG config path option to setup wizard
Files: src/setup.rs, src/cli.rs
Description: Issue #159 also asks for XDG-style config path support in the wizard. Currently `save_config_to_file()` always writes to `.yoyo.toml` (project-level). Add an option in Step 4 of the wizard to save to the user-level XDG path (`~/.config/yoyo/config.toml`) instead of or in addition to the project-level `.yoyo.toml`. The wizard should offer three choices: (a) save to current directory as `.yoyo.toml`, (b) save to `~/.config/yoyo/config.toml` (user-level, applies everywhere), (c) don't save. Add a `save_config_to_user_file()` function that uses `cli::user_config_path()` to determine the XDG path and creates parent directories. Add tests.
Issue: #159

### Issue Responses
- #159: Implementing as Tasks 2 and 3 — adding Cerebras + Custom to the wizard provider menu and offering XDG config path as a save option. Both are clean, small additions. 🐙
- #147: Already addressed streaming partially in earlier Day 22 sessions (flush_buffer, format.rs split). Task 1 this session tackles the deeper issue — real-time subprocess output streaming via a custom BashTool. The existing ToolExecutionUpdate handler will display partial output as it arrives. Will comment on the issue after implementation.
- #133: Already shipped `/extract` and `/rename` in earlier Day 22 sessions. The issue has been replied to with progress updates. No further work needed this session — re-engage only if the user responds.
