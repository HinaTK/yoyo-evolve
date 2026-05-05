#!/usr/bin/env python3

import argparse
import datetime as dt
import itertools
import json
import pathlib
import sys
import tomllib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from backtest_investment_strategy import backtest  # noqa: E402
from rank_investment_universe import DEFAULT_SAFETY_INVARIANTS, DEFAULT_STRATEGY_WEIGHTS, load_strategy_config  # noqa: E402


IMMUTABLE_TRUE_INVARIANTS = {
    "forbid_automatic_trading",
    "forbid_cost_gate_reduction",
    "forbid_edge_gate_reduction",
    "forbid_history_tampering",
    "forbid_snapshot_mutation",
    "auto_select_active_research_strategy",
    "research_only",
}


def read_toml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_date(value: str | None) -> dt.date | None:
    return dt.date.fromisoformat(value) if value else None


def candidate_weights(search: dict[str, list[float]]) -> list[dict[str, float]]:
    allowed = list(DEFAULT_STRATEGY_WEIGHTS)
    values = [search.get(key, [DEFAULT_STRATEGY_WEIGHTS[key]]) for key in allowed]
    return [dict(zip(allowed, (float(value) for value in combo), strict=True)) for combo in itertools.product(*values)]


def score_summary(summary: dict[str, Any]) -> float:
    avg_return = float(summary.get("avg_net_return_pct") or 0.0)
    avg_alpha = float(summary.get("avg_alpha_pct") or 0.0)
    win_rate = float(summary.get("win_rate") or 0.0)
    adverse = float(summary.get("max_adverse_pct") or 0.0)
    avg_adverse = float(summary.get("avg_max_adverse_pct") or 0.0)
    adverse_breach_rate = float(summary.get("adverse_breach_rate") or 0.0)
    sample_quality = str(summary.get("sample_quality") or "thin")
    quality_penalty = {"sufficient": 0.0, "thin": 2.0, "relaxed_fallback": 6.0}.get(sample_quality, 2.0)
    return avg_return + avg_alpha * 0.5 + win_rate * 2.0 + min(adverse, 0.0) * 0.1 + min(avg_adverse, 0.0) * 0.08 - adverse_breach_rate * 4.0 - quality_penalty


