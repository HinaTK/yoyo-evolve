Title: Add context window percentage to usage display
Files: src/format/mod.rs, src/format/cost.rs
Issue: none

## What

Add context window usage percentage to the post-turn usage line, so users can see how much of their context budget they've consumed. Currently we show `↳ 2.3s · 1234→567 tokens · $0.02` but not how full the context window is. Add a context percentage indicator like `[47% context]` to the usage line.

## Why

Claude Code shows context window usage after every turn. Users need to know when they're approaching the limit so they can `/compact`, `/clear`, or start a new session. Currently you have to run `/tokens` to check. This information should be ambient — always visible without asking.

## Design

1. In `format_usage_line()` in `src/format/mod.rs`, add a parameter for current context token count and max context tokens
2. Compute the percentage: `(current_tokens as f64 / max_tokens as f64 * 100.0) as u32`
3. Append to the usage line: `[47% context]` 
4. Color-code: green if <50%, yellow if 50-80%, red if >80%
5. In `print_usage()`, pass the agent's current message token count and effective_context_tokens

## Implementation

Update `format_usage_line` signature:
```rust
pub fn format_usage_line(
    usage: &yoagent::Usage,
    total: &yoagent::Usage,
    model: &str,
    elapsed: std::time::Duration,
    verbose: bool,
    context_used: Option<u64>,    // NEW: current context tokens
    context_max: Option<u64>,     // NEW: max context tokens
) -> Option<String> {
```

When both are Some, append context info:
```rust
let ctx_suffix = match (context_used, context_max) {
    (Some(used), Some(max)) if max > 0 => {
        let pct = (used as f64 / max as f64 * 100.0) as u32;
        let color = if pct > 80 { RED } else if pct > 50 { YELLOW } else { "" };
        format!(" · {color}{pct}% context{RESET}")
    }
    _ => String::new(),
};
```

Update `print_usage()` to accept and pass through the context parameters.

Update all call sites of `print_usage()` in `src/prompt.rs` — there should be 1-2 calls. Pass the agent's total message tokens and effective context max. The agent's messages are available via `agent.messages()`, and we can use `yoagent::context::total_tokens()` to count them.

Wait — `print_usage` is called from prompt.rs, which would be a third file. Let me reconsider.

**Revised approach:** Instead of changing the signature of print_usage (which is called from prompt.rs), make the context info a separate function and call it from prompt.rs right after print_usage. But that's still 3 files.

**Simpler approach:** Add a new `pub fn print_context_indicator(used: u64, max: u64)` function in `format/mod.rs` that prints a one-line context percentage. Then call it from prompt.rs after `print_usage()`. This way format/mod.rs gets the new function, and prompt.rs gets a one-line call — 2 files.

Actually format/mod.rs is `src/format/mod.rs` and prompt.rs is `src/prompt.rs` — that's 2 source files. The task limit is 3 files. This is fine.

## Implementation (revised)

In `src/format/mod.rs`, add:
```rust
/// Print a context window usage indicator line.
pub fn print_context_usage(used_tokens: u64, max_tokens: u64) {
    if max_tokens == 0 { return; }
    let pct = (used_tokens as f64 / max_tokens as f64 * 100.0) as u32;
    let color = if pct > 80 { RED } else if pct > 50 { YELLOW } else { GREEN };
    let bar = context_bar(used_tokens, max_tokens);  // reuse existing context_bar function
    println!("{DIM}  {bar} {color}{pct}% context{RESET}");
}
```

Wait, `context_bar` is in `format/cost.rs`. It's re-exported through `format/mod.rs`? Let me not use that — just print a simple percentage.

```rust
pub fn print_context_usage(used_tokens: u64, max_tokens: u64) {
    if max_tokens == 0 { return; }
    let pct = (used_tokens as f64 / max_tokens as f64 * 100.0) as u32;
    let color = if pct > 80 { RED } else if pct > 50 { YELLOW } else { GREEN };
    println!("{DIM}  {color}⬤{RESET}{DIM} {pct}% of context window used{RESET}");
}
```

In `src/prompt.rs`, after the `print_usage()` call (around line 1558), add:
```rust
let ctx_used = yoagent::context::total_tokens(agent.messages()) as u64;
let ctx_max = crate::cli::effective_context_tokens() as u64;
crate::format::print_context_usage(ctx_used, ctx_max);
```

## Files touched
- `src/format/mod.rs` — add `print_context_usage()` function + tests
- `src/prompt.rs` — add 3 lines after `print_usage()` call

## Tests to add

1. `test_print_context_usage_zero_max` — verify no panic/output when max is 0
2. Test the percentage calculation at boundaries (0%, 50%, 80%, 100%)
3. Test color selection (green/yellow/red)

Make the color logic a testable helper:
```rust
fn context_usage_color(pct: u32) -> &'static str { ... }
// test that directly
```

## Verification

- `cargo build` must pass
- `cargo test` must pass
- `cargo clippy --all-targets -- -D warnings` must pass
- After running the agent, each turn should show context percentage below the token usage line
