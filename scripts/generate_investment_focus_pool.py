#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import tomllib
from statistics import mean
from typing import Any


DEFAULT_POLICY = {
    "max_active_industries": 4,
    "max_active_symbols_per_industry": 4,
    "max_watch_symbols_per_industry": 2,
    "min_active_industry_score": 55.0,
    "min_watch_industry_score": 42.0,
    "min_focus_symbol_score": 35.0,
}

DEFAULT_WEIGHTS = {
    "leader_score": 0.30,
    "average_top_score": 0.25,
    "breadth": 0.15,
    "volume_confirmation": 0.15,
    "actionability": 0.15,
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_toml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def as_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def merge_numeric_defaults(defaults: dict[str, float], raw: dict[str, Any]) -> dict[str, float]:
    values = dict(defaults)
    for key in values:
        if key in raw:
            values[key] = as_float(raw[key], values[key])
    return values


def normalize_industries(config: dict[str, Any]) -> list[dict[str, Any]]:
    industries = []
    for index, raw in enumerate(config.get("industries", []), start=1):
        if not isinstance(raw, dict):
            continue
        industry_id = str(raw.get("id") or raw.get("name") or f"industry_{index}").strip()
        if not industry_id:
            continue
        industries.append(
            {
                "id": industry_id,
                "name": str(raw.get("name") or industry_id),
                "strategic_weight": as_float(raw.get("strategic_weight"), 1.0),
                "priority": int(as_float(raw.get("priority"), index)),
                "max_active_symbols": int(as_float(raw.get("max_active_symbols"), 0)),
                "themes": [str(item) for item in raw.get("themes", [])],
                "leader_symbols": [str(item) for item in raw.get("leader_symbols", [])],
                "high_beta_symbols": [str(item) for item in raw.get("high_beta_symbols", [])],
                "confirming_symbols": [str(item) for item in raw.get("confirming_symbols", [])],
            }
        )
    return industries


def build_lookup(industries: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_theme: dict[str, dict[str, Any]] = {}
    by_symbol: dict[str, dict[str, Any]] = {}
    for industry in industries:
        for theme in industry["themes"]:
            by_theme.setdefault(theme, industry)
        for key in ("leader_symbols", "high_beta_symbols", "confirming_symbols"):
            for symbol in industry[key]:
                by_symbol.setdefault(symbol, industry)
    return by_theme, by_symbol


def industry_for_row(row: dict[str, Any], by_theme: dict[str, dict[str, Any]], by_symbol: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    symbol = str(row.get("symbol") or "")
    if symbol in by_symbol:
        return by_symbol[symbol]
    theme = str(row.get("theme") or "")
    return by_theme.get(theme)


def role_for_symbol(symbol: str, industry: dict[str, Any]) -> str:
    if symbol in industry["confirming_symbols"]:
        return "confirming_etf"
    if symbol in industry["leader_symbols"]:
        return "leader"
    if symbol in industry["high_beta_symbols"]:
        return "high_beta"
    return "configured_theme_member"


def volume_score(row: dict[str, Any]) -> float:
    ratio = row.get("volume_ratio_20")
    if ratio is None:
        return 45.0
    return clamp(as_float(ratio) / 2.0 * 100.0, 0.0, 100.0)


def actionability_score(rows: list[dict[str, Any]]) -> float:
    if any(row.get("qualified_for_action") is True for row in rows):
        return 100.0
    if any(row.get("qualified_for_watch") is True for row in rows):
        return 65.0
    if rows:
        return 25.0
    return 0.0


def focus_state(row: dict[str, Any]) -> str:
    if row.get("qualified_for_action") is True:
        return "actionable"
    if row.get("qualified_for_watch") is True:
        return "watch_only"
    return "diagnostic"


def focus_sort_key(row: dict[str, Any]) -> tuple[bool, bool, bool, float, float]:
    return (
        row.get("qualified_for_action") is True,
        row.get("qualified_for_watch") is True,
        not bool(row.get("diagnostic_only")),
        as_float(row.get("score")),
        volume_score(row),
    )


def compact_symbol(row: dict[str, Any], industry: dict[str, Any], industry_score: float, industry_rank: int | None, industry_status: str) -> dict[str, Any]:
    symbol = str(row.get("symbol") or "")
    return {
        "symbol": symbol,
        "name": row.get("name"),
        "theme": row.get("theme"),
        "kind": row.get("kind"),
        "score": row.get("score"),
        "focus_industry": industry["id"],
        "focus_industry_name": industry["name"],
        "focus_industry_score": industry_score,
        "focus_industry_rank": industry_rank,
        "focus_industry_status": industry_status,
        "focus_role": role_for_symbol(symbol, industry),
        "focus_state": focus_state(row),
        "qualified_for_action": row.get("qualified_for_action"),
        "qualified_for_watch": row.get("qualified_for_watch"),
        "diagnostic_only": row.get("diagnostic_only"),
        "cost_gate_passed": row.get("cost_gate_passed"),
        "volume_ratio_20": row.get("volume_ratio_20"),
        "disqualifiers": row.get("disqualifiers", []),
        "action_disqualifiers": row.get("action_disqualifiers", []),
    }


def rank_industries(ranking: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    policy = merge_numeric_defaults(DEFAULT_POLICY, config.get("policy", {}) if isinstance(config.get("policy"), dict) else {})
    weights = merge_numeric_defaults(DEFAULT_WEIGHTS, config.get("weights", {}) if isinstance(config.get("weights"), dict) else {})
    weight_total = sum(weights.values()) or 1.0
    industries = normalize_industries(config)
    by_theme, by_symbol = build_lookup(industries)
    rows_by_industry: dict[str, list[dict[str, Any]]] = {industry["id"]: [] for industry in industries}
    industry_by_id = {industry["id"]: industry for industry in industries}

    for row in ranking.get("all_ranked", []):
        if not isinstance(row, dict):
            continue
        industry = industry_for_row(row, by_theme, by_symbol)
        if industry is None:
            continue
        rows_by_industry[industry["id"]].append(row)

    industry_rows = []
    for industry in industries:
        rows = sorted(rows_by_industry.get(industry["id"], []), key=lambda row: as_float(row.get("score")), reverse=True)
        top_rows = rows[:4]
        leader = top_rows[0] if top_rows else None
        leader_score = as_float(leader.get("score")) if leader else 0.0
        average_top_score = mean(as_float(row.get("score")) for row in top_rows) if top_rows else 0.0
        breadth = 100.0 * sum(1 for row in rows if row.get("qualified_for_watch") is True) / max(1, len(rows))
        volume = mean(volume_score(row) for row in top_rows) if top_rows else 0.0
        actionability = actionability_score(rows)
        raw_score = (
            leader_score * weights["leader_score"]
            + average_top_score * weights["average_top_score"]
            + breadth * weights["breadth"]
            + volume * weights["volume_confirmation"]
            + actionability * weights["actionability"]
        ) / weight_total
        score = round(clamp(raw_score * industry["strategic_weight"], 0.0, 100.0), 2)
        if score >= policy["min_active_industry_score"] and rows:
            status = "active"
        elif score >= policy["min_watch_industry_score"] and rows:
            status = "watch"
        else:
            status = "diagnostic"
        industry_rows.append(
            {
                "id": industry["id"],
                "name": industry["name"],
                "strategic_weight": industry["strategic_weight"],
                "configured_priority": industry["priority"],
                "score": score,
                "status": status,
                "matched_symbol_count": len(rows),
                "qualified_watch_count": sum(1 for row in rows if row.get("qualified_for_watch") is True),
                "qualified_action_count": sum(1 for row in rows if row.get("qualified_for_action") is True),
                "leader_symbol": leader.get("symbol") if leader else None,
                "leader_score": round(leader_score, 2),
                "average_top_score": round(average_top_score, 2),
                "breadth_score": round(breadth, 2),
                "volume_confirmation_score": round(volume, 2),
                "actionability_score": round(actionability, 2),
                "reasons": [
                    f"leader={leader.get('symbol') if leader else 'none'} leader_score={round(leader_score, 2)}",
                    f"qualified_action_count={sum(1 for row in rows if row.get('qualified_for_action') is True)}",
                    f"qualified_watch_count={sum(1 for row in rows if row.get('qualified_for_watch') is True)}",
                    f"strategic_weight={industry['strategic_weight']}",
                ],
                "top_symbols": [],
            }
        )

    industry_rows.sort(key=lambda item: (as_float(item.get("score")), -as_float(item.get("configured_priority"), 99)), reverse=True)
    for rank, item in enumerate(industry_rows, start=1):
        item["rank"] = rank
        industry = industry_by_id[item["id"]]
        rows = sorted(rows_by_industry.get(item["id"], []), key=lambda row: as_float(row.get("score")), reverse=True)
        item["top_symbols"] = [compact_symbol(row, industry, item["score"], rank, item["status"]) for row in rows[:6]]

    active_industries = [item for item in industry_rows if item["status"] == "active"][: int(policy["max_active_industries"])]
    active_ids = {item["id"] for item in active_industries}
    active_symbols: list[dict[str, Any]] = []
    for item in active_industries:
        industry = industry_by_id[item["id"]]
        rows = sorted(rows_by_industry.get(item["id"], []), key=focus_sort_key, reverse=True)
        limit = industry["max_active_symbols"] or int(policy["max_active_symbols_per_industry"])
        selected = [row for row in rows if as_float(row.get("score")) >= policy["min_focus_symbol_score"]][:limit]
        active_symbols.extend(compact_symbol(row, industry, item["score"], item["rank"], item["status"]) for row in selected)

    watch_symbols: list[dict[str, Any]] = []
    watch_industries = [item for item in industry_rows if item["status"] == "watch"]
    for item in watch_industries:
        industry = industry_by_id[item["id"]]
        rows = sorted(rows_by_industry.get(item["id"], []), key=focus_sort_key, reverse=True)
        selected = [row for row in rows if row.get("qualified_for_watch") is True and as_float(row.get("score")) >= policy["min_focus_symbol_score"]][: int(policy["max_watch_symbols_per_industry"])]
        watch_symbols.extend(compact_symbol(row, industry, item["score"], item["rank"], item["status"]) for row in selected)

    return {
        "generated_at": utc_now(),
        "source_ranking": ranking.get("snapshot"),
        "as_of_date": ranking.get("as_of_date"),
        "as_of_session": ranking.get("as_of_session"),
        "policy": policy,
        "weights": weights,
        "focus_universe": [
            {
                "id": industry["id"],
                "name": industry["name"],
                "themes": industry["themes"],
                "leader_symbols": industry["leader_symbols"],
                "high_beta_symbols": industry["high_beta_symbols"],
                "confirming_symbols": industry["confirming_symbols"],
            }
            for industry in industries
        ],
        "industry_ranking": industry_rows,
        "active_focus_industries": [item["id"] for item in active_industries],
        "active_focus_symbols": active_symbols,
        "watch_focus_industries": [item["id"] for item in watch_industries],
        "watch_focus_symbols": watch_symbols,
        "diagnostic_only_industries": [item["id"] for item in industry_rows if item["id"] not in active_ids and item["status"] == "diagnostic"],
        "notes": [
            "Dynamic focus pool only changes daily attention, not the durable trade_universe whitelist.",
            "watch_focus_symbols are observation candidates from watch-level industries; they are not eligible for action unless deterministic ranking gates also pass.",
            "Symbols outside active_focus_symbols may remain in trade_universe but should not be upgraded solely because another focus industry is strong.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate dynamic focus industries and symbols from deterministic ranking output.")
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    ranking_path = pathlib.Path(args.ranking)
    config_path = pathlib.Path(args.config)
    result = rank_industries(load_json(ranking_path), load_toml(config_path))
    result["source_ranking_file"] = str(ranking_path)
    result["source_config"] = str(config_path)
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote investment focus pool: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
