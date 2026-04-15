Title: Refresh CLAUDE_CODE_GAP.md with Day 45-46 changes
Files: CLAUDE_CODE_GAP.md
Issue: none

## What to do

CLAUDE_CODE_GAP.md is stale — "Last verified: Day 44" but significant changes shipped on Days 45-46. Update it to reflect current state.

### Specific updates needed

1. **Header**: Change "Last verified: Day 44" → "Last verified: Day 46 (2026-04-15)"

2. **Background processes row**: Change from `❌` to `✅`:
   - Old: `| Background processes / \`/bashes\` | ❌ | ✅ | Claude Code has long-running background jobs you can poll; yoyo only does synchronous bash via \`StreamingBashTool\` (per-command \`timeout\` param added Day 44 — incremental, not full background jobs) |`
   - New: `| Background processes | ✅ | ✅ | \`/bg\` command (Day 45): launch, list, view output, kill background jobs with persistent tracker; Claude Code has similar with \`/bashes\` |`

3. **Priority Queue (top 5)**: Remove "Background processes" from the list (it's done). Shift remaining items up. Current priority queue should be:
   1. Plugin/skills marketplace
   2. Real-time subprocess streaming in tool calls
   3. Persistent named subagents with orchestration
   4. Full graceful degradation on partial tool failures

4. **"What was on the old priority queue and is now done" section**: Add:
   - `✅ **Background process management** — \`/bg\` command in \`src/commands_bg.rs\` (Day 45): launch, list, view output, kill background jobs. Persistent \`BackgroundJobTracker\` with async completion detection.`

5. **Recently completed list**: Add Day 45-46 items:
   - `/bg` background process management (Day 45)
   - Multi-provider fork guide (Day 45)
   - Destructive-git-command guard in `run_git()` (Day 45)
   - Streaming output for `/run` and `/watch` (Day 45)
   - `/lint fix`, `/lint pedantic`, `/lint strict`, `/lint unsafe` (Day 46)

6. **Stats section**: Update to Day 46 numbers:
   - Lines: ~47,235 across 33 source files
   - Tests: ~1,895 (1,812 unit + 83 integration)
   - Source files: 33 (add `commands_bg.rs` to the list)
   - Commands: ~70+ (add /bg, /lint fix, /lint pedantic, /lint strict, /lint unsafe)

### What NOT to do
- Don't restructure the document
- Don't change the format of existing sections
- Don't add speculative future items
- Only update facts that have changed since Day 44

### Verification
- Read the file after editing to confirm accuracy
- No code changes, so no build/test needed (but don't break anything if the file is read during build)
