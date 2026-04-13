Title: Add /evolution command to view evolution session history
Files: src/commands_info.rs, src/commands.rs
Issue: #226

## What

Add a `/evolution` command that displays yoyo's evolution history by reading the journal
file (`journals/JOURNAL.md`). This lets users (and the agent itself) see the timeline of
evolution sessions — what shipped, what bounced, what day it was — without leaving the REPL.

Issue #226 from @yuanhao asks for exactly this: "Are you aware that you have direct access
to your own evolution logs?" The community wants yoyo to be able to introspect on its own
history from within the agent.

## Why

This is a community request from a sponsor's co-contributor (@yuanhao filed #226, @Reithan
endorsed it). The journal already exists and is structured — every entry starts with
`## Day N — HH:MM — title`. Parsing and displaying it is straightforward.

## How

1. In `src/commands_info.rs`, add `pub fn handle_evolution(input: &str)`:
   - Read `journals/JOURNAL.md` (use `std::fs::read_to_string`, fall back to "No journal found")
   - Parse entries by splitting on lines matching `^## Day \d+` regex
   - Default: show last 5 entries (titles + first paragraph only)
   - `/evolution all` — show all entry titles with day numbers
   - `/evolution N` — show the last N entries in full
   - `/evolution day N` — show entries from a specific day
   - Format with colors: day number in cyan, time in dim, title in bold

2. In `src/commands.rs`:
   - Add `"/evolution"` to `KNOWN_COMMANDS`
   - Add completion entry in `command_arg_completions` with subcommands: `"all"`, `"day"`

3. Add tests in `commands_info.rs`:
   - `test_parse_journal_entries` — parse a sample journal string, verify entry extraction
   - `test_evolution_day_filter` — filter entries by day number
   - `test_evolution_count_limit` — verify last-N limiting works

4. The REPL routing (`src/repl.rs`) will need a match arm — but since `commands_info.rs`
   already has public handlers called from repl.rs, just follow the same pattern. However,
   to stay within the 3-file limit, only modify `commands_info.rs` and `commands.rs`.
   The repl.rs routing can be added as a follow-up or the implementation agent can add it
   if they judge it fits within scope. If repl.rs must be touched, drop the `commands.rs`
   completion entry (it's nice-to-have) and touch repl.rs instead.

Do NOT modify more than 3 files total.
