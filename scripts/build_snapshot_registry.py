#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import re
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAPSHOT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(morning|midday|close|historical))?(?:-(radar|trade))?$")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_snapshot(path: pathlib.Path, payload: dict[str, Any]) -> dict[str, str]:
    match = SNAPSHOT_RE.match(path.stem)
    date = str(payload.get("as_of_date") or "unknown")
    session = "close"
    kind = "trade"
    if match:
        date = match.group(1)
        session = match.group(2) or "close"
        kind = match.group(3) or "trade"
    return {"date": date, "session": session, "kind": kind}


def quality_for(payload: dict[str, Any], file_date: str) -> dict[str, Any]:
    items = payload.get("items", [])
    missing_latest_close = sum(1 for item in items if item.get("latest_close") in (None, ""))
    future_quote_date_count = 0
    quote_date_mismatch_count = 0
    invalid_quote_date_count = 0
    parsed_quote_dates = []
    try:
        snapshot_date = dt.date.fromisoformat(file_date)
    except ValueError:
        snapshot_date = None
    for item in items:
        quote_date = item.get("quote_trade_date")
        if not quote_date:
            continue
        if str(quote_date) != file_date:
            quote_date_mismatch_count += 1
        try:
            parsed_quote_date = dt.date.fromisoformat(str(quote_date))
        except ValueError:
            invalid_quote_date_count += 1
            continue
        parsed_quote_dates.append(parsed_quote_date)
        if snapshot_date is not None and parsed_quote_date > snapshot_date:
            future_quote_date_count += 1
    generated_at = payload.get("generated_at")
    freshness = "unknown"
    if generated_at:
        try:
            generated = dt.datetime.fromisoformat(str(generated_at).replace("Z", "+00:00"))
            age_hours = (dt.datetime.now(dt.timezone.utc) - generated).total_seconds() / 3600
            freshness = "fresh" if age_hours <= 36 else "stale"
        except ValueError:
            freshness = "unknown"
    return {
        "item_count": len(items),
        "missing_latest_close": missing_latest_close,
        "date_mismatch": bool(payload.get("as_of_date") and str(payload.get("as_of_date")) != file_date),
        "quote_date_mismatch_count": quote_date_mismatch_count,
        "future_quote_date_count": future_quote_date_count,
        "invalid_quote_date_count": invalid_quote_date_count,
        "max_quote_trade_date": max(parsed_quote_dates).isoformat() if parsed_quote_dates else None,
        "freshness": freshness,
        "has_failures": bool(payload.get("failures")),
    }


def build_registry(snapshot_dir: pathlib.Path) -> dict[str, Any]:
    entries = []
    for path in sorted(snapshot_dir.glob("*.json")):
        if path.name == "registry.json":
            continue
        try:
            payload = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            entries.append({"path": str(path), "error": str(exc), "quality": {"freshness": "unknown"}})
            continue
        classification = classify_snapshot(path, payload)
        entries.append(
            {
                "path": str(path),
                "file": path.name,
                "date": classification["date"],
                "session": classification["session"],
                "snapshot_type": classification["kind"],
                "as_of_date": payload.get("as_of_date"),
                "generated_at": payload.get("generated_at"),
                "quality": quality_for(payload, classification["date"]),
            }
        )

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "snapshot_dir": str(snapshot_dir),
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a registry for investment snapshot files.")
    parser.add_argument("--snapshot-dir", default=str(ROOT / "data" / "snapshots"))
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    snapshot_dir = pathlib.Path(args.snapshot_dir)
    output = pathlib.Path(args.output) if args.output else snapshot_dir / "registry.json"
    registry = build_registry(snapshot_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Wrote snapshot registry: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
