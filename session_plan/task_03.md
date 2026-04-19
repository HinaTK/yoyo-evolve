Title: Add /explain command for AI-powered code explanation
Files: src/commands_file.rs, src/repl.rs, src/commands.rs
Issue: none

## What to do

Add a `/explain` command that reads code from a file (with optional line range) and
sends it to the agent with a clear "explain this code" prompt. This is a natural
developer workflow command — you're staring at unfamiliar code, you want to understand
it quickly.

### In `src/commands_file.rs`:

Add a new public function:

```rust
pub fn build_explain_prompt(input: &str) -> Option<String>
```

This function:
1. Parses the argument after `/explain` — expects a file path with optional line range
   (same format as `/add`: `path/to/file.rs:10-50`)
2. Uses the existing `parse_add_arg()` to extract path and optional range
3. Reads the file (or just the specified lines)
4. Returns `Some(prompt)` where prompt is:
   ```
   Explain the following code from `{filename}` (lines {start}-{end}):
   
   ```{language}
   {code}
   ```
   
   Focus on: what it does, how it works, any notable patterns or potential issues.
   ```
5. Returns `None` if file doesn't exist or args are empty (after printing usage)
6. Detect language from file extension for the code fence (reuse `detect_language` from
   `commands_map.rs` if accessible, otherwise just use the extension directly)

Print usage when called with no arguments:
```
  usage: /explain <file>[:<start>-<end>]
  Read code from a file and ask the agent to explain it.
  Example: /explain src/main.rs:50-100
```

### In `src/repl.rs`:

Add dispatch for `/explain`:
```rust
s if s.starts_with("/explain") => {
    if let Some(prompt) = commands::build_explain_prompt(input) {
        last_input = Some(prompt.clone());
        let outcome = run_prompt_with_changes(
            &mut agent, &prompt, &mut session_total, &agent_config.model, &session_changes,
        ).await;
        // ... same pattern as /plan dispatch
    }
    continue;
}
```

### In `src/commands.rs`:

Add `"/explain"` to the `KNOWN_COMMANDS` array (single line addition).

### Tests in `src/commands_file.rs`:

- `build_explain_prompt` with a real file returns Some with code content
- `build_explain_prompt` with nonexistent file returns None  
- `build_explain_prompt` with line range includes only those lines
- `build_explain_prompt` with empty input returns None

Total scope: ~80-120 new lines + tests. 3 files touched.
