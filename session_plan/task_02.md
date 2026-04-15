Title: Extract parse_args into grouped helper functions
Files: src/cli.rs
Issue: none

## What to do

`parse_args` is 409 lines (lines 851-1260) — the largest single function in the codebase. It parses CLI flags sequentially. Extract logical groups into private helper functions within cli.rs to improve readability.

### Extraction targets

Group the flag-parsing logic into 3-4 helpers. Suggested groupings:

1. **`parse_model_config(args, file_config) -> (provider, model, api_key, base_url, fallback_provider, fallback_model)`**
   - Provider selection and validation (~lines 910-930)
   - Base URL (~line 926)
   - API key resolution (flag → provider env → ANTHROPIC_API_KEY → config file → setup wizard) (~lines 964-1010)
   - Model selection (~lines 1010-1020)
   - Fallback provider and model (~lines near end)

2. **`parse_permission_config(args, raw_config_content) -> (PermissionConfig, DirectoryRestrictions)`**
   - --allow/--deny patterns (~lines 1110-1130)
   - --allow-dir/--deny-dir (~lines 1140-1160)
   - Merging with config file defaults

3. **`parse_mcp_config(args, file_config, raw_config_content) -> (Vec<String>, Vec<McpServerConfig>, Vec<String>)`**
   - --mcp flags + config file merge
   - --openapi flags
   - Structured [mcp_servers.*] parsing

4. **`parse_output_flags(args, file_config) -> OutputFlags`** (or just return a tuple)
   - --verbose, --yes, --auto-commit, --no-update-check, --json, --audit, --print-system-prompt
   - These are all simple boolean flags, currently scattered through lines 1085-1110

### Approach

- Create the helper functions as `fn parse_xxx(args: &[String], ...) -> ...` — private functions in cli.rs
- Use tuples for return values if the group is small (3-4 items). Use a small struct if 5+.
- Move the logic out of `parse_args` into the helpers. `parse_args` calls each helper and assembles the final `Config`.
- Do NOT rename or change any public API. The `parse_args` function signature stays the same.
- Do NOT change behavior — this is a pure refactor. Every flag should work exactly as before.

### What NOT to do

- Don't touch any other source files
- Don't add new features or flags
- Don't change the Config struct
- Don't break any existing tests (there are tests for parse_args behavior)

### Verification
- `cargo build`
- `cargo test` (especially any tests in cli.rs that exercise parse_args)
- `cargo clippy --all-targets -- -D warnings`
- `cargo fmt -- --check`
