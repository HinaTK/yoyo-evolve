#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
from collections import Counter, defaultdict
from typing import Any


BULLISH_STATES = {"buy_candidate", "accumulate", "hold"}
BEARISH_STATES = {"trim", "sell_candidate", "avoid"}
NEUTRAL_STATES = {"watch_only"}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(text: str) -> dt.date:
    return dt.date.fromisoformat(text)


def available_snapshots(snapshot_dir: pathlib.Path) -> dict[dt.date, pathlib.Path]:
    out = {}
    for path in sorted(snapshot_dir.glob("*.json")):
        try:
            out[parse_date(path.stem)] = path
        except ValueError:
            continue
    return out


def snapshot_price(snapshot: dict[str, Any], symbol: str) -> float | None:
    for item in snapshot.get("items", []):
        if item.get("symbol") == symbol:
            return float(item["latest_close"])
    return None


def verdict_for_state(state: str, return_pct: float) -> str:
    if state in BULLISH_STATES:
        if return_pct > 0.5:
            return "pass"
        if return_pct < -0.5:
            return "fail"
        return "mixed"
    if state in BEARISH_STATES:
        if return_pct < -0.5:
            return "pass"
        if return_pct > 0.5:
            return "fail"
        return "mixed"
    return "informational"


def classify_learning(call: dict[str, Any], return_pct: float, verdict: str) -> str | None:
    confidence = float(call.get("confidence", 0.0))
    state = call.get("state")
    if verdict == "fail" and confidence >= 0.7:
        return "overconfidence"
    if verdict == "pass" and confidence <= 0.4:
        return "underconfidence"
    if verdict == "fail" and state in BULLISH_STATES:
        return "bullish_misread"
    if verdict == "fail" and state in BEARISH_STATES:
        return "defensive_misread"
    if verdict == "mixed" and abs(return_pct) < 1.0:
        return "timing_unclear"
    return None


def evaluate_calls(calls_dir: pathlib.Path, snapshot_dir: pathlib.Path, windows: list[int]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    snapshot_paths = available_snapshots(snapshot_dir)
    snapshots = {day: load_json(path) for day, path in snapshot_paths.items()}
    evaluations: list[dict[str, Any]] = []
    verdict_counts = Counter()
    learning_counts = Counter()
    symbol_stats = defaultdict(list)

    for call_path in sorted(calls_dir.glob("*-calls.json")):
        payload = load_json(call_path)
        call_date = parse_date(payload["date"])
        base_snapshot = snapshots.get(call_date)
        if base_snapshot is None:
            continue

        for rec in payload.get("recommendations", []):
            symbol = rec["symbol"]
            base_price = snapshot_price(base_snapshot, symbol)
            if base_price is None:
                continue

            for window in windows:
                future_snapshot = snapshots.get(call_date + dt.timedelta(days=window))
                if future_snapshot is None:
                    continue
                future_price = snapshot_price(future_snapshot, symbol)
                if future_price is None:
                    continue

                return_pct = ((future_price / base_price) - 1.0) * 100.0
                verdict = verdict_for_state(rec["state"], return_pct)
                learning = classify_learning(rec, return_pct, verdict)
                record = {
                    "call_date": payload["date"],
                    "window_days": window,
                    "symbol": symbol,
                    "state": rec["state"],
                    "confidence": rec.get("confidence"),
                    "base_price": round(base_price, 4),
                    "future_price": round(future_price, 4),
                    "return_pct": round(return_pct, 3),
                    "verdict": verdict,
                    "learning_tag": learning,
                }
                evaluations.append(record)
                verdict_counts[verdict] += 1
                if learning:
                    learning_counts[learning] += 1
                symbol_stats[symbol].append(record)

    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "evaluations": len(evaluations),
        "verdict_counts": dict(verdict_counts),
        "learning_counts": dict(learning_counts),
        "symbol_stats": {
            symbol: {
                "samples": len(records),
                "avg_return_pct": round(sum(item["return_pct"] for item in records) / len(records), 3),
                "pass_rate": round(sum(1 for item in records if item["verdict"] == "pass") / len(records), 3),
            }
            for symbol, records in symbol_stats.items()
        },
        "top_learning_candidates": [tag for tag, _count in learning_counts.most_common(5)],
        "recent_misfires": [item for item in evaluations[-10:] if item["verdict"] == "fail"],
    }
    return evaluations, summary


def write_markdown(summary_path: pathlib.Path, summary: dict[str, Any], evaluations: list[dict[str, Any]]) -> None:
    lines = [
        "# Posterior Evaluation Summary",
        "",
        f"Generated: `{summary['generated_at']}`",
        f"Evaluations: `{summary['evaluations']}`",
        "",
        "## Verdict Counts",
    ]
    for key, value in sorted(summary["verdict_counts"].items()):
        lines.append(f"- `{key}`: {value}")

    lines.extend(["", "## Learning Candidates"])
    if summary["learning_counts"]:
        for key, value in sorted(summary["learning_counts"].items(), key=lambda item: item[1], reverse=True):
            lines.append(f"- `{key}`: {value}")
    else:
        lines.append("- No repeated learning candidates yet.")

    lines.extend(["", "## Symbol Stats"])
    if summary["symbol_stats"]:
        for symbol, stats in sorted(summary["symbol_stats"].items()):
            lines.append(
                f"- `{symbol}`: samples={stats['samples']}, avg_return={stats['avg_return_pct']}%, pass_rate={stats['pass_rate']}"
            )
    else:
        lines.append("- No mature calls available for evaluation yet.")

    lines.extend(["", "## Recent Misfires"])
    if summary["recent_misfires"]:
        for item in summary["recent_misfires"]:
            lines.append(
                f"- `{item['call_date']}` `{item['symbol']}` `{item['state']}` over T+{item['window_days']}: {item['return_pct']}%"
            )
    else:
        lines.append("- No failed calls in the most recent evaluated set.")

    lines.extend(["", "## Recent Evaluations"])
    for item in evaluations[-15:]:
        lines.append(
            f"- `{item['call_date']}` `{item['symbol']}` `{item['state']}` T+{item['window_days']}: {item['return_pct']}% -> `{item['verdict']}`"
        )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate historical investment calls against later snapshots.")
    parser.add_argument("--calls-dir", default="research/calls")
    parser.add_argument("--snapshot-dir", default="data/snapshots")
    parser.add_argument("--summary-md", default="research/evaluations/latest.md")
    parser.add_argument("--summary-json", default="research/evaluations/latest.json")
    parser.add_argument("--windows", nargs="+", type=int, default=[3, 5, 10, 20])
    args = parser.parse_args()

    calls_dir = pathlib.Path(args.calls_dir)
    snapshot_dir = pathlib.Path(args.snapshot_dir)
    summary_md = pathlib.Path(args.summary_md)
    summary_json = pathlib.Path(args.summary_json)
    summary_md.parent.mkdir(parents=True, exist_ok=True)

    evaluations, summary = evaluate_calls(calls_dir, snapshot_dir, args.windows)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_markdown(summary_md, summary, evaluations)
    print(f"Posterior evaluation summary written to {summary_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
