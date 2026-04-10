Title: Extract parse_numeric_flag helper from parse_args
Files: src/cli.rs
Issue: #261

## Problem

`parse_args` is 467 lines. Four blocks follow an identical pattern for parsing numeric CLI flags with config file fallback: `--max-tokens` (u32), `--max-turns` (usize), `--temperature` (f32), and `--context-window` (u32). Each block is ~15 lines doing the same thing: find flag position → get next arg → parse → warn on failure → fall back to config file.

## Solution

Extract a generic `parse_numeric_flag<T: FromStr + Display>` helper that:
1. Takes `args: &[String]`, `flag_name: &str`, `file_config: &HashMap<String, String>`, `config_key: &str`
2. Checks args for the flag, parses the value as T
3. Falls back to the config file value
4. Prints a warning on parse failure
5. Returns `Option<T>`

Then replace the four inline blocks in `parse_args` with calls to this helper.

### Concrete steps:

1. **Add helper function** above `parse_args`:
   ```rust
   fn parse_numeric_flag<T: std::str::FromStr + std::fmt::Display>(
       args: &[String],
       flag_name: &str,
       file_config: &std::collections::HashMap<String, String>,
       config_key: &str,
   ) -> Option<T> {
       args.iter()
           .position(|a| a == flag_name)
           .and_then(|i| args.get(i + 1))
           .and_then(|s| {
               s.parse::<T>().ok().or_else(|| {
                   eprintln!(
                       "{YELLOW}warning:{RESET} Invalid {flag_name} value '{s}', using default"
                   );
                   None
               })
           })
           .or_else(|| {
               file_config
                   .get(config_key)
                   .and_then(|s| s.parse::<T>().ok())
           })
   }
   ```

2. **Replace the four blocks** in `parse_args`:
   - `max_tokens` → `parse_numeric_flag::<u32>(args, "--max-tokens", &file_config, "max_tokens")`
   - `max_turns` → `parse_numeric_flag::<usize>(args, "--max-turns", &file_config, "max_turns")`
   - `context_window` → `parse_numeric_flag::<u32>(args, "--context-window", &file_config, "context_window")`
   - `temperature` → `parse_numeric_flag::<f32>(args, "--temperature", &file_config, "temperature").map(clamp_temperature)`

   Each replacement saves ~12 lines.

3. **Tests**: Add unit tests for `parse_numeric_flag`:
   - Parses valid value from args
   - Returns None for missing flag
   - Falls back to config value when CLI not present
   - Warns on invalid value and returns None (falls through to config)
   - Config file fallback also returns None on invalid config value

4. **Verify**: `cargo build && cargo test` — all existing CLI tests must still pass.

## Expected reduction

~48 lines removed from `parse_args`, replaced with 4 one-liners. Net reduction of ~44 lines inside parse_args, plus ~20 lines of helper + ~30 lines of tests.

## What NOT to do

- Don't try to extract more than this one pattern — keep the PR small
- Don't change the warning messages (they should stay the same or very similar)
- Don't touch any other file
