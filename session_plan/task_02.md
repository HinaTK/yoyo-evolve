Title: Integrate RTK (Rust Token Killer) as optional bash command proxy
Files: src/tools.rs, src/cli.rs
Issue: #229

## Context

Issue #229 requests integration with RTK (https://github.com/rtk-ai/rtk), a CLI proxy that reduces 
LLM token consumption by 60-90% on common dev commands. Yuanhao (creator) explicitly asked for this 
in a follow-up comment — not just yoyo's internal compression, but RTK for real users whose usage 
patterns are unknown.

RTK is a standalone binary (`rtk`). It works by prefixing commands: `git status` → `rtk git status`. 
It supports 100+ commands including git, ls, find, grep, cargo, npm, etc. It outputs compressed, 
token-optimized versions of command output.

## Implementation

### In `src/tools.rs`:

1. Add a function `detect_rtk() -> bool` that checks if `rtk` is in PATH (cache the result in a 
   `OnceLock<bool>` so we only check once per session).

2. Add a function `maybe_prefix_rtk(command: &str) -> String` that:
   - Returns the command unchanged if RTK is not installed OR if RTK integration is disabled
   - Returns the command unchanged if it starts with `rtk` already  
   - Returns the command unchanged for commands RTK doesn't help with (e.g., `echo`, `cd`, `python`, 
     pipes with `|`, redirects, control flow `&&`/`||`/`;` at the top level)
   - Prefixes with `rtk` for supported commands: git, ls, find, grep, cat, head, tail, cargo, npm, 
     pip, docker, kubectl, gh, tree, diff, du, wc, ps, and other commands from RTK's supported list
   - Only prefix simple commands (no complex shell expressions)

3. In `StreamingBashTool::execute`, after safety checks but before spawning the command, call 
   `maybe_prefix_rtk(command)` and use the result.

### In `src/cli.rs`:

4. Add a `--no-rtk` flag that disables RTK integration even when installed. Store this as a global 
   flag accessible by the tools module (similar to `is_verbose()`).

5. When RTK is detected on first command execution, print a brief info message to stderr: 
   `"📦 RTK detected — using compressed output (disable with --no-rtk)"` (only once per session).

### Tests:

- Test `detect_rtk()` returns false in CI (RTK likely not installed)
- Test `maybe_prefix_rtk("git status")` returns `"rtk git status"` when RTK is enabled
- Test `maybe_prefix_rtk("echo hello")` returns unchanged
- Test `maybe_prefix_rtk("rtk git status")` returns unchanged (no double prefix)
- Test complex commands with pipes/semicolons are NOT prefixed
- Test `--no-rtk` flag disables prefixing

## Verification

- `cargo build && cargo test`
- `cargo clippy --all-targets -- -D warnings`
- Without RTK installed: behavior unchanged (all tests pass, no RTK messages)
- With RTK installed: commands get transparently prefixed
