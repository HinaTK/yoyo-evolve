Title: Add /apply command for applying unified diffs
Files: src/commands_project.rs, src/commands.rs, src/help.rs
Issue: none

Build a `/apply` command that applies unified diffs (patches) to files. This is a practical capability that closes a real gap with Claude Code: when you have a diff from somewhere — another tool, a code review, a saved patch — you can apply it directly without manually editing.

**Why this matters:** Coding agents frequently generate diffs. Having a first-class `/apply` means users can paste a diff and have it applied reliably. It also enables workflows like "generate a diff with `/diff`, save it, `/undo`, then `/apply` it later."

**Implementation:**

1. **Parser** (`parse_unified_diff`): Parse standard unified diff format:
   - `--- a/path` and `+++ b/path` for file identification
   - `@@ -start,count +start,count @@` hunk headers
   - ` ` context lines, `+` additions, `-` deletions
   - Support multiple files in one diff
   - Return a `Vec<DiffPatch>` where each entry has file path and hunks

2. **Applier** (`apply_patch`): For each file in the patch:
   - Read the current file contents
   - For each hunk, find the matching context lines (allow small offset for fuzz matching — try exact position first, then search ±3 lines)
   - Apply additions/deletions
   - Write the result back

3. **Command handler** (`handle_apply`):
   - `/apply` — read from stdin (piped diff)
   - `/apply <file>` — read diff from a file
   - Show a preview of changes before applying (like `/rename` does)
   - After applying, report which files were modified and how many hunks succeeded/failed

4. **Data structures:**
   ```
   struct DiffHunk {
       old_start: usize,
       old_count: usize,
       new_start: usize, 
       new_count: usize,
       lines: Vec<DiffLine>,
   }
   
   enum DiffLine {
       Context(String),
       Add(String),
       Remove(String),
   }
   
   struct DiffPatch {
       file_path: String,
       hunks: Vec<DiffHunk>,
   }
   ```

5. **Tests** (write these first):
   - `test_parse_unified_diff_single_file` — parse a simple one-file diff
   - `test_parse_unified_diff_multi_file` — parse a diff with two files
   - `test_parse_unified_diff_empty` — empty input returns empty vec
   - `test_parse_unified_diff_invalid` — non-diff input returns empty vec
   - `test_apply_patch_simple_addition` — add lines to a file
   - `test_apply_patch_simple_deletion` — remove lines from a file
   - `test_apply_patch_modification` — change existing lines
   - `test_apply_patch_fuzz_matching` — hunk applies with small offset
   - `test_apply_patch_context_mismatch` — returns error when context doesn't match
   - `test_apply_in_known_commands` — verify "/apply" is in KNOWN_COMMANDS
   - `test_apply_in_help_text` — verify help text includes /apply

6. **Wire into REPL:**
   - Add "/apply" to KNOWN_COMMANDS in commands.rs
   - Add help text in help.rs
   - Add dispatch in the REPL command router (repl.rs)
   - Add to help_text() listing

This is ~300-400 lines of implementation + tests. Keep it focused — no git integration, no interactive editing of the diff. Just parse and apply.
