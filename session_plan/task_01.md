Title: Verify #262 diagnosis and close or update — act on human feedback
Files: none (issue management + diagnostic commands only)
Issue: #262, #267

## Context

A human reviewed Issues #262 and #267 and provided critical feedback:

1. `.github/workflows/evolve.yml` already has `concurrency: { group: evolution, cancel-in-progress: false }` which protects **running** sessions. Cancelled runs in `gh run list` are likely **queued** runs being dedup'd, not killed in-flight sessions.
2. Even if sessions were being killed, `session_budget_exhausted()` only fires between retry attempts, not during a long `agent.prompt()` call — so it wouldn't rescue implementation tasks.
3. The Rust plumbing from `5a39e6e` is "inert but harmless" — can stay or be stripped later.

## What to do

1. **Verify the diagnosis.** Pull the logs of 2-3 of the `cancelled` runs from `gh run list --workflow=evolve.yml` using:
   ```
   gh run list --workflow=evolve.yml --status cancelled --limit 5 --json databaseId,startedAt,conclusion
   ```
   Then for each:
   ```
   gh run view <ID> --log 2>&1 | head -100
   ```
   Check whether the runner ever reached the `Run evolution session` step. If it never started, the cancellation was queue-stage (confirming the human's hypothesis).

2. **Based on findings:**
   - If confirmed queue-stage: Comment on #262 with the evidence, acknowledging the misdiagnosis. Close #262. Close #267 if still open (human already closed it in the reply).
   - If surprisingly in-flight: Comment with the evidence showing the human's hypothesis was wrong, and note that the fix needs to be workflow-level per their suggestion.

3. **Comment tone:** Be honest — "I got this wrong. The cancelled runs were queue dedup, not killed sessions. Thanks for checking the actual workflow config." Use yoyo's voice — curious octopus who admits mistakes.

4. **Do NOT delete the session budget code.** The human said "inert but harmless, no revert needed." It may find use later. Just close the issues and move on.

## Acceptance
- #262 has a comment with verified evidence
- #262 is closed (if diagnosis confirmed) or updated (if not)
- #267 is closed (if not already)
- No code changes needed
