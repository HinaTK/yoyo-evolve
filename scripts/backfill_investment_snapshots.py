#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import math
import pathlib
import statistics
from typing import Any

from fetch_investment_data import ensure_dir, fetch_tencent_bundle, read_toml, summarize_market


ROOT = pathlib.Path(__file__).resolve().parent.parent


def build_historical_metric(symbol: str, name: str, kind: str, theme: str, series: list[list[Any]], index: int) -> dict[str, Any]:
    history = []
    for row in series[: index + 1]:
        date_str, open_p, close_p, high_p, low_p, volume = row[:6]
        history.append(
            {
                "date": date_str,
                "open": float(open_p),
                "close": float(close_p),
                "high": float(high_p),
                "low": float(low_p),
                "volume": float(volume),
                "turnover": float(row[8]) if len(row) > 8 else None,
            }
        )

    if len(history) < 20:
        raise ValueError(f"Not enough history for {symbol} at index {index}")

    latest = history[-1]
    prev = history[-2]
    closes = [item["close"] for item in history]
    volumes = [item["volume"] for item in history]
    ma20 = statistics.fmean(closes[-20:])
    ma60 = statistics.fmean(closes[-60:]) if len(closes) >= 60 else statistics.fmean(closes)
    high_60 = max(closes[-60:]) if len(closes) >= 60 else max(closes)
    low_60 = min(closes[-60:]) if len(closes) >= 60 else min(closes)
    range_pos_60 = 0.5 if math.isclose(high_60, low_60) else (latest["close"] - low_60) / (high_60 - low_60)
    avg_volume_20 = statistics.fmean(volumes[-20:]) if len(volumes) >= 20 else statistics.fmean(volumes)
    volume_ratio_20 = (latest["volume"] / avg_volume_20) if avg_volume_20 else None

    regime_flags = []
    if latest["close"] > ma20 > ma60:
        regime_flags.append("uptrend")
    elif latest["close"] < ma20 < ma60:
        regime_flags.append("downtrend")
    else:
        regime_flags.append("range")
    if volume_ratio_20 and volume_ratio_20 > 1.5:
        regime_flags.append("volume-expansion")

    pct_change_1d = ((latest["close"] / prev["close"]) - 1.0) * 100.0 if prev["close"] else 0.0
    return {
        "symbol": symbol,
        "name": name,
        "kind": kind,
        "theme": theme,
        "currency": "HKD",
        "exchange": "HKEX",
        "latest_close": round(latest["close"], 4),
        "prev_close": round(prev["close"], 4),
        "pct_change_1d": round(pct_change_1d, 3),
        "ma20": round(ma20, 4),
        "ma60": round(ma60, 4),
        "range_pos_60": round(range_pos_60, 4),
        "latest_volume": int(latest["volume"]),
        "volume_ratio_20": round(volume_ratio_20, 4) if volume_ratio_20 is not None else None,
        "latest_high": round(latest["high"], 4),
        "latest_low": round(latest["low"], 4),
        "turnover": latest["turnover"],
        "as_of": latest["date"],
        "regime_flags": regime_flags,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill historical daily snapshots for the investment loop.")
    parser.add_argument("--watchlist", default=str(ROOT / "config" / "watchlist.toml"))
    parser.add_argument("--output-dir", default=str(ROOT / "data" / "snapshots"))
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()

    watchlist = read_toml(pathlib.Path(args.watchlist))
    output_dir = pathlib.Path(args.output_dir)
    ensure_dir(output_dir)

    per_symbol: dict[str, dict[str, Any]] = {}
    common_dates: set[str] | None = None

    for entry in watchlist.get("symbols", []):
        symbol = entry["symbol"]
        _quote, kline = fetch_tencent_bundle(symbol)
        series = kline
        date_to_metric = {}
        for index in range(19, len(series)):
            metric = build_historical_metric(symbol, entry.get("name", symbol), entry.get("kind", "unknown"), entry.get("theme", "unknown"), series, index)
            date_to_metric[metric["as_of"]] = metric
        per_symbol[symbol] = date_to_metric
        symbol_dates = set(date_to_metric.keys())
        common_dates = symbol_dates if common_dates is None else common_dates & symbol_dates

    if not common_dates:
        raise SystemExit("No common historical dates available across watchlist")

    selected_dates = sorted(common_dates)[-args.days :]
    for date_str in selected_dates:
        items = [per_symbol[entry["symbol"]][date_str] for entry in watchlist.get("symbols", [])]
        snapshot = {
            "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "as_of_date": date_str,
            "items": items,
            "market_summary": summarize_market(items),
            "failures": [],
            "backfilled": True,
        }
        (output_dir / f"{date_str}.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

    print(f"Backfilled {len(selected_dates)} historical snapshots into {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
