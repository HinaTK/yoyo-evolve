Title: Add TodoTool — let the model manage tasks autonomously during agentic runs
Files: src/main.rs, src/commands.rs, src/help.rs
Issue: #176

## Problem

yoyo has a working `/todo` REPL command (in commands_project.rs) but the AI model has no way to use it as a tool during autonomous operation. Claude Code has `TodoRead`/`TodoWrite` tools that let the model track multi-step plans, check items off, and maintain state across long sessions. Without a TodoTool, yoyo's model loses track of complex plans purely from conversation context, which degrades on long sessions.

Issue #176 was a previous attempt that was reverted because tests failed. This is a retry with a focused scope: just the agent tool, since the REPL command and data structures already exist and work.

## What already exists

In `src/commands_project.rs`:
- `TodoItem` struct with `id: usize`, `description: String`, `status: TodoStatus`
- `TodoStatus` enum: `Pending`, `InProgress`, `Done` (with Display impl for checkboxes)
- `todo_add(description: &str) -> usize`
- `todo_update(id: usize, status: TodoStatus) -> Result<(), String>`
- `todo_list() -> Vec<TodoItem>`
- `todo_clear()`
- `todo_remove(id: usize) -> Result<TodoItem, String>`
- `format_todo_list(items: &[TodoItem]) -> String`

All tested. The REPL command `/todo` dispatches to these functions.

## Implementation

### Step 1: Create `TodoTool` struct in `src/main.rs`

Add a new struct near the other tool implementations (after `AskUserTool`):

```rust
/// Agent tool for managing a task list during complex multi-step operations.
/// Wraps the existing todo functions from commands_project.
pub struct TodoTool;

impl AgentTool for TodoTool {
    fn name(&self) -> &str {
        "todo"
    }

    fn description(&self) -> &str {
        "Manage a task list to track progress on complex multi-step operations. \
         Use this to plan work, check off completed steps, and see what's remaining. \
         Available actions: list, add, done, wip, remove, clear."
    }

    fn parameters(&self) -> serde_json::Value {
        serde_json::json!({
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["list", "add", "done", "wip", "remove", "clear"],
                    "description": "Action to perform: list (show all), add (create task), done (mark complete), wip (mark in-progress), remove (delete task), clear (delete all)"
                },
                "description": {
                    "type": "string",
                    "description": "Task description (required for 'add')"
                },
                "id": {
                    "type": "integer",
                    "description": "Task ID number (required for 'done', 'wip', 'remove')"
                }
            },
            "required": ["action"]
        })
    }

    fn execute(
        &self,
        args: &serde_json::Value,
        _cx: &yoagent::tools::ToolContext,
    ) -> Result<String, String> {
        let action = args.get("action")
            .and_then(|v| v.as_str())
            .ok_or_else(|| "Missing required 'action' parameter".to_string())?;

        match action {
            "list" => {
                let items = commands_project::todo_list();
                if items.is_empty() {
                    Ok("No tasks. Use action 'add' to create one.".to_string())
                } else {
                    Ok(commands_project::format_todo_list(&items))
                }
            }
            "add" => {
                let desc = args.get("description")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| "Missing 'description' for add action".to_string())?;
                let id = commands_project::todo_add(desc);
                Ok(format!("Added task #{id}: {desc}"))
            }
            "done" => {
                let id = args.get("id")
                    .and_then(|v| v.as_u64())
                    .ok_or_else(|| "Missing 'id' for done action".to_string())? as usize;
                commands_project::todo_update(id, commands_project::TodoStatus::Done)?;
                Ok(format!("Task #{id} marked as done ✓"))
            }
            "wip" => {
                let id = args.get("id")
                    .and_then(|v| v.as_u64())
                    .ok_or_else(|| "Missing 'id' for wip action".to_string())? as usize;
                commands_project::todo_update(id, commands_project::TodoStatus::InProgress)?;
                Ok(format!("Task #{id} marked as in-progress"))
            }
            "remove" => {
                let id = args.get("id")
                    .and_then(|v| v.as_u64())
                    .ok_or_else(|| "Missing 'id' for remove action".to_string())? as usize;
                let item = commands_project::todo_remove(id)?;
                Ok(format!("Removed task #{id}: {}", item.description))
            }
            "clear" => {
                commands_project::todo_clear();
                Ok("All tasks cleared.".to_string())
            }
            other => Err(format!("Unknown action '{other}'. Use: list, add, done, wip, remove, clear"))
        }
    }
}
```

### Step 2: Add TodoTool to `build_tools()`

In the `build_tools()` function, add TodoTool to the tools vector. It does NOT need permission confirmation (it only modifies in-memory state, not filesystem). Add it after the AskUserTool block:

