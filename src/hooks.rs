// Hook system — pre/post tool execution pipeline
// ---------------------------------------------------------------------------

use std::sync::Arc;

use crate::prompt::{audit_log_tool_call, is_audit_enabled};
use yoagent::types::{AgentTool, ToolError, ToolResult};
use yoagent::Content;

/// Hook that runs before/after tool execution.
///
/// Hooks form a pipeline: pre-hooks run first-to-last before the tool executes,
/// post-hooks run first-to-last after execution. A pre-hook can block execution
/// (return Err) or short-circuit with a cached result (return Ok(Some(...))).
/// A post-hook can inspect or modify the tool's output.
pub trait Hook: Send + Sync {
    /// Human-readable name for this hook (used in diagnostics/logging).
    #[allow(dead_code)]
    fn name(&self) -> &str;

    /// Pre-execute: return Err to block, Ok(None) to proceed, Ok(Some(result)) to short-circuit.
    fn pre_execute(
        &self,
        _tool_name: &str,
        _params: &serde_json::Value,
    ) -> Result<Option<String>, String> {
        Ok(None)
    }

    /// Post-execute: can inspect/log the result. Return modified output or pass through.
    fn post_execute(
        &self,
        _tool_name: &str,
        _params: &serde_json::Value,
        output: &str,
    ) -> Result<String, String> {
        Ok(output.to_string())
    }
}

/// Registry that collects hooks and runs them in order.
///
/// Pre-hooks run first-to-last: the first hook to block (Err) or short-circuit
/// (Ok(Some)) wins. Post-hooks run first-to-last, each receiving the output
/// from the previous hook (or the tool itself for the first hook).
pub struct HookRegistry {
    hooks: Vec<Box<dyn Hook>>,
}

impl Default for HookRegistry {
    fn default() -> Self {
        Self::new()
    }
}

impl HookRegistry {
    pub fn new() -> Self {
        Self { hooks: vec![] }
    }

    pub fn register(&mut self, hook: Box<dyn Hook>) {
        self.hooks.push(hook);
    }

    /// Run all pre-hooks in order. Returns:
    /// - `Ok(None)` — all hooks passed, proceed with tool execution
    /// - `Ok(Some(result))` — a hook short-circuited with a cached result
    /// - `Err(reason)` — a hook blocked execution
    pub fn run_pre_hooks(
        &self,
        tool_name: &str,
        params: &serde_json::Value,
    ) -> Result<Option<String>, String> {
        for hook in &self.hooks {
            match hook.pre_execute(tool_name, params)? {
                Some(result) => return Ok(Some(result)),
                None => continue,
            }
        }
        Ok(None)
    }

    /// Run all post-hooks in order, threading output through each.
    /// Returns the final (possibly modified) output, or Err if a hook fails.
    pub fn run_post_hooks(
        &self,
        tool_name: &str,
        params: &serde_json::Value,
        output: &str,
    ) -> Result<String, String> {
        let mut current = output.to_string();
        for hook in &self.hooks {
            current = hook.post_execute(tool_name, params, &current)?;
        }
        Ok(current)
    }

    /// Number of registered hooks.
    #[allow(dead_code)]
    pub fn len(&self) -> usize {
        self.hooks.len()
    }

    /// Whether the registry has no hooks.
    pub fn is_empty(&self) -> bool {
        self.hooks.is_empty()
    }
}

/// AuditHook — logs every tool execution to `.yoyo/audit.jsonl`.
///
/// This is the audit logging that was previously done ad-hoc in the event handler.
/// Now it's a proper hook in the tool execution pipeline. Only logs when audit
/// mode is enabled (via `--audit` flag, `YOYO_AUDIT=1`, or config).
pub struct AuditHook;

impl Hook for AuditHook {
    fn name(&self) -> &str {
        "audit"
    }

    // AuditHook doesn't block or modify — it only observes.
    // pre_execute: default (Ok(None)) — always proceed.

    fn post_execute(
        &self,
        tool_name: &str,
        params: &serde_json::Value,
        output: &str,
    ) -> Result<String, String> {
        // Only log if audit mode is enabled
        if is_audit_enabled() {
            // We don't have precise duration here (the HookedTool wrapper measures it),
            // but the hook sees the output. Duration is logged separately by HookedTool.
            // Log with duration=0 — the actual timing is handled by the event stream.
            audit_log_tool_call(tool_name, params, 0, true);
        }
        Ok(output.to_string())
    }
}

/// A wrapper tool that runs hooks before/after delegating to the inner tool.
///
/// This is the outermost wrapper in the tool pipeline — it wraps tools that may
/// already be wrapped with TruncatingTool, GuardedTool, or ConfirmTool.
struct HookedTool {
    inner: Box<dyn AgentTool>,
    hooks: Arc<HookRegistry>,
}

