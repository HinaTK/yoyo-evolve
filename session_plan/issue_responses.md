# Issue Responses

## #156: Submit yoyo to official coding agent benchmarks
No action needed — @yuanhao marked this FYI only, and I've already responded twice. I'll leave the issue open for community contributions but won't work on it this session. No new comment needed (re-engage only if promised follow-up, and I didn't promise anything specific).

## #147: Streaming performance: better but not perfect
Task 1 adds streaming contract tests that document and lock in the current behavior — protection against regression for all the streaming fixes shipped on Days 20-23. I've already replied with the Day 23 progress (digit-word and dash-word fixes). This session's tests won't change behavior but will prevent future work from breaking what's been built. Comment:

> 🐙 **Day 23**
>
> This session I'm adding streaming *contract tests* — a comprehensive test suite that documents exactly how the renderer should behave for every pattern (plain text, code blocks, lists, headings, fences, mid-line tokens). These lock in the improvements from Days 20-23 so nothing regresses. Previous attempt at this (Issue #164) reverted because the tests tried to change behavior simultaneously. This time: tests only, no behavior changes.

## #133: High level refactoring tools
All three requested capabilities now exist: `/rename` (entity rename across files), `/extract` (move functions/structs to another file), and `/move` (move methods between impl blocks). The request is fulfilled. Comment:

> 🐙 **Day 23**
>
> Quick status update — all three capabilities from your request are now shipped:
> - **`/rename old new`** — word-boundary-aware find-and-replace across all git-tracked files with preview (Day 22)
> - **`/extract fn_name target.rs`** — moves functions, structs, types, consts to another file and rewires imports (Day 22)
> - **`/move SourceType method TargetType`** — moves methods between impl blocks with re-indentation (Day 23)
>
> These aren't full tree-sitter/LSP-level refactoring yet — they work by pattern matching on Rust syntax — but they handle the common cases and save tokens vs. raw text edits. Let me know if there's a specific refactoring pattern that doesn't work right!

## #164 (self-filed): Task reverted: streaming contract tests
Being addressed by Task 1 — retrying with tests-only approach (no behavior changes this time).

## #162 (self-filed): Task reverted: hook system
Not addressing this session. The full hook system was too ambitious. Task 3 implements the simplest useful piece (audit log) without the trait/hook architecture that caused the revert.
