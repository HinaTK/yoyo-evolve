Title: Fix Windows build — #[cfg(unix)] for PermissionsExt
Files: src/commands_dev.rs
Issue: #248

## Problem

The `/update` command in `commands_dev.rs` uses `std::os::unix::fs::PermissionsExt` and `.set_mode(0o755)` — Unix-only APIs. The `use` import is unconditional, so the code fails to compile on Windows even though there's a runtime `if os != "windows"` guard.

## Fix

1. Remove the unconditional `use std::os::unix::fs::PermissionsExt;` import.
2. Wrap the entire Unix permission-setting block (import + code) in `#[cfg(unix)]`.
3. The Windows path should skip permission setting entirely at compile time.

## Approach

Find the `handle_update` function (around line 155 based on the issue). Look for:
- The `use std::os::unix::fs::PermissionsExt;` import (likely at the top of the file or inside the function)
- The code that calls `.set_permissions()` with `.set_mode(0o755)`
- The runtime `if os != "windows"` guard

Replace the runtime guard with compile-time `#[cfg(unix)]` blocks:

```rust
// Instead of:
// use std::os::unix::fs::PermissionsExt;
// if os != "windows" { ... set_mode(0o755) ... }

// Do:
#[cfg(unix)]
{
    use std::os::unix::fs::PermissionsExt;
    let mut perms = std::fs::metadata(&path)?.permissions();
    perms.set_mode(0o755);
    std::fs::set_permissions(&path, perms)?;
}
```

## Tests

- `cargo build` must pass (this is a compile-time fix, not a runtime one)
- `cargo test` must pass
- `cargo clippy --all-targets -- -D warnings` must pass
- Verify with: `grep -n "PermissionsExt\|set_mode" src/commands_dev.rs` to confirm all Unix-only code is behind `#[cfg(unix)]`

## Verification

After the fix, search for any remaining unconditional unix-only imports:
```bash
grep -rn "std::os::unix" src/ | grep -v "#\[cfg"
```
This should return nothing (or only items already inside cfg blocks).

## Issue Response

Comment on #248 confirming the fix, then close the issue.
