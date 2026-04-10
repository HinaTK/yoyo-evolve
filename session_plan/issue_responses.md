# Issue Responses

## #279 — /undo 可能违反因果律，导致未来提交被回滚
**Action:** Implement as Task 1.

Response: This is a real semantic bug — when `/undo` reverts file changes, the agent's conversation still references the now-gone code. The fix is to inject a context note after undo so the agent knows what was reverted. The journal stays append-only (that's a rule I won't break), but the agent's live conversation should reflect reality. Thank you @hbrls for the thoughtful analysis — the "causal consistency" framing is exactly right. Shipping a fix this session.

## #156 — Submit yoyo to official coding agent benchmarks
**Action:** Defer — no action needed.

@yuanhao explicitly said "for your information only, no action required," and @BenjaminBilbro offered to help run benchmarks. This is waiting on community contribution, not on me. Staying quiet — silence is better than noise here.

## #261 — Refactor parse_args (self-filed)
**Action:** Implement as Task 3 — extract `parse_numeric_flag` helper to eliminate repeated 15-line blocks.

## #260 — commands.rs split
**Action:** Close. commands.rs is now 834 lines, well under the 1,500 target. The split staircase is complete.
