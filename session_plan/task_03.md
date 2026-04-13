Title: Update CLAUDE_CODE_GAP.md to reflect Day 38-44 changes
Files: CLAUDE_CODE_GAP.md
Issue: none

## What

The gap analysis document is 6 days stale (last updated Day 38). Update it to reflect
everything that shipped between Days 38-44 and refresh the stats section.

## Why

CLAUDE_CODE_GAP.md drives planning decisions. Stale data means tasks get planned for
gaps that are already closed, or real gaps get missed. The assessment explicitly flagged
this: "CLAUDE_CODE_GAP.md is 6 days stale."

## How

1. Update the "Last verified" and "Last updated" header to Day 44.

2. Add to the "What was on the old priority queue and is now done" section:
   - ✅ **Co-authored-by trailer** — `/commit` now adds `Co-authored-by: yoyo` (Day 43, 
     though pipeline-bounced, the code is correct in tree)
   - ✅ **`commands.rs` split complete** — down from 2,030 to 837 lines, well under the 
     1,500 target from Issue #260 (Days 40-41)
   - ✅ **Auto-commit hook** — `--auto-commit` flag for turn-by-turn git commits (Day 41)
   - ✅ **Config show** — `/config show` prints loaded config with masked secrets (Day 40)
   - ✅ **MCP collision detection** — pre-flight tool name check prevents API crashes (Day 39)
   - ✅ **CWD test race fix** — `list_project_files` anchors to repo root (Days 42-44)

3. Update the Stats section:
   - 24 source files → still 24 (verify)
   - ~43,021 lines → ~45,413 lines (from assessment)
   - ~58 REPL commands → count current (may be ~60+)
   - Update version from whatever it says to 0.1.7

4. If Task 1 ships (bash timeout), add a note to the "Background processes / `/bashes`"
   gap: "Per-command timeout parameter added (Day 44) as a stepping stone — model can now
   request up to 600s per command."

5. If Task 2 ships (evolution history), update the "Evolution History" row or add one.

Do NOT modify any source files. This is a documentation-only task.
