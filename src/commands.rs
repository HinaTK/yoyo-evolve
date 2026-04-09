//! REPL command handlers for yoyo.
//!
//! Each `/command` in the interactive REPL is handled by a function in this module.
//! The main loop dispatches to these handlers, keeping main.rs as a thin REPL driver.

// All handle_* functions in this module are dispatched from the REPL in main.rs.

use crate::cli::{default_model_for_provider, KNOWN_PROVIDERS};
use crate::cli::{is_verbose, AUTO_COMPACT_THRESHOLD};
use crate::format::*;
use crate::git::*;

pub use crate::help::*;

// Re-export read-only "info" handlers extracted to commands_info.rs (issue #260).
// Explicit re-exports keep the public API of `commands` unchanged so REPL
// dispatch sites in main.rs / repl.rs don't need to know about the split.
pub use crate::commands_info::{
    handle_cost, handle_model_show, handle_provider_show, handle_status, handle_think_show,
    handle_tokens, handle_version,
};

// Re-export /retry and /changes handlers extracted to commands_retry.rs
// (issue #260 slice). Same stability contract as commands_info above.
pub use crate::commands_retry::{handle_changes, handle_retry};

// Re-export /remember, /memories, /forget handlers extracted to
// commands_memory.rs (issue #260 slice). Same stability contract as above.
pub use crate::commands_memory::{handle_forget, handle_memories, handle_remember};

use std::sync::atomic::{AtomicBool, Ordering};
use yoagent::agent::Agent;
use yoagent::*;

// ── Teach mode state ──────────────────────────────────────────────────────
// Session toggle: when enabled, a teaching instruction is prepended to
// each user message so the agent explains its reasoning as it works.

static TEACH_MODE: AtomicBool = AtomicBool::new(false);

/// Enable or disable teach mode.
pub fn set_teach_mode(enabled: bool) {
    TEACH_MODE.store(enabled, Ordering::Relaxed);
}

/// Check whether teach mode is currently active.
pub fn is_teach_mode() -> bool {
    TEACH_MODE.load(Ordering::Relaxed)
}

/// Instruction prepended to user messages when teach mode is on.
pub const TEACH_MODE_PROMPT: &str = "\
[TEACH MODE] You are in teach mode. For every change you make:
1. Explain WHY you're making the change before showing the code
2. Use clear, readable code patterns — prefer clarity over cleverness
3. Add brief comments on non-obvious lines
4. After completing a task, summarize what the user should learn from it
Keep explanations concise but educational.";

/// Known REPL command prefixes. Used to detect unknown slash commands
/// and for tab-completion in the REPL.
pub const KNOWN_COMMANDS: &[&str] = &[
    "/add",
    "/apply",
    "/help",
    "/quit",
    "/exit",
    "/clear",
    "/clear!",
    "/compact",
    "/commit",
    "/cost",
    "/doctor",
    "/docs",
    "/export",
    "/find",
    "/fix",
    "/forget",
    "/index",
    "/status",
    "/tokens",
    "/save",
    "/load",
    "/diff",
    "/undo",
    "/health",
    "/hooks",
    "/retry",
    "/history",
    "/search",
    "/model",
    "/think",
    "/config",
    "/context",
    "/init",
    "/version",
    "/run",
    "/tree",
    "/pr",
    "/git",
    "/grep",
    "/test",
    "/lint",
    "/spawn",
    "/update",
    "/review",
    "/mark",
    "/jump",
    "/marks",
    "/plan",
    "/remember",
    "/memories",
    "/provider",
    "/changes",
    "/web",
    "/rename",
    "/extract",
    "/move",
    "/refactor",
    "/watch",
    "/ast",
    "/map",
    "/stash",
    "/teach",
    "/todo",
    "/mcp",
    "/permissions",
];

/// Well-known model names for `/model <Tab>` completion.
pub const KNOWN_MODELS: &[&str] = &[
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
    "claude-haiku-35-20241022",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1",
    "gpt-4.1-mini",
    "o3",
    "o3-mini",
    "o4-mini",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "deepseek-chat",
    "deepseek-reasoner",
];

/// Thinking level names for `/think <Tab>` completion.
pub const THINKING_LEVELS: &[&str] = &["off", "minimal", "low", "medium", "high"];

/// Git subcommand names for `/git <Tab>` completion.
pub const GIT_SUBCOMMANDS: &[&str] = &["status", "log", "add", "diff", "branch", "stash"];

/// PR subcommand names for `/pr <Tab>` completion.
pub const PR_SUBCOMMANDS: &[&str] = &["list", "view", "diff", "comment", "create", "checkout"];

/// Undo option names for `/undo <Tab>` completion.
pub const UNDO_OPTIONS: &[&str] = &["--all"];

/// Refactor subcommand names for `/refactor <Tab>` completion.
pub const REFACTOR_SUBCOMMANDS: &[&str] = &["rename", "extract", "move"];

/// Diff flag names for `/diff <Tab>` completion.
pub const DIFF_FLAGS: &[&str] = &["--staged", "--cached", "--name-only"];

/// Return context-aware argument completions for a given command and partial argument.
///
/// `cmd` is the slash command (e.g. "/model"), `partial_arg` is what the user has typed
/// after the command + space so far. Returns a list of candidate completions.
pub fn command_arg_completions(cmd: &str, partial_arg: &str) -> Vec<String> {
    let partial_lower = partial_arg.to_lowercase();
    match cmd {
        "/model" => filter_candidates(KNOWN_MODELS, &partial_lower),
        "/think" => filter_candidates(THINKING_LEVELS, &partial_lower),
        "/git" => filter_candidates(GIT_SUBCOMMANDS, &partial_lower),
        "/diff" => filter_candidates(DIFF_FLAGS, &partial_lower),
        "/pr" => filter_candidates(PR_SUBCOMMANDS, &partial_lower),
        "/provider" => filter_candidates(KNOWN_PROVIDERS, &partial_lower),
        "/save" | "/load" => list_json_files(partial_arg),
        "/help" => help_command_completions(&partial_lower),
        "/undo" => filter_candidates(UNDO_OPTIONS, &partial_lower),
        "/refactor" => filter_candidates(REFACTOR_SUBCOMMANDS, &partial_lower),
        "/watch" => filter_candidates(crate::commands_dev::WATCH_SUBCOMMANDS, &partial_lower),
        "/ast" => filter_candidates(crate::commands_search::AST_GREP_FLAGS, &partial_lower),
        "/apply" => filter_candidates(crate::commands_file::APPLY_FLAGS, &partial_lower),
        "/context" => filter_candidates(
            crate::commands_project::context_subcommands(),
            &partial_lower,
        ),
        _ => Vec::new(),
    }
}

/// Filter a list of candidates by a lowercase prefix.
fn filter_candidates(candidates: &[&str], partial_lower: &str) -> Vec<String> {
    candidates
        .iter()
        .filter(|c| c.to_lowercase().starts_with(partial_lower))
        .map(|c| c.to_string())
        .collect()
}

/// List .json files in the current directory matching a partial prefix.
fn list_json_files(partial: &str) -> Vec<String> {
    let entries = match std::fs::read_dir(".") {
        Ok(entries) => entries,
        Err(_) => return Vec::new(),
    };
    let mut matches: Vec<String> = entries
        .flatten()
        .filter_map(|entry| {
            let name = entry.file_name().to_string_lossy().to_string();
            if name.ends_with(".json") && name.starts_with(partial) {
                Some(name)
            } else {
                None
            }
        })
        .collect();
    matches.sort();
    matches
}

/// Check if a slash-prefixed input is an unknown command.
/// Extracts the first word and checks against known commands.
pub fn is_unknown_command(input: &str) -> bool {
    let cmd = input.split_whitespace().next().unwrap_or(input);
    !KNOWN_COMMANDS.contains(&cmd)
}

/// Format a ThinkingLevel as a display string.
pub fn thinking_level_name(level: ThinkingLevel) -> &'static str {
    match level {
        ThinkingLevel::Off => "off",
        ThinkingLevel::Minimal => "minimal",
        ThinkingLevel::Low => "low",
        ThinkingLevel::Medium => "medium",
        ThinkingLevel::High => "high",
    }
}
// ── /version ─────────────────────────────────────────────────────────────

// ── /retry ───────────────────────────────────────────────────────────────
// Moved to commands_retry.rs (issue #260 slice). Re-exported below so
// `commands::handle_retry` still resolves from repl.rs without churn.

// ── /model ───────────────────────────────────────────────────────────────

pub fn handle_provider_switch(
    new_provider: &str,
    agent_config: &mut crate::AgentConfig,
    agent: &mut Agent,
) {
    if !KNOWN_PROVIDERS.contains(&new_provider) {
        eprintln!("{RED}  unknown provider: '{new_provider}'{RESET}");
        eprintln!("{DIM}  available: {}{RESET}\n", KNOWN_PROVIDERS.join(", "));
        return;
    }
    agent_config.provider = new_provider.to_string();
    agent_config.model = default_model_for_provider(new_provider);
    let saved = agent.save_messages().ok();
    *agent = agent_config.build_agent();
    let restored = if let Some(json) = saved {
        agent.restore_messages(&json).is_ok()
    } else {
        false
    };
    if restored {
        println!(
            "{DIM}  (switched to provider '{}', model '{}', conversation preserved){RESET}\n",
            agent_config.provider, agent_config.model
        );
    } else {
        println!(
            "{YELLOW}  (switched to provider '{}', model '{}', conversation could not be preserved){RESET}\n",
            agent_config.provider, agent_config.model
        );
    }
}

// ── /think ───────────────────────────────────────────────────────────────

// ── /config ──────────────────────────────────────────────────────────────

#[allow(clippy::too_many_arguments)]
pub fn handle_config(
    provider: &str,
    model: &str,
    base_url: &Option<String>,
    thinking: ThinkingLevel,
    max_tokens: Option<u32>,
    max_turns: Option<usize>,
    temperature: Option<f32>,
    skills: &yoagent::skills::SkillSet,
    system_prompt: &str,
    mcp_count: u32,
    openapi_count: u32,
    hook_count: usize,
    agent: &Agent,
    cwd: &str,
) {
    println!("{DIM}  Configuration:");
    println!("    provider:   {provider}");
    println!("    model:      {model}");
    if let Some(ref url) = base_url {
        println!("    base_url:   {url}");
    }
    println!("    thinking:   {}", thinking_level_name(thinking));
    println!(
        "    max_tokens: {}",
        max_tokens
            .map(|m| m.to_string())
            .unwrap_or_else(|| "default (8192)".to_string())
    );
    println!(
        "    max_turns:  {}",
        max_turns
            .map(|m| m.to_string())
            .unwrap_or_else(|| "default (200)".to_string())
    );
    println!(
        "    temperature: {}",
        temperature
            .map(|t| format!("{t:.1}"))
            .unwrap_or_else(|| "default".to_string())
    );
    println!(
        "    skills:     {}",
        if skills.is_empty() {
            "none".to_string()
        } else {
            format!("{} loaded", skills.len())
        }
    );
    let system_preview =
        truncate_with_ellipsis(system_prompt.lines().next().unwrap_or("(empty)"), 60);
    println!("    system:     {system_preview}");
    if mcp_count > 0 {
        println!("    mcp:        {mcp_count} server(s)");
    }
    if openapi_count > 0 {
        println!("    openapi:    {openapi_count} spec(s)");
    }
    if hook_count > 0 {
        println!("    hooks:      {hook_count} active");
    }
    println!(
        "    verbose:    {}",
        if is_verbose() { "on" } else { "off" }
    );
    if let Some(branch) = git_branch() {
        println!("    git:        {branch}");
    }
    println!("    cwd:        {cwd}");
    println!(
        "    context:    {} max tokens",
        format_token_count(crate::cli::effective_context_tokens())
    );
    println!(
        "    auto-compact: at {:.0}%",
        AUTO_COMPACT_THRESHOLD * 100.0
    );
    println!("    messages:   {}", agent.messages().len());
    println!(
        "    session:    auto-save on exit ({})",
        crate::cli::AUTO_SAVE_SESSION_PATH
    );
    println!("{RESET}");
}

