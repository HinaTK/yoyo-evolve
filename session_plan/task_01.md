Title: Add /skill command for skill discovery and inspection
Files: src/commands.rs, src/commands_project.rs, src/help.rs
Issue: none

## Context

The #1 gap in CLAUDE_CODE_GAP.md is "Plugin / skills marketplace." Claude Code has
formal skill packs with discoverability and install commands. yoyo has `--skills <dir>`
(yoagent's `SkillSet`) but no way to list, inspect, or discover skills from within
the tool.

This task adds the first step: a `/skill` command with subcommands:
- `/skill list` — list all loaded skills with name and description
- `/skill show <name>` — show the full content of a named skill
- `/skill path` — show the current skills directory path

This is also wired as `yoyo skill list` / `yoyo skill show <name>` shell subcommands.

## Implementation

### In `src/commands_project.rs`:

Add `handle_skill()` function:

```rust
pub fn handle_skill(args: &str, skills_dir: Option<&str>) {
    let sub = args.trim();
    if sub.is_empty() || sub == "list" {
        // List all skills: scan skills_dir for directories containing SKILL.md
        // For each, parse YAML frontmatter to get name + description
        // Print formatted table: name, description
        // If no skills_dir configured, print helpful message about --skills flag
    } else if sub == "path" {
        // Print the current skills directory path (or "no skills directory configured")
    } else if sub.starts_with("show ") {
        let name = sub.strip_prefix("show ").unwrap().trim();
        // Find skills_dir/name/SKILL.md, read and print it
        // If not found, suggest /skill list
    } else {
        eprintln!("Unknown subcommand. Try: /skill list, /skill show <name>, /skill path");
    }
}
```

The function scans the skills directory for subdirectories containing `SKILL.md`,
parses the YAML frontmatter (between `---` markers) to extract `name` and `description`
fields, and formats the output with ANSI colors.

### In `src/commands.rs`:

- Add `"skill"` to `KNOWN_COMMANDS` array
- Add skill subcommands to `command_arg_completions` (list, show, path)
- Wire `/skill` dispatch in the command handler (pass skills_dir from config)

### In `src/help.rs`:

- Add help text for `/skill` command with subcommands
- Categorize under "Project" or "Configuration" group

### Shell subcommand wiring:

In `src/cli.rs` `try_dispatch_subcommand()`, add `"skill"` case that calls
`handle_skill()` and exits.

### Tests:

- Test that `handle_skill("list", Some("./skills"))` finds and lists the 7 core skills
- Test that `handle_skill("show evolve", Some("./skills"))` prints the evolve skill content  
- Test that `handle_skill("list", None)` prints a helpful message about --skills
- Test that `handle_skill("unknown", Some("./skills"))` prints error message

## Verification

```bash
cargo build && cargo test
# Manual: cargo run -- skill list --skills ./skills
```

## Docs

- Add `/skill` to help.rs command help
- Add `skill` to shell subcommands in help text
