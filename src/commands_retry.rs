//! `/retry` and `/changes` REPL command handlers.
//!
//! Extracted from `commands.rs` as another slice of issue #260, which tracks
//! splitting the multi-thousand-line `commands.rs` into focused modules.
//! These two handlers are self-contained and only touch session state through
//! well-defined helpers (`build_retry_prompt`, `run_prompt`,
//! `auto_compact_if_needed`, `format_changes`), which makes them a safe,
//! mechanical slice to pull out.

use crate::commands_session::auto_compact_if_needed;
use crate::format::*;
use crate::prompt::{build_retry_prompt, format_changes, run_prompt, SessionChanges};

use yoagent::agent::Agent;
use yoagent::*;

// ── /retry ───────────────────────────────────────────────────────────────

pub async fn handle_retry(
    agent: &mut Agent,
    last_input: &Option<String>,
    last_error: &Option<String>,
    session_total: &mut Usage,
    model: &str,
) -> Option<String> {
    match last_input {
        Some(prev) => {
            let retry_input = build_retry_prompt(prev, last_error);
            if last_error.is_some() {
                println!("{DIM}  (retrying with error context){RESET}");
            } else {
                println!("{DIM}  (retrying last input){RESET}");
            }
            let outcome = run_prompt(agent, &retry_input, session_total, model).await;
            auto_compact_if_needed(agent);
            outcome.last_tool_error
        }
        None => {
            eprintln!("{DIM}  (nothing to retry — no previous input){RESET}\n");
            None
        }
    }
}

// ── /changes ─────────────────────────────────────────────────────────────

pub fn handle_changes(changes: &SessionChanges) {
    let output = format_changes(changes);
    if output.is_empty() {
        println!("{DIM}  No files modified yet this session.");
        println!(
            "  Files touched by write_file or edit_file tool calls will appear here.{RESET}\n"
        );
    } else {
        println!("{DIM}{output}{RESET}");
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::prompt::ChangeKind;

    #[test]
    fn test_handle_changes_empty_does_not_panic() {
        let changes = SessionChanges::new();
        // Should not panic — just prints a message
        handle_changes(&changes);
    }

    #[test]
    fn test_handle_changes_with_entries_does_not_panic() {
        let changes = SessionChanges::new();
        changes.record("src/main.rs", ChangeKind::Write);
        changes.record("src/cli.rs", ChangeKind::Edit);
        // Should not panic
        handle_changes(&changes);
    }
}