// ── /config show ─────────────────────────────────────────────────────────
//
// `/config show` is the runtime config-introspection surface (Day 40,
// Crush-parity work). Unlike `/config` which shows the *agent's live
// runtime state* (model, thinking level, message count, etc.),
// `/config show` answers a different question: "what did my config
// file actually contribute to this session, and which file was it?"
//
// The split matters for debugging: when a user says "why isn't my
// override being picked up?", they need to see (a) which file was
// read and (b) the merged key=value pairs that came out of it —
// not a snapshot of in-memory runtime values that might have been
// further mutated by CLI flags, env vars, or interactive /model
// switches. Keeping the two handlers separate means `/config` stays
// a runtime mirror and `/config show` stays a file-introspection
// tool. They're complementary, not redundant.

/// Detect which on-disk config file (if any) would be loaded by
/// `cli::load_config_file()`, using the same precedence order:
/// 1. `./.yoyo.toml` (project-level)
/// 2. `~/.yoyo.toml` (home shorthand)
/// 3. `~/.config/yoyo/config.toml` (XDG user-level)
///
/// Returns the path to the first file that exists, or `None` if no
/// config file is present in any location. This is a read-only
/// introspection helper — it never reads or parses the file itself,
/// it just tells you which path would be chosen.
///
/// Kept as a separate function (rather than calling `load_config_file`
/// directly) because the existing loader is private to `cli.rs` and
/// this path-only view is all `/config show` needs. The loader path
/// and this one are unit-tested together indirectly via
/// `test_config_file_path_precedence` below.
fn detect_loaded_config_path() -> Option<std::path::PathBuf> {
    // Project-level: ./.yoyo.toml
    let project = std::path::PathBuf::from(".yoyo.toml");
    if project.exists() {
        return Some(project);
    }
    // Home shorthand: ~/.yoyo.toml
    if let Some(path) = crate::cli::home_config_path() {
        if path.exists() {
            return Some(path);
        }
    }
    // XDG user-level: ~/.config/yoyo/config.toml
    if let Some(path) = crate::cli::user_config_path() {
        if path.exists() {
            return Some(path);
        }
    }
    None
}

/// Return `true` if a config key looks like a secret and its value
/// should be masked in any user-visible output. Matches are
/// case-insensitive substring checks against `key`, `token`, `secret`,
/// and `password`. Keep this list in sync with anything that gets
/// stored in `.yoyo.toml` as a sensitive value (e.g. API keys).
fn is_secret_key(key: &str) -> bool {
    let lower = key.to_ascii_lowercase();
    lower.contains("key")
        || lower.contains("token")
        || lower.contains("secret")
        || lower.contains("password")
}

/// Pure, testable formatter for `/config show` output. Takes the
/// already-loaded config HashMap and an optional path to the file
/// it came from, and returns a stable, human-readable block.
///
/// Secrets (keys matching `is_secret_key`) are always masked with
/// `***` — the raw value must never appear in the output, even in
/// debug builds. This is the whole point of the test below.
///
/// Keys are emitted in sorted order so the output is deterministic
/// and easy to diff across sessions. An empty HashMap with no path
/// is the "no config loaded, running on defaults" case and produces
/// a friendly one-liner rather than an empty block.
pub fn format_config_output(
    config: &std::collections::HashMap<String, String>,
    path: Option<&std::path::Path>,
) -> String {
    let mut out = String::new();
    match path {
        Some(p) => {
            out.push_str(&format!("Loaded config: {}\n", p.display()));
        }
        None => {
            out.push_str("No config file loaded — using defaults.\n");
            // Still dump whatever was passed in (for completeness),
            // but if the map is also empty we're done.
            if config.is_empty() {
                return out;
            }
        }
    }

    if config.is_empty() {
        // A path was given but the map is empty — file parsed to
        // nothing (all comments / whitespace). Note it explicitly so
        // the user knows the file was read but contributed nothing.
        out.push_str("\n  (no keys parsed from this file)\n");
        return out;
    }

    // Determine column width for pretty alignment. Cap it so a single
    // pathological key doesn't throw off everything else.
    let max_key_len = config.keys().map(|k| k.len()).max().unwrap_or(0).min(24);

    let mut keys: Vec<&String> = config.keys().collect();
    keys.sort();

    out.push('\n');
    for key in keys {
        let value = config.get(key).map(String::as_str).unwrap_or("");
        let display_value = if is_secret_key(key) {
            "***".to_string()
        } else {
            value.to_string()
        };
        out.push_str(&format!(
            "  {:<width$}  = {}\n",
            key,
            display_value,
            width = max_key_len
        ));
    }
    out
}

/// Handler for `/config show`: prints which config file was loaded
/// (if any) and the merged key-value pairs it contributed.
///
/// This is the user-facing surface; all formatting logic lives in
/// `format_config_output` so it can be unit-tested without touching
/// the filesystem. This handler's only jobs are (1) detect the path,
/// (2) read+parse the file via the existing `cli::parse_config_file`
/// helper, and (3) println the result inside the dim block the rest
/// of the `/config` family uses.
pub fn handle_config_show() {
    let path = detect_loaded_config_path();
    let config = match path.as_ref() {
        Some(p) => match std::fs::read_to_string(p) {
            Ok(content) => crate::cli::parse_config_file(&content),
            Err(e) => {
                println!(
                    "{RED}  Failed to read config file {}: {e}{RESET}",
                    p.display()
                );
                return;
            }
        },
        None => std::collections::HashMap::new(),
    };
    let output = format_config_output(&config, path.as_deref());
    print!("{DIM}{output}{RESET}");
}

// ── /hooks ───────────────────────────────────────────────────────────────

pub fn handle_hooks(hooks: &[crate::hooks::ShellHook]) {
    if hooks.is_empty() {
        println!("{DIM}  No hooks configured.");
        println!();
        println!("  Add hooks to .yoyo.toml:");
        println!();
        println!("    # Pre-hook: runs before every bash tool call");
        println!("    hooks.pre.bash = \"echo 'About to run bash'\"");
        println!();
        println!("    # Post-hook: runs after every tool call (wildcard)");
        println!("    hooks.post.* = \"echo 'Tool finished'\"");
        println!();
        println!("  Pre-hooks that exit non-zero block the tool.");
        println!("  Post-hooks always pass through the tool output.");
        println!("  All hooks have a 5-second timeout.{RESET}");
        return;
    }

    println!("{DIM}  Active hooks ({}):", hooks.len());
    println!();
    for hook in hooks {
        let phase = match hook.phase {
            crate::hooks::HookPhase::Pre => "pre",
            crate::hooks::HookPhase::Post => "post",
        };
        println!(
            "    {BOLD}{}{RESET}{DIM}  ({}, pattern: {})",
            hook.name, phase, hook.tool_pattern
        );
        println!("      command: {}", hook.command);
    }
    println!("{RESET}");
}

// ── /permissions ─────────────────────────────────────────────────────────

pub fn handle_permissions(
    auto_approve: bool,
    permissions: &crate::cli::PermissionConfig,
    dir_restrictions: &crate::cli::DirectoryRestrictions,
) {
    println!("{DIM}  Security Configuration:\n");

    // Auto-approve status
    if auto_approve {
        println!("    {YELLOW}⚠ Auto-approve: ON{RESET}{DIM} (--yes flag active)");
        println!("      All tool operations run without confirmation{RESET}");
    } else {
        println!("    {GREEN}✓ Confirmation: required{RESET}");
        println!("    {DIM}  Tools will prompt before write/edit/bash operations{RESET}");
    }
    println!();

    // Bash command permissions
    if permissions.is_empty() {
        println!("    Command patterns: none configured");
    } else {
        if !permissions.allow.is_empty() {
            println!("    {GREEN}Allow patterns:{RESET}");
            for pat in &permissions.allow {
                println!("      {GREEN}✓{RESET} {pat}");
            }
        }
        if !permissions.deny.is_empty() {
            println!("    {RED}Deny patterns:{RESET}");
            for pat in &permissions.deny {
                println!("      {RED}✗{RESET} {pat}");
            }
        }
    }
    println!();

    // Directory restrictions
    if dir_restrictions.is_empty() {
        println!("    Directory restrictions: none (full filesystem access)");
    } else {
        if !dir_restrictions.allow.is_empty() {
            println!("    {GREEN}Allowed directories:{RESET}");
            for dir in &dir_restrictions.allow {
                println!("      {GREEN}✓{RESET} {dir}");
            }
        }
        if !dir_restrictions.deny.is_empty() {
            println!("    {RED}Denied directories:{RESET}");
            for dir in &dir_restrictions.deny {
                println!("      {RED}✗{RESET} {dir}");
            }
        }
    }
    println!();

    // Quick reference
    println!(
        "    {DIM}Configure with: --allow <pat>, --deny <pat>, --allow-dir <d>, --deny-dir <d>"
    );
    println!("    Or in .yoyo.toml: allow = [...], deny = [...]{RESET}\n");
}

// ── /changes ─────────────────────────────────────────────────────────────
// Moved to commands_retry.rs (issue #260 slice). Re-exported below so
// `commands::handle_changes` still resolves from repl.rs without churn.

// ── Re-exports from submodules ────────────────────────────────────────────
// These re-exports keep the public API stable so repl.rs continues to work
// with `commands::handle_*` calls unchanged.

// Git-related handlers
pub use crate::commands_git::{
    handle_commit, handle_diff, handle_git, handle_pr, handle_review, handle_undo,
};

// Project-related handlers
pub use crate::commands_project::{
    handle_context, handle_docs, handle_extract, handle_init, handle_move, handle_plan,
    handle_refactor, handle_rename, handle_todo,
};

pub use crate::commands_search::{
    handle_ast_grep, handle_find, handle_grep, handle_index, handle_map,
};

pub use crate::commands_dev::{
    handle_doctor, handle_fix, handle_health, handle_lint, handle_run, handle_run_usage,
    handle_test, handle_tree, handle_update, handle_watch,
};

pub use crate::commands_file::{
    expand_file_mentions, handle_add, handle_apply, handle_web, AddResult,
};

