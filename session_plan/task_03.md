Title: Improve error diagnostics for "Stream ended" and write_file failures
Files: src/prompt.rs
Issue: #199

## Problem

Issue #199 reports that when write_file fails (e.g., due to container sandboxing or filesystem restrictions), the user sees only a cryptic "Stream ended" error with no explanation, recovery suggestion, or actionable information.

The "Stream ended" error isn't from yoyo — it's from the API provider's streaming response getting cut off (network issue, context overflow, or server-side abort). But yoyo can diagnose it better.

## Analysis

Looking at the code:
1. `diagnose_api_error()` in `src/prompt.rs` handles auth (401), model not found (404), network, and permission (403) errors — but NOT "stream ended" or generic disconnection errors.
2. `is_retriable_error()` doesn't match "stream ended" either, so it won't auto-retry.
3. The write_file tool itself (in yoagent) does return errors on failure, but if the API stream dies mid-response, the tool result never arrives — the user just sees "Stream ended."

## Fix: Two improvements

### Improvement 1: Add "stream ended" to retriable errors and diagnostics

In `src/prompt.rs`, update `is_retriable_error()` — add to the retriable patterns:
```rust
"stream ended",
"stream closed",
"unexpected eof",
"broken pipe",
"reset by peer",
"incomplete",
```

These are all transient network/streaming errors that should trigger auto-retry.

In `diagnose_api_error()`, add a new diagnostic section after the network errors block:

```rust
// ── Stream / connection interruption ────────────────────────────
if lower.contains("stream ended")
    || lower.contains("stream closed")
    || lower.contains("unexpected eof")
    || lower.contains("broken pipe")
    || lower.contains("incomplete")
{
    return Some(
        "The API stream was interrupted before the response completed.\n\
         This is usually a transient network issue — yoyo will auto-retry.\n\
         If it persists, check your internet connection or try a different model."
            .to_string(),
    );
}
```

### Improvement 2: Add tests for new patterns

Add tests to the existing test section in `src/prompt.rs`:

```rust
#[test]
fn test_stream_ended_is_retriable() {
    assert!(is_retriable_error("Stream ended"));
    assert!(is_retriable_error("stream closed unexpectedly"));
    assert!(is_retriable_error("unexpected eof while reading"));
    assert!(is_retriable_error("broken pipe"));
}

#[test]
fn test_diagnose_stream_ended() {
    let diag = diagnose_api_error("error: Stream ended", "claude-sonnet-4-20250514");
    assert!(diag.is_some());
    assert!(diag.unwrap().contains("interrupted"));
}
```

### What this does NOT fix

The underlying write_file tool behavior is in yoagent, not yoyo. If the tool itself fails silently, that's a yoagent issue. What yoyo CAN do is:
1. Make "stream ended" a retriable error → auto-retry kicks in
2. Show a helpful diagnostic → user knows what happened
3. These two together mean the user sees a brief "auto-retrying..." message and the operation usually succeeds on retry

### Verify

```bash
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt -- --check
```
