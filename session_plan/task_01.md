Title: Wire up --audit flag and YOYO_AUDIT env var (fix dead audit system)
Files: src/cli.rs, src/main.rs
Issue: none

The audit logging system exists in `prompt.rs` and `hooks.rs` but can never be activated
because `enable_audit_log()` is never called. The `--audit` flag and `YOYO_AUDIT=1` env var
are documented in comments but never implemented in CLI parsing.

This is a real bug: the audit system was built (Day 24) but the activation path was never wired up.

**What to do:**

1. In `src/cli.rs`:
   - Add `--audit` to `KNOWN_FLAGS` list (around line 615)
   - Add `audit: bool` field to `Config` struct (around line 345)
   - In `parse_args()`, check for `--audit` flag OR `YOYO_AUDIT=1` env var OR `audit = true` in config file
   - Set `config.audit = true` when any of these are present
   - Add `--audit` to `print_help()` output under the appropriate section

2. In `src/main.rs`:
   - After config is parsed, if `config.audit` is true, call `prompt::enable_audit_log()`
   - This should happen early in `main()`, before `build_agent()` is called
   - The existing `is_audit_enabled()` call in `build_tools()` will then work correctly

3. Remove the `#[allow(dead_code)]` from `enable_audit_log()` in `prompt.rs` since it will now be called.
   Wait — that's a 3rd file. Instead, just note that removing the dead_code annotation from
   `enable_audit_log` can be done in task 2 which already touches prompt.rs.

4. Add a test in `cli.rs` that verifies `--audit` flag is parsed correctly.

This fixes a genuine feature gap where the audit system was built but unreachable.
