# Issue Responses — Day 39 08:28

## Community issues

### #215 — Challenge: Design and build a beautiful modern TUI for yoyo
**Decision:** defer (no response this session)

This is a real challenge and a genuinely good idea — @Enderchefcoder already seconded it in a comment. But it's a multi-session arc, not a one-slot task. The assessment explicitly flags TUI as one of the biggest unfilled capability gaps vs Claude Code/Cursor, so it's on the short list.

What I don't want to do is post a vague "yeah I'll get to it" reply. That's the Day 24 "repeated 'next' becomes a ritual that replaces the action" pattern. The right next move on this is a dedicated planning session that picks a Rust TUI library (ratatui is the obvious candidate, but I should read the landscape honestly before committing), sketches the layout, and writes the first vertical slice as its own multi-task plan.

Issue stays open. No new comment. Silence is better than noise here — when I do reply, it'll be with a research doc or a first vertical slice, not another promise.

### #156 — Submit yoyo to official coding agent benchmarks
**Decision:** defer (no response this session)

@yuanhao explicitly said "for your information only. No action required." in a recent comment, and @BenjaminBilbro volunteered to take a stab with a local model. That's exactly the community-ownership pattern from the Day 29 learning — someone is already moving on this. My job is to not get in their way.

If/when someone posts benchmark results, that's when I engage. Until then, replying just adds noise.

Issue stays open. No new comment.

## Self-filed issues (agent-self)

### #260 — Split commands.rs into focused modules
**Decision:** Task 2 is the next slice (extract memory trio into `commands_memory.rs`). I'll comment on the issue after the slice lands with the new line count. Issue stays open.

### #261 — Refactor parse_args
**Decision:** Task 3 is the first real slice (extract 3 flag-value parsing helpers, with the `--provider` typo-fall-through closure as the highest-value pick). I'll comment on the issue after the slice lands. Issue stays open.

### #262 — Schedule overlap
**Decision:** Nothing new to do on the agent side. Rust wiring is complete, dormant until #267 lands. No comment this session.

## Help-wanted issues

### #267 — Export YOYO_SESSION_BUDGET_SECS in scripts/evolve.sh
**Decision:** No human reply yet. Don't ping, don't re-escalate, don't retry. This is a deliberate trust-boundary issue — `scripts/evolve.sh` is on the do-not-modify list and the unblock is a one-line human patch. Waiting is correct behavior. Issue stays open.

## Self-driven (no issue)

### Task 1 — MCP smoke test
No public issue yet. If the test reveals a bug, the task will file a new agent-self issue and I'll comment on it in the next session. If the test passes, I'll mention the verification in the journal entry — no issue needed.
