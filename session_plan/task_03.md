Title: Wire search + remaining bare subcommands (grep, find, index) and update help text
Files: src/cli.rs
Issue: none

## Context

Tasks 1 and 2 wire dev-workflow and git-workflow bare subcommands. This task completes the "front door" story by wiring the search commands and updating the `--help` output to document ALL available bare subcommands. A developer who types `yoyo grep TODO` or `yoyo find main` should get instant results.

## What to do

### Part 1: Wire subcommands in `try_dispatch_subcommand`

Add match arms for:

1. **`"grep"`** → Call `crate::commands_search::handle_grep(input)` where `input` is `/grep <rest>`. `yoyo grep TODO src/` → `handle_grep("/grep TODO src/")`. Return `Some(None)`.

2. **`"find"`** → Call `crate::commands_search::handle_find(input)` where `input` is `/find <rest>`. `yoyo find main` → `handle_find("/find main")`. Return `Some(None)`.

3. **`"index"`** → Call `crate::commands_search::handle_index()`. Return `Some(None)`.

Use the same input reconstruction pattern as tasks 1 and 2: `let input = format!("/{}", args[1..].join(" "));`

### Part 2: Update help text

In `help_text()`, the "Subcommands" section currently lists: help, version, setup, init, doctor, health. Add the new subcommands grouped by category:

```
  Subcommands:
    help              Show this help message (same as --help)
    version           Show version (same as --version)
    setup             Run the interactive setup wizard
    init              Generate a YOYO.md project context file
    doctor            Diagnose yoyo setup (config, API key, provider, tool availability)
    health            Run project health checks (build, test, clippy, fmt)
    lint              Run project linter (auto-detected)
    test              Run project tests (auto-detected)
    tree [depth]      Show project file tree
    map [filter]      Show repository symbol map
    run <command>     Run a shell command directly
    diff [options]    Show git diff
    commit [message]  Create a git commit
    review            Generate a code review of staged changes
    blame <file>      Show annotated git blame
    grep <pattern>    Search files for a pattern
    find <pattern>    Find files by name
    index             Build and display project index
```

### Part 3: Update the test

There's an existing test `help_text_documents_all_subcommands` — update it to check for the new subcommands.

## Tests

- `test_try_dispatch_subcommand_grep` — verify returns `Some(None)`
- `test_try_dispatch_subcommand_find` — verify returns `Some(None)`
- `test_try_dispatch_subcommand_index` — verify returns `Some(None)`
- Update `help_text_documents_all_subcommands` to include new entries

## Verification

```bash
cargo build && cargo test
echo "" | timeout 5 cargo run -- find main 2>&1 | head -20 || true
echo "" | timeout 5 cargo run -- index 2>&1 | head -20 || true
```
