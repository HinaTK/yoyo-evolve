#!/usr/bin/env python3

import argparse
import json
import pathlib
from datetime import datetime, timezone
from typing import Any


CONFIDENCE_RISK_PENALTIES = {
    "low_symbol_pass_rate": 0.06,
    "negative_symbol_avg_return": 0.05,
    "recent_symbol_adverse_breach": 0.06,
    "repeated_symbol_selection_error": 0.05,
    "backtest_adverse_breach": 0.08,
}
WATCH_COMPATIBLE_DISQUALIFIERS = {"cost_gate_failed"}


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def focus_rows(focus_pool: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not focus_pool:
        return {}
    rows = {}
    for key in ("active_focus_symbols", "watch_focus_symbols"):
        for row in focus_pool.get(key, []):
            if isinstance(row, dict) and row.get("symbol"):
                rows[str(row["symbol"])] = row
    for industry in focus_pool.get("industry_ranking", []):
        if not isinstance(industry, dict):
            continue
        for row in industry.get("top_symbols", []):
            if isinstance(row, dict) and row.get("symbol"):
                rows.setdefault(str(row["symbol"]), row)
    return rows


def recommendation_state(row: dict[str, Any], source_layer: str) -> str:
    if (
        source_layer == "actionable_candidates"
        and bool(row.get("qualified_for_action"))
        and bool(row.get("cost_gate_passed"))
        and row.get("same_theme_peer_evidence_passed") is True
        and not row.get("action_disqualifiers")
    ):
        return "buy_candidate"
    if bool(row.get("qualified_for_watch")):
        disqualifiers = {str(item) for item in row.get("disqualifiers", [])}
        if not disqualifiers or disqualifiers <= WATCH_COMPATIBLE_DISQUALIFIERS:
            return "watch_only"
    if source_layer == "startup_candidates" and row.get("startup_watch_candidate") is True:
        return "watch_only"
    return "avoid"


def confidence_penalty(row: dict[str, Any], state: str) -> float:
    penalty = 0.0
    risk = row.get("symbol_risk") if isinstance(row.get("symbol_risk"), dict) else {}
    risk_tags = {str(tag) for tag in risk.get("tags", [])} if isinstance(risk, dict) else set()
    for tag, value in CONFIDENCE_RISK_PENALTIES.items():
        if tag in risk_tags:
            penalty += value
    if row.get("same_theme_peer_evidence_passed") is not True:
        penalty += 0.08
    if row.get("action_disqualifiers"):
        penalty += 0.06
    if row.get("disqualifiers"):
        penalty += 0.08
    if row.get("cost_gate_passed") is False:
        penalty += 0.08
    if state == "buy_candidate":
        return min(penalty, 0.20)
    if state == "watch_only":
        return min(penalty, 0.15)
    return min(penalty, 0.10)


def confidence(row: dict[str, Any], state: str) -> float:
    score = float(row.get("score") or 0.0)
    penalty = confidence_penalty(row, state)
    if state == "buy_candidate":
        return round(max(0.45, min(0.75, 0.50 + (score / 100.0) * 0.25) - penalty), 2)
    if state == "watch_only":
        return round(max(0.25, min(0.55, 0.30 + (score / 100.0) * 0.25) - penalty), 2)
    return round(max(0.15, min(0.45, 0.20 + (score / 100.0) * 0.20) - penalty), 2)


def evidence(row: dict[str, Any], state: str, focus_row: dict[str, Any] | None = None) -> list[str]:
    risk = row.get("symbol_risk") if isinstance(row.get("symbol_risk"), dict) else {}
    nontechnical = row.get("nontechnical_evidence") if isinstance(row.get("nontechnical_evidence"), dict) else {}
    values = [
        f"score={row.get('score')}, trend_score={row.get('trend_score')}, momentum_score={row.get('momentum_score')}",
        f"expected_edge_bps={row.get('expected_edge_bps')}, net_expected_edge_bps={row.get('net_expected_edge_bps')}, cost_gate_passed={row.get('cost_gate_passed')}",
        f"source_layer={row.get('source_layer')}, eligible_for_action_from_layer={row.get('eligible_for_action_from_layer')}, layer_action_cap={row.get('layer_action_cap')}",
        f"market_context proxy={row.get('market_proxy_symbol')}, range_pos_60={row.get('market_range_pos_60')}, max_market_range_for_action={row.get('max_market_range_for_action')}, pct_change_1d={row.get('market_pct_change_1d')}",
        f"same_theme_peer_check theme_rank={row.get('theme_rank')}, theme_leader={row.get('theme_leader')}, is_theme_leader={row.get('is_theme_leader')}, theme_peer_count={row.get('theme_peer_count')}",
        f"same_theme_best_peer_evidence passed={row.get('same_theme_peer_evidence_passed')}, best_symbol={row.get('same_theme_best_symbol')}, best_score={row.get('same_theme_best_score')}, selected_vs_best_score_gap={row.get('same_theme_selected_vs_best_score_gap')}, next_best_symbol={row.get('same_theme_next_best_symbol')}, selected_vs_next_best_score_gap={row.get('same_theme_selected_vs_next_best_score_gap')}, peer_relative_decision={row.get('peer_relative_decision')}",
        f"action_tier={row.get('action_tier')}, action_tier_label={row.get('action_tier_label')}, manual_confirmation_required={row.get('manual_confirmation_required')}",
        f"startup_candidate stage={row.get('startup_candidate_stage')}, label={row.get('startup_candidate_label')}, ma20_distance_pct={row.get('ma20_distance_pct')}, theme_startup={row.get('theme_startup')}",
        f"confidence_calibration penalty={confidence_penalty(row, state)}, symbol_risk_tags={risk.get('tags', [])}, action_disqualifiers={row.get('action_disqualifiers', [])}",
        f"nontechnical_evidence status={nontechnical.get('status')}, total_score={nontechnical.get('total_score')}, event_risk={nontechnical.get('event_risk')}, flags={row.get('nontechnical_evidence_flags', [])}",
        f"latest_close={row.get('latest_close')}, ma20={row.get('ma20')}, ma60={row.get('ma60')}, range_pos_60={row.get('range_pos_60')}, volume_ratio_20={row.get('volume_ratio_20')}",
    ]
    if focus_row:
        values.append(
            f"focus_industry={focus_row.get('focus_industry')} rank={focus_row.get('focus_industry_rank')} score={focus_row.get('focus_industry_score')} role={focus_row.get('focus_role')} focus_state={focus_row.get('focus_state')}"
        )
    return values


def risks(row: dict[str, Any], horizon_days_min: int, horizon_days_max: int) -> list[str]:
    values = [str(item) for item in row.get("disqualifiers", [])]
    values.extend(str(item) for item in row.get("action_disqualifiers", []))
    if row.get("eligible_for_action_from_layer") is False:
        values.append("diagnostic_layer_action_cap_watch_only")
    if row.get("is_theme_leader") is False:
        values.append("same_theme_non_leader_requires_peer_relative_confirmation")
    if row.get("same_theme_peer_evidence_passed") is not True:
        values.append("same_theme_best_peer_evidence_missing_or_failed")
    market_range = row.get("market_range_pos_60")
    market_limit = row.get("max_market_range_for_action")
    if market_range is not None and market_limit is not None and float(market_range) > float(market_limit):
        values.append("market_range_pos_60_above_action_limit")
    if not bool(row.get("cost_gate_passed")):
        values.append("cost_or_minimum_edge_gate_not_met")
    if not values:
        values.append(f"technical signal may fail before the {horizon_days_min}-{horizon_days_max} day horizon")
    return list(dict.fromkeys(values))


def make_recommendation(row: dict[str, Any], horizon_days_min: int, horizon_days_max: int, source_layer: str, focus_row: dict[str, Any] | None = None) -> dict[str, Any]:
    state = recommendation_state(row, source_layer)
    symbol = str(row.get("symbol") or "")
    method = row.get("edge_method") or "technical_snapshot_score_v1"
    recommendation = {
        "symbol": symbol,
        "state": state,
        "theme": row.get("theme") or "unknown",
        "kind": row.get("kind") or "unknown",
        "horizon_days_min": horizon_days_min,
        "horizon_days_max": horizon_days_max,
        "confidence": confidence(row, state),
        "action_tier": row.get("action_tier"),
        "action_tier_label": row.get("action_tier_label"),
        "action_tier_description": row.get("action_tier_description"),
        "action_tier_reasons": row.get("action_tier_reasons", []),
        "startup_candidate_stage": row.get("startup_candidate_stage"),
        "startup_candidate_label": row.get("startup_candidate_label"),
        "startup_candidate_reasons": row.get("startup_candidate_reasons", []),
        "startup_watch_candidate": row.get("startup_watch_candidate") is True,
        "ma20_distance_pct": row.get("ma20_distance_pct"),
        "theme_startup": row.get("theme_startup"),
        "formal_actionable": bool(row.get("formal_actionable")),
        "manual_confirmation_required": row.get("manual_confirmation_required") is not False,
        "rationale": f"Draft {state} generated from deterministic ranking and edge gate fields for {symbol}.",
        "evidence": evidence(row, state, focus_row),
        "risks": risks(row, horizon_days_min, horizon_days_max),
        "invalidation": "Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.",
        "selection_source_theme": row.get("theme") or "unknown",
        "selection_reason": f"source_layer={source_layer} rank_score={row.get('score')} edge_method={method} evidence_window={row.get('evidence_window')} startup_stage={row.get('startup_candidate_stage')}",
    }
    if focus_row:
        recommendation.update(
            {
                "focus_industry": focus_row.get("focus_industry"),
                "focus_industry_name": focus_row.get("focus_industry_name"),
                "focus_industry_score": focus_row.get("focus_industry_score"),
                "focus_industry_rank": focus_row.get("focus_industry_rank"),
                "focus_role": focus_row.get("focus_role"),
                "focus_state": focus_row.get("focus_state"),
            }
        )
        recommendation["selection_reason"] += f" focus_industry={focus_row.get('focus_industry')} focus_rank={focus_row.get('focus_industry_rank')} focus_role={focus_row.get('focus_role')}"
    return recommendation


def ranking_rows_by_symbol(ranking: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for key in ("all_ranked", "top_candidates", "startup_candidates", "diagnostic_candidates", "actionable_candidates"):
        for row in ranking.get(key, []):
            if isinstance(row, dict) and row.get("symbol"):
                rows[str(row["symbol"])] = row
    return rows


def build_calls(
    ranking: dict[str, Any],
    include_diagnostics: bool,
    focus_pool: dict[str, Any] | None = None,
    date: str | None = None,
    session: str | None = None,
    horizon_days_min: int = 14,
    horizon_days_max: int = 90,
) -> dict[str, Any]:
    rows: list[tuple[dict[str, Any], str]] = [(row, "actionable_candidates") for row in ranking.get("actionable_candidates", [])]
    seen = {row.get("symbol") for row, _source_layer in rows}
    if include_diagnostics:
        for row in ranking.get("startup_candidates", []):
            if row.get("symbol") not in seen:
                rows.append((row, "startup_candidates"))
                seen.add(row.get("symbol"))
        for row in ranking.get("diagnostic_candidates", []):
            if row.get("symbol") not in seen:
                rows.append((row, "diagnostic_candidates"))
                seen.add(row.get("symbol"))
    focus_by_symbol = focus_rows(focus_pool)
    ranked_by_symbol = ranking_rows_by_symbol(ranking)
    if include_diagnostics and focus_by_symbol:
        for symbol in focus_by_symbol:
            if symbol in seen:
                continue
            row = ranked_by_symbol.get(symbol)
            if row is None:
                continue
            rows.append((row, "focus_watch_symbols"))
            seen.add(symbol)
    return {
        "date": date or ranking.get("as_of_date"),
        "session": session or ranking.get("as_of_session") or ranking.get("session") or "unknown",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_ranking": ranking.get("snapshot"),
        "strategy_version": ranking.get("strategy_version"),
        "strategy_weights": ranking.get("strategy_weights"),
        "draft_policy": {
            "source": "deterministic_ranking_edge_gate",
            "actionable_rule": "buy_candidate requires qualified_for_action=true, cost_gate_passed=true, and same_theme_peer_evidence_passed=true",
            "tier_rule": "action_tier separates formal_actionable, manual_probe, observe, suspended, and blocked; manual_probe is still research-only and requires human confirmation",
            "startup_rule": "startup_candidates surface theme breadth plus near-MA20 or MA20-reclaim setups as watch_only research candidates, never as automatic buy candidates",
            "confidence_rule": "confidence is capped by score and reduced for adverse symbol risk, failed peer evidence, disqualifiers, and failed edge/cost gates",
        },
        "focus_policy": {
            "source": "dynamic_focus_pool" if focus_pool else None,
            "active_focus_industries": (focus_pool or {}).get("active_focus_industries", []),
            "active_focus_symbol_count": len((focus_pool or {}).get("active_focus_symbols", [])),
            "watch_focus_industries": (focus_pool or {}).get("watch_focus_industries", []),
            "watch_focus_symbol_count": len((focus_pool or {}).get("watch_focus_symbols", [])),
        },
        "recommendations": [make_recommendation(row, horizon_days_min, horizon_days_max, source_layer, focus_by_symbol.get(str(row.get("symbol")))) for row, source_layer in rows],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate schema-valid draft investment calls from a ranking JSON.")
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--date", default=None)
    parser.add_argument("--session", default=None)
    parser.add_argument("--focus-pool", default=None)
    parser.add_argument("--horizon-days-min", type=int, default=14)
    parser.add_argument("--horizon-days-max", type=int, default=90)
    parser.add_argument("--include-diagnostics", action="store_true")
    args = parser.parse_args()

    ranking_path = pathlib.Path(args.ranking)
    focus_pool = load_json(pathlib.Path(args.focus_pool)) if args.focus_pool else None
    calls = build_calls(load_json(ranking_path), args.include_diagnostics, focus_pool, args.date, args.session, args.horizon_days_min, args.horizon_days_max)
    calls["source_ranking"] = str(ranking_path)
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(calls, indent=2), encoding="utf-8")
    print(f"Wrote draft investment calls: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
