Title: Proactive context budget warnings after each agent turn
Files: src/format/mod.rs, src/prompt.rs
Issue: none

## What to do

Add escalating context usage warnings that appear after each agent turn, giving users
actionable advice before they hit the context overflow wall. Claude Code does this;
yoyo currently just shows a tiny status dot.

### In `src/format/mod.rs`:

Add a new public function `context_budget_warning(used: u64, max: u64) -> Option<String>` that:
- Returns `None` if usage is below 60%
- At 60%: returns a dim info message: "Context is 60% full — consider /compact to free space"
- At 80%: returns a yellow warning: "⚠ Context is 80% full — /compact or /save + /clear recommended"
- At 90%: returns a red warning: "🔴 Context is 90% full — /save your session, then /clear to avoid overflow"
- At 95%+: returns a bold red warning: "🔴 Context nearly full! /clear now or risk overflow errors"

Use the existing `context_usage_color()` for color selection. Only warn once per threshold
crossing (use a simple static AtomicU32 to track the last warned threshold, reset it on clear).

Add tests:
- Test each threshold returns the correct severity
- Test below 60% returns None
- Test threshold tracking (same threshold doesn't warn twice)

### In `src/prompt.rs`:

In both `run_prompt_with_changes` and `run_prompt_with_content_and_changes`, after the
existing `print_context_usage()` call, add:

```rust
if let Some(warning) = context_budget_warning(ctx_used, ctx_max) {
    eprintln!("{warning}");
}
```

This is ~2 lines added to each of the two prompt functions, plus the new function in format/mod.rs.
Total scope: ~50-70 new lines + tests.