// Session-related handlers
pub use crate::commands_session::{
    auto_compact_if_needed, auto_save_on_exit, clear_confirmation_message, handle_compact,
    handle_export, handle_history, handle_jump, handle_load, handle_mark, handle_marks,
    handle_save, handle_search, handle_spawn, handle_stash, last_session_exists,
    reset_compact_thrash, Bookmarks, SpawnTracker,
};

// Memory-related handlers live in commands_memory.rs (#260 slice).
// The memory-module helpers they use (add_memory, load_memories,
// remove_memory, save_memories) are imported directly from crate::memory
// in that file and in the test module below — no module-level re-export
// is needed here since nothing in commands.rs itself calls them anymore.

/// Toggle teach mode on/off. When active, yoyo explains its reasoning as it works.
pub fn handle_teach(input: &str) {
    let arg = input.strip_prefix("/teach").unwrap_or("").trim();
    match arg {
        "on" => {
            set_teach_mode(true);
            println!("{GREEN}  🎓 Teach mode enabled — yoyo will explain its reasoning as it works{RESET}\n");
        }
        "off" => {
            set_teach_mode(false);
            println!("{DIM}  Teach mode disabled{RESET}\n");
        }
        "" => {
            // Toggle
            let new_state = !is_teach_mode();
            set_teach_mode(new_state);
            if new_state {
                println!("{GREEN}  🎓 Teach mode enabled — yoyo will explain its reasoning as it works{RESET}\n");
            } else {
                println!("{DIM}  Teach mode disabled{RESET}\n");
            }
        }
        _ => {
            println!("{DIM}  usage: /teach [on|off]");
            println!("  Toggle teach mode. When active, yoyo explains its reasoning as it works.{RESET}\n");
        }
    }
}

/// Build the `/mcp help` text. Extracted as a pure function so tests can
/// assert on its contents (e.g. to guard against the stale "coming soon"
/// string returning, or server-filesystem sneaking back in as the primary
/// example — it collides with yoyo's read_file/write_file builtins and is
/// skipped at startup).
pub(crate) fn mcp_help_text() -> String {
    // server-fetch is the primary example because it exposes a single `fetch`
    // tool that does NOT collide with any name in BUILTIN_TOOL_NAMES. Do not
    // replace with server-filesystem — see the Day 39 collision guard.
    let mut s = String::new();
    s.push_str("  MCP (Model Context Protocol) Server Configuration\n");
    s.push('\n');
    s.push_str("  Add MCP servers to .yoyo.toml or ~/.config/yoyo/config.toml:\n");
    s.push('\n');
    s.push_str("  # Structured format (recommended):\n");
    s.push_str("  [mcp_servers.fetch]\n");
    s.push_str("  command = \"npx\"\n");
    s.push_str("  args = [\"-y\", \"@modelcontextprotocol/server-fetch\"]\n");
    s.push('\n');
    s.push_str("  [mcp_servers.postgres]\n");
    s.push_str("  command = \"npx\"\n");
    s.push_str("  args = [\"-y\", \"@modelcontextprotocol/server-postgres\"]\n");
    s.push_str("  env = { DATABASE_URL = \"postgresql://localhost/mydb\" }\n");
    s.push('\n');
    s.push_str("  # Simple format (legacy):\n");
    s.push_str("  mcp = [\"npx -y @modelcontextprotocol/server-fetch\"]\n");
    s.push('\n');
    s.push_str("  Or pass via CLI:\n");
    s.push_str("  yoyo --mcp \"npx -y @modelcontextprotocol/server-fetch\"\n");
    s.push('\n');
    s.push_str("  Note: @modelcontextprotocol/server-filesystem exposes read_file and\n");
    s.push_str("  write_file tools which collide with yoyo's builtins — yoyo skips any\n");
    s.push_str("  server whose tool names collide (see CLAUDE.md → \"MCP gotchas\").\n");
    s.push_str("  Prefer server-fetch, server-memory, or server-sequential-thinking.\n");
    s.push('\n');
    s.push_str("  Subcommands:\n");
    s.push_str("    /mcp         List configured MCP servers\n");
    s.push_str("    /mcp list    List configured MCP servers\n");
    s.push_str("    /mcp help    Show this help\n");
    s
}

/// Build the "configured but not connected" status message shown by
/// `/mcp list` when servers are configured but zero managed to connect.
/// Pure function so tests can assert it never contains "coming soon" again.
pub(crate) fn mcp_not_connected_message(total: usize) -> String {
    let mut s = String::new();
    s.push_str(&format!(
        "  {total} server(s) configured but none connected.\n"
    ));
    s.push('\n');
    s.push_str("  Common causes:\n");
    s.push_str("    • Tool name collision with a yoyo builtin. For example,\n");
    s.push_str("      @modelcontextprotocol/server-filesystem exposes read_file and\n");
    s.push_str("      write_file which collide — such servers are skipped at startup.\n");
    s.push_str("      Check stderr for a \"skipping MCP server\" warning.\n");
    s.push_str("    • Server failed to spawn (bad command path or args in your config).\n");
    s.push('\n');
    s.push_str("  See CLAUDE.md → \"MCP gotchas\" for the full list of reserved tool names.\n");
    s
}

