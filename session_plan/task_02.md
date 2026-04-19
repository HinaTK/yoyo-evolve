Title: Enrich /status with context info and add /context tokens subcommand
Files: src/commands_info.rs, src/commands_project.rs
Issue: none

## What to do

Two small improvements that help users understand where their token budget is going.

### Part A: Add context usage to `/status` (in `src/commands_info.rs`)

The current `handle_status` function shows model, git branch, cwd, session elapsed, and
token counts — but NOT how much of the context window is used. Add context usage info.

Modify `handle_status` to accept two additional parameters: `context_used: u64` and
`context_max: u64`. Then add a line like:

```
  context: 45,231 / 200,000 tokens (23%)
```

Use `format_token_count()` from `format/cost.rs` for nice formatting.
Color the percentage using `context_usage_color()`.

Update all call sites of `handle_status` (likely in `src/repl.rs` and `src/cli.rs` — 
check with grep). The callers already have access to the agent, so they can compute
`total_tokens(agent.messages())` and `effective_context_tokens()`.

NOTE: If updating call sites would push this past 3 files, just add a default of 0/0
that skips the context line, and update the call site in repl.rs only (the main place
users invoke /status).

### Part B: Add `/context tokens` subcommand (in `src/commands_project.rs`)

Extend `handle_context` to recognize the `tokens` subcommand. When invoked:

1. Show system prompt estimated tokens (use `estimate_tokens()` which already exists in
   `commands_project.rs` — it does word_count * 1.3)
2. Show conversation message count and total tokens (from agent.messages())
3. Show context limit and percentage used
4. Show estimated remaining tokens

The function signature needs to accept `agent: &Agent` (or just the messages + token counts).

Add `"tokens"` to `context_subcommands()`.

Add tests for:
- Token estimation output format
- Context subcommand routing

Total scope: ~60-80 new lines + tests.
