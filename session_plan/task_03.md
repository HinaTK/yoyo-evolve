Title: Expose rename_in_project as an agent-invocable tool for token-efficient refactoring
Files: src/main.rs, src/commands_project.rs
Issue: #133

## Context

Issue #133 asks for high-level refactoring tools that the LLM can invoke directly instead of doing raw text edits. We already have `/rename`, `/extract`, and `/move` as REPL commands, but the LLM can't call them — it can only use bash, read_file, write_file, edit_file, search, and list_files. When the agent needs to rename a symbol across files, it currently has to do multiple edit_file calls, which is slow and error-prone.

This task exposes `rename_in_project` as an agent tool — the first language-aware refactoring tool the model can use. This is a significant step: it means the agent can do `rename_symbol(old="Foo", new="Bar")` in a single tool call instead of editing every file individually.

## Implementation

1. **In `src/main.rs`**: Create a new `RenameSymbolTool` struct that implements `AgentTool`:

   ```rust
   struct RenameSymbolTool;

   #[async_trait::async_trait]
   impl AgentTool for RenameSymbolTool {
       fn name(&self) -> &str { "rename_symbol" }
       fn label(&self) -> &str { "Rename" }
       fn description(&self) -> &str {
           "Rename a symbol across the project. Performs word-boundary-aware find-and-replace \
            in all git-tracked files. More reliable than multiple edit_file calls for renames. \
            Returns a preview of changes and the number of files modified."
       }
       fn parameters_schema(&self) -> serde_json::Value {
           serde_json::json!({
               "type": "object",
               "properties": {
                   "old_name": {
                       "type": "string",
                       "description": "The current name of the symbol to rename"
                   },
                   "new_name": {
                       "type": "string",
                       "description": "The new name for the symbol"
                   },
                   "path": {
                       "type": "string",
                       "description": "Optional: limit rename to a specific file or directory (default: entire project)"
                   }
                },
               "required": ["old_name", "new_name"]
           })
       }
       
       async fn execute(&self, params: Value, _ctx: ToolContext) -> Result<ToolResult> {
           // Extract params
           // Call rename_in_project(old_name, new_name, scope)
           // Format results showing which files were changed and how many replacements
       }
   }
   ```

2. **In `src/commands_project.rs`**: Make `rename_in_project()` return structured results instead of just printing. Currently it prints directly. Refactor to return a `RenameResult` struct:

   ```rust
   pub struct RenameResult {
       pub files_changed: Vec<String>,
       pub total_replacements: usize,
       pub preview: String, // human-readable summary
   }
   ```

   The existing `handle_rename()` REPL handler calls this and prints. The new tool also calls this and returns the result as tool output.

   **Important**: Check the existing `rename_in_project` function signature carefully before changing. Ensure backward compatibility with the REPL `/rename` command.

3. **In `src/main.rs` `build_tools()`**: Add `RenameSymbolTool` to the tool list. The tool should respect directory restrictions (wrap with `GuardedTool` if it writes files — but since rename_in_project operates on git-tracked files, it should at minimum not rename into denied directories).

4. **Tests**:
   - `test_rename_symbol_tool_schema` — verify parameters_schema has old_name, new_name, path
   - `test_rename_symbol_tool_name` — name is "rename_symbol"
   - `test_rename_result_struct` — RenameResult can be constructed and has expected fields
   - Verify existing `/rename` tests still pass (don't break the REPL command)

This is the first of potentially three refactoring tools (rename, extract, move) that the LLM can invoke. Start with rename because it's the simplest and most commonly needed.
