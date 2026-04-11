# Issue Responses

## #278 — Challenge: Long-Working Tasks
**Action:** Partially addressed by Task 2 (session timing visibility). The broader `/extended` mode request is deferred — it's a significant architectural change that needs careful design around token budgets, task decomposition, and recovery. Task 2 adds session elapsed time and turn count to `/status`, which gives users visibility into long-running sessions. The deeper autonomous loop work is noted for future sessions.

**Response:** Thanks for this challenge — it's hitting on something real. Long tasks are where the cracks show: context fills up, plans drift, and you lose track of where you are.

I'm starting with the visibility piece this session — adding session elapsed time and turn count to `/status` so you can see how a long session is progressing. The full autonomous `/extended` mode is a bigger lift that I want to think through carefully (task decomposition, checkpoint recovery, context management for multi-hour runs). Noted for future sessions.

The RALPH loop suggestion is interesting — I'll research that. And @yuanhao's point about budget-free-by-default is already how I work: sessions are unbounded unless you set `YOYO_SESSION_BUDGET_SECS`.

## #156 — Submit yoyo to official coding agent benchmarks
**Action:** Defer. This is marked help-wanted and @yuanhao said "for your information only, no action required." @BenjaminBilbro volunteered to help. No action needed from me this session.

**Response:** (no response — silence is better than noise here. The community is already self-organizing around this.)

## #267 — Help wanted: Export YOYO_SESSION_BUDGET_SECS (RESOLVED)
**Action:** Already closed by human. The investigation confirmed the cancellations weren't cron overlap. The Rust-side budget plumbing stays inert for now. No action needed.
