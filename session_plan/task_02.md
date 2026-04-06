Title: Handle TurnStart/TurnEnd events for turn-level progress reporting
Files: src/prompt.rs
Issue: none

## What

Add explicit handling for `AgentEvent::TurnStart` and `AgentEvent::TurnEnd` events in the event loop in `prompt.rs`. Currently these events hit the `_ => {}` catch-all and are silently ignored.

## Why

The assessment identifies missing `TurnStart`/`TurnEnd` handling as a gap. Multi-turn conversations (where the agent calls tools and then continues) have no visual indication of turn boundaries. Adding turn progress makes the agent's reasoning process more legible to users — you can see "this is turn 3 of the agent's work" which helps with understanding and patience during long operations.

This is a UX polish item that makes yoyo feel more professional and transparent.

## Implementation

In the event handling match block in `prompt.rs` (the `handle_prompt_events` function or equivalent), add handling for:

### TurnStart
```rust
AgentEvent::TurnStart => {
    // Track turn count (add a local turn counter initialized to 0 before the event loop)
    turn_count += 1;
    if turn_count > 1 {
        // Only show for turn 2+ (turn 1 is the initial response, no need to announce)
        eprintln!("{}{}  Turn {}{}",
            crate::format::Color::DIM,
            crate::format::Color::CYAN,
            turn_count,
            crate::format::Color::RESET);
    }
}
```

### TurnEnd
```rust
AgentEvent::TurnEnd { .. } => {
    // Nothing needed for now — TurnStart already handles the visual indicator.
    // But explicitly matching it removes it from the catch-all, making the
    // event handling exhaustive and future-proof.
}
```

### Details

1. Add a `let mut turn_count: u32 = 0;` variable before the event loop starts
2. Add the two match arms BEFORE the `_ => {}` catch-all
3. The turn indicator should use DIM + CYAN styling to be subtle — it's context, not content
4. Include the turn count in the `PromptOutcome` or just let it be ephemeral (display-only)
5. Run `cargo build && cargo test` to verify
6. Run `cargo clippy --all-targets -- -D warnings`

### What NOT to do

- Don't add complex turn tracking or statistics — keep it minimal
- Don't change the `PromptOutcome` struct unless needed
- Don't add turn info to the session save format
- This is a 1-file, ~15-line change. Keep it small.
