#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import tomllib
from typing import Any

import fetch_investment_data as fetch_data
import rank_investment_universe as ranker


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_POLICY = {
    "min_score": 70.0,
    "min_pct_change_1d": 5.0,
    "min_recent_limit_up_count": 1,
    "recent_window_days": 12,
    "min_catalyst_tags": 2,
    "min_source_count": 2,
    "max_candidates": 10,
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_toml(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def load_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def policy_from_config(config: dict[str, Any]) -> dict[str, Any]:
    policy = DEFAULT_POLICY.copy()
    raw = config.get("policy", {}) if isinstance(config.get("policy"), dict) else {}
    for key, value in raw.items():
        if key in policy:
            policy[key] = value
    policy["min_score"] = float(policy["min_score"])
    policy["min_pct_change_1d"] = float(policy["min_pct_change_1d"])
    policy["min_recent_limit_up_count"] = int(policy["min_recent_limit_up_count"])
    policy["recent_window_days"] = int(policy["recent_window_days"])
    policy["min_catalyst_tags"] = int(policy["min_catalyst_tags"])
    policy["min_source_count"] = int(policy["min_source_count"])
    policy["max_candidates"] = int(policy["max_candidates"])
    return policy


def trade_universe_symbols(path: pathlib.Path | None) -> set[str]:
    return {str(row.get("symbol")) for row in read_toml(path).get("symbols", []) if isinstance(row, dict) and row.get("symbol")}


def configured_candidates(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in config.get("symbols", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows.append(dict(row))
    return rows


def snapshot_items(path: pathlib.Path | None) -> dict[str, dict[str, Any]]:
    payload = load_json(path)
    rows = {}
    for row in payload.get("items", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = dict(row)
    return rows


def recent_limit_up_count_from_kline(kline: list[list[Any]], window_days: int) -> int:
    count = 0
    recent = kline[-max(1, window_days) :]
    for index, row in enumerate(recent):
        source_index = len(kline) - len(recent) + index
        if source_index <= 0:
            continue
        prev_close = as_float(kline[source_index - 1][2], 0.0)
        close = as_float(row[2], 0.0)
        if prev_close > 0 and ((close / prev_close) - 1.0) * 100.0 >= ranker.CN_LIMIT_MOVE_PCT:
            count += 1
    return count


def metrics_for_candidate(candidate: dict[str, Any], snapshot: dict[str, dict[str, Any]], policy: dict[str, Any], live_fetch: bool) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    symbol = str(candidate["symbol"])
    item = snapshot.get(symbol)
    if item is not None:
        enriched = {**candidate, **item}
        enriched.setdefault("recent_limit_up_count", as_int(candidate.get("recent_limit_up_count"), 1 if as_float(enriched.get("pct_change_1d")) >= ranker.CN_LIMIT_MOVE_PCT else 0))
        return enriched, None

    if not live_fetch:
        return None, {"symbol": symbol, "error": "missing_snapshot_row_and_live_fetch_disabled"}

    try:
        quote, kline = fetch_data.fetch_tencent_bundle(symbol)
        item = fetch_data.compute_metrics(symbol, candidate.get("name", symbol), candidate.get("kind", "stock"), candidate.get("theme", "unknown"), quote, kline)
        item["recent_limit_up_count"] = recent_limit_up_count_from_kline(kline, int(policy["recent_window_days"]))
        return {**candidate, **item}, None
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        return None, {"symbol": symbol, "error": str(exc)}


def normalized_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    raw = candidate.get("sources")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, dict)]


def source_count(candidate: dict[str, Any]) -> int:
    if candidate.get("source_count") is not None:
        return as_int(candidate.get("source_count"), 0)
    return len(normalized_sources(candidate))


def trigger_tags(candidate: dict[str, Any]) -> list[str]:
    raw = candidate.get("trigger_tags", candidate.get("discovery_tags", []))
    return [str(item) for item in raw] if isinstance(raw, list) else []


def score_candidate(item: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    scored = ranker.item_score(item, min_watch_score=45.0)
    ranker.apply_edge_cost_fields([scored], round_trip_bps=35.0, minimum_edge_bps=100.0)
    scored["recent_limit_up_count"] = as_int(item.get("recent_limit_up_count"), 0)
    scored["watch_reason"] = item.get("watch_reason")
    scored["trigger_tags"] = trigger_tags(item)
    scored["sources"] = normalized_sources(item)
    scored["source_count"] = source_count(item)
    scored["configured_priority"] = as_int(item.get("priority"), 100)
    return scored


def discovery_reasons(row: dict[str, Any], policy: dict[str, Any], outside_trade_universe: bool) -> list[str]:
    reasons = []
    pct_change = as_float(row.get("pct_change_1d"))
    recent_limit_ups = as_int(row.get("recent_limit_up_count"), 0)
    if outside_trade_universe:
        reasons.append("outside_trade_universe")
    if pct_change >= float(policy["min_pct_change_1d"]):
        reasons.append("major_single_day_move")
    if pct_change >= ranker.CN_LIMIT_MOVE_PCT:
        reasons.append("cn_limit_up_or_near_limit_up")
    if recent_limit_ups >= int(policy["min_recent_limit_up_count"]):
        reasons.append("recent_limit_up_history")
    if as_float(row.get("score")) >= float(policy["min_score"]):
        reasons.append("strong_technical_score")
    if len(row.get("trigger_tags", [])) >= int(policy["min_catalyst_tags"]):
        reasons.append("catalyst_cluster")
    if as_int(row.get("source_count"), 0) >= int(policy["min_source_count"]):
        reasons.append("source_count_confirmed")
    return reasons


def qualifies_for_external_queue(row: dict[str, Any], policy: dict[str, Any], reasons: list[str], outside_trade_universe: bool) -> bool:
    movement = bool({"major_single_day_move", "cn_limit_up_or_near_limit_up", "recent_limit_up_history"} & set(reasons))
    evidence = bool({"strong_technical_score", "catalyst_cluster", "source_count_confirmed"} & set(reasons))
    return outside_trade_universe and movement and evidence


def build_discovery(
    config_path: pathlib.Path,
    trade_universe_path: pathlib.Path,
    as_of_date: str,
    as_of_session: str | None = None,
    snapshot_path: pathlib.Path | None = None,
    live_fetch: bool = True,
) -> dict[str, Any]:
    config = read_toml(config_path)
    policy = policy_from_config(config)
    trade_symbols = trade_universe_symbols(trade_universe_path)
    snapshot = snapshot_items(snapshot_path)
    external_candidates = []
    covered_candidates = []
    rejected_candidates = []
    failures = []

    for candidate in configured_candidates(config):
        item, failure = metrics_for_candidate(candidate, snapshot, policy, live_fetch)
        if failure is not None:
            failures.append(failure)
            continue
        if item is None:
            continue
        row = score_candidate(item, policy)
        outside_trade_universe = str(row["symbol"]) not in trade_symbols
        row["outside_trade_universe"] = outside_trade_universe
        row["discovery_reasons"] = discovery_reasons(row, policy, outside_trade_universe)
        row["recommended_next_step"] = "consider_adding_to_trade_universe" if outside_trade_universe else "already_covered_by_trade_universe"
        if qualifies_for_external_queue(row, policy, row["discovery_reasons"], outside_trade_universe):
            external_candidates.append(row)
        elif not outside_trade_universe:
            covered_candidates.append(row)
        else:
            rejected_candidates.append(row)

    external_candidates = sorted(external_candidates, key=lambda row: (-as_float(row.get("score")), row.get("configured_priority", 100), str(row.get("symbol"))))[: int(policy["max_candidates"])]
    return {
        "generated_at": utc_now(),
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "research_only": True,
        "no_execution": True,
        "policy": policy,
        "summary": {
            "configured_count": len(configured_candidates(config)),
            "external_candidate_count": len(external_candidates),
            "covered_candidate_count": len(covered_candidates),
            "rejected_candidate_count": len(rejected_candidates),
            "failure_count": len(failures),
        },
        "external_candidates": external_candidates,
        "covered_candidates": covered_candidates,
        "rejected_candidates": rejected_candidates,
        "failures": failures,
        "sources": {
            "config": str(config_path),
            "trade_universe": str(trade_universe_path),
            "snapshot": str(snapshot_path) if snapshot_path else None,
        },
    }


def write_markdown(path: pathlib.Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# External Investment Candidate Discovery",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"As-of: `{payload['as_of_date']}` session=`{payload.get('as_of_session')}`",
        f"Research-only: `{payload['research_only']}` no_execution=`{payload['no_execution']}`",
        "",
        "## Summary",
        f"- configured: `{summary['configured_count']}`",
        f"- external_candidates: `{summary['external_candidate_count']}`",
        f"- covered_candidates: `{summary['covered_candidate_count']}`",
        f"- rejected: `{summary['rejected_candidate_count']}` failures=`{summary['failure_count']}`",
        "",
        "## External Candidates",
    ]
    if not payload["external_candidates"]:
        lines.append("- No outside-universe candidates cleared the discovery queue.")
    for row in payload["external_candidates"]:
        lines.append(f"- `{row['symbol']}` {row.get('name')}: score `{row.get('score')}`, pct_1d `{row.get('pct_change_1d')}`, reasons `{', '.join(row.get('discovery_reasons', []))}`")
    lines.append("")
    lines.append("## Covered By Trade Universe")
    if not payload["covered_candidates"]:
        lines.append("- None.")
    for row in payload["covered_candidates"]:
        lines.append(f"- `{row['symbol']}` {row.get('name')}: already in trade universe; reasons `{', '.join(row.get('discovery_reasons', []))}`")
    if payload["failures"]:
        lines.append("")
        lines.append("## Failures")
        for failure in payload["failures"]:
            lines.append(f"- `{failure['symbol']}`: {failure['error']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover strong outside-universe investment candidates for manual review.")
    parser.add_argument("--config", default=str(ROOT / "config" / "external_signal_candidates.toml"))
    parser.add_argument("--trade-universe", default=str(ROOT / "config" / "trade_universe.toml"))
    parser.add_argument("--snapshot", default=None, help="Optional snapshot whose rows can be reused before live fetching missing symbols.")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", default=None)
    parser.add_argument("--no-live-fetch", action="store_true")
    args = parser.parse_args()

    payload = build_discovery(
        pathlib.Path(args.config),
        pathlib.Path(args.trade_universe),
        args.date,
        as_of_session=args.as_of_session,
        snapshot_path=pathlib.Path(args.snapshot) if args.snapshot else None,
        live_fetch=not args.no_live_fetch,
    )
    out_path = pathlib.Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.output_md:
        write_markdown(pathlib.Path(args.output_md), payload)
    print(f"Wrote external candidate discovery: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
