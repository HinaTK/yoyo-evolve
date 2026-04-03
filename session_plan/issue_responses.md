# Issue Responses — Day 34 (11:02)

## #240: Release changelog
**Status:** Already shipped (Day 34, 01:08)
**Response:** The script shipped, retroactive changelogs were applied to all 5 releases, and @yuanhao confirmed the workflow change (#241) is live. @danstis's request is fully addressed. Close the issue with a thank-you.

**Comment to post:**
Closing this one — the changelog extraction is shipped and wired into the release workflow. Next release will automatically include curated notes from CHANGELOG.md. Thanks @danstis for the push, and @yuanhao for merging the workflow change! 🐙

## #156: Submit yoyo to official coding agent benchmarks
**Status:** Help-wanted, community volunteer active
**Response:** @BenjaminBilbro volunteered to run benchmarks with a local model. @yuanhao confirmed that would be great. No action needed from me — the community is handling this. Skip responding (silence is better than noise — the last update was between @yuanhao and @BenjaminBilbro, and they don't need me in the middle of that conversation).

## #21: Hook Architecture Pattern (not in today's issues but flagged in assessment)
**Status:** Fully implemented — Hook trait, HookRegistry, AuditHook, ShellHook, HookedTool wrapper, config-based hook registration via `.yoyo.toml` all exist in src/hooks.rs. This is exactly what @theLightArchitect proposed and @yuanhao endorsed.
**Action:** Close with a detailed comment explaining what shipped.

**Comment to post:**
🐙 Closing this one — the hook architecture is fully shipped!

Here's what landed across Days 22-31:

- **`Hook` trait** with `pre_execute` / `post_execute` — exactly the pattern @theLightArchitect proposed
- **`HookRegistry`** — ordered pipeline, pre-hooks can block or short-circuit, post-hooks can modify output
- **`AuditHook`** — logs all tool calls to `.yoyo/audit.jsonl` (enable with `--audit` or `YOYO_AUDIT=1`)
- **`ShellHook`** — runs arbitrary shell commands before/after tool execution
- **`HookedTool`** wrapper — the outermost layer in the tool pipeline
- **Config-based registration** via `.yoyo.toml`:
  ```toml
  [hooks]
  pre.bash = "echo 'about to run bash'"
  post.write_file = "echo 'file was written'"
  ```

All in `src/hooks.rs` (830 lines, 20+ tests). Thanks for the design that made this possible — the pattern was exactly right.
