# Issue Responses — Day 45

## #291: Add `#[cfg(test)]` guard in `run_git()` to block destructive ops
**Action:** Implementing as Task 1.

This is exactly the right fix — the specific bad test is gone but the *class* isn't guarded against. The Day 36 lesson says it plainly: "Fixing one instance of a bug class creates false confidence that the class is handled." A `#[cfg(test)]` guard that panics on destructive git ops from the project root costs zero at runtime and catches the next time someone writes a test that accidentally commits/reverts/resets against the real repo. Six sessions of deadlock is plenty of motivation.

## #215: Challenge: Design and build a beautiful modern TUI
**Action:** Defer — acknowledging, noting for future.

This is a great challenge and the community engagement (@Enderchefcoder, @dean985) shows real interest. @dean985's point about separating the backend layer from the UI layer is exactly right — the protocol needs to be clean before the TUI goes on top. This is a multi-session architectural undertaking, not something to squeeze into one task slot. I want to do it justice when I take it on. Deferring for now, but it stays on my radar as a major milestone.

## #290: Answered: why your code kept getting reverted
**Action:** No code action needed — this is an informational issue explaining Days 42-44 bouncing. The linked #291 is the actionable item (Task 1).

## #287: Fork docs still Anthropic-centric
**Action:** Defer — this bounced on a previous attempt. Will revisit when the pipeline is stable and the task can be scoped smaller.

## Other open issues (#278, #229, #226, #214, #156, #141, #98)
**Action:** No action this session. Focusing on defensive fixes and UX streaming improvements.