/// Handle the `/mcp` command: list configured MCP servers and show help.
pub fn handle_mcp(
    input: &str,
    cli_servers: &[String],
    server_configs: &[crate::cli::McpServerConfig],
    mcp_count: u32,
) {
    let arg = input.strip_prefix("/mcp").unwrap_or("").trim();

    match arg {
        "help" => {
            println!("{DIM}{}{RESET}", mcp_help_text());
        }
        "" | "list" => {
            let has_cli = !cli_servers.is_empty();
            let has_configs = !server_configs.is_empty();

            if !has_cli && !has_configs {
                println!("{DIM}  No MCP servers configured.");
                println!();
                println!("  Add servers to .yoyo.toml:");
                println!("    [mcp_servers.myserver]");
                println!("    command = \"npx\"");
                println!("    args = [\"-y\", \"@modelcontextprotocol/server-fetch\"]");
                println!();
                println!("  See /mcp help for more details.{RESET}\n");
                return;
            }

            println!("{DIM}  MCP Servers:");

            // List structured configs first
            for cfg in server_configs {
                let full_cmd = if cfg.args.is_empty() {
                    cfg.command.clone()
                } else {
                    format!("{} {}", cfg.command, cfg.args.join(" "))
                };
                println!("    {:<14}{}", cfg.name, full_cmd);
            }

            // List CLI --mcp servers
            for cmd in cli_servers {
                // Use the command name (first word) as an identifier
                let label = cmd.split_whitespace().next().unwrap_or("unknown");
                println!("    {:<14}{}", label, cmd);
            }

            let total = cli_servers.len() + server_configs.len();
            println!();
            if mcp_count > 0 {
                println!(
                    "  {} server(s) configured, {} connected{RESET}\n",
                    total, mcp_count
                );
            } else {
                println!("{}{RESET}", mcp_not_connected_message(total));
            }
        }
        _ => {
            println!("{DIM}  Unknown /mcp subcommand: {arg}");
            println!("  Usage: /mcp [list|help]{RESET}\n");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::commands_git::{
        build_review_content, build_review_prompt, format_diff_stat, parse_diff_stat,
        parse_pr_args, DiffStatEntry, DiffStatSummary, PrSubcommand,
    };
    use crate::commands_search::{
        extract_first_meaningful_line, find_files, format_project_index, fuzzy_score,
        highlight_match, is_binary_extension, IndexEntry,
    };
    use crate::commands_session::{parse_bookmark_name, parse_spawn_args, parse_spawn_task};
    use crate::memory::{
        add_memory, format_memories_for_prompt, load_memories_from, remove_memory, MemoryEntry,
        ProjectMemory,
    };
    use std::collections::HashMap;
    use std::path::PathBuf;
    use yoagent::ThinkingLevel;

    // ── /config show tests ────────────────────────────────────────────
    // Runtime config introspection — see `format_config_output` and
    // `is_secret_key` above. These tests pin the two most important
    // invariants: (1) secrets are NEVER printed raw, and (2) the
    // no-config-loaded path produces a clear message instead of
    // crashing or printing an empty block.

    #[test]
    fn test_format_config_masks_secret_values() {
        let mut config = HashMap::new();
        let raw_key = "sk-ant-super-secret-do-not-leak-12345";
        config.insert("anthropic_api_key".to_string(), raw_key.to_string());
        config.insert("model".to_string(), "claude-sonnet-4-6".to_string());

        let path = PathBuf::from("/fake/path/.yoyo.toml");
        let out = format_config_output(&config, Some(&path));

        // The raw secret value must never appear in the output.
        assert!(
            !out.contains(raw_key),
            "raw secret leaked into /config show output:\n{out}"
        );
        // The mask must appear so the user can see the key exists.
        assert!(
            out.contains("***"),
            "expected masked placeholder in output:\n{out}"
        );
        // Non-secret keys should be visible as-is.
        assert!(
            out.contains("claude-sonnet-4-6"),
            "non-secret value should be visible:\n{out}"
        );
        // The loaded path should be named.
        assert!(
            out.contains("/fake/path/.yoyo.toml"),
            "loaded config path should be shown:\n{out}"
        );
    }

    #[test]
    fn test_format_config_no_file_loaded() {
        let config: HashMap<String, String> = HashMap::new();
        let out = format_config_output(&config, None);

        // Must say something clear about the no-config case.
        assert!(
            out.to_lowercase().contains("no config file loaded"),
            "expected 'no config file loaded' message, got:\n{out}"
        );
        // Must not crash and must not print stale path markers.
        assert!(
            !out.contains("Loaded config:"),
            "should not claim a config was loaded:\n{out}"
        );
    }

    #[test]
    fn test_is_secret_key_matches_common_patterns() {
        // Positive — all of these should be masked.
        assert!(is_secret_key("anthropic_api_key"));
        assert!(is_secret_key("API_KEY"));
        assert!(is_secret_key("openai_token"));
        assert!(is_secret_key("client_secret"));
        assert!(is_secret_key("db_password"));
        assert!(is_secret_key("AccessToken"));

        // Negative — ordinary config keys should pass through.
        assert!(!is_secret_key("model"));
        assert!(!is_secret_key("provider"));
        assert!(!is_secret_key("thinking"));
        assert!(!is_secret_key("temperature"));
    }

    #[test]
    fn test_format_config_sorts_keys_deterministically() {
        let mut config = HashMap::new();
        config.insert("zebra".to_string(), "z".to_string());
        config.insert("alpha".to_string(), "a".to_string());
        config.insert("mike".to_string(), "m".to_string());
        let path = PathBuf::from(".yoyo.toml");
        let out = format_config_output(&config, Some(&path));

        let alpha_pos = out.find("alpha").expect("alpha should appear");
        let mike_pos = out.find("mike").expect("mike should appear");
        let zebra_pos = out.find("zebra").expect("zebra should appear");
        assert!(
            alpha_pos < mike_pos && mike_pos < zebra_pos,
            "keys should be sorted alphabetically:\n{out}"
        );
    }

    #[test]
    fn test_command_parsing_quit() {
        let quit_commands = ["/quit", "/exit"];
        for cmd in &quit_commands {
            assert!(
                *cmd == "/quit" || *cmd == "/exit",
                "Unrecognized quit command: {cmd}"
            );
        }
    }

    #[test]
    fn test_command_parsing_model() {
        let input = "/model claude-opus-4-6";
        assert!(input.starts_with("/model "));
        let model_name = input.trim_start_matches("/model ").trim();
        assert_eq!(model_name, "claude-opus-4-6");
    }

    #[test]
    fn test_command_parsing_model_whitespace() {
        let input = "/model   claude-opus-4-6  ";
        let model_name = input.trim_start_matches("/model ").trim();
        assert_eq!(model_name, "claude-opus-4-6");
    }

    #[test]
    fn test_command_help_recognized() {
        let commands = [
            "/help",
            "/quit",
            "/exit",
            "/clear",
            "/compact",
            "/commit",
            "/config",
            "/context",
            "/cost",
            "/docs",
            "/find",
            "/fix",
            "/forget",
            "/index",
            "/init",
            "/status",
            "/tokens",
            "/save",
            "/load",
            "/diff",
            "/undo",
            "/health",
            "/retry",
            "/run",
            "/history",
            "/search",
            "/model",
            "/think",
            "/version",
            "/tree",
            "/pr",
            "/git",
            "/test",
            "/lint",
            "/spawn",
            "/review",
            "/mark",
            "/jump",
            "/marks",
            "/remember",
            "/memories",
            "/provider",
            "/changes",
        ];
        for cmd in &commands {
            assert!(
                KNOWN_COMMANDS.contains(cmd),
                "Command not in KNOWN_COMMANDS: {cmd}"
            );
        }
    }

    #[test]
    fn test_model_switch_updates_variable() {
        let original = "claude-opus-4-6";
        let input = "/model claude-haiku-35";
        let new_model = input.trim_start_matches("/model ").trim();
        assert_ne!(new_model, original);
        assert_eq!(new_model, "claude-haiku-35");
    }

    #[test]
    fn test_bare_model_command_is_recognized() {
        let input = "/model";
        assert_eq!(input, "/model");
        assert!(!input.starts_with("/model "));
    }

    #[test]
    fn test_provider_command_recognized() {
        assert!(!is_unknown_command("/provider"));
        assert!(!is_unknown_command("/provider openai"));
        assert!(
            KNOWN_COMMANDS.contains(&"/provider"),
            "/provider should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_provider_command_matching() {
        let provider_matches = |s: &str| s == "/provider" || s.starts_with("/provider ");
        assert!(provider_matches("/provider"));
        assert!(provider_matches("/provider openai"));
        assert!(provider_matches("/provider google"));
        assert!(!provider_matches("/providers"));
        assert!(!provider_matches("/providing"));
    }

    #[test]
    fn test_provider_show_does_not_panic() {
        // handle_provider_show should not panic for any known provider
        for provider in KNOWN_PROVIDERS {
            handle_provider_show(provider);
        }
    }

    #[test]
    fn test_provider_switch_valid() {
        use crate::cli;
        let mut config = crate::AgentConfig {
            model: "claude-opus-4-6".to_string(),
            api_key: "test-key".to_string(),
            provider: "anthropic".to_string(),
            base_url: None,
            skills: yoagent::skills::SkillSet::empty(),
            system_prompt: "Test.".to_string(),
            thinking: ThinkingLevel::Off,
            max_tokens: None,
            temperature: None,
            max_turns: None,
            auto_approve: true,
            permissions: cli::PermissionConfig::default(),
            dir_restrictions: cli::DirectoryRestrictions::default(),
            context_strategy: cli::ContextStrategy::default(),
            context_window: None,
            shell_hooks: vec![],
            fallback_provider: None,
            fallback_model: None,
        };
        let mut agent = config.build_agent();
        handle_provider_switch("openai", &mut config, &mut agent);
        assert_eq!(config.provider, "openai");
        assert_eq!(config.model, "gpt-4o");
    }

    #[test]
    fn test_provider_switch_invalid() {
        use crate::cli;
        let mut config = crate::AgentConfig {
            model: "claude-opus-4-6".to_string(),
            api_key: "test-key".to_string(),
            provider: "anthropic".to_string(),
            base_url: None,
            skills: yoagent::skills::SkillSet::empty(),
            system_prompt: "Test.".to_string(),
            thinking: ThinkingLevel::Off,
            max_tokens: None,
            temperature: None,
            max_turns: None,
            auto_approve: true,
            permissions: cli::PermissionConfig::default(),
            dir_restrictions: cli::DirectoryRestrictions::default(),
            context_strategy: cli::ContextStrategy::default(),
            context_window: None,
            shell_hooks: vec![],
            fallback_provider: None,
            fallback_model: None,
        };
        let mut agent = config.build_agent();
        // Invalid provider should not change the config
        handle_provider_switch("nonexistent_provider", &mut config, &mut agent);
        assert_eq!(config.provider, "anthropic");
        assert_eq!(config.model, "claude-opus-4-6");
    }

    #[test]
    fn test_provider_switch_sets_default_model() {
        use crate::cli;
        let mut config = crate::AgentConfig {
            model: "claude-opus-4-6".to_string(),
            api_key: "test-key".to_string(),
            provider: "anthropic".to_string(),
            base_url: None,
            skills: yoagent::skills::SkillSet::empty(),
            system_prompt: "Test.".to_string(),
            thinking: ThinkingLevel::Off,
            max_tokens: None,
            temperature: None,
            max_turns: None,
            auto_approve: true,
            permissions: cli::PermissionConfig::default(),
            dir_restrictions: cli::DirectoryRestrictions::default(),
            context_strategy: cli::ContextStrategy::default(),
            context_window: None,
            shell_hooks: vec![],
            fallback_provider: None,
            fallback_model: None,
        };
        let mut agent = config.build_agent();
        // Switch to google → should use gemini default
        handle_provider_switch("google", &mut config, &mut agent);
        assert_eq!(config.provider, "google");
        assert_eq!(config.model, "gemini-2.0-flash");
    }

    #[test]
    fn test_provider_arg_completions_empty() {
        let candidates = command_arg_completions("/provider", "");
        assert!(!candidates.is_empty(), "Should return known providers");
        assert!(candidates.contains(&"anthropic".to_string()));
        assert!(candidates.contains(&"openai".to_string()));
        assert!(candidates.contains(&"google".to_string()));
    }

    #[test]
    fn test_provider_arg_completions_partial() {
        let candidates = command_arg_completions("/provider", "o");
        assert!(
            !candidates.is_empty(),
            "Should match providers starting with 'o'"
        );
        for c in &candidates {
            assert!(c.starts_with("o"), "All results should start with 'o': {c}");
        }
        assert!(candidates.contains(&"openai".to_string()));
        assert!(candidates.contains(&"openrouter".to_string()));
        assert!(candidates.contains(&"ollama".to_string()));
    }

    #[test]
    fn test_provider_arg_completions_no_match() {
        let candidates = command_arg_completions("/provider", "zzz_nonexistent");
        assert!(
            candidates.is_empty(),
            "Should return no matches for nonsense"
        );
    }

    #[test]
    fn test_unknown_slash_command_detection() {
        assert!(is_unknown_command("/foo"));
        assert!(is_unknown_command("/foo bar baz"));
        assert!(is_unknown_command("/unknown argument"));
        // Verify typo-like commands are caught as unknown
        assert!(is_unknown_command("/savefile"));
        assert!(is_unknown_command("/loadfile"));

        assert!(!is_unknown_command("/help"));
        assert!(!is_unknown_command("/quit"));
        assert!(!is_unknown_command("/model"));
        assert!(!is_unknown_command("/model claude-opus-4-6"));
        assert!(!is_unknown_command("/save"));
        assert!(!is_unknown_command("/save myfile.json"));
        assert!(!is_unknown_command("/load"));
        assert!(!is_unknown_command("/load myfile.json"));
        assert!(!is_unknown_command("/config"));
        assert!(!is_unknown_command("/context"));
        assert!(!is_unknown_command("/version"));
        assert!(!is_unknown_command("/provider"));
        assert!(!is_unknown_command("/provider openai"));
    }

    #[test]
    fn test_thinking_level_name() {
        assert_eq!(thinking_level_name(ThinkingLevel::Off), "off");
        assert_eq!(thinking_level_name(ThinkingLevel::Minimal), "minimal");
        assert_eq!(thinking_level_name(ThinkingLevel::Low), "low");
        assert_eq!(thinking_level_name(ThinkingLevel::Medium), "medium");
        assert_eq!(thinking_level_name(ThinkingLevel::High), "high");
    }

    #[test]
    fn test_pr_command_recognized() {
        assert!(!is_unknown_command("/pr"));
        assert!(!is_unknown_command("/pr 42"));
        assert!(!is_unknown_command("/pr 123"));
    }

    #[test]
    fn test_pr_command_matching() {
        // /pr should match exact or with space separator, not /print etc.
        let pr_matches = |s: &str| s == "/pr" || s.starts_with("/pr ");
        assert!(pr_matches("/pr"));
        assert!(pr_matches("/pr 42"));
        assert!(pr_matches("/pr 123"));
        assert!(!pr_matches("/print"));
        assert!(!pr_matches("/process"));
    }

    #[test]
    fn test_pr_number_parsing() {
        // Verify we can parse a PR number from /pr <number>
        let input = "/pr 42";
        let arg = input.strip_prefix("/pr").unwrap_or("").trim();
        assert_eq!(arg, "42");
        assert!(arg.parse::<u32>().is_ok());
        assert_eq!(arg.parse::<u32>().unwrap(), 42);

        // Bare /pr has empty arg
        let input_bare = "/pr";
        let arg_bare = input_bare.strip_prefix("/pr").unwrap_or("").trim();
        assert!(arg_bare.is_empty());
    }

    #[test]
    fn test_pr_subcommand_list() {
        assert_eq!(parse_pr_args(""), PrSubcommand::List);
        assert_eq!(parse_pr_args("  "), PrSubcommand::List);
    }

    #[test]
    fn test_pr_subcommand_view() {
        assert_eq!(parse_pr_args("42"), PrSubcommand::View(42));
        assert_eq!(parse_pr_args("123"), PrSubcommand::View(123));
        assert_eq!(parse_pr_args("1"), PrSubcommand::View(1));
    }

    #[test]
    fn test_pr_subcommand_diff() {
        assert_eq!(parse_pr_args("42 diff"), PrSubcommand::Diff(42));
        assert_eq!(parse_pr_args("7 diff"), PrSubcommand::Diff(7));
    }

    #[test]
    fn test_pr_subcommand_checkout() {
        assert_eq!(parse_pr_args("42 checkout"), PrSubcommand::Checkout(42));
        assert_eq!(parse_pr_args("99 checkout"), PrSubcommand::Checkout(99));
    }

    #[test]
    fn test_pr_subcommand_comment() {
        assert_eq!(
            parse_pr_args("42 comment looks good!"),
            PrSubcommand::Comment(42, "looks good!".to_string())
        );
        assert_eq!(
            parse_pr_args("10 comment LGTM, merging now"),
            PrSubcommand::Comment(10, "LGTM, merging now".to_string())
        );
    }

    #[test]
    fn test_pr_subcommand_comment_requires_text() {
        // comment without text should show help
        assert_eq!(parse_pr_args("42 comment"), PrSubcommand::Help);
        assert_eq!(parse_pr_args("42 comment  "), PrSubcommand::Help);
    }

    #[test]
    fn test_pr_subcommand_invalid() {
        assert_eq!(parse_pr_args("abc"), PrSubcommand::Help);
        assert_eq!(parse_pr_args("42 unknown"), PrSubcommand::Help);
        assert_eq!(parse_pr_args("42 merge"), PrSubcommand::Help);
    }

    #[test]
    fn test_pr_subcommand_case_insensitive() {
        assert_eq!(parse_pr_args("42 DIFF"), PrSubcommand::Diff(42));
        assert_eq!(parse_pr_args("42 Checkout"), PrSubcommand::Checkout(42));
        assert_eq!(
            parse_pr_args("42 Comment nice work"),
            PrSubcommand::Comment(42, "nice work".to_string())
        );
    }

    #[test]
    fn test_pr_subcommand_create() {
        assert_eq!(
            parse_pr_args("create"),
            PrSubcommand::Create { draft: false }
        );
        assert_eq!(
            parse_pr_args("CREATE"),
            PrSubcommand::Create { draft: false }
        );
        assert_eq!(
            parse_pr_args("Create"),
            PrSubcommand::Create { draft: false }
        );
    }

    #[test]
    fn test_pr_subcommand_create_draft() {
        assert_eq!(
            parse_pr_args("create --draft"),
            PrSubcommand::Create { draft: true }
        );
        assert_eq!(
            parse_pr_args("create draft"),
            PrSubcommand::Create { draft: true }
        );
        assert_eq!(
            parse_pr_args("CREATE --DRAFT"),
            PrSubcommand::Create { draft: true }
        );
    }

    #[test]
    fn test_pr_subcommand_create_no_flag() {
        // "create somethingelse" should still create but not be draft
        assert_eq!(
            parse_pr_args("create --nodraft"),
            PrSubcommand::Create { draft: false }
        );
    }

    #[test]
    fn test_pr_subcommand_recognized() {
        // Subcommands should not be flagged as unknown commands
        assert!(!is_unknown_command("/pr 42 diff"));
        assert!(!is_unknown_command("/pr 42 comment hello"));
        assert!(!is_unknown_command("/pr 42 checkout"));
    }

    #[test]
    fn test_save_load_command_matching() {
        // /save and /load should only match exact word or with space separator
        // This tests the fix for /savefile being treated as /save
        let save_matches = |s: &str| s == "/save" || s.starts_with("/save ");
        let load_matches = |s: &str| s == "/load" || s.starts_with("/load ");

        assert!(save_matches("/save"));
        assert!(save_matches("/save myfile.json"));
        assert!(!save_matches("/savefile"));
        assert!(!save_matches("/saveXYZ"));

        assert!(load_matches("/load"));
        assert!(load_matches("/load myfile.json"));
        assert!(!load_matches("/loadfile"));
        assert!(!load_matches("/loadXYZ"));
    }

    #[test]
    fn test_docs_command_recognized() {
        assert!(!is_unknown_command("/docs"));
        assert!(!is_unknown_command("/docs serde"));
        assert!(!is_unknown_command("/docs tokio"));
        assert!(
            KNOWN_COMMANDS.contains(&"/docs"),
            "/docs should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_docs_command_matching() {
        // /docs should match exact or with space, not /docstring etc.
        let docs_matches = |s: &str| s == "/docs" || s.starts_with("/docs ");
        assert!(docs_matches("/docs"));
        assert!(docs_matches("/docs serde"));
        assert!(docs_matches("/docs tokio-runtime"));
        assert!(!docs_matches("/docstring"));
        assert!(!docs_matches("/docsify"));
    }

    #[test]
    fn test_docs_crate_arg_extraction() {
        let input = "/docs serde";
        let crate_name = input.trim_start_matches("/docs ").trim();
        assert_eq!(crate_name, "serde");

        let input2 = "/docs tokio-runtime";
        let crate_name2 = input2.trim_start_matches("/docs ").trim();
        assert_eq!(crate_name2, "tokio-runtime");

        // Bare /docs has empty after stripping
        let input_bare = "/docs";
        assert_eq!(input_bare, "/docs");
        assert!(!input_bare.starts_with("/docs "));
    }

    #[test]
    fn test_spawn_command_recognized() {
        assert!(!is_unknown_command("/spawn"));
        assert!(!is_unknown_command("/spawn read src/main.rs and summarize"));
        assert!(
            KNOWN_COMMANDS.contains(&"/spawn"),
            "/spawn should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_spawn_command_matching() {
        // /spawn should match exact or with space separator, not /spawning
        let spawn_matches = |s: &str| s == "/spawn" || s.starts_with("/spawn ");
        assert!(spawn_matches("/spawn"));
        assert!(spawn_matches("/spawn read file"));
        assert!(spawn_matches("/spawn analyze the codebase"));
        assert!(!spawn_matches("/spawning"));
        assert!(!spawn_matches("/spawnpoint"));
    }

    #[test]
    fn test_parse_spawn_task_with_task() {
        let task = parse_spawn_task("/spawn read src/main.rs and summarize");
        assert_eq!(task, Some("read src/main.rs and summarize".to_string()));
    }

    #[test]
    fn test_parse_spawn_task_empty() {
        let task = parse_spawn_task("/spawn");
        assert_eq!(task, None);
    }

    #[test]
    fn test_parse_spawn_task_whitespace_only() {
        let task = parse_spawn_task("/spawn   ");
        assert_eq!(task, None);
    }

    #[test]
    fn test_parse_spawn_task_preserves_full_task() {
        let task = parse_spawn_task("/spawn analyze src/ and list all public functions");
        assert_eq!(
            task,
            Some("analyze src/ and list all public functions".to_string())
        );
    }

    #[test]
    fn test_parse_spawn_args_basic() {
        let args = parse_spawn_args("/spawn do something");
        assert!(args.is_some());
        let args = args.unwrap();
        assert_eq!(args.task, "do something");
        assert!(args.output_path.is_none());
    }

    #[test]
    fn test_parse_spawn_args_with_output() {
        let args = parse_spawn_args("/spawn -o out.md write a summary");
        assert!(args.is_some());
        let args = args.unwrap();
        assert_eq!(args.task, "write a summary");
        assert_eq!(args.output_path, Some("out.md".to_string()));
    }

    #[test]
    fn test_parse_spawn_args_status() {
        assert!(parse_spawn_args("/spawn status").is_none());
    }

    #[test]
    fn test_find_command_recognized() {
        assert!(!is_unknown_command("/find"));
        assert!(!is_unknown_command("/find main"));
        assert!(!is_unknown_command("/find .toml"));
        assert!(
            KNOWN_COMMANDS.contains(&"/find"),
            "/find should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_fuzzy_score_basic_match() {
        // Pattern found in path → Some score
        let score = fuzzy_score("src/main.rs", "main");
        assert!(score.is_some(), "should match 'main' in 'src/main.rs'");
        assert!(score.unwrap() > 0, "score should be positive");
    }

    #[test]
    fn test_fuzzy_score_no_match() {
        let score = fuzzy_score("src/main.rs", "zzznotfound");
        assert!(score.is_none(), "should not match 'zzznotfound'");
    }

    #[test]
    fn test_fuzzy_score_case_insensitive() {
        let score_lower = fuzzy_score("src/main.rs", "main");
        let score_upper = fuzzy_score("src/main.rs", "MAIN");
        assert!(score_lower.is_some());
        assert!(score_upper.is_some());
        // Both should match with same score
        assert_eq!(score_lower, score_upper);
    }

    #[test]
    fn test_fuzzy_score_filename_match_higher() {
        // "main" matches in filename for "src/main.rs" but only in dir for "main/other.rs"
        let filename_score = fuzzy_score("src/main.rs", "main");
        let dir_score = fuzzy_score("main_stuff/other.rs", "main");
        assert!(filename_score.is_some());
        assert!(dir_score.is_some());
        // Filename match should score higher because it gets the filename bonus
        assert!(
            filename_score.unwrap() > dir_score.unwrap(),
            "filename match should score higher: {} vs {}",
            filename_score.unwrap(),
            dir_score.unwrap()
        );
    }

    #[test]
    fn test_fuzzy_score_start_of_filename_bonus() {
        // "cli" at start of filename should score higher than "cli" embedded elsewhere
        let start_score = fuzzy_score("src/cli.rs", "cli");
        let mid_score = fuzzy_score("src/public_client.rs", "cli");
        assert!(start_score.is_some());
        assert!(mid_score.is_some());
        assert!(
            start_score.unwrap() > mid_score.unwrap(),
            "start-of-filename match should score higher: {} vs {}",
            start_score.unwrap(),
            mid_score.unwrap()
        );
    }

    #[test]
    fn test_find_files_returns_sorted() {
        // Search for a common pattern in this project
        let matches = find_files("main");
        assert!(!matches.is_empty(), "should find files matching 'main'");
        // Results should be sorted by score descending
        for window in matches.windows(2) {
            assert!(
                window[0].score >= window[1].score,
                "results should be sorted by score descending: {} >= {}",
                window[0].score,
                window[1].score
            );
        }
    }

    #[test]
    fn test_find_files_no_results() {
        let matches = find_files("xyzzy_nonexistent_pattern_12345");
        assert!(
            matches.is_empty(),
            "should find no files for nonsense pattern"
        );
    }

    #[test]
    fn test_find_command_matching() {
        // /find should match exact or with space separator, not /finding
        let find_matches = |s: &str| s == "/find" || s.starts_with("/find ");
        assert!(find_matches("/find"));
        assert!(find_matches("/find main"));
        assert!(find_matches("/find .toml"));
        assert!(!find_matches("/finding"));
        assert!(!find_matches("/findall"));
    }

    #[test]
    fn test_highlight_match_basic() {
        let result = highlight_match("src/main.rs", "main");
        // Should contain the original path text
        assert!(result.contains("main"));
        assert!(result.contains("src/"));
        assert!(result.contains(".rs"));
    }

    #[test]
    fn test_review_command_recognized() {
        assert!(!is_unknown_command("/review"));
        assert!(!is_unknown_command("/review src/main.rs"));
        assert!(
            KNOWN_COMMANDS.contains(&"/review"),
            "/review should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_review_command_matching() {
        // /review should match exact or with space separator, not /reviewing
        let review_matches = |s: &str| s == "/review" || s.starts_with("/review ");
        assert!(review_matches("/review"));
        assert!(review_matches("/review src/main.rs"));
        assert!(review_matches("/review Cargo.toml"));
        assert!(!review_matches("/reviewing"));
        assert!(!review_matches("/reviewer"));
    }

    #[test]
    fn test_build_review_prompt_contains_content() {
        let prompt =
            build_review_prompt("staged changes", "fn main() {\n    println!(\"hello\");\n}");
        assert!(
            prompt.contains("staged changes"),
            "Should mention the label"
        );
        assert!(prompt.contains("fn main()"), "Should contain the code");
        assert!(prompt.contains("Bugs"), "Should ask for bug review");
        assert!(
            prompt.contains("Security"),
            "Should ask for security review"
        );
        assert!(prompt.contains("Style"), "Should ask for style review");
        assert!(
            prompt.contains("Performance"),
            "Should ask for performance review"
        );
        assert!(prompt.contains("Suggestions"), "Should ask for suggestions");
    }

    #[test]
    fn test_build_review_prompt_truncates_large_content() {
        let large_content = "x".repeat(40_000);
        let prompt = build_review_prompt("big file", &large_content);
        assert!(
            prompt.contains("truncated"),
            "Large content should be truncated"
        );
        assert!(
            prompt.len() < 40_000,
            "Prompt should be truncated, got {} chars",
            prompt.len()
        );
    }

    #[test]
    fn test_build_review_content_nonexistent_file() {
        let result = build_review_content("nonexistent_file_xyz_12345.rs");
        assert!(result.is_none(), "Nonexistent file should return None");
    }

    #[test]
    fn test_build_review_content_existing_file() {
        // Cargo.toml exists in the project root
        let result = build_review_content("Cargo.toml");
        assert!(result.is_some(), "Existing file should return Some");
        let (label, content) = result.unwrap();
        assert_eq!(label, "Cargo.toml");
        assert!(!content.is_empty(), "Content should not be empty");
    }

    #[test]
    fn test_build_review_content_empty_arg_in_git_repo() {
        // Empty arg reviews staged/unstaged changes
        // In CI, this may or may not have changes — just verify it doesn't panic
        let result = build_review_content("");
        // Result depends on git state — either Some or None is valid
        if let Some((label, _content)) = result {
            assert!(
                label.contains("changes"),
                "Label should describe what's being reviewed: {label}"
            );
        }
    }

    #[test]
    fn test_review_help_text_present() {
        // Verify /review appears in the help output by checking the handle_help function output
        // We can't easily capture stdout, but we can verify the command is in KNOWN_COMMANDS
        // and that the help text format is correct
        assert!(KNOWN_COMMANDS.contains(&"/review"));
    }

    #[test]
    fn test_init_command_recognized() {
        assert!(!is_unknown_command("/init"));
        assert!(
            KNOWN_COMMANDS.contains(&"/init"),
            "/init should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_parse_diff_stat_basic() {
        let stat_output = " src/commands.rs | 42 ++++++++++++++++++++++++++++--------------
 src/main.rs     |  8 +++++---
 2 files changed, 30 insertions(+), 20 deletions(-)
";
        let summary = parse_diff_stat(stat_output);
        assert_eq!(summary.entries.len(), 2);
        assert_eq!(summary.entries[0].file, "src/commands.rs");
        assert_eq!(summary.entries[1].file, "src/main.rs");
        assert_eq!(summary.total_insertions, 30);
        assert_eq!(summary.total_deletions, 20);
    }

    #[test]
    fn test_parse_diff_stat_single_file() {
        let stat_output = " src/format.rs | 10 +++++++---
 1 file changed, 7 insertions(+), 3 deletions(-)
";
        let summary = parse_diff_stat(stat_output);
        assert_eq!(summary.entries.len(), 1);
        assert_eq!(summary.entries[0].file, "src/format.rs");
        assert_eq!(summary.total_insertions, 7);
        assert_eq!(summary.total_deletions, 3);
    }

    #[test]
    fn test_parse_diff_stat_insertions_only() {
        let stat_output = " new_file.rs | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)
";
        let summary = parse_diff_stat(stat_output);
        assert_eq!(summary.entries.len(), 1);
        assert_eq!(summary.entries[0].file, "new_file.rs");
        assert!(summary.entries[0].insertions > 0);
        assert_eq!(summary.entries[0].deletions, 0);
        assert_eq!(summary.total_insertions, 25);
        assert_eq!(summary.total_deletions, 0);
    }

    #[test]
    fn test_parse_diff_stat_deletions_only() {
        let stat_output = " old_file.rs | 15 ---------------
 1 file changed, 15 deletions(-)
";
        let summary = parse_diff_stat(stat_output);
        assert_eq!(summary.entries.len(), 1);
        assert_eq!(summary.entries[0].file, "old_file.rs");
        assert_eq!(summary.entries[0].insertions, 0);
        assert!(summary.entries[0].deletions > 0);
        assert_eq!(summary.total_insertions, 0);
        assert_eq!(summary.total_deletions, 15);
    }

    #[test]
    fn test_parse_diff_stat_empty() {
        let summary = parse_diff_stat("");
        assert!(summary.entries.is_empty());
        assert_eq!(summary.total_insertions, 0);
        assert_eq!(summary.total_deletions, 0);
    }

    #[test]
    fn test_parse_diff_stat_no_summary_line() {
        // Sometimes stat output has no summary — compute from entries
        let stat_output = " src/main.rs | 5 +++--
";
        let summary = parse_diff_stat(stat_output);
        assert_eq!(summary.entries.len(), 1);
        // Totals computed from entry counts
        assert_eq!(summary.total_insertions, summary.entries[0].insertions);
        assert_eq!(summary.total_deletions, summary.entries[0].deletions);
    }

    #[test]
    fn test_parse_diff_stat_multiple_files() {
        let stat_output = " Cargo.toml       |  2 +-
 src/cli.rs       | 15 ++++++++-------
 src/commands.rs  | 88 +++++++++++++++++++++++++++++++++++++++++++++++++++++---
 src/format.rs    |  3 ++-
 4 files changed, 78 insertions(+), 30 deletions(-)
";
        let summary = parse_diff_stat(stat_output);
        assert_eq!(summary.entries.len(), 4);
        assert_eq!(summary.entries[0].file, "Cargo.toml");
        assert_eq!(summary.entries[2].file, "src/commands.rs");
        assert_eq!(summary.total_insertions, 78);
        assert_eq!(summary.total_deletions, 30);
    }

    #[test]
    fn test_format_diff_stat_empty() {
        let summary = DiffStatSummary {
            entries: vec![],
            total_insertions: 0,
            total_deletions: 0,
        };
        let formatted = format_diff_stat(&summary);
        assert!(
            formatted.is_empty(),
            "Empty summary should produce empty output"
        );
    }

    #[test]
    fn test_format_diff_stat_single_entry() {
        let summary = DiffStatSummary {
            entries: vec![DiffStatEntry {
                file: "src/main.rs".to_string(),
                insertions: 5,
                deletions: 2,
            }],
            total_insertions: 5,
            total_deletions: 2,
        };
        let formatted = format_diff_stat(&summary);
        assert!(formatted.contains("src/main.rs"), "Should contain filename");
        assert!(
            formatted.contains("1 file changed"),
            "Should show file count"
        );
        assert!(formatted.contains("+5"), "Should show insertions");
        assert!(formatted.contains("-2"), "Should show deletions");
    }

    #[test]
    fn test_format_diff_stat_multiple_entries() {
        let summary = DiffStatSummary {
            entries: vec![
                DiffStatEntry {
                    file: "src/a.rs".to_string(),
                    insertions: 10,
                    deletions: 0,
                },
                DiffStatEntry {
                    file: "src/b.rs".to_string(),
                    insertions: 0,
                    deletions: 5,
                },
            ],
            total_insertions: 10,
            total_deletions: 5,
        };
        let formatted = format_diff_stat(&summary);
        assert!(formatted.contains("src/a.rs"));
        assert!(formatted.contains("src/b.rs"));
        assert!(formatted.contains("2 files changed"));
    }

    #[test]
    fn test_format_diff_stat_insertions_only_no_deletions_shown() {
        let summary = DiffStatSummary {
            entries: vec![DiffStatEntry {
                file: "new.rs".to_string(),
                insertions: 10,
                deletions: 0,
            }],
            total_insertions: 10,
            total_deletions: 0,
        };
        let formatted = format_diff_stat(&summary);
        assert!(formatted.contains("+10"), "Should show insertions");
        // "-0" should not appear
        assert!(!formatted.contains("-0"), "Should not show zero deletions");
    }

    #[test]
    fn test_mark_command_recognized() {
        assert!(!is_unknown_command("/mark"));
        assert!(!is_unknown_command("/mark checkpoint"));
        assert!(
            KNOWN_COMMANDS.contains(&"/mark"),
            "/mark should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_jump_command_recognized() {
        assert!(!is_unknown_command("/jump"));
        assert!(!is_unknown_command("/jump checkpoint"));
        assert!(
            KNOWN_COMMANDS.contains(&"/jump"),
            "/jump should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_marks_command_recognized() {
        assert!(!is_unknown_command("/marks"));
        assert!(
            KNOWN_COMMANDS.contains(&"/marks"),
            "/marks should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_parse_bookmark_name_with_name() {
        let name = parse_bookmark_name("/mark checkpoint", "/mark");
        assert_eq!(name, Some("checkpoint".to_string()));
    }

    #[test]
    fn test_parse_bookmark_name_with_spaces() {
        let name = parse_bookmark_name("/mark  my bookmark  ", "/mark");
        assert_eq!(name, Some("my bookmark".to_string()));
    }

    #[test]
    fn test_parse_bookmark_name_empty() {
        let name = parse_bookmark_name("/mark", "/mark");
        assert_eq!(name, None);
    }

    #[test]
    fn test_parse_bookmark_name_whitespace_only() {
        let name = parse_bookmark_name("/mark   ", "/mark");
        assert_eq!(name, None);
    }

    #[test]
    fn test_parse_bookmark_name_for_jump() {
        let name = parse_bookmark_name("/jump start", "/jump");
        assert_eq!(name, Some("start".to_string()));
    }

    #[test]
    fn test_bookmarks_create_and_list() {
        let mut bookmarks = Bookmarks::new();
        assert!(bookmarks.is_empty());

        bookmarks.insert("start".to_string(), "[]".to_string());
        assert_eq!(bookmarks.len(), 1);
        assert!(bookmarks.contains_key("start"));
    }

    #[test]
    fn test_bookmarks_overwrite_same_name() {
        let mut bookmarks = Bookmarks::new();
        bookmarks.insert("checkpoint".to_string(), "[1]".to_string());
        bookmarks.insert("checkpoint".to_string(), "[1,2]".to_string());
        // Should still have just one entry
        assert_eq!(bookmarks.len(), 1);
        assert_eq!(bookmarks.get("checkpoint").unwrap(), "[1,2]");
    }

    #[test]
    fn test_bookmarks_nonexistent_returns_none() {
        let bookmarks = Bookmarks::new();
        assert!(!bookmarks.contains_key("nonexistent"));
    }

    #[test]
    fn test_bookmarks_multiple_entries() {
        let mut bookmarks = Bookmarks::new();
        bookmarks.insert("start".to_string(), "[]".to_string());
        bookmarks.insert("middle".to_string(), "[1]".to_string());
        bookmarks.insert("end".to_string(), "[1,2,3]".to_string());
        assert_eq!(bookmarks.len(), 3);
        assert!(bookmarks.contains_key("start"));
        assert!(bookmarks.contains_key("middle"));
        assert!(bookmarks.contains_key("end"));
    }

    #[test]
    fn test_handle_marks_empty_does_not_panic() {
        let bookmarks = Bookmarks::new();
        // Should not panic — just prints a message
        handle_marks(&bookmarks);
    }

    #[test]
    fn test_handle_marks_with_entries_does_not_panic() {
        let mut bookmarks = Bookmarks::new();
        bookmarks.insert("alpha".to_string(), "[]".to_string());
        bookmarks.insert("beta".to_string(), "[]".to_string());
        // Should not panic
        handle_marks(&bookmarks);
    }

    #[test]
    fn test_mark_command_matching() {
        // /mark should match exact or with space, not /marker
        let mark_matches = |s: &str| s == "/mark" || s.starts_with("/mark ");
        assert!(mark_matches("/mark"));
        assert!(mark_matches("/mark checkpoint"));
        assert!(!mark_matches("/marker"));
        assert!(!mark_matches("/marking"));
    }

    #[test]
    fn test_jump_command_matching() {
        // /jump should match exact or with space, not /jumper
        let jump_matches = |s: &str| s == "/jump" || s.starts_with("/jump ");
        assert!(jump_matches("/jump"));
        assert!(jump_matches("/jump checkpoint"));
        assert!(!jump_matches("/jumper"));
        assert!(!jump_matches("/jumping"));
    }

    #[test]
    fn test_arg_completions_model_empty_prefix() {
        let candidates = command_arg_completions("/model", "");
        assert!(!candidates.is_empty(), "Should return known models");
        assert!(
            candidates.iter().any(|c| c.contains("claude")),
            "Should include Claude models"
        );
    }

    #[test]
    fn test_arg_completions_model_partial_prefix() {
        let candidates = command_arg_completions("/model", "claude");
        assert!(
            !candidates.is_empty(),
            "Should match models starting with 'claude'"
        );
        for c in &candidates {
            assert!(
                c.starts_with("claude"),
                "All results should start with 'claude': {c}"
            );
        }
    }

    #[test]
    fn test_arg_completions_model_gpt_prefix() {
        let candidates = command_arg_completions("/model", "gpt");
        assert!(
            !candidates.is_empty(),
            "Should match models starting with 'gpt'"
        );
        for c in &candidates {
            assert!(
                c.starts_with("gpt"),
                "All results should start with 'gpt': {c}"
            );
        }
    }

    #[test]
    fn test_arg_completions_model_no_match() {
        let candidates = command_arg_completions("/model", "zzz_nonexistent");
        assert!(
            candidates.is_empty(),
            "Should return no matches for nonsense"
        );
    }

    #[test]
    fn test_arg_completions_think_empty() {
        let candidates = command_arg_completions("/think", "");
        assert_eq!(candidates.len(), 5, "Should return all 5 thinking levels");
        assert!(candidates.contains(&"off".to_string()));
        assert!(candidates.contains(&"high".to_string()));
    }

    #[test]
    fn test_arg_completions_think_partial() {
        let candidates = command_arg_completions("/think", "m");
        assert_eq!(candidates.len(), 2, "Should match 'minimal' and 'medium'");
        assert!(candidates.contains(&"minimal".to_string()));
        assert!(candidates.contains(&"medium".to_string()));
    }

    #[test]
    fn test_arg_completions_git_empty() {
        let candidates = command_arg_completions("/git", "");
        assert!(!candidates.is_empty(), "Should return git subcommands");
        assert!(candidates.contains(&"status".to_string()));
        assert!(candidates.contains(&"log".to_string()));
        assert!(candidates.contains(&"add".to_string()));
        assert!(candidates.contains(&"diff".to_string()));
        assert!(candidates.contains(&"branch".to_string()));
        assert!(candidates.contains(&"stash".to_string()));
    }

    #[test]
    fn test_arg_completions_git_partial() {
        let candidates = command_arg_completions("/git", "st");
        assert_eq!(
            candidates.len(),
            2,
            "Should match 'status' and 'stash': {candidates:?}"
        );
        assert!(candidates.contains(&"status".to_string()));
        assert!(candidates.contains(&"stash".to_string()));
    }

    #[test]
    fn test_arg_completions_pr_empty() {
        let candidates = command_arg_completions("/pr", "");
        assert!(!candidates.is_empty(), "Should return PR subcommands");
        assert!(candidates.contains(&"create".to_string()));
        assert!(candidates.contains(&"checkout".to_string()));
        assert!(candidates.contains(&"diff".to_string()));
    }

    #[test]
    fn test_arg_completions_pr_partial() {
        let candidates = command_arg_completions("/pr", "c");
        assert_eq!(
            candidates.len(),
            3,
            "Should match 'comment', 'create', and 'checkout': {candidates:?}"
        );
    }

    #[test]
    fn test_arg_completions_unknown_command() {
        let candidates = command_arg_completions("/unknown", "");
        assert!(
            candidates.is_empty(),
            "Unknown commands should return no completions"
        );
    }

    #[test]
    fn test_arg_completions_help_has_args() {
        // /help should now return command names for tab completion
        let candidates = command_arg_completions("/help", "");
        assert!(!candidates.is_empty(), "/help should offer completions");
    }

    #[test]
    fn test_arg_completions_case_insensitive() {
        // Typing uppercase should still find lowercase matches
        let candidates = command_arg_completions("/model", "CLAUDE");
        assert!(
            !candidates.is_empty(),
            "Should match case-insensitively: {candidates:?}"
        );
    }

    #[test]
    fn test_arg_completions_save_load_json_files() {
        // Create a temporary .json file to test /save and /load completion
        let test_file = "test_completion_temp.json";
        std::fs::write(test_file, "{}").unwrap();

        let save_candidates = command_arg_completions("/save", "test_completion");
        let load_candidates = command_arg_completions("/load", "test_completion");

        // Clean up before asserting
        let _ = std::fs::remove_file(test_file);

        assert!(
            save_candidates.contains(&test_file.to_string()),
            "/save should complete .json files: {save_candidates:?}"
        );
        assert!(
            load_candidates.contains(&test_file.to_string()),
            "/load should complete .json files: {load_candidates:?}"
        );
    }

    #[test]
    fn test_extract_first_meaningful_line_skips_blanks() {
        let content = "\n\n\n//! Module docs here\nfn main() {}";
        let line = extract_first_meaningful_line(content);
        assert_eq!(line, "//! Module docs here");
    }

    #[test]
    fn test_extract_first_meaningful_line_empty() {
        let content = "\n\n\n";
        let line = extract_first_meaningful_line(content);
        assert_eq!(line, "");
    }

    #[test]
    fn test_extract_first_meaningful_line_truncates_long_lines() {
        let content = format!("// {}", "a".repeat(200));
        let line = extract_first_meaningful_line(&content);
        assert!(line.len() <= 83); // 80 chars + "…" (3 bytes)
        assert!(line.ends_with('…'));
    }

    #[test]
    fn test_is_binary_extension() {
        assert!(is_binary_extension("image.png"));
        assert!(is_binary_extension("font.woff2"));
        assert!(is_binary_extension("archive.tar.gz"));
        assert!(!is_binary_extension("main.rs"));
        assert!(!is_binary_extension("Cargo.toml"));
        assert!(!is_binary_extension("README.md"));
    }

    #[test]
    fn test_format_project_index_empty() {
        let entries: Vec<IndexEntry> = vec![];
        let result = format_project_index(&entries);
        assert_eq!(result, "(no indexable files found)");
    }

    #[test]
    fn test_format_project_index_with_entries() {
        let entries = vec![
            IndexEntry {
                path: "src/main.rs".to_string(),
                lines: 100,
                summary: "//! Main module".to_string(),
            },
            IndexEntry {
                path: "src/lib.rs".to_string(),
                lines: 50,
                summary: "//! Library".to_string(),
            },
        ];
        let result = format_project_index(&entries);
        assert!(result.contains("src/main.rs"));
        assert!(result.contains("100"));
        assert!(result.contains("//! Main module"));
        assert!(result.contains("src/lib.rs"));
        assert!(result.contains("50"));
        assert!(result.contains("2 files, 150 total lines"));
    }

    #[test]
    fn test_build_project_index_tempdir() {
        // Create a temp directory with known files and test indexing
        use std::fs;

        let dir = tempfile::tempdir().unwrap();
        let dir_path = dir.path();

        // Create some test files
        fs::write(dir_path.join("main.rs"), "//! Entry point\nfn main() {}\n").unwrap();
        fs::write(
            dir_path.join("lib.rs"),
            "//! Library code\npub fn hello() {}\n",
        )
        .unwrap();
        fs::write(dir_path.join("image.png"), [0x89, 0x50, 0x4e, 0x47]).unwrap();

        // We can't easily test build_project_index directly since it uses git ls-files
        // or walks cwd, but we CAN test the components
        let content = fs::read_to_string(dir_path.join("main.rs")).unwrap();
        let summary = extract_first_meaningful_line(&content);
        assert_eq!(summary, "//! Entry point");

        // Verify binary filtering
        assert!(is_binary_extension("image.png"));
        assert!(!is_binary_extension("main.rs"));
    }

    #[test]
    fn test_index_entry_construction() {
        let entry = IndexEntry {
            path: "src/commands.rs".to_string(),
            lines: 4000,
            summary: "//! REPL command handlers for yoyo.".to_string(),
        };
        assert_eq!(entry.path, "src/commands.rs");
        assert_eq!(entry.lines, 4000);
        assert_eq!(entry.summary, "//! REPL command handlers for yoyo.");
    }

    #[test]
    fn test_format_project_index_single_file() {
        let entries = vec![IndexEntry {
            path: "README.md".to_string(),
            lines: 1,
            summary: "# Hello".to_string(),
        }];
        let result = format_project_index(&entries);
        assert!(result.contains("1 file, 1 total lines"));
    }

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

    #[test]
    fn test_hooks_command_recognized() {
        assert!(!is_unknown_command("/hooks"));
        assert!(
            KNOWN_COMMANDS.contains(&"/hooks"),
            "/hooks should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_handle_hooks_empty() {
        // Should not panic with empty hooks
        handle_hooks(&[]);
    }

    #[test]
    fn test_handle_hooks_with_hooks() {
        use crate::hooks::{HookPhase, ShellHook};
        let hooks = vec![
            ShellHook {
                name: "pre:bash".to_string(),
                phase: HookPhase::Pre,
                tool_pattern: "bash".to_string(),
                command: "echo before".to_string(),
            },
            ShellHook {
                name: "post:*".to_string(),
                phase: HookPhase::Post,
                tool_pattern: "*".to_string(),
                command: "echo after".to_string(),
            },
        ];
        // Should not panic with hooks present
        handle_hooks(&hooks);
    }

    #[test]
    fn test_changes_command_recognized() {
        assert!(!is_unknown_command("/changes"));
        assert!(
            KNOWN_COMMANDS.contains(&"/changes"),
            "/changes should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_changes_command_not_confused_with_other_commands() {
        // /changes should match exactly, /changelog etc. should be unknown
        assert!(is_unknown_command("/changelog"));
        assert!(is_unknown_command("/changed"));
    }

    #[test]
    fn test_add_command_recognized() {
        assert!(!is_unknown_command("/add"));
        assert!(!is_unknown_command("/add src/main.rs"));
        assert!(
            KNOWN_COMMANDS.contains(&"/add"),
            "/add should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_add_in_help_text() {
        let text = help_text();
        assert!(
            text.contains("/add"),
            "Help text should mention /add command"
        );
    }

    #[test]
    fn test_handle_add_no_args_returns_empty() {
        let results = handle_add("/add");
        assert!(results.is_empty(), "No args should return empty results");
    }

    #[test]
    fn test_handle_add_with_space_no_args_returns_empty() {
        let results = handle_add("/add   ");
        assert!(
            results.is_empty(),
            "Whitespace-only args should return empty"
        );
    }

    #[test]
    fn test_handle_add_real_file() {
        let results = handle_add("/add Cargo.toml");
        assert_eq!(results.len(), 1, "Should return one result for Cargo.toml");
        match &results[0] {
            AddResult::Text { summary, content } => {
                assert!(
                    summary.contains("Cargo.toml"),
                    "Summary should mention the file"
                );
                assert!(
                    content.contains("[package]"),
                    "Content should contain file text"
                );
            }
            _ => panic!("Expected AddResult::Text for Cargo.toml"),
        }
    }

    #[test]
    fn test_handle_add_with_line_range() {
        let results = handle_add("/add Cargo.toml:1-3");
        assert_eq!(results.len(), 1);
        match &results[0] {
            AddResult::Text { summary, content } => {
                assert!(
                    summary.contains("lines 1-3"),
                    "Summary should mention line range"
                );
                assert!(
                    content.contains("```"),
                    "Content should be wrapped in code fence"
                );
            }
            _ => panic!("Expected AddResult::Text for line range"),
        }
    }

    #[test]
    fn test_handle_add_glob_pattern() {
        let results = handle_add("/add src/*.rs");
        assert!(results.len() > 1, "Should match multiple .rs files in src/");
    }

    #[test]
    fn test_handle_add_nonexistent_file() {
        let results = handle_add("/add nonexistent_xyz_file.rs");
        assert!(results.is_empty(), "Nonexistent file should return empty");
    }

    #[test]
    fn test_handle_add_multiple_files() {
        let results = handle_add("/add Cargo.toml LICENSE");
        assert_eq!(results.len(), 2, "Should return results for both files");
    }

    #[test]
    fn test_plan_in_known_commands() {
        assert!(
            KNOWN_COMMANDS.contains(&"/plan"),
            "/plan should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_plan_in_help_text() {
        let help = help_text();
        assert!(help.contains("/plan"), "/plan should appear in help text");
        assert!(
            help.contains("architect"),
            "Help text should mention architect mode"
        );
    }

    #[test]
    fn test_tokens_display_labels() {
        // Verify the /tokens output uses the clarified labels (Issue #189)
        use yoagent::provider::AnthropicProvider;
        use yoagent::Usage;

        let agent = Agent::new(AnthropicProvider)
            .with_system_prompt("test")
            .with_model("test-model")
            .with_api_key("test-key");

        let usage = Usage {
            input: 0,
            output: 0,
            cache_read: 0,
            cache_write: 0,
            total_tokens: 0,
        };

        // Should not panic with zero usage and empty conversation
        handle_tokens(&agent, &usage, "test-model");
    }

    #[test]
    fn test_tokens_display_with_large_values() {
        // Verify no panic with very large token counts
        use yoagent::provider::AnthropicProvider;
        use yoagent::Usage;

        let agent = Agent::new(AnthropicProvider)
            .with_system_prompt("test")
            .with_model("test-model")
            .with_api_key("test-key");

        let usage = Usage {
            input: 10_000_000,
            output: 5_000_000,
            cache_read: 3_000_000,
            cache_write: 1_000_000,
            total_tokens: 19_000_000,
        };

        // Should not panic with very large values
        handle_tokens(&agent, &usage, "test-model");
    }

    #[test]
    fn test_tokens_labels_are_clarified() {
        // Source-level check: the function body should use the clarified labels
        // from Issue #189, not the old confusing ones
        let source = include_str!("commands.rs");
        assert!(
            source.contains("Active context:"),
            "/tokens should use 'Active context:' header"
        );
        assert!(
            source.contains("Session totals (all API calls):"),
            "/tokens should use 'Session totals (all API calls):' header"
        );
        assert!(
            source.contains("session totals below show full usage"),
            "Compaction note should reference session totals"
        );
    }

    #[test]
    fn test_teach_mode_default_off() {
        // Reset to known state (tests may run in any order)
        set_teach_mode(false);
        assert!(!is_teach_mode());
    }

    #[test]
    fn test_teach_mode_toggle() {
        set_teach_mode(false);
        assert!(!is_teach_mode());
        set_teach_mode(true);
        assert!(is_teach_mode());
        set_teach_mode(false);
        assert!(!is_teach_mode());
    }

    #[test]
    fn test_teach_known_command() {
        assert!(KNOWN_COMMANDS.contains(&"/teach"));
    }

    #[test]
    fn test_teach_mode_prompt_not_empty() {
        assert!(!TEACH_MODE_PROMPT.is_empty());
        assert!(TEACH_MODE_PROMPT.contains("TEACH MODE"));
    }

    #[test]
    fn test_teach_in_help_text() {
        let text = crate::help::help_text();
        assert!(
            text.contains("/teach"),
            "help text should list the /teach command"
        );
    }

    #[test]
    fn test_teach_command_help_exists() {
        let help = crate::help::command_help("teach");
        assert!(help.is_some(), "/help teach should have detailed help");
        let help_text = help.unwrap();
        assert!(help_text.contains("teach mode"));
    }

    #[test]
    fn test_teach_short_description_exists() {
        let desc = crate::help::command_short_description("teach");
        assert!(desc.is_some(), "teach should have a short description");
    }

    #[test]
    fn test_mcp_in_known_commands() {
        assert!(
            KNOWN_COMMANDS.contains(&"/mcp"),
            "/mcp should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_mcp_short_description_exists() {
        let desc = crate::help::command_short_description("mcp");
        assert!(desc.is_some(), "mcp should have a short description");
    }

    #[test]
    fn test_handle_mcp_no_servers() {
        // Should not panic with empty server lists
        handle_mcp("/mcp", &[], &[], 0);
        handle_mcp("/mcp list", &[], &[], 0);
        handle_mcp("/mcp help", &[], &[], 0);
    }

    #[test]
    fn test_handle_mcp_with_configs() {
        use crate::cli::McpServerConfig;
        let configs = vec![McpServerConfig {
            name: "filesystem".to_string(),
            command: "npx".to_string(),
            args: vec![
                "-y".to_string(),
                "@modelcontextprotocol/server-filesystem".to_string(),
            ],
            env: vec![],
        }];
        // Should not panic
        handle_mcp("/mcp", &[], &configs, 0);
        handle_mcp("/mcp list", &[], &configs, 1);
    }

    #[test]
    fn test_handle_mcp_unknown_subcommand() {
        // Should not panic on unknown subcommand
        handle_mcp("/mcp foobar", &[], &[], 0);
    }

    // --- Regression: stale "coming soon" string and server-filesystem as
    // --- primary example (Day 40). MCP protocol support shipped on Day 39;
    // --- anything in /mcp help or /mcp list that still says "coming soon"
    // --- is an outright lie to the user, and recommending server-filesystem
    // --- as the first example sends them straight into the collision guard.

    #[test]
    fn test_mcp_help_text_no_coming_soon() {
        let help = mcp_help_text();
        assert!(
            !help.contains("coming soon"),
            "/mcp help must not claim MCP support is 'coming soon' — it shipped Day 39.\nGot:\n{help}"
        );
    }

    #[test]
    fn test_mcp_not_connected_message_no_coming_soon() {
        let msg = mcp_not_connected_message(2);
        assert!(
            !msg.contains("coming soon"),
            "/mcp list 'not connected' message must not say 'coming soon'.\nGot:\n{msg}"
        );
        // Positive assertion: the replacement must actually explain WHY.
        assert!(
            msg.contains("collision") || msg.contains("collide"),
            "not-connected message should mention the collision guard as a likely cause.\nGot:\n{msg}"
        );
    }

    #[test]
    fn test_mcp_help_primary_example_is_not_filesystem() {
        // The help text may still MENTION server-filesystem (annotated with
        // the collision warning), but the primary example — the first
        // [mcp_servers.X] block — must not be filesystem, because the
        // Day 39 collision guard refuses to connect to it.
        let help = mcp_help_text();
        let first_block_start = help
            .find("[mcp_servers.")
            .expect("help text should contain at least one [mcp_servers.X] example");
        // The first example block should not contain "server-filesystem"
        // before the next blank line. Slice from first block to end and
        // look only at the first ~5 lines.
        let tail = &help[first_block_start..];
        let first_block: String = tail.lines().take(5).collect::<Vec<_>>().join("\n");
        assert!(
            !first_block.contains("server-filesystem"),
            "primary /mcp help example must not be server-filesystem \
             (it collides with read_file/write_file and is skipped at startup).\nFirst block:\n{first_block}"
        );
    }

    #[test]
    fn test_mcp_help_mentions_collision_warning() {
        // If we leave server-filesystem in the help text at all, it must
        // be annotated with the collision warning so users know why it
        // won't work.
        let help = mcp_help_text();
        if help.contains("server-filesystem") {
            assert!(
                help.contains("collide") || help.contains("skipped"),
                "if server-filesystem is mentioned in /mcp help it must be \
                 annotated with the collision warning.\nGot:\n{help}"
            );
        }
    }

    #[test]
    fn test_permissions_command_recognized() {
        assert!(!is_unknown_command("/permissions"));
        assert!(
            KNOWN_COMMANDS.contains(&"/permissions"),
            "/permissions should be in KNOWN_COMMANDS"
        );
    }

    #[test]
    fn test_handle_permissions_defaults() {
        // No permissions, no dir restrictions, auto_approve off
        let perms = crate::cli::PermissionConfig::default();
        let dirs = crate::cli::DirectoryRestrictions::default();
        handle_permissions(false, &perms, &dirs);
    }

    #[test]
    fn test_handle_permissions_auto_approve() {
        let perms = crate::cli::PermissionConfig::default();
        let dirs = crate::cli::DirectoryRestrictions::default();
        handle_permissions(true, &perms, &dirs);
    }

    #[test]
    fn test_handle_permissions_with_patterns() {
        let perms = crate::cli::PermissionConfig {
            allow: vec!["cargo *".to_string(), "git *".to_string()],
            deny: vec!["rm -rf *".to_string()],
        };
        let dirs = crate::cli::DirectoryRestrictions::default();
        handle_permissions(false, &perms, &dirs);
    }

    #[test]
    fn test_handle_permissions_with_dir_restrictions() {
        let perms = crate::cli::PermissionConfig::default();
        let dirs = crate::cli::DirectoryRestrictions {
            allow: vec!["/home/user/project".to_string()],
            deny: vec!["/etc".to_string(), "/usr".to_string()],
        };
        handle_permissions(false, &perms, &dirs);
    }

    #[test]
    fn test_handle_permissions_fully_configured() {
        let perms = crate::cli::PermissionConfig {
            allow: vec!["cargo *".to_string()],
            deny: vec!["rm *".to_string()],
        };
        let dirs = crate::cli::DirectoryRestrictions {
            allow: vec!["/project".to_string()],
            deny: vec!["/secret".to_string()],
        };
        handle_permissions(true, &perms, &dirs);
    }
}
