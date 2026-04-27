#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import re
import statistics
from collections import Counter, defaultdict
from typing import Any


BULLISH_STATES = {"buy_candidate", "accumulate", "hold"}
BEARISH_STATES = {"trim", "sell_candidate", "avoid"}
NEUTRAL_STATES = {"watch_only"}
INTRADAY_SESSIONS = {"morning", "midday"}
EVALUATED_SESSIONS = {"morning", "midday", "close", "historical"}
SNAPSHOT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(morning|midday|close|historical))?$")
CALL_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(morning|midday|close|historical))?-calls$")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(text: str) -> dt.date:
    return dt.date.fromisoformat(text)


def available_snapshots(snapshot_dir: pathlib.Path) -> dict[tuple[dt.date, str], pathlib.Path]:
    out = {}
    for path in sorted(snapshot_dir.glob("*.json")):
        if path.stem.endswith("-radar"):
            continue
        match = SNAPSHOT_RE.match(path.stem)
        if not match:
            continue
        session = match.group(2) or "close"
        out[(parse_date(match.group(1)), session)] = path
    return out


def call_session(call_path: pathlib.Path, payload: dict[str, Any]) -> str:
    session = payload.get("session")
    if session:
        return str(session)
    match = CALL_RE.match(call_path.stem)
    if match and match.group(2):
        return match.group(2)
    return "historical"


def snapshot_for(snapshots: dict[tuple[dt.date, str], dict[str, Any]], day: dt.date, session: str) -> dict[str, Any] | None:
    if session == "historical":
        session = "close"
    return snapshots.get((day, session)) or snapshots.get((day, "close"))


def snapshot_item(snapshot: dict[str, Any], symbol: str) -> dict[str, Any] | None:
    for item in snapshot.get("items", []):
        if item.get("symbol") == symbol:
            return item
    return None


def snapshot_price(snapshot: dict[str, Any], symbol: str) -> float | None:
    item = snapshot_item(snapshot, symbol)
    if item is not None:
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


def peer_return_stats(
    base_snapshot: dict[str, Any],
    future_snapshot: dict[str, Any],
    theme: str | None,
    selected_symbol: str,
) -> dict[str, Any]:
    if not theme:
        return {}
    returns = []
    for base_item in base_snapshot.get("items", []):
        if base_item.get("theme") != theme:
            continue
        symbol = base_item.get("symbol")
        future_price = snapshot_price(future_snapshot, symbol)
        if future_price is None:
            continue
        base_price = float(base_item["latest_close"])
        if not base_price:
            continue
        returns.append((symbol, ((future_price / base_price) - 1.0) * 100.0))

    if len(returns) < 2:
        return {}

    selected = next((value for symbol, value in returns if symbol == selected_symbol), None)
    if selected is None:
        return {}
    sorted_returns = sorted(returns, key=lambda item: item[1], reverse=True)
    return {
        "peer_count": len(returns),
        "peer_median_return_pct": round(statistics.median(value for _symbol, value in returns), 3),
        "peer_best_symbol": sorted_returns[0][0],
        "peer_best_return_pct": round(sorted_returns[0][1], 3),
        "peer_rank": next(index + 1 for index, (symbol, _value) in enumerate(sorted_returns) if symbol == selected_symbol),
    }


def classify_learning(
    call: dict[str, Any],
    return_pct: float,
    verdict: str,
    peer_median_return_pct: float | None = None,
    peer_count: int = 0,
) -> str | None:
    confidence = float(call.get("confidence", 0.0))
    state = call.get("state")
    if peer_count >= 2 and peer_median_return_pct is not None and return_pct < peer_median_return_pct - 1.0:
        return "symbol_selection_error"
    if verdict == "fail" and peer_median_return_pct is not None:
        if state in BULLISH_STATES and peer_median_return_pct < -0.5:
            return "theme_error"
        if state in BEARISH_STATES and peer_median_return_pct > 0.5:
            return "theme_error"
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


