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

from rank_investment_universe import DEFAULT_STRATEGY_WEIGHTS, annotate_theme_positions, apply_action_qualification, apply_edge_cost_fields, candidate_layers, item_score, load_strategy_config  # noqa: E402


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def load_weights(path: pathlib.Path | None, weights_json: str | None) -> tuple[str, dict[str, float]]:
    if weights_json:
        data = json.loads(weights_json)
        weights = DEFAULT_STRATEGY_WEIGHTS.copy()
        weights.update({key: float(value) for key, value in data.items() if key in weights})
        return "inline_weights", weights
    strategy = load_strategy_config(path) if path else load_strategy_config(None)
    return strategy["strategy_version"], strategy["weights"]


def registry_entries(registry: dict[str, Any], snapshot_type: str) -> list[dict[str, Any]]:
    entries = []
    for entry in registry.get("entries", []):
        if entry.get("snapshot_type") != snapshot_type:
            continue
        if entry.get("session") not in {"close", "historical"}:
            continue
        if entry.get("quality", {}).get("missing_latest_close", 0) != 0:
            continue
        if entry.get("quality", {}).get("date_mismatch"):
            continue
        if entry.get("as_of_date") and str(entry.get("as_of_date")) != str(entry.get("date")):
            continue
        try:
            entry_date = parse_date(str(entry.get("date")))
        except ValueError:
            continue
        entries.append({**entry, "_date": entry_date})
    return sorted(entries, key=lambda item: item["_date"])


def filter_entries_as_of(entries: list[dict[str, Any]], as_of_date: dt.date | None) -> list[dict[str, Any]]:
    if as_of_date is None:
        return entries
    return [entry for entry in entries if entry["_date"] <= as_of_date]


def snapshot_items(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("symbol")): item for item in snapshot.get("items", []) if item.get("symbol")}


def nearest_future(entries: list[dict[str, Any]], base_date: dt.date, horizon_days: int) -> dict[str, Any] | None:
    target = base_date + dt.timedelta(days=horizon_days)
    for entry in entries:
        if entry["_date"] >= target:
            return entry
    return None


def adverse_return_pct(entries: list[dict[str, Any]], base_date: dt.date, future_date: dt.date, symbol: str, base_price: float) -> float | None:
    values = []
    for entry in entries:
        if not (base_date < entry["_date"] <= future_date):
            continue
        item = snapshot_items(load_json(pathlib.Path(entry["path"]))).get(symbol)
        if item and item.get("latest_close") and base_price:
            values.append(((float(item["latest_close"]) / base_price) - 1.0) * 100.0)
    return min(values) if values else None


