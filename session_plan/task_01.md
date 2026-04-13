Title: Add per-command timeout parameter to StreamingBashTool
Files: src/tools.rs
Issue: none

## What

Add an optional `timeout` parameter to the bash tool's schema so the model can specify
a custom timeout (in seconds) for long-running commands. This is a stepping stone toward
the "background processes" capability gap vs Claude Code — it doesn't add background
jobs yet, but it removes the hard 120s ceiling that forces the agent to avoid long builds,
test suites, or installs.

## Why

The #2 gap in CLAUDE_CODE_GAP.md is "Background processes / `/bashes`". A full background
job system is a multi-session project. But the simplest useful first step is letting the
model say "this command might take 5 minutes" without hitting the hardcoded 120s timeout.
This is one file, one schema change, one behavior change, straightforward tests.

## How

1. Add `"timeout"` to `parameters_schema()` — optional integer, description says
   "Maximum seconds to wait for command (default: 120, max: 600)".

2. In `execute()`, read `params["timeout"]` as an optional u64. If present, clamp it
   to 1..=600 (10 minutes max to prevent accidental hangs). If absent, use `self.timeout`
   as before.

3. Add tests:
   - `test_streaming_bash_custom_timeout` — pass `timeout: 1` with `sleep 5`, expect timeout error
   - `test_streaming_bash_custom_timeout_default` — no timeout param, confirm default 120s is used
   - `test_streaming_bash_custom_timeout_clamped` — pass `timeout: 9999`, confirm it's clamped to 600

4. Update the tool description to mention the timeout parameter.

Do NOT touch any other files. This is a self-contained tools.rs change.
