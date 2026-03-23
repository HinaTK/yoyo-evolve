Title: Add ast-grep integration as an optional structural search/replace tool
Files: src/commands_project.rs, src/main.rs, src/help.rs
Issue: #133

## Context

Issue #133 asks for language-specific high-level refactoring tools. @yuanhao suggested [ast-grep](https://github.com/ast-grep/ast-grep) — a fast, polyglot tool for structural code search and rewriting using AST patterns. Rather than building a full AST parser ourselves, we can integrate with ast-grep as an optional external tool. When `sg` (ast-grep's binary) is available on PATH, the agent gets access to structural search and replace. When it's not installed, everything still works — it just falls back to text-based operations.

## Implementation

1. **In `src/commands_project.rs`**:
   - Add `fn is_ast_grep_available() -> bool` — check if `sg` is on PATH via `Command::new("sg").arg("--version").output()`.
   - Add `fn run_ast_grep_search(pattern: &str, lang: Option<&str>, path: Option<&str>) -> Result<String, String>` — runs `sg --pattern '<pattern>' [--lang <lang>] [<path>]` and returns results.
   - Add `fn run_ast_grep_replace(pattern: &str, replacement: &str, lang: Option<&str>, path: Option<&str>) -> Result<String, String>` — runs `sg --pattern '<pattern>' --rewrite '<replacement>' [--lang <lang>] [<path>] --update-all` for actual replacements. **Important**: before running with `--update-all`, first run without it to show a preview.
   - Add `pub fn handle_ast_grep(input: &str)` — REPL command handler for `/ast <search|replace> <pattern> [--lang rust] [--in src/]`. Parse subcommands.

2. **In `src/main.rs`**:
   - Add an `AstGrepSearchTool` agent tool that wraps `run_ast_grep_search`, with a schema accepting `pattern` (required), `lang` (optional), and `path` (optional). This lets the model use structural search during agentic runs.
   - Add it to `build_tools()` **only if** `is_ast_grep_available()` returns true — don't advertise a tool the model can't use.
   - The tool description should explain that patterns use ast-grep's pattern syntax (e.g., `$VAR.unwrap()` matches any `.unwrap()` call).

3. **In `src/help.rs`**:
   - Add help entry for `/ast` — show usage, explain it requires `sg` (ast-grep) to be installed, link to https://ast-grep.github.io/.

4. **In `src/commands.rs`**:
   - Add `/ast` to `KNOWN_COMMANDS`.

5. **In `/doctor`**: Add a check for ast-grep availability, listed as optional:
   ```
   ✓ ast-grep (sg): installed (v0.x.x)    — or —
   ○ ast-grep (sg): not installed (optional — install for structural refactoring)
   ```

6. **Tests**:
   - `test_is_ast_grep_available_no_panic` — function doesn't panic when sg isn't installed
   - `test_ast_grep_search_no_sg` — returns appropriate error when sg not available
   - `test_parse_ast_grep_args` — parse `/ast search $EXPR.unwrap() --lang rust --in src/`
   - `test_ast_in_known_commands`
   - `test_ast_in_help_text`
   - `test_ast_grep_tool_only_when_available` — when sg not on PATH, build_tools doesn't include it
   - `test_doctor_shows_ast_grep_status`

This is a practical, opt-in integration — it doesn't add a build dependency, just shells out to an external tool when available. It directly addresses Issue #133's ask for language-specific refactoring.