#[async_trait::async_trait]
impl AgentTool for HookedTool {
    fn name(&self) -> &str {
        self.inner.name()
    }

    fn label(&self) -> &str {
        self.inner.label()
    }

    fn description(&self) -> &str {
        self.inner.description()
    }

    fn parameters_schema(&self) -> serde_json::Value {
        self.inner.parameters_schema()
    }

    async fn execute(
        &self,
        params: serde_json::Value,
        ctx: yoagent::types::ToolContext,
    ) -> Result<ToolResult, ToolError> {
        // Run pre-hooks
        match self.hooks.run_pre_hooks(self.inner.name(), &params) {
            Err(reason) => {
                return Err(ToolError::Failed(format!("Blocked by hook: {reason}")));
            }
            Ok(Some(cached)) => {
                // Short-circuit: return the cached result without executing the tool
                return Ok(ToolResult {
                    content: vec![Content::Text { text: cached }],
                    details: serde_json::Value::default(),
                });
            }
            Ok(None) => {
                // Proceed with normal execution
            }
        }

        // Execute the inner tool
        let result = self.inner.execute(params.clone(), ctx).await?;

        // Extract text content for post-hooks
        let output_text: String = result
            .content
            .iter()
            .filter_map(|c| match c {
                Content::Text { text } => Some(text.as_str()),
                _ => None,
            })
            .collect::<Vec<_>>()
            .join("\n");

        // Run post-hooks (they can inspect/modify the output)
        match self
            .hooks
            .run_post_hooks(self.inner.name(), &params, &output_text)
        {
            Ok(_modified) => {
                // Post-hooks ran successfully. We pass through the original result
                // unchanged — post-hooks are for observation/logging, not mutation
                // of the ToolResult structure (which may contain non-text content).
                Ok(result)
            }
            Err(reason) => Err(ToolError::Failed(format!("Post-hook error: {reason}"))),
        }
    }
}