def backtest(
    registry_path: pathlib.Path,
    strategy_version: str,
    weights: dict[str, float],
    top_n: int,
    horizon_days: int,
    round_trip_bps: float,
    benchmark_symbol: str,
    min_watch_score: float = 45.0,
    min_action_score: float = 65.0,
    candidate_policy: str = "strict",
    min_samples: int = 12,
    max_adverse_limit_pct: float = -8.0,
    as_of_date: dt.date | None = None,
    actionable_top_n: int | None = None,
    diagnostic_top_n: int | None = None,
    minimum_edge_bps: float = 100.0,
) -> dict[str, Any]:
    if candidate_policy not in {"strict", "relaxed"}:
        raise ValueError("candidate_policy must be strict or relaxed")
    registry = load_json(registry_path)
    entries = filter_entries_as_of(registry_entries(registry, "trade"), as_of_date)
    cost_pct = round_trip_bps / 100.0
    actionable_top_n = top_n if actionable_top_n is None else actionable_top_n
    diagnostic_top_n = top_n if diagnostic_top_n is None else diagnostic_top_n
    diagnostic_records = []

    def collect_records(use_relaxed_top_n: bool) -> list[dict[str, Any]]:
        collected = []
        for entry in entries:
            base_snapshot = load_json(pathlib.Path(entry["path"]))
            future_entry = nearest_future(entries, entry["_date"], horizon_days)
            if future_entry is None:
                continue
            future_snapshot = load_json(pathlib.Path(future_entry["path"]))
            future_items = snapshot_items(future_snapshot)
            base_items = snapshot_items(base_snapshot)
            scored = annotate_theme_positions([item_score(item, weights, min_watch_score) for item in base_items.values()])
            apply_edge_cost_fields(scored, round_trip_bps, minimum_edge_bps)
            ranked = sorted(scored, key=lambda row: row["score"], reverse=True)
            apply_action_qualification(ranked, min_action_score, {})
            actionable, diagnostics, _top = candidate_layers(ranked, actionable_top_n, diagnostic_top_n)
            if use_relaxed_top_n:
                candidates = list(actionable)
                if len(candidates) < actionable_top_n:
                    fill = [row for row in diagnostics if row.get("symbol") not in {candidate.get("symbol") for candidate in candidates}]
                    candidates.extend(fill[: actionable_top_n - len(candidates)])
            else:
                candidates = actionable
            benchmark_base = base_items.get(benchmark_symbol)
            benchmark_future = future_items.get(benchmark_symbol)
            benchmark_return = None
            if benchmark_base and benchmark_future and benchmark_base.get("latest_close"):
                benchmark_return = ((float(benchmark_future["latest_close"]) / float(benchmark_base["latest_close"])) - 1.0) * 100.0 - cost_pct

            def append_record(candidate: dict[str, Any], rank: int, sample_type: str) -> None:
                symbol = str(candidate["symbol"])
                base_item = base_items.get(symbol)
                future_item = future_items.get(symbol)
                if not base_item or not future_item or not base_item.get("latest_close") or not future_item.get("latest_close"):
                    return
                base_price = float(base_item["latest_close"])
                gross_return = ((float(future_item["latest_close"]) / base_price) - 1.0) * 100.0
                net_return = gross_return - cost_pct
                adverse = adverse_return_pct(entries, entry["_date"], future_entry["_date"], symbol, base_price)
                below_watch_score = candidate["score"] < min_watch_score
                adverse_breach = adverse is not None and adverse < max_adverse_limit_pct
                low_quality_flags = []
                if below_watch_score:
                    low_quality_flags.append("below_watch_score")
                if candidate.get("diagnostic_only"):
                    low_quality_flags.append("diagnostic_only")
                low_quality_flags.extend(candidate.get("disqualifiers") or [])
                record = {
                    "base_date": entry["date"],
                    "future_date": future_entry["date"],
                    "window_days": (future_entry["_date"] - entry["_date"]).days,
                    "rank": rank,
                    "sample_type": sample_type,
                    "symbol": symbol,
                    "score": candidate["score"],
                    "below_watch_score": below_watch_score,
                    "qualified_for_watch": bool(candidate.get("qualified_for_watch")),
                    "qualified_for_action": bool(candidate.get("qualified_for_action")),
                    "diagnostic_only": bool(candidate.get("diagnostic_only")),
                    "theme_rank": candidate.get("theme_rank"),
                    "theme_peer_count": candidate.get("theme_peer_count"),
                    "theme_leader": candidate.get("theme_leader"),
                    "is_theme_leader": bool(candidate.get("is_theme_leader")),
                    "qualification_flags": candidate.get("qualification_flags", []),
                    "disqualifiers": candidate.get("disqualifiers", []),
                    "low_quality_flags": low_quality_flags,
                    "base_price": round(base_price, 4),
                    "future_price": round(float(future_item["latest_close"]), 4),
                    "net_return_pct": round(net_return, 3),
                    "max_adverse_pct": round(adverse, 3) if adverse is not None else None,
                    "adverse_breach": adverse_breach,
                    "benchmark_return_pct": round(benchmark_return, 3) if benchmark_return is not None else None,
                    "alpha_pct": round(net_return - benchmark_return, 3) if benchmark_return is not None else None,
                }
                if sample_type == "diagnostic":
                    diagnostic_records.append(record)
                else:
                    collected.append(record)

            for rank, candidate in enumerate(candidates, start=1):
                append_record(candidate, rank, "actionable" if candidate.get("qualified_for_action") else "relaxed_diagnostic")
            for rank, candidate in enumerate(diagnostics, start=1):
                append_record(candidate, rank, "diagnostic")
        return collected

    strict_records = collect_records(use_relaxed_top_n=False)
    use_relaxed = candidate_policy == "relaxed" and len(strict_records) < min_samples
    records = collect_records(use_relaxed_top_n=True) if use_relaxed else strict_records

    returns = [record["net_return_pct"] for record in records]
    alphas = [record["alpha_pct"] for record in records if record["alpha_pct"] is not None]
    adverse_values = [record["max_adverse_pct"] for record in records if record["max_adverse_pct"] is not None]
    adverse_breaches = [value for value in adverse_values if value < max_adverse_limit_pct]
    qualified_sample_count = sum(1 for record in records if record.get("qualified_for_action"))
    diagnostic_sample_count = len(diagnostic_records) + sum(1 for record in records if record.get("sample_type") == "relaxed_diagnostic")
    strict_sample_count = len(strict_records)
    relaxed_sample_count = diagnostic_sample_count if use_relaxed else 0
    if use_relaxed:
        sample_quality = "relaxed_fallback"
    elif len(records) >= min_samples:
        sample_quality = "sufficient"
    else:
        sample_quality = "thin"
    summary = {
        "strategy_version": strategy_version,
        "strategy_weights": weights,
        "top_n": top_n,
        "actionable_top_n": actionable_top_n,
        "diagnostic_top_n": diagnostic_top_n,
        "horizon_days": horizon_days,
        "round_trip_bps": round_trip_bps,
        "minimum_edge_bps": minimum_edge_bps,
        "benchmark_symbol": benchmark_symbol,
        "min_watch_score": min_watch_score,
        "min_action_score": min_action_score,
        "candidate_policy": candidate_policy,
        "max_adverse_limit_pct": max_adverse_limit_pct,
        "as_of_date": as_of_date.isoformat() if as_of_date else None,
        "sample_count": len(records),
        "strict_sample_count": strict_sample_count,
        "relaxed_sample_count": relaxed_sample_count,
        "qualified_sample_count": qualified_sample_count,
        "diagnostic_sample_count": diagnostic_sample_count,
        "sample_quality": sample_quality,
        "avg_net_return_pct": round(statistics.fmean(returns), 3) if returns else None,
        "median_net_return_pct": round(statistics.median(returns), 3) if returns else None,
        "win_rate": round(sum(1 for value in returns if value > 0) / len(returns), 3) if returns else None,
        "avg_alpha_pct": round(statistics.fmean(alphas), 3) if alphas else None,
        "avg_max_adverse_pct": round(statistics.fmean(adverse_values), 3) if adverse_values else None,
        "max_adverse_pct": round(min(adverse_values), 3) if adverse_values else None,
        "adverse_breach_rate": round(len(adverse_breaches) / len(adverse_values), 3) if adverse_values else None,
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "registry": str(registry_path),
        "summary": summary,
        "records": records,
        "diagnostic_records": diagnostic_records,
    }


