Title: Add AWS Bedrock provider support (Issue #213)
Files: src/main.rs, src/cli.rs
Issue: #213

## Context

yoagent v0.7.5 already has `BedrockProvider` in `src/provider/bedrock.rs` and exports it via
`yoagent::provider::BedrockProvider`. It uses `ApiProtocol::BedrockConverseStream` and expects:
- `api_key` formatted as `{access_key_id}:{secret_access_key}` (with optional `:{session_token}`)
- `base_url` as the Bedrock endpoint, e.g. `https://bedrock-runtime.us-east-1.amazonaws.com`

This task wires Bedrock into yoyo as a named provider. No new yoagent features needed.

## What to do

### 1. In `src/cli.rs`:

**Add "bedrock" to KNOWN_PROVIDERS** (around line 39):
```rust
pub const KNOWN_PROVIDERS: &[&str] = &[
    "anthropic",
    "openai",
    "google",
    "openrouter",
    "ollama",
    "xai",
    "groq",
    "deepseek",
    "mistral",
    "cerebras",
    "zai",
    "minimax",
    "bedrock",  // <-- add here
    "custom",
];
```

**Add to `provider_api_key_env()`** (around line 1463):
```rust
"bedrock" => Some("AWS_ACCESS_KEY_ID"),
```
Note: Bedrock uses AWS credentials, not a single API key. The env var check ensures we detect
that the user has AWS creds configured. The actual key construction (access_key:secret_key) 
happens at runtime.

**Add to `known_models_for_provider()`** (around line 1519):
```rust
"bedrock" => &[
    "anthropic.claude-sonnet-4-20250514-v1:0",
    "anthropic.claude-haiku-4-5-20250414-v1:0",
    "amazon.nova-pro-v1:0",
    "amazon.nova-lite-v1:0",
],
```

**Add to `default_model_for_provider()`** (around line 1565):
```rust
"bedrock" => "anthropic.claude-sonnet-4-20250514-v1:0".into(),
```

### 2. In `src/main.rs`:

**Import BedrockProvider** — add to the existing yoagent import line (around line 67):
```rust
use yoagent::provider::{
    AnthropicProvider, BedrockProvider, GoogleProvider, ModelConfig, OpenAiCompat, OpenAiCompatProvider,
};
```

**Add Bedrock to `build_sub_agent_tool()` provider match** (around line 1082):
```rust
"bedrock" => Arc::new(BedrockProvider),
```

**Add Bedrock to `create_model_config()`** (around line 1130):
```rust
"bedrock" => {
    let url = base_url
        .unwrap_or("https://bedrock-runtime.us-east-1.amazonaws.com");
    let mut config = ModelConfig {
        id: model.into(),
        name: model.into(),
        api: yoagent::provider::ApiProtocol::BedrockConverseStream,
        provider: "bedrock".into(),
        base_url: url.to_string(),
        reasoning: false,
        context_window: 200_000,
        max_tokens: 8192,
        cost: Default::default(),
        headers: std::collections::HashMap::new(),
        compat: None,
    };
    config
}
```

**Handle Bedrock API key construction in `build_agent()` or `parse_args()`**:
Bedrock expects `api_key` as `access_key:secret_key[:session_token]`. When provider is "bedrock",
construct the api_key from environment variables:
- `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` + optional `AWS_SESSION_TOKEN`
- Format: `{access_key}:{secret_key}` or `{access_key}:{secret_key}:{session_token}`

Find where `api_key` is resolved in `parse_args()` (look for the config/env var resolution logic)
and add a special case for bedrock that combines the AWS env vars into the colon-separated format.

### 3. Tests

Add tests in `src/cli.rs` tests section:
- `test_bedrock_in_known_providers` — verify "bedrock" is in KNOWN_PROVIDERS
- `test_bedrock_provider_api_key_env` — verify returns `AWS_ACCESS_KEY_ID`
- `test_bedrock_default_model` — verify default model

Add test in `src/main.rs` tests section:
- `test_bedrock_model_config` — verify `create_model_config("bedrock", ...)` produces correct ApiProtocol

### 4. Update docs

Update `docs/src/configuration/models.md` if it exists, or add Bedrock to any provider documentation.
Update help text if providers are listed anywhere in `src/help.rs`.

## Verification

```bash
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```