def split_dates_for_window(records: list[dict[str, Any]], window_count: int) -> list[set[str]]:
    dates = sorted({str(record["base_date"]) for record in records})
    if window_count <= 1 or len(dates) < window_count:
        return [set(dates)]
    size = max(1, len(dates) // window_count)
    return [set(dates[index * size : len(dates) if index == window_count - 1 else (index + 1) * size]) for index in range(window_count)]


def trade_entry_count(registry_path: pathlib.Path) -> int:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    return sum(
        1
        for entry in registry.get("entries", [])
        if entry.get("snapshot_type") == "trade" and entry.get("session") in {"close", "historical"}
    )


def robust_score(result: dict[str, Any], window_count: int) -> float:
    records = result.get("records", [])
    if not records:
        return -999.0
    base_score = score_summary(result["summary"])
    windows = split_dates_for_window(records, window_count)
    if len(windows) <= 1:
        return base_score
    chunks = []
    for dates in windows:
        chunk = [record for record in records if str(record["base_date"]) in dates]
        if not chunk:
            continue
        avg_return = sum(item["net_return_pct"] for item in chunk) / len(chunk)
        win_rate = sum(1 for item in chunk if item["net_return_pct"] > 0) / len(chunk)
        chunks.append(avg_return + win_rate * 2.0)
    return base_score + (min(chunks) * 0.25 if chunks else 0.0)


def invariant_block(active: dict[str, Any], optimization: dict[str, Any]) -> dict[str, Any]:
    safety = DEFAULT_SAFETY_INVARIANTS.copy()
    safety.update(active.get("safety_invariants", {}))
    safety.update(optimization.get("safety_invariants", {}))
    if safety.get("automatic_trading_enabled") is not False:
        raise SystemExit("Refusing optimization because automatic_trading_enabled must be false")
    safety["automatic_trading_enabled"] = False
    for key in IMMUTABLE_TRUE_INVARIANTS:
        if safety.get(key) is not True:
            raise SystemExit(f"Refusing optimization because safety invariant {key} must be true")
        safety[key] = True
    return safety


def active_strategy_toml(
    active: dict[str, Any],
    weights: dict[str, float],
    safety: dict[str, Any],
    cost_gate: dict[str, Any],
    champion_id: str,
) -> str:
    lines = [
        "# Active investment ranking strategy. Defaults are intentionally conservative.",
        "",
        f"strategy_id = \"{champion_id}\"",
        f"strategy_version = \"{champion_id}\"",
        "status = \"active\"",
        "description = \"Conservative Level 5 MVP ranking strategy for research-only HK stock/ETF recommendations.\"",
        f"last_optimized_at = \"{utc_now()}\"",
        "",
        "[weights]",
    ]
    for key in DEFAULT_STRATEGY_WEIGHTS:
        lines.append(f"{key} = {weights[key]:.4f}")
    lines.extend(["", "[cost_gate]"])
    lines.append(f"estimated_round_trip_bps = {float(cost_gate.get('estimated_round_trip_bps', 35)):.0f}")
    lines.append(f"minimum_edge_bps = {float(cost_gate.get('minimum_edge_bps', 100)):.0f}")
    lines.extend(["", "[safety_invariants]"])
    for key in sorted(safety):
        value = safety[key]
        if isinstance(value, bool):
            lines.append(f"{key} = {str(value).lower()}")
        else:
            lines.append(f"{key} = \"{value}\"")
    _ = active
    return "\n".join(lines) + "\n"


def write_markdown(path: pathlib.Path, result: dict[str, Any]) -> None:
    lines = [
        "# Investment Parameter Optimization",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Updated active strategy: `{result['updated_active_strategy']}`",
        f"Reason: {result['decision_reason']}",
        "",
        "## Champion",
    ]
    champion = result.get("champion", {})
    if champion:
        summary = champion["summary"]
        lines.extend(
            [
                f"- strategy: `{champion['strategy_version']}`",
                f"- robust_score: `{champion['robust_score']}`",
                f"- samples: `{summary['sample_count']}`",
                f"- avg_net_return_pct: `{summary['avg_net_return_pct']}`",
                f"- win_rate: `{summary['win_rate']}`",
                f"- avg_alpha_pct: `{summary['avg_alpha_pct']}`",
                f"- sample_quality: `{summary.get('sample_quality')}`",
                f"- avg_max_adverse_pct: `{summary.get('avg_max_adverse_pct')}`",
                f"- max_adverse_pct: `{summary['max_adverse_pct']}`",
                f"- adverse_breach_rate: `{summary.get('adverse_breach_rate')}`",
            ]
        )
    lines.extend(["", "## Challenger Candidates"])
    for item in result.get("top_candidates", [])[:10]:
        summary = item["summary"]
        lines.append(
            f"- `{item['strategy_version']}` score={item['robust_score']} samples={summary['sample_count']} "
            f"quality={summary.get('sample_quality')} avg={summary['avg_net_return_pct']}% win={summary['win_rate']} "
            f"alpha={summary['avg_alpha_pct']}% adverse_breach={summary.get('adverse_breach_rate')}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize whitelisted investment ranking parameters.")
    parser.add_argument("--config", default=str(ROOT / "config" / "optimization.toml"))
    parser.add_argument("--as-of-date", default=None, help="Only use samples whose future leg is available by this date.")
    parser.add_argument("--session", default="close", choices=["morning", "midday", "close", "historical"])
    args = parser.parse_args()

    opt_path = pathlib.Path(args.config)
    opt = read_toml(opt_path)
    if not bool(opt.get("enabled", True)):
        print("Investment parameter optimization disabled by config.")
        return 0
    active_path = ROOT / opt.get("active_strategy", "config/active_strategy.toml")
    registry_path = ROOT / opt.get("snapshot_registry", "data/snapshots/registry.json")
    output_dir = ROOT / opt.get("output_dir", "research/experiments")
    output_dir.mkdir(parents=True, exist_ok=True)

    active = load_strategy_config(active_path)
    active_raw = read_toml(active_path)
    safety = invariant_block(active, opt)
    as_of_date = parse_date(args.as_of_date)

    diagnostic_top_n = int(opt.get("diagnostic_top_n", opt.get("top_n", 3)))
    actionable_top_n = int(opt.get("actionable_top_n", opt.get("top_n", 1)))
    top_n = diagnostic_top_n
    horizon_days = int(opt.get("horizon_days", 3))
    round_trip_bps = float(opt.get("round_trip_bps", 35))
    minimum_edge_bps = float(opt.get("minimum_edge_bps", 100))
    active_cost_gate = active_raw.get("cost_gate", {})
    if safety.get("forbid_cost_gate_reduction"):
        round_trip_bps = max(round_trip_bps, float(active_cost_gate.get("estimated_round_trip_bps", round_trip_bps)))
    if safety.get("forbid_edge_gate_reduction"):
        minimum_edge_bps = max(minimum_edge_bps, float(active_cost_gate.get("minimum_edge_bps", minimum_edge_bps)))
    benchmark_symbol = str(opt.get("benchmark_symbol", "2800.HK"))
    min_watch_score = float(opt.get("min_watch_score", 45))
    min_action_score = float(opt.get("min_action_score", 65))
    min_samples = int(opt.get("min_samples", 30))
    min_improvement_bps = float(opt.get("min_improvement_bps", 25))
    min_win_rate = float(opt.get("min_win_rate", 0.45))
    max_adverse_limit_pct = float(opt.get("max_adverse_limit_pct", -8.0))
    max_adverse_breach_rate = float(opt.get("max_adverse_breach_rate", 0.25))
    candidate_policy = str(opt.get("candidate_policy", "strict"))
    if candidate_policy == "strict_with_fallback":
        candidate_policy = "relaxed"
    if candidate_policy not in {"strict", "relaxed"}:
        raise SystemExit("candidate_policy must be strict, relaxed, or strict_with_fallback")
    window_count = min(int(opt.get("walk_forward_windows", 3)), max(1, trade_entry_count(registry_path)))
    promotion = opt.get("promotion", {})
    promotion_enabled = bool(promotion.get("enabled", True))
    promotion_sessions = set(promotion.get("sessions", ["close", "historical"]))

    results = []
    baseline = backtest(
        registry_path,
        active["strategy_version"],
        active["weights"],
        top_n,
        horizon_days,
        round_trip_bps,
        benchmark_symbol,
        min_watch_score,
        min_action_score,
        candidate_policy,
        min_samples,
        max_adverse_limit_pct,
        as_of_date,
        actionable_top_n,
        diagnostic_top_n,
        minimum_edge_bps,
    )
    baseline_score = robust_score(baseline, window_count)
    results.append({"strategy_version": active["strategy_version"], "weights": active["weights"], "summary": baseline["summary"], "robust_score": round(baseline_score, 4)})

    for index, weights in enumerate(candidate_weights(opt.get("search", {})), start=1):
        version = f"challenger_{index:03d}"
        candidate = backtest(
            registry_path,
            version,
            weights,
            top_n,
            horizon_days,
            round_trip_bps,
            benchmark_symbol,
            min_watch_score,
            min_action_score,
            candidate_policy,
            min_samples,
            max_adverse_limit_pct,
            as_of_date,
            actionable_top_n,
            diagnostic_top_n,
            minimum_edge_bps,
        )
        score = robust_score(candidate, window_count)
        results.append({"strategy_version": version, "weights": weights, "summary": candidate["summary"], "robust_score": round(score, 4)})

    ranked = sorted(results, key=lambda item: item["robust_score"], reverse=True)
    champion = ranked[0] if ranked else None
    updated = False
    decision_reason = "No valid champion candidate found."
    if champion:
        summary = champion["summary"]
        improvement_bps = (float(summary.get("avg_net_return_pct") or 0.0) - float(baseline["summary"].get("avg_net_return_pct") or 0.0)) * 100.0
        has_samples = int(summary.get("sample_count") or 0) >= min_samples
        has_improvement = improvement_bps >= min_improvement_bps
        has_win_rate = float(summary.get("win_rate") or 0.0) >= min_win_rate
        adverse = summary.get("max_adverse_pct")
        has_adverse = adverse is None or float(adverse) >= max_adverse_limit_pct
        adverse_breach_rate = summary.get("adverse_breach_rate")
        has_adverse_breach_rate = adverse_breach_rate is None or float(adverse_breach_rate) <= max_adverse_breach_rate
        has_sample_quality = summary.get("sample_quality") == "sufficient"
        is_challenger = champion["strategy_version"] != active["strategy_version"]
        can_promote_session = args.session in promotion_sessions
        if is_challenger and promotion_enabled and can_promote_session and has_samples and has_improvement and has_win_rate and has_adverse and has_adverse_breach_rate and has_sample_quality:
            champion_id = f"l5_mvp_optimized_{dt.date.today().isoformat().replace('-', '')}"
            active_cost_gate = active_raw.get("cost_gate", {})
            cost_gate = {
                "estimated_round_trip_bps": max(round_trip_bps, float(active_cost_gate.get("estimated_round_trip_bps", 35))),
                "minimum_edge_bps": max(float(opt.get("minimum_edge_bps", 100)), float(active_cost_gate.get("minimum_edge_bps", 100))),
            }
            active_path.write_text(active_strategy_toml(active, champion["weights"], safety, cost_gate, champion_id), encoding="utf-8")
            updated = True
            decision_reason = f"Promoted challenger with {improvement_bps:.1f} bps average-return improvement."
        else:
            decision_reason = (
                "Kept active strategy; gates: "
                f"challenger={is_challenger}, promotion={promotion_enabled}, session={can_promote_session}, samples={has_samples}, improvement={has_improvement}, "
                f"win_rate={has_win_rate}, adverse={has_adverse}, adverse_breach_rate={has_adverse_breach_rate}, sample_quality={has_sample_quality}."
            )

    output = {
        "generated_at": utc_now(),
        "config": str(opt_path),
        "active_strategy": str(active_path),
        "as_of_date": args.as_of_date,
        "session": args.session,
        "candidate_policy": candidate_policy,
        "max_adverse_limit_pct": max_adverse_limit_pct,
        "max_adverse_breach_rate": max_adverse_breach_rate,
        "updated_active_strategy": updated,
        "decision_reason": decision_reason,
        "baseline": results[0] if results else None,
        "champion": champion,
        "top_candidates": ranked[:10],
        "safety_invariants": safety,
    }
    json_path = output_dir / "latest_optimization.json"
    md_path = output_dir / "latest_optimization.md"
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    write_markdown(md_path, output)
    print(f"Wrote optimization: {json_path}")
    print(decision_reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
