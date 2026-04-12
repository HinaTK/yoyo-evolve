# Grow Your Own Agent

Fork yoyo-evolve, edit two files, and run your own self-evolving coding agent on GitHub Actions.

## What You Get

A coding agent that:
- Runs on GitHub Actions every ~8 hours
- Reads its own source code, picks improvements, implements them
- Writes a journal of its evolution
- Responds to community issues in its own voice
- Gets smarter over time through a persistent memory system

## Quick Start

### 1. Fork the repo

Fork [yologdev/yoyo-evolve](https://github.com/yologdev/yoyo-evolve) on GitHub.

### 2. Edit your agent's identity

**`IDENTITY.md`** — your agent's constitution: name, mission, goals, and rules.

**`PERSONALITY.md`** — your agent's voice: how it writes, speaks, and expresses itself.

These are the only files you *need* to edit. Everything else auto-detects.

### 3. Create a GitHub App

Your agent needs a GitHub App to commit code and interact with issues.

1. Go to **Settings > Developer settings > GitHub Apps > New GitHub App**
2. Give it your agent's name
3. Set permissions:
   - **Repository > Contents**: Read and write
   - **Repository > Issues**: Read and write
   - **Repository > Discussions**: Read and write (optional, for social features)
4. Install it on your forked repo
5. Note the **App ID**, **Private Key** (generate one), and **Installation ID**
   - Installation ID: visit `https://github.com/settings/installations` and click your app — the ID is in the URL

### 4. Set repo secrets

In your fork, go to **Settings > Secrets and variables > Actions** and add:

#### GitHub App secrets (always required)

| Secret | Description |
|--------|-------------|
| `APP_ID` | GitHub App ID |
| `APP_PRIVATE_KEY` | GitHub App private key (PEM) |
| `APP_INSTALLATION_ID` | GitHub App installation ID |

#### AI provider secret (pick one)

yoyo supports 13+ AI providers. Add the secret for whichever provider you want to use:

| Provider | Secret Name | Example Models |
|----------|-------------|----------------|
| Anthropic | `ANTHROPIC_API_KEY` | `claude-opus-4-6`, `claude-sonnet-4-20250514` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4o`, `gpt-4.1`, `o3`, `o4-mini` |
| Google | `GOOGLE_API_KEY` | `gemini-2.5-pro`, `gemini-2.5-flash` |
| OpenRouter | `OPENROUTER_API_KEY` | Access many models via one key |
| xAI | `XAI_API_KEY` | `grok-3`, `grok-3-mini` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat`, `deepseek-reasoner` |
| Groq | `GROQ_API_KEY` | `llama-3.3-70b-versatile` (fast inference) |
| Mistral | `MISTRAL_API_KEY` | `mistral-large-latest`, `codestral-latest` |
| AWS Bedrock | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` | Claude & Nova on AWS |

The default workflow uses `ANTHROPIC_API_KEY`. If you want a different provider, see [Choose Your Provider](#choose-your-provider) below.

### 5. Choose your provider

The evolution workflow uses Anthropic's Claude by default. To use a different provider:

1. **Add your provider's API key** as a repo secret (see the table above)
2. **Set environment variables** in `.github/workflows/evolve.yml`:

For **Anthropic** (default — no changes needed):
```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

For **OpenAI**:
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  MODEL: gpt-4o
```

For **Google Gemini**:
```yaml
env:
  GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
  MODEL: gemini-2.5-pro
```

For **OpenRouter** (access many models with one key):
```yaml
env:
  OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
  MODEL: anthropic/claude-sonnet-4-20250514
```

yoyo auto-detects the provider from the model name in most cases. Setting `MODEL` is usually enough — but you can also set `PROVIDER` explicitly if needed (e.g., `PROVIDER: openai`).

### 6. Enable the Evolution workflow

Go to **Actions** in your fork and enable the **Evolution** workflow. Your agent will start evolving on its next scheduled run, or trigger it manually with **Run workflow**.

## What Each File Does

| File | Purpose |
|------|---------|
| `IDENTITY.md` | Agent's constitution — name, mission, goals, rules |
| `PERSONALITY.md` | Agent's voice — writing style, personality traits |
| `ECONOMICS.md` | What money/sponsorship means to the agent |
| `journals/JOURNAL.md` | Chronological log of evolution sessions (auto-maintained) |
| `DAY_COUNT` | Tracks the agent's current evolution day |
| `memory/` | Persistent learning system (auto-maintained) |
| `SPONSORS.md` | Sponsor recognition (auto-maintained) |

## Costs

Costs depend on which provider and model you choose:

- **Anthropic Claude Opus** (default): ~$3–8 per session, ~$10–25/day
- **Anthropic Claude Sonnet**: Significantly cheaper than Opus
- **OpenAI GPT-4o**: Comparable to Claude Sonnet
- **Google Gemini 2.5 Pro/Flash**: Competitive pricing, Flash is very cheap
- **DeepSeek**: Very affordable
- **Groq**: Free tier available for smaller models
- **OpenRouter**: Prices vary by model — lets you comparison-shop

The agent runs ~3 sessions per day (8-hour gap between runs). To reduce costs, switch to a cheaper model by setting the `MODEL` environment variable in `.github/workflows/evolve.yml`.

## Customization

### Change the model

Set the `MODEL` environment variable in the workflow. Some examples:

| Model | Provider | Notes |
|-------|----------|-------|
| `claude-opus-4-6` | Anthropic | Default, most capable, most expensive |
| `claude-sonnet-4-20250514` | Anthropic | Good balance of quality and cost |
| `gpt-4o` | OpenAI | Requires `OPENAI_API_KEY` secret |
| `gemini-2.5-pro` | Google | Requires `GOOGLE_API_KEY` secret |
| `anthropic/claude-sonnet-4-20250514` | OpenRouter | Requires `OPENROUTER_API_KEY` secret |
| `deepseek-chat` | DeepSeek | Requires `DEEPSEEK_API_KEY` secret |

Remember to add the matching API key secret when switching providers.

### Change session frequency

Edit the cron schedule in `.github/workflows/evolve.yml`. The default `0 * * * *` (every hour) is gated by an 8-hour gap in the script, so the agent runs ~3 times/day.

### Add custom skills

Create markdown files with YAML frontmatter in the `skills/` directory. The agent loads them automatically via `--skills ./skills`.

### Sponsor system

The sponsor system auto-detects your GitHub Sponsors. No configuration needed — just set up GitHub Sponsors on your account.

## The `/update` Command

The yoyo binary's `/update` command checks for releases from `yologdev/yoyo-evolve`, not your fork. This is expected behavior. As a fork maintainer, rebuild from source after pulling changes:

```bash
cargo build --release
```

In the future, an evolve portal will provide guided setup including custom update targets.

## Optional: Dashboard Notifications

If you have a dashboard repo that accepts repository dispatch events, set a repo variable:

```bash
gh variable set DASHBOARD_REPO --body "your-user/your-dashboard" --repo your-user/your-fork
```

And add the `DASHBOARD_TOKEN` secret with a token that can dispatch to that repo.
