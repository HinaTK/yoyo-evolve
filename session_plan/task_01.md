Title: Fix multi-word argument handling in bare subcommands
Files: src/cli.rs, src/commands_search.rs
Issue: none

## Problem

`yoyo grep "fn main"` silently fails. The shell correctly passes `["yoyo", "grep", "fn main"]` as args (with "fn main" as one element), but `try_dispatch_subcommand` reconstructs the input as:

```rust
let input = format!("/{}", args[1..].join(" "));
// produces: "/grep fn main"
```

Then `parse_grep_args` splits on whitespace, treats "fn" as the pattern and "main" as the path → "No matches found". The quoting boundary from the shell is destroyed.

This affects `grep`, `find`, `blame`, and any subcommand that takes multi-word arguments.

## Fix

The root cause is that `args[1..].join(" ")` loses the information about which args were a single quoted token. Two complementary fixes:

### Fix 1: Quote args that contain spaces in `try_dispatch_subcommand` (cli.rs)

When reconstructing the `/command ...` string from shell args, any arg that contains whitespace should be wrapped in double quotes so the downstream parsers can distinguish multi-word patterns from separate arguments:

```rust
// Instead of: format!("/{}", args[1..].join(" "))
// Do:
let parts: Vec<String> = args[1..].iter().map(|a| {
    if a.contains(' ') || a.contains('\t') {
        format!("\"{}\"", a)
    } else {
        a.clone()
    }
}).collect();
let input = format!("/{}", parts.join(" "));
```

This produces `/grep "fn main"` instead of `/grep fn main`.

### Fix 2: Make `parse_grep_args` respect quoted strings (commands_search.rs)

Update `parse_grep_args` to handle double-quoted patterns. Instead of naive `split_whitespace()`, use a simple shell-like tokenizer that keeps quoted strings together:

```rust
// Tokenize respecting double quotes
// "fn main" src/ → ["fn main", "src/"]
```

Apply the same fix to any other parsers that have the same problem (`parse_blame_args` if relevant, etc.).

### Tests

Add tests:
- `parse_grep_args` with quoted pattern: `'/grep "fn main"'` → pattern = "fn main", path = "."
- `parse_grep_args` with quoted pattern and explicit path: `'/grep "fn main" src/'` → pattern = "fn main", path = "src/"
- `try_dispatch_subcommand` with multi-word arg: verify the quoting reconstruction
- Integration-style test: ensure `["yoyo", "grep", "fn main"]` produces correct `/grep "fn main"` input

Write a small shared tokenizer helper if the quoting logic is needed in multiple parsers. Keep it simple — just double-quote awareness, not full shell parsing.
