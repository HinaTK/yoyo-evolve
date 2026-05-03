#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
from collections import Counter, defaultdict
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluation_inputs(latest_json: pathlib.Path, records_json: pathlib.Path | None, evaluations_dir: pathlib.Path) -> list[dict[str, Any]]:
    inputs = []
    if latest_json.exists():
        inputs.append(load_json(latest_json))
    if records_json and records_json.exists():
        inputs.append(load_json(records_json))
    if inputs:
        return inputs
    if not evaluations_dir.exists():
        return []
    for path in sorted(evaluations_dir.glob("*.json")):
        if path.name == "symbol_risk_memory.json":
            continue
        try:
            inputs.append(load_json(path))
        except json.JSONDecodeError:
            continue
    return inputs


def symbol_from_record(record: dict[str, Any]) -> str | None:
    symbol = record.get("symbol")
    return str(symbol) if symbol else None


def add_reason(symbols: dict[str, dict[str, Any]], symbol: str, tag: str, reason: str) -> None:
    row = symbols.setdefault(symbol, {"tags": [], "reasons": [], "action_veto": False})
    if tag not in row["tags"]:
        row["tags"].append(tag)
    if reason not in row["reasons"]:
        row["reasons"].append(reason)
    row["action_veto"] = True


def build_memory(inputs: list[dict[str, Any]], as_of_date: str) -> dict[str, Any]:
    symbols: dict[str, dict[str, Any]] = {}
    selection_error_counts: Counter[str] = Counter()
    complete_records = False

    for data in inputs:
        records = data.get("records")
        if isinstance(records, list):
            complete_records = True
            per_symbol_records: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for record in records:
                symbol = symbol_from_record(record)
                if symbol:
                    per_symbol_records[symbol].append(record)
            for symbol, symbol_records in per_symbol_records.items():
                decisive = [record for record in symbol_records if record.get("verdict") in {"pass", "fail"}]
                pass_count = sum(1 for record in decisive if record.get("verdict") == "pass")
                avg_return = sum(float(record.get("return_pct") or 0.0) for record in symbol_records) / len(symbol_records)
                if len(decisive) >= 3 and pass_count / len(decisive) < 0.25:
                    add_reason(symbols, symbol, "low_symbol_pass_rate", f"records_pass_rate={pass_count / len(decisive):.3f} over {len(decisive)} decisive records")
                if len(symbol_records) >= 3 and avg_return < 0.0:
                    add_reason(symbols, symbol, "negative_symbol_avg_return", f"records_avg_return_pct={avg_return:.3f} over {len(symbol_records)} records")
                if any(float(record.get("return_pct") or 0.0) <= -8.0 for record in symbol_records):
                    add_reason(symbols, symbol, "recent_symbol_adverse_breach", "record return breached -8.0% adverse threshold")
                if sum(1 for record in symbol_records if record.get("learning_tag") == "symbol_selection_error") >= 1:
                    add_reason(symbols, symbol, "repeated_symbol_selection_error", "records include symbol_selection_error")
        for symbol, stats in (data.get("symbol_stats") or {}).items():
            samples = int(stats.get("samples") or 0)
            pass_rate = stats.get("pass_rate")
            avg_return = stats.get("avg_return_pct")
            if samples <= 0:
                continue
            if pass_rate is not None and float(pass_rate) < 0.25:
                add_reason(
                    symbols,
                    str(symbol),
                    "low_symbol_pass_rate",
                    f"pass_rate={float(pass_rate):.3f} over {samples} evaluated calls",
                )
            if avg_return is not None and float(avg_return) < 0.0:
                add_reason(
                    symbols,
                    str(symbol),
                    "negative_symbol_avg_return",
                    f"avg_return_pct={float(avg_return):.3f} over {samples} evaluated calls",
                )

        for record in data.get("recent_misfires") or []:
            symbol = symbol_from_record(record)
            if not symbol:
                continue
            return_pct = record.get("return_pct")
            if return_pct is None or float(return_pct) <= -1.0:
                add_reason(
                    symbols,
                    symbol,
                    "recent_symbol_adverse_breach",
                    f"recent misfire on {record.get('call_date')} returned {return_pct}%",
                )

        for record in data.get("recent_selection_errors") or []:
            symbol = symbol_from_record(record)
            if symbol:
                selection_error_counts[symbol] += 1

    for symbol, count in selection_error_counts.items():
        if count >= 1:
            add_reason(
                symbols,
                symbol,
                "repeated_symbol_selection_error",
                f"recent symbol-selection errors={count}",
            )

    return {
        "metadata": {
            "generated_at": utc_now(),
            "as_of_date": as_of_date,
            "as_of_limited": not complete_records,
            "source_count": len(inputs),
            "method": "summary_symbol_stats_recent_errors_mvp" if not complete_records else "records_plus_summary_mvp",
        },
        "symbols": dict(sorted(symbols.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build as-of symbol risk memory from investment evaluation summaries.")
    parser.add_argument("--latest-json", default=str(ROOT / "research" / "evaluations" / "latest.json"))
    parser.add_argument("--records-json", default=str(ROOT / "research" / "evaluations" / "latest_records.json"))
    parser.add_argument("--evaluations-dir", default=str(ROOT / "research" / "evaluations"))
    parser.add_argument("--output", default=str(ROOT / "research" / "experiments" / "symbol_risk_memory.json"))
    parser.add_argument("--as-of-date", required=True)
    args = parser.parse_args()

    inputs = evaluation_inputs(pathlib.Path(args.latest_json), pathlib.Path(args.records_json), pathlib.Path(args.evaluations_dir))
    result = build_memory(inputs, args.as_of_date)
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote symbol risk memory: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
