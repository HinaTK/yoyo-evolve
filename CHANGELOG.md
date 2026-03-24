# Changelog

All notable changes to **yoyo-agent** (`cargo install yoyo-agent`) are documented here.

This project is a self-evolving coding agent — every change was planned, implemented, and tested by yoyo itself during automated evolution sessions. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] — 2026-03-24

Feature release adding file watching, structural search, refactoring tools, and piped-mode improvements — built across Days 22–24.

### Added

- **`/watch <command>`** — auto-run tests after every agent turn that modifies files (Day 23)
- **`/ast <pattern>`** — structural code search via ast-grep integration, graceful fallback when `sg` not installed (Day 24)
- **`/refactor` umbrella** — groups `/extract`, `/rename`, `/move` under one discoverable entry (Day 23)
- **`rename_symbol` agent tool** — model can do project-wide renames in a single tool call (Day 23)
- **Terminal bell notification** — rings `\x07` after operations >3s; disable with `--no-bell` or `YOYO_NO_BELL=1` (Day 23)
- **`system_prompt` and `system_file` keys** in `.yoyo.toml` config (Day 23)
- **Git-aware system prompt** — agent automatically sees current branch and dirty-file status (Day 23)

### Improved

- **Per-turn `/undo`** — undo individual agent turns instead of all-or-nothing (Day 22)
- **Onboarding wizard** — added Cerebras provider, XDG user-level config path option (Day 22)
- **Streaming latency** — tighter flush logic for digit-word and dash-word patterns (Day 23)

### Fixed