def write_markdown(path: pathlib.Path, result: dict[str, Any]) -> None:
    summary = result["summary"]
    lines = [
        "# Investment Strategy Backtest",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Strategy: `{summary['strategy_version']}`",
        f"Samples: `{summary['sample_count']}`",
        f"Sample quality: `{summary['sample_quality']}`",
        f"Strict samples: `{summary['strict_sample_count']}`",
        f"Relaxed samples: `{summary['relaxed_sample_count']}`",
        f"Qualified samples: `{summary['qualified_sample_count']}`",
        f"Diagnostic samples: `{summary['diagnostic_sample_count']}`",
        f"Average net return: `{summary['avg_net_return_pct']}`%",
        f"Win rate: `{summary['win_rate']}`",
        f"Average benchmark alpha: `{summary['avg_alpha_pct']}`%",
        f"Average max adverse return: `{summary['avg_max_adverse_pct']}`%",
        f"Max adverse-ish return: `{summary['max_adverse_pct']}`%",
        f"Adverse breach rate: `{summary['adverse_breach_rate']}`",
        "",
        "## Weights",
    ]
    for key, value in summary["strategy_weights"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Recent Records"])
    for record in result["records"][-20:]:
        lines.append(
            f"- `{record['base_date']}` rank {record['rank']} `{record['symbol']}`: "
            f"net={record['net_return_pct']}%, alpha={record['alpha_pct']}%, adverse={record['max_adverse_pct']}%, "
            f"qualified={record['qualified_for_watch']}, diagnostic={record['diagnostic_only']}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Backtest investment ranking weights against historical snapshots.")
    parser.add_argument("--registry", default=str(ROOT / "data" / "snapshots" / "registry.json"))
    parser.add_argument("--strategy-config", default=str(ROOT / "config" / "active_strategy.toml"))
    parser.add_argument("--weights-json", default=None)
    parser.add_argument("--output-dir", default=str(ROOT / "research" / "experiments"))
    parser.add_argument("--top-n", type=int, default=3)
    parser.add_argument("--actionable-top-n", type=int, default=None)
    parser.add_argument("--diagnostic-top-n", type=int, default=None)
    parser.add_argument("--horizon-days", type=int, default=3)
    parser.add_argument("--round-trip-bps", type=float, default=35)
    parser.add_argument("--minimum-edge-bps", type=float, default=100)
    parser.add_argument("--benchmark-symbol", default="2800.HK")
    parser.add_argument("--min-watch-score", type=float, default=45)
    parser.add_argument("--min-action-score", type=float, default=65)
    parser.add_argument("--candidate-policy", choices=["strict", "relaxed"], default="strict")
    parser.add_argument("--min-samples", type=int, default=12)
    parser.add_argument("--max-adverse-limit-pct", type=float, default=-8.0)
    parser.add_argument("--as-of-date", default=None, help="Only use snapshots and future legs available on or before this date.")
    args = parser.parse_args()

    strategy_version, weights = load_weights(pathlib.Path(args.strategy_config) if args.strategy_config else None, args.weights_json)
    as_of_date = parse_date(args.as_of_date) if args.as_of_date else None
    result = backtest(
        pathlib.Path(args.registry),
        strategy_version,
        weights,
        args.top_n,
        args.horizon_days,
        args.round_trip_bps,
        args.benchmark_symbol,
        args.min_watch_score,
        args.min_action_score,
        args.candidate_policy,
        args.min_samples,
        args.max_adverse_limit_pct,
        as_of_date,
        args.actionable_top_n,
        args.diagnostic_top_n,
        args.minimum_edge_bps,
    )
    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "latest_backtest.json"
    md_path = output_dir / "latest_backtest.md"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(md_path, result)
    print(f"Wrote backtest: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
