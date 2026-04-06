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

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `APP_ID` | GitHub App ID |
| `APP_PRIVATE_KEY` | GitHub App private key (PEM) |
| `APP_INSTALLATION_ID` | GitHub App installation ID |

### 5. Enable the Evolution workflow

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

The agent uses the Anthropic API (Claude Opus by default):
- **~$3-8 per evolution session** depending on task complexity
- **~3 sessions per day** (8-hour gap between runs)
- **~$10-25/day** typical cost

To reduce costs, set the `MODEL` environment variable in `.github/workflows/evolve.yml` to a cheaper model (e.g., `claude-sonnet-4-6`).

## Customization

### Change the model

Set the `MODEL` environment variable in the workflow, or edit the default in `scripts/evolve.sh`.

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
