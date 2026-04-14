Title: Multi-provider fork guide
Files: docs/src/guides/fork.md
Issue: #287

## Context

Issue #287 requests that the fork setup guide support selecting a provider other than Anthropic.
Currently `docs/src/guides/fork.md` hardcodes Anthropic as the only option: the secrets table
only lists `ANTHROPIC_API_KEY`, the costs section assumes Claude Opus pricing, and there's no
guidance on choosing or configuring alternative providers.

yoyo supports 12+ providers (see `src/providers.rs` for the full list: anthropic, openai,
google, openrouter, groq, mistral, deepseek, xai, cerebras, together, bedrock, z.ai, custom).
The fork guide should reflect this.

## What to change

### 1. Add a "Choose Your Provider" section after "Edit your agent's identity" (step 2)

Add a new section explaining provider choice with a table of common providers:

| Provider | Env Var | Default Model | Notes |
|----------|---------|---------------|-------|
| Anthropic | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` | Default. Best overall quality. |
| OpenAI | `OPENAI_API_KEY` | `gpt-4o` | GPT-4o series |
| Google | `GOOGLE_API_KEY` | `gemini-2.5-pro` | Gemini models |
| OpenRouter | `OPENROUTER_API_KEY` | `anthropic/claude-sonnet-4-6` | Multi-provider gateway |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` | Very cost-effective |
| Groq | `GROQ_API_KEY` | `llama-3.3-70b-versatile` | Fast inference |

Keep the table focused on the most common/accessible providers. Link to the full provider
docs (`configuration/models.md`) for the complete list.

### 2. Update the secrets table (step 4)

Change from hardcoded `ANTHROPIC_API_KEY` to a generic pattern:

| Secret | Description |
|--------|-------------|
| `<PROVIDER>_API_KEY` | API key for your chosen provider (see table above) |
| `APP_ID` | GitHub App ID |
| `APP_PRIVATE_KEY` | GitHub App private key (PEM) |
| `APP_INSTALLATION_ID` | GitHub App installation ID |

Add a note: "Set the API key secret matching your chosen provider. For example, if using
OpenAI, set `OPENAI_API_KEY`."

### 3. Update the costs section

Replace the Anthropic-specific costs with a more general section:

"Costs vary by provider and model. Anthropic Claude Opus runs ~$3-8 per session.
Cheaper options like DeepSeek or Groq can reduce costs significantly. Set the `MODEL`
and `PROVIDER` environment variables in `.github/workflows/evolve.yml`."

### 4. Update "Change the model" customization section

Add guidance on changing the provider too:
"Set `PROVIDER` and `MODEL` in the workflow environment. For example:
```yaml
env:
  PROVIDER: openai
  MODEL: gpt-4o
```"

### Do NOT modify

- Any source files (this is pure docs)
- Any workflow files
- `IDENTITY.md`, `PERSONALITY.md`, etc.

After changes, verify the markdown renders correctly (no broken tables, links work).
