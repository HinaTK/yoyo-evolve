Title: Add streaming contract tests documenting current behavior
Files: src/format.rs
Issue: #164, #147

The reverted task #164 failed because it tried to change buffering behavior AND add tests simultaneously. This task takes the safe approach: add tests that document and lock in the *current* behavior of the streaming pipeline. No behavior changes — just a regression test suite.

**Why this matters:** The streaming renderer has been modified across Days 20-23 with incremental fixes. Without a comprehensive contract test suite, any future changes risk regressing the carefully tuned behavior. These tests protect what works.

**Specific tests to add** (all in `src/format.rs` under `#[cfg(test)]`):

1. **`test_streaming_contract_plain_text_no_buffering`** — Feed "Hello world" token-by-token at line start. The first token "H" should produce immediate output (not special char). Verify `line_buffer` stays empty for subsequent mid-line tokens.

2. **`test_streaming_contract_code_block_passthrough`** — Open a code fence with "```rust\n", then feed tokens "let x" and " = 42;". All tokens inside the code block should produce immediate output (code blocks use the fast path, not the buffered path).

3. **`test_streaming_contract_heading_detection`** — Feed "#" at line start, then "# Title\n". The "#" should buffer. After " Title\n" completes the line, output should contain the heading with bold formatting.

4. **`test_streaming_contract_blockquote_detection`** — Feed "> " at line start, then "quoted text\n". Verify the blockquote formatting is applied.

5. **`test_streaming_contract_inline_formatting_mid_line`** — Mid-line **bold**, *italic*, and `code` formatting. Feed "This is **bold** text" as mid-line content and verify bold ANSI codes appear.

6. **`test_streaming_contract_empty_delta`** — Calling `render_delta("")` should return an empty string and not corrupt state. Test at both line_start=true and line_start=false.

7. **`test_streaming_contract_newline_resets_line_start`** — After rendering mid-line content, a "\n" should set `line_start = true` for the next token.

8. **`test_streaming_contract_consecutive_code_blocks`** — Open fence, content, close fence, then open another fence. State should correctly track in_code_block across transitions.

9. **`test_streaming_contract_flush_final`** — After feeding partial content without a trailing newline, `flush()` should emit whatever's in the line buffer. This protects the end-of-response path.

10. **`test_streaming_contract_nested_formatting_in_list`** — Feed "- **bold item**\n" and verify both list formatting and bold formatting apply.

**Important:** For each test, first verify what the renderer *actually does* by running the code mentally through the existing `render_delta` and `flush` paths. Write tests that assert the actual behavior, not aspirational behavior. If you're unsure what the current behavior is, write a small exploration first, run it, then write the assertion.

The tests should be grouped under a comment header `// ── Streaming contract tests ──` near the end of the test module.
