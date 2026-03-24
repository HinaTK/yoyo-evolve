Title: Add /todo command and TodoTool agent tool for task tracking
Files: src/commands_project.rs, src/main.rs, src/help.rs, src/commands.rs, src/repl.rs
Issue: #176

## Context

Claude Code has `TodoRead`/`TodoWrite` tools that let the model track tasks during complex multi-step operations. yoyo has no equivalent — the model has to remember what it's doing purely from conversation context, which degrades on long sessions. This is Issue #176 (previously reverted due to test failures). This time, we need to be very careful about test isolation with global state.

## Implementation

### 1. In-memory task store in `src/commands_project.rs`

Add a thread-safe global todo list using `std::sync::Mutex` (NOT `RwLock` — simpler for a Vec):

```rust
use std::sync::Mutex;

#[derive(Debug, Clone, PartialEq)]
pub enum TodoStatus {
    Pending,
    InProgress,
    Done,
}

impl std::fmt::Display for TodoStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            TodoStatus::Pending => write!(f, "pending"),
            TodoStatus::InProgress => write!(f, "in_progress"),
            TodoStatus::Done => write!(f, "done"),
        }
    }
}

#[derive(Debug, Clone)]
pub struct TodoItem {
    pub id: usize,
    pub description: String,
    pub status: TodoStatus,
}

static TODO_LIST: Mutex<Vec<TodoItem>> = Mutex::new(Vec::new());
static TODO_NEXT_ID: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(1);
```

Functions (all must lock/unlock TODO_LIST):
- `pub fn todo_add(description: &str) -> usize` — add item, return its ID (use TODO_NEXT_ID.fetch_add)
- `pub fn todo_update(id: usize, status: TodoStatus) -> Result<(), String>` — update status
- `pub fn todo_list() -> Vec<TodoItem>` — snapshot of all items
- `pub fn todo_clear()` — clear all items AND reset TODO_NEXT_ID to 1
- `pub fn todo_remove(id: usize) -> Result<TodoItem, String>` — remove a single item
- `pub fn format_todo_list(items: &[TodoItem]) -> String` — formatted display:
  - `[ ] pending` (or ` ` for pending)
  - `[~] in progress`
  - `[✓] done`
  - If empty, return "(no tasks)"

### 2. REPL command `/todo` handler

Add `pub fn handle_todo(input: &str)` in `src/commands_project.rs`:

```
/todo                    Show all tasks
/todo add <description>  Add a new task
/todo done <id>          Mark task as done
/todo wip <id>           Mark task as in-progress
/todo pending <id>       Reset task to pending
/todo remove <id>        Remove a task
/todo clear              Clear all tasks
```

Parse subcommands from the input after `/todo `. Print colored output using existing ANSI helpers.

### 3. Agent tool `TodoTool` in `src/main.rs`

Create a `TodoTool` struct implementing `AgentTool`:

```rust
struct TodoTool;

#[async_trait::async_trait]
impl AgentTool for TodoTool {
    fn name(&self) -> &str { "todo" }
    fn description(&self) -> &str {
        "Manage a task list to track progress on complex multi-step operations. Use this to plan work, check off completed items, and see what's remaining."
    }
    fn parameters_schema(&self) -> serde_json::Value {
        serde_json::json!({
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["add", "update", "list", "remove", "clear"],
                    "description": "The action to perform"
                },
                "description": {
                    "type": "string",
                    "description": "Task description (required for 'add')"
                },
                "id": {
                    "type": "integer",
                    "description": "Task ID (required for 'update' and 'remove')"
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "done"],
                    "description": "New status (required for 'update')"
                }
            },
            "required": ["action"]
        })
    }
    // execute() — dispatch to todo_add/update/list/remove/clear based on action param
    // Return the formatted todo list or confirmation message as ToolResult
}
```

The tool should NOT require permission confirmation — it only touches in-memory state.

Add it to `build_tools()` at the end of the tools vec. No guarding or confirmation needed.

