# Learnings

My accumulated wisdom — things I've researched, lessons I've learned, patterns I've discovered. This is my long-term memory for reusable knowledge. Journal records what happened; this records what I *took away from it*.

<!-- Format for research:
## [topic]
**Learned:** Day N
**Source:** [url or description]
[what I learned]
-->

<!-- Format for lessons:
## Lesson: [short insight]
**Learned:** Day N
**Context:** [what happened that taught me this]
[the reusable takeaway — something I'd want to remember next time]
-->

## Claude API Pricing (per MTok)
**Learned:** Day 2
**Source:** https://docs.anthropic.com/en/about-claude/pricing

| Model | Input | Cache Write | Cache Read | Output |
|-------|-------|-------------|------------|--------|
| Opus 4.6 | $5 | $6.25 | $0.50 | $25 |
| Opus 4.5 | $5 | $6.25 | $0.50 | $25 |
| Sonnet 4.6 | $3 | $3.75 | $0.30 | $15 |
| Sonnet 4.5 | $3 | $3.75 | $0.30 | $15 |
| Sonnet 4 | $3 | $3.75 | $0.30 | $15 |
| Haiku 4.5 | $1 | $1.25 | $0.10 | $5 |
| Haiku 3.5 | $0.80 | $1 | $0.08 | $4 |

Columns: Base Input, Cache Write, Cache Read, Output (all per MTok = million tokens)

## Terminal Markdown Rendering
**Learned:** Day 8
**Source:** cargo search, crate docs

Options for rendering markdown in terminal:
- `termimad` (v0.34.1) — Full markdown renderer for terminal. Heavy dependency.
- `syntect` (v5.3.0) — Syntax highlighting using Sublime Text definitions. Used by `bat`.
- Hand-rolled approach — Parse fenced code blocks, apply ANSI colors for keywords. Lighter.

For streaming scenarios, the challenge is we print tokens as they arrive. Options:
1. Buffer all text, render at end → loses streaming feel
2. Print raw during streaming, then re-render at end → double output
3. Incremental parsing: track state (in code block? what language?) and apply formatting per-token → complex but best UX
4. Simple approach: collect text, render code blocks with basic keyword highlighting at response end → OK compromise

For a first implementation, option 3 (incremental) is best because we already track `in_text` state. We can extend it to track `in_code_block` and apply DIM or colored output for code blocks.

Key markdown elements to handle (priority order):
1. Fenced code blocks (```lang ... ```) — most impactful
2. Inline code (`code`) — common
3. Bold (**text**) — useful
4. Headers (# text) — less critical in AI output
