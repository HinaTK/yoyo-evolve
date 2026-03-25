Title: Add --context-strategy flag with checkpoint-restart support
Files: src/cli.rs, src/main.rs, src/prompt.rs
Issue: #185

## Context

Compaction is lossy — it truncates tool outputs and drops old messages. For the evolution pipeline (`evolve.sh`), a structured checkpoint + fresh restart produces better results than compacted context. But compaction is still the right default for interactive users.

This task adds a `--context-strategy <compaction|checkpoint>` CLI flag. When `checkpoint` is used, yoyo monitors context usage via `on_before_turn` and, when approaching the limit, steers the agent to write a checkpoint file and then exits with code 2.

**Prerequisite**: Task 1 must have landed first (wires `with_context_config` and handles `MessageStart`/`MessageEnd` events).

## Implementation

### 1. Add CLI flag parsing (src/cli.rs)

Add a new enum and field to `AgentConfig`:

```rust
/// Context management strategy.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ContextStrategy {
    /// Default: auto-compact conversation when approaching context limit
    Compaction,
    /// Write checkpoint file and exit with code 2 when approaching limit
    Checkpoint,
}

impl Default for ContextStrategy {
    fn default() -> Self {
        ContextStrategy::Compaction
    }
}
```

Add `pub context_strategy: ContextStrategy` to `AgentConfig`.

In `parse_args()`, handle `--context-strategy`:
```rust
"--context-strategy" => {
    if let Some(val) = args.get(i + 1) {
        match val.as_str() {
            "compaction" => config.context_strategy = ContextStrategy::Compaction,
            "checkpoint" => config.context_strategy = ContextStrategy::Checkpoint,
            _ => eprintln!("Warning: unknown context strategy '{}', using compaction", val),
        }
        i += 1;
    }
}
```

### 2. Wire checkpoint behavior in `configure_agent` (src/main.rs)

When `context_strategy == Checkpoint`, register an `on_before_turn` callback:

```rust
if self.context_strategy == cli::ContextStrategy::Checkpoint {
    use yoagent::context::total_tokens;
    let threshold = 0.75; // 75% of context budget
    let max_tokens = 200_000u64;
    
    agent = agent.on_before_turn(move |messages, _turn| {
        let used = total_tokens(messages) as u64;
        let ratio = used as f64 / max_tokens as f64;
        if ratio > threshold {
            // Signal that context is approaching the limit
            // Return false to stop the agent loop
            eprintln!("\n⚡ Context at {:.0}% — checkpoint-restart triggered", ratio * 100.0);
            return false;
        }
        true
    });
}
```

### 3. Handle exit code 2 (src/main.rs)

In `main()`, after the REPL or piped mode completes, check if checkpoint mode was active and the agent was stopped by the before_turn callback. The simplest approach:

Add a global `AtomicBool` flag `CHECKPOINT_TRIGGERED`:
```rust
static CHECKPOINT_TRIGGERED: AtomicBool = AtomicBool::new(false);
```

Set it in the `on_before_turn` callback when context exceeds the threshold. Then at the end of `main()`:
```rust
if CHECKPOINT_TRIGGERED.load(Ordering::SeqCst) {
    std::process::exit(2);
}
```

### 4. Steer agent to write checkpoint before stopping (src/main.rs or src/prompt.rs)

When checkpoint mode triggers, before stopping, inject a steering message asking the agent to write a checkpoint file:

In the `on_before_turn` callback, instead of just returning false immediately, use `agent.steer()` to queue a steering message. However, `on_before_turn` only has access to messages, not the agent. 

Alternative approach: Use `on_before_turn` to return `false` (stop loop), and then after the agent stops, the caller in main.rs/repl.rs can detect the checkpoint condition and run one final prompt asking the agent to write a checkpoint.

Simplest viable approach for this task:
1. `on_before_turn` returns `false` and sets `CHECKPOINT_TRIGGERED`
2. After the agent loop exits in piped mode (the evolution pipeline path), check `CHECKPOINT_TRIGGERED`
3. If set, print a message about the checkpoint exit and exit with code 2
4. The evolution pipeline (`evolve.sh`) handles the restart — this is out of scope for this task

### 5. Tests

In `src/cli.rs` tests:
- `test_context_strategy_default_is_compaction`
- `test_context_strategy_parses_checkpoint`
- `test_context_strategy_parses_compaction_explicit`
- `test_context_strategy_unknown_defaults_to_compaction`

In `src/main.rs` tests:
- `test_checkpoint_triggered_flag_starts_false`

### 6. Verify

Run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings`.

### 7. Notes

This is the minimal viable checkpoint-restart. Future tasks can:
- Have the agent write an actual checkpoint file before exiting
- Parse the checkpoint file when restarting
- Add `--checkpoint-path` for custom checkpoint locations
- Wire it into `evolve.sh`
