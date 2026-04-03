Title: Autocompact thrash detection
Files: src/commands_session.rs
Issue: none

## What

Add thrash detection to the auto-compact and proactive-compact functions so that if compaction doesn't meaningfully reduce tokens (less than 10% reduction), we stop trying and warn the user instead of repeatedly compacting to no effect.

## Why

Claude Code 2.1.91 has autocompact thrash detection — it detects when compaction keeps firing but doesn't free enough tokens, and stops. Our current implementation blindly compacts whenever the threshold is hit, even if the previous compaction barely freed anything. This wastes time and creates a false sense of progress. In the worst case, the context is mostly system prompt + recent messages that can't be compacted, and we keep trying every turn.

## Design

Add a simple thrash detection mechanism using a module-level counter:

1. Add a `static` atomic counter tracking consecutive low-yield compactions
2. In `compact_agent()`, after compacting, check if the reduction was meaningful (>10% of before_tokens)
3. If not meaningful, increment the thrash counter
4. If meaningful, reset the thrash counter to 0
5. In `auto_compact_if_needed()` and `proactive_compact_if_needed()`, check the thrash counter before attempting compaction
6. If thrash counter >= 2 (two consecutive low-yield compactions), skip compaction and print a warning: "⚠ Context is mostly incompressible — consider /clear or starting a new session"
7. The `/compact` manual command should always work regardless of thrash state (user explicitly asked)
8. Add a `reset_compact_thrash()` function called when conversation is cleared or loaded (since the context changed)

## Implementation details

```rust
use std::sync::atomic::{AtomicU32, Ordering};

static COMPACT_THRASH_COUNT: AtomicU32 = AtomicU32::new(0);
const COMPACT_THRASH_THRESHOLD: u32 = 2;
const COMPACT_MIN_REDUCTION: f64 = 0.10; // 10% minimum to be "meaningful"

pub fn reset_compact_thrash() {
    COMPACT_THRASH_COUNT.store(0, Ordering::Relaxed);
}
```

In `compact_agent()`, after computing before/after:
- If `(before_tokens - after_tokens) as f64 / before_tokens as f64 < COMPACT_MIN_REDUCTION`, increment thrash counter
- Otherwise reset to 0

In `auto_compact_if_needed()` and `proactive_compact_if_needed()`:
- Check `COMPACT_THRASH_COUNT.load(Ordering::Relaxed) >= COMPACT_THRASH_THRESHOLD`
- If thrashing, print warning and return without compacting

Call `reset_compact_thrash()` from:
- The `/clear` handler (conversation reset)
- The `/load` handler (new conversation loaded)
- These are in the same file so no extra file touches needed

## Tests to add

1. `test_compact_thrash_detection_resets_on_meaningful_reduction` — verify counter resets
2. `test_compact_thrash_detection_increments_on_low_reduction` — verify counter increments
3. `test_compact_thrash_threshold` — verify the threshold constant
4. `test_reset_compact_thrash` — verify reset function works
5. Test that `compact_agent` returns None when nothing changes (already exists? verify)

## Verification

- `cargo build` must pass
- `cargo test` must pass
- `cargo clippy --all-targets -- -D warnings` must pass
- The thrash counter uses atomics so it's thread-safe

## What NOT to do

- Don't modify any other files — everything is in commands_session.rs
- Don't change the compaction logic itself — just add the thrash detection wrapper
- Don't break the existing `/compact` manual command — it should always work
