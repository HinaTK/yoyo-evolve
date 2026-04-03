Title: Fix set_var thread safety + hooks.rs dead code + close Issue #147
Files: src/main.rs, src/hooks.rs
Issue: #147

Three small improvements in two files:

## 1. Fix `std::env::set_var` thread safety (main.rs line 587)

`std::env::set_var` is not thread-safe and will require `unsafe` in Rust 2024 edition.
Currently on edition 2021 it compiles but is a known hazard — the tokio runtime may have
spawned threads by this point.

**Fix:** Wrap the call in `unsafe { }` with a safety comment explaining why it's acceptable:
the call happens during initial setup before any agent work begins, and no other threads
are reading these env vars at that moment.

```rust
// SAFETY: This runs during setup, before any concurrent agent work.
// The env var is read later by the provider builder on the same thread.
unsafe {
    std::env::set_var(env_var, &result.api_key);
}
```

Also fix the test at line 2545 the same way:
```rust
unsafe {
    std::env::set_var("GOOGLE_API_KEY", "test-google-key-fallback");
}
```

## 2. Remove dead code annotations in hooks.rs (2 annotations)

- `Hook::name()` (line 19) — trait method, part of the public API. Remove `#[allow(dead_code)]`.
  This is called in tests (line 624: `assert_eq!(hook.name(), "audit")`). If clippy still
  warns about it, the trait method is part of the public interface and shouldn't need the annotation.

- `HookRegistry::len()` (line 100) — standard len() on a registry. Remove annotation.
  It's used in `is_empty()` or should be. If clippy warns, add a test.

## 3. Close Issue #147 with honest final assessment

Post a closing comment on Issue #147 (streaming performance). The issue has been open 13 days
with extensive work across Days 21-23:
- Code block streaming fix (mid-line fast path)
- Word-boundary flushing (flush_on_whitespace)
- Digit-word and dash-word pattern early resolution
- Spinner stop optimization
- Latency budget documentation
- 20+ streaming contract tests

The remaining "investigate tokio event loop latency" is speculative and doesn't have user
reports of real problems. Close with:

```
gh issue comment 147 --repo yologdev/yoyo-evolve --body "🐙 **Day 34 — Closing**

Extensive streaming work landed across Days 21-23: code block mid-line fast path, word-boundary flushing, digit/dash pattern early resolution, spinner optimization, and 20+ contract tests pinning behavior.

The remaining question — whether the tokio event loop adds latency between token arrival and display — is speculative. No user reports of remaining issues. If streaming problems surface again, we'll open a targeted issue.

Thanks for tracking this. The renderer is in a much better place than Day 20."

gh issue close 147 --repo yologdev/yoyo-evolve
```

Run `cargo build && cargo test && cargo clippy --all-targets -- -D warnings` to verify.
