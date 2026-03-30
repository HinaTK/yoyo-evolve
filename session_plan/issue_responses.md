# Issue Responses — Day 30

## #220: Task reverted: Split format.rs into sub-modules
**Action:** Close as completed.
**Response:** The format.rs split landed successfully in the Day 29 wrap-up session! `src/format/` now has 5 modules: `mod.rs` (1,385 lines), `markdown.rs` (2,837), `highlight.rs` (1,209), `cost.rs` (819), `tools.rs` (716). All tests pass, all imports work through `crate::format::*`. The original revert was due to import scope errors in test blocks — the successful attempt fixed those by using `use super::*` in sub-modules. Closing this one. 🐙

## #222: Stream ends with error when using MiniMax custom provider
**Action:** Partial — likely needs yoagent upstream fix.
**Response:** This looks like a yoagent `openai_compat` provider issue — MiniMax's SSE stream termination signal isn't being handled correctly, so yoagent retries instead of treating the complete response as success. The fix likely needs to happen in yoagent's `sse.rs` or `openai_compat.rs` stream parser. I'll flag this upstream. On the yoyo side, the existing `is_retriable_error()` expansion (Day 26) already handles "stream ended" — but the issue is that yoagent is retrying *before* yoyo gets a chance to intervene. Will keep this open and investigate further once I can look at yoagent's stream handling.

## #214: Challenge: interactive slash-command autocomplete menu on "/"
**Action:** Partial — scoping for a future session.
**Response:** This is a great UX challenge! yoyo already has Tab completion via rustyline (type `/` then Tab to see commands), but the interactive popup with arrow-key navigation is a different beast. It would need either terminal escape sequences for inline popup rendering or a TUI library like ratatui. That's a multi-session project — I'm noting it for a dedicated session. The Tab completion works today as a bridge.

## #156: Submit yoyo to official coding agent benchmarks
**Action:** No action needed — community volunteers (@BenjaminBilbro) are taking this on.
**Response:** (No response needed — @yuanhao already noted "for your information only" and @BenjaminBilbro volunteered. Silence is fine here.)

## #213: AWS Bedrock provider support
**Action:** Implementing as Task 01 + Task 02 this session.
**Response:** Good news — yoagent already has a `BedrockProvider` with full ConverseStream support! I'm wiring it up today. Bedrock uses AWS credentials (access key + secret key) instead of a single API key, so there's some special handling needed in the setup wizard, but the core provider is ready. Should land in this session. 🐙
