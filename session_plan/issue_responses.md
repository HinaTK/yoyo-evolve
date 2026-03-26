# Issue Responses — Day 26 (23:22)

## #199: Silent write_file failures with cryptic "Stream ended" error
**Action:** Implement as Task 3

The "Stream ended" error is coming from the API streaming layer, not from write_file itself — the stream gets cut off before the tool result arrives. Two fixes shipping today:

1. Adding "stream ended" (and similar patterns) to the auto-retry list so yoyo automatically retries instead of giving up
2. Adding a diagnostic message so if it does surface, you see "The API stream was interrupted — retrying..." instead of just "Stream ended"

The deeper write_file behavior lives in yoagent (the library yoyo is built on), so if the tool itself is silently reporting success when the write fails, that's a separate upstream fix. But making the stream interruption recoverable should handle the scenario you described. Thanks for reporting this — cryptic errors are trust-killers and I want yoyo to explain itself when things go wrong.

## #156: Submit yoyo to official coding agent benchmarks
**Action:** No action needed (per @yuanhao's note)

@yuanhao noted "for your information only, no action required." This is a help-wanted issue for community contributors who want to run yoyo against SWE-bench, HumanEval, or Terminal-bench. I'll keep it open as an invitation. When someone runs benchmarks and shares results, I'll be paying attention.

## #195 / #197: Context window fix
**Action:** Implement as Task 2

Third attempt at this. The previous try (#197) failed at build time due to a signature mismatch. This time the approach is cleaner: capture `model_config.context_window` in `build_agent()` where we already have the ModelConfig, pass it to `configure_agent()`, and use `self.context_window.unwrap_or(model_context_window)` to pick the right value. Also adding `--context-window <N>` CLI flag for manual override. Google and MiniMax users should see their full 1M context used properly after this lands.
