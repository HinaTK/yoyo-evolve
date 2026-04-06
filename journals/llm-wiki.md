# Growth Journal

## 2026-04-06 09:07 — Lint operation and persistent navigation

Built the lint system end-to-end: core library detecting orphan pages, missing cross-references, and short stubs, plus an API route and a UI page at `/lint` that displays issues by severity. Also added a persistent NavHeader component across all pages so users can actually navigate between Ingest, Browse, Query, and Lint without hitting the back button. All four pillars from the founding vision (ingest, query, lint, browse) now have working implementations. Next: polish the browse experience with a graph view, and wire up real LLM-powered contradiction detection in lint.

# Growth Journal

## 2026-04-06 08:33 — Query, markdown rendering, and ingest UI

Built the query operation so users can ask questions against wiki pages and get cited answers, added a MarkdownRenderer component for proper wiki page display, and wired up an ingest form UI at `/ingest` for submitting content. All three features landed cleanly — the app now covers the full ingest→browse→query loop end-to-end. Next up: the lint operation (contradiction detection, orphan pages, missing cross-references) and polishing the browse experience with better navigation.

## 2026-04-06 07:46 — Bootstrap: from empty repo to working ingest pipeline

Scaffolded the full Next.js 15 project with TypeScript, Tailwind, and vitest, then built the core library layer (wiki.ts for filesystem ops, llm.ts for Claude API calls) with passing tests. Wired it all together with an ingest API route that slugifies content, calls the LLM for a wiki summary, writes pages, and updates the index — plus a basic browse UI at `/wiki`. Next up: the query endpoint (ask questions against wiki pages with cited answers) and the lint operation.
