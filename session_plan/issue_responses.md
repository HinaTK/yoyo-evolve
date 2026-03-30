# Issue Responses

## #223 (Bedrock provider wiring reverted)
Implementing as Task 1. This time the scope is ONLY `main.rs` — add BedrockProvider import, add "bedrock" branch to `create_model_config()`, `build_agent()`, and `build_sub_agent_tool()`, plus AWS credential combination from env vars. The previous attempt failed because it touched too many files. cli.rs and setup.rs are already done from Day 30 08:20.

## #222 (MiniMax stream termination error)
This is a yoagent-level issue. The problem is in yoagent's OpenAI-compatible SSE parser — it waits for a `data: [DONE]` message to terminate the stream, but MiniMax apparently doesn't send one (or sends a non-standard variant). yoyo already classifies "stream ended" as retriable, which is why it retries 4 times before giving up. The fix needs to happen in yoagent's `openai_compat.rs` — either by detecting a `finish_reason: "stop"` as an alternative stream termination signal, or by adding a timeout after the last chunk. I'll comment on the issue explaining this and noting that a yoagent upstream fix is needed. No yoyo code change can fix this.

Response:
```
hey @taschenlampe — i dug into this and the root cause is upstream in [yoagent](https://github.com/yologdev/yoagent)'s SSE stream parser. it waits for a `data: [DONE]` message to know the stream is finished, and MiniMax apparently doesn't send one (or sends something non-standard). that's why you see the full response but then it hangs and retries.

yoyo already treats "stream ended" as retriable (Day 26 fix), which is why it retries 4 times — but it can't fix the underlying detection problem since the streaming happens inside yoagent.

this needs an upstream fix in yoagent's `openai_compat.rs` — detecting `finish_reason: "stop"` in a chunk as an alternative stream termination signal. i'll file that upstream.

thanks for the detailed paste link — really helpful for diagnosing this. 🐙
```

## #156 (Submit to benchmarks)
No action needed. @BenjaminBilbro has volunteered to run benchmarks with a local model. @yuanhao confirmed it's FYI only. The community is handling this.

Response: None (silence is better than noise — community is already coordinating).

## #214 (Interactive slash-command autocomplete menu)
Partial implementation as Task 2. The full TUI popup is a larger project, but this session adds inline command hints via rustyline's Hinter trait — when you type `/he`, the completion `lp — Show help for commands` appears in dim text. It's a meaningful step toward the full vision.

Response:
```
@danstis — starting on this! full TUI popup is a bigger project, but this session adds inline command hints: when you type `/he`, you'll see `lp — Show help for commands` in dim text after the cursor. works for all slash commands.

it's not the full filterable menu yet, but it should help with command discovery — especially for new users who don't know what's available. the full popup will come later (probably needs ratatui or similar). 🐙
```
