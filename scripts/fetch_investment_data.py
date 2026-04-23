#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import math
import pathlib
import statistics
import sys
import time
import tomllib
import urllib.parse
import urllib.request
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent


def read_toml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def fetch_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("gbk", errors="ignore")


def to_tencent_symbol(symbol: str) -> str:
    if symbol.endswith(".HK"):
        code = symbol.split(".")[0].zfill(5)
        return f"hk{code}"
    return symbol.lower()


def fetch_tencent_bundle(symbol: str) -> tuple[dict[str, Any], list[list[Any]]]:
    tencent_symbol = to_tencent_symbol(symbol)
    quote_text = fetch_text(f"https://qt.gtimg.cn/q={tencent_symbol}")
    parts = quote_text.split("~")
    if len(parts) < 50:
        raise ValueError(f"Unexpected quote payload for {symbol}")

    quote = {
        "name": parts[1],
        "code": parts[2],
        "last": float(parts[3]),
        "prev_close": float(parts[4]),
        "open": float(parts[5]),
        "volume": float(parts[6]),
        "trade_time": parts[30],
        "pct_change": float(parts[32]),
        "high": float(parts[33]),
        "low": float(parts[34]),
        "turnover": float(parts[37]),
        "currency": parts[90] if len(parts) > 90 else "HKD",
    }

    kline = fetch_json(f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param={tencent_symbol},day,,,120,qfq")
    node = kline["data"][tencent_symbol]
    series = node.get("qfqday") or node.get("day") or []
    if not series:
        raise ValueError(f"No kline series for {symbol}")
    return quote, series


def compute_metrics(symbol: str, name: str, kind: str, theme: str, quote: dict[str, Any], kline: list[list[Any]]) -> dict[str, Any]:
    series = []
    for row in kline:
        date_str, open_p, close_p, high_p, low_p, volume = row[:6]
        ts = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc).timestamp()
        series.append((ts, float(close_p), float(volume), float(open_p), float(high_p), float(low_p), date_str))

    if len(series) < 20:
        raise ValueError(f"Not enough price history for {symbol}")

    close_values = [row[1] for row in series]
    volume_values = [row[2] for row in series if row[2] is not None]
    latest_ts, latest_close, latest_volume, _latest_open, latest_high, latest_low, latest_date = series[-1]
    prev_close = quote["prev_close"] or series[-2][1]
    pct_change_1d = ((latest_close / prev_close) - 1.0) * 100.0 if prev_close else 0.0
    ma20 = statistics.fmean(close_values[-20:])
    ma60 = statistics.fmean(close_values[-60:]) if len(close_values) >= 60 else statistics.fmean(close_values)
    high_60 = max(close_values[-60:]) if len(close_values) >= 60 else max(close_values)
    low_60 = min(close_values[-60:]) if len(close_values) >= 60 else min(close_values)
    range_pos_60 = 0.5 if math.isclose(high_60, low_60) else (latest_close - low_60) / (high_60 - low_60)
    avg_volume_20 = statistics.fmean(volume_values[-20:]) if len(volume_values) >= 20 else statistics.fmean(volume_values or [0])
    volume_ratio_20 = (latest_volume / avg_volume_20) if latest_volume and avg_volume_20 else None

    regime_flags = []
    if latest_close > ma20 > ma60:
        regime_flags.append("uptrend")
    elif latest_close < ma20 < ma60:
        regime_flags.append("downtrend")
    else:
        regime_flags.append("range")
    if volume_ratio_20 and volume_ratio_20 > 1.5:
        regime_flags.append("volume-expansion")

    return {
        "symbol": symbol,
        "name": name or quote["name"],
        "kind": kind,
        "theme": theme,
        "currency": quote.get("currency", "HKD"),
        "exchange": "HKEX",
        "latest_close": round(latest_close, 4),
        "prev_close": round(prev_close, 4),
        "pct_change_1d": round(pct_change_1d, 3),
        "ma20": round(ma20, 4),
        "ma60": round(ma60, 4),
        "range_pos_60": round(range_pos_60, 4),
        "latest_volume": int(latest_volume),
        "volume_ratio_20": round(volume_ratio_20, 4) if volume_ratio_20 is not None else None,
        "latest_high": round(latest_high, 4),
        "latest_low": round(latest_low, 4),
        "turnover": quote.get("turnover"),
        "as_of": latest_date,
        "regime_flags": regime_flags,
    }


def summarize_market(items: list[dict[str, Any]]) -> dict[str, Any]:
    etfs = [item for item in items if item["kind"] == "etf"]
    stocks = [item for item in items if item["kind"] == "stock"]
    avg_stock_move = statistics.fmean([item["pct_change_1d"] for item in stocks]) if stocks else 0.0
    avg_etf_move = statistics.fmean([item["pct_change_1d"] for item in etfs]) if etfs else 0.0
    risk_state = "neutral"
    if avg_etf_move > 0.75 and avg_stock_move > 0:
        risk_state = "risk_on"
    elif avg_etf_move < -0.75 and avg_stock_move < 0:
        risk_state = "risk_off"

    return {
        "risk_state": risk_state,
        "avg_stock_move_1d": round(avg_stock_move, 3),
        "avg_etf_move_1d": round(avg_etf_move, 3),
        "leaders": sorted(items, key=lambda item: item["pct_change_1d"], reverse=True)[:3],
        "laggards": sorted(items, key=lambda item: item["pct_change_1d"])[:3],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch investment snapshot data for configured symbols.")
    parser.add_argument("--watchlist", default=str(ROOT / "config" / "watchlist.toml"))
    parser.add_argument("--output-dir", default=str(ROOT / "data" / "snapshots"))
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()

    watchlist = read_toml(pathlib.Path(args.watchlist))
    output_dir = pathlib.Path(args.output_dir)
    ensure_dir(output_dir)

    items = []
    failures = []
    for entry in watchlist.get("symbols", []):
        symbol = entry["symbol"]
        try:
            quote, kline = fetch_tencent_bundle(symbol)
            items.append(compute_metrics(symbol, entry.get("name", symbol), entry.get("kind", "unknown"), entry.get("theme", "unknown"), quote, kline))
            time.sleep(0.2)
        except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
            failures.append({"symbol": symbol, "error": str(exc)})

    snapshot = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "as_of_date": args.date,
        "items": items,
        "market_summary": summarize_market(items) if items else {},
        "failures": failures,
    }

    out_file = output_dir / f"{args.date}.json"
    out_file.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

    print(f"Wrote snapshot: {out_file}")
    if failures:
        print(f"Warnings: {len(failures)} symbols failed", file=sys.stderr)
    return 0 if items else 1


if __name__ == "__main__":
    raise SystemExit(main())
