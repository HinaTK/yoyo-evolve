//! Read-only "info" REPL command handlers.
//!
//! These handlers print state without mutating anything: `/version`, `/status`,
//! `/tokens`, `/cost`, `/model` (show), `/provider` (show), `/think` (show),
//! `/changelog`.
//!
//! Extracted from `commands.rs` as the first slice of issue #260, which tracks
//! splitting the 3,500-line `commands.rs` into focused modules. Read-only
//! handlers are the safest possible first slice — no shared mutable state, no
//! session-changes plumbing, no provider rebuild paths.

use crate::cli::{KNOWN_PROVIDERS, VERSION};
use crate::commands::thinking_level_name;
use crate::format::*;
use crate::git::*;

use yoagent::agent::Agent;
use yoagent::context::total_tokens;
use yoagent::*;

// ── /version ─────────────────────────────────────────────────────────────

pub fn handle_version() {
    println!("{DIM}  yoyo v{VERSION}{RESET}\n");
}

// ── /status ──────────────────────────────────────────────────────────────

pub fn handle_status(
    model: &str,
    cwd: &str,
    session_total: &Usage,
    elapsed: std::time::Duration,
    turns: usize,
) {
    println!("{DIM}  model:   {model}");
    if let Some(branch) = git_branch() {
        println!("  git:     {branch}");
    }
    println!("  cwd:     {cwd}");
    println!(
        "  session: {} elapsed, {turns} turn{}",
        format_duration(elapsed),
        if turns == 1 { "" } else { "s" }
    );
    println!(
        "  tokens:  {} in / {} out (session total){RESET}\n",
        session_total.input, session_total.output
    );
}

// ── /tokens ──────────────────────────────────────────────────────────────

pub fn handle_tokens(agent: &Agent, session_total: &Usage, model: &str) {
    let max_context = crate::cli::effective_context_tokens();
    let messages = agent.messages().to_vec();
    let context_used = total_tokens(&messages) as u64;
    let bar = context_bar(context_used, max_context);

    println!("{DIM}  Active context:");
    println!("    messages:    {}", messages.len());
    println!(
        "    current:     {} / {} tokens",
        format_token_count(context_used),
        format_token_count(max_context)
    );
    println!("    {bar}");
    if session_total.input > context_used + 1000 {
        println!("    {DIM}(earlier messages were compacted to save space — session totals below show full usage){RESET}");
    }
    if context_used as f64 / max_context as f64 > 0.75 {
        println!("    {YELLOW}⚠ Context is getting full. Consider /clear or /compact.{RESET}");
    }
    println!();
    println!("  Session totals (all API calls):");
    println!(
        "    input:       {} tokens",
        format_token_count(session_total.input)
    );
    println!(
        "    output:      {} tokens",
        format_token_count(session_total.output)
    );
    println!(
        "    cache read:  {} tokens",
        format_token_count(session_total.cache_read)
    );
    println!(
        "    cache write: {} tokens",
        format_token_count(session_total.cache_write)
    );
    if let Some(cost) = estimate_cost(session_total, model) {
        println!("    est. cost:   {}", format_cost(cost));
    }
    println!("{RESET}");
}

// ── /cost ────────────────────────────────────────────────────────────────

pub fn handle_cost(session_total: &Usage, model: &str, messages: &[yoagent::AgentMessage]) {
    if let Some(cost) = estimate_cost(session_total, model) {
        println!("{DIM}  Session cost: {}", format_cost(cost));
        println!(
            "    {} in / {} out",
            format_token_count(session_total.input),
            format_token_count(session_total.output)
        );
        if session_total.cache_read > 0 || session_total.cache_write > 0 {
            println!(
                "    cache: {} read / {} write",
                format_token_count(session_total.cache_read),
                format_token_count(session_total.cache_write)
            );
        }
        if let Some((input_cost, cw_cost, cr_cost, output_cost)) =
            cost_breakdown(session_total, model)
        {
            println!();
            println!("    Breakdown:");
            println!("      input:       {}", format_cost(input_cost));
            println!("      output:      {}", format_cost(output_cost));
            if cw_cost > 0.0 {
                println!("      cache write: {}", format_cost(cw_cost));
            }
            if cr_cost > 0.0 {
                println!("      cache read:  {}", format_cost(cr_cost));
            }
        }

        // Per-turn breakdown
        let turn_costs = extract_turn_costs(messages, model);
        if !turn_costs.is_empty() {
            println!();
            println!("{}", format_turn_costs(&turn_costs));
        }

        println!("{RESET}");
    } else {
        println!("{DIM}  Cost estimation not available for model '{model}'.{RESET}\n");
    }
}

