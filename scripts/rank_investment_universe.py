#!/usr/bin/env python3

import argparse
import json
import pathlib
import tomllib
from collections import defaultdict
from typing import Any


DEFAULT_STRATEGY_VERSION = "legacy-default"
DEFAULT_STRATEGY_WEIGHTS = {
    "trend_weight": 0.45,
    "momentum_weight": 0.35,
    "range_weight": 0.20,
    "risk_penalty_weight": 1.0,
}
DEFAULT_SAFETY_INVARIANTS = {
    "automatic_trading_enabled": False,
    "forbid_cost_gate_reduction": True,
    "forbid_edge_gate_reduction": True,
    "forbid_history_tampering": True,
}


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_symbol_risk(path: pathlib.Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    data = load_json(path)
    raw_symbols = data.get("symbols", data)
    if not isinstance(raw_symbols, dict):
        return {}
    return {str(symbol): value for symbol, value in raw_symbols.items() if isinstance(value, dict)}


def load_strategy_config(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None:
        return {
            "strategy_id": DEFAULT_STRATEGY_VERSION,
            "strategy_version": DEFAULT_STRATEGY_VERSION,
            "status": "implicit",
            "weights": DEFAULT_STRATEGY_WEIGHTS.copy(),
            "safety_invariants": DEFAULT_SAFETY_INVARIANTS.copy(),
        }

    with path.open("rb") as fh:
        data = tomllib.load(fh)
    weights = DEFAULT_STRATEGY_WEIGHTS.copy()
    weights.update({key: float(value) for key, value in data.get("weights", {}).items() if key in weights})
    safety = DEFAULT_SAFETY_INVARIANTS.copy()
    safety.update(data.get("safety_invariants", {}))
    return {
        "strategy_id": str(data.get("strategy_id") or path.stem),
        "strategy_version": str(data.get("strategy_version") or data.get("strategy_id") or path.stem),
        "status": str(data.get("status") or "unknown"),
        "weights": weights,
        "cost_gate": data.get("cost_gate", {}),
        "safety_invariants": safety,
    }


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def trend_score(item: dict[str, Any]) -> float:
    price = float(item.get("latest_close") or 0)
    ma20 = float(item.get("ma20") or 0)
    ma60 = float(item.get("ma60") or 0)
    if not price or not ma20 or not ma60:
        return 0.0
    score = 0.0
    score += 25 if price >= ma20 else max(0.0, 25 + ((price / ma20) - 1.0) * 250)
    score += 25 if price >= ma60 else max(0.0, 25 + ((price / ma60) - 1.0) * 200)
    if ma20 >= ma60:
        score += 20
    score += clamp(float(item.get("range_pos_60") or 0) * 30, 0, 30)
    return clamp(score, 0, 100)


def momentum_score(item: dict[str, Any]) -> float:
    pct = float(item.get("pct_change_1d") or 0)
    volume_ratio = item.get("volume_ratio_20")
    volume_ratio = float(volume_ratio) if volume_ratio is not None else 0.0
    score = 50 + pct * 8
    score += clamp((volume_ratio - 1.0) * 20, -15, 25)
    return clamp(score, 0, 100)


def risk_penalty(item: dict[str, Any]) -> float:
    penalty = 0.0
    flags = set(item.get("regime_flags") or [])
    if "downtrend" in flags:
        penalty += 25
    price = float(item.get("latest_close") or 0)
    ma20 = float(item.get("ma20") or 0)
    ma60 = float(item.get("ma60") or 0)
    if float(item.get("range_pos_60") or 0) < 0.15:
        penalty += 12
    if item.get("volume_ratio_20") is not None and float(item["volume_ratio_20"]) < 0.6:
        penalty += 12
    if price and ma20 and ma60 and price < ma20 and price < ma60:
        penalty += 15
    return penalty


def qualification_signals(item: dict[str, Any], score: float, min_watch_score: float) -> tuple[list[str], list[str]]:
    flags = set(item.get("regime_flags") or [])
    price = float(item.get("latest_close") or 0)
    ma20 = float(item.get("ma20") or 0)
    ma60 = float(item.get("ma60") or 0)
    range_pos = float(item.get("range_pos_60") or 0)
    volume_ratio = item.get("volume_ratio_20")
    volume_ratio = float(volume_ratio) if volume_ratio is not None else None

    qualification_flags = []
    disqualifiers = []
    if score >= min_watch_score:
        qualification_flags.append("score_meets_watch_threshold")
    else:
        qualification_flags.append("below_watch_score")
    if price and ma20 and price >= ma20:
        qualification_flags.append("price_above_ma20")
    if price and ma60 and price >= ma60:
        qualification_flags.append("price_above_ma60")
    if ma20 and ma60 and ma20 >= ma60:
        qualification_flags.append("ma20_above_ma60")
    if volume_ratio is not None and volume_ratio >= 1.0:
        qualification_flags.append("volume_confirmed")
    if range_pos >= 0.35:
        qualification_flags.append("constructive_range_position")

    if volume_ratio is not None and volume_ratio < 0.6:
        disqualifiers.append("low_volume_ratio_20_below_0_6")
    if "downtrend" in flags:
        disqualifiers.append("downtrend_regime")
    if range_pos < 0.12:
        disqualifiers.append("range_pos_60_below_0_12")
    if price and ma20 and ma60 and price < ma20 and price < ma60:
        disqualifiers.append("price_below_ma20_and_ma60")
    return qualification_flags, disqualifiers


def expected_edge_fields(row: dict[str, Any], round_trip_bps: float, minimum_edge_bps: float) -> dict[str, Any]:
    score = float(row.get("score") or 0.0)
    range_pos = float(row.get("range_pos_60") or 0.0)
    pct_change = float(row.get("pct_change_1d") or 0.0)
    volume_ratio = row.get("volume_ratio_20")
    volume_ratio = float(volume_ratio) if volume_ratio is not None else 0.0
    risk = float(row.get("risk_penalty") or 0.0)

    price = float(row.get("latest_close") or 0.0)
    ma20 = float(row.get("ma20") or 0.0)
    ma60 = float(row.get("ma60") or 0.0)
    flags = set(row.get("regime_flags") or [])

    gross_edge = 0.0
    gross_edge += max(0.0, score - 55.0) * 5.0
    if price and ma20 and price >= ma20:
        gross_edge += 18.0
    if price and ma60 and price >= ma60:
        gross_edge += 24.0
    if ma20 and ma60 and ma20 >= ma60:
        gross_edge += 18.0
    if 0.30 <= range_pos <= 0.80:
        gross_edge += 30.0 * range_pos
    elif range_pos > 0.80:
        gross_edge += 12.0
    gross_edge += clamp(pct_change, -2.0, 3.0) * 6.0
    gross_edge += clamp((volume_ratio - 1.0) * 24.0, -18.0, 24.0)
    gross_edge -= risk * 2.0
    if "downtrend" in flags:
        gross_edge -= 35.0

    expected_edge_bps = round(clamp(gross_edge, 0.0, 300.0), 2)
    net_expected_edge_bps = round(expected_edge_bps - round_trip_bps, 2)
    return {
        "expected_edge_bps": expected_edge_bps,
        "net_expected_edge_bps": net_expected_edge_bps,
        "cost_gate_passed": bool(expected_edge_bps > round_trip_bps and net_expected_edge_bps >= minimum_edge_bps),
        "edge_method": "technical_snapshot_score_v1",
        "evidence_window": "1d_momentum_20d_volume_20d_60d_trend_60d_range",
    }


def apply_edge_cost_fields(ranked: list[dict[str, Any]], round_trip_bps: float, minimum_edge_bps: float) -> None:
    for row in ranked:
        row.update(expected_edge_fields(row, round_trip_bps, minimum_edge_bps))
        if row["cost_gate_passed"]:
            row.setdefault("qualification_flags", []).append("cost_gate_passed")
        else:
            row.setdefault("qualification_flags", []).append("cost_gate_failed")


def item_score(item: dict[str, Any], weights: dict[str, float] | None = None, min_watch_score: float = 45.0) -> dict[str, Any]:
    weights = weights or DEFAULT_STRATEGY_WEIGHTS
    t_score = trend_score(item)
    m_score = momentum_score(item)
    penalty = risk_penalty(item)
    total = clamp(
        t_score * float(weights["trend_weight"])
        + m_score * float(weights["momentum_weight"])
        + float(item.get("range_pos_60") or 0) * 100 * float(weights["range_weight"])
        - penalty * float(weights["risk_penalty_weight"]),
        0,
        100,
    )
    rounded_total = round(total, 2)
    qualification_flags, disqualifiers = qualification_signals(item, rounded_total, min_watch_score)
    qualified_for_watch = rounded_total >= min_watch_score and not disqualifiers
    return {
        "symbol": item.get("symbol"),
        "name": item.get("name"),
        "kind": item.get("kind"),
        "theme": item.get("theme"),
        "score": rounded_total,
        "trend_score": round(t_score, 2),
        "momentum_score": round(m_score, 2),
        "risk_penalty": round(penalty, 2),
        "qualification_flags": qualification_flags,
        "disqualifiers": disqualifiers,
        "qualified_for_watch": qualified_for_watch,
        "diagnostic_only": not qualified_for_watch,
        "latest_close": item.get("latest_close"),
        "pct_change_1d": item.get("pct_change_1d"),
        "ma20": item.get("ma20"),
        "ma60": item.get("ma60"),
        "range_pos_60": item.get("range_pos_60"),
        "volume_ratio_20": item.get("volume_ratio_20"),
        "regime_flags": item.get("regime_flags", []),
        "price_source": item.get("price_source"),
        "quote_trade_time": item.get("quote_trade_time"),
    }


def annotate_theme_positions(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        groups[str(row.get("theme") or "unknown")].append(row)

    for theme_items in groups.values():
        ordered = sorted(theme_items, key=lambda row: row["score"], reverse=True)
        leader = str(ordered[0].get("symbol")) if ordered else None
        for index, row in enumerate(ordered, start=1):
            row["theme_rank"] = index
            row["theme_peer_count"] = len(ordered)
            row["theme_leader"] = leader
            row["is_theme_leader"] = index == 1
            if index != 1:
                row.setdefault("qualification_flags", []).append("same_theme_non_leader")
                row.setdefault("disqualifiers", []).append("not_theme_score_leader")
                row["qualified_for_watch"] = False
                row["diagnostic_only"] = True
    return scored


def theme_summary(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in scored:
        groups[str(item.get("theme") or "unknown")].append(item)

    summaries = []
    for theme, items in groups.items():
        ordered = sorted(items, key=lambda row: row["score"], reverse=True)
        summaries.append(
            {
                "theme": theme,
                "avg_score": round(sum(row["score"] for row in items) / len(items), 2),
                "leader": ordered[0]["symbol"],
                "leader_score": ordered[0]["score"],
                "leader_qualified": bool(ordered[0].get("qualified_for_watch")),
                "members": [row["symbol"] for row in ordered],
            }
        )
    return sorted(summaries, key=lambda row: row["avg_score"], reverse=True)


def apply_action_qualification(ranked: list[dict[str, Any]], min_action_score: float, symbol_risk: dict[str, dict[str, Any]]) -> None:
    for row in ranked:
        symbol = str(row.get("symbol") or "")
        risk = symbol_risk.get(symbol, {})
        reasons = [str(reason) for reason in risk.get("reasons", risk.get("reason", []))] if isinstance(risk.get("reasons", risk.get("reason", [])), list) else []
        row["symbol_risk"] = {
            "action_veto": bool(risk.get("action_veto", False)),
            "reasons": reasons,
            "tags": risk.get("tags", []),
        }
        if row["symbol_risk"]["action_veto"]:
            row.setdefault("disqualifiers", []).append("symbol_risk_veto")
            row["diagnostic_only"] = True
        if not bool(row.get("cost_gate_passed")):
            row.setdefault("disqualifiers", []).append("cost_gate_failed")
            row["diagnostic_only"] = True
        score_ok = float(row.get("score") or 0.0) >= min_action_score
        if score_ok:
            row.setdefault("qualification_flags", []).append("score_meets_action_threshold")
        else:
            row.setdefault("qualification_flags", []).append("below_action_score")
        row["qualified_for_action"] = bool(
            row.get("qualified_for_watch")
            and score_ok
            and row.get("is_theme_leader")
            and row.get("cost_gate_passed")
            and not row["symbol_risk"]["action_veto"]
        )
        if not row["qualified_for_action"]:
            row["diagnostic_only"] = True


def candidate_layers(ranked: list[dict[str, Any]], actionable_top_n: int, diagnostic_top_n: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    actionable = [row for row in ranked if row.get("qualified_for_action")][:actionable_top_n]
    diagnostics = []
    for row in ranked[:diagnostic_top_n]:
        diagnostic = dict(row)
        diagnostic["diagnostic_only"] = not bool(row.get("qualified_for_action"))
        if diagnostic["diagnostic_only"]:
            diagnostic.setdefault("qualification_flags", []).append("diagnostic_candidate")
        diagnostics.append(diagnostic)
    top_candidates = list(actionable)
    seen = {row.get("symbol") for row in top_candidates}
    for row in diagnostics:
        if row.get("symbol") in seen:
            continue
        top_candidates.append(row)
    return actionable, diagnostics, top_candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank a trade universe snapshot with deterministic technical scores.")
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-candidates", type=int, default=8)
    parser.add_argument("--actionable-top-n", type=int, default=1)
    parser.add_argument("--diagnostic-top-n", type=int, default=None)
    parser.add_argument("--top-n", type=int, default=None, help="Legacy alias for --diagnostic-top-n.")
    parser.add_argument("--min-watch-score", type=float, default=45)
    parser.add_argument("--min-action-score", type=float, default=65)
    parser.add_argument("--round-trip-bps", type=float, default=35)
    parser.add_argument("--minimum-edge-bps", type=float, default=100)
    parser.add_argument("--strategy-config", default=None, help="Optional active strategy TOML with ranking weights and safety invariants.")
    parser.add_argument("--symbol-risk-json", default=None, help="Optional symbol risk memory JSON with action_veto tags.")
    args = parser.parse_args()

    snapshot_path = pathlib.Path(args.snapshot)
    snapshot = load_json(snapshot_path)
    strategy = load_strategy_config(pathlib.Path(args.strategy_config) if args.strategy_config else None)
    symbol_risk = load_symbol_risk(pathlib.Path(args.symbol_risk_json) if args.symbol_risk_json else None)
    diagnostic_top_n = args.diagnostic_top_n if args.diagnostic_top_n is not None else (args.top_n if args.top_n is not None else 3)
    scored = annotate_theme_positions([item_score(item, strategy["weights"], args.min_watch_score) for item in snapshot.get("items", [])])
    apply_edge_cost_fields(scored, args.round_trip_bps, args.minimum_edge_bps)
    ranked = sorted(scored, key=lambda row: row["score"], reverse=True)
    apply_action_qualification(ranked, args.min_action_score, symbol_risk)
    actionable_candidates, diagnostic_candidates, top_candidates = candidate_layers(ranked, args.actionable_top_n, diagnostic_top_n)

    output = {
        "snapshot": str(snapshot_path),
        "as_of_date": snapshot.get("as_of_date"),
        "generated_at": snapshot.get("generated_at"),
        "strategy_id": strategy["strategy_id"],
        "strategy_version": strategy["strategy_version"],
        "strategy_status": strategy["status"],
        "strategy_weights": strategy["weights"],
        "safety_invariants": strategy["safety_invariants"],
        "cost_gate": {
            "estimated_round_trip_bps": args.round_trip_bps,
            "minimum_edge_bps": args.minimum_edge_bps,
            "action_rule": "Do not upgrade unless expected swing edge exceeds both cost and minimum edge gates.",
        },
        "thresholds": {
            "min_watch_score": args.min_watch_score,
            "min_action_score": args.min_action_score,
            "actionable_top_n": args.actionable_top_n,
            "diagnostic_top_n": diagnostic_top_n,
        },
        "theme_summary": theme_summary(scored),
        "actionable_candidates": actionable_candidates,
        "diagnostic_candidates": diagnostic_candidates,
        "top_candidates": top_candidates[: args.max_candidates],
        "all_ranked": ranked,
    }
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote ranking: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
