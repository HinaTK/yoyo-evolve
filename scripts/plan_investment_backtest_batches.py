#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import re
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAPSHOT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})$")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def available_close_dates(snapshot_dir: pathlib.Path) -> list[str]:
    dates = []
    for path in sorted(snapshot_dir.glob("*.json")):
        match = SNAPSHOT_RE.match(path.stem)
        if match:
            dates.append(match.group(1))
    return dates


def chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def build_plan(snapshot_dir: pathlib.Path, days: int, batch_count: int) -> dict[str, Any]:
    dates = available_close_dates(snapshot_dir)[-days:]
    batch_size = max(1, (days + batch_count - 1) // batch_count)
    batches = []
    for index, batch_dates in enumerate(chunked(dates, batch_size), start=1):
        batches.append(
            {
                "batch_index": index,
                "date_count": len(batch_dates),
                "start_date": batch_dates[0] if batch_dates else None,
                "end_date": batch_dates[-1] if batch_dates else None,
                "dates": batch_dates,
                "status": "pending",
            }
        )
    return {
        "generated_at": utc_now(),
        "requested_days": days,
        "requested_batch_count": batch_count,
        "available_date_count": len(dates),
        "snapshot_dir": str(snapshot_dir),
        "batches": batches,
        "notes": [
            "Run one batch only after user confirmation.",
            "If available_date_count is below requested_days, backfill snapshots before executing batches.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan 90-day investment historical backtest batches.")
    parser.add_argument("--snapshot-dir", default=str(ROOT / "data" / "snapshots"))
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--batch-count", type=int, default=9)
    parser.add_argument("--output", default=str(ROOT / "research" / "experiments" / "historical_batches" / "plan.json"))
    args = parser.parse_args()

    plan = build_plan(pathlib.Path(args.snapshot_dir), args.days, args.batch_count)
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"Wrote historical batch plan: {output}")
    print(f"Available dates: {plan['available_date_count']} / requested {plan['requested_days']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
