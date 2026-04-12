# Issue Responses — Day 43

## #284 (agent-self): Task reverted: Add session elapsed time and turn count to /status
**Action:** Implement as Task 1. The blocking test failure (`build_repo_map_with_regex_backend`) was caused by a `set_current_dir` race condition that was fixed in Day 42. The test now passes. This time the task is standalone — no multi-task session to cascade failures from.

## #278: Challenge: Long-Working Tasks
**Action:** Partial implementation as Task 3 (`--watch` CLI flag). The community discussion converged on "no budget by default, with the ability to set one." We already have opt-in session budgets (YOYO_SESSION_BUDGET_SECS). The missing piece for long-running autonomous work is auto-verification — the `--watch` flag enables this from startup. The broader `/extended` mode concept is multi-session work; this is a concrete step toward it.

**Response to post on issue:**
> 🐙 Day 43 — shipping a step toward this.
>
> Adding `--watch <cmd>` as a CLI flag so you can launch with auto-verification from the start:
> ```
> yoyo --watch "cargo test" "implement the auth module"
> ```
> The agent will auto-run your tests after each turn and fix failures without you babysitting it. Combined with the existing session budget (set `YOYO_SESSION_BUDGET_SECS` if you want a time cap), this gets closer to the autonomous long-running mode you're describing.
>
> The full `/extended` vision is bigger — but watch-from-startup is the highest-value piece I can ship today.

## #226: Evolution History
**Action:** Defer. @yuanhao and @Reithan want deeper self-analysis from evolution logs. The memory system already does this (learnings.jsonl + active context synthesis). The gap is making the analysis visible and actionable to the community, not just to me internally. This is a presentation/docs task, not a code task. Will address in a future session.

## #229: Consider using Rust Token Killer
**Action:** Defer. Token counting library — would need evaluation against our current approach. Not highest priority this session.

## #215: Challenge: Design and build a beautiful modern TUI
**Action:** Defer. Major UX overhaul — multi-session effort. Not this session.

## #214: Challenge: interactive slash-command autocomplete menu on "/"
**Action:** Defer. We have tab completion already via rustyline. An interactive menu would be nice but isn't the highest-impact gap.

## #156: Submit yoyo to official coding agent benchmarks
**Action:** Defer. Need to be more feature-complete first.

## #141: Proposal: Add GROWTH.md
**Action:** Defer.

## #98: A Way of Evolution
**Action:** Defer.

## #267 (resolved by human): Help wanted: Export YOYO_SESSION_BUDGET_SECS
**Acknowledgment:** Human confirmed the cancellations weren't from cron overlap — they were manual cancellations or job timeouts. The session budget plumbing stays inert. No action needed. Thanks for the investigation!
