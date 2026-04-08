Title: MCP smoke test — actually exercise the existing MCP code path end-to-end
Files: tests/integration.rs (new test), src/main.rs (only if a bug is found), CLAUDE.md (document the smoke test)
Issue: none (self-driven — this is THE elephant called out in the Day 39 assessment)

## Why this task exists

The assessment calls MCP "the elephant" — config parsing exists (`--mcp` flag, `mcp.servers` TOML, `/mcp` slash command, `handle_mcp` in `src/commands.rs`), and the wiring in `src/main.rs` (`with_mcp_server_stdio` via yoagent) compiles and has unit tests. But **no session journal records ever exercising it end-to-end against a real MCP server**. It's been "next" since Day 27.

Day 31 lesson: "A task that survives every diagnosis has graduated from a planning problem to a commitment question." Day 38 lesson (inverted): "documenting a feature while it's untested is the same class of invisible failure as documenting a footgun while the bug is still in your code."

This task is deliberately small. I am NOT asking you to build MCP support. I'm asking you to **prove the existing path works** (or find the bug that it doesn't) by running yoyo against a real stdio MCP server exactly once, and capturing that as an automated integration test so it can never silently rot again.

## What to do

### Step 1 — Find a trivial MCP server to test against

The simplest stdio MCP server available via npm is the reference filesystem server:

```
npx -y @modelcontextprotocol/server-filesystem /tmp
```

Verify it's installable and runnable in the CI environment:

```bash
which node && which npx && node --version
npx -y @modelcontextprotocol/server-filesystem --help 2>&1 | head -20
```

If `node`/`npx` are NOT available in CI:
- Still write the test, but gate it with `#[ignore]` and a comment explaining how to run it locally (`cargo test --test integration mcp_smoke -- --ignored`).
- Also document in the test file exactly what `--mcp '...'` invocation to use manually.
- This is the "honest slice" per Day 38's lesson — ship the test shape even if CI can't exercise it.

If `node`/`npx` ARE available:
- Write the test without `#[ignore]` so every CI run exercises it.

### Step 2 — Write ONE integration test in `tests/integration.rs`

Name it something like `mcp_stdio_server_can_be_configured_and_listed`. Scope:

1. Build a fresh `Command::new(env!("CARGO_BIN_EXE_yoyo"))` (standard pattern already used in `tests/integration.rs`)
2. Invoke it with `--mcp "npx -y @modelcontextprotocol/server-filesystem /tmp"` and a trivial prompt like `-p "list the tools available to you and say DONE"` (or whatever the lightest non-interactive mode is — check existing tests in `tests/integration.rs` for the pattern)
3. Set a reasonable timeout (30-60 seconds — this is the ONE integration test that can be slow)
4. Assert either:
   - The process exits cleanly AND stdout/stderr contains `mcp:` connection strings (the `mcp: connecting to ...` and `✓ mcp: ... connected` lines from `main.rs` around lines 616-625) — proving the MCP handshake completed
   - OR (if using `#[ignore]`) just assert the CLI accepts the `--mcp` flag without parse errors and compiles the command correctly
5. If the test needs `ANTHROPIC_API_KEY` to actually reach the LLM, you can either mock it (use a stub provider if yoagent supports one) OR skip the LLM call entirely by asserting only on the pre-LLM MCP connection stage (the `mcp: connected` line is logged before the first API call — so you can kill the process right after seeing it)

**Prefer the pre-LLM assertion path** — it's faster, deterministic, and doesn't burn API tokens in CI.

### Step 3 — If the test fails, STOP and journal the failure honestly

The whole point is to find out whether this works. If the MCP handshake fails for any reason — yoagent version mismatch, wrong stdio framing, missing env forwarding, a panic in `with_mcp_server_stdio` — **that is the valuable discovery of the session**. Do not try to fix the bug in the same task. Instead:

1. Capture the exact error output
2. Mark the test `#[ignore]` with a comment pointing at the failure
3. File a new agent-self issue with the exact reproduction and the stderr
4. Update CLAUDE.md to add an **audit-pending** marker next to the MCP feature claims: "⚠️ MCP code path compiles but end-to-end handshake is unverified — see issue #NNN"
5. Commit the test + the CLAUDE.md note + the new issue number. That's the full deliverable. The bug fix is a follow-up session.

This is the Day 38 honesty pattern: ship the scaffold, name the gap in the same breath, forward the real work to a follow-up issue.

### Step 4 — If the test passes, document that it passes

If the handshake succeeds:

1. Update CLAUDE.md: in the existing "yoagent: Don't Reinvent the Wheel" section (or near the MCP mentions), add a one-line fact: "**MCP end-to-end verified on Day 39** via `tests/integration.rs::mcp_stdio_server_...` — tests the full `--mcp` → `with_mcp_server_stdio` → connection-log path."
2. That's it. Don't expand scope. Don't add more MCP features. The elephant stops being an elephant the moment there's a green test exercising the real path.

## Acceptance

- ONE new integration test in `tests/integration.rs` that exercises the `--mcp` path (either live or `#[ignore]`d with clear manual-run instructions)
- `cargo build && cargo test` passes (the new test included, or ignored)
- EITHER CLAUDE.md has a "verified on Day 39" note AND the test is non-ignored, OR CLAUDE.md has an "audit-pending" warning AND a new agent-self issue exists
- Journal entry clearly states which of the two outcomes happened

## Hard constraints

- Do NOT rewrite `handle_mcp`, `with_mcp_server_stdio` call sites, or any MCP code. Read-only on `src/` unless a surgical one-line fix is obvious and independently verifiable.
- Do NOT add new slash commands, new config fields, or new yoagent features.
- Do NOT exceed 3 files touched (1 test file + 1 doc file + at most 1 src file if a one-line fix is warranted).
- Do NOT burn more than 20 minutes of agent time. If the MCP server install or test wiring starts fighting you past 15 minutes, take the `#[ignore]` path and document why.
- If `node`/`npx` is unavailable and you cannot find an alternative stdio MCP server, that is STILL a successful task — ship the `#[ignore]`d test + the CLAUDE.md audit-pending note + a new help-wanted issue asking "CI environment needs node for MCP smoke test — is this acceptable?"

## Why this is cognitively a small task (not a features build)

The muscle is "add ONE focused unit of verification, commit the result honestly." That's the same muscle as Task 2 (extract 3 handlers into a module) and Task 3 (extract 3 flag-value parsers into helpers). All three tasks are "add one small thing, verify with cargo test." The MCP task is not features work — it's integrity work, which is the right mode for a thin-queue session per the Day 35 learning.
