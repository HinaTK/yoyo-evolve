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

from rank_investment_universe import DEFAULT_CN_MARKET_PROXY_SYMBOL, DEFAULT_MARKET_PROXY_SYMBOL, DEFAULT_MAX_MARKET_RANGE_FOR_ACTION, DEFAULT_STRATEGY_WEIGHTS, annotate_theme_positions, apply_action_qualification, apply_edge_cost_fields, apply_market_context, candidate_layers, item_score, load_strategy_config, load_symbol_risk, market_family_for_symbol  # noqa: E402


EXPERIMENTAL_RISK_FILTERS = {
    "off",
    "pct_heat_5",
    "volume_range_heat",
    "market_pct_heat",
    "combined_heat",
    "mid_range",
    "low_score_70",
    "combined_heat_mid_range",
    "combined_heat_low_score",
    "combined_heat_mid_range_low_score",
    "market_stall",
    "combined_heat_mid_range_market_stall",
}
PCT_HEAT_FILTERS = {"pct_heat_5", "combined_heat", "combined_heat_mid_range", "combined_heat_low_score", "combined_heat_mid_range_low_score", "combined_heat_mid_range_market_stall"}
VOLUME_RANGE_HEAT_FILTERS = {"volume_range_heat", "combined_heat", "combined_heat_mid_range", "combined_heat_low_score", "combined_heat_mid_range_low_score", "combined_heat_mid_range_market_stall"}
MARKET_PCT_HEAT_FILTERS = {"market_pct_heat", "combined_heat", "combined_heat_mid_range", "combined_heat_low_score", "combined_heat_mid_range_low_score", "combined_heat_mid_range_market_stall"}
MID_RANGE_FILTERS = {"mid_range", "combined_heat_mid_range", "combined_heat_mid_range_low_score", "combined_heat_mid_range_market_stall"}
LOW_SCORE_FILTERS = {"low_score_70", "combined_heat_low_score", "combined_heat_mid_range_low_score"}
MARKET_STALL_FILTERS = {"market_stall", "combined_heat_mid_range_market_stall"}
EXPERIMENTAL_EXIT_RULES = {"off", "daily_close_stop"}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def add_symbol_risk(symbols: dict[str, dict[str, Any]], symbol: str, tag: str, reason: str) -> None:
    row = symbols.setdefault(symbol, {"tags": [], "reasons": [], "action_veto": False})
    if tag not in row["tags"]:
        row["tags"].append(tag)
    if reason not in row["reasons"]:
        row["reasons"].append(reason)


def point_in_time_symbol_risk(records: list[dict[str, Any]], as_of_date: dt.date) -> dict[str, dict[str, Any]]:
    per_symbol: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        symbol = record.get("symbol")
        call_date = record.get("call_date")
        if not symbol or not call_date:
            continue
        try:
            parsed_call_date = parse_date(str(call_date))
        except ValueError:
            continue
        if parsed_call_date >= as_of_date:
            continue
        per_symbol.setdefault(str(symbol), []).append(record)

    symbols: dict[str, dict[str, Any]] = {}
    for symbol, symbol_records in per_symbol.items():
        decisive = [record for record in symbol_records if record.get("verdict") in {"pass", "fail"}]
        pass_count = sum(1 for record in decisive if record.get("verdict") == "pass")
        if len(decisive) >= 3 and pass_count / len(decisive) < 0.25:
            add_symbol_risk(symbols, symbol, "low_symbol_pass_rate", f"point_in_time_pass_rate={pass_count / len(decisive):.3f} over {len(decisive)} decisive records")
        returns = [float(record.get("return_pct") or 0.0) for record in symbol_records]
        if len(returns) >= 3 and statistics.fmean(returns) < 0.0:
            add_symbol_risk(symbols, symbol, "negative_symbol_avg_return", f"point_in_time_avg_return_pct={statistics.fmean(returns):.3f} over {len(returns)} records")
        if any(float(record.get("return_pct") or 0.0) <= -8.0 for record in symbol_records):
            add_symbol_risk(symbols, symbol, "recent_symbol_adverse_breach", "point-in-time record return breached -8.0% adverse threshold")
        if any(record.get("learning_tag") == "symbol_selection_error" for record in symbol_records):
            add_symbol_risk(symbols, symbol, "repeated_symbol_selection_error", "point-in-time records include symbol_selection_error")
    return symbols


