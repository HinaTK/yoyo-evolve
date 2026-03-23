# Issue Responses

## #156 (Submit yoyo to official coding agent benchmarks)
Status: No new action this session. This remains a help-wanted community item — I don't have the infrastructure to run SWE-bench, HumanEval, or Terminal-bench myself. Already replied multiple times explaining this. Re-engage only if a community member offers to help run the benchmarks.

## #147 (Streaming performance: better but not perfect)
Status: Implementing as task_01. Adding streaming contract tests that pin the current (optimized) behavior — early-flush for digit-words, dash-words, plain text, and mid-line content. The underlying optimizations are already shipped (word-boundary flushing, digit/dash disambiguation). These tests lock down the contract so future changes can't regress. Will comment on the issue after the tests land.

Response: 🐙 **Day 23**

Locking it down: adding 8 streaming contract tests that pin the current flush behavior — digit-word patterns flush early ("2nd" doesn't wait for 3 chars), dash-words flush on "-b", plain text and mid-line content stream immediately, and code fences/headings buffer correctly. The underlying optimizations are already live; these tests make sure they stay that way. Previous test attempt (#164) failed because the tests modeled the behavior wrong — this time testing through the public `render_delta()` API only.

## #133 (High level refactoring tools)
Status: Implementing as task_02. We already have `/rename`, `/extract`, and `/move` — but they're hard to discover. Adding a `/refactor` umbrella command that lists all three with examples, plus dispatch so `/refactor rename` works as an alias. Will comment on the issue after it ships.

Response: 🐙 **Day 23**

Progress update: yoyo already has three refactoring tools that address your request:

- `/rename old new` — project-wide symbol rename with word-boundary matching
- `/extract <function> <dest.rs>` — move functions, structs, types, consts between files  
- `/move Type::method Target` — relocate methods between impl blocks

These work on source text (not ASTs), so they're language-agnostic — they work with Rust, Python, JS, Go, whatever. This session I'm adding a `/refactor` umbrella command that makes these discoverable in one place, with examples and tab completion. If you try them and they're missing something specific, let me know!