- **Suppressed partial tool output in piped/CI mode** — eliminates ~6500 noise lines from CI logs ([#172](https://github.com/yologdev/yoyo-evolve/issues/172))
- **Reduced tool output truncation** from 30K to 15K chars in piped mode — cuts context growth rate to prevent 400 errors ([#173](https://github.com/yologdev/yoyo-evolve/issues/173))

## [0.1.2] — 2026-03-22

Feature release adding per-command help, inline file mentions, new commands, and polished rendering — built across Days 20–22.

### Added

- **Per-command `/help <command>`** — detailed usage, examples, and flags for any slash command (Day 21)
- **`/grep` command** — direct file search from the REPL without an API round-trip (Day 21)
- **`/git stash` subcommand** — `save`, `pop`, `list`, `apply`, `drop` for git stash management (Day 21)
- **Inline `@file` mentions** — `@path` in prompts expands to file contents; supports line ranges `@file:10-20` and image files (Day 21)
- **First-run welcome & setup guide** — detects first run, shows welcome message, guides API key and model configuration (Day 22)
- **Visual section headers** — output hierarchy with section dividers for clearer structure (Day 22)

### Improved

- **Markdown rendering** — lists, italic, blockquotes, and horizontal rules now render properly with ANSI formatting (Day 21)
- **`/diff` with inline colored patches** — diff output shows +/- lines with red/green highlighting (Day 22)
- **Code block streaming** — token-by-token instead of line-buffered; tokens now flow immediately during code output (Day 21)
- **Architecture documentation** — Mermaid diagrams added to mdbook docs (Day 21)
- **`run_git()` helper deduplication** — consolidated repeated git command patterns into shared helper (Day 20)
- **`configure_agent()` provider setup deduplication** — cleaned up provider configuration logic (Day 20)
- **Tool output summaries** — richer context for `read_file`, `edit_file`, `search`, and `bash` tool results (Day 21)

### Fixed

- **Code block streaming buffering** — tokens inside code blocks now flow immediately instead of buffering entire lines (Day 21)
- **Missing transition separator** — added separator between thinking output and text response sections (Day 22)

## [0.1.1] — 2026-03-20

Bug fix release addressing two community-reported issues.

### Fixed

- **Image support broken via `/add`** — images added with `/add photo.png` were base64-encoded but injected as plain text content blocks instead of proper image content blocks, so the model couldn't actually see them. Now `/add` detects image files (JPEG, PNG, GIF, WebP) and sends them as real image blocks the model can interpret. Closes [#138](https://github.com/yologdev/yoyo-evolve/issues/138).
- **Streaming output appeared all at once** — three root causes fixed: (1) spinner stop had a race condition that could prevent the clear sequence from executing, now clears synchronously; (2) thinking tokens went to stdout causing interleaving with text, now routed to stderr; (3) no separator between thinking and text output, now inserts a newline on transition. Also reduced the line-start resolve threshold so common short first tokens flush immediately. Closes [#137](https://github.com/yologdev/yoyo-evolve/issues/137).

## [0.1.0] — 2026-03-19

The initial release. Everything below was built from scratch over 19 days of autonomous evolution, starting from a 200-line CLI example.

### Added

#### Core Agent Loop
- **Streaming text output** — tokens stream to the terminal as they arrive, not after completion
- **Multi-turn conversation** with full history tracking
- **Thinking/reasoning display** — extended thinking shown dimmed below responses
- **Automatic API retry** with exponential backoff (3 retries via yoagent)
- **Rate limit handling** — respects `retry-after` headers on 429 responses
- **Parallel tool execution** via yoagent 0.6's `ToolExecutionStrategy::Parallel`
- **Subagent spawning** — `/spawn` delegates focused tasks to a child agent with scoped context
- **Tool output streaming** — `ToolExecutionUpdate` events shown as they arrive

#### Tools
- `bash` — run shell commands with interactive confirmation
- `read_file` — read files with optional offset/limit
- `write_file` — create or overwrite files with content preview
- `edit_file` — surgical text replacement with colored inline diffs (red/green removed/added lines)
- `search` — regex-powered grep across files
- `list_files` — directory listing with glob filtering

#### REPL & Interactive Features
- **Interactive REPL** with rustyline — arrow keys, Ctrl-A/E/K/W, persistent history (`~/.local/share/yoyo/history`)
- **Tab completion** — slash commands, file paths, and argument-aware suggestions (model values, git subcommands, `/pr` subcommands)
- **Multi-line input** via backslash continuation and fenced code blocks
- **Markdown rendering** — incremental ANSI formatting: headers, bold, italic, code blocks with syntax-labeled headers, horizontal rules
- **Syntax highlighting** — language-aware ANSI coloring for Rust, Python, JS/TS, Go, Shell, C/C++, JSON, YAML, TOML
- **Braille spinner** animation while waiting for AI responses
- **Conversation bookmarks** — `/mark`, `/jump`, `/marks` to name and revisit points in a conversation
- **Conversation search** — `/search` with highlighted matches in results
- **Fuzzy file search** — `/find` with scoring, git-aware file listing, top-10 ranked results
- **Direct shell escape** — `/run <cmd>` and `!<cmd>` execute commands without an API round-trip
- **Elapsed time display** after each response, plus per-tool execution timing (`✓ (1.2s)`)

#### Git Integration
- Git branch display in REPL prompt
- `/diff` — full `git status` plus diff, with file-level insertion/deletion summary
- `/commit` — AI-generated commit messages from staged changes
- `/undo` — revert last commit, including cleanup of untracked files
- `/git` — shortcuts for `status`, `log`, `diff`, `branch`
- `/pr` — full PR workflow: `list`, `view`, `create [--draft]`, `diff`, `comment`, `checkout`
- `/review` — AI-powered code review of staged/unstaged changes against main
- `/changes` — show files modified (written/edited) during the current session

#### Project Tooling
- `/health` — run full build/test/clippy/fmt diagnostic for Rust, Node, Python, Go, and Make projects
- `/fix` — run the check gauntlet and auto-apply fixes for failures
- `/test` — auto-detect project type and run the right test command
- `/lint` — auto-detect project type and run the right linter
- `/init` — scan project structure and generate a starter YOYO.md context file
- `/index` — build a lightweight codebase index: file counts, language breakdown, key files
- `/docs` — quick documentation/API lookup without leaving the REPL
- `/tree` — project structure visualization

#### Session Management
- `/save` and `/load` — persist and restore conversation sessions as JSON
- `--continue/-c` — auto-load the most recent session on startup
- **Auto-save on exit** — sessions saved automatically on clean exit and crash recovery
- **Auto-compaction** at 80% context window usage, plus manual `/compact`
- `/tokens` — visual token usage bar with percentage
- `/cost` — per-model input/output/cache pricing breakdown
- `/status` — show current session state

#### Context & Memory
- **Project context files** — auto-loads YOYO.md, CLAUDE.md, and `.yoyo/instructions.md`
- **Git-aware context** — recently changed files injected into system prompt
- **Codebase indexing** — `/index` summarizes project structure for the agent
- **Project memories** — `/remember`, `/memories`, `/forget` for persistent cross-session notes stored in `.yoyo/memory.json`

#### Configuration
- **Config file support** — `.yoyo.toml` (per-project) and `~/.config/yoyo/config.toml` (global)
- `--model` / `/model` — select or switch models mid-session
- `--provider` / `/provider` — switch between 11 provider backends mid-session (Anthropic, OpenAI, Google, Ollama, z.ai, and more)
- `--thinking` / `/think` — toggle extended thinking level
- `--temperature` — sampling randomness control (0.0–1.0)
- `--max-tokens` — cap response length
- `--max-turns` — limit agent turns per prompt (useful for scripted runs)
- `--system` / `--system-file` — custom system prompts
- `--verbose/-v` — show full tool arguments and result previews
- `--output/-o` — pipe response to a file
- `--api-key` — pass API key directly instead of relying on environment
- `/config` — display all active settings

#### Permission System
- **Interactive tool approval** — confirm prompts for `bash`, `write_file`, and `edit_file` with content/diff preview
- **"Always" option** — persists per-session via `AtomicBool`, so you only approve once
- `--yes/-y` — auto-approve all tool executions
- `--allow` / `--deny` — glob-based allowlist/blocklist for tool patterns
- `--allow-dir` / `--deny-dir` — directory restrictions with canonicalized path checks preventing traversal
- `[permissions]` and `[directories]` config file sections
- Deny-overrides-allow policy

#### Extensibility
- **MCP server support** — `--mcp` connects to MCP servers via stdio transport
- **OpenAPI tool loading** — `--openapi <spec>` registers tools from OpenAPI specifications
- **Skills system** — `--skills <dir>` loads markdown skill files with YAML frontmatter

#### CLI Modes
- **Interactive REPL** — default mode with full feature set
- **Single-shot prompt** — `--prompt/-p "question"` for one-off queries
- **Piped/stdin mode** — reads from stdin when not a TTY, auto-disables colors
- **Color control** — `--no-color` flag, `NO_COLOR` env var, auto-detection for non-TTY

#### Other
- `--help` / `--version` / `/version` — CLI metadata
- `/help` — grouped command reference (Navigation, Git, Project, Session, Config)
- **Ctrl+C handling** — graceful interrupt
- **Unknown flag warnings** — instead of silent ignoring
- **Unambiguous prefix matching** for slash commands (with greedy-match fix)

### Architecture

The codebase evolved from a single 200-line `main.rs` to 12 focused modules (~17,400 lines):

| Module | Lines | Responsibility |
|--------|-------|----------------|
| `main.rs` | ~1,470 | Entry point, tool building, `AgentConfig`, model config |
| `cli.rs` | ~2,360 | CLI argument parsing, config file loading, conversation bookmarks |
| `commands.rs` | ~2,990 | Slash command dispatch and grouped `/help` |
| `commands_git.rs` | ~1,190 | Git commands: `/diff`, `/commit`, `/pr`, `/review`, `/changes` |
| `commands_project.rs` | ~1,950 | Project commands: `/health`, `/fix`, `/test`, `/lint`, `/init`, `/index` |
| `commands_session.rs` | ~465 | Session commands: `/save`, `/load`, `/compact`, `/tokens`, `/cost` |
| `docs.rs` | ~520 | `/docs` crate API lookup |
| `format.rs` | ~3,280 | Output formatting, ANSI colors, markdown rendering, syntax highlighting, cost tracking |
| `git.rs` | ~790 | Git operations: branch detection, diff handling, PR interactions |
| `memory.rs` | ~375 | Project memory system (`.yoyo/memory.json`) |
| `prompt.rs` | ~1,090 | System prompt construction, project context assembly |
| `repl.rs` | ~880 | REPL loop, input handling, tab completion |

### Testing

- **800 tests** (733 unit + 67 integration)
- Integration tests run the actual binary as a subprocess — dogfooding real invocations
- Coverage includes: CLI flag validation, command parsing, error quality, exit codes, output formatting, edge cases (1000-char model names, Unicode emoji in arguments), project type detection, fuzzy scoring, health checks, git operations, session management, markdown rendering, cost calculation, permission logic, and more
- Mutation testing infrastructure via `cargo-mutants` with threshold-based pass/fail

### Documentation

- **mdbook guide** at `docs/book/` covering installation, all CLI flags, every REPL command, multi-line input, models, system prompts, thinking, skills, sessions, context management, git integration, cost tracking, troubleshooting, and permissions
- Landing page at `docs/index.html`
- In-code `/help` with grouped categories

### Evolution Infrastructure

- **3-phase evolution pipeline** (`scripts/evolve.sh`): plan → implement → communicate
- **GitHub issue integration** — reads community issues, self-filed issues, and help-wanted labels
- **Journal** (`JOURNAL.md`) — chronological log of every evolution session
- **Learnings** (`memory/learnings.jsonl`) — self-reflections archive (JSONL, append-only with timestamps and source attribution)
- **Skills** — structured markdown guides for self-assessment, evolution, communication, research, release, and social interaction
- **CI** — build, test, clippy (warnings as errors), fmt check on every push/PR

---

### Development Timeline

| Day | Highlights |
|-----|-----------|
| 0 | Born — 200-line CLI on yoagent |
| 1 | Panic fixes, `--help`/`--version`, multi-line input, `/save`/`/load`, Ctrl+C, git branch prompt, custom system prompts |
| 2 | Tool execution timing, `/compact`, `/undo`, `--thinking`, `--continue`, `--prompt`, auto-compaction, `format_token_count` fix |
| 3 | mdbook documentation, `/model` UX fix |
| 4 | Module split (cli, format, prompt), `--max-tokens`, `/version`, `NO_COLOR`, `--no-color`, `/diff` improvements, `/undo` cleanup |
| 5 | `--verbose`, `/init`, `/context`, YOYO.md/CLAUDE.md project context, `.yoyo.toml` config files, Claude Code gap analysis |
| 6 | `--temperature`, `/health`, `/think`, `--api-key`, `/cost` breakdown, `--max-turns`, partial tool streaming, CLI hardening |
| 7 | `/tree`, `/pr`, project file context in prompt, retry logic, `/search`, `/run` and `!` shell escape, mutation testing setup |
| 8 | Rustyline + tab completion, markdown rendering, file path completion, `/commit`, `/git`, spinner, multi-provider + MCP support |
| 9 | yoagent 0.6.0, `--openapi`, `/fix`, `/git diff`/`branch`, "always" confirm fix, multi-language `/health`, YOYO.md identity, safety docs |
| 10 | Integration tests (subprocess dogfooding), syntax highlighting, `/docs`, git module extraction, docs module extraction, commands module extraction, 49 subprocess tests |
| 11 | Main.rs extraction (3,400→1,800 lines), PR dedup, timing tests |
| 12 | `/test`, `/lint`, search highlighting, `/find`, git-aware context, code block highlighting, `AgentConfig`, `repl.rs` extraction, `/spawn` |
| 13 | `/review`, `/pr create`, `/init` onboarding, smarter `/diff`, main.rs final cleanup (770 lines) |
| 14 | Colored edit diffs, conversation bookmarks (`/mark`, `/jump`), argument-aware tab completion, `/index` codebase indexing |
| 15 | Permission prompts (all tools), project memories (`/remember`, `/memories`, `/forget`), module split (commands→4 files), grouped `/help`, `/provider` |
| 16 | Auto-save sessions on exit, crash recovery, documentation overhaul, CHANGELOG.md |
| 17 | True token-by-token streaming fix, multi-provider cost tracking (7 providers), crates.io package rename, pluralization fix, `/changes` command |
| 18 | z.ai (Zhipu AI) provider support, test backfill for `commands_git` and `commands_project` (1,118 lines of tests) |
| 19 | Published to crates.io as v0.1.0 🎉 |
| 20 | `run_git()` dedup, `configure_agent()` dedup, context overflow auto-recovery, v0.1.1 bug fix release |
| 21 | Per-command `/help <cmd>`, `/grep`, `/git stash`, inline `@file` mentions, markdown rendering (lists, italic, blockquotes), code block streaming fix, tool output summaries, architecture docs |
| 22 | First-run welcome & setup guide, `/diff` inline colored patches, visual section headers, v0.1.2 release |
| 23 | `/watch` auto-test, `/refactor` umbrella, `rename_symbol` tool, terminal bell, `system_prompt`/`system_file` config, git-aware prompt, streaming flush improvements |
| 24 | `/ast` structural search, piped-mode output fixes, v0.1.3 release |

[0.1.3]: https://github.com/yologdev/yoyo-evolve/releases/tag/v0.1.3
[0.1.2]: https://github.com/yologdev/yoyo-evolve/releases/tag/v0.1.2
[0.1.1]: https://github.com/yologdev/yoyo-evolve/releases/tag/v0.1.1
[0.1.0]: https://github.com/yologdev/yoyo-evolve/releases/tag/v0.1.0
