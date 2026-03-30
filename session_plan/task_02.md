Title: Add inline command hints in REPL (step toward Issue #214)
Files: src/repl.rs, src/help.rs
Issue: #214

## Context

Issue #214 requests an interactive slash-command autocomplete menu. The full TUI popup is a large
feature, but rustyline's `Hinter` trait lets us show inline suggestions — a meaningful step that
gives users instant command discovery.

Currently the `Hinter` impl for `YoyoHelper` is empty — no hints shown. When a user types `/he`,
nothing appears until they press Tab. With this change, a dimmed completion suggestion appears
inline as they type: `/he` → shows `lp — Show help for commands` in dim text after the cursor.

This is a small, self-contained change to `src/repl.rs` with a helper function in `src/help.rs`.

## What to do

### 1. Add a `command_short_description()` function in `src/help.rs`

Add a new public function that returns a short one-line description for each known command:

```rust
/// Returns a short one-line description for a command (used for inline hints).
pub fn command_short_description(cmd: &str) -> Option<&'static str> {
    match cmd {
        "add" => Some("Add file contents to conversation"),
        "apply" => Some("Apply a diff or patch file"),
        "ast" => Some("Structural code search via ast-grep"),
        "changes" => Some("Show files modified during this session"),
        "clear" => Some("Clear conversation history"),
        "clear!" => Some("Force-clear without confirmation"),
        "commit" => Some("Commit staged changes"),
        "compact" => Some("Compact conversation to save context"),
        "config" => Some("Show current settings"),
        "context" => Some("Show loaded project context"),
        "cost" => Some("Show estimated session cost"),
        "diff" => Some("Show git changes"),
        "doctor" => Some("Run environment diagnostics"),
        "docs" => Some("Look up crate documentation"),
        "exit" => Some("Exit yoyo"),
        "export" => Some("Export conversation as markdown"),
        "extract" => Some("Extract a function/block to a new file"),
        "find" => Some("Find files by name pattern"),
        "fix" => Some("Auto-fix build/lint errors"),
        "forget" => Some("Remove a saved memory"),
        "git" => Some("Quick git commands"),
        "grep" => Some("Search file contents"),
        "health" => Some("Run project health checks"),
        "help" => Some("Show help for commands"),
        "history" => Some("Show conversation message summary"),
        "index" => Some("Show project file index"),
        "init" => Some("Generate a YOYO.md context file"),
        "jump" => Some("Restore conversation to a bookmark"),
        "lint" => Some("Run project linter"),
        "load" => Some("Load session from file"),
        "map" => Some("Show project symbol map"),
        "mark" => Some("Bookmark current conversation state"),
        "marks" => Some("List saved bookmarks"),
        "memories" => Some("Show saved memories"),
        "model" => Some("Switch or show current model"),
        "move" => Some("Move a method between files"),
        "plan" => Some("AI-generate a task plan"),
        "pr" => Some("List, view, or create pull requests"),
        "provider" => Some("Switch or show current provider"),
        "quit" => Some("Exit yoyo"),
        "refactor" => Some("Refactoring tools (extract, rename, move)"),
        "remember" => Some("Save a memory note"),
        "rename" => Some("Rename a symbol across the project"),
        "retry" => Some("Re-send the last input"),
        "review" => Some("AI code review"),
        "run" => Some("Run a shell command"),
        "save" => Some("Save session to file"),
        "search" => Some("Search conversation history"),
        "spawn" => Some("Run a task in a sub-agent"),
        "stash" => Some("Stash conversation and start fresh"),
        "status" => Some("Show session info"),
        "test" => Some("Run project tests"),
        "think" => Some("Set thinking level"),
        "todo" => Some("Track tasks (add, done, remove, clear)"),
        "tokens" => Some("Show token usage and context window"),
        "tree" => Some("Show project directory tree"),
        "undo" => Some("Undo last turn's changes"),
        "version" => Some("Show yoyo version"),
        "watch" => Some("Auto-run command after file changes"),
        "web" => Some("Fetch a web page"),
        _ => None,
    }
}
```

### 2. Implement `Hinter` for `YoyoHelper` in `src/repl.rs`

Replace the empty Hinter impl:

```rust
impl Hinter for YoyoHelper {
    type Hint = String;
}
```

With a real implementation:

```rust
impl Hinter for YoyoHelper {
    type Hint = String;

    fn hint(&self, line: &str, pos: usize, _ctx: &rustyline::Context<'_>) -> Option<String> {
        // Only hint when cursor is at the end of the line
        if pos != line.len() {
            return None;
        }
        // Only hint for slash commands
        if !line.starts_with('/') {
            return None;
        }
        let typed = &line[1..]; // strip the leading /
        if typed.is_empty() {
            return None; // Don't hint on bare "/"
        }
        // Don't hint if there's already a space (user is typing arguments)
        if typed.contains(' ') {
            return None;
        }
        // Find the first matching command
        use crate::commands::KNOWN_COMMANDS;
        for cmd in KNOWN_COMMANDS {
            let cmd_name = &cmd[1..]; // strip leading /
            if cmd_name.starts_with(typed) && cmd_name != typed {
                // Show the rest of the command + description
                let rest = &cmd_name[typed.len()..];
                if let Some(desc) = crate::help::command_short_description(cmd_name) {
                    return Some(format!("{rest} — {desc}"));
                } else {
                    return Some(rest.to_string());
                }
            }
        }
        // If user typed a complete command name, show its description
        for cmd in KNOWN_COMMANDS {
            let cmd_name = &cmd[1..];
            if cmd_name == typed {
                if let Some(desc) = crate::help::command_short_description(cmd_name) {
                    return Some(format!(" — {desc}"));
                }
            }
        }
        None
    }
}
```

### 3. Enable Highlighter for hints

rustyline needs the `Highlighter` trait to render hints in a different style. Replace:

```rust
impl Highlighter for YoyoHelper {}
```

With:

```rust
impl Highlighter for YoyoHelper {
    fn highlight_hint<'h>(&self, hint: &'h str) -> std::borrow::Cow<'h, str> {
        // Show hints in dim text
        std::borrow::Cow::Owned(format!("\x1b[2m{hint}\x1b[0m"))
    }
}
```

### 4. Tests

Add tests in `src/repl.rs` tests section:

```rust
#[test]
fn test_hinter_shows_command_completion() {
    let helper = YoyoHelper;
    let ctx = rustyline::Context::new(&rustyline::history::DefaultHistory::new());
    // Typing "/he" should suggest "lp — Show help for commands"
    let hint = helper.hint("/he", 3, &ctx);
    assert!(hint.is_some());
    assert!(hint.unwrap().starts_with("lp"));
}

#[test]
fn test_hinter_no_hint_for_complete_command() {
    let helper = YoyoHelper;
    let ctx = rustyline::Context::new(&rustyline::history::DefaultHistory::new());
    // Typing "/help" exactly should show description
    let hint = helper.hint("/help", 5, &ctx);
    assert!(hint.is_some());
    assert!(hint.unwrap().contains("—"));
}

#[test]
fn test_hinter_no_hint_for_arguments() {
    let helper = YoyoHelper;
    let ctx = rustyline::Context::new(&rustyline::history::DefaultHistory::new());
    // After space (typing arguments), no hint
    let hint = helper.hint("/add src/", 9, &ctx);
    assert!(hint.is_none());
}

#[test]
fn test_hinter_no_hint_for_non_slash() {
    let helper = YoyoHelper;
    let ctx = rustyline::Context::new(&rustyline::history::DefaultHistory::new());
    let hint = helper.hint("hello", 5, &ctx);
    assert!(hint.is_none());
}
```

Also add a test in `src/help.rs`:

```rust
#[test]
fn test_command_short_description_coverage() {
    // Every KNOWN_COMMAND should have a short description
    for cmd in crate::commands::KNOWN_COMMANDS {
        let name = &cmd[1..]; // strip /
        assert!(
            command_short_description(name).is_some(),
            "Missing short description for command: {cmd}"
        );
    }
}
```

## Verification

```bash
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```

## What NOT to do

- Do NOT build a full TUI popup menu — this is just inline hints
- Do NOT modify the Completer implementation — Tab completion stays as-is
- Do NOT add complex state management — hints are stateless, computed from the current line
