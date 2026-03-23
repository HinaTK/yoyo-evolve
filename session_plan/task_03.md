Title: Add tool execution audit log to .yoyo/audit.jsonl
Files: src/main.rs, src/format.rs
Issue: #21

Add a lightweight audit log that records every tool execution to `.yoyo/audit.jsonl`. This is the simplest useful piece of Issue #21 (hook system), stripped down to avoid the complexity that caused #162 to revert.

**Why this matters:** When the agent makes changes, users need to understand what happened — especially when something goes wrong. An audit trail is the foundation for debugging agent behavior. It's also a prerequisite for more advanced features like replay and cost analysis.

**Previous attempt (#162) failed because:** It tried to build a full hook trait system with pre/post hooks, deny patterns, timing hooks, and hook ordering — all at once. Too many moving parts, tests failed.

**This attempt is minimal:** Just log tool calls. No hooks, no traits, no configuration beyond a single flag.

**Implementation:**

1. **Audit log writer** in `src/main.rs` (or a small helper):
   - `AuditLogger` struct with an optional file handle (None when disabled)
   - `fn log_tool_call(&mut self, tool_name: &str, args: &serde_json::Value, duration: Duration, success: bool)`
   - Each entry is a single JSON line: `{"ts":"2026-03-23T09:50:00Z","tool":"bash","args":{"command":"ls"},"duration_ms":42,"success":true}`
   - File is opened lazily on first write, appended to (not overwritten)
   - Path: `.yoyo/audit.jsonl`
   - Directory `.yoyo/` created if needed

2. **Wire into event handling** in `src/main.rs`:
   - In the `StreamEvent::ToolResult` handler (where tool results are already processed), extract the tool name, args, and success status
   - Call `audit_logger.log_tool_call(...)` if auditing is enabled
   - Use the existing `tool_start_time` tracking to compute duration

3. **CLI flag**: Add `--audit` flag to `src/cli.rs`:
   - `pub audit_log: bool` in the config struct
   - Parse `--audit` from args
   - Also support `audit = true` in `.yoyo.toml` config file

4. **Show audit status** in `/status` or `/config` output when enabled.

5. **Tests:**
   - `test_audit_logger_disabled_by_default` — AuditLogger::new(false) produces no file
   - `test_audit_logger_writes_valid_jsonl` — create temp file, log a call, verify JSON parses
   - `test_audit_logger_appends` — log two calls, verify both lines exist
   - `test_audit_log_entry_fields` — verify all expected fields are present
   - `test_audit_flag_in_config` — verify --audit is parsed correctly

**Scope constraints:**
- No pre/post hooks
- No hook traits or extensibility
- No filtering or configuration of what gets logged
- No reading/querying the audit log (that's a future feature)
- Just write JSONL on every tool execution when --audit is enabled
