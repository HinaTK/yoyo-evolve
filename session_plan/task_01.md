Title: /update command — self-update from GitHub releases (Issue #234)
Files: src/commands_dev.rs, src/commands.rs, src/help.rs
Issue: #234

## What to build

Add a `/update` command that downloads the latest yoyo release from GitHub and replaces the current binary in-place. This pairs with the startup update notification shipped in Day 32 (Issue #233).

## Implementation details

### In `commands_dev.rs` — add `handle_update()` function

The function should:

1. **Check current version** — use `env!("CARGO_PKG_VERSION")` or the existing `VERSION` constant from `cli.rs`
2. **Fetch latest release from GitHub** — `curl -sL "https://api.github.com/repos/yologdev/yoyo-evolve/releases/latest"` with a 10s timeout. Parse the JSON to get tag_name and assets list.
3. **Compare versions** — reuse the `version_is_newer()` function from `cli.rs` (it already exists for the update notification). If already on latest, print "Already on the latest version (v0.1.5). No update needed." and return.
4. **Detect platform** — determine the right asset name:
   - Linux x86_64: `yoyo-x86_64-unknown-linux-gnu.tar.gz`
   - macOS Intel: `yoyo-x86_64-apple-darwin.tar.gz`
   - macOS ARM: `yoyo-aarch64-apple-darwin.tar.gz`
   - Windows: `yoyo-x86_64-pc-windows-msvc.zip`
   Use `std::env::consts::OS` and `std::env::consts::ARCH` to detect.
5. **Show confirmation prompt** — "Update yoyo from v0.1.5 to v0.2.0? [y/N]" — require explicit 'y'. In non-interactive (piped) mode, skip the prompt or require `--yes` is not needed (just print instructions instead).
6. **Download the asset** — use `curl -fSL <url> -o /tmp/yoyo-update.tar.gz` (or .zip on Windows)
7. **Extract the binary** — `tar xzf` on Unix, skip on Windows (print manual instructions for now)
8. **Get current binary path** — `std::env::current_exe()` to find where yoyo is installed
9. **Backup current binary** — rename current to `<path>.bak`
10. **Replace** — move extracted binary to current path, `chmod +x` on Unix
11. **Print success** — "Updated to v0.2.0! Restart yoyo to use the new version."
12. **On failure** — restore from backup, print error, suggest manual install: `curl -fsSL https://raw.githubusercontent.com/yologdev/yoyo-evolve/main/install.sh | bash`

### In `commands.rs` — add dispatch

Add `/update` to the KNOWN_COMMANDS list and add a match arm in the command dispatch that calls `handle_update()`. The command takes no arguments.

### In `help.rs` — add help text

Add `/update` to the help system with description: "Check for and install the latest version of yoyo"

Under the "Development" category (near `/doctor`, `/health`).

### Tests

Write tests in `commands_dev.rs`:
- `test_update_version_check` — test that the version comparison logic works (reuse `version_is_newer`)
- `test_update_platform_detection` — test that platform detection returns valid asset names for known OS/ARCH combos
- `test_update_already_latest` — test the early-return path when current == latest
- Don't test actual download/replace in unit tests — those are integration-level concerns

### Edge cases
- No internet / GitHub unreachable → graceful error with fallback suggestion
- Permission denied on binary replacement → catch error, restore backup, suggest `sudo` or manual install
- Running from cargo (development) vs installed binary → detect and suggest `cargo install yoyo-agent` instead
- Non-interactive mode → print "Run `/update` in interactive mode" or provide the curl command

### Docs
- Add `/update` to `docs/src/usage/commands.md` if that file lists commands
- No CLAUDE.md changes needed (command list updates are implicit)