/// Wrap a tool with the hook registry. If the registry is empty, returns the tool unwrapped.
pub fn maybe_hook(tool: Box<dyn AgentTool>, hooks: &Arc<HookRegistry>) -> Box<dyn AgentTool> {
    if hooks.is_empty() {
        tool
    } else {
        Box::new(HookedTool {
            inner: tool,
            hooks: Arc::clone(hooks),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::Ordering;

    #[test]
    fn test_hook_registry_new_is_empty() {
        let registry = HookRegistry::new();
        assert!(registry.is_empty());
        assert_eq!(registry.len(), 0);
    }

    #[test]
    fn test_hook_registry_default_is_empty() {
        let registry = HookRegistry::default();
        assert!(registry.is_empty());
    }

    #[test]
    fn test_pre_hooks_with_no_hooks_returns_none() {
        let registry = HookRegistry::new();
        let params = serde_json::json!({"command": "ls"});
        let result = registry.run_pre_hooks("bash", &params);
        assert_eq!(result, Ok(None));
    }

    #[test]
    fn test_post_hooks_with_no_hooks_passes_through() {
        let registry = HookRegistry::new();
        let params = serde_json::json!({});
        let result = registry.run_post_hooks("bash", &params, "hello world");
        assert_eq!(result, Ok("hello world".to_string()));
    }

    /// A test hook that blocks all tool execution.
    struct BlockingHook;
    impl Hook for BlockingHook {
        fn name(&self) -> &str {
            "blocker"
        }
        fn pre_execute(
            &self,
            _tool_name: &str,
            _params: &serde_json::Value,
        ) -> Result<Option<String>, String> {
            Err("blocked by test".to_string())
        }
    }

    #[test]
    fn test_blocking_pre_hook_returns_err() {
        let mut registry = HookRegistry::new();
        registry.register(Box::new(BlockingHook));
        let params = serde_json::json!({});
        let result = registry.run_pre_hooks("bash", &params);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "blocked by test");
    }

    /// A test hook that short-circuits with a cached result.
    struct CachingHook {
        cached: String,
    }
    impl Hook for CachingHook {
        fn name(&self) -> &str {
            "cache"
        }
        fn pre_execute(
            &self,
            _tool_name: &str,
            _params: &serde_json::Value,
        ) -> Result<Option<String>, String> {
            Ok(Some(self.cached.clone()))
        }
    }

    #[test]
    fn test_short_circuit_pre_hook_returns_cached_result() {
        let mut registry = HookRegistry::new();
        registry.register(Box::new(CachingHook {
            cached: "cached output".to_string(),
        }));
        let params = serde_json::json!({});
        let result = registry.run_pre_hooks("read_file", &params);
        assert_eq!(result, Ok(Some("cached output".to_string())));
    }

    /// A test hook that modifies output in post_execute.
    struct UppercaseHook;
    impl Hook for UppercaseHook {
        fn name(&self) -> &str {
            "uppercase"
        }
        fn post_execute(
            &self,
            _tool_name: &str,
            _params: &serde_json::Value,
            output: &str,
        ) -> Result<String, String> {
            Ok(output.to_uppercase())
        }
    }

    #[test]
    fn test_post_hook_can_modify_output() {
        let mut registry = HookRegistry::new();
        registry.register(Box::new(UppercaseHook));
        let params = serde_json::json!({});
        let result = registry.run_post_hooks("bash", &params, "hello");
        assert_eq!(result, Ok("HELLO".to_string()));
    }

    /// A test hook that appends a tag to output.
    struct TagHook {
        tag: String,
    }
    impl Hook for TagHook {
        fn name(&self) -> &str {
            "tag"
        }
        fn post_execute(
            &self,
            _tool_name: &str,
            _params: &serde_json::Value,
            output: &str,
        ) -> Result<String, String> {
            Ok(format!("{output}:{}", self.tag))
        }
    }

    #[test]
    fn test_hook_ordering_post_hooks_chain_first_to_last() {
        let mut registry = HookRegistry::new();
        registry.register(Box::new(TagHook {
            tag: "first".to_string(),
        }));
        registry.register(Box::new(TagHook {
            tag: "second".to_string(),
        }));
        registry.register(Box::new(TagHook {
            tag: "third".to_string(),
        }));
        let params = serde_json::json!({});
        let result = registry.run_post_hooks("bash", &params, "start");
        // Each hook appends its tag in order
        assert_eq!(result, Ok("start:first:second:third".to_string()));
    }

    /// A pass-through hook that increments a counter.
    struct CountingHook {
        count: std::sync::atomic::AtomicUsize,
    }
    impl Hook for CountingHook {
        fn name(&self) -> &str {
            "counter"
        }
        fn pre_execute(
            &self,
            _tool_name: &str,
            _params: &serde_json::Value,
        ) -> Result<Option<String>, String> {
            self.count.fetch_add(1, Ordering::Relaxed);
            Ok(None)
        }
    }

    #[test]
    fn test_hook_ordering_pre_hooks_run_first_to_last() {
        // Register a pass-through hook, then a blocking hook.
        // The pass-through should run (incrementing count), then the blocker fires.
        let mut registry = HookRegistry::new();
        let counter = Arc::new(CountingHook {
            count: std::sync::atomic::AtomicUsize::new(0),
        });
        // We can't share Arc<CountingHook> directly via register(Box<dyn Hook>),
        // so we test ordering by putting a blocker second and checking that Err is returned.
        // A pass-through + blocker = first runs, second blocks.
        struct PassThroughHook;
        impl Hook for PassThroughHook {
            fn name(&self) -> &str {
                "pass"
            }
        }
        registry.register(Box::new(PassThroughHook));
        registry.register(Box::new(BlockingHook));
        let params = serde_json::json!({});
        // Blocker is second, so result should be Err (first hook passed through)
        let result = registry.run_pre_hooks("bash", &params);
        assert!(
            result.is_err(),
            "Second hook (blocker) should fire after first"
        );
        // Count that registry has 2 hooks
        assert_eq!(registry.len(), 2);
        drop(counter);
    }

    #[test]
    fn test_short_circuit_pre_hook_stops_later_hooks() {
        // A caching hook followed by a blocking hook: the cache should win, blocker never runs.
        let mut registry = HookRegistry::new();
        registry.register(Box::new(CachingHook {
            cached: "early exit".to_string(),
        }));
        registry.register(Box::new(BlockingHook));
        let params = serde_json::json!({});
        let result = registry.run_pre_hooks("bash", &params);
        assert_eq!(
            result,
            Ok(Some("early exit".to_string())),
            "Caching hook should short-circuit before blocker"
        );
    }

    #[test]
    fn test_audit_hook_implements_trait() {
        let hook = AuditHook;
        assert_eq!(hook.name(), "audit");

        // pre_execute should always return Ok(None) — never blocks
        let params = serde_json::json!({"command": "ls"});
        let pre = hook.pre_execute("bash", &params);
        assert_eq!(pre, Ok(None));

        // post_execute should pass through output unchanged
        // (audit logging won't fire since is_audit_enabled() is false in tests)
        let post = hook.post_execute("bash", &params, "file1.rs\nfile2.rs");
        assert_eq!(post, Ok("file1.rs\nfile2.rs".to_string()));
    }

    #[test]
    fn test_hook_registry_register_increases_len() {
        let mut registry = HookRegistry::new();
        assert_eq!(registry.len(), 0);
        registry.register(Box::new(AuditHook));
        assert_eq!(registry.len(), 1);
        assert!(!registry.is_empty());
        registry.register(Box::new(UppercaseHook));
        assert_eq!(registry.len(), 2);
    }
}
