Title: Fix /tokens display — clarify context vs cumulative labeling
Files: src/commands.rs
Issue: #189

## Context

Issue #189 reports that `/tokens` is confusing because the "Context window" section shows current loaded message tokens while "Session totals" shows cumulative tokens, and users conflate the two. The reporter (@BenjaminBilbro) followed up saying it "might not be 100% correct" after further testing — suggesting the display is more accurate than initially reported but the labeling is still unclear.

## The problem

The current display:
```
  Context window:
    messages:    10
    current:     1.8k / 200.0k tokens
    [████░░░░░░]
    (some earlier context was compacted)

  Cumulative session totals:
    input:       22.0k tokens
    output:      1.8k tokens
    ...
```

The `current` line uses `total_tokens()` which estimates tokens from the in-memory messages. After compaction, this drops because compacted messages are removed. This is CORRECT behavior — it shows what's actually in the context window. But users expect "context" to mean "total tokens sent to the model this session."

## Fix

The display is already mostly right (after previous fixes changed "context:" to "current:"). The remaining issue is clarity. Make these changes in `handle_tokens()` (line ~213 of `src/commands.rs`):

1. **Rename section header** from "Context window:" to "Active context:" — emphasizes that this is what's loaded NOW, not cumulative.

2. **Add explanatory note** when compaction has occurred:
   - Change `(some earlier context was compacted)` to `(earlier messages were compacted to save space — session totals below show full usage)`

3. **Make session totals header clearer**:
   - Change `Cumulative session totals:` to `Session totals (all API calls):`

4. **Tests**: Add a test in `src/commands.rs` that verifies `handle_tokens` output contains expected labels. Since `handle_tokens` prints to stdout, this might be tricky to test directly — instead verify the formatting helper functions (`format_token_count`, `context_bar`) which are already tested. Add a simple test that verifies the function doesn't panic with various inputs (zero messages, zero usage, very large values).

The fix is small — just label changes that make the display unambiguous. No logic changes needed.
