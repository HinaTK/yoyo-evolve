Title: Add /web search subcommand for DuckDuckGo web search
Files: src/commands_file.rs
Issue: none

## Problem

The assessment identifies "No built-in web search" as a capability gap vs Claude Code.
Currently, yoyo can fetch known URLs via `/web <url>`, but cannot SEARCH the web.
The agent can use `curl` through bash, but doesn't have a convenient, structured way
to get search results.

Adding `/web search <query>` gives both the user and the agent a way to quickly look
things up without leaving the session.

## Approach

Use DuckDuckGo Lite (https://lite.duckduckgo.com/lite/) which is a text-only search
page that's stable and easy to parse. The flow:

1. User types `/web search how to use tokio spawn`
2. yoyo sends a POST to `https://lite.duckduckgo.com/lite/` with form data `q=<query>`
3. Parse the HTML response to extract result titles, URLs, and snippets
4. Display the top 5-8 results in a compact format

## Implementation

In `commands_file.rs`, modify `handle_web()` to detect the `search` subcommand:

```rust
pub fn handle_web(input: &str) {
    let rest = input.strip_prefix("/web").unwrap_or("").trim();
    
    // Check for /web search <query>
    if let Some(query) = rest.strip_prefix("search").map(|s| s.trim()) {
        if query.is_empty() {
            println!("{DIM}  Usage: /web search <query>{RESET}");
            return;
        }
        handle_web_search(query);
        return;
    }
    
    // ... existing URL fetch logic
}
```

Add the search function:

```rust
fn handle_web_search(query: &str) {
    println!("{DIM}  Searching: {query}...{RESET}");
    
    let output = std::process::Command::new("curl")
        .args([
            "-s", "-L",
            "--max-time", "10",
            "-X", "POST",
            "-d", &format!("q={}", urlencoded(query)),
            "-H", "Content-Type: application/x-www-form-urlencoded",
            "https://lite.duckduckgo.com/lite/"
        ])
        .output();
    
    match output {
        Ok(out) if out.status.success() => {
            let html = String::from_utf8_lossy(&out.stdout);
            let results = parse_ddg_results(&html);
            if results.is_empty() {
                println!("{DIM}  No results found.{RESET}");
            } else {
                for (i, (title, url, snippet)) in results.iter().enumerate().take(8) {
                    println!("  {BOLD}{}.{RESET} {title}", i + 1);
                    println!("     {CYAN}{url}{RESET}");
                    if !snippet.is_empty() {
                        println!("     {DIM}{snippet}{RESET}");
                    }
                    println!();
                }
                println!("{DIM}  Use /web <url> to read any result.{RESET}");
            }
        }
        _ => println!("{RED}  Search failed. Check your internet connection.{RESET}"),
    }
}
```

The HTML parser (`parse_ddg_results`) extracts results from DuckDuckGo Lite's simple HTML
structure. The results are in `<a>` tags within table rows. The parser should:
- Find links that point to external URLs (not ddg internal links)
- Extract the link text as the title
- Extract the snippet text from the surrounding table cell
- Return a Vec of (title, url, snippet) tuples

Also add a simple URL encoding helper for the query string (replace spaces with +,
encode special chars).

## Tests

Add tests for:
1. `parse_ddg_results()` with a sample HTML snippet (unit test, no network)
2. `urlencoded()` helper produces correct output
3. The `/web search` subcommand is recognized (doesn't fall through to URL fetch)

## Documentation

Update the help text for `/web` in `help.rs` to mention the search subcommand:
```
/web <url>              Fetch and display a web page
/web search <query>     Search the web via DuckDuckGo
```

Note: This touches help.rs for the description update, but the help text is a one-line
change and can be done inline. The main implementation is in commands_file.rs only.
