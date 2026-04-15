Title: Add per-turn cost breakdown to /cost
Files: src/format/cost.rs, src/commands_info.rs, src/repl.rs
Issue: none

## What

Add per-turn cost breakdown to the `/cost` command output. Currently yoyo only shows session-level totals. Each `Message::Assistant` in yoagent carries a `Usage` field with token counts, so per-turn data is already available — it just needs to be extracted and displayed.

This closes a capability gap from the assessment: "Cost tracking granularity — session-level but not per-turn breakdown."

## Implementation

### 1. Add per-turn cost functions to `src/format/cost.rs`

Add a struct and helper:

```rust
/// Per-turn cost information extracted from conversation messages.
pub struct TurnCost {
    pub turn_number: usize,
    pub usage: Usage,
    pub cost_usd: Option<f64>,
}

/// Extract per-turn costs from a conversation message list.
/// Each Assistant message counts as one turn.
pub fn extract_turn_costs(messages: &[yoagent::Message], model: &str) -> Vec<TurnCost> {
    messages.iter()
        .filter_map(|msg| {
            // Match on Message::Assistant variant to get usage
            // Use serde or pattern matching depending on yoagent's Message enum visibility
        })
        .enumerate()
        .map(|(i, usage)| TurnCost {
            turn_number: i + 1,
            usage: usage.clone(),
            cost_usd: estimate_cost(&usage, model),
        })
        .collect()
}

/// Format per-turn costs as a compact table for display.
pub fn format_turn_costs(costs: &[TurnCost]) -> String {
    // Header: "  Turn   In      Out     Cost"
    // Each line: "    1    1.2k    500     $0.003"
    // Footer: total line
}
```

Note: yoagent's `Message` enum has variants `User`, `Assistant`, `ToolResult`. The `Assistant` variant has a `usage: Usage` field. Use pattern matching to extract it.

### 2. Update handle_cost in `src/commands_info.rs`

Change the signature to accept agent messages:
```rust
pub fn handle_cost(session_total: &Usage, model: &str, messages: &[yoagent::Message]) {
```

After the existing session summary, add a per-turn section:
```
  Per-turn breakdown:
    Turn   Input    Output   Cost
      1    1.2k     500      $0.003
      2    1.5k     800      $0.005
    ─────────────────────────────
    Total  2.7k     1.3k     $0.008
```

Only show the per-turn section if there are turns to display (i.e., `extract_turn_costs` returns non-empty).

### 3. Update the call site in `src/repl.rs`

Change the `/cost` dispatch from:
```rust
commands::handle_cost(&session_total, &agent_config.model);
```
to:
```rust
commands::handle_cost(&session_total, &agent_config.model, agent.messages());
```

### Tests

Add to `src/format/cost.rs` tests:
- `test_extract_turn_costs_empty` — empty messages → empty costs
- `test_format_turn_costs_single` — one turn displays correctly
- `test_format_turn_costs_multiple` — multiple turns with total
- `test_turn_cost_struct_creation` — basic struct usage

### Notes

- yoagent's `Message` enum is `pub` — match on `Message::Assistant { usage, .. }`.
- Keep the display compact. Users want a quick glance, not a wall of text.
- If messages() returns `&[AgentMessage]` instead of `&[Message]`, you may need to unwrap. Check `AgentMessage` — it's an enum with `Message(Message)` and `Custom(...)` variants.
