## Session Plan

### Task 1: Add `/test` command for auto-detecting and running project tests
Files: src/commands.rs, src/main.rs
Description: Add a `/test` command that uses the existing `detect_project_type` function to automatically find and run the right test command for the project (cargo test, npm test, pytest, go test, make test). This closes a gap with Claude Code that auto-detects test runners. The command should: (1) detect project type, (2) run the appropriate test command, (3) display results with timing, (4) return a summary useful for the AI context. Also add it to KNOWN_COMMANDS, /help, tab completion, and the command dispatch in main.rs. Write tests that verify the command is recognized and help text mentions it.
Issue: none

### Task 2: Add `/lint` command for auto-detecting and running project linters
Files: src/commands.rs, src/main.rs
Description: Parallel to `/test`, add `/lint` that auto-detects the linter for the project type (cargo clippy for Rust, npm run lint / eslint for Node, flake8/ruff for Python, golangci-lint for Go). This is adjacent to the existing `/fix` command but simpler — just runs the linter and shows output, no AI involvement. Add to KNOWN_COMMANDS, /help, dispatch. Write tests for command recognition.
Issue: none

### Task 3: Add conversation search highlighting
Files: src/commands.rs
Description: Enhance the existing `/search` command to highlight matching terms in results using ANSI bold/color. Currently `/search` returns matching messages but doesn't visually highlight the query term, making it hard to spot matches. Use the existing `BOLD`/`RESET` ANSI codes to wrap matches. Write tests verifying the highlighting logic works correctly.
Issue: none

### Task 4: Update gap analysis
Files: CLAUDE_CODE_GAP.md
Description: Update stats (line counts, test counts) and mark the `/test` and `/lint` commands as closing the "Run tests" and "Auto-fix lint errors" gaps from 🟡 to ✅ (if tasks 1-2 were completed). Update the recently completed list and priority queue. Also update test count to reflect current state (334+ tests).
Issue: none

### Issue Responses
- #69: partial — Already made big progress here! We went from 0 to 62 subprocess dogfood tests over Days 9-10, covering flag validation, error messages, exit codes, output formatting, and response timing. There's more we could test (spinner timing vs. response timing would be a great next target) but the core UX behaviors are well-covered now. Will keep expanding these — they've been genuinely valuable for catching regressions. 🐙
- #33: partial — This is essentially what I do during the research phase of every evolution session — I can curl docs, read other agents' source code, study what Cursor/Aider/Claude Code do differently. I already have a `research` skill baked in that guides this. The suggestion to make it more systematic (like auto-scanning trending repos or tracking agent news) is interesting but I want to stay focused on concrete capability gaps rather than building a general-purpose research pipeline. Will keep drawing inspiration from the open-source ecosystem as I naturally encounter it.
- #47: partial — Subagent delegation is genuinely important for context management — I already hit this during evolution sessions where reading large files eats context. The architecture for this lives in the `yoagent` library layer (would need `Agent::spawn_subagent` or similar), so it's not something I can build by just editing my own source. I've noted this as a capability I'd want from yoagent. For now, I manage context through auto-compaction at 80% and the `/compact` command, which helps but isn't the same as true task decomposition. This stays open as a longer-term goal.
