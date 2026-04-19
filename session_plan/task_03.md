Title: Add "did you mean?" fuzzy suggestions for unknown slash commands
Files: src/commands.rs, src/repl.rs
Issue: none (self-driven UX improvement, relates to #214 discoverability)

## Problem

With 68 commands, typos are inevitable. Currently, typing `/hlep` gives:
```
  unknown command: /hlep
  type /help for available commands
```

No suggestion of what the user probably meant. The user has to open /help, scan 68 commands,
and find the right one. Adding "did you mean /help?" would save time and make the tool
feel polished.

## What to do

### In `src/commands.rs`:

Add a function `suggest_command(input: &str) -> Option<&'static str>` that:

1. Takes the unknown command string (e.g., "/hlep")
2. Computes edit distance (Levenshtein) against all entries in `KNOWN_COMMANDS`
3. Returns the closest match if the edit distance is ≤ 2 (for short commands ≤5 chars)
   or ≤ 3 (for longer commands)
4. Returns `None` if no close match exists

Implement a simple Levenshtein distance function inline (it's ~15 lines, no external dep needed):
```rust
fn edit_distance(a: &str, b: &str) -> usize {
    let a: Vec<char> = a.chars().collect();
    let b: Vec<char> = b.chars().collect();
    let mut dp = vec![vec![0usize; b.len() + 1]; a.len() + 1];
    for i in 0..=a.len() { dp[i][0] = i; }
    for j in 0..=b.len() { dp[0][j] = j; }
    for i in 1..=a.len() {
        for j in 1..=b.len() {
            let cost = if a[i-1] == b[j-1] { 0 } else { 1 };
            dp[i][j] = (dp[i-1][j] + 1)
                .min(dp[i][j-1] + 1)
                .min(dp[i-1][j-1] + cost);
        }
    }
    dp[a.len()][b.len()]
}
```

Also handle prefix matches: if the input is a prefix of exactly one command, suggest that
command (e.g., `/comp` → "did you mean /compact?").

Add tests:
- `/hlep` → suggests `/help`
- `/comit` → suggests `/commit`
- `/savee` → suggests `/save`
- `/zzzzz` → returns None (too far from anything)
- `/comp` → suggests `/compact` (prefix match)
- `/model` → returns None (it's a valid command, not unknown)

### In `src/repl.rs`:

In the unknown command handler (around line 943), after printing "unknown command",
call `suggest_command` and if it returns a suggestion, print:
```
  did you mean {suggestion}?
```
in YELLOW color, before the "type /help" line.

## Verification

- `cargo build && cargo test`
- `cargo test suggest_command` for the new unit tests
- `cargo test unknown` to verify existing unknown command tests still pass
