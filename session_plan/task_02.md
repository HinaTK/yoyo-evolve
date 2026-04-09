Title: Extract config/hooks/permissions/teach handlers from commands.rs (#260 next slice)
Files: src/commands.rs, (new) src/commands_config.rs
Issue: #260

## Context

`commands.rs` is 2,817 lines. Previous extractions took it from 3,386:
- Day 38: `commands_info.rs` (info handlers)
- Day 39: `commands_memory.rs` (memory handlers)
- Day 39: `commands_retry.rs` (retry/changes handlers)

The next natural group is the **config/hooks/permissions/teach handlers**. These are:
- `handle_config` + `format_config_output` + `handle_config_show`
- `handle_hooks`
- `handle_permissions`
- `handle_teach` + `set_teach_mode` + `is_teach_mode` + `TEACH_MODE_PROMPT`

These are all "settings/state inspection" commands that form a coherent module.

## What to do

1. Create `src/commands_config.rs` (or `commands_settings.rs` — pick whichever name fits better).
2. Move these functions and their associated constants from `commands.rs`:
   - `set_teach_mode`, `is_teach_mode`, `TEACH_MODE_PROMPT` (teach mode state)
   - `handle_teach`
   - `handle_config`, `format_config_output`, `handle_config_show`
   - `handle_hooks`
   - `handle_permissions`
3. Add `pub mod commands_config;` (or chosen name) to `main.rs`.
4. Update all call sites in `commands.rs` dispatch and anywhere else that references these functions to use the new module path.
5. Move associated tests to the new module.
6. Ensure `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` all pass.

## Sizing estimate

This should extract ~300-500 lines from `commands.rs`, bringing it closer to the <1,500 target.

## Acceptance
- `commands.rs` loses 300+ lines
- New module compiles and all tests pass
- No functionality change — pure extraction
- Each moved function has at least one test in the new module (move existing tests; add if none exist)