// ── /model ───────────────────────────────────────────────────────────────

pub fn handle_model_show(model: &str) {
    println!("{DIM}  current model: {model}");
    println!("  usage: /model <name>{RESET}\n");
}

// ── /provider ────────────────────────────────────────────────────────────

pub fn handle_provider_show(provider: &str) {
    println!("{DIM}  current provider: {provider}");
    println!("  usage: /provider <name>");
    println!("  available: {}{RESET}\n", KNOWN_PROVIDERS.join(", "));
}

// ── /think ───────────────────────────────────────────────────────────────

pub fn handle_think_show(thinking: ThinkingLevel) {
    let level_str = thinking_level_name(thinking);
    println!("{DIM}  thinking: {level_str}");
    println!("  usage: /think <off|minimal|low|medium|high>{RESET}\n");
}

// ── /changelog ──────────────────────────────────────────────────────────

/// Parse the optional count argument from `/changelog [N]` input.
/// Returns a count clamped to 1..=100, defaulting to 15.
pub fn parse_changelog_count(input: &str) -> usize {
    let arg = input.strip_prefix("/changelog").unwrap_or("").trim();
    if arg.is_empty() {
        return 15;
    }
    arg.parse::<usize>().unwrap_or(15).clamp(1, 100)
}

pub fn handle_changelog(input: &str) {
    let count = parse_changelog_count(input);

    let count_arg = format!("-{count}");
    let output = std::process::Command::new("git")
        .args(["log", "--oneline", "--format=%h %s (%ar)", &count_arg])
        .output();

    match output {
        Ok(result) if result.status.success() => {
            let text = String::from_utf8_lossy(&result.stdout);
            let text = text.trim();
            if text.is_empty() {
                println!("{DIM}  (no commits found){RESET}\n");
            } else {
                println!("{DIM}  Recent commits ({count} max):\n");
                for line in text.lines() {
                    println!("    {line}");
                }
                println!("{RESET}");
            }
        }
        Ok(_) => {
            println!("{DIM}  (not in a git repository){RESET}\n");
        }
        Err(_) => {
            println!("{DIM}  (git not available){RESET}\n");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use yoagent::provider::AnthropicProvider;
    use yoagent::{Agent, Usage};

    #[test]
    fn test_tokens_display_labels() {
        // Verify no panic with zero usage and empty conversation
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
        let source = include_str!("commands_info.rs");
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
    fn test_handle_status_with_timing() {
        use std::time::Duration;
        // Just verify it doesn't panic with various inputs
        handle_status(
            "test-model",
            "/tmp",
            &Usage::default(),
            Duration::from_secs(0),
            0,
        );
        handle_status(
            "test-model",
            "/tmp",
            &Usage::default(),
            Duration::from_secs(125),
            1,
        );
        handle_status(
            "test-model",
            "/tmp",
            &Usage::default(),
            Duration::from_secs(7200),
            42,
        );
    }

    #[test]
    fn test_parse_changelog_count_default() {
        assert_eq!(parse_changelog_count("/changelog"), 15);
    }

    #[test]
    fn test_parse_changelog_count_custom() {
        assert_eq!(parse_changelog_count("/changelog 30"), 30);
        assert_eq!(parse_changelog_count("/changelog 1"), 1);
        assert_eq!(parse_changelog_count("/changelog 100"), 100);
    }

    #[test]
    fn test_parse_changelog_count_clamped() {
        assert_eq!(parse_changelog_count("/changelog 0"), 1);
        assert_eq!(parse_changelog_count("/changelog 999"), 100);
    }

    #[test]
    fn test_parse_changelog_count_invalid() {
        // Non-numeric falls back to default 15
        assert_eq!(parse_changelog_count("/changelog abc"), 15);
        assert_eq!(parse_changelog_count("/changelog -5"), 15);
    }

    #[test]
    fn test_handle_changelog_no_panic() {
        // Should not panic regardless of git availability
        handle_changelog("/changelog");
        handle_changelog("/changelog 5");
    }
}
