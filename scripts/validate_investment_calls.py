#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys
import tomllib
from typing import Any


REQUIRED_TOP_LEVEL = ["date", "session", "recommendations"]
REQUIRED_RECOMMENDATION_FIELDS = [
    "symbol",
    "state",
    "theme",
    "kind",
    "horizon_days_min",
    "horizon_days_max",
    "confidence",
    "rationale",
    "evidence",
    "risks",
    "invalidation",
    "selection_source_theme",
    "selection_reason",
]
VALID_STATES = {"watch_only", "buy_candidate", "accumulate", "hold", "trim", "sell_candidate", "avoid"}
ACTIONABLE_STATES = {"buy_candidate", "accumulate", "hold"}
NON_DIAGNOSTIC_STATES = ACTIONABLE_STATES | {"trim", "sell_candidate"}
STATE_RANK = {"avoid": 0, "watch_only": 1, "sell_candidate": 2, "trim": 2, "buy_candidate": 2, "accumulate": 3, "hold": 3}
ALLOWED_FINAL_STATES_BY_CAP = {
    "avoid": {"avoid"},
    "watch_only": {"watch_only", "avoid"},
    "buy_candidate": {"buy_candidate", "watch_only", "avoid"},
    "accumulate": {"accumulate", "buy_candidate", "watch_only", "avoid"},
    "hold": {"hold", "watch_only", "avoid"},
    "trim": {"trim", "watch_only", "avoid"},
    "sell_candidate": {"sell_candidate", "trim", "watch_only", "avoid"},
}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def trade_universe_symbols(path: pathlib.Path) -> set[str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return {str(item.get("symbol")) for item in data.get("symbols", []) if item.get("symbol")}


def ranking_rows(ranking: dict[str, Any]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    actionable_symbols = {str(row.get("symbol")) for row in ranking.get("actionable_candidates", []) if row.get("symbol")}
    rows: dict[str, dict[str, Any]] = {}
    for key in ("all_ranked", "top_candidates", "diagnostic_candidates", "actionable_candidates"):
        for row in ranking.get(key, []):
            symbol = row.get("symbol")
            if symbol:
                rows[str(symbol)] = row
    return actionable_symbols, rows


def draft_rows(draft_calls: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not draft_calls:
        return {}
    rows = {}
    for rec in draft_calls.get("recommendations", []):
        if isinstance(rec, dict) and rec.get("symbol"):
            rows[str(rec["symbol"])] = rec
    return rows


def risk_review_rows(risk_review: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not risk_review:
        return {}
    rows = {}
    for verdict in risk_review.get("verdicts", []):
        if isinstance(verdict, dict) and verdict.get("symbol"):
            rows[str(verdict["symbol"])] = verdict
    return rows


def state_allowed_under_cap(state: str, cap: str) -> bool:
    allowed = ALLOWED_FINAL_STATES_BY_CAP.get(cap)
    if allowed is None:
        return False
    return state in allowed


def validate(
    calls: dict[str, Any],
    ranking: dict[str, Any],
    symbols: set[str],
    draft_calls: dict[str, Any] | None = None,
    risk_review: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TOP_LEVEL:
        if field not in calls:
            errors.append(f"missing top-level field: {field}")

    recommendations = calls.get("recommendations")
    if not isinstance(recommendations, list):
        errors.append("top-level recommendations must be a list")
        return errors

    actionable_symbols, rows = ranking_rows(ranking)
    drafts = draft_rows(draft_calls)
    risk_verdicts = risk_review_rows(risk_review)
    for index, rec in enumerate(recommendations):
        prefix = f"recommendations[{index}]"
        if not isinstance(rec, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in REQUIRED_RECOMMENDATION_FIELDS:
            if field not in rec:
                errors.append(f"{prefix} missing field: {field}")

        symbol = rec.get("symbol")
        state = rec.get("state")
        if symbol not in symbols:
            errors.append(f"{prefix}.symbol {symbol!r} is not in trade universe")
        if state not in VALID_STATES:
            errors.append(f"{prefix}.state {state!r} is not valid")

        confidence = rec.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            errors.append(f"{prefix}.confidence must be a number between 0 and 1")
        if not isinstance(rec.get("evidence"), list):
            errors.append(f"{prefix}.evidence must be a list")
        if not isinstance(rec.get("risks"), list):
            errors.append(f"{prefix}.risks must be a list")

        row = rows.get(str(symbol))
        draft = drafts.get(str(symbol))
        risk_verdict = risk_verdicts.get(str(symbol))
        if draft is not None and state in STATE_RANK:
            draft_state = draft.get("state")
            if draft_state not in STATE_RANK:
                errors.append(f"{prefix} draft state {draft_state!r} is not valid")
            elif not state_allowed_under_cap(str(state), str(draft_state)):
                errors.append(f"{prefix}.{state} state upgrades beyond deterministic draft state {draft_state}")
            draft_confidence = draft.get("confidence")
            if (
                isinstance(confidence, (int, float))
                and not isinstance(confidence, bool)
                and isinstance(draft_confidence, (int, float))
                and not isinstance(draft_confidence, bool)
                and confidence > draft_confidence + 0.001
            ):
                errors.append(f"{prefix}.confidence exceeds deterministic draft confidence cap {draft_confidence}")
        elif draft_calls is not None and state in NON_DIAGNOSTIC_STATES:
            errors.append(f"{prefix}.{state} state requires matching deterministic draft call")
        if risk_review is not None:
            if risk_verdict is None and state in NON_DIAGNOSTIC_STATES:
                errors.append(f"{prefix}.{state} state requires matching deterministic risk verdict")
            elif risk_verdict is not None:
                cap = risk_verdict.get("final_state_cap")
                if cap not in STATE_RANK:
                    errors.append(f"{prefix} risk final_state_cap {cap!r} is not valid")
                elif state in STATE_RANK and not state_allowed_under_cap(str(state), str(cap)):
                    errors.append(f"{prefix}.{state} state exceeds deterministic risk final_state_cap {cap}")
        if state in NON_DIAGNOSTIC_STATES:
            if row is None:
                errors.append(f"{prefix}.{state} state requires a ranking row")
            elif bool(row.get("diagnostic_only")) or not bool(row.get("qualified_for_watch")):
                errors.append(f"{prefix}.{state} state is forbidden for diagnostic or non-watch ranking row")

        if state in ACTIONABLE_STATES:
            if symbol not in actionable_symbols:
                errors.append(f"{prefix} actionable state requires symbol in ranking actionable_candidates")
            if row is None:
                errors.append(f"{prefix} actionable state requires a ranking row")
                continue
            if not bool(row.get("qualified_for_action")):
                errors.append(f"{prefix} actionable state requires qualified_for_action=true")
            if bool(row.get("diagnostic_only")):
                errors.append(f"{prefix} actionable state is forbidden for diagnostic_only ranking row")
            if not bool(row.get("qualified_for_watch")):
                errors.append(f"{prefix} actionable state is forbidden when qualified_for_watch=false")
            if row.get("cost_gate_passed") is False:
                errors.append(f"{prefix} actionable state is forbidden when cost_gate_passed=false")
            for field in ("expected_edge_bps", "net_expected_edge_bps", "cost_gate_passed", "edge_method", "evidence_window"):
                if field not in row:
                    errors.append(f"{prefix} actionable state requires ranking field {field}")
            if row.get("cost_gate_passed") is not True:
                errors.append(f"{prefix} actionable state requires cost_gate_passed=true")
            if not isinstance(row.get("expected_edge_bps"), (int, float)) or isinstance(row.get("expected_edge_bps"), bool):
                errors.append(f"{prefix} actionable state requires numeric expected_edge_bps")
            if not isinstance(row.get("net_expected_edge_bps"), (int, float)) or isinstance(row.get("net_expected_edge_bps"), bool):
                errors.append(f"{prefix} actionable state requires numeric net_expected_edge_bps")
            for field in (
                "same_theme_peer_evidence_passed",
                "same_theme_best_symbol",
                "same_theme_best_score",
                "same_theme_selected_vs_best_score_gap",
                "peer_relative_decision",
            ):
                if field not in row:
                    errors.append(f"{prefix} actionable state requires ranking field {field}")
            if row.get("same_theme_peer_evidence_passed") is not True:
                errors.append(f"{prefix} actionable state requires same_theme_peer_evidence_passed=true")
            if row.get("is_theme_leader") is not True:
                errors.append(f"{prefix} actionable state requires is_theme_leader=true")
            if row.get("theme_rank") != 1:
                errors.append(f"{prefix} actionable state requires theme_rank=1")
            if row.get("theme_leader") != str(symbol):
                errors.append(f"{prefix} actionable state requires theme_leader to match symbol")
            if row.get("same_theme_best_symbol") != str(symbol):
                errors.append(f"{prefix} actionable state requires same_theme_best_symbol to match symbol")
            if row.get("peer_relative_decision") not in {"theme_leader", "sole_theme_candidate"}:
                errors.append(f"{prefix} actionable state requires peer_relative_decision=theme_leader or sole_theme_candidate")
            selected_vs_best = row.get("same_theme_selected_vs_best_score_gap")
            if not isinstance(selected_vs_best, (int, float)) or isinstance(selected_vs_best, bool):
                errors.append(f"{prefix} actionable state requires numeric same_theme_selected_vs_best_score_gap")
            elif selected_vs_best < 0:
                errors.append(f"{prefix} actionable state requires selected score to be at least same-theme best score")
            market_range = row.get("market_range_pos_60")
            market_limit = row.get("max_market_range_for_action")
            if market_range is not None and market_limit is not None:
                if not isinstance(market_range, (int, float)) or isinstance(market_range, bool):
                    errors.append(f"{prefix} actionable state requires numeric market_range_pos_60")
                elif not isinstance(market_limit, (int, float)) or isinstance(market_limit, bool):
                    errors.append(f"{prefix} actionable state requires numeric max_market_range_for_action")
                elif market_range > market_limit:
                    errors.append(f"{prefix} actionable state requires market_range_pos_60 <= max_market_range_for_action")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate structured investment calls against ranking and trade universe constraints.")
    parser.add_argument("--calls", required=True)
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--trade-universe", required=True)
    parser.add_argument("--draft-calls", default=None, help="Optional deterministic draft calls JSON to enforce no-upgrade policy.")
    parser.add_argument("--risk-review", default=None, help="Optional deterministic risk review JSON to enforce final state caps.")
    args = parser.parse_args()

    errors = validate(
        load_json(pathlib.Path(args.calls)),
        load_json(pathlib.Path(args.ranking)),
        trade_universe_symbols(pathlib.Path(args.trade_universe)),
        load_json(pathlib.Path(args.draft_calls)) if args.draft_calls else None,
        load_json(pathlib.Path(args.risk_review)) if args.risk_review else None,
    )
    if errors:
        print("Investment calls validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Investment calls validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
