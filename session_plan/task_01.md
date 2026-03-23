Title: Streaming contract tests covering the optimized flush logic
Files: src/format.rs
Issue: #147

## Context

Issue #147 (streaming performance) has been worked on across multiple sessions. The streaming pipeline now has early-flush optimizations for digit-word patterns ("2nd"), dash-word patterns ("-based"), and whitespace-based flushing. But the previous attempt to add contract tests (reverted as Issue #164) failed because the tests didn't accurately model the renderer's behavior.

This task adds contract tests that document the *actual current behavior* of `needs_line_buffering()` and the render pipeline — they pin what exists, not what we wish existed.

## Implementation

Add these tests to the `#[cfg(test)] mod tests` block in `src/format.rs`:

1. **`test_streaming_contract_digit_word_flushes`** — Create a fresh `MarkdownRenderer`, set it to line_start=true (fresh state). Feed "2" then "n" then "d" via `render_delta()`. After "2n", the output should be non-empty because `needs_line_buffering()` returns false when a digit is followed by a non-`.`/non-`)` character. Verify the output contains "2" somewhere before the "d" arrives.

2. **`test_streaming_contract_dash_word_flushes`** — Same approach: feed "-" then "b" then "ased". After "-b", needs_line_buffering should return false (second char is not space or dash). Verify output is non-empty after "-b".

3. **`test_streaming_contract_numbered_list_buffers`** — Feed "1" then "." then " " then "item". The "1." pattern should keep buffering (needs_line_buffering returns true because the non-digit IS `.`). Verify that after "1.", the output is still empty or contains only the resolved prefix when " " arrives.

4. **`test_streaming_contract_unordered_list_buffers`** — Feed "- " then "item". The "- " pattern triggers list detection. Verify the output after "- " contains the bullet character (CYAN bullet).

5. **`test_streaming_contract_code_fence_buffers`** — Feed "`" then "`" then "`" then "rust\n". Should buffer until the fence resolves. Verify no output leaks before "```" is fully resolved.

6. **`test_streaming_contract_mid_line_immediate`** — Set line_start=false by first feeding "Hello" at line start (which flushes immediately). Then feed " world" — mid-line content should always flush immediately. Verify "world" appears in the output.

7. **`test_streaming_contract_plain_text_immediate`** — Feed "Hello" at line start. Since 'H' doesn't trigger any line-buffering pattern, it should flush immediately. Verify "Hello" is in the output.

8. **`test_streaming_contract_heading_buffers_then_resolves`** — Feed "#" then " " then "Title". After "#", should buffer. After "# ", should resolve as heading. Verify the heading marker appears.

**Important**: Each test must use a fresh `MarkdownRenderer::new()` and call `render_delta()` to simulate actual streaming. Do NOT call internal methods directly — test the public API only. Concatenate all outputs and verify the final string contains expected content.

**Testing approach**: Run each test individually first with `cargo test <test_name>` to verify before committing. The key insight from the failed attempt: the renderer's exact output depends on the full `render_delta` flow, not just `needs_line_buffering` in isolation. Test the integrated behavior.
