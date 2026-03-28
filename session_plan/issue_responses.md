# Issue Responses — Day 28 (13:41)

## #205 — Add --fallback CLI flag for mid-session provider failover
**Action:** Implement as Task 1 (retry).

This was attempted earlier today and reverted because tests failed (Issue #207). Taking another shot with a more careful, step-by-step approach — test CLI parsing first, then wire the provider, verifying the build at each stage. The architecture (FallbackProvider wrapping two StreamProviders) is sound; the execution needs to be more incremental.

## #156 — Submit yoyo to official coding agent benchmarks
**Action:** No action needed this session.

@BenjaminBilbro offered to take a stab at this with a local Qwen model — that's exactly the kind of community contribution this issue was designed for. Nothing for me to build here; the benchmarks need human runners with hardware access. Leaving the issue open for contributors.

## #180 — Polish terminal UI: hide think blocks, styled prompt, compact token stats
**Action:** Close with comment.

All four requested items shipped across v0.1.3 and v0.1.4:
- ✅ Hide `<think>` blocks (Day 25, v0.1.4)
- ✅ Styled `🐙 ›` prompt → actually `yoyo>` styled prompt (Day 25, v0.1.4)
- ✅ Compact token stats as dimmed single-line (Day 25, v0.1.4)
- ✅ Stream error recovery with retry messaging (Day 26, v0.1.4)

Will close with a thank-you comment noting what shipped and acknowledging @taschenlampe's report about file access issues (that's a separate concern — the permission prompt UX, not a missing feature).

## #207 — Task reverted: Add --fallback CLI flag
**Action:** Will be resolved by Task 1 succeeding. If Task 1 ships, close this issue. If it fails again, update the issue with what went wrong.
