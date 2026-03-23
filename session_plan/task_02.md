Title: Add /refactor umbrella command and improve refactoring tool discoverability
Files: src/commands_project.rs, src/commands.rs, src/repl.rs, src/help.rs
Issue: #133

## Context

Issue #133 asks for "high level refactoring tools like rename entity, move method to another file, move method up & down on class hierarchy." We already have:
- `/rename old new` — project-wide word-boundary-aware find-and-replace
- `/extract <item> <dest>` — move a function/struct/type/const/static to another file
- `/move Source::method Target` — relocate a method between impl blocks

But these are scattered and hard to discover. Users have to already know they exist. Issue #133 keeps getting reopened because the user doesn't see the tools are there.

## Implementation

1. **Add `/refactor` command** to `commands_project.rs`:
   ```
   pub fn handle_refactor(input: &str) {
   ```
   - If called with no args (`/refactor`), display a summary of all available refactoring commands:
     ```
     Refactoring Tools:
       /rename <old> <new>              Rename a symbol across all project files
       /extract <item> <dest>           Move a function, struct, or type to another file
       /move <Type>::<method> <Target>  Relocate a method between impl blocks
     
     Examples:
       /rename MyOldStruct MyNewStruct
       /extract parse_config src/config.rs
       /move Parser::validate Validator
     
     These operate on source text (not ASTs), so they work with any language.
     ```
   - If called with a subcommand (`/refactor rename ...`, `/refactor extract ...`, `/refactor move ...`), dispatch to the corresponding handler.

2. **Wire `/refactor` into the REPL** in `repl.rs`:
   Add the dispatch case for `/refactor` similar to other commands.

3. **Add `/refactor` to KNOWN_COMMANDS** in `commands.rs`.

4. **Add help entry** in `help.rs` for `/refactor` that describes the umbrella and sub-commands.

5. **Update tab completion** so `/refactor` offers subcommand completions: `rename`, `extract`, `move`.

6. **Tests**:
   - `test_refactor_no_args_shows_help` — calling `handle_refactor("/refactor")` should print (verify it doesn't panic, captures output pattern)
   - `test_refactor_in_known_commands` — verify `/refactor` is in KNOWN_COMMANDS
   - `test_refactor_help_exists` — verify `command_help("refactor")` returns Some
   - `test_refactor_tab_completion` — verify `/refactor ` offers subcommand completions

This makes the refactoring tools *discoverable* — users who type `/refactor` learn about all three tools at once, and users who already know what they want can use the direct commands.
