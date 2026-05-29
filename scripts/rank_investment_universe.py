#!/usr/bin/env python3

import argparse
import datetime as dt
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
DEFAULT_MARKET_PROXY_SYMBOL = "2800.HK"
DEFAULT_CN_MARKET_PROXY_SYMBOL = "510300.SH"
DEFAULT_MAX_MARKET_RANGE_FOR_ACTION = 0.70
DEFAULT_BASE_CURRENCY = "HKD"
CN_LIMIT_MOVE_PCT = 9.5
THEME_STARTUP_MIN_MEMBERS = 4
THEME_STARTUP_MIN_NEAR_MA20_COUNT = 3
THEME_STARTUP_MIN_NEAR_MA20_RATIO = 0.40
THEME_STARTUP_MAX_HOT_EXTENDED_RATIO = 0.30
MA20_NEAR_LOWER_PCT = -3.0
MA20_RECLAIM_UPPER_PCT = 5.0
MA20_HOT_DISTANCE_PCT = 8.0
HOT_DAILY_MOVE_PCT = 5.0
MAX_PREMARKET_PREVIOUS_CLOSE_AGE_DAYS = 4
SESSION_ORDER = {"morning": 0, "midday": 1, "close": 2, "historical": 2}
DEFAULT_NONTECHNICAL_POLICY = {
    "require_for_action": False,
    "max_staleness_days": 30,
    "min_total_score_for_action": 0.55,
}
DEFAULT_NONTECHNICAL_WEIGHTS = {
    "fundamental_score": 0.30,
    "valuation_score": 0.20,
    "catalyst_score": 0.25,
    "flow_score": 0.15,
    "macro_score": 0.10,
}
DEFAULT_NONTECHNICAL_COMPONENT_MAX_STALENESS_DAYS = {
    "fundamental_score": 120,
    "valuation_score": 45,
    "catalyst_score": 30,
    "flow_score": 5,
    "macro_score": 14,
    "event_risk": 7,
}
NONTECHNICAL_HARD_EVENT_RISKS = {"elevated", "earnings_gap", "regulatory", "policy", "suspension", "accounting", "quote_stale"}
ACTION_TIER_LABELS = {
    "formal_actionable": "正式可行动",
    "manual_probe": "小仓试错需人工确认",
    "observe": "继续观察",
    "suspended": "暂停行动",
    "blocked": "禁止追入",
}
ACTION_TIER_DESCRIPTIONS = {
    "formal_actionable": "所有正式行动硬门槛均通过；仍然只输出研究结论，不自动交易。",
    "manual_probe": "核心技术、成本、流动性和市场门槛通过，但只剩可人工复核的轻量非技术面缺口；任何小仓试错都必须人工确认。",
    "observe": "有跟踪价值，但未达到正式行动或小仓试错条件。",
    "suspended": "行情、资料、成本、量能或风险门槛暂未通过；不是追高结论，需等阻断项清零。",
    "blocked": "存在涨停追高或高位过热阻断，不应升级为行动。",
}
STARTUP_STAGE_LABELS = {
    "pre_breakout_watch": "启动前观察",
    "ma20_reclaim_candidate": "MA20收复候选",
    "extended_hot_candidate": "热门延伸勿追",
    "theme_ready_wait_confirm": "主题转强待确认",
    "theme_ready_not_near_ma20": "主题转强但未近MA20",
    "theme_not_ready": "主题未转强",
}
ACTION_TIER_CHASE_BLOCK_REASONS = {
    "cn_limit_up_chase_block",
    "market_range_pos_60_above_action_limit",
}
ACTION_TIER_SUSPENDED_REASONS = {
    "cost_gate_failed",
    "volume_ratio_20_below_1_0",
    "market_proxy_missing",
    "quote_trade_date_mismatch",
    "quote_trade_date_missing",
    "hk_halt_or_no_turnover_suspected",
    "cn_limit_down_liquidity_block",
    "symbol_risk_veto",
    "symbol_recent_adverse_breach",
    "downtrend_regime",
    "price_below_ma20_and_ma60",
    "range_pos_60_below_0_12",
    "same_theme_best_peer_evidence_missing_or_failed",
    "nontechnical_evidence_missing",
    "nontechnical_evidence_date_missing",
    "nontechnical_evidence_from_future",
    "nontechnical_evidence_from_future_session",
    "nontechnical_proxy_only",
    "nontechnical_source_missing",
    "nontechnical_component_date_missing",
    "nontechnical_component_from_future",
    "nontechnical_component_missing",
    "nontechnical_score_missing",
    "event_risk_unknown",
    "event_risk_elevated",
    "event_risk_earnings_gap",
    "event_risk_regulatory",
    "event_risk_policy",
    "event_risk_suspension",
    "event_risk_accounting",
    "event_risk_quote_stale",
    "event_risk_from_future",
}
MANUAL_PROBE_COMPATIBLE_NONTECHNICAL_BLOCKERS = {
    "nontechnical_score_below_action_min",
    "nontechnical_evidence_stale",
    "nontechnical_component_stale",
    "event_risk_stale",
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


def load_nontechnical_evidence(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {
            "policy": DEFAULT_NONTECHNICAL_POLICY.copy(),
            "weights": DEFAULT_NONTECHNICAL_WEIGHTS.copy(),
            "symbols": {},
            "path": str(path) if path else None,
        }
    if path.suffix.lower() == ".json":
        data = load_json(path)
    else:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
    policy = DEFAULT_NONTECHNICAL_POLICY.copy()
    policy.update(data.get("policy", {}))
    freshness = data.get("freshness", {}) if isinstance(data.get("freshness"), dict) else {}
    component_days = DEFAULT_NONTECHNICAL_COMPONENT_MAX_STALENESS_DAYS.copy()
    existing_component_days = policy.get("component_max_staleness_days", {}) if isinstance(policy.get("component_max_staleness_days"), dict) else {}
    component_days.update({key: int(value) for key, value in existing_component_days.items() if key in component_days})
    for key in component_days:
        config_key = f"{key}_days"
        if freshness.get(config_key) is not None:
            component_days[key] = int(freshness[config_key])
    policy["component_max_staleness_days"] = component_days
    weights = DEFAULT_NONTECHNICAL_WEIGHTS.copy()
    weights.update({key: float(value) for key, value in data.get("weights", {}).items() if key in weights})
    symbols = {}
    raw_symbols = data.get("symbols", {})
    if isinstance(raw_symbols, dict):
        for symbol, row in raw_symbols.items():
            if isinstance(row, dict):
                symbols[str(symbol)] = {"symbol": str(symbol), **row}
    for row in data.get("evidence", []):
        if isinstance(row, dict) and row.get("symbol"):
            symbols[str(row["symbol"])] = row
    return {"policy": policy, "weights": weights, "symbols": symbols, "path": str(path), "as_of_date": data.get("as_of_date"), "as_of_session": data.get("as_of_session")}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def as_float(value: Any, default: float | None = 0.0) -> float | None:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def date_token(value: Any) -> str | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    if len(text) >= 8 and text[:8].isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    return None


def parse_date_token(value: Any) -> dt.date | None:
    token = date_token(value)
    if token is None:
        return None
    try:
        return dt.date.fromisoformat(token)
    except ValueError:
        return None


def append_unique(target: list[str], values: list[str]) -> None:
    seen = set(target)
    for value in values:
        if value not in seen:
            target.append(value)
            seen.add(value)


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def explicit_true(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() == "true")


def ma20_distance_pct(row: dict[str, Any]) -> float | None:
    price = as_float(row.get("latest_close"), None)
    ma20 = as_float(row.get("ma20"), None)
    if price is None or ma20 is None or price <= 0 or ma20 <= 0:
        return None
    return round(((price / ma20) - 1.0) * 100.0, 2)


def market_family_for_symbol(symbol: str) -> str:
    normalized = symbol.upper()
    if normalized.endswith(".HK"):
        return "hk"
    if normalized.endswith((".SH", ".SZ", ".BJ")):
        return "cn"
    return "unknown"


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


def market_proxy_item(snapshot: dict[str, Any], market_proxy_symbol: str) -> dict[str, Any] | None:
    for item in snapshot.get("items", []):
        if item.get("symbol") == market_proxy_symbol:
            return item
    return None


def proxy_symbol_for_row(row: dict[str, Any], snapshot: dict[str, Any], default_market_proxy_symbol: str) -> str:
    symbol = str(row.get("symbol") or "")
    if market_family_for_symbol(symbol) == "cn":
        return DEFAULT_CN_MARKET_PROXY_SYMBOL
    return default_market_proxy_symbol


def apply_market_context(
    ranked: list[dict[str, Any]],
    snapshot: dict[str, Any],
    market_proxy_symbol: str = DEFAULT_MARKET_PROXY_SYMBOL,
    max_market_range_for_action: float = DEFAULT_MAX_MARKET_RANGE_FOR_ACTION,
) -> None:
    for row in ranked:
        row_proxy_symbol = proxy_symbol_for_row(row, snapshot, market_proxy_symbol)
        proxy = market_proxy_item(snapshot, row_proxy_symbol)
        fields = {
            "market_proxy_symbol": row_proxy_symbol,
            "market_range_pos_60": proxy.get("range_pos_60") if proxy else None,
            "market_pct_change_1d": proxy.get("pct_change_1d") if proxy else None,
            "market_volume_ratio_20": proxy.get("volume_ratio_20") if proxy else None,
            "market_proxy_available": proxy is not None,
            "max_market_range_for_action": max_market_range_for_action,
        }
        row.update(fields)


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
        "currency": item.get("currency"),
        "exchange": item.get("exchange"),
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
        "prev_close": item.get("prev_close"),
        "latest_open": item.get("latest_open"),
        "latest_high": item.get("latest_high"),
        "latest_low": item.get("latest_low"),
        "latest_volume": item.get("latest_volume"),
        "as_of": item.get("as_of"),
        "quote_trade_time": item.get("quote_trade_time"),
        "quote_trade_date": item.get("quote_trade_date"),
        "quote_last": item.get("quote_last"),
        "quote_volume": item.get("quote_volume"),
        "ah_pair": item.get("ah_pair"),
        "ah_premium_pct": item.get("ah_premium_pct"),
        "fx_reference": item.get("fx_reference"),
        "hkd_cny_reference": item.get("hkd_cny_reference"),
    }


def annotate_theme_positions(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        groups[str(row.get("theme") or "unknown")].append(row)

    for theme_items in groups.values():
        ordered = sorted(theme_items, key=lambda row: row["score"], reverse=True)
        leader = str(ordered[0].get("symbol")) if ordered else None
        leader_score = float(ordered[0].get("score") or 0.0) if ordered else 0.0
        peer_scores = [
            {"symbol": row.get("symbol"), "score": row.get("score"), "rank": index}
            for index, row in enumerate(ordered[:3], start=1)
        ]
        for index, row in enumerate(ordered, start=1):
            score = float(row.get("score") or 0.0)
            is_leader = index == 1
            next_best = ordered[1] if is_leader and len(ordered) > 1 else None
            row["theme_rank"] = index
            row["theme_peer_count"] = len(ordered)
            row["theme_leader"] = leader
            row["theme_leader_score"] = round(leader_score, 2)
            row["theme_score_gap_to_leader"] = round(leader_score - score, 2)
            row["theme_top_peer_scores"] = peer_scores
            row["same_theme_best_symbol"] = leader
            row["same_theme_best_score"] = round(leader_score, 2)
            row["same_theme_selected_vs_best_score_gap"] = round(score - leader_score, 2)
            row["same_theme_next_best_symbol"] = next_best.get("symbol") if next_best else None
            row["same_theme_selected_vs_next_best_score_gap"] = round(score - float(next_best.get("score") or 0.0), 2) if next_best else None
            row["is_theme_leader"] = is_leader
            row["same_theme_peer_evidence_passed"] = bool(is_leader and leader == row.get("symbol"))
            row["peer_relative_decision"] = "theme_leader" if is_leader else "blocked_by_same_theme_leader"
            if len(ordered) == 1:
                row["peer_relative_decision"] = "sole_theme_candidate"
            if not is_leader:
                row.setdefault("qualification_flags", []).append("same_theme_non_leader")
                row.setdefault("disqualifiers", []).append("not_theme_score_leader")
                row["qualified_for_watch"] = False
                row["diagnostic_only"] = True
    return scored


def apply_theme_startup_context(scored: list[dict[str, Any]]) -> None:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        groups[str(row.get("theme") or "unknown")].append(row)

    for theme_items in groups.values():
        for row in theme_items:
            distance = ma20_distance_pct(row)
            pct_change = as_float(row.get("pct_change_1d"), 0.0) or 0.0
            range_pos = as_float(row.get("range_pos_60"), 0.0) or 0.0
            near_or_above_ma20 = distance is not None and MA20_NEAR_LOWER_PCT <= distance <= MA20_RECLAIM_UPPER_PCT
            hot_extended = bool(distance is not None and distance > MA20_HOT_DISTANCE_PCT) or pct_change >= HOT_DAILY_MOVE_PCT or range_pos > 0.85
            if market_family_for_symbol(str(row.get("symbol") or "")) == "cn" and str(row.get("kind") or "").lower() == "stock" and pct_change >= CN_LIMIT_MOVE_PCT:
                hot_extended = True
            row["ma20_distance_pct"] = distance
            row["near_ma20"] = distance is not None and MA20_NEAR_LOWER_PCT <= distance <= 3.0
            row["near_or_above_ma20"] = near_or_above_ma20
            row["pre_breakout_zone"] = distance is not None and MA20_NEAR_LOWER_PCT <= distance < 0.0
            row["ma20_reclaim_zone"] = distance is not None and 0.0 <= distance <= MA20_RECLAIM_UPPER_PCT
            row["hot_extended"] = hot_extended

        ordered = sorted(theme_items, key=lambda row: row["score"], reverse=True)
        leader = ordered[0] if ordered else {}
        member_count = len(theme_items)
        near_count = sum(1 for row in theme_items if row.get("near_or_above_ma20"))
        hot_count = sum(1 for row in theme_items if row.get("hot_extended"))
        near_ratio = round(near_count / member_count, 3) if member_count else 0.0
        hot_ratio = round(hot_count / member_count, 3) if member_count else 0.0
        leader_distance = leader.get("ma20_distance_pct")
        leader_above_ma20 = leader_distance is not None and float(leader_distance) >= 0.0
        theme_ready = bool(
            member_count >= THEME_STARTUP_MIN_MEMBERS
            and near_count >= THEME_STARTUP_MIN_NEAR_MA20_COUNT
            and near_ratio >= THEME_STARTUP_MIN_NEAR_MA20_RATIO
            and leader_above_ma20
            and hot_ratio <= THEME_STARTUP_MAX_HOT_EXTENDED_RATIO
        )
        context = {
            "qualified": theme_ready,
            "member_count": member_count,
            "near_or_above_ma20_count": near_count,
            "near_or_above_ma20_ratio": near_ratio,
            "leader_symbol": leader.get("symbol"),
            "leader_above_ma20": leader_above_ma20,
            "hot_extended_count": hot_count,
            "hot_extended_ratio": hot_ratio,
            "rule": "members>=4, near_or_above_ma20>=3 and >=40%, leader_above_ma20, hot_extended<=30%",
        }
        not_ready_reasons = []
        if member_count < THEME_STARTUP_MIN_MEMBERS:
            not_ready_reasons.append("theme_member_count_below_4")
        if near_count < THEME_STARTUP_MIN_NEAR_MA20_COUNT:
            not_ready_reasons.append("near_or_above_ma20_count_below_3")
        if near_ratio < THEME_STARTUP_MIN_NEAR_MA20_RATIO:
            not_ready_reasons.append("near_or_above_ma20_ratio_below_0_40")
        if not leader_above_ma20:
            not_ready_reasons.append("leader_below_ma20")
        if hot_ratio > THEME_STARTUP_MAX_HOT_EXTENDED_RATIO:
            not_ready_reasons.append("hot_extended_ratio_above_0_30")

        for row in theme_items:
            volume_ratio = as_float(row.get("volume_ratio_20"), None)
            range_pos = as_float(row.get("range_pos_60"), None)
            volume_ok = volume_ratio is not None and volume_ratio >= 0.8
            range_ok = range_pos is None or range_pos <= 0.75
            reasons = ["theme_startup_breadth_confirmed"] if theme_ready else list(not_ready_reasons)
            if not theme_ready:
                stage = "theme_not_ready"
            elif row.get("hot_extended"):
                stage = "extended_hot_candidate"
                reasons.append("price_or_range_hot_extended")
            elif row.get("pre_breakout_zone") and volume_ok and range_ok:
                stage = "pre_breakout_watch"
                reasons.extend(["price_near_ma20_before_breakout", "volume_at_least_0_8", "range_not_overextended"])
            elif row.get("ma20_reclaim_zone") and volume_ok and range_ok:
                stage = "ma20_reclaim_candidate"
                reasons.extend(["price_reclaimed_ma20", "volume_at_least_0_8", "range_not_overextended"])
            elif row.get("near_or_above_ma20"):
                stage = "theme_ready_wait_confirm"
                if not volume_ok:
                    reasons.append("volume_below_0_8")
                if not range_ok:
                    reasons.append("range_position_above_startup_limit")
            else:
                stage = "theme_ready_not_near_ma20"
                reasons.append("price_not_near_ma20")

            row["theme_startup"] = context
            row["startup_candidate_stage"] = stage
            row["startup_candidate_label"] = STARTUP_STAGE_LABELS[stage]
            row["startup_candidate_reasons"] = unique(reasons)
            row["startup_watch_candidate"] = stage in {"pre_breakout_watch", "ma20_reclaim_candidate"}
            if row["startup_watch_candidate"]:
                append_unique(row.setdefault("qualification_flags", []), [stage, "startup_watch_candidate"])


def theme_startup_summary(scored: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = {}
    for row in scored:
        theme = str(row.get("theme") or "unknown")
        context = row.get("theme_startup") if isinstance(row.get("theme_startup"), dict) else None
        if context and theme not in summaries:
            summaries[theme] = {"theme": theme, **context}
    return sorted(summaries.values(), key=lambda row: (not row.get("qualified"), -float(row.get("near_or_above_ma20_ratio") or 0.0), str(row.get("theme") or "")))


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


def allows_premarket_previous_close(row: dict[str, Any], snapshot_date: str, quote_date: str) -> bool:
    session = str(row.get("snapshot_as_of_session") or row.get("as_of_session") or "").lower()
    if session != "morning":
        return False
    snapshot_day = parse_date_token(snapshot_date)
    quote_day = parse_date_token(quote_date)
    if snapshot_day is None or quote_day is None or quote_day >= snapshot_day:
        return False
    return (snapshot_day - quote_day).days <= MAX_PREMARKET_PREVIOUS_CLOSE_AGE_DAYS


def market_specific_risk_signals(row: dict[str, Any], base_currency: str = DEFAULT_BASE_CURRENCY) -> tuple[list[str], list[str]]:
    symbol = str(row.get("symbol") or "")
    family = market_family_for_symbol(symbol)
    kind = str(row.get("kind") or "").lower()
    flags: list[str] = []
    action_disqualifiers: list[str] = []

    snapshot_date = date_token(row.get("snapshot_as_of_date") or row.get("as_of_date"))
    quote_date = date_token(row.get("quote_trade_date") or row.get("as_of"))
    price_source = str(row.get("price_source") or "")
    if snapshot_date and quote_date and quote_date != snapshot_date:
        if allows_premarket_previous_close(row, snapshot_date, quote_date):
            flags.append("premarket_previous_close_reference")
        else:
            flags.append("quote_trade_date_mismatch")
            action_disqualifiers.append("quote_trade_date_mismatch")
    elif price_source == "quote" and snapshot_date and not quote_date:
        flags.append("quote_trade_date_missing")
        action_disqualifiers.append("quote_trade_date_missing")

    pct_change = as_float(row.get("pct_change_1d"), 0.0) or 0.0
    if family == "hk" and kind == "stock" and price_source == "quote":
        quote_volume = as_float(row.get("quote_volume"), None)
        latest_volume = as_float(row.get("latest_volume"), None)
        prev_close = as_float(row.get("prev_close"), None)
        latest_close = as_float(row.get("latest_close"), None)
        no_turnover = (quote_volume is not None and quote_volume <= 0) or (latest_volume is not None and latest_volume <= 0)
        unchanged = prev_close is not None and latest_close is not None and prev_close > 0 and abs((latest_close / prev_close) - 1.0) < 0.0001
        if no_turnover and (unchanged or abs(pct_change) < 0.01):
            flags.append("hk_halt_or_no_turnover_suspected")
            action_disqualifiers.append("hk_halt_or_no_turnover_suspected")

    if family == "cn" and kind == "stock":
        if pct_change >= CN_LIMIT_MOVE_PCT:
            flags.append("cn_limit_up_chase_block")
            action_disqualifiers.append("cn_limit_up_chase_block")
        elif pct_change <= -CN_LIMIT_MOVE_PCT:
            flags.append("cn_limit_down_liquidity_block")
            action_disqualifiers.append("cn_limit_down_liquidity_block")

    currency = str(row.get("currency") or "").upper()
    if family == "cn" and currency == "CNY" and base_currency.upper() == "HKD":
        flags.append("hkd_cny_cross_currency_exposure")
        if row.get("fx_reference") is None and row.get("hkd_cny_reference") is None:
            flags.append("hkd_cny_fx_reference_missing")

    if row.get("ah_pair") and row.get("ah_premium_pct") is None:
        flags.append("ah_premium_discount_unavailable")

    return flags, action_disqualifiers


def component_max_staleness_days(policy: dict[str, Any]) -> dict[str, int]:
    days = DEFAULT_NONTECHNICAL_COMPONENT_MAX_STALENESS_DAYS.copy()
    raw = policy.get("component_max_staleness_days", {}) if isinstance(policy.get("component_max_staleness_days"), dict) else {}
    for key, value in raw.items():
        if key in days:
            days[key] = int(value)
    return days


def raw_component_as_of_dates(raw: dict[str, Any]) -> dict[str, str | None]:
    configured = raw.get("component_as_of_dates", {}) if isinstance(raw.get("component_as_of_dates"), dict) else {}
    has_component_dates = bool(configured) or any(raw.get(f"{key}_as_of_date") is not None for key in DEFAULT_NONTECHNICAL_WEIGHTS)
    if not has_component_dates:
        return {key: None for key in DEFAULT_NONTECHNICAL_WEIGHTS}
    return {key: date_token(configured.get(key) or raw.get(f"{key}_as_of_date") or raw.get("as_of_date")) for key in DEFAULT_NONTECHNICAL_WEIGHTS}


def append_staleness_signal(flags: list[str], action_disqualifiers: list[str], reason: str, require_for_action: bool) -> None:
    flags.append(reason)
    if require_for_action:
        action_disqualifiers.append(reason)


def nontechnical_evidence_signals(
    row: dict[str, Any],
    evidence: dict[str, Any] | None,
    snapshot_date: str | None = None,
    snapshot_session: str | None = None,
) -> tuple[dict[str, Any], list[str], list[str]]:
    evidence = evidence or {"policy": DEFAULT_NONTECHNICAL_POLICY.copy(), "weights": DEFAULT_NONTECHNICAL_WEIGHTS.copy(), "symbols": {}}
    policy = evidence.get("policy", DEFAULT_NONTECHNICAL_POLICY) if isinstance(evidence.get("policy"), dict) else DEFAULT_NONTECHNICAL_POLICY
    weights = evidence.get("weights", DEFAULT_NONTECHNICAL_WEIGHTS) if isinstance(evidence.get("weights"), dict) else DEFAULT_NONTECHNICAL_WEIGHTS
    symbols = evidence.get("symbols", {}) if isinstance(evidence.get("symbols"), dict) else {}
    require_for_action = bool(policy.get("require_for_action", False))
    symbol = str(row.get("symbol") or "")
    raw = symbols.get(symbol)
    flags: list[str] = []
    action_disqualifiers: list[str] = []
    if not raw or raw.get("evidence_mode") == "missing_fail_closed":
        flags.append("nontechnical_evidence_missing")
        if require_for_action:
            action_disqualifiers.append("nontechnical_evidence_missing")
        return {
            "status": "missing",
            "required_for_action": require_for_action,
            "total_score": None,
            "as_of_date": None,
            "source_count": 0,
            "notes": [],
        }, flags, action_disqualifiers

    evidence_mode = str(raw.get("evidence_mode") or "").strip()
    proxy_only = evidence_mode == "automatic_local_proxy" or explicit_true(raw.get("proxy_only"))
    if proxy_only:
        flags.append("nontechnical_proxy_only")
        action_disqualifiers.append("nontechnical_proxy_only")

    as_of_date = parse_date_token(raw.get("as_of_date") or evidence.get("as_of_date"))
    evidence_session = str(raw.get("as_of_session") or evidence.get("as_of_session") or "").lower() or None
    report_date = parse_date_token(snapshot_date or row.get("snapshot_as_of_date") or row.get("as_of_date"))
    report_session = str(snapshot_session or row.get("snapshot_as_of_session") or row.get("as_of_session") or "").lower() or None
    component_dates = raw_component_as_of_dates(raw)
    component_ages: dict[str, int] = {}
    stale_components: list[str] = []
    future_components: list[str] = []
    missing_component_dates: list[str] = []
    max_component_days = component_max_staleness_days(policy)
    if as_of_date is None:
        flags.append("nontechnical_evidence_date_missing")
        if require_for_action:
            action_disqualifiers.append("nontechnical_evidence_date_missing")
    elif report_date is not None:
        age_days = (report_date - as_of_date).days
        if age_days < 0:
            flags.append("nontechnical_evidence_from_future")
            action_disqualifiers.append("nontechnical_evidence_from_future")
        elif not any(component_dates.values()) and age_days > int(policy.get("max_staleness_days", 30)):
            flags.append("nontechnical_evidence_stale")
            if require_for_action:
                action_disqualifiers.append("nontechnical_evidence_stale")
        elif age_days == 0 and evidence_session and report_session and SESSION_ORDER.get(evidence_session, 99) > SESSION_ORDER.get(report_session, 99):
            flags.append("nontechnical_evidence_from_future_session")
            action_disqualifiers.append("nontechnical_evidence_from_future_session")
    if report_date is not None and any(component_dates.values()):
        for key, raw_date in component_dates.items():
            component_date = parse_date_token(raw_date)
            if component_date is None:
                missing_component_dates.append(key)
                continue
            age_days = (report_date - component_date).days
            component_ages[key] = age_days
            if age_days < 0:
                future_components.append(key)
            elif age_days > int(max_component_days.get(key, policy.get("max_staleness_days", 30))):
                stale_components.append(key)
        if missing_component_dates:
            append_staleness_signal(flags, action_disqualifiers, "nontechnical_component_date_missing", require_for_action)
        if future_components:
            flags.append("nontechnical_component_from_future")
            action_disqualifiers.append("nontechnical_component_from_future")
        if stale_components:
            append_staleness_signal(flags, action_disqualifiers, "nontechnical_component_stale", require_for_action)

    event_risk_as_of_date = parse_date_token(raw.get("event_risk_as_of_date") or raw.get("event_as_of_date") or raw.get("as_of_date") or evidence.get("as_of_date"))
    event_risk_age_days = None
    if report_date is not None and event_risk_as_of_date is not None:
        event_risk_age_days = (report_date - event_risk_as_of_date).days
        if event_risk_age_days < 0:
            flags.append("event_risk_from_future")
            action_disqualifiers.append("event_risk_from_future")
        elif event_risk_age_days > int(max_component_days.get("event_risk", policy.get("max_staleness_days", 30))):
            append_staleness_signal(flags, action_disqualifiers, "event_risk_stale", require_for_action)

    score_sum = 0.0
    weight_sum = 0.0
    components: dict[str, float | None] = {}
    for key, weight in weights.items():
        value = as_float(raw.get(key), None)
        components[key] = value
        if value is None:
            continue
        score_sum += clamp(value, 0.0, 1.0) * float(weight)
        weight_sum += float(weight)
    missing_components = [key for key in weights if components.get(key) is None]
    if missing_components:
        flags.append("nontechnical_component_missing")
        if require_for_action:
            action_disqualifiers.append("nontechnical_component_missing")
    total_score = round(score_sum / weight_sum, 3) if weight_sum else None
    min_score = float(policy.get("min_total_score_for_action", 0.55))
    if total_score is None:
        flags.append("nontechnical_score_missing")
        if require_for_action:
            action_disqualifiers.append("nontechnical_score_missing")
    elif total_score < min_score:
        flags.append("nontechnical_score_below_action_min")
        if require_for_action:
            action_disqualifiers.append("nontechnical_score_below_action_min")

    event_risk = str(raw.get("event_risk") or "unknown").lower()
    if event_risk == "unknown":
        flags.append("event_risk_unknown")
        if require_for_action and bool(policy.get("block_unknown_event_risk", True)):
            action_disqualifiers.append("event_risk_unknown")
    elif event_risk in NONTECHNICAL_HARD_EVENT_RISKS:
        flags.append(f"event_risk_{event_risk}")
        action_disqualifiers.append(f"event_risk_{event_risk}")

    proxy_source_count = len(raw.get("sources", [])) if isinstance(raw.get("sources"), list) else 0
    if proxy_only:
        source_count = 0
    elif raw.get("source_count") is not None:
        source_count = int(raw.get("source_count") or 0)
    elif isinstance(raw.get("sources"), list):
        source_count = len(raw.get("sources", []))
    else:
        source_count = 0
    if source_count <= 0:
        flags.append("nontechnical_source_missing")
        if require_for_action:
            action_disqualifiers.append("nontechnical_source_missing")

    return {
        "status": "proxy_only" if proxy_only else "available",
        "required_for_action": require_for_action,
        "evidence_mode": evidence_mode or None,
        "proxy_only": proxy_only,
        "total_score": total_score,
        "min_total_score_for_action": min_score,
        "as_of_date": as_of_date.isoformat() if as_of_date else raw.get("as_of_date"),
        "as_of_session": evidence_session,
        "component_as_of_dates": component_dates,
        "component_age_days": component_ages,
        "stale_components": stale_components,
        "future_components": future_components,
        "missing_component_dates": missing_component_dates,
        "event_risk_as_of_date": event_risk_as_of_date.isoformat() if event_risk_as_of_date else raw.get("event_risk_as_of_date"),
        "event_risk_age_days": event_risk_age_days,
        "source_count": source_count,
        "proxy_source_count": proxy_source_count if proxy_only else None,
        "components": components,
        "event_risk": event_risk,
        "notes": raw.get("notes", []),
    }, flags, action_disqualifiers


def action_tier_for(row: dict[str, Any], core_action_ok: bool, nontechnical_disqualifiers: list[str]) -> dict[str, Any]:
    blockers = unique([str(item) for item in row.get("action_disqualifiers", [])] + [str(item) for item in row.get("disqualifiers", [])])
    blocker_set = set(blockers)
    if row.get("qualified_for_action") is True:
        tier = "formal_actionable"
        reasons: list[str] = []
    else:
        nontechnical_blockers = {str(item) for item in nontechnical_disqualifiers}
        chase_blockers = sorted(blocker_set & ACTION_TIER_CHASE_BLOCK_REASONS)
        suspended_blockers = sorted((blocker_set & ACTION_TIER_SUSPENDED_REASONS) - MANUAL_PROBE_COMPATIBLE_NONTECHNICAL_BLOCKERS)
        manual_probe_ok = (
            bool(row.get("qualified_for_watch"))
            and core_action_ok
            and bool(nontechnical_blockers)
            and nontechnical_blockers <= MANUAL_PROBE_COMPATIBLE_NONTECHNICAL_BLOCKERS
            and not chase_blockers
            and not suspended_blockers
        )
        if manual_probe_ok:
            tier = "manual_probe"
            reasons = sorted(nontechnical_blockers)
        elif chase_blockers:
            tier = "blocked"
            reasons = chase_blockers
        elif suspended_blockers:
            tier = "suspended"
            reasons = suspended_blockers
        elif row.get("qualified_for_watch") is True or float(row.get("score") or 0.0) >= 45.0:
            tier = "observe"
            reasons = blockers[:4]
        else:
            tier = "suspended"
            reasons = blockers[:4]
    return {
        "key": tier,
        "label": ACTION_TIER_LABELS[tier],
        "description": ACTION_TIER_DESCRIPTIONS[tier],
        "reasons": reasons,
        "formal_actionable": tier == "formal_actionable",
        "manual_confirmation_required": tier != "formal_actionable",
        "research_only": True,
    }


def apply_action_qualification(
    ranked: list[dict[str, Any]],
    min_action_score: float,
    symbol_risk: dict[str, dict[str, Any]],
    base_currency: str = DEFAULT_BASE_CURRENCY,
    nontechnical_evidence: dict[str, Any] | None = None,
) -> None:
    for row in ranked:
        symbol = str(row.get("symbol") or "")
        risk = symbol_risk.get(symbol, {})
        reasons = [str(reason) for reason in risk.get("reasons", risk.get("reason", []))] if isinstance(risk.get("reasons", risk.get("reason", [])), list) else []
        row["symbol_risk"] = {
            "action_veto": bool(risk.get("action_veto", False)),
            "reasons": reasons,
            "tags": risk.get("tags", []),
        }
        risk_tags = {str(tag) for tag in row["symbol_risk"].get("tags", [])}
        if row["symbol_risk"]["action_veto"]:
            row.setdefault("disqualifiers", []).append("symbol_risk_veto")
            row["diagnostic_only"] = True
        if not bool(row.get("cost_gate_passed")):
            row.setdefault("disqualifiers", []).append("cost_gate_failed")
            row["diagnostic_only"] = True
        market_risk_flags, market_action_disqualifiers = market_specific_risk_signals(row, base_currency)
        append_unique(row.setdefault("market_specific_risk_flags", []), market_risk_flags)
        append_unique(row.setdefault("action_disqualifiers", []), market_action_disqualifiers)
        market_specific_action_ok = not market_action_disqualifiers
        if market_specific_action_ok:
            row.setdefault("qualification_flags", []).append("market_specific_risk_gate_clear")
        else:
            row.setdefault("qualification_flags", []).append("market_specific_risk_gate_blocked")
            row["diagnostic_only"] = True
        nontechnical_profile, nontechnical_flags, nontechnical_disqualifiers = nontechnical_evidence_signals(row, nontechnical_evidence, row.get("snapshot_as_of_date"), row.get("snapshot_as_of_session"))
        row["nontechnical_evidence"] = nontechnical_profile
        append_unique(row.setdefault("nontechnical_evidence_flags", []), nontechnical_flags)
        append_unique(row.setdefault("action_disqualifiers", []), nontechnical_disqualifiers)
        nontechnical_ok = not nontechnical_disqualifiers
        if nontechnical_ok:
            row.setdefault("qualification_flags", []).append("nontechnical_evidence_gate_clear")
        else:
            row.setdefault("qualification_flags", []).append("nontechnical_evidence_gate_blocked")
            row["diagnostic_only"] = True
        score_ok = float(row.get("score") or 0.0) >= min_action_score
        if score_ok:
            row.setdefault("qualification_flags", []).append("score_meets_action_threshold")
        else:
            row.setdefault("qualification_flags", []).append("below_action_score")
        volume_ratio = row.get("volume_ratio_20")
        volume_action_ok = volume_ratio is not None and float(volume_ratio) >= 1.0
        if volume_action_ok:
            row.setdefault("qualification_flags", []).append("volume_meets_action_threshold")
        else:
            row.setdefault("qualification_flags", []).append("below_action_volume_ratio")
            row.setdefault("action_disqualifiers", []).append("volume_ratio_20_below_1_0")
        market_range = row.get("market_range_pos_60")
        market_limit = float(row.get("max_market_range_for_action") or DEFAULT_MAX_MARKET_RANGE_FOR_ACTION)
        market_proxy_available = row.get("market_proxy_available", True) is not False
        market_range_ok = market_proxy_available and (market_range is None or float(market_range) <= market_limit)
        if market_range_ok:
            row.setdefault("qualification_flags", []).append("market_range_not_overextended")
        elif not market_proxy_available:
            row.setdefault("qualification_flags", []).append("market_proxy_missing")
            row.setdefault("action_disqualifiers", []).append("market_proxy_missing")
        else:
            row.setdefault("qualification_flags", []).append("market_range_overextended")
            row.setdefault("action_disqualifiers", []).append("market_range_pos_60_above_action_limit")
        symbol_action_risk_ok = "recent_symbol_adverse_breach" not in risk_tags
        if symbol_action_risk_ok:
            row.setdefault("qualification_flags", []).append("symbol_recent_adverse_breach_clear")
        else:
            row.setdefault("qualification_flags", []).append("symbol_recent_adverse_breach_present")
            row.setdefault("action_disqualifiers", []).append("symbol_recent_adverse_breach")
        peer_evidence_ok = row.get("same_theme_peer_evidence_passed") is True
        if peer_evidence_ok:
            row.setdefault("qualification_flags", []).append("same_theme_best_peer_evidence_passed")
        else:
            row.setdefault("qualification_flags", []).append("same_theme_best_peer_evidence_failed")
            row.setdefault("action_disqualifiers", []).append("same_theme_best_peer_evidence_missing_or_failed")
        row["qualified_for_action"] = bool(
            row.get("qualified_for_watch")
            and score_ok
            and volume_action_ok
            and market_range_ok
            and market_specific_action_ok
            and nontechnical_ok
            and symbol_action_risk_ok
            and peer_evidence_ok
            and row.get("cost_gate_passed")
            and not row["symbol_risk"]["action_veto"]
        )
        core_action_ok = bool(
            row.get("qualified_for_watch")
            and score_ok
            and volume_action_ok
            and market_range_ok
            and market_specific_action_ok
            and symbol_action_risk_ok
            and peer_evidence_ok
            and row.get("cost_gate_passed")
            and not row["symbol_risk"]["action_veto"]
        )
        action_tier = action_tier_for(row, core_action_ok, nontechnical_disqualifiers)
        row["action_tier"] = action_tier["key"]
        row["action_tier_label"] = action_tier["label"]
        row["action_tier_description"] = action_tier["description"]
        row["action_tier_reasons"] = action_tier["reasons"]
        row["formal_actionable"] = action_tier["formal_actionable"]
        row["manual_confirmation_required"] = action_tier["manual_confirmation_required"]
        if not row["qualified_for_action"]:
            row["diagnostic_only"] = True


def candidate_layers(ranked: list[dict[str, Any]], actionable_top_n: int, diagnostic_top_n: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    actionable = []
    for row in ranked:
        if len(actionable) >= actionable_top_n:
            break
        if not row.get("qualified_for_action"):
            continue
        candidate = dict(row)
        candidate["source_layer"] = "actionable_candidates"
        candidate["eligible_for_action_from_layer"] = True
        candidate["layer_action_cap"] = "buy_candidate"
        actionable.append(candidate)
    diagnostics = []
    for row in ranked[:diagnostic_top_n]:
        diagnostic = dict(row)
        diagnostic["source_layer"] = "diagnostic_candidates"
        diagnostic["eligible_for_action_from_layer"] = False
        diagnostic["layer_action_cap"] = "watch_only"
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


def startup_candidate_layer(ranked: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    candidates = []
    for row in ranked:
        if len(candidates) >= limit:
            break
        if row.get("startup_watch_candidate") is not True:
            continue
        candidate = dict(row)
        candidate["source_layer"] = "startup_candidates"
        candidate["eligible_for_action_from_layer"] = False
        candidate["layer_action_cap"] = "watch_only"
        candidate["diagnostic_only"] = True
        candidates.append(candidate)
    return candidates


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
    parser.add_argument("--market-proxy-symbol", default=DEFAULT_MARKET_PROXY_SYMBOL)
    parser.add_argument("--max-market-range-for-action", type=float, default=DEFAULT_MAX_MARKET_RANGE_FOR_ACTION)
    parser.add_argument("--base-currency", default=DEFAULT_BASE_CURRENCY)
    parser.add_argument("--strategy-config", default=None, help="Optional active strategy TOML with ranking weights and safety invariants.")
    parser.add_argument("--symbol-risk-json", default=None, help="Optional symbol risk memory JSON with action_veto tags.")
    parser.add_argument("--nontechnical-evidence", default=None, help="Optional TOML evidence file with fundamentals, valuation, catalyst, flow, macro, and event-risk checks.")
    parser.add_argument("--as-of-session", default=None, choices=sorted(SESSION_ORDER), help="Decision session for point-in-time evidence checks.")
    args = parser.parse_args()

    snapshot_path = pathlib.Path(args.snapshot)
    snapshot = load_json(snapshot_path)
    strategy = load_strategy_config(pathlib.Path(args.strategy_config) if args.strategy_config else None)
    symbol_risk = load_symbol_risk(pathlib.Path(args.symbol_risk_json) if args.symbol_risk_json else None)
    default_nontechnical_path = pathlib.Path("config") / "nontechnical_evidence.toml"
    nontechnical_path = pathlib.Path(args.nontechnical_evidence) if args.nontechnical_evidence else (default_nontechnical_path if default_nontechnical_path.exists() else None)
    nontechnical_evidence = load_nontechnical_evidence(nontechnical_path)
    diagnostic_top_n = args.diagnostic_top_n if args.diagnostic_top_n is not None else (args.top_n if args.top_n is not None else 3)
    scored = annotate_theme_positions([item_score(item, strategy["weights"], args.min_watch_score) for item in snapshot.get("items", [])])
    apply_theme_startup_context(scored)
    for row in scored:
        row["snapshot_as_of_date"] = snapshot.get("as_of_date")
        row["snapshot_as_of_session"] = args.as_of_session
    apply_market_context(scored, snapshot, args.market_proxy_symbol, args.max_market_range_for_action)
    apply_edge_cost_fields(scored, args.round_trip_bps, args.minimum_edge_bps)
    ranked = sorted(scored, key=lambda row: row["score"], reverse=True)
    apply_action_qualification(ranked, args.min_action_score, symbol_risk, args.base_currency, nontechnical_evidence)
    actionable_candidates, diagnostic_candidates, top_candidates = candidate_layers(ranked, args.actionable_top_n, diagnostic_top_n)
    startup_candidates = startup_candidate_layer(ranked, args.max_candidates)

    output = {
        "snapshot": str(snapshot_path),
        "as_of_date": snapshot.get("as_of_date"),
        "as_of_session": args.as_of_session,
        "generated_at": snapshot.get("generated_at"),
        "strategy_id": strategy["strategy_id"],
        "strategy_version": strategy["strategy_version"],
        "strategy_status": strategy["status"],
        "strategy_weights": strategy["weights"],
        "safety_invariants": strategy["safety_invariants"],
        "theme_startup_policy": {
            "min_member_count": THEME_STARTUP_MIN_MEMBERS,
            "min_near_or_above_ma20_count": THEME_STARTUP_MIN_NEAR_MA20_COUNT,
            "min_near_or_above_ma20_ratio": THEME_STARTUP_MIN_NEAR_MA20_RATIO,
            "max_hot_extended_ratio": THEME_STARTUP_MAX_HOT_EXTENDED_RATIO,
            "near_ma20_lower_pct": MA20_NEAR_LOWER_PCT,
            "reclaim_upper_pct": MA20_RECLAIM_UPPER_PCT,
            "hot_distance_pct": MA20_HOT_DISTANCE_PCT,
            "hot_daily_move_pct": HOT_DAILY_MOVE_PCT,
        },
        "cost_gate": {
            "estimated_round_trip_bps": args.round_trip_bps,
            "minimum_edge_bps": args.minimum_edge_bps,
            "action_rule": "Do not upgrade unless expected swing edge exceeds both cost and minimum edge gates.",
            "same_theme_peer_rule": "Do not upgrade unless same-theme best-peer evidence passes.",
            "market_regime_rule": "Do not upgrade when the market proxy is above the action range limit.",
            "market_specific_risk_rule": "Do not upgrade when deterministic HK/A-share quote, halt, or limit-board gates are blocked.",
            "nontechnical_evidence_rule": "Do not upgrade when required fundamentals, valuation, catalyst, flow, macro, and event-risk evidence is missing, stale, or below threshold.",
            "symbol_adverse_rule": "Do not upgrade symbols with a recent adverse-breach risk tag; keep them watch-only until evidence improves.",
        },
        "action_tier_policy": {
            "formal_actionable": "All hard gates pass; research-only and no automatic execution.",
            "manual_probe": "Core technical, edge/cost, liquidity, market, symbol-risk, and peer gates pass; only compatible soft nontechnical evidence blockers remain, and human confirmation is required.",
            "observe": "Track without action when the symbol has watch value but lacks formal or manual-probe readiness.",
            "suspended": "Do not initiate while quote freshness, formal evidence, cost/edge, volume, symbol-risk, peer, or event-risk gates are unresolved; this is not a chase-specific verdict.",
            "blocked": "Do not chase when limit-up or overextended market-position blockers are present.",
        },
        "thresholds": {
            "min_watch_score": args.min_watch_score,
            "min_action_score": args.min_action_score,
            "actionable_top_n": args.actionable_top_n,
            "diagnostic_top_n": diagnostic_top_n,
            "market_proxy_symbol": args.market_proxy_symbol,
            "cn_market_proxy_symbol": DEFAULT_CN_MARKET_PROXY_SYMBOL,
            "max_market_range_for_action": args.max_market_range_for_action,
            "base_currency": args.base_currency,
            "nontechnical_evidence": nontechnical_evidence.get("path"),
            "nontechnical_evidence_required_for_action": bool(nontechnical_evidence.get("policy", {}).get("require_for_action", False)),
        },
        "theme_summary": theme_summary(scored),
        "theme_startup_summary": theme_startup_summary(scored),
        "actionable_candidates": actionable_candidates,
        "startup_candidates": startup_candidates,
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