### 4. Wire into REPL dispatch

In `src/repl.rs`, add `/todo` dispatch in the command match block, calling `handle_todo(input)`.

### 5. Update known commands and help

- Add `/todo` to `KNOWN_COMMANDS` in `src/commands.rs`
- Add help entry in `src/help.rs` for `command_help("todo")`
- Add `/todo` to `help_text()` command listing

### 6. Tests — CRITICAL: Test isolation

Since TODO_LIST is global state, **every test that modifies it must call `todo_clear()` at the start**. Do NOT rely on test ordering.

In `src/commands_project.rs` tests:
```rust
#[test]
fn test_todo_add_returns_incrementing_ids() {
    todo_clear();
    let id1 = todo_add("first task");
    let id2 = todo_add("second task");
    assert_eq!(id1, 1); // IDs should be sequential after clear
    // Note: id2 might not be 2 if other tests ran between clear and here
    // Better: just assert id2 > id1
    assert!(id2 > id1);
}

#[test]
fn test_todo_update_status() {
    todo_clear();
    let id = todo_add("task");
    assert!(todo_update(id, TodoStatus::InProgress).is_ok());
    let items = todo_list();
    assert_eq!(items[0].status, TodoStatus::InProgress);
}

#[test]
fn test_todo_update_invalid_id() {
    todo_clear();
    assert!(todo_update(9999, TodoStatus::Done).is_err());
}

#[test]
fn test_todo_remove() {
    todo_clear();
    let id = todo_add("remove me");
    assert!(todo_remove(id).is_ok());
    assert!(todo_list().is_empty());
}

#[test]
fn test_todo_remove_invalid_id() {
    todo_clear();
    assert!(todo_remove(9999).is_err());
}

#[test]
fn test_todo_clear_resets_everything() {
    todo_clear();
    todo_add("a");
    todo_add("b");
    assert_eq!(todo_list().len(), 2);
    todo_clear();
    assert!(todo_list().is_empty());
}

#[test]
fn test_todo_list_empty() {
    todo_clear();
    assert!(todo_list().is_empty());
}

#[test]
fn test_format_todo_list_with_items() {
    todo_clear();
    let id1 = todo_add("write tests");
    let _ = todo_add("write code");
    todo_update(id1, TodoStatus::Done).unwrap();
    let items = todo_list();
    let formatted = format_todo_list(&items);
    assert!(formatted.contains("[✓]"));
    assert!(formatted.contains("[ ]"));
    assert!(formatted.contains("write tests"));
}

#[test]
fn test_format_todo_list_empty() {
    let formatted = format_todo_list(&[]);
    assert!(formatted.contains("no tasks"));
}
```

In `src/main.rs` tests:
```rust
#[test]
fn test_todo_tool_in_build_tools() {
    let perms = cli::PermissionConfig::default();
    let dirs = cli::DirectoryRestrictions::default();
    let tools = build_tools(true, &perms, &dirs, TOOL_OUTPUT_MAX_CHARS);
    assert!(tools.iter().any(|t| t.name() == "todo"), "build_tools should include todo tool");
}
```

In `src/help.rs` tests:
```rust
#[test]
fn test_todo_in_known_commands() {
    assert!(KNOWN_COMMANDS.contains(&"/todo"));
}

#[test]
fn test_todo_help_exists() {
    assert!(command_help("todo").is_some());
}
```

**IMPORTANT**: The previous attempt failed on tests. Key differences this time:
- Use `Mutex` not `RwLock` for simpler semantics
- Use `AtomicUsize` for ID generation separate from the list
- Every single test starts with `todo_clear()` 
- Don't assert exact ID values — assert relative ordering instead
- TWO existing tests need updating:
  1. `test_build_tools_returns_six_tools` (line ~1386) — change assert from 7 to 8
  2. `test_build_tools_with_piped_limit` (line ~2335) — change assert from 7 to 8 and update message
