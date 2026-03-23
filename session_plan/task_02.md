Title: Add /doctor command for environment diagnostics
Files: src/commands.rs, src/commands_project.rs, src/help.rs
Issue: none

## Context

Claude Code and other professional coding agents have built-in environment diagnostics. When something goes wrong (API key invalid, git not installed, config malformed), users need a single command to check everything. Currently yoyo has `/health` which just shows version and basic stats, but no real environment check.

`/doctor` should be the "is everything working?" command that developers run when they hit issues.

## Implementation

1. **In `src/commands_project.rs`**: Add a `handle_doctor()` function that runs a series of diagnostic checks and prints a report:

   ```
   🩺 yoyo doctor
   ─────────────────────────────
   ✓ Version: 0.1.2
   ✓ Git: installed (2.43.0)
   ✓ Git repo: yes (branch: main)
   ✓ Provider: anthropic
   ✓ API key: set (ANTHROPIC_API_KEY)
   ✓ Model: claude-sonnet-4-20250514
   ✓ Config file: .yoyo.toml (found)
   ✓ Project context: CLAUDE.md (47 lines)
   ✓ Curl: installed (for /docs and /web)
   ✗ Memory dir: .yoyo/ not found (run /remember to create)

   7/8 checks passed
   ```

   Checks to run:
   - **Version**: print current version from `VERSION` const
   - **Git**: run `git --version`, report installed/not found
   - **Git repo**: run `git rev-parse --is-inside-work-tree`, report branch if yes
   - **Provider**: show configured provider name
   - **API key**: check if the relevant env var is set (don't print the key!), show which env var
   - **Model**: show configured model name
   - **Config file**: check for `.yoyo.toml` and `~/.config/yoyo/config.toml`, report which found
   - **Project context**: check for YOYO.md, CLAUDE.md, .yoyo/instructions.md — report lines
   - **Curl**: run `curl --version`, needed for /docs and /web
   - **Memory dir**: check if .yoyo/ directory exists

   Use green ✓ for pass, red ✗ for fail, yellow ⚠ for warning (e.g., API key set but model might not match provider). Print summary count at end.

2. **In `src/commands.rs`**:
   - Add `/doctor` to `KNOWN_COMMANDS`
   - Add dispatch in the command handler: when input starts with `/doctor`, call `handle_doctor()`
   - The command takes the current `AgentConfig` fields needed (provider, model, api_key presence)

3. **In `src/help.rs`**:
   - Add `/doctor` to the help text with description: "Run environment diagnostics"
   - Add detailed help entry for `/help doctor`

4. **Tests** (in `commands_project.rs` test module):
   - `test_doctor_in_known_commands` — `/doctor` in KNOWN_COMMANDS
   - `test_doctor_in_help_text` — `/doctor` appears in help output
   - Create a `run_doctor_checks()` function that returns a `Vec<DoctorCheck>` struct (name, status enum: Pass/Fail/Warn, detail string) instead of printing directly — this makes it testable
   - `test_doctor_checks_version` — version check always passes
   - `test_doctor_checks_git` — git check detects git (it's installed in CI)
   - `test_doctor_checks_structure` — verify the check list is non-empty and every check has a name
