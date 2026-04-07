#!/usr/bin/env python3
"""Process sponsor data fetched from the GitHub Sponsors API.

This is the single source of truth for sponsor state. Reads the raw
GraphQL response from /tmp/sponsor_raw.json (written by the caller's
`gh api graphql` invocation) and updates:

  - sponsors/credits.json      — one-time sponsor credit ledger
  - sponsors/active.json       — flat list of currently-active sponsors
  - sponsors/sponsor_info.json — rich per-login dict (committed, read by evolve.sh)
  - sponsors/shoutouts.json    — recurring sponsor shoutout tracker
  - SPONSORS.md                — append-only sponsor wall
  - README.md                  — auto-maintained block between SPONSORS_START/END markers

Side effect: opens GitHub issues for newly-eligible shoutout sponsors
($10+ recurring or $10+ one-time) using `gh issue create`. Requires
`gh` to be authenticated with a token that has `issues: write`.

Stdout: exactly one line `<monthly_cents>|<true|false>` consumed by
callers that want a summary (currently nothing — kept for ad-hoc use).

Stderr: WARNING/ERROR lines.

Exit codes:
  0 — success
  2 — sponsor fetch failed: missing/empty/invalid /tmp/sponsor_raw.json,
      GraphQL errors, unexpected response shape, or truncated results
      (totalCount > len(nodes)). On exit 2 NO files are written, so a
      transient API failure cannot wipe the committed sponsor state.
  3 — an existing state file (credits.json, shoutouts.json) is unreadable
      (corrupt JSON or I/O error). Refuses to overwrite with defaults
      because that would destroy sponsors' run_used flags.
  4 — SPONSORS.md is missing a required section header for a sponsor we
      need to add (e.g. "## 💎 Genesis ($1,200)"). Human must add the
      section before the refresh can proceed.
  5 — README.md is missing, or missing the SPONSORS_START/SPONSORS_END
      markers, or the markers are in the wrong order. This is the exact
      silent-drop class the refactor targets, so it is fatal by design.
  Other non-zero — unhandled exception during file writes (loud).
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

RAW_JSON = "/tmp/sponsor_raw.json"
CREDITS_FILE = "sponsors/credits.json"
SHOUTOUTS_FILE = "sponsors/shoutouts.json"
ACTIVE_FILE = "sponsors/active.json"
SPONSOR_INFO_FILE = "sponsors/sponsor_info.json"
SPONSORS_MD = "SPONSORS.md"
README_MD = "README.md"

README_MARKER_START = "<!-- SPONSORS_START -->"
README_MARKER_END = "<!-- SPONSORS_END -->"

REPO = os.environ.get("REPO", "yologdev/yoyo-evolve")


class FetchFailed(Exception):
    """Raised when the sponsor query failed and no file writes should happen."""


def warn(msg):
    print(f"WARNING: {msg}", file=sys.stderr)


def err(msg):
    print(f"ERROR: {msg}", file=sys.stderr)


def load_raw_nodes(path):
    """Load sponsor nodes from the GraphQL response.

    Raises FetchFailed for any condition that means we don't have
    trustworthy sponsor data — caller must abort before touching
    committed files.
    """
    if not os.path.exists(path):
        raise FetchFailed(f"sponsor raw file missing: {path}")
    if os.path.getsize(path) == 0:
        raise FetchFailed(f"sponsor raw file is empty: {path} (gh likely failed before writing)")

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise FetchFailed(f"sponsor raw file is not valid JSON: {e}")

    if not isinstance(data, dict):
        raise FetchFailed(f"sponsor raw file has unexpected top-level type: {type(data).__name__}")

    if data.get("errors"):
        msgs = "; ".join(str(e.get("message", e)) for e in data["errors"])
        raise FetchFailed(f"GraphQL errors: {msgs}")

    try:
        shipments = data["data"]["viewer"]["sponsorshipsAsMaintainer"]
        nodes = shipments["nodes"] or []
    except (KeyError, TypeError):
        raise FetchFailed("sponsor raw file has unexpected shape (no viewer.sponsorshipsAsMaintainer.nodes)")

    # Pagination guard. The query requests first:100; if totalCount exceeds
    # that we'd silently drop sponsors beyond the first page — the exact
    # silent-data-loss class this refactor exists to kill. Fail loudly
    # instead and force a human to add pagination support.
    total = shipments.get("totalCount")
    if isinstance(total, int) and total > len(nodes):
        raise FetchFailed(
            f"sponsor query truncated: totalCount={total} but only {len(nodes)} "
            f"nodes returned. Add pagination (endCursor/hasNextPage) to the "
            f"GraphQL query in .github/workflows/sponsors-refresh.yml."
        )

    return nodes


def recurring_benefits(monthly_cents):
    dollars = monthly_cents / 100
    b = []
    if dollars >= 5:
        b.append("priority")
    if dollars >= 10:
        b.append("shoutout")
    if dollars >= 25:
        b.append("sponsors_md")
    if dollars >= 50:
        b.append("readme")
    return b


def onetime_benefits(total_cents):
    dollars = total_cents / 100
    b = []
    if dollars >= 5:
        b.append("priority")
    if dollars >= 10:
        b.append("shoutout")
    if dollars >= 20:
        b.append("sponsors_md")
    if dollars >= 50:
        b.append("readme")
    if dollars >= 1200:
        b.append("genesis")
    return b


def split_nodes(nodes):
    """Split GraphQL nodes into recurring map and one-time list."""
    recurring = {}  # login -> monthly_cents
    onetime = []
    monthly_cents = 0

    for n in nodes:
        login = (n.get("sponsorEntity") or {}).get("login", "")
        if not login:
            continue
        cents = (n.get("tier") or {}).get("monthlyPriceInCents", 0)
        if n.get("isOneTimePayment", False):
            onetime.append({"login": login, "cents": cents})
        else:
            recurring[login] = cents
            monthly_cents += cents
    return recurring, onetime, monthly_cents


def load_json_or_default(path, default):
    """Load JSON from path. Missing file → default. Unreadable/corrupt → fatal.

    The "missing" case is fine (first run, fresh checkout). The "unreadable"
    case must NEVER silently overwrite the file with default data — that's how
    you destroy a sponsor's run_used flags.
    """
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        err(f"refusing to overwrite unreadable file {path}: {e}")
        sys.exit(3)


def update_credits(credits, onetime_sponsors, today):
    """Add new one-time sponsors to the ledger and compute benefit_expires."""
    for s in onetime_sponsors:
        login = s["login"]
        if login not in credits:
            credits[login] = {
                "total_cents": s["cents"],
                "run_used": False,
                "first_seen": today,
                "benefit_expires": "",
                "shouted_out": False,
            }

    # Compute benefit_expires for one-time sponsors based on amount
    # (only set once at creation — never overwrite)
    for login, info in credits.items():
        if info.get("benefit_expires", ""):
            continue
        dollars = info.get("total_cents", 0) / 100
        first_seen = info.get("first_seen", today)
        try:
            fs_date = datetime.strptime(first_seen, "%Y-%m-%d")
        except ValueError:
            fs_date = datetime.now(timezone.utc)
        if dollars >= 1200:
            info["benefit_expires"] = "never"
        elif dollars >= 50:
            info["benefit_expires"] = (fs_date + timedelta(days=60)).strftime("%Y-%m-%d")
        elif dollars >= 10:
            info["benefit_expires"] = (fs_date + timedelta(days=30)).strftime("%Y-%m-%d")
        elif dollars >= 5:
            info["benefit_expires"] = (fs_date + timedelta(days=14)).strftime("%Y-%m-%d")

    # Expire credit entries older than 90 days, except Genesis sponsors.
    # Any row lacking first_seen (legacy data, partial write) is KEPT —
    # empty-string compare against the cutoff would evaluate False and
    # silently drop the row, which is a data-loss path we refuse to take.
    cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
    return {
        k: v
        for k, v in credits.items()
        if v.get("benefit_expires") == "never"
        or (v.get("first_seen") or today) >= cutoff
    }


def build_sponsor_info(recurring, credits, shoutouts, today):
    """Merge recurring + one-time data into a unified per-login dict."""
    sponsor_info = {}

    for login, cents in recurring.items():
        sponsor_info[login] = {
            "type": "recurring",
            "monthly_cents": cents,
            "benefits": recurring_benefits(cents),
            "shouted_out": shoutouts.get(login, False),
        }

    for login, info in credits.items():
        dollars = info.get("total_cents", 0) / 100
        benefit_expires = info.get("benefit_expires", "")
        active = True
        if benefit_expires and benefit_expires != "never" and benefit_expires < today:
            active = False
        benefits = onetime_benefits(info.get("total_cents", 0)) if (active and dollars >= 5) else []
        entry = {
            "type": "onetime",
            "total_cents": info.get("total_cents", 0),
            "benefits": benefits,
            "benefit_expires": benefit_expires,
            "shouted_out": info.get("shouted_out", False),
            "run_used": info.get("run_used", False),
        }
        if login in sponsor_info:
            # Recurring takes precedence; nest the one-time entry under it
            sponsor_info[login]["onetime"] = entry
        else:
            sponsor_info[login] = entry

    return sponsor_info


def update_sponsors_md(sponsor_info, path=SPONSORS_MD):
    """Append-only update of SPONSORS.md. Returns True if file changed.

    Missing section header is fatal — silently dropping a sponsor is the
    exact bug class this refactor exists to eliminate.
    """
    if os.path.exists(path):
        with open(path) as f:
            existing = f.read()
    else:
        existing = ""

    def already_listed(login):
        return f"@{login}" in existing

    new_lines = {}  # section_header -> list of entry strings
    for login, info in sponsor_info.items():
        if already_listed(login):
            continue
        if info.get("type") == "recurring":
            dollars = info.get("monthly_cents", 0) // 100
            if dollars >= 50:
                section = "## 🦈 Patron ($50+/mo)"
                new_lines.setdefault(section, []).append(f"- @{login} — ${dollars}/mo")
            elif dollars >= 25:
                section = "## 🦑 Boost ($25+/mo)"
                new_lines.setdefault(section, []).append(f"- @{login} — ${dollars}/mo")
        else:
            dollars = info.get("total_cents", 0) // 100
            benefits = info.get("benefits", [])
            if "genesis" in benefits:
                section = "## 💎 Genesis ($1,200)"
                new_lines.setdefault(section, []).append(f"- @{login} — ${dollars:,}")
            elif dollars >= 50:
                section = "## 🚀 Rocket Fuel ($50+)"
                new_lines.setdefault(section, []).append(f"- @{login} — ${dollars}")
            elif "sponsors_md" in benefits:
                section = "## 🧬 Evolution Boost ($20+)"
                new_lines.setdefault(section, []).append(f"- @{login} — ${dollars}")

    if not new_lines:
        return False

    lines = existing.split("\n")
    missing_sections = []
    for section, entries in new_lines.items():
        try:
            idx = lines.index(section)
            for entry in reversed(entries):
                lines.insert(idx + 1, entry)
        except ValueError:
            missing_sections.append((section, len(entries)))

    if missing_sections:
        for section, n in missing_sections:
            err(f"section '{section}' not found in {path} — {n} sponsor(s) cannot be added")
        sys.exit(4)

    _atomic_write_text(path, "\n".join(lines))
    print(f"  Updated {path}.")
    return True


def render_readme_block(sponsor_info):
    """Render the auto-maintained sponsors block for README.md.

    Only sponsors with the 'readme' or 'genesis' benefit appear here.
    Returns the full block including START/END markers.
    """
    genesis = []
    patrons = []  # $50+/mo recurring or $50+ one-time with active readme benefit

    for login, info in sponsor_info.items():
        benefits = info.get("benefits", [])
        if "genesis" in benefits:
            dollars = info.get("total_cents", 0) // 100
            genesis.append((login, dollars))
        elif "readme" in benefits:
            if info.get("type") == "recurring":
                dollars = info.get("monthly_cents", 0) // 100
                patrons.append((login, f"${dollars}/mo"))
            else:
                dollars = info.get("total_cents", 0) // 100
                patrons.append((login, f"${dollars}"))

    lines = [README_MARKER_START]
    lines.append("<!-- This block is auto-maintained by scripts/refresh_sponsors.py — do not edit by hand. -->")
    lines.append("")

    if not genesis and not patrons:
        lines.append("_No top-tier sponsors yet. Be the first — [sponsor yoyo](https://github.com/sponsors/yologdev)._")
    else:
        if genesis:
            lines.append("**💎 Genesis Sponsors:**")
            lines.append("")
            for login, dollars in sorted(genesis):
                lines.append(f"- [@{login}](https://github.com/{login}) — ${dollars:,}")
            lines.append("")
        if patrons:
            lines.append("**🚀 Patron Sponsors ($50+):**")
            lines.append("")
            for login, amount in sorted(patrons):
                lines.append(f"- [@{login}](https://github.com/{login}) — {amount}")
            lines.append("")

    lines.append(README_MARKER_END)
    return "\n".join(lines)


def update_readme(sponsor_info, path=README_MD):
    """Replace the SPONSORS_START..SPONSORS_END block in README.

    Missing/malformed markers are FATAL (exit 5). This is the exact
    silent-failure class the refactor exists to kill: if a maintainer
    restructures README and accidentally drops the markers, top-tier
    sponsors would silently vanish from README forever. We'd rather
    fail the hourly job loudly and force a human to notice.

    Missing README file (first-run / fresh checkout) is also fatal,
    since this script is the single source of truth for that file.
    """
    if not os.path.exists(path):
        err(f"{path} not found — README.md must exist with SPONSORS_START/END markers")
        sys.exit(5)

    with open(path) as f:
        content = f.read()
    start_idx = content.find(README_MARKER_START)
    end_idx = content.find(README_MARKER_END)

    if start_idx == -1 or end_idx == -1:
        err(
            f"{path} is missing {README_MARKER_START} or {README_MARKER_END} — "
            f"refusing to silently drop sponsors from README"
        )
        sys.exit(5)
    if end_idx < start_idx:
        err(f"{path} markers are in the wrong order — refusing to update")
        sys.exit(5)

    new_block = render_readme_block(sponsor_info)
    end_of_end_marker = end_idx + len(README_MARKER_END)
    new_content = content[:start_idx] + new_block + content[end_of_end_marker:]

    if new_content == content:
        return False

    _atomic_write_text(path, new_content)
    print(f"  Updated {path} sponsor block.")
    return True


def write_active_json(sponsor_info, path=ACTIVE_FILE):
    """Persist a flat list of active sponsors. Write failures are fatal."""
    active = []
    for login, info in sponsor_info.items():
        benefits = info.get("benefits", [])
        if "priority" not in benefits and "genesis" not in benefits:
            continue  # Not active — expired or too small
        if info.get("type") == "recurring":
            dollars = info.get("monthly_cents", 0) // 100
            active.append({"login": login, "amount": f"${dollars}/mo", "type": "recurring"})
        else:
            dollars = info.get("total_cents", 0) // 100
            if "genesis" in benefits:
                active.append({"login": login, "amount": f"${dollars:,}", "type": "genesis"})
            else:
                active.append({"login": login, "amount": f"${dollars}", "type": "onetime"})
    _atomic_write_text(path, json.dumps(active, indent=2))
    return active


def create_shoutout_issues(sponsor_info, credits, shoutouts):
    """Open GitHub issues for newly-eligible shoutout sponsors.

    Eligibility: $10+/mo recurring OR $10+ one-time, NOT yet shouted out.
    Dedup: query existing issues with `Shoutout: @login` in title before
    creating. On any subprocess failure, warn and continue (this is a
    side effect — don't take down the whole refresh job over a flaky API).

    Mutates `credits` and `shoutouts` in-place when an issue is created
    (or when an existing one is found). Caller is responsible for
    persisting them.
    """
    if not _gh_available():
        warn("gh CLI not available — skipping shoutout issue creation")
        return

    for login, info in sponsor_info.items():
        if "shoutout" not in info.get("benefits", []):
            continue
        if info.get("shouted_out", False):
            continue

        # Dedup against existing issues
        try:
            result = subprocess.run(
                ["gh", "issue", "list", "--repo", REPO, "--state", "all",
                 "--search", f'"Shoutout: @{login}" in:title',
                 "--json", "number", "--jq", "length"],
                capture_output=True, text=True, timeout=15,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            warn(f"could not check shoutouts for @{login}: {e}")
            continue

        if result.returncode != 0:
            warn(f"could not check shoutouts for @{login}: {result.stderr.strip()}")
            continue
        if result.stdout.strip() not in ("", "0"):
            # Already exists — mark as shouted out so we don't query again
            _mark_shouted_out(login, info, credits, shoutouts)
            continue

        # Compose title and body
        if info.get("type") == "recurring":
            dollars = info.get("monthly_cents", 0) // 100
            amount_str = f"${dollars}/mo"
        else:
            dollars = info.get("total_cents", 0) // 100
            amount_str = f"${dollars}"

        title = f"Shoutout: @{login} — {amount_str} sponsor"
        body = (
            f"Thank you @{login} for sponsoring yoyo! 🐙💖\n\n"
            f"Tier: {amount_str}\n\n"
            f"Your support helps keep yoyo evolving."
        )

        try:
            result = subprocess.run(
                ["gh", "issue", "create", "--repo", REPO,
                 "--title", title, "--label", "shoutout", "--body", body],
                capture_output=True, text=True, timeout=15,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            warn(f"failed to create shoutout for @{login}: {e}")
            continue

        if result.returncode != 0:
            warn(f"failed to create shoutout for @{login}: {result.stderr.strip()}")
            continue

        print(f"  Created shoutout issue for @{login}")
        _mark_shouted_out(login, info, credits, shoutouts)


def _gh_available():
    try:
        subprocess.run(["gh", "--version"], capture_output=True, timeout=5, check=True)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _mark_shouted_out(login, info, credits, shoutouts):
    """Mutate the right ledger so we don't shout out the same sponsor twice."""
    if info.get("type") == "recurring":
        shoutouts[login] = True
    elif login in credits:
        credits[login]["shouted_out"] = True


def _atomic_write_text(path, text):
    """Write `text` to `path` atomically via tempfile + os.replace.

    A crash mid-write leaves the tempfile behind (which we'd rather leak
    than corrupt the target) but never leaves `path` truncated. The
    target file either has the old content or the full new content —
    never a half-written JSON blob that the next run would silently
    treat as an empty file.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def write_json(path, data):
    """Atomic JSON write. See _atomic_write_text."""
    _atomic_write_text(path, json.dumps(data, indent=2))


def main():
    # Phase 1: fetch + validate. Any failure raises FetchFailed and we
    # exit BEFORE touching any committed file.
    try:
        nodes = load_raw_nodes(RAW_JSON)
    except FetchFailed as e:
        err(f"sponsor fetch failed — refusing to update committed files: {e}")
        sys.exit(2)

    recurring, onetime_sponsors, monthly_cents = split_nodes(nodes)

    # Phase 2: load existing state (missing files OK, unreadable files fatal)
    credits = load_json_or_default(CREDITS_FILE, {})
    shoutouts = load_json_or_default(SHOUTOUTS_FILE, {})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    credits = update_credits(credits, onetime_sponsors, today)
    sponsor_info = build_sponsor_info(recurring, credits, shoutouts, today)

    # Phase 3: side effects (issue creation) — mutates shoutouts/credits
    # in-place. Side-effect failures warn but don't abort.
    create_shoutout_issues(sponsor_info, credits, shoutouts)

    # Rebuild sponsor_info after shoutout mutations so the dump reflects
    # current shouted_out flags
    sponsor_info = build_sponsor_info(recurring, credits, shoutouts, today)

    # Phase 4: write all files. Any unhandled write error here propagates
    # as a non-zero exit (loud) — we never silently continue past a
    # failed write.
    #
    # Write order matters: listings (SPONSORS.md, README.md, active.json,
    # sponsor_info.json) happen BEFORE the mutation ledgers (credits.json,
    # shoutouts.json). Rationale: if a listing write fails, we abort
    # without persisting the in-memory mutations from create_shoutout_issues.
    # The next run will then re-load the on-disk ledger, re-derive the
    # same sponsor_info, and re-attempt shoutout creation — which hits the
    # dedup path (existing issue found) and self-heals. If we persisted
    # the ledger first and then failed on a listing, the ledger would
    # claim shouted_out=true while the listing never got updated.
    update_sponsors_md(sponsor_info)
    update_readme(sponsor_info)
    write_active_json(sponsor_info)
    write_json(SPONSOR_INFO_FILE, sponsor_info)
    write_json(CREDITS_FILE, credits)
    write_json(SHOUTOUTS_FILE, shoutouts)

    onetime_with_run = [
        login
        for login, info in credits.items()
        if info.get("total_cents", 0) >= 200 and not info.get("run_used", False)
    ]
    has_credits = "true" if onetime_with_run else "false"
    print(f"{monthly_cents}|{has_credits}")


if __name__ == "__main__":
    main()
