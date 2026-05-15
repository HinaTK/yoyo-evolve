#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import tomllib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_POLICY = {
    "require_for_action": True,
    "max_staleness_days": 30,
    "min_total_score_for_action": 0.55,
    "block_unknown_event_risk": True,
}
DEFAULT_WEIGHTS = {
    "fundamental_score": 0.30,
    "valuation_score": 0.20,
    "catalyst_score": 0.25,
    "flow_score": 0.15,
    "macro_score": 0.10,
}
COMPONENT_KEYS = tuple(DEFAULT_WEIGHTS.keys())


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


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def parse_policy(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, float]]:
    policy = DEFAULT_POLICY.copy()
    policy.update(config.get("policy", {}) if isinstance(config.get("policy"), dict) else {})
    weights = DEFAULT_WEIGHTS.copy()
    raw_weights = config.get("weights", {}) if isinstance(config.get("weights"), dict) else {}
    for key, value in raw_weights.items():
        if key in weights:
            weights[key] = float(value)
    return policy, weights


def configured_symbols(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in config.get("evidence", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = row
    return rows


def universe_symbols(universe: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in universe.get("symbols", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = row
    return rows


def snapshot_symbols(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in snapshot.get("items", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = row
    return rows


def ranking_symbols(ranking: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for key in ("top_candidates", "actionable_candidates", "diagnostic_candidates", "all_ranked"):
        for row in ranking.get(key, []):
            if isinstance(row, dict) and row.get("symbol") and str(row["symbol"]) not in rows:
                rows[str(row["symbol"])] = row
    return rows


def date_token(value: Any) -> str | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return None


def parse_date(value: Any) -> dt.date | None:
    token = date_token(value)
    if token is None:
        return None
    try:
        return dt.date.fromisoformat(token)
    except ValueError:
        return None


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def total_score(row: dict[str, Any], weights: dict[str, float]) -> float | None:
    score_sum = 0.0
    weight_sum = 0.0
    for key, weight in weights.items():
        value = as_float(row.get(key))
        if value is None:
            continue
        score_sum += max(0.0, min(1.0, value)) * float(weight)
        weight_sum += float(weight)
    return round(score_sum / weight_sum, 3) if weight_sum else None


def normalize_sources(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    sources = []
    for item in raw:
        if isinstance(item, dict):
            sources.append(dict(item))
        elif item:
            sources.append({"label": str(item)})
    return sources


def build_symbol_evidence(
    symbol: str,
    metadata: dict[str, Any],
    configured: dict[str, Any] | None,
    as_of_date: str,
    as_of_session: str | None,
    policy: dict[str, Any],
    weights: dict[str, float],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    configured = configured or {}
    sources = normalize_sources(configured.get("sources"))
    source_count = int(configured.get("source_count") or len(sources) or 0)
    raw_as_of = configured.get("as_of_date")
    evidence_date = parse_date(raw_as_of)
    report_date = parse_date(as_of_date)
    row: dict[str, Any] = {
        "symbol": symbol,
        "name": metadata.get("name"),
        "kind": metadata.get("kind"),
        "theme": metadata.get("theme"),
        "as_of_date": date_token(raw_as_of),
        "as_of_session": configured.get("as_of_session") or as_of_session,
        "event_risk": str(configured.get("event_risk") or "unknown").lower(),
        "source_count": source_count,
        "sources": sources,
        "notes": configured.get("notes", []) if isinstance(configured.get("notes", []), list) else [],
        "evidence_mode": "curated_point_in_time" if configured else "missing_fail_closed",
    }
    for key in COMPONENT_KEYS:
        row[key] = as_float(configured.get(key))
    row["total_score"] = total_score(row, weights)

    missing_components = [key for key in COMPONENT_KEYS if row.get(key) is None]
    if not configured:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_evidence_missing"})
    if evidence_date is None:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_evidence_date_missing"})
    elif report_date is not None:
        age_days = (report_date - evidence_date).days
        row["age_days"] = age_days
        if age_days < 0:
            findings.append({"symbol": symbol, "severity": "critical", "reason": "nontechnical_evidence_from_future"})
        elif age_days > int(policy.get("max_staleness_days", 30)):
            findings.append({"symbol": symbol, "severity": "info", "reason": "nontechnical_evidence_stale", "age_days": age_days})
    if missing_components:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_component_missing", "components": missing_components})
    if row["total_score"] is None:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_score_missing"})
    elif row["total_score"] < float(policy.get("min_total_score_for_action", 0.55)):
        findings.append({"symbol": symbol, "severity": "info", "reason": "nontechnical_score_below_action_min", "total_score": row["total_score"]})
    if row["event_risk"] == "unknown" and policy.get("block_unknown_event_risk", True):
        findings.append({"symbol": symbol, "severity": "warning", "reason": "event_risk_unknown"})
    if source_count <= 0:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_source_missing"})
    return row, findings


def build_evidence(
    config_path: pathlib.Path,
    as_of_date: str,
    trade_universe_path: pathlib.Path | None = None,
    snapshot_path: pathlib.Path | None = None,
    ranking_path: pathlib.Path | None = None,
    as_of_session: str | None = None,
) -> dict[str, Any]:
    config = read_toml(config_path)
    policy, weights = parse_policy(config)
    configured = configured_symbols(config)
    universe = universe_symbols(read_toml(trade_universe_path))
    snapshot = snapshot_symbols(load_json(snapshot_path))
    ranking = ranking_symbols(load_json(ranking_path))
    symbols: dict[str, dict[str, Any]] = {}
    for source in (universe, snapshot, ranking, {symbol: {"symbol": symbol} for symbol in configured}):
        for symbol, row in source.items():
            symbols.setdefault(symbol, {}).update(row)

    rows: dict[str, dict[str, Any]] = {}
    findings: list[dict[str, Any]] = []
    for symbol in sorted(symbols):
        row, row_findings = build_symbol_evidence(symbol, symbols[symbol], configured.get(symbol), as_of_date, as_of_session, policy, weights)
        rows[symbol] = row
        findings.extend(row_findings)

    missing_count = sum(1 for row in rows.values() if row.get("evidence_mode") == "missing_fail_closed")
    available_count = len(rows) - missing_count
    return {
        "generated_at": utc_now(),
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "research_only": True,
        "no_execution": True,
        "evidence_mode": "point_in_time_curated_or_missing_fail_closed",
        "policy": policy,
        "weights": weights,
        "summary": {
            "symbol_count": len(rows),
            "available_count": available_count,
            "missing_count": missing_count,
            "coverage_ratio": round(available_count / len(rows), 3) if rows else None,
            "actionable_evidence_count": sum(
                1
                for row in rows.values()
                if row.get("total_score") is not None
                and row.get("total_score") >= float(policy.get("min_total_score_for_action", 0.55))
                and row.get("source_count", 0) > 0
                and row.get("event_risk") not in {"unknown", "regulatory", "policy", "suspension", "accounting", "elevated", "earnings_gap"}
            ),
            "finding_count": len(findings),
            "critical_finding_count": sum(1 for finding in findings if finding.get("severity") == "critical"),
            "blocking_finding_count": sum(1 for finding in findings if finding.get("severity") in {"critical", "warning"}),
        },
        "symbols": rows,
        "findings": findings,
        "sources": {
            "config": str(config_path),
            "trade_universe": str(trade_universe_path) if trade_universe_path else None,
            "snapshot": str(snapshot_path) if snapshot_path else None,
            "ranking": str(ranking_path) if ranking_path else None,
        },
    }


def write_markdown(path: pathlib.Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# Nontechnical Evidence Ledger",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"As-of: `{payload['as_of_date']}`",
        f"Research only: `{payload['research_only']}`; no execution: `{payload['no_execution']}`",
        "",
        "## Summary",
        f"- symbols: `{summary['symbol_count']}`",
        f"- available: `{summary['available_count']}`",
        f"- missing: `{summary['missing_count']}`",
        f"- coverage_ratio: `{summary['coverage_ratio']}`",
        f"- actionable_evidence_count: `{summary['actionable_evidence_count']}`",
        f"- findings: `{summary['finding_count']}` critical=`{summary['critical_finding_count']}`",
        "",
        "## Findings",
    ]
    for finding in payload.get("findings", [])[:20]:
        lines.append(f"- `{finding.get('symbol')}` {finding.get('reason')} severity={finding.get('severity')}")
    if not payload.get("findings"):
        lines.append("- No evidence integrity findings.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build point-in-time nontechnical evidence used as an action gate.")
    parser.add_argument("--config", default=str(ROOT / "config" / "nontechnical_evidence.toml"))
    parser.add_argument("--trade-universe", default=str(ROOT / "config" / "trade_universe.toml"))
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--ranking", default=None)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--output-json", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.md"))
    args = parser.parse_args()

    payload = build_evidence(
        resolve_path(args.config) or pathlib.Path(args.config),
        args.as_of_date,
        resolve_path(args.trade_universe),
        resolve_path(args.snapshot),
        resolve_path(args.ranking),
        args.as_of_session,
    )
    output_json = resolve_path(args.output_json) or pathlib.Path(args.output_json)
    output_md = resolve_path(args.output_md) or pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(output_md, payload)
    print(f"Wrote nontechnical evidence: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
