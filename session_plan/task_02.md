Title: Auto-remember successful build/test commands as project memories
Files: src/tools.rs, src/memory.rs
Issue: none

## What

When yoyo executes a bash command that looks like a build or test command and it succeeds, automatically save it as a project memory. This is the #1 closeable gap vs Claude Code, which automatically remembers build commands, test commands, and debugging insights across sessions.

## Why

Claude Code's auto-memory is called out in the assessment as the biggest closeable gap. Users expect their agent to remember what worked without being told to `/remember` it. Currently yoyo requires manual `/remember` for everything. Even a basic version — detecting successful build/test patterns — is a major UX improvement.

## Implementation

### In `src/memory.rs`:
1. Add a new function `pub fn auto_remember_if_novel(note: &str)` that:
   - Calls `load_memories()` to get current memories
   - Checks if any existing memory contains the same note text (exact match or substring)
   - If not found, calls `add_memory()` and `save_memories()` 
   - This is the deduplication gate — prevents saving "cargo test" 50 times

2. Add a new function `pub fn detect_auto_memory(command: &str, exit_code: i32) -> Option<String>` that:
   - Returns `None` if exit_code != 0 (only remember successes)
   - Checks if the command matches known build/test patterns:
     - `cargo build`, `cargo test`, `cargo clippy`, `cargo fmt`
     - `npm test`, `npm run build`, `yarn test`, `yarn build`
     - `python -m pytest`, `pytest`, `python setup.py test`
     - `make`, `make test`, `make build`
     - `go test`, `go build`
     - `mvn test`, `gradle test`
   - Returns `Some(formatted_note)` like `"Build command: cargo test (auto-detected)"` or `"Test command: npm test (auto-detected)"`
   - Only matches commands that START with these patterns (not arbitrary bash commands that happen to contain "test")

3. Add tests:
   - `detect_auto_memory("cargo test", 0)` → `Some("Test command: cargo test (auto-detected)")`
   - `detect_auto_memory("cargo test", 1)` → `None` (failed command)
   - `detect_auto_memory("echo hello", 0)` → `None` (not a build/test command)
   - `detect_auto_memory("cargo build --release", 0)` → `Some(...)` (with flags)
   - `auto_remember_if_novel` deduplication test

### In `src/tools.rs`:
1. In `StreamingBashTool`'s `execute` method (or wherever the bash result is produced), after getting the exit code:
   - Call `memory::detect_auto_memory(&command, exit_code)`
   - If it returns `Some(note)`, call `memory::auto_remember_if_novel(&note)`
   - Print a dim hint: `"  {DIM}📝 Auto-remembered: {note}{RESET}"`

2. This is a ~5-line addition at the point where bash results are returned.

## Key constraints

- **Deduplication is critical.** Without it, every `cargo test` run would add a duplicate memory. The `auto_remember_if_novel` function handles this.
- **Only successful commands.** Failed builds should NOT be remembered as "the build command."
- **Conservative pattern matching.** Only match well-known build/test command prefixes. Don't try to be clever about arbitrary commands.
- **No prompt changes.** The existing `format_memories_for_prompt` already includes all memories in the system prompt — auto-memories will appear there automatically.

## Tests

At minimum:
- Pattern detection for each supported ecosystem (cargo, npm, python, make, go)  
- Negative cases (random commands, failed commands)
- Deduplication gate
- Edge cases (empty command, command with pipes)
