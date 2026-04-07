Title: Wire session_budget_remaining() into task dispatch (finish #262)
Files: src/prompt.rs, scripts/evolve.sh (check only, do not modify — .github/workflows/ is DO-NOT-MODIFY)
Issue: #262

## Context

The 09:55 session added `prompt::session_budget_remaining()` — a function that returns `Some(remaining_secs)` when `YOYO_SESSION_BUDGET_SECS` is set, and `None` otherwise. It has three unit tests. **But nothing in production actually calls it.** CLAUDE.md literally says "currently exposed but not yet wired into task dispatch — that's a follow-up task."

This is the exact "facade before substance" trap from the Day 30 learning. Either wire it up or delete it. This task wires it up.

## What to do

**Step 1: find the call sites in prompt.rs that do repeated work.**

The agent side of the evolution loop consists of multiple `run_prompt*` functions and retry loops in `src/prompt.rs`:
- `run_prompt_auto_retry` (with `MAX_AUTO_RETRIES`)
- `run_prompt_auto_retry_with_content`
- The watch-mode fix loop (`MAX_WATCH_FIX_ATTEMPTS`, `build_watch_fix_prompt`, `run_watch_command`)
- Any retry helper that loops on overflow/retriable errors

These are the places where a budget check makes sense: **before starting a new retry attempt**, ask `session_budget_remaining()`. If it returns `Some(0)` or a value below a small threshold (e.g. 30 seconds), log a single line ("⏱ session budget exhausted, stopping retries early") and return the most recent outcome instead of starting another attempt.

**DO NOT** add budget checks inside tight inner loops (per-token, per-event). Only at the retry boundaries — that's what matters for #262 (the session being killed mid-push after too many fix attempts).

**Step 2: add a helper.**

In `src/prompt.rs`, add a small helper right below `session_budget_remaining()`:

```rust
/// Returns true if the session budget is set and has ≤ `grace_secs` remaining.
/// Returns false if the budget is unset (unbounded) or there's still headroom.
pub fn session_budget_exhausted(grace_secs: u64) -> bool {
    match session_budget_remaining() {
        Some(remaining) => remaining.as_secs() <= grace_secs,
        None => false,
    }
}
```

Write 3 unit tests:
1. With `YOYO_SESSION_BUDGET_SECS` unset → `session_budget_exhausted(30)` returns `false` (unbounded sessions never "exhaust")
2. With `YOYO_SESSION_BUDGET_SECS=9999` → `session_budget_exhausted(30)` returns `false` (headroom)
3. With `YOYO_SESSION_BUDGET_SECS=1` and a `std::thread::sleep` past the budget → `session_budget_exhausted(30)` returns `true`

**IMPORTANT:** `session_budget_remaining()` uses a process-wide `OnceLock` or lazy initializer for the start time. The existing tests almost certainly isolate via env vars with unique names or `serial_test`. Study how the existing tests around `session_budget_remaining` handle this and **follow the same pattern exactly**. If the existing tests use `std::sync::Mutex` to serialize, use the same mutex. If they use `serial_test`, add `#[serial]`.

**Step 3: call it from the retry loops.**

In `run_prompt_auto_retry` (and `run_prompt_auto_retry_with_content` — they likely share structure), right at the top of the retry loop body (before calling `run_prompt`), add:

```rust
if session_budget_exhausted(30) {
    eprintln!("⏱ session budget nearly exhausted, stopping retries early");
    break; // or return the current outcome, whichever fits the fn signature
}
```

For the watch fix loop (`MAX_WATCH_FIX_ATTEMPTS`), add the same check at the top of each attempt.

**Step 4: verify scripts/evolve.sh does NOT set YOYO_SESSION_BUDGET_SECS.**

Just `grep -n YOYO_SESSION_BUDGET_SECS scripts/evolve.sh` and note the result. **DO NOT modify evolve.sh** — it's in the do-not-modify list. If it already exports the var, great. If not, file the shell-side wiring as a follow-up in the journal. The point of this task is to make the Rust side ready; the shell-side export is a separate concern (and a separate PR that a human would need to approve, since evolve.sh is protected).

**Step 5: update CLAUDE.md.**

Find the paragraph in CLAUDE.md that starts "Currently exposed but not yet wired into task dispatch — that's a follow-up task." Replace it with a sentence describing the actual wiring: "`session_budget_remaining()` is now consulted at the top of each retry attempt in `run_prompt_auto_retry` and the watch-mode fix loop via `session_budget_exhausted(30)`; when ≤30s remain, retries stop early and the current outcome is returned."

## Acceptance

- `cargo build && cargo test && cargo clippy --all-targets -- -D warnings && cargo fmt --check` all pass
- New helper `session_budget_exhausted` exists with 3 unit tests
- At least one retry loop in `run_prompt_auto_retry` (and the watch loop) calls `session_budget_exhausted(30)` and breaks/returns early when true
- Running `cargo run -- --version` still works (smoke test — the change must not break cold-start)
- `YOYO_SESSION_BUDGET_SECS=10000 cargo run -- --version` still works (env var set, budget not exhausted, no behavior change)
- CLAUDE.md paragraph updated to reflect actual wiring (not "follow-up task")
- One-line note in the journal: whether `scripts/evolve.sh` exports the env var or not (finding, not action)

## Why

This closes issue #262's Rust-side arc. The 09:55 session built the plumbing; this session connects the drain. If the budget function is wired but `evolve.sh` never sets the env var, the behavior is unchanged (unbounded sessions, as today) — which is safe. If a human updates `evolve.sh` later to set the env var, the retry loops immediately start respecting it. Either way, the trap from Day 30 is resolved and CLAUDE.md stops lying about what's done.
