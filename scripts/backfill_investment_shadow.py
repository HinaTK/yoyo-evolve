#!/usr/bin/env python3

import argparse
import json
import pathlib
import re
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from log_investment_shadow import (  # noqa: E402
    DEFAULT_SHADOW_EXIT_RULE,
    DEFAULT_SHADOW_HORIZON_DAYS,
    DEFAULT_SHADOW_RISK_FILTER,
    DEFAULT_SHADOW_STOP_LOSS_PCT,
    build_shadow_log,
    load_json,
)


RANKING_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})(?:-(?P<session>[A-Za-z0-9_]+))?-ranking\.json$")


def ranking_info(path: pathlib.Path) -> dict[str, Any] | None:
    match = RANKING_RE.match(path.name)
    if not match:
        return None
    session = match.group("session") or "close"
    return {"date": match.group("date"), "session": session, "path": path}


def discover_rankings(input_dir: pathlib.Path, limit: int, before_date: str | None = None) -> list[dict[str, Any]]:
    rows = []
    for path in input_dir.glob("*-ranking.json"):
        info = ranking_info(path)
        if not info:
            continue
        if before_date and str(info["date"]) >= before_date:
            continue
        rows.append(info)
    rows.sort(key=lambda row: (str(row["date"]), str(row["session"])), reverse=True)
    return rows[:limit]


def build_replay_logs(
    rankings: list[dict[str, Any]],
    output_dir: pathlib.Path,
    risk_filter: str,
    exit_rule: str,
    stop_loss_pct: float,
    horizon_days: int,
    overwrite: bool = False,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    skipped = []
    for info in rankings:
        date = str(info["date"])
        session = str(info["session"])
        output_path = output_dir / f"{date}-{session}-shadow.json"
        if output_path.exists() and not overwrite:
            skipped.append(str(output_path))
            continue
        ranking_path = pathlib.Path(info["path"])
        ranking = load_json(ranking_path)
        snapshot_path = pathlib.Path(str(ranking.get("snapshot"))) if ranking.get("snapshot") else None
        shadow = build_shadow_log(
            ranking,
            ranking_path=ranking_path,
            snapshot_path=snapshot_path,
            date=date,
            session=session,
            risk_filter=risk_filter,
            exit_rule=exit_rule,
            stop_loss_pct=stop_loss_pct,
            horizon_days=horizon_days,
            evidence_mode="historical_replay",
        )
        output_path.write_text(json.dumps(shadow, indent=2), encoding="utf-8")
        written.append(str(output_path))
    return {
        "requested_count": len(rankings),
        "written_count": len(written),
        "skipped_count": len(skipped),
        "written": written,
        "skipped": skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill shadow-only logs from existing ranking JSON files as historical replay evidence.")
    parser.add_argument("--input-dir", default=str(ROOT / "research" / "rankings"))
    parser.add_argument("--output-dir", default=str(ROOT / "research" / "shadow" / "replay"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--before-date", default=None, help="Only replay rankings before this YYYY-MM-DD date.")
    parser.add_argument("--risk-filter", default=DEFAULT_SHADOW_RISK_FILTER)
    parser.add_argument("--exit-rule", default=DEFAULT_SHADOW_EXIT_RULE)
    parser.add_argument("--stop-loss-pct", type=float, default=DEFAULT_SHADOW_STOP_LOSS_PCT)
    parser.add_argument("--horizon-days", type=int, default=DEFAULT_SHADOW_HORIZON_DAYS)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rankings = discover_rankings(pathlib.Path(args.input_dir), args.limit, args.before_date)
    result = build_replay_logs(rankings, pathlib.Path(args.output_dir), args.risk_filter, args.exit_rule, args.stop_loss_pct, args.horizon_days, args.overwrite)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
