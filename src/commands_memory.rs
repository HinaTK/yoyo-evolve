//! `/remember`, `/memories`, and `/forget` REPL command handlers.
//!
//! Extracted from `commands.rs` as another slice of issue #260, which tracks
//! splitting the multi-thousand-line `commands.rs` into focused modules.
//! These three handlers form a coherent unit — they all operate on
//! `memory::ProjectMemory` through helpers already living in `src/memory.rs`,
//! so the move is purely mechanical and carries no behavioral risk.

use crate::format::*;
use crate::memory::{add_memory, load_memories, remove_memory, save_memories};

// ── /remember ────────────────────────────────────────────────────────────

pub fn handle_remember(input: &str) {
    let note = input
        .strip_prefix("/remember")
        .unwrap_or("")
        .trim()
        .to_string();
    if note.is_empty() {
        println!("{DIM}  usage: /remember <note>");
        println!("  Save a project-specific memory that persists across sessions.");
        println!("  Examples:");
        println!("    /remember this project uses sqlx for database access");
        println!("    /remember tests require docker running");
        println!("    /remember always run cargo fmt before committing{RESET}\n");
        return;
    }
    let mut memory = load_memories();
    add_memory(&mut memory, &note);
    match save_memories(&memory) {
        Ok(_) => {
            println!(
                "{GREEN}  ✓ Remembered: \"{note}\" ({} total memories){RESET}\n",
                memory.entries.len()
            );
        }
        Err(e) => {
            eprintln!("{RED}  error saving memory: {e}{RESET}\n");
        }
    }
}

// ── /memories ────────────────────────────────────────────────────────────

pub fn handle_memories() {
    let memory = load_memories();
    if memory.entries.is_empty() {
        println!("{DIM}  No project memories yet.");
        println!("  Use /remember <note> to add one.{RESET}\n");
        return;
    }
    println!("{DIM}  Project memories ({}):", memory.entries.len());
    for (i, entry) in memory.entries.iter().enumerate() {
        println!("    [{i}] {} ({})", entry.note, entry.timestamp);
    }
    println!("  Use /forget <n> to remove a memory.{RESET}\n");
}

// ── /forget ──────────────────────────────────────────────────────────────

pub fn handle_forget(input: &str) {
    let arg = input.strip_prefix("/forget").unwrap_or("").trim();
    if arg.is_empty() {
        println!("{DIM}  usage: /forget <n>");
        println!("  Remove a project memory by index. Use /memories to see indexes.{RESET}\n");
        return;
    }
    let index = match arg.parse::<usize>() {
        Ok(i) => i,
        Err(_) => {
            eprintln!("{RED}  error: '{arg}' is not a valid index. Use /memories to see indexes.{RESET}\n");
            return;
        }
    };
    let mut memory = load_memories();
    match remove_memory(&mut memory, index) {
        Some(removed) => match save_memories(&memory) {
            Ok(_) => {
                println!(
                    "{GREEN}  ✓ Forgot: \"{}\" ({} memories remaining){RESET}\n",
                    removed.note,
                    memory.entries.len()
                );
            }
            Err(e) => {
                eprintln!("{RED}  error saving memory: {e}{RESET}\n");
            }
        },
        None => {
            eprintln!(
                "{RED}  error: index {index} out of range (have {} memories). Use /memories to see indexes.{RESET}\n",
                memory.entries.len()
            );
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::commands::{is_unknown_command, KNOWN_COMMANDS};
    use crate::memory::{
        add_memory, format_memories_for_prompt, load_memories_from, remove_memory, MemoryEntry,
        ProjectMemory,
    };

    #[test]
    fn test_remember_command_recognized() {
        assert!(!is_unknown_command("/remember"));
        assert!(!is_unknown_command("/remember this uses sqlx"));
        assert!(
            KNOWN_COMMANDS.contains(&"/remember"),
            "/remember should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_memories_command_recognized() {
        assert!(!is_unknown_command("/memories"));
        assert!(
            KNOWN_COMMANDS.contains(&"/memories"),
            "/memories should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_forget_command_recognized() {
        assert!(!is_unknown_command("/forget"));
        assert!(!is_unknown_command("/forget 0"));
        assert!(
            KNOWN_COMMANDS.contains(&"/forget"),
            "/forget should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_remember_command_matching() {
        let remember_matches = |s: &str| s == "/remember" || s.starts_with("/remember ");
        assert!(remember_matches("/remember"));
        assert!(remember_matches("/remember this uses sqlx"));
        assert!(!remember_matches("/remembering"));
        assert!(!remember_matches("/remembrance"));
    }

    #[test]
    fn test_forget_command_matching() {
        let forget_matches = |s: &str| s == "/forget" || s.starts_with("/forget ");
        assert!(forget_matches("/forget"));
        assert!(forget_matches("/forget 0"));
        assert!(forget_matches("/forget 42"));
        assert!(!forget_matches("/forgetting"));
        assert!(!forget_matches("/forgetful"));
    }

    #[test]
    fn test_memory_crud_roundtrip() {
        use std::fs;
        let dir = std::env::temp_dir().join("yoyo_test_memory_cmd_crud");
        let _ = fs::remove_dir_all(&dir);
        let _ = fs::create_dir_all(&dir);
        let path = dir.join("memory.json");

        // Start empty
        let mut mem = load_memories_from(&path);
        assert!(mem.entries.is_empty());

        // Add
        add_memory(&mut mem, "uses sqlx");
        add_memory(&mut mem, "docker needed");
        assert_eq!(mem.entries.len(), 2);

        // Save & reload
        crate::memory::save_memories_to(&mem, &path).unwrap();
        let reloaded = load_memories_from(&path);
        assert_eq!(reloaded.entries.len(), 2);
        assert_eq!(reloaded.entries[0].note, "uses sqlx");

        // Remove
        let mut reloaded = reloaded;
        let removed = remove_memory(&mut reloaded, 0);
        assert_eq!(removed.unwrap().note, "uses sqlx");
        assert_eq!(reloaded.entries.len(), 1);
        assert_eq!(reloaded.entries[0].note, "docker needed");

        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn test_memory_format_for_prompt_integration() {
        let memory = ProjectMemory {
            entries: vec![MemoryEntry {
                note: "always run cargo fmt".to_string(),
                timestamp: "2026-03-15 08:00".to_string(),
            }],
        };
        let prompt = format_memories_for_prompt(&memory);
        assert!(prompt.is_some());
        let prompt = prompt.unwrap();
        assert!(prompt.contains("Project Memories"));
        assert!(prompt.contains("always run cargo fmt"));
    }
}
