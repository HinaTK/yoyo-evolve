#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import statistics
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from backtest_investment_strategy import load_json, nearest_future, price_path_points, registry_entries, snapshot_items  # noqa: E402
from log_investment_shadow import DEFAULT_SHADOW_HORIZON_DAYS, benchmark_symbol  # noqa: E402


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_shadow_logs(shadow_dir: pathlib.Path) -> list[tuple[pathlib.Path, dict[str, Any]]]:
    logs = []
    for path in sorted(shadow_dir.glob("**/*-shadow.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and data.get("mode") == "shadow_logging":
            logs.append((path, data))
    return logs


def shadow_candidates(log: dict[str, Any]) -> list[dict[str, Any]]:
    rows = log.get("shadow_actionable_candidates")
    return rows if isinstance(rows, list) else []


def outcome_for_candidate(
    candidate: dict[str, Any],
    base_date: dt.date,
    entries: list[dict[str, Any]],
    horizon_days: int,
    round_trip_bps: float,
    max_adverse_limit_pct: float,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    symbol = str(candidate.get("symbol") or "")
    base_price = as_float(candidate.get("latest_close"))
    if not symbol or base_price is None or base_price <= 0:
        return None, {"symbol": symbol, "reason": "missing_shadow_entry_price"}

    future_entry = nearest_future(entries, base_date, horizon_days)
    if future_entry is None:
        return None, {"symbol": symbol, "reason": "future_horizon_not_available"}

    price_points = price_path_points(entries, base_date, future_entry["_date"], symbol, base_price)
    if not price_points:
        return None, {"symbol": symbol, "reason": "future_symbol_prices_not_available"}

    stop_loss_pct = as_float(candidate.get("stop_loss_pct"))
    exit_entry = future_entry
    exit_triggered = False
    exit_reason = None
    if stop_loss_pct is not None:
        for point in price_points:
            if point["return_pct"] <= stop_loss_pct:
                exit_entry = point["entry"]
                exit_triggered = True
                exit_reason = "daily_close_stop_loss"
                break

    exit_snapshot = load_json(pathlib.Path(exit_entry["path"]))
    exit_items = snapshot_items(exit_snapshot)
    exit_item = exit_items.get(symbol)
    if not exit_item or not exit_item.get("latest_close"):
        return None, {"symbol": symbol, "reason": "exit_symbol_price_not_available"}

    cost_pct = round_trip_bps / 100.0
    exit_price = float(exit_item["latest_close"])
    gross_return = ((exit_price / base_price) - 1.0) * 100.0
    net_return = gross_return - cost_pct
    managed_points = [point for point in price_points if point["_date"] <= exit_entry["_date"]]
    adverse = min((point["return_pct"] for point in managed_points), default=None)
    unmanaged_adverse = min((point["return_pct"] for point in price_points), default=None)

    candidate_benchmark = str(candidate.get("benchmark_symbol") or benchmark_symbol(symbol))
    benchmark_return = None
    base_entry = next((entry for entry in entries if entry["_date"] == base_date), None)
    if base_entry is not None:
        base_items = snapshot_items(load_json(pathlib.Path(base_entry["path"])))
        benchmark_base = base_items.get(candidate_benchmark)
        benchmark_exit = exit_items.get(candidate_benchmark)
        if benchmark_base and benchmark_exit and benchmark_base.get("latest_close"):
            benchmark_return = ((float(benchmark_exit["latest_close"]) / float(benchmark_base["latest_close"])) - 1.0) * 100.0 - cost_pct

    return (
        {
            "base_date": base_date.isoformat(),
            "future_date": exit_entry["date"],
            "planned_future_date": future_entry["date"],
            "symbol": symbol,
            "market_family": candidate.get("market_family"),
            "theme": candidate.get("theme"),
            "entry_price": round(base_price, 4),
            "exit_price": round(exit_price, 4),
            "net_return_pct": round(net_return, 3),
            "benchmark_symbol": candidate_benchmark,
            "benchmark_return_pct": round(benchmark_return, 3) if benchmark_return is not None else None,
            "alpha_pct": round(net_return - benchmark_return, 3) if benchmark_return is not None else None,
            "max_adverse_pct": round(adverse, 3) if adverse is not None else None,
            "unmanaged_max_adverse_pct": round(unmanaged_adverse, 3) if unmanaged_adverse is not None else None,
            "adverse_breach": bool(adverse is not None and adverse < max_adverse_limit_pct),
            "exit_triggered": exit_triggered,
            "exit_reason": exit_reason,
            "stop_loss_pct": stop_loss_pct,
            "shadow_filter_profile": candidate.get("shadow_filter_profile"),
            "shadow_filter_reasons": candidate.get("shadow_filter_reasons", []),
        },
        None,
    )


def performance_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    returns = [value for value in (as_float(record.get("net_return_pct")) for record in records) if value is not None]
    alphas = [value for value in (as_float(record.get("alpha_pct")) for record in records) if value is not None]
    adverse_values = [value for value in (as_float(record.get("max_adverse_pct")) for record in records) if value is not None]
    stop_count = sum(1 for record in records if record.get("exit_triggered"))
    breach_count = sum(1 for record in records if record.get("adverse_breach"))
    return {
        "sample_count": len(records),
        "win_rate": round(sum(1 for value in returns if value > 0) / len(returns), 3) if returns else None,
        "avg_net_return_pct": round(statistics.fmean(returns), 3) if returns else None,
        "median_net_return_pct": round(statistics.median(returns), 3) if returns else None,
        "avg_alpha_pct": round(statistics.fmean(alphas), 3) if alphas else None,
        "max_adverse_pct": round(min(adverse_values), 3) if adverse_values else None,
        "adverse_breach_rate": round(breach_count / len(adverse_values), 3) if adverse_values else None,
        "stop_triggered_rate": round(stop_count / len(records), 3) if records else None,
    }


def build_evaluation(
    shadow_dir: pathlib.Path,
    registry_path: pathlib.Path,
    include_replay: bool = False,
    round_trip_bps: float = 35.0,
    max_adverse_limit_pct: float = -8.0,
    min_forward_shadow_days: int = 20,
) -> dict[str, Any]:
    registry = load_json(registry_path)
    entries = registry_entries(registry, "trade")
    logs = load_shadow_logs(shadow_dir)
    records = []
    pending_records = []
    skipped_logs = []
    evaluated_log_count = 0
    forward_log_count = 0
    replay_log_count = 0
    no_action_log_count = 0
    matured_log_dates: set[str] = set()

    for path, log in logs:
        is_forward = log.get("evidence_mode") == "forward_shadow" and log.get("counts_toward_forward_evidence") is True
        is_replay = log.get("evidence_mode") == "historical_replay"
        if is_forward:
            forward_log_count += 1
        if is_replay:
            replay_log_count += 1
        if not is_forward and not include_replay:
            skipped_logs.append({"path": str(path), "evidence_mode": log.get("evidence_mode"), "reason": "not_forward_shadow"})
            continue

        date_text = str(log.get("date") or "")
        try:
            base_date = parse_date(date_text)
        except ValueError:
            skipped_logs.append({"path": str(path), "evidence_mode": log.get("evidence_mode"), "reason": "invalid_shadow_date"})
            continue
        candidates = shadow_candidates(log)
        if not candidates:
            no_action_log_count += 1
        evaluated_log_count += 1
        log_horizon = int((log.get("shadow_policy") or {}).get("horizon_days") or DEFAULT_SHADOW_HORIZON_DAYS)
        future_entry = nearest_future(entries, base_date, log_horizon)
        if future_entry is not None:
            matured_log_dates.add(date_text)
        for candidate in candidates:
            record, pending = outcome_for_candidate(candidate, base_date, entries, log_horizon, round_trip_bps, max_adverse_limit_pct)
            if record is not None:
                record["shadow_log"] = str(path)
                record["evidence_mode"] = log.get("evidence_mode")
                record["counts_toward_forward_evidence"] = is_forward
                records.append(record)
            elif pending is not None:
                pending_records.append({"shadow_log": str(path), "base_date": date_text, "evidence_mode": log.get("evidence_mode"), **pending})

    stats = performance_summary(records)
    findings = []
    matured_forward_days = len(matured_log_dates) if not include_replay else sum(1 for path, log in logs if log.get("evidence_mode") == "forward_shadow" and log.get("date") in matured_log_dates)
    if forward_log_count < min_forward_shadow_days:
        findings.append({"metric": "forward_shadow_days", "actual": forward_log_count, "expected": f">= {min_forward_shadow_days}"})
    if matured_forward_days < min_forward_shadow_days:
        findings.append({"metric": "matured_forward_shadow_days", "actual": matured_forward_days, "expected": f">= {min_forward_shadow_days}"})
    if records and (stats.get("adverse_breach_rate") or 0.0) > 0.0:
        findings.append({"metric": "forward_adverse_breach_rate", "actual": stats.get("adverse_breach_rate"), "expected": "<= 0.0"})
    if not records:
        findings.append({"metric": "forward_sample_count", "actual": 0, "expected": "> 0"})

    return {
        "generated_at": utc_now(),
        "shadow_dir": str(shadow_dir),
        "registry": str(registry_path),
        "evaluation_mode": "historical_replay_diagnostic" if include_replay else "forward_shadow_only",
        "counts_toward_forward_evidence": not include_replay,
        "thresholds": {
            "min_forward_shadow_days": min_forward_shadow_days,
            "max_forward_adverse_breach_rate": 0.0,
            "max_adverse_limit_pct": max_adverse_limit_pct,
            "round_trip_bps": round_trip_bps,
        },
        "summary": {
            "total_shadow_log_count": len(logs),
            "forward_shadow_log_count": forward_log_count,
            "historical_replay_log_count": replay_log_count,
            "evaluated_log_count": evaluated_log_count,
            "matured_forward_shadow_days": matured_forward_days,
            "no_action_log_count": no_action_log_count,
            "pending_sample_count": len(pending_records),
            **stats,
        },
        "gate": {"passed": not findings, "findings": findings},
        "records": records,
        "pending_records": pending_records,
        "skipped_logs": skipped_logs,
    }


def write_markdown(path: pathlib.Path, result: dict[str, Any]) -> None:
    summary = result["summary"]
    lines = [
        "# Shadow Forward Evaluation",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Evaluation mode: `{result['evaluation_mode']}`",
        f"Counts toward forward evidence: `{result['counts_toward_forward_evidence']}`",
        f"Gate passed: `{result['gate']['passed']}`",
        "",
        "## Summary",
        f"- forward shadow logs: `{summary['forward_shadow_log_count']}`",
        f"- matured forward days: `{summary['matured_forward_shadow_days']}`",
        f"- samples: `{summary['sample_count']}`",
        f"- pending samples: `{summary['pending_sample_count']}`",
        f"- win rate: `{summary['win_rate']}`",
        f"- avg net return: `{summary['avg_net_return_pct']}`%",
        f"- avg alpha: `{summary['avg_alpha_pct']}`%",
        f"- max adverse: `{summary['max_adverse_pct']}`%",
        f"- adverse breach rate: `{summary['adverse_breach_rate']}`",
        f"- stop triggered rate: `{summary['stop_triggered_rate']}`",
        "",
        "## Findings",
    ]
    if result["gate"]["findings"]:
        for finding in result["gate"]["findings"]:
            lines.append(f"- `{finding['metric']}` actual `{finding['actual']}`, expected `{finding['expected']}`")
    else:
        lines.append("- no forward gate blockers")
    lines.extend(["", "## Recent Records"])
    for record in result.get("records", [])[-20:]:
        lines.append(
            f"- `{record['base_date']}` `{record['symbol']}`: net={record['net_return_pct']}%, "
            f"alpha={record.get('alpha_pct')}%, adverse={record.get('max_adverse_pct')}%, stop={record.get('exit_triggered')}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate matured shadow-only investment logs against later snapshots.")
    parser.add_argument("--shadow-dir", default=str(ROOT / "research" / "shadow"))
    parser.add_argument("--registry", default=str(ROOT / "data" / "snapshots" / "registry.json"))
    parser.add_argument("--output-json", default=str(ROOT / "research" / "shadow" / "latest_forward_evaluation.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "shadow" / "latest_forward_evaluation.md"))
    parser.add_argument("--include-replay", action="store_true", help="Diagnostic only: include historical replay logs, but do not count this output as forward evidence.")
    parser.add_argument("--round-trip-bps", type=float, default=35.0)
    parser.add_argument("--max-adverse-limit-pct", type=float, default=-8.0)
    parser.add_argument("--min-forward-shadow-days", type=int, default=20)
    args = parser.parse_args()

    result = build_evaluation(
        pathlib.Path(args.shadow_dir),
        pathlib.Path(args.registry),
        args.include_replay,
        args.round_trip_bps,
        args.max_adverse_limit_pct,
        args.min_forward_shadow_days,
    )
    output_json = pathlib.Path(args.output_json)
    output_md = pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(output_md, result)
    print(json.dumps(result["summary"], indent=2))
    print(json.dumps(result["gate"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
