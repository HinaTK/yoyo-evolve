#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import tomllib
from typing import Any


SEVERE_DISQUALIFIERS = {
    "downtrend_regime",
    "symbol_risk_veto",
    "diagnostic_only",
    "not_qualified_for_watch",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile(path: pathlib.Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def ranking_rows(ranking: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for key in ("all_ranked", "actionable_candidates", "top_candidates", "diagnostic_candidates"):
        for row in ranking.get(key, []):
            symbol = row.get("symbol")
            if symbol:
                rows[str(symbol)] = row
    return rows


def symbol_risk_rows(symbol_risk: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not symbol_risk:
        return {}
    rows = symbol_risk.get("symbols")
    if isinstance(rows, dict):
        return {str(symbol): value for symbol, value in rows.items() if isinstance(value, dict)}
    return {str(symbol): value for symbol, value in symbol_risk.items() if isinstance(value, dict)}


def as_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def unique(values: list[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output


def base_tags(row: dict[str, Any] | None, risk_row: dict[str, Any] | None) -> list[str]:
    tags: list[str] = []
    if row:
        tags.extend(str(item) for item in row.get("disqualifiers", []) if item)
        tags.extend(str(item) for item in row.get("action_disqualifiers", []) if item)
        if row.get("diagnostic_only") is True:
            tags.append("diagnostic_only")
        if row.get("qualified_for_watch") is False:
            tags.append("not_qualified_for_watch")
        if row.get("qualified_for_action") is False:
            tags.append("not_qualified_for_action")
        if row.get("cost_gate_passed") is False:
            tags.append("cost_gate_failed")
        if row.get("same_theme_peer_evidence_passed") is not True:
            tags.append("same_theme_best_peer_evidence_missing_or_failed")
        if as_float(row.get("volume_ratio_20"), 0.0) < 1.0:
            tags.append("volume_ratio_20_below_1_0")
        if has_downtrend(row):
            tags.append("downtrend_regime")
    else:
        tags.append("missing_ranking_row")
    if risk_row:
        tags.extend(str(item) for item in risk_row.get("tags", []) if item)
        if risk_row.get("action_veto") is True:
            tags.append("symbol_risk_veto")
    return unique(tags)


def has_downtrend(row: dict[str, Any]) -> bool:
    disqualifiers = {str(item) for item in row.get("disqualifiers", [])}
    regime_flags = {str(item) for item in row.get("regime_flags", [])}
    return "downtrend_regime" in disqualifiers or "downtrend" in regime_flags or "downtrend_regime" in regime_flags


def confirmations_for(tags: list[str], final_state_cap: str) -> list[str]:
    confirmations: list[str] = []
    if "not_qualified_for_action" in tags:
        confirmations.append("ranking row must regain qualified_for_action=true")
    if "cost_gate_failed" in tags:
        confirmations.append("expected edge must pass the cost gate")
    if "volume_ratio_20_below_1_0" in tags:
        confirmations.append("volume_ratio_20 must be at least 1.0")
    if "same_theme_best_peer_evidence_missing_or_failed" in tags:
        confirmations.append("same-theme best-peer evidence must pass")
    if "market_range_pos_60_above_action_limit" in tags:
        confirmations.append("market proxy range_pos_60 must fall below the action limit")
    if "quote_trade_date_mismatch" in tags or "quote_trade_date_missing" in tags:
        confirmations.append("quote freshness must match the ranking snapshot date")
    if "hk_halt_or_no_turnover_suspected" in tags:
        confirmations.append("HK turnover and quote activity must confirm the instrument is trading normally")
    if "cn_limit_up_chase_block" in tags or "cn_limit_down_liquidity_block" in tags:
        confirmations.append("A-share limit-board condition must clear before action upgrade")
    if any(tag.startswith("nontechnical_") or tag.startswith("event_risk_") for tag in tags):
        confirmations.append("fresh fundamentals, valuation, catalyst, capital-flow, macro, and event-risk evidence must pass before action upgrade")
    if "downtrend_regime" in tags:
        confirmations.append("downtrend regime must clear")
    if final_state_cap == "buy_candidate" and not confirmations:
        confirmations.append("maintain qualified_for_action=true, cost_gate_passed=true, volume_ratio_20>=1.0, and no downtrend_regime")
        confirmations.append("maintain same_theme_peer_evidence_passed=true")
    return unique(confirmations)


def make_verdict(draft: dict[str, Any], row: dict[str, Any] | None, risk_row: dict[str, Any] | None, max_single_position_pct: float) -> dict[str, Any]:
    symbol = str(draft.get("symbol") or "")
    draft_state = str(draft.get("state") or "avoid")
    tags = base_tags(row, risk_row)
    reasons: list[str] = []

    if risk_row and risk_row.get("reasons"):
        reasons.extend(str(reason) for reason in risk_row.get("reasons", []))

    if risk_row and risk_row.get("action_veto") is True:
        decision = "veto"
        cap = "avoid"
        max_position = 0.0
        reasons.append("symbol risk memory has action_veto=true")
    elif draft_state == "avoid":
        decision = "veto"
        cap = "avoid"
        max_position = 0.0
        reasons.append("deterministic draft state is avoid")
    elif draft_state == "watch_only":
        decision = "pass"
        cap = "watch_only"
        max_position = 0.0
        reasons.append("deterministic draft state is watch_only, so final state is capped at watch_only")
    elif draft_state == "buy_candidate":
        severe = row is None or any(tag in SEVERE_DISQUALIFIERS for tag in tags)
        qualifies = bool(row and row.get("qualified_for_action") is True)
        cost_passed = bool(row and row.get("cost_gate_passed") is True)
        peer_evidence_ok = bool(row and row.get("same_theme_peer_evidence_passed") is True)
        action_checks_clear = bool(row and not row.get("action_disqualifiers"))
        volume_ok = bool(row and as_float(row.get("volume_ratio_20"), 0.0) >= 1.0)
        # Fold peer evidence into the existing action gate so missing evidence cannot pass.
        volume_ok = volume_ok and peer_evidence_ok and action_checks_clear
        trend_ok = bool(row and not has_downtrend(row))
        if qualifies and cost_passed and volume_ok and trend_ok:
            decision = "pass"
            cap = "buy_candidate"
            max_position = max_single_position_pct
            reasons.append("buy_candidate passes action, cost, volume, and trend gates")
            reasons.append("buy_candidate passes same-theme peer evidence gate")
        elif severe:
            decision = "veto"
            cap = "avoid"
            max_position = 0.0
            reasons.append("buy_candidate has severe deterministic risk disqualifier")
        else:
            decision = "downgrade"
            cap = "watch_only"
            max_position = round(max_single_position_pct * 0.5, 4)
            reasons.append("buy_candidate failed one or more action hardening checks and is downgraded to watch_only")
    else:
        decision = "veto"
        cap = "avoid"
        max_position = 0.0
        reasons.append(f"unsupported deterministic draft state {draft_state!r}")

    return {
        "symbol": symbol,
        "draft_state": draft_state,
        "risk_decision": decision,
        "final_state_cap": cap,
        "max_position_pct": min(round(max_position, 4), max_single_position_pct),
        "position_policy": "recommendation_cap_only",
        "execution_allowed": False,
        "risk_tags": tags,
        "reasons": unique(reasons),
        "required_confirmations": confirmations_for(tags, cap),
    }


def build_review(draft_calls: dict[str, Any], ranking: dict[str, Any], profile: dict[str, Any], symbol_risk: dict[str, Any] | None = None) -> dict[str, Any]:
    max_single_position_pct = as_float(profile.get("risk", {}).get("max_single_position_pct"), 0.0)
    rows = ranking_rows(ranking)
    risk_rows = symbol_risk_rows(symbol_risk)
    verdicts = []
    for draft in draft_calls.get("recommendations", []):
        if not isinstance(draft, dict) or not draft.get("symbol"):
            continue
        symbol = str(draft["symbol"])
        verdicts.append(make_verdict(draft, rows.get(symbol), risk_rows.get(symbol), max_single_position_pct))
    return {
        "date": draft_calls.get("date") or ranking.get("as_of_date"),
        "session": draft_calls.get("session") or ranking.get("as_of_session") or ranking.get("session"),
        "generated_at": utc_now(),
        "source": "deterministic_level6_risk_review",
        "policy": {
            "primary_use": "recommendation_only",
            "execution_allowed": False,
            "position_policy": "max_position_pct is a recommendation cap only; this system never executes orders or mutates a portfolio.",
            "max_single_position_pct": max_single_position_pct,
            "buy_candidate_pass_rule": "qualified_for_action=true, cost_gate_passed=true, volume_ratio_20>=1.0, and no downtrend_regime",
            "same_theme_peer_rule": "same_theme_peer_evidence_passed=true",
            "nontechnical_evidence_rule": "buy_candidate also requires fresh non-technical evidence when the ranking policy requires it",
        },
        "verdicts": verdicts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic second-layer risk review for draft HK investment calls.")
    parser.add_argument("--draft-calls", required=True)
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--investment-profile", required=True)
    parser.add_argument("--symbol-risk-json", default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    symbol_risk = load_json(pathlib.Path(args.symbol_risk_json)) if args.symbol_risk_json else None
    review = build_review(
        load_json(pathlib.Path(args.draft_calls)),
        load_json(pathlib.Path(args.ranking)),
        load_profile(pathlib.Path(args.investment_profile)),
        symbol_risk,
    )
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(review, indent=2), encoding="utf-8")
    print(f"Wrote investment risk review: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
