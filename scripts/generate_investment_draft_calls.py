#!/usr/bin/env python3

import argparse
import json
import pathlib
from datetime import datetime, timezone
from typing import Any


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def recommendation_state(row: dict[str, Any], source_layer: str) -> str:
    if source_layer == "actionable_candidates" and bool(row.get("qualified_for_action")) and bool(row.get("cost_gate_passed")):
        return "buy_candidate"
    if bool(row.get("qualified_for_watch")) and not row.get("disqualifiers"):
        return "watch_only"
    return "avoid"


def confidence(row: dict[str, Any], state: str) -> float:
    score = float(row.get("score") or 0.0)
    if state == "buy_candidate":
        return round(min(0.75, 0.50 + (score / 100.0) * 0.25), 2)
    if state == "watch_only":
        return round(min(0.55, 0.30 + (score / 100.0) * 0.25), 2)
    return round(min(0.45, 0.20 + (score / 100.0) * 0.20), 2)


def evidence(row: dict[str, Any]) -> list[str]:
    return [
        f"score={row.get('score')}, trend_score={row.get('trend_score')}, momentum_score={row.get('momentum_score')}",
        f"expected_edge_bps={row.get('expected_edge_bps')}, net_expected_edge_bps={row.get('net_expected_edge_bps')}, cost_gate_passed={row.get('cost_gate_passed')}",
        f"latest_close={row.get('latest_close')}, ma20={row.get('ma20')}, ma60={row.get('ma60')}, range_pos_60={row.get('range_pos_60')}, volume_ratio_20={row.get('volume_ratio_20')}",
    ]


def risks(row: dict[str, Any], horizon_days_min: int, horizon_days_max: int) -> list[str]:
    values = [str(item) for item in row.get("disqualifiers", [])]
    if not bool(row.get("cost_gate_passed")):
        values.append("cost_or_minimum_edge_gate_not_met")
    if not values:
        values.append(f"technical signal may fail before the {horizon_days_min}-{horizon_days_max} day horizon")
    return values


def make_recommendation(row: dict[str, Any], horizon_days_min: int, horizon_days_max: int, source_layer: str) -> dict[str, Any]:
    state = recommendation_state(row, source_layer)
    symbol = str(row.get("symbol") or "")
    method = row.get("edge_method") or "technical_snapshot_score_v1"
    return {
        "symbol": symbol,
        "state": state,
        "theme": row.get("theme") or "unknown",
        "kind": row.get("kind") or "unknown",
        "horizon_days_min": horizon_days_min,
        "horizon_days_max": horizon_days_max,
        "confidence": confidence(row, state),
        "rationale": f"Draft {state} generated from deterministic ranking and edge gate fields for {symbol}.",
        "evidence": evidence(row),
        "risks": risks(row, horizon_days_min, horizon_days_max),
        "invalidation": "Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.",
        "selection_source_theme": row.get("theme") or "unknown",
        "selection_reason": f"source_layer={source_layer} rank_score={row.get('score')} edge_method={method} evidence_window={row.get('evidence_window')}",
    }


def build_calls(
    ranking: dict[str, Any],
    include_diagnostics: bool,
    date: str | None = None,
    session: str | None = None,
    horizon_days_min: int = 14,
    horizon_days_max: int = 90,
) -> dict[str, Any]:
    rows: list[tuple[dict[str, Any], str]] = [(row, "actionable_candidates") for row in ranking.get("actionable_candidates", [])]
    seen = {row.get("symbol") for row, _source_layer in rows}
    if include_diagnostics:
        for row in ranking.get("diagnostic_candidates", []):
            if row.get("symbol") not in seen:
                rows.append((row, "diagnostic_candidates"))
                seen.add(row.get("symbol"))
    return {
        "date": date or ranking.get("as_of_date"),
        "session": session or ranking.get("as_of_session") or ranking.get("session") or "unknown",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_ranking": ranking.get("snapshot"),
        "strategy_version": ranking.get("strategy_version"),
        "strategy_weights": ranking.get("strategy_weights"),
        "draft_policy": {
            "source": "deterministic_ranking_edge_gate",
            "actionable_rule": "buy_candidate requires qualified_for_action=true and cost_gate_passed=true",
        },
        "recommendations": [make_recommendation(row, horizon_days_min, horizon_days_max, source_layer) for row, source_layer in rows],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate schema-valid draft investment calls from a ranking JSON.")
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--date", default=None)
    parser.add_argument("--session", default=None)
    parser.add_argument("--horizon-days-min", type=int, default=14)
    parser.add_argument("--horizon-days-max", type=int, default=90)
    parser.add_argument("--include-diagnostics", action="store_true")
    args = parser.parse_args()

    ranking_path = pathlib.Path(args.ranking)
    calls = build_calls(load_json(ranking_path), args.include_diagnostics, args.date, args.session, args.horizon_days_min, args.horizon_days_max)
    calls["source_ranking"] = str(ranking_path)
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(calls, indent=2), encoding="utf-8")
    print(f"Wrote draft investment calls: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
