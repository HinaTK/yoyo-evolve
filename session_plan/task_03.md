Title: Add /providers command listing all providers with API key status
Files: src/commands_info.rs, src/repl.rs
Issue: none

## What to do

Add a `/providers` command that lists all supported providers with their default model, API key environment variable, and whether the key is currently set. This helps users (especially fork owners choosing a provider) see at a glance what's available and configured.

### Changes to `src/commands_info.rs`:

1. Add import for `default_model_for_provider` and `provider_api_key_env` from `crate::providers` (check what's already imported — `KNOWN_PROVIDERS` is imported from `crate::cli`).

2. Add a new public function:

```rust
pub fn handle_providers() {
    println!("{DIM}  Supported providers:\n");
    for provider in KNOWN_PROVIDERS {
        if *provider == "custom" { continue; }
        let default_model = default_model_for_provider(provider);
        let env_var = provider_api_key_env(provider);
        let key_status = match env_var {
            Some(var) if std::env::var(var).is_ok() => format!("{GREEN}✓ set{RESET}{DIM}"),
            Some(var) => format!("{RED}✗ not set{RESET}{DIM} ({var})"),
            None if *provider == "ollama" => format!("{GREEN}✓ local{RESET}{DIM}"),
            None => format!("{YELLOW}? unknown{RESET}{DIM}"),
        };
        println!("    {BOLD}{provider}{RESET}{DIM}");
        println!("      default: {default_model}");
        println!("      key:     {key_status}");
        println!();
    }
    println!("  Switch with: /provider <name>{RESET}\n");
}
```

3. Add tests:
   - `test_handle_providers_no_panic` — call `handle_providers()` and verify no panic
   - `test_handle_providers_source_lists_known_providers` — source-level check that the function iterates KNOWN_PROVIDERS

### Changes to `src/repl.rs`:

1. Find where `/provider` is dispatched (around line 501-502) and add a new match arm BEFORE it:

```rust
"/providers" => {
    commands::handle_providers();
    continue;
}
```

This goes in the match block where other slash commands are dispatched. It should be placed before the `/provider` arm (since `/providers` is more specific and Rust match arms are checked in order — but since these are exact string matches, order doesn't matter as long as both arms exist).

### Important constraints:
- Only 2 source files: commands_info.rs and repl.rs
- Pure additive — no existing behavior changes
- The function uses only existing imports (KNOWN_PROVIDERS, provider_api_key_env, default_model_for_provider, color constants)
- No changes to help.rs or commands.rs in this task (those are follow-ups)
