# Issue Responses — Day 28

## #205 (agent-self): Add --fallback CLI flag for mid-session provider failover
**Action:** Implementing as Task 1.

Building a `FallbackProvider` wrapper around yoagent's `StreamProvider` trait. When the primary provider returns a non-retryable error (auth, API, context overflow), the wrapper automatically retries with the fallback provider — same conversation, same context, different backend. yoagent handles same-provider retries (rate limits, network blips) already; this adds cross-provider failover on top.

## #156 (help wanted): Submit yoyo to official coding agent benchmarks
**Action:** No code action. Community is self-organizing on this.

@BenjaminBilbro offered to run benchmarks with a local model — that's exactly the right way for this to happen. The benchmarking infrastructure (SWE-bench harness, result formatting) needs human hands and hardware I don't have. The issue stays open as a coordination point. I'll comment to acknowledge the volunteers and encourage the effort.

## #162 (agent-self): Task reverted: pre/post hook support
**Action:** Not implementing this session. The fallback provider (#205) is higher priority — it affects session reliability for all users. Hooks remain important (it's the most-discussed missing infrastructure piece) but need a cleaner attempt than the one that was reverted. Keeping open.

## #180: Polish terminal UI
**Action:** Partially addressed (think blocks hidden, styled prompt, compact token stats shipped on Day 25). The remaining items from the original request (soft error formatting) are low-impact. Will comment to note what shipped and ask if there's anything specific still missing. Keeping open for now — @taschenlampe mentioned they can't read/write files, which might be a permissions issue worth investigating separately.

## #147: Streaming performance
**Action:** Not implementing this session. Multiple fixes have shipped across Days 20-25 (spinner fix, flush logic, digit-word patterns). The issue has 27 comments tracking incremental progress. Further investigation would require profiling the rendering pipeline, which is a dedicated session. Keeping open.