```rust
// TodoTool is always available — it only modifies in-memory state
tools.push(Box::new(TodoTool));
```

### Step 3: Update tool count in tests

The `test_build_tools_returns_six_tools()` test (and similar) check exact tool counts. After adding TodoTool:
- Tools without terminal (piped mode): 7 base + 1 TodoTool = 8
- Tools with terminal: 7 base + AskUserTool + TodoTool = 9

Update all tool count assertions. Search for `build_tools` in test functions and update the expected counts.

Actually, check the current count: base tools are bash, read_file, write_file, edit_file, list_files, search, rename_symbol = 7. Plus AskUserTool (only in terminal mode). So:
- Non-terminal: 7 + 1 (TodoTool) = 8
- Terminal: 7 + 1 (AskUserTool) + 1 (TodoTool) = 9

### Step 4: Update help and known commands

In `src/commands.rs`, ensure `todo` tool is documented if there's a tool listing.

In `src/help.rs`, update the `/todo` help entry to mention that the AI can also use it as a tool:
```
The AI agent can also manage tasks via the todo tool during
agentic runs, helping it stay organized on multi-step operations.
```

### Step 5: Tests

In `src/main.rs` tests:

```rust
#[test]
fn test_todo_tool_name() {
    let tool = TodoTool;
    assert_eq!(tool.name(), "todo");
}

#[test]
fn test_todo_tool_schema_has_action() {
    let tool = TodoTool;
    let params = tool.parameters();
    assert!(params["properties"]["action"].is_object());
    assert!(params["properties"]["description"].is_object());
    assert!(params["properties"]["id"].is_object());
}

#[test]
fn test_todo_tool_list_empty() {
    commands_project::todo_clear(); // Reset state
    let tool = TodoTool;
    let cx = yoagent::tools::ToolContext::default();
    let result = tool.execute(&serde_json::json!({"action": "list"}), &cx);
    assert!(result.is_ok());
    assert!(result.unwrap().contains("No tasks"));
}

#[test]
fn test_todo_tool_add_and_list() {
    commands_project::todo_clear();
    let tool = TodoTool;
    let cx = yoagent::tools::ToolContext::default();
    
    let result = tool.execute(&serde_json::json!({"action": "add", "description": "Write tests"}), &cx);
    assert!(result.is_ok());
    assert!(result.unwrap().contains("#1"));
    
    let result = tool.execute(&serde_json::json!({"action": "list"}), &cx);
    assert!(result.unwrap().contains("Write tests"));
}

#[test]
fn test_todo_tool_done_and_remove() {
    commands_project::todo_clear();
    let tool = TodoTool;
    let cx = yoagent::tools::ToolContext::default();
    
    tool.execute(&serde_json::json!({"action": "add", "description": "Task A"}), &cx).unwrap();
    
    let result = tool.execute(&serde_json::json!({"action": "done", "id": 1}), &cx);
    assert!(result.unwrap().contains("done ✓"));
    
    let result = tool.execute(&serde_json::json!({"action": "remove", "id": 1}), &cx);
    assert!(result.unwrap().contains("Removed"));
}

#[test]
fn test_todo_tool_invalid_action() {
    let tool = TodoTool;
    let cx = yoagent::tools::ToolContext::default();
    let result = tool.execute(&serde_json::json!({"action": "explode"}), &cx);
    assert!(result.is_err());
}

#[test]
fn test_todo_tool_missing_description() {
    let tool = TodoTool;
    let cx = yoagent::tools::ToolContext::default();
    let result = tool.execute(&serde_json::json!({"action": "add"}), &cx);
    assert!(result.is_err());
}

#[test]
fn test_todo_tool_in_build_tools() {
    let perms = cli::PermissionConfig::default();
    let dirs = cli::DirectoryRestrictions::default();
    let tools = build_tools(true, &perms, &dirs, TOOL_OUTPUT_MAX_CHARS);
    let names: Vec<&str> = tools.iter().map(|t| t.name()).collect();
    assert!(names.contains(&"todo"), "build_tools should include todo, got: {names:?}");
}
```

**IMPORTANT**: Since TodoTool uses the global `TODO_LIST`, tests that modify it must call `todo_clear()` at the start to avoid cross-test interference. The todo tests in commands_project.rs likely already do this.

### Step 6: Update tool count tests

Find and update these tests that check exact tool counts:
- `test_build_tools_returns_six_tools` — update comment and expected count (currently expects 7, should be 8)
- `test_build_tools_count_unchanged_with_sub_agent` — update expected count
- `test_build_tools_with_piped_limit` — update expected count if it checks count
- Any other tests that assert on `tools.len()`

Search pattern: `grep -n "tools.len()\|build_tools.*7\|build_tools.*six" src/main.rs`
