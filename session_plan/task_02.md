Title: Add audit log for tool executions
Files: src/main.rs, src/prompt.rs, src/cli.rs, src/help.rs, src/commands.rs
Issue: #21

## Context

Issue #21 asks for a hook architecture for tool execution. The full pre/post hook system (Issue #162) has failed twice — too complex. This task implements the simplest useful piece: an audit log that records every tool call to `.yoyo/audit.jsonl` for debugging and transparency. This gives users visibility into what the agent did during long sessions, which is valuable for trust and debugging.

## Implementation

### 1. Audit log writer in `src/prompt.rs`

Add a simple audit logger:

```rust
use std::io::Write;

/// Write a tool execution record to `.yoyo/audit.jsonl`.
/// Each line is a JSON object: {"ts": "...", "tool": "...", "args": {...}, "duration_ms": N, "success": bool}
/// Silently does nothing if the audit directory doesn't exist or writing fails.
pub fn audit_log_tool_call(
    tool_name: &str,
    args: &serde_json::Value,
    duration_ms: u64,
    success: bool,
) {
    if !is_audit_enabled() {
        return;
    }
    let _ = write_audit_entry(tool_name, args, duration_ms, success);
}

fn is_audit_enabled() -> bool {
    AUDIT_ENABLED.load(std::sync::atomic::Ordering::Relaxed)
}

static AUDIT_ENABLED: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

pub fn enable_audit_log() {
    AUDIT_ENABLED.store(true, std::sync::atomic::Ordering::Relaxed);
}

fn write_audit_entry(
    tool_name: &str,
    args: &serde_json::Value,
    duration_ms: u64,
    success: bool,
) -> std::io::Result<()> {
    let dir = std::path::Path::new(".yoyo");
    std::fs::create_dir_all(dir)?;
    let path = dir.join("audit.jsonl");
    let mut file = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(&path)?;

    // Get current timestamp
    let ts = std::process::Command::new("date")
        .arg("+%Y-%m-%dT%H:%M:%S")
        .output()
        .ok()
        .and_then(|o| String::from_utf8(o.stdout).ok())
        .map(|s| s.trim().to_string())
        .unwrap_or_else(|| "unknown".to_string());

    // Truncate args to avoid huge entries (e.g., file content in write_file)
    let truncated_args = truncate_audit_args(args);

    let entry = serde_json::json!({
        "ts": ts,
        "tool": tool_name,
        "args": truncated_args,
        "duration_ms": duration_ms,
        "success": success,
    });
    writeln!(file, "{}", entry)?;
    Ok(())
}

/// Truncate tool arguments for audit logging.
/// Keeps keys but truncates long string values (like file contents) to 200 chars.
fn truncate_audit_args(args: &serde_json::Value) -> serde_json::Value {
    match args {
        serde_json::Value::Object(map) => {
            let mut new_map = serde_json::Map::new();
            for (k, v) in map {
                new_map.insert(k.clone(), truncate_audit_value(v));
            }
            serde_json::Value::Object(new_map)
        }
        other => other.clone(),
    }
}

fn truncate_audit_value(v: &serde_json::Value) -> serde_json::Value {
    match v {
        serde_json::Value::String(s) if s.len() > 200 => {
            serde_json::Value::String(format!("{}... [truncated, {} chars total]", &s[..200], s.len()))
        }
        other => other.clone(),
    }
}
```

### 2. Wire into event handling in `src/prompt.rs`

In `handle_prompt_events()`, we already capture `ToolExecutionStart` and `ToolExecutionEnd` events. Add timing tracking:
- On `ToolExecutionStart`: record the tool name, args, and start time in a local HashMap
- On `ToolExecutionEnd`: compute duration, check success, call `audit_log_tool_call()`

This means adding a `HashMap<String, (String, serde_json::Value, Instant)>` local variable in the event loop to track in-flight tool calls.

Look at how `handle_prompt_events` currently processes these events and add the audit calls at the appropriate points.

### 3. CLI flag `--audit` in `src/cli.rs`

Add `--audit` to the CLI argument parsing section (where `--no-color`, `--no-bell`, etc. are parsed):
- When `--audit` is present, call `enable_audit_log()`
- Also support `YOYO_AUDIT=1` environment variable

In the config file parsing, also support `audit = true` under `[general]` or top-level.

### 4. REPL command `/audit` to view the log

Add a simple `/audit` command that reads and displays the last N entries from `.yoyo/audit.jsonl`:
- `/audit` — show last 20 entries
- `/audit N` — show last N entries  
- `/audit clear` — clear the audit log

Add to `KNOWN_COMMANDS`, help text, and REPL dispatch.

### 5. Tests

In `src/prompt.rs` tests:
- `test_truncate_audit_args_short_values` — short strings pass through unchanged
- `test_truncate_audit_args_long_values` — long strings get truncated at 200 chars
- `test_truncate_audit_args_non_string` — numbers, bools pass through
- `test_truncate_audit_args_nested_object` — only top-level values truncated
- `test_audit_enabled_default_false` — audit is off by default
- `test_enable_audit_log` — calling enable makes is_audit_enabled() return true

In `src/help.rs` tests:
- `test_audit_in_known_commands`
- `test_audit_help_exists`

In `src/main.rs` tests:
- `test_audit_flag_parsing` — if feasible via subprocess test

**IMPORTANT**: After enabling audit in a test, disable it to avoid affecting other tests. Use a cleanup pattern or only test the flag logic, not actual file writes, in unit tests.

### 6. Update CLAUDE.md and docs

Mention audit logging in the architecture section of CLAUDE.md if it changes behavior significantly.
