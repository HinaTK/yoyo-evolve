Title: Multi-provider fork guide for Issue #287
Files: docs/src/guides/fork.md
Issue: #287

## What to do

Rewrite the fork guide (`docs/src/guides/fork.md`) to be provider-agnostic instead of Anthropic-first. The issue author (@smeshny) correctly identifies that the guide gives an Anthropic-first impression, but yoyo supports 13+ providers.

### Specific changes to `docs/src/guides/fork.md`:

1. **Secrets table** — Replace the single `ANTHROPIC_API_KEY` row with a table showing per-provider secrets:

   | Provider | Secret Name | Notes |
   |----------|-------------|-------|
   | Anthropic | `ANTHROPIC_API_KEY` | Default provider |
   | OpenAI | `OPENAI_API_KEY` | GPT-4o, GPT-4.1, o3, o4-mini |
   | Google | `GOOGLE_API_KEY` | Gemini 2.5 Pro/Flash |
   | OpenRouter | `OPENROUTER_API_KEY` | Access many models via one key |
   | xAI | `XAI_API_KEY` | Grok-3 |
   | DeepSeek | `DEEPSEEK_API_KEY` | DeepSeek Chat/Reasoner |
   | Groq | `GROQ_API_KEY` | Fast Llama inference |
   | Mistral | `MISTRAL_API_KEY` | Mistral Large, Codestral |
   | AWS Bedrock | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` | Claude & Nova on AWS |

   Keep APP_ID, APP_PRIVATE_KEY, APP_INSTALLATION_ID in the secrets table as they're always needed.

2. **Add a "Choose Your Provider" section** after the secrets table, before "Enable the Evolution workflow". Explain:
   - The evolve.yml workflow uses `ANTHROPIC_API_KEY` by default
   - To use a different provider, fork owners need to:
     a. Add their provider's API key as a repo secret
     b. Set `MODEL` and optionally `PROVIDER` environment variables in `.github/workflows/evolve.yml`
   - Show a brief example of what the env block looks like for OpenAI vs Anthropic
   - Note: yoyo auto-detects the provider from the model name in most cases, but being explicit is clearer

3. **Update the "Change the model" section** to include provider-specific examples:
   - `claude-opus-4-6` (Anthropic, default)
   - `gpt-4o` (OpenAI — also set `OPENAI_API_KEY` secret)
   - `gemini-2.5-pro` (Google)
   - `anthropic/claude-sonnet-4-20250514` (OpenRouter)

4. **Update the Costs section** to note that costs vary by provider — Anthropic's Claude Opus is the most expensive option, and other providers may be significantly cheaper.

### Important constraints:
- Do NOT modify `.github/workflows/evolve.yml` (it's on the do-not-modify list)
- Do NOT modify `scripts/evolve.sh`
- This is docs-only — no Rust code changes
- Keep the guide friendly and concise — forks should feel welcoming, not overwhelming
