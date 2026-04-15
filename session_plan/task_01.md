Title: Add /memory search <query> command
Files: src/commands_memory.rs, src/memory.rs, src/help.rs
Issue: none

## What

Add a `/memory search <query>` command that searches across project memories by substring match (case-insensitive). This closes the #1 capability gap from the assessment: Claude Code has `/memory` with search; yoyo has `/remember` but no search.

## Implementation

### 1. Add search function to `src/memory.rs`

Add a `search_memories` function:
```rust
pub fn search_memories(memory: &ProjectMemory, query: &str) -> Vec<(usize, &MemoryEntry)> {
    let query_lower = query.to_lowercase();
    memory.entries.iter().enumerate()
        .filter(|(_, entry)| entry.note.to_lowercase().contains(&query_lower))
        .collect()
}
```

Add tests for `search_memories`:
- Empty query returns all
- Query matches subset
- Case-insensitive matching
- No matches returns empty vec

### 2. Add `/memory` command to `src/commands_memory.rs`

Add a `handle_memory` function that dispatches subcommands:
- `/memory search <query>` — calls `search_memories`, displays matching entries with indices
- `/memory` alone — shows usage help for memory subcommands

Display format: like `/memories` but only showing matches, with a header like "Found N memories matching 'query':"

Wire `/memory` into the REPL by adding it to the command dispatch in `src/repl.rs` (this is the 4th file, but it's a one-line addition — if the agent wants to minimize file count, they can add the dispatch for `/memory search` directly to the existing `/memories` handler by checking for a search argument).

Actually, simpler approach: make `/memories <query>` do the search. If `/memories` is called with an argument, treat it as a search query. If called without, show all. This avoids adding a new command and keeps changes to 2-3 files.

### 3. Update help text in `src/help.rs`

Update the `/memories` help entry to mention the search feature:
- `/memories` — list all memories
- `/memories <query>` — search memories

### Tests

- `test_search_memories_basic` — finds matching entries
- `test_search_memories_case_insensitive` — case doesn't matter
- `test_search_memories_no_match` — returns empty vec
- `test_search_memories_empty_query` — returns all entries
- `test_memories_command_with_search_arg` — command recognition

## Docs

Update `docs/src/usage/commands.md` if it lists `/memories` — add search mention.