def load_symbol_risk_records(path: pathlib.Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    data = load_json(path)
    records = data.get("records") if isinstance(data, dict) else data
    return records if isinstance(records, list) else []


def quality_count(entry: dict[str, Any], key: str) -> int:
    try:
        return int(entry.get("quality", {}).get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0


def registry_rejection_reasons(entry: dict[str, Any]) -> list[str]:
    reasons = []
    if quality_count(entry, "missing_latest_close") != 0:
        reasons.append("missing_latest_close")
    if entry.get("quality", {}).get("date_mismatch"):
        reasons.append("date_mismatch")
    if entry.get("as_of_date") and str(entry.get("as_of_date")) != str(entry.get("date")):
        reasons.append("as_of_date_mismatch")
    if quality_count(entry, "quote_date_mismatch_count") != 0:
        reasons.append("quote_date_mismatch")
    if quality_count(entry, "future_quote_date_count") != 0:
        reasons.append("future_quote_date")
    if quality_count(entry, "invalid_quote_date_count") != 0:
        reasons.append("invalid_quote_date")
    try:
        parse_date(str(entry.get("date")))
    except ValueError:
        reasons.append("invalid_entry_date")
    return reasons


def registry_quality_summary(registry: dict[str, Any], snapshot_type: str) -> dict[str, int]:
    summary = {
        "registry_entry_count": 0,
        "usable_registry_entry_count": 0,
        "skipped_registry_entry_count": 0,
        "skipped_missing_latest_close_count": 0,
        "skipped_date_mismatch_count": 0,
        "skipped_as_of_date_mismatch_count": 0,
        "skipped_quote_date_mismatch_count": 0,
        "skipped_future_quote_date_count": 0,
        "skipped_invalid_quote_date_count": 0,
        "skipped_invalid_entry_date_count": 0,
        "quote_date_mismatch_item_count": 0,
        "future_quote_date_item_count": 0,
        "invalid_quote_date_item_count": 0,
    }
    for entry in registry.get("entries", []):
        if entry.get("snapshot_type") != snapshot_type:
            continue
        if entry.get("session") not in {"close", "historical"}:
            continue
        summary["registry_entry_count"] += 1
        summary["quote_date_mismatch_item_count"] += quality_count(entry, "quote_date_mismatch_count")
        summary["future_quote_date_item_count"] += quality_count(entry, "future_quote_date_count")
        summary["invalid_quote_date_item_count"] += quality_count(entry, "invalid_quote_date_count")
        reasons = registry_rejection_reasons(entry)
        if not reasons:
            summary["usable_registry_entry_count"] += 1
            continue
        summary["skipped_registry_entry_count"] += 1
        for reason in set(reasons):
            summary[f"skipped_{reason}_count"] += 1
    return summary


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
        if entry.get("as_of_date") and str(entry.get("as_of_date")) != str(entry.get("date")):
            continue
        if registry_rejection_reasons(entry):
            continue
        entry_date = parse_date(str(entry.get("date")))
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


def price_path_points(entries: list[dict[str, Any]], base_date: dt.date, future_date: dt.date, symbol: str, base_price: float) -> list[dict[str, Any]]:
    points = []
    for entry in entries:
        if not (base_date < entry["_date"] <= future_date):
            continue
        item = snapshot_items(load_json(pathlib.Path(entry["path"]))).get(symbol)
        if item and item.get("latest_close") and base_price:
            price = float(item["latest_close"])
            points.append(
                {
                    "entry": entry,
                    "date": entry["date"],
                    "_date": entry["_date"],
                    "price": price,
                    "return_pct": ((price / base_price) - 1.0) * 100.0,
                }
            )
    return points


def experimental_exit_outcome(
    price_points: list[dict[str, Any]],
    fallback_entry: dict[str, Any],
    exit_rule: str,
    stop_loss_pct: float,
) -> tuple[dict[str, Any], bool, str | None]:
    if exit_rule == "off":
        return fallback_entry, False, None
    if exit_rule != "daily_close_stop":
        raise ValueError(f"experimental_exit_rule must be one of {sorted(EXPERIMENTAL_EXIT_RULES)}")
    for point in price_points:
        if point["return_pct"] <= stop_loss_pct:
            return point["entry"], True, "daily_close_stop_loss"
    return fallback_entry, False, None


def safe_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def bucket_numeric(value: Any, cuts: list[tuple[float, str]], high_label: str, missing_label: str = "missing") -> str:
    number = safe_float(value)
    if number is None:
        return missing_label
    for upper, label in cuts:
        if number < upper:
            return label
    return high_label


def market_family_for_record(record: dict[str, Any]) -> str:
    family = record.get("market_family")
    if family:
        return str(family)
    return market_family_for_symbol(str(record.get("symbol") or ""))


def performance_stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    returns = [value for value in (safe_float(record.get("net_return_pct")) for record in records) if value is not None]
    alphas = [value for value in (safe_float(record.get("alpha_pct")) for record in records) if value is not None]
    adverse_values = [value for value in (safe_float(record.get("max_adverse_pct")) for record in records) if value is not None]
    scores = [value for value in (safe_float(record.get("score")) for record in records) if value is not None]
    ranges = [value for value in (safe_float(record.get("range_pos_60")) for record in records) if value is not None]
    volumes = [value for value in (safe_float(record.get("volume_ratio_20")) for record in records) if value is not None]
    pct_changes = [value for value in (safe_float(record.get("pct_change_1d")) for record in records) if value is not None]
    market_ranges = [value for value in (safe_float(record.get("market_range_pos_60")) for record in records) if value is not None]
    breach_count = sum(1 for record in records if record.get("adverse_breach"))
    return {
        "sample_count": len(records),
        "win_rate": round(sum(1 for value in returns if value > 0) / len(returns), 3) if returns else None,
        "avg_net_return_pct": round(statistics.fmean(returns), 3) if returns else None,
        "median_net_return_pct": round(statistics.median(returns), 3) if returns else None,
        "avg_alpha_pct": round(statistics.fmean(alphas), 3) if alphas else None,
        "avg_max_adverse_pct": round(statistics.fmean(adverse_values), 3) if adverse_values else None,
        "max_adverse_pct": round(min(adverse_values), 3) if adverse_values else None,
        "adverse_breach_count": breach_count,
        "adverse_breach_rate": round(breach_count / len(adverse_values), 3) if adverse_values else None,
        "avg_score": round(statistics.fmean(scores), 3) if scores else None,
        "avg_range_pos_60": round(statistics.fmean(ranges), 3) if ranges else None,
        "avg_volume_ratio_20": round(statistics.fmean(volumes), 3) if volumes else None,
        "avg_pct_change_1d": round(statistics.fmean(pct_changes), 3) if pct_changes else None,
        "avg_market_range_pos_60": round(statistics.fmean(market_ranges), 3) if market_ranges else None,
    }


def grouped_stats(records: list[dict[str, Any]], field_name: str, key_fn) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        key = str(key_fn(record) or "unknown")
        buckets.setdefault(key, []).append(record)
    rows = [{field_name: key, **performance_stats(rows)} for key, rows in buckets.items()]
    return sorted(rows, key=lambda row: (row.get("sample_count") or 0, row.get("adverse_breach_count") or 0), reverse=True)


def driver_bucket_stats(records: list[dict[str, Any]], field_name: str, bucket_fn) -> list[dict[str, Any]]:
    rows = grouped_stats(records, "bucket", lambda record: bucket_fn(record.get(field_name)))
    return sorted(rows, key=lambda row: (row.get("adverse_breach_rate") or 0.0, row.get("adverse_breach_count") or 0, row.get("sample_count") or 0), reverse=True)


def compact_record(record: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "base_date",
        "future_date",
        "planned_future_date",
        "exit_rule",
        "exit_triggered",
        "exit_reason",
        "stop_loss_pct",
        "symbol",
        "market_family",
        "theme",
        "net_return_pct",
        "unmanaged_net_return_pct",
        "alpha_pct",
        "max_adverse_pct",
        "unmanaged_max_adverse_pct",
        "score",
        "range_pos_60",
        "volume_ratio_20",
        "pct_change_1d",
        "market_proxy_symbol",
        "market_range_pos_60",
    ]
    return {key: record.get(key) for key in keys if key in record}


def build_risk_diagnostics(records: list[dict[str, Any]], max_adverse_limit_pct: float) -> dict[str, Any]:
    adverse_records = [record for record in records if record.get("adverse_breach")]
    worst_records = sorted(
        [record for record in records if safe_float(record.get("max_adverse_pct")) is not None],
        key=lambda record: safe_float(record.get("max_adverse_pct")) or 0.0,
    )[:20]
    return {
        "max_adverse_limit_pct": max_adverse_limit_pct,
        "by_market_family": grouped_stats(records, "market_family", market_family_for_record),
        "by_theme": grouped_stats(records, "theme", lambda record: record.get("theme")),
        "by_symbol": grouped_stats(records, "symbol", lambda record: record.get("symbol")),
        "by_month": grouped_stats(records, "month", lambda record: str(record.get("base_date") or "")[:7]),
        "adverse_breach_count": len(adverse_records),
        "adverse_breach_records": [compact_record(record) for record in sorted(adverse_records, key=lambda record: safe_float(record.get("max_adverse_pct")) or 0.0)[:50]],
        "worst_adverse_records": [compact_record(record) for record in worst_records],
        "driver_buckets": {
            "range_pos_60": driver_bucket_stats(
                records,
                "range_pos_60",
                lambda value: bucket_numeric(value, [(0.35, "lt_0_35"), (0.70, "0_35_to_0_70"), (0.85, "0_70_to_0_85"), (1.01, "0_85_to_1_00")], "gt_1_00"),
            ),
            "volume_ratio_20": driver_bucket_stats(
                records,
                "volume_ratio_20",
                lambda value: bucket_numeric(value, [(1.0, "lt_1_00"), (1.5, "1_00_to_1_50"), (2.5, "1_50_to_2_50")], "gte_2_50"),
            ),
            "pct_change_1d": driver_bucket_stats(
                records,
                "pct_change_1d",
                lambda value: bucket_numeric(value, [(-2.0, "lt_neg_2"), (0.0, "neg_2_to_0"), (2.0, "0_to_2"), (5.0, "2_to_5")], "gte_5"),
            ),
            "market_range_pos_60": driver_bucket_stats(
                records,
                "market_range_pos_60",
                lambda value: bucket_numeric(value, [(0.30, "lt_0_30"), (0.50, "0_30_to_0_50"), (0.70, "0_50_to_0_70"), (1.01, "0_70_to_1_00")], "gt_1_00"),
            ),
        },
    }


def append_unique(row: dict[str, Any], key: str, value: str) -> None:
    values = row.setdefault(key, [])
    if value not in values:
        values.append(value)


def experimental_risk_filter_reasons(row: dict[str, Any], profile: str) -> list[str]:
    if profile == "off":
        return []
    pct_change = safe_float(row.get("pct_change_1d"))
    volume_ratio = safe_float(row.get("volume_ratio_20"))
    range_pos = safe_float(row.get("range_pos_60"))
    market_range = safe_float(row.get("market_range_pos_60"))
    score = safe_float(row.get("score"))
    reasons = []
    if profile in PCT_HEAT_FILTERS and pct_change is not None and pct_change >= 5.0:
        reasons.append("pct_change_1d_gte_5")
    if (
        profile in VOLUME_RANGE_HEAT_FILTERS
        and volume_ratio is not None
        and range_pos is not None
        and volume_ratio >= 2.5
        and range_pos >= 0.85
    ):
        reasons.append("volume_ratio_20_gte_2_5_and_range_pos_60_gte_0_85")
    if (
        profile in MARKET_PCT_HEAT_FILTERS
        and market_range is not None
        and pct_change is not None
        and market_range >= 0.50
        and pct_change >= 5.0
    ):
        reasons.append("market_range_pos_60_gte_0_50_and_pct_change_1d_gte_5")
    if profile in MID_RANGE_FILTERS and range_pos is not None and 0.35 <= range_pos < 0.70:
        reasons.append("range_pos_60_between_0_35_and_0_70")
    if profile in LOW_SCORE_FILTERS and score is not None and score < 70.0:
        reasons.append("score_below_70")
    if (
        profile in MARKET_STALL_FILTERS
        and range_pos is not None
        and market_range is not None
        and pct_change is not None
        and range_pos >= 0.88
        and market_range >= 0.55
        and pct_change <= 1.5
    ):
        reasons.append("range_pos_60_gte_0_88_market_range_pos_60_gte_0_55_pct_change_1d_lte_1_5")
    return reasons


def apply_experimental_risk_filter(ranked: list[dict[str, Any]], profile: str) -> None:
    if profile not in EXPERIMENTAL_RISK_FILTERS:
        raise ValueError(f"experimental risk filter must be one of {sorted(EXPERIMENTAL_RISK_FILTERS)}")
    if profile == "off":
        return
    for row in ranked:
        if not row.get("qualified_for_action"):
            continue
        reasons = experimental_risk_filter_reasons(row, profile)
        if not reasons:
            continue
        row["qualified_for_action"] = False
        row["diagnostic_only"] = True
        row["experimental_risk_filter_profile"] = profile
        row["experimental_risk_filter_reasons"] = reasons
        append_unique(row, "qualification_flags", "experimental_risk_filter_applied")
        for reason in reasons:
            append_unique(row, "action_disqualifiers", f"experimental_{reason}")


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
    symbol_risk: dict[str, dict[str, Any]] | None = None,
    market_proxy_symbol: str = DEFAULT_MARKET_PROXY_SYMBOL,
    max_market_range_for_action: float = DEFAULT_MAX_MARKET_RANGE_FOR_ACTION,
    symbol_risk_mode: str = "full",
    symbol_risk_records: list[dict[str, Any]] | None = None,
    experimental_risk_filter: str = "off",
    experimental_exit_rule: str = "off",
    stop_loss_pct: float = -6.0,
) -> dict[str, Any]:
    if candidate_policy not in {"strict", "relaxed"}:
        raise ValueError("candidate_policy must be strict or relaxed")
    if symbol_risk_mode not in {"full", "point_in_time", "off"}:
        raise ValueError("symbol_risk_mode must be full, point_in_time, or off")
    if experimental_risk_filter not in EXPERIMENTAL_RISK_FILTERS:
        raise ValueError(f"experimental_risk_filter must be one of {sorted(EXPERIMENTAL_RISK_FILTERS)}")
    if experimental_exit_rule not in EXPERIMENTAL_EXIT_RULES:
        raise ValueError(f"experimental_exit_rule must be one of {sorted(EXPERIMENTAL_EXIT_RULES)}")
    if experimental_exit_rule != "off" and stop_loss_pct >= 0:
        raise ValueError("stop_loss_pct must be negative for experimental exit rules")
    registry = load_json(registry_path)
    quality_summary = registry_quality_summary(registry, "trade")
    entries = filter_entries_as_of(registry_entries(registry, "trade"), as_of_date)
    cost_pct = round_trip_bps / 100.0
    actionable_top_n = top_n if actionable_top_n is None else actionable_top_n
    diagnostic_top_n = top_n if diagnostic_top_n is None else diagnostic_top_n
    diagnostic_records = []
    symbol_risk = symbol_risk or {}
    symbol_risk_records = symbol_risk_records or []

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
            benchmark_future = future_items.get(benchmark_symbol)
            scored = annotate_theme_positions([item_score(item, weights, min_watch_score) for item in base_items.values()])
            apply_market_context(scored, base_snapshot, market_proxy_symbol, max_market_range_for_action)
            apply_edge_cost_fields(scored, round_trip_bps, minimum_edge_bps)
            ranked = sorted(scored, key=lambda row: row["score"], reverse=True)
            if symbol_risk_mode == "point_in_time":
                entry_symbol_risk = point_in_time_symbol_risk(symbol_risk_records, entry["_date"])
            elif symbol_risk_mode == "off":
                entry_symbol_risk = {}
            else:
                entry_symbol_risk = symbol_risk
            apply_action_qualification(ranked, min_action_score, entry_symbol_risk)
            apply_experimental_risk_filter(ranked, experimental_risk_filter)
            actionable, diagnostics, _top = candidate_layers(ranked, actionable_top_n, diagnostic_top_n)
            if use_relaxed_top_n:
                candidates = list(actionable)
                if len(candidates) < actionable_top_n:
                    fill = [row for row in diagnostics if row.get("symbol") not in {candidate.get("symbol") for candidate in candidates}]
                    candidates.extend(fill[: actionable_top_n - len(candidates)])
            else:
                candidates = actionable
            def append_record(candidate: dict[str, Any], rank: int, sample_type: str) -> None:
                symbol = str(candidate["symbol"])
                base_item = base_items.get(symbol)
                future_item = future_items.get(symbol)
                horizon_item = future_item
                if not base_item or not horizon_item or not base_item.get("latest_close") or not horizon_item.get("latest_close"):
                    return
                base_price = float(base_item["latest_close"])
                price_points = price_path_points(entries, entry["_date"], future_entry["_date"], symbol, base_price)
                outcome_entry, exit_triggered, exit_reason = experimental_exit_outcome(price_points, future_entry, experimental_exit_rule, stop_loss_pct)
                outcome_snapshot = future_snapshot if outcome_entry["date"] == future_entry["date"] else load_json(pathlib.Path(outcome_entry["path"]))
                outcome_items = snapshot_items(outcome_snapshot)
                outcome_item = outcome_items.get(symbol)
                if not outcome_item or not outcome_item.get("latest_close"):
                    return
                candidate_benchmark_symbol = benchmark_symbol
                if market_family_for_symbol(symbol) == "cn" and base_items.get(DEFAULT_CN_MARKET_PROXY_SYMBOL) and outcome_items.get(DEFAULT_CN_MARKET_PROXY_SYMBOL):
                    candidate_benchmark_symbol = DEFAULT_CN_MARKET_PROXY_SYMBOL
                benchmark_base = base_items.get(candidate_benchmark_symbol)
                benchmark_future = outcome_items.get(candidate_benchmark_symbol)
                benchmark_return = None
                if benchmark_base and benchmark_future and benchmark_base.get("latest_close"):
                    benchmark_return = ((float(benchmark_future["latest_close"]) / float(benchmark_base["latest_close"])) - 1.0) * 100.0 - cost_pct
                gross_return = ((float(outcome_item["latest_close"]) / base_price) - 1.0) * 100.0
                unmanaged_gross_return = ((float(horizon_item["latest_close"]) / base_price) - 1.0) * 100.0
                net_return = gross_return - cost_pct
                unmanaged_adverse_values = [point["return_pct"] for point in price_points]
                managed_adverse_values = [point["return_pct"] for point in price_points if point["_date"] <= outcome_entry["_date"]]
                adverse = min(managed_adverse_values) if managed_adverse_values else None
                unmanaged_adverse = min(unmanaged_adverse_values) if unmanaged_adverse_values else None
                below_watch_score = candidate["score"] < min_watch_score
                adverse_breach = adverse is not None and adverse < max_adverse_limit_pct
                low_quality_flags = []
                if below_watch_score:
                    low_quality_flags.append("below_watch_score")
                if candidate.get("diagnostic_only"):
                    low_quality_flags.append("diagnostic_only")
                low_quality_flags.extend(candidate.get("disqualifiers") or [])
                default_actionable_layer = sample_type == "actionable"
                source_layer = candidate.get("source_layer") or ("actionable_candidates" if default_actionable_layer else "diagnostic_candidates")
                layer_action_cap = candidate.get("layer_action_cap") or ("buy_candidate" if default_actionable_layer else "watch_only")
                record = {
                    "base_date": entry["date"],
                    "future_date": outcome_entry["date"],
                    "planned_future_date": future_entry["date"],
                    "window_days": (outcome_entry["_date"] - entry["_date"]).days,
                    "planned_window_days": (future_entry["_date"] - entry["_date"]).days,
                    "rank": rank,
                    "sample_type": sample_type,
                    "source_layer": source_layer,
                    "eligible_for_action_from_layer": bool(candidate.get("eligible_for_action_from_layer", default_actionable_layer)),
                    "layer_action_cap": layer_action_cap,
                    "symbol": symbol,
                    "market_family": market_family_for_symbol(symbol),
                    "theme": candidate.get("theme"),
                    "kind": candidate.get("kind"),
                    "score": candidate["score"],
                    "below_watch_score": below_watch_score,
                    "qualified_for_watch": bool(candidate.get("qualified_for_watch")),
                    "qualified_for_action": bool(candidate.get("qualified_for_action")),
                    "diagnostic_only": bool(candidate.get("diagnostic_only")),
                    "theme_rank": candidate.get("theme_rank"),
                    "theme_peer_count": candidate.get("theme_peer_count"),
                    "theme_leader": candidate.get("theme_leader"),
                    "theme_leader_score": candidate.get("theme_leader_score"),
                    "theme_score_gap_to_leader": candidate.get("theme_score_gap_to_leader"),
                    "same_theme_best_symbol": candidate.get("same_theme_best_symbol"),
                    "same_theme_best_score": candidate.get("same_theme_best_score"),
                    "same_theme_selected_vs_best_score_gap": candidate.get("same_theme_selected_vs_best_score_gap"),
                    "same_theme_next_best_symbol": candidate.get("same_theme_next_best_symbol"),
                    "same_theme_selected_vs_next_best_score_gap": candidate.get("same_theme_selected_vs_next_best_score_gap"),
                    "same_theme_peer_evidence_passed": candidate.get("same_theme_peer_evidence_passed"),
                    "peer_relative_decision": candidate.get("peer_relative_decision"),
                    "is_theme_leader": bool(candidate.get("is_theme_leader")),
                    "qualification_flags": candidate.get("qualification_flags", []),
                    "disqualifiers": candidate.get("disqualifiers", []),
                    "action_disqualifiers": candidate.get("action_disqualifiers", []),
                    "experimental_risk_filter_profile": candidate.get("experimental_risk_filter_profile"),
                    "experimental_risk_filter_reasons": candidate.get("experimental_risk_filter_reasons", []),
                    "low_quality_flags": low_quality_flags,
                    "pct_change_1d": candidate.get("pct_change_1d"),
                    "range_pos_60": candidate.get("range_pos_60"),
                    "volume_ratio_20": candidate.get("volume_ratio_20"),
                    "market_proxy_symbol": candidate.get("market_proxy_symbol"),
                    "market_range_pos_60": candidate.get("market_range_pos_60"),
                    "market_pct_change_1d": candidate.get("market_pct_change_1d"),
                    "market_volume_ratio_20": candidate.get("market_volume_ratio_20"),
                    "max_market_range_for_action": candidate.get("max_market_range_for_action"),
                    "base_price": round(base_price, 4),
                    "future_price": round(float(outcome_item["latest_close"]), 4),
                    "planned_future_price": round(float(horizon_item["latest_close"]), 4),
                    "net_return_pct": round(net_return, 3),
                    "unmanaged_net_return_pct": round(unmanaged_gross_return - cost_pct, 3),
                    "max_adverse_pct": round(adverse, 3) if adverse is not None else None,
                    "unmanaged_max_adverse_pct": round(unmanaged_adverse, 3) if unmanaged_adverse is not None else None,
                    "adverse_breach": adverse_breach,
                    "exit_rule": experimental_exit_rule,
                    "exit_triggered": exit_triggered,
                    "exit_reason": exit_reason,
                    "stop_loss_pct": stop_loss_pct if experimental_exit_rule != "off" else None,
                    "benchmark_symbol": candidate_benchmark_symbol,
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
    relaxed_diagnostic_sample_count = sum(1 for record in records if record.get("sample_type") == "relaxed_diagnostic")
    qualified_sample_count = sum(1 for record in records if record.get("qualified_for_action"))
    promotable_sample_count = sum(1 for record in records if record.get("eligible_for_action_from_layer") and record.get("qualified_for_action"))
    exit_triggered_count = sum(1 for record in records if record.get("exit_triggered"))
    diagnostic_layer_sample_count = len(diagnostic_records)
    diagnostic_only_sample_count = sum(
        1
        for record in [*diagnostic_records, *records]
        if record.get("source_layer") == "diagnostic_candidates" or record.get("sample_type") == "relaxed_diagnostic" or record.get("diagnostic_only")
    )
    diagnostic_sample_count = diagnostic_layer_sample_count + relaxed_diagnostic_sample_count
    strict_sample_count = len(strict_records)
    relaxed_sample_count = relaxed_diagnostic_sample_count if use_relaxed else 0
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
        "cn_benchmark_symbol": DEFAULT_CN_MARKET_PROXY_SYMBOL,
        "min_watch_score": min_watch_score,
        "min_action_score": min_action_score,
        "candidate_policy": candidate_policy,
        "max_adverse_limit_pct": max_adverse_limit_pct,
        "symbol_risk_mode": symbol_risk_mode,
        "symbol_risk_point_in_time": symbol_risk_mode == "point_in_time",
        "symbol_risk_record_count": len(symbol_risk_records),
        "experimental_risk_filter": experimental_risk_filter,
        "experimental_exit_rule": experimental_exit_rule,
        "stop_loss_pct": stop_loss_pct if experimental_exit_rule != "off" else None,
        "market_proxy_symbol": market_proxy_symbol,
        "cn_market_proxy_symbol": DEFAULT_CN_MARKET_PROXY_SYMBOL,
        "max_market_range_for_action": max_market_range_for_action,
        "as_of_date": as_of_date.isoformat() if as_of_date else None,
        "sample_count": len(records),
        "production_sample_count": len(records),
        "promotable_sample_count": promotable_sample_count,
        "strict_sample_count": strict_sample_count,
        "relaxed_sample_count": relaxed_sample_count,
        "qualified_sample_count": qualified_sample_count,
        "exit_triggered_count": exit_triggered_count,
        "exit_triggered_rate": round(exit_triggered_count / len(records), 3) if records else None,
        "diagnostic_layer_sample_count": diagnostic_layer_sample_count,
        "diagnostic_only_sample_count": diagnostic_only_sample_count,
        "diagnostic_sample_count": diagnostic_sample_count,
        "sample_quality": sample_quality,
        "avg_net_return_pct": round(statistics.fmean(returns), 3) if returns else None,
        "median_net_return_pct": round(statistics.median(returns), 3) if returns else None,
        "win_rate": round(sum(1 for value in returns if value > 0) / len(returns), 3) if returns else None,
        "avg_alpha_pct": round(statistics.fmean(alphas), 3) if alphas else None,
        "avg_max_adverse_pct": round(statistics.fmean(adverse_values), 3) if adverse_values else None,
        "max_adverse_pct": round(min(adverse_values), 3) if adverse_values else None,
        "adverse_breach_rate": round(len(adverse_breaches) / len(adverse_values), 3) if adverse_values else None,
        **quality_summary,
    }
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "registry": str(registry_path),
        "summary": summary,
        "risk_diagnostics": build_risk_diagnostics(records, max_adverse_limit_pct),
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
        f"Production samples: `{summary.get('production_sample_count', summary['sample_count'])}`",
        f"Promotable samples: `{summary.get('promotable_sample_count', summary['qualified_sample_count'])}`",
        f"Sample quality: `{summary['sample_quality']}`",
        f"Strict samples: `{summary['strict_sample_count']}`",
        f"Relaxed samples: `{summary['relaxed_sample_count']}`",
        f"Qualified samples: `{summary['qualified_sample_count']}`",
        f"Symbol risk mode: `{summary.get('symbol_risk_mode')}`",
        f"Symbol risk point-in-time: `{summary.get('symbol_risk_point_in_time')}`",
        f"Experimental risk filter: `{summary.get('experimental_risk_filter')}`",
        f"Experimental exit rule: `{summary.get('experimental_exit_rule')}`",
        f"Stop loss pct: `{summary.get('stop_loss_pct')}`",
        f"Exit triggered rate: `{summary.get('exit_triggered_rate')}`",
        f"Default market proxy: `{summary.get('market_proxy_symbol')}`",
        f"CN market proxy: `{summary.get('cn_market_proxy_symbol')}`",
        f"Diagnostic layer samples: `{summary.get('diagnostic_layer_sample_count', summary['diagnostic_sample_count'])}`",
        f"Diagnostic-only samples: `{summary.get('diagnostic_only_sample_count', summary['diagnostic_sample_count'])}`",
        f"Diagnostic samples: `{summary['diagnostic_sample_count']}`",
        f"Average net return: `{summary['avg_net_return_pct']}`%",
        f"Win rate: `{summary['win_rate']}`",
        f"Default benchmark: `{summary.get('benchmark_symbol')}`",
        f"CN benchmark: `{summary.get('cn_benchmark_symbol')}`",
        f"Average benchmark alpha: `{summary['avg_alpha_pct']}`%",
        f"Average max adverse return: `{summary['avg_max_adverse_pct']}`%",
        f"Max adverse-ish return: `{summary['max_adverse_pct']}`%",
        f"Adverse breach rate: `{summary['adverse_breach_rate']}`",
        f"Registry entries: `{summary.get('registry_entry_count')}`",
        f"Usable registry entries: `{summary.get('usable_registry_entry_count')}`",
        f"Skipped registry entries: `{summary.get('skipped_registry_entry_count')}`",
        f"Skipped quote-date mismatch entries: `{summary.get('skipped_quote_date_mismatch_count')}`",
        f"Skipped future quote-date entries: `{summary.get('skipped_future_quote_date_count')}`",
        "",
        "## Weights",
    ]
    for key, value in summary["strategy_weights"].items():
        lines.append(f"- `{key}`: {value}")
    diagnostics = result.get("risk_diagnostics", {}) if isinstance(result.get("risk_diagnostics"), dict) else {}
    lines.extend(["", "## Market Family Risk"])
    for row in diagnostics.get("by_market_family", []):
        lines.append(
            f"- `{row.get('market_family')}`: samples={row.get('sample_count')}, win={row.get('win_rate')}, "
            f"avg={row.get('avg_net_return_pct')}%, alpha={row.get('avg_alpha_pct')}%, "
            f"max_adverse={row.get('max_adverse_pct')}%, breach_rate={row.get('adverse_breach_rate')}"
        )
    lines.extend(["", "## Worst Adverse Records"])
    for record in diagnostics.get("worst_adverse_records", [])[:10]:
        lines.append(
            f"- `{record.get('base_date')}` `{record.get('symbol')}` ({record.get('market_family')}): "
            f"net={record.get('net_return_pct')}%, adverse={record.get('max_adverse_pct')}%, "
            f"range={record.get('range_pos_60')}, volume={record.get('volume_ratio_20')}, pct_1d={record.get('pct_change_1d')}"
        )
    lines.extend(["", "## Adverse Driver Buckets"])
    for field, rows in diagnostics.get("driver_buckets", {}).items():
        lines.append(f"### `{field}`")
        for row in rows[:5]:
            lines.append(
                f"- `{row.get('bucket')}`: samples={row.get('sample_count')}, breaches={row.get('adverse_breach_count')}, "
                f"breach_rate={row.get('adverse_breach_rate')}, max_adverse={row.get('max_adverse_pct')}%"
            )
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
    parser.add_argument("--symbol-risk-json", default=None, help="Optional symbol risk memory JSON for current-production diagnostic backtests.")
    parser.add_argument("--symbol-risk-mode", choices=["full", "point_in_time", "off"], default="full")
    parser.add_argument("--symbol-risk-records-json", default=None, help="Evaluation records JSON used to build point-in-time symbol risk during historical backtests.")
    parser.add_argument("--experimental-risk-filter", choices=sorted(EXPERIMENTAL_RISK_FILTERS), default="off", help="Backtest-only action downgrade profile for candidate risk-filter experiments.")
    parser.add_argument("--experimental-exit-rule", choices=sorted(EXPERIMENTAL_EXIT_RULES), default="off", help="Backtest-only holding-period exit rule experiment.")
    parser.add_argument("--stop-loss-pct", type=float, default=-6.0, help="Daily-close stop threshold for experimental exit rules.")
    parser.add_argument("--market-proxy-symbol", default=DEFAULT_MARKET_PROXY_SYMBOL)
    parser.add_argument("--max-market-range-for-action", type=float, default=DEFAULT_MAX_MARKET_RANGE_FOR_ACTION)
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
        load_symbol_risk(pathlib.Path(args.symbol_risk_json)) if args.symbol_risk_json else None,
        args.market_proxy_symbol,
        args.max_market_range_for_action,
        args.symbol_risk_mode,
        load_symbol_risk_records(pathlib.Path(args.symbol_risk_records_json)) if args.symbol_risk_records_json else None,
        args.experimental_risk_filter,
        args.experimental_exit_rule,
        args.stop_loss_pct,
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
