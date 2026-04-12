Title: Add --watch CLI flag to enable watch mode from startup
Files: src/cli.rs, src/repl.rs
Issue: #278 (partial — enables long-running autonomous tasks with automatic verification)

## Problem

Watch mode (`/watch`) auto-runs a test/lint command after each agent turn and feeds failures back to the agent for auto-fixing. Currently it can only be activated via the REPL command `/watch cargo test`. There's no way to start a session with watch mode already active from the command line.

For long-running autonomous tasks (#278), users want to launch with:
```bash
yoyo --watch "cargo test" "implement the feature described in SPEC.md"
```

This is what Aider's `--auto-test` does, and it's a significant competitive gap. The plumbing already exists — we just need to wire it up.

## Implementation

### 1. Add `watch_command` field to Config struct in cli.rs

Near line 83 (where `auto_commit` is defined):
```rust
pub auto_commit: bool,
pub watch_command: Option<String>,
```

### 2. Parse `--watch <cmd>` flag in parse_args (cli.rs)

Near line 1090 where `auto_commit` is parsed:
```rust
let watch_command = flag_value(&args, "--watch").map(|s| s.to_string());
```

Add `"--watch"` to the known flags list (around line 550 where other flags are listed).

Add to the Config construction (around line 1246):
```rust
watch_command,
```

Add to help text (around line 213):
```
"  --watch <cmd>     Enable watch mode — run <cmd> after each agent turn"
```

### 3. Wire watch_command through to run_repl in main.rs

The `config.watch_command` needs to be passed to `run_repl`. But instead of changing run_repl's signature (which already has 9 parameters), the simplest approach is to call `set_watch_command` in main.rs right before calling `run_repl`:

In main.rs, before the `repl::run_repl(...)` call (around line 1002):
```rust
if let Some(ref cmd) = config.watch_command {
    crate::prompt::set_watch_command(cmd);
}
```

This uses the existing global state that `/watch` already uses, so all the watch mode machinery (run after each turn, auto-fix on failure) works automatically.

### 4. Show watch mode status in REPL banner

In repl.rs, after the existing banner prints (around line 310-320 where auto_commit is displayed), add:
```rust
if let Some(ref cmd) = crate::prompt::get_watch_command() {
    println!("{DIM}  watch: {cmd}{RESET}");
}
```

### 5. Add tests in cli.rs

```rust
#[test]
fn test_watch_flag_default_none() {
    let args: Vec<String> = vec!["yoyo".to_string()];
    let config = parse_args(args).unwrap();
    assert!(config.watch_command.is_none(), "watch_command should default to None");
}

#[test]
fn test_watch_flag_parsed() {
    let args: Vec<String> = vec![
        "yoyo".to_string(),
        "--watch".to_string(),
        "cargo test".to_string(),
    ];
    let config = parse_args(args).unwrap();
    assert_eq!(
        config.watch_command.as_deref(),
        Some("cargo test"),
        "watch_command should be parsed from --watch flag"
    );
}
```

## Verification

1. `cargo build` — compiles clean
2. `cargo test` — all pass including new tests
3. `cargo clippy --all-targets -- -D warnings` — zero warnings
4. `--help` output includes the --watch flag description

## Why this matters

This closes a real gap with Aider's `--auto-test` and addresses #278's request for better long-running task support. With `--watch`, piped mode becomes useful for autonomous tasks:
```bash
echo "refactor the auth module" | yoyo --watch "cargo test"
```

The agent will automatically verify its work after each turn and fix failures — no manual intervention needed.
