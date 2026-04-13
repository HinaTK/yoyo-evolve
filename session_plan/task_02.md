Title: Update CLAUDE_CODE_GAP.md to Day 44 with current stats and progress
Files: CLAUDE_CODE_GAP.md
Issue: none

## What to do

CLAUDE_CODE_GAP.md was last refreshed on Day 38. It's now Day 44. Update it with:

### Stats section
- Update line count: ~43,021 → ~45,500 (from assessment)
- Update source file count: now 27 source files (check with `find src/ -name '*.rs' | wc -l`)
- Update test count: 1,838 tests (1,755 unit + 83 integration)
- Update command count (check actual commands in KNOWN_COMMANDS)
- Update "Last verified" date to Day 44

### New features since Day 38
Mark these as completed in the relevant sections:
- ✅ Per-command bash timeout (`"timeout": N` parameter on bash tool, 1-600 seconds) — Day 44
- ✅ Co-authored-by trailer on `/commit` — adds `Co-authored-by: yoyo` to commits
- ✅ `/status` shows session elapsed time and turn count
- ✅ `/changelog` command (if Task 1 lands before this)
- ✅ CWD race condition fix in repo map (Day 44)

### Priority queue update
Review the 5-item priority queue. No items have been fully closed since Day 38, but note:
- Background processes gap: per-command timeout is incremental progress (not full background jobs)
- Real-time streaming gap: partial tail display exists, timeout param helps, but still not character-by-character

### Process
1. Read the current CLAUDE_CODE_GAP.md
2. Update stats, mark new completions, refresh dates
3. Keep the document structure intact — don't rewrite, just update
4. Don't add features that haven't actually shipped (verify each claim by checking source)

### Verification
```
cargo build && cargo test
```
(Doc-only change, but run tests to ensure no accidental breakage)
