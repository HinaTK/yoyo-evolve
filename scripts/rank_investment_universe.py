#!/usr/bin/env python3

import argparse
import json
import pathlib
from collections import defaultdict
from typing import Any


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
        penalty += 20
    if float(item.get("range_pos_60") or 0) < 0.15:
        penalty += 10
    if item.get("volume_ratio_20") is not None and float(item["volume_ratio_20"]) < 0.5:
        penalty += 8
    return penalty


def item_score(item: dict[str, Any]) -> dict[str, Any]:
    t_score = trend_score(item)
    m_score = momentum_score(item)
    penalty = risk_penalty(item)
    total = clamp(t_score * 0.45 + m_score * 0.35 + float(item.get("range_pos_60") or 0) * 20 - penalty, 0, 100)
    return {
        "symbol": item.get("symbol"),
        "name": item.get("name"),
        "kind": item.get("kind"),
        "theme": item.get("theme"),
        "score": round(total, 2),
        "trend_score": round(t_score, 2),
        "momentum_score": round(m_score, 2),
        "risk_penalty": round(penalty, 2),
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
                "members": [row["symbol"] for row in ordered],
            }
        )
    return sorted(summaries, key=lambda row: row["avg_score"], reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank a trade universe snapshot with deterministic technical scores.")
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-candidates", type=int, default=8)
    parser.add_argument("--min-watch-score", type=float, default=45)
    parser.add_argument("--min-action-score", type=float, default=65)
    parser.add_argument("--round-trip-bps", type=float, default=35)
    parser.add_argument("--minimum-edge-bps", type=float, default=100)
    args = parser.parse_args()

    snapshot_path = pathlib.Path(args.snapshot)
    snapshot = load_json(snapshot_path)
    scored = [item_score(item) for item in snapshot.get("items", [])]
    ranked = sorted(scored, key=lambda row: row["score"], reverse=True)
    candidates = [row for row in ranked if row["score"] >= args.min_watch_score][: args.max_candidates]

    output = {
        "snapshot": str(snapshot_path),
        "as_of_date": snapshot.get("as_of_date"),
        "generated_at": snapshot.get("generated_at"),
        "cost_gate": {
            "estimated_round_trip_bps": args.round_trip_bps,
            "minimum_edge_bps": args.minimum_edge_bps,
            "action_rule": "Do not upgrade unless expected swing edge exceeds both cost and minimum edge gates.",
        },
        "thresholds": {
            "min_watch_score": args.min_watch_score,
            "min_action_score": args.min_action_score,
        },
        "theme_summary": theme_summary(scored),
        "top_candidates": candidates,
        "all_ranked": ranked,
    }
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote ranking: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
