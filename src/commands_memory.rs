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
