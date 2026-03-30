Title: Wire BedrockProvider in build_agent() and create_model_config() (Issue #223)
Files: src/main.rs
Issue: #223

## Context

The Bedrock setup wizard and CLI metadata already shipped (Day 30 08:20) — `setup.rs` and `cli.rs` have full Bedrock support. But `build_agent()` in `main.rs` routes Bedrock to `OpenAiCompatProvider` (the catch-all `else` branch), which won't work because Bedrock uses a completely different API protocol (ConverseStream with AWS SigV4 signing).

yoagent 0.7.5 already exports `BedrockProvider` at `yoagent::provider::BedrockProvider` and `ApiProtocol::BedrockConverseStream`. This is purely a wiring task — no new functionality, just connecting existing pieces.

**Previous attempt was reverted** because it was too ambitious (touched multiple files, complex credential logic). This attempt is ONLY `main.rs`, minimal changes.

## What to do

### 1. Add `BedrockProvider` import

In the existing import line (around line 67):
```rust
use yoagent::provider::{
    AnthropicProvider, BedrockProvider, GoogleProvider, ModelConfig, OpenAiCompat, OpenAiCompatProvider,
};
```

Also import `ApiProtocol` if not already imported:
```rust
use yoagent::provider::{
    AnthropicProvider, ApiProtocol, BedrockProvider, GoogleProvider, ModelConfig, OpenAiCompat, OpenAiCompatProvider,
};
```

### 2. Add "bedrock" branch in `create_model_config()` (around line 1205, near the minimax branch)

```rust
"bedrock" => {
    let url = base_url
        .unwrap_or("https://bedrock-runtime.us-east-1.amazonaws.com");
    ModelConfig {
        id: model.into(),
        name: model.into(),
        api: ApiProtocol::BedrockConverseStream,
        provider: "bedrock".into(),
        base_url: url.to_string(),
        reasoning: false,
        context_window: 200_000,
        max_tokens: 8192,
        cost: Default::default(),
        headers: std::collections::HashMap::new(),
        compat: None,
    }
}
```

### 3. Add "bedrock" branch in `build_agent()` (around line 1345, after the google branch)

```rust
} else if self.provider == "bedrock" {
    let model_config = create_model_config(&self.provider, &self.model, base_url);
    let context_window = model_config.context_window;
    let agent = Agent::new(BedrockProvider).with_model_config(model_config);
    self.configure_agent(agent, context_window)
}
```

Make sure this goes BEFORE the final `else` (OpenAiCompatProvider) branch.

### 4. Add "bedrock" branch in `build_sub_agent_tool()` (around line 1082)

```rust
"bedrock" => Arc::new(BedrockProvider),
```

Add this alongside the existing "anthropic" and "google" branches.

### 5. Handle Bedrock API key construction from env vars

In `parse_args()` in `cli.rs`, the api_key for bedrock currently comes from `AWS_ACCESS_KEY_ID` alone. But `BedrockProvider` expects `access_key:secret_key[:session_token]` format.

**IMPORTANT**: Do this in `main.rs` only — add a post-processing step in the `main()` function (after `parse_args()` returns, around line 1392-1395) that checks if provider is "bedrock" and the api_key doesn't contain `:` (meaning it came from just AWS_ACCESS_KEY_ID), then constructs the combined key:

```rust
// After parse_args returns and before agent_config is built:
if provider == "bedrock" && !api_key.contains(':') {
    // Combine AWS credentials into the format BedrockProvider expects
    let access_key = api_key.clone(); // This was AWS_ACCESS_KEY_ID
    if let Ok(secret) = std::env::var("AWS_SECRET_ACCESS_KEY") {
        api_key = match std::env::var("AWS_SESSION_TOKEN") {
            Ok(token) if !token.is_empty() => format!("{access_key}:{secret}:{token}"),
            _ => format!("{access_key}:{secret}"),
        };
    }
}
```

Look at where `api_key` is used after `parse_args()` — find the variable and modify it before it goes into `AgentConfig`.

### 6. Tests

Add these tests in the `#[cfg(test)]` module in `main.rs`:

```rust
#[test]
fn test_bedrock_model_config() {
    let config = create_model_config("bedrock", "anthropic.claude-sonnet-4-20250514-v1:0", None);
    assert_eq!(config.provider, "bedrock");
    assert_eq!(config.base_url, "https://bedrock-runtime.us-east-1.amazonaws.com");
    // Verify it uses BedrockConverseStream protocol (not OpenAI)
    assert_eq!(format!("{}", config.api), "bedrock_converse_stream");
}

#[test]
fn test_bedrock_model_config_custom_url() {
    let config = create_model_config(
        "bedrock",
        "anthropic.claude-sonnet-4-20250514-v1:0",
        Some("https://bedrock-runtime.eu-west-1.amazonaws.com"),
    );
    assert_eq!(config.base_url, "https://bedrock-runtime.eu-west-1.amazonaws.com");
}

#[test]
fn test_build_agent_bedrock() {
    let config = AgentConfig {
        model: "anthropic.claude-sonnet-4-20250514-v1:0".into(),
        api_key: "test-access:test-secret".into(),
        provider: "bedrock".into(),
        base_url: Some("https://bedrock-runtime.us-east-1.amazonaws.com".into()),
        skills: Default::default(),
        system_prompt: "test".into(),
        thinking: yoagent::ThinkingLevel::Off,
        max_tokens: None,
        temperature: None,
        max_turns: None,
        auto_approve: false,
        permissions: Default::default(),
        dir_restrictions: Default::default(),
        context_strategy: Default::default(),
        context_window: None,
    };
    let _agent = config.build_agent();
    // If this compiles and runs, BedrockProvider is correctly wired
}
```

**Note on the ApiProtocol Display format**: Check what `BedrockConverseStream` displays as by looking at yoagent's `Display` impl. If it's different from `"bedrock_converse_stream"`, adjust the test assertion. You can check with:
```bash
grep -A2 "BedrockConverseStream" ~/.cargo/registry/src/*/yoagent-*/src/provider/model.rs
```

### 7. No docs changes needed

The CLI help, setup wizard, and docs already mention Bedrock from the Day 30 08:20 session. This task just makes it actually work.

## Verification

```bash
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```

## What NOT to do

- Do NOT modify `cli.rs` or `setup.rs` — they're already done
- Do NOT add complex credential validation — just combine the env vars
- Do NOT add new provider detection logic — `parse_args()` already handles "bedrock"
- Keep it to ONLY `src/main.rs`
