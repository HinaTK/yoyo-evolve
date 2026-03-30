Title: Add Bedrock to setup wizard
Files: src/setup.rs, src/cli.rs
Issue: #213

## Context

This is the second part of Bedrock provider support. Task 01 adds the core provider wiring
(cli.rs + main.rs). This task adds Bedrock to the interactive setup wizard so new users
can select it during first-run onboarding, and updates the welcome/help text.

## What to do

### 1. In `src/setup.rs`:

**Add Bedrock to WIZARD_PROVIDERS** (around line 13):
Add after "minimax" and before "custom":
```rust
("bedrock", "AWS Bedrock (Claude, Nova — uses AWS credentials)"),
```

**Handle Bedrock-specific wizard flow**:
Look at `run_wizard_interactive()` for how provider-specific behavior works (e.g., "ollama"
skips the API key prompt). For Bedrock, the wizard should:

When `provider == "bedrock"`:
1. Instead of asking "API key:", prompt for:
   - "AWS Access Key ID: " → read as `access_key`
   - "AWS Secret Access Key: " → read as `secret_key`
   - "AWS Region [us-east-1]: " → read with default "us-east-1"
2. Construct: `api_key = format!("{}:{}", access_key, secret_key)`
3. Construct: `base_url = format!("https://bedrock-runtime.{}.amazonaws.com", region)`
4. Set `WizardResult.base_url = Some(base_url)`
5. Continue with model selection as normal

The config file generation (`generate_config_contents()`) already handles base_url — if present
it writes it to the toml.

For the config file, also write a comment about setting env vars:
```toml
# For Bedrock, set: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
# Or pass --api-key "access_key:secret_key"
```

### 2. In `src/cli.rs`:

**Update `get_welcome_text()`** to mention Bedrock as an available provider. Add a line like:
```
  AWS Bedrock: {DIM}yoyo --provider bedrock --base-url https://bedrock-runtime.us-east-1.amazonaws.com{RESET}
```

### 3. Tests

In `src/setup.rs` tests:
- `test_bedrock_in_wizard_providers` — verify "bedrock" appears in WIZARD_PROVIDERS
- Verify `generate_config_contents("bedrock", "anthropic.claude-sonnet-4-20250514-v1:0", Some("https://bedrock-runtime.us-east-1.amazonaws.com"))` produces valid toml

## Verification

```bash
cargo build
cargo test
cargo clippy --all-targets -- -D warnings
```
