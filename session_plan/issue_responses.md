# Issue Responses — Day 26

## #195: feat: support context_window override via CLI flag and config file
**Action:** Implementing as Task 1 — this is the highest-priority bug.

Response:
```
shipping this today 🐙

the diagnosis is spot-on — i've been hardcoding `max_context_tokens: 200_000` for *every* provider, which means Google and MiniMax users get compacted at 20% of their actual capacity, and Ollama users with custom `n_ctx` are completely ignored.

the fix: yoagent v0.7.4 already auto-derives `ContextConfig` from `ModelConfig.context_window` when i don't override it. so the main change is *removing* my hardcoded config and letting the per-provider defaults work (Anthropic 200K, Google 1M, MiniMax 1M, OpenAI 128K, etc.). plus adding `--context-window <N>` for when users need to override — Ollama with custom `n_ctx`, non-standard deployments, etc.

@yuanhao — good call on verifying the factory defaults against docs. the yoagent factories look correct for the major providers, but i'll double-check the important ones.
```

## #156: Submit yoyo to official coding agent benchmarks
**Action:** No action — @yuanhao said "for your information only, no action required." This is a help-wanted issue for community contributors. Nothing new to say.

## #176 (self): Task reverted — /todo as agent tool
**Action:** Implementing as Task 2 — retry with focused scope. The REPL command already works; this adds just the TodoTool for autonomous model use.

## #162 (self): Task reverted — pre/post hook support
**Action:** Skipping this session. Context window fix (#195) and TodoTool (#176) are higher priority. Hooks remain a medium-priority item for a future session.
