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
use crate::git::{colorize_diff, run_git};
use crate::prompt::{build_retry_prompt, format_changes, run_prompt, ChangeKind, SessionChanges};

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

// ── exit summary ─────────────────────────────────────────────────────────

/// Returns a compact one-line summary of session changes for display on REPL
/// exit, or `None` if no files were modified during the session.
///
/// Example output: `"Session: 3 files changed"`
pub fn format_exit_summary(changes: &SessionChanges) -> Option<String> {
    let snapshot = changes.snapshot();
    if snapshot.is_empty() {
        return None;
    }
    let n = snapshot.len();
    let edits = snapshot
        .iter()
        .filter(|c| c.kind == ChangeKind::Edit)
        .count();
    let writes = snapshot
        .iter()
        .filter(|c| c.kind == ChangeKind::Write)
        .count();

    let mut parts = Vec::new();
    if writes > 0 {
        parts.push(format!("{writes} written"));
    }
    if edits > 0 {
        parts.push(format!("{edits} edited"));
    }

    Some(format!(
        "Session: {} {} changed ({})",
        n,
        pluralize(n, "file", "files"),
        parts.join(", "),
    ))
}

// ── /changes ─────────────────────────────────────────────────────────────

/// Returns `true` if the raw `/changes` input contains the `--diff` flag.
fn wants_diff(input: &str) -> bool {
    input
        .split_whitespace()
        .skip(1) // skip "/changes" itself
        .any(|arg| arg == "--diff")
}

/// Collect colorized git diffs for the given file paths.
///
/// For each file we try both unstaged (`git diff`) and staged
/// (`git diff --cached`) so we catch changes regardless of staging state.
fn collect_diffs(paths: &[String]) -> String {
    let mut out = String::new();
    for path in paths {
        // Try unstaged diff first, then staged
        let unstaged = run_git(&["diff", "--", path]).unwrap_or_default();
        let staged = run_git(&["diff", "--cached", "--", path]).unwrap_or_default();

        let combined = match (unstaged.is_empty(), staged.is_empty()) {
            (false, false) => format!("{unstaged}\n{staged}"),
            (false, true) => unstaged,
            (true, false) => staged,
            (true, true) => String::new(),
        };

        if combined.is_empty() {
            out.push_str(&format!("    {DIM}({path}: no diff available){RESET}\n"));
        } else {
            out.push_str(&colorize_diff(&combined));
            out.push('\n');
        }
    }
    out
}

pub fn handle_changes(changes: &SessionChanges, input: &str) {
    let output = format_changes(changes);
    if output.is_empty() {
        println!("{DIM}  No files modified yet this session.");
        println!(
            "  Files touched by write_file or edit_file tool calls will appear here.{RESET}\n"
        );
        return;
    }

    println!("{DIM}{output}{RESET}");

    if wants_diff(input) {
        let snapshot = changes.snapshot();
        let paths: Vec<String> = snapshot.iter().map(|c| c.path.clone()).collect();
        let diffs = collect_diffs(&paths);
        if !diffs.is_empty() {
            println!("{diffs}");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_handle_changes_empty_does_not_panic() {
        let changes = SessionChanges::new();
        // Should not panic — just prints a message
        handle_changes(&changes, "/changes");
    }

    #[test]
    fn test_handle_changes_with_entries_does_not_panic() {
        let changes = SessionChanges::new();
        changes.record("src/main.rs", ChangeKind::Write);
        changes.record("src/cli.rs", ChangeKind::Edit);
        // Should not panic
        handle_changes(&changes, "/changes");
    }

    #[test]
    fn test_handle_changes_diff_flag_does_not_panic() {
        let changes = SessionChanges::new();
        // Empty session with --diff should not panic
        handle_changes(&changes, "/changes --diff");
    }

    #[test]
    fn test_handle_changes_diff_flag_with_entries_does_not_panic() {
        let changes = SessionChanges::new();
        changes.record("src/main.rs", ChangeKind::Write);
        // With files and --diff — may not produce real diffs in test env, but shouldn't panic
        handle_changes(&changes, "/changes --diff");
    }

    #[test]
    fn test_wants_diff_flag_parsing() {
        assert!(!wants_diff("/changes"));
        assert!(wants_diff("/changes --diff"));
        assert!(wants_diff("/changes   --diff"));
        assert!(!wants_diff("/changes --dif"));
        assert!(!wants_diff("/changes --verbose"));
    }

    #[test]
    fn test_format_exit_summary_empty_returns_none() {
        let changes = SessionChanges::new();
        assert_eq!(format_exit_summary(&changes), None);
    }

    #[test]
    fn test_format_exit_summary_single_write() {
        let changes = SessionChanges::new();
        changes.record("src/main.rs", ChangeKind::Write);
        let summary = format_exit_summary(&changes).unwrap();
        assert_eq!(summary, "Session: 1 file changed (1 written)");
    }

    #[test]
    fn test_format_exit_summary_single_edit() {
        let changes = SessionChanges::new();
        changes.record("src/cli.rs", ChangeKind::Edit);
        let summary = format_exit_summary(&changes).unwrap();
        assert_eq!(summary, "Session: 1 file changed (1 edited)");
    }

    #[test]
    fn test_format_exit_summary_mixed() {
        let changes = SessionChanges::new();
        changes.record("src/main.rs", ChangeKind::Write);
        changes.record("src/cli.rs", ChangeKind::Edit);
        changes.record("src/tools.rs", ChangeKind::Edit);
        let summary = format_exit_summary(&changes).unwrap();
        assert_eq!(summary, "Session: 3 files changed (1 written, 2 edited)");
    }

    #[test]
    fn test_format_exit_summary_all_writes() {
        let changes = SessionChanges::new();
        changes.record("a.rs", ChangeKind::Write);
        changes.record("b.rs", ChangeKind::Write);
        let summary = format_exit_summary(&changes).unwrap();
        assert_eq!(summary, "Session: 2 files changed (2 written)");
    }

    // ── Tests moved from commands.rs — /changes command tests ────────

    #[test]
    fn test_changes_command_recognized() {
        use crate::commands::{is_unknown_command, KNOWN_COMMANDS};
        assert!(!is_unknown_command("/changes"));
        assert!(
            KNOWN_COMMANDS.contains(&"/changes"),
            "/changes should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_changes_command_not_confused_with_other_commands() {
        use crate::commands::is_unknown_command;
        // /changes should match exactly, unrelated words should be unknown
        assert!(is_unknown_command("/changed"));
        // /changelog is now a valid command (Issue #226)
        assert!(!is_unknown_command("/changelog"));
    }
}