def evaluate_calls(
    calls_dir: pathlib.Path,
    snapshot_dir: pathlib.Path,
    close_windows: list[int],
    intraday_windows: list[int],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    snapshot_paths = available_snapshots(snapshot_dir)
    snapshots = {key: load_json(path) for key, path in snapshot_paths.items()}
    evaluations: list[dict[str, Any]] = []
    verdict_counts = Counter()
    learning_counts = Counter()
    session_counts = Counter()
    symbol_stats = defaultdict(list)

    for call_path in sorted(calls_dir.glob("*-calls.json")):
        payload = load_json(call_path)
        session = call_session(call_path, payload)
        if session not in EVALUATED_SESSIONS:
            continue
        call_date = parse_date(payload["date"])
        base_snapshot = snapshot_for(snapshots, call_date, session)
        if base_snapshot is None:
            continue
        windows = intraday_windows if session in INTRADAY_SESSIONS else close_windows

        for rec in payload.get("recommendations", []):
            symbol = rec["symbol"]
            base_item = snapshot_item(base_snapshot, symbol)
            if base_item is None:
                continue
            base_price = float(base_item["latest_close"])
            theme = rec.get("theme") or base_item.get("theme")

            for window in windows:
                future_snapshot = snapshot_for(snapshots, call_date + dt.timedelta(days=window), "close")
                if future_snapshot is None:
                    continue
                future_price = snapshot_price(future_snapshot, symbol)
                if future_price is None:
                    continue

                return_pct = ((future_price / base_price) - 1.0) * 100.0
                verdict = verdict_for_state(rec["state"], return_pct)
                peer_stats = peer_return_stats(base_snapshot, future_snapshot, theme, symbol)
                learning = classify_learning(
                    rec,
                    return_pct,
                    verdict,
                    peer_stats.get("peer_median_return_pct"),
                    int(peer_stats.get("peer_count", 0)),
                )
                record = {
                    "call_date": payload["date"],
                    "session": session,
                    "window_days": window,
                    "symbol": symbol,
                    "theme": theme,
                    "state": rec["state"],
                    "confidence": rec.get("confidence"),
                    "base_price": round(base_price, 4),
                    "future_price": round(future_price, 4),
                    "return_pct": round(return_pct, 3),
                    "verdict": verdict,
                    "learning_tag": learning,
                    "selection_source_theme": rec.get("selection_source_theme"),
                    "selection_reason": rec.get("selection_reason"),
                    **peer_stats,
                }
                evaluations.append(record)
                verdict_counts[verdict] += 1
                session_counts[session] += 1
                if learning:
                    learning_counts[learning] += 1
                symbol_stats[symbol].append(record)

    summary = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "evaluations": len(evaluations),
        "verdict_counts": dict(verdict_counts),
        "learning_counts": dict(learning_counts),
        "session_counts": dict(session_counts),
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
        "recent_selection_errors": [item for item in evaluations[-20:] if item.get("learning_tag") == "symbol_selection_error"],
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

    lines.extend(["", "## Session Counts"])
    if summary["session_counts"]:
        for key, value in sorted(summary["session_counts"].items()):
            lines.append(f"- `{key}`: {value}")
    else:
        lines.append("- No evaluated sessions yet.")

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

    lines.extend(["", "## Recent Selection Errors"])
    if summary["recent_selection_errors"]:
        for item in summary["recent_selection_errors"]:
            lines.append(
                f"- `{item['call_date']}` `{item['session']}` `{item['symbol']}` `{item['theme']}` T+{item['window_days']}: "
                f"{item['return_pct']}% vs peer median {item.get('peer_median_return_pct')}%, "
                f"best `{item.get('peer_best_symbol')}` {item.get('peer_best_return_pct')}%"
            )
    else:
        lines.append("- No recent same-theme symbol-selection errors detected.")

    lines.extend(["", "## Recent Evaluations"])
    for item in evaluations[-15:]:
        lines.append(
            f"- `{item['call_date']}` `{item['session']}` `{item['symbol']}` `{item['state']}` T+{item['window_days']}: {item['return_pct']}% -> `{item['verdict']}`"
        )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate historical investment calls against later snapshots.")
    parser.add_argument("--calls-dir", default="research/calls")
    parser.add_argument("--snapshot-dir", default="data/snapshots")
    parser.add_argument("--summary-md", default="research/evaluations/latest.md")
    parser.add_argument("--summary-json", default="research/evaluations/latest.json")
    parser.add_argument("--windows", nargs="+", type=int, default=[3, 5, 10, 20], help="Close/historical evaluation windows.")
    parser.add_argument("--intraday-windows", nargs="+", type=int, default=[0, 1, 3], help="Morning/midday evaluation windows, where 0 means same-day close.")
    args = parser.parse_args()

    calls_dir = pathlib.Path(args.calls_dir)
    snapshot_dir = pathlib.Path(args.snapshot_dir)
    summary_md = pathlib.Path(args.summary_md)
    summary_json = pathlib.Path(args.summary_json)
    summary_md.parent.mkdir(parents=True, exist_ok=True)

    evaluations, summary = evaluate_calls(calls_dir, snapshot_dir, args.windows, args.intraday_windows)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_markdown(summary_md, summary, evaluations)
    print(f"Posterior evaluation summary written to {summary_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
