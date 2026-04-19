Title: Update DAY_COUNT to 50 and add /config edit command
Files: DAY_COUNT, src/commands_config.rs, src/help.rs
Issue: none

## Context

Two small improvements:
1. DAY_COUNT is 49 but today is Day 50. Update it.
2. Add `/config edit` subcommand — opens the user's config file in $EDITOR.
   Every real CLI tool has this. Currently users must know the config file path
   (`~/.config/yoyo/config.toml` or `.yoyo.toml`) and open it manually.

## Implementation

### Step 1: Update DAY_COUNT

Write `50` to the DAY_COUNT file (just the number, with a trailing newline).

### Step 2: Add /config edit subcommand

In `src/commands_config.rs`, in the `handle_config()` function, add a new
`"edit"` subcommand case:

```rust
"edit" => {
    // Determine config file path priority:
    // 1. .yoyo.toml in current directory (project-level)
    // 2. ~/.config/yoyo/config.toml (user-level)
    // If neither exists, default to user-level path
    
    let project_config = std::path::Path::new(".yoyo.toml");
    let user_config = cli::user_config_path();
    
    let config_path = if project_config.exists() {
        project_config.to_path_buf()
    } else if let Some(ref uc) = user_config {
        if std::path::Path::new(uc).exists() {
            std::path::PathBuf::from(uc)
        } else {
            // Create a starter config file at user path
            // with helpful comments
            std::path::PathBuf::from(uc)
        }
    } else {
        eprintln!("Could not determine config file path");
        return;
    };
    
    // Get editor from $EDITOR, $VISUAL, or fall back to common editors
    let editor = std::env::var("EDITOR")
        .or_else(|_| std::env::var("VISUAL"))
        .unwrap_or_else(|_| {
            if cfg!(target_os = "windows") { "notepad".to_string() }
            else { "vi".to_string() }
        });
    
    println!("Opening {} in {}", config_path.display(), editor);
    let status = std::process::Command::new(&editor)
        .arg(&config_path)
        .status();
    
    match status {
        Ok(s) if s.success() => {
            println!("{}Config saved.{}", Color::GREEN, Color::RESET);
        }
        Ok(_) => {
            eprintln!("Editor exited with non-zero status");
        }
        Err(e) => {
            eprintln!("Failed to open editor '{}': {}", editor, e);
            eprintln!("Set $EDITOR to your preferred editor");
        }
    }
}
```

### Step 3: Add /config edit to help text

In `src/help.rs`, update the `/config` help text to include the `edit` subcommand.

### Step 4: Add /config edit to tab completions

In `src/commands.rs`, if there's a config subcommand list for tab completion,
add `"edit"` to it.

### Tests

- Test that the edit subcommand path resolution works (project config preferred over user config)
- Test that when neither exists, user config path is returned as default
- No need to test the actual editor launch (that's OS-dependent)

## Verification

```bash
cargo build && cargo test
```
