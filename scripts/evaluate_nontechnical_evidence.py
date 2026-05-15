#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import statistics
import sys
from collections import defaultdict
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from build_nontechnical_evidence import COMPONENT_KEYS, parse_date  # noqa: E402
from evaluate_investment_calls import evaluate_calls  # noqa: E402
from evaluate_investment_shadow import build_evaluation  # noqa: E402


EVENT_RISK_HARD = {"elevated", "earnings_gap", "regulatory", "policy", "suspension", "accounting"}
SESSION_ORDER = {"morning": 0, "midday": 1, "close": 2, "historical": 2}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def success_for_call(record: dict[str, Any]) -> float | None:
    verdict = record.get("verdict")
    if verdict == "pass":
        return 1.0
    if verdict == "fail":
        return 0.0
    if verdict == "mixed":
        return 0.5
    return None


def success_for_shadow(record: dict[str, Any]) -> float | None:
    net_return = as_float(record.get("net_return_pct"))
    if record.get("adverse_breach") is True:
        return 0.0
    if net_return is None:
        return None
    if net_return > 0:
        return 1.0
    if net_return < 0:
        return 0.0
    return 0.5


def bucket_for_score(value: float | None) -> str:
    if value is None:
        return "missing"
    if value < 0.4:
        return "0.00-0.40"
    if value < 0.55:
        return "0.40-0.55"
    if value < 0.7:
        return "0.55-0.70"
    if value < 0.85:
        return "0.70-0.85"
    return "0.85-1.00"


def evidence_for_symbol(evidence: dict[str, Any], symbol: str, outcome_date: dt.date | None, outcome_session: str | None = None) -> dict[str, Any] | None:
    symbols = evidence.get("symbols", {}) if isinstance(evidence.get("symbols"), dict) else {}
    row = symbols.get(symbol)
    if not isinstance(row, dict):
        return None
    evidence_date = parse_date(row.get("as_of_date")) or parse_date(evidence.get("as_of_date"))
    if outcome_date is not None and evidence_date is not None and evidence_date > outcome_date:
        return None
    evidence_session = str(row.get("as_of_session") or evidence.get("as_of_session") or "").lower() or None
    outcome_session = str(outcome_session or "").lower() or None
    if outcome_date is not None and evidence_date == outcome_date and evidence_session and outcome_session:
        if SESSION_ORDER.get(evidence_session, 99) > SESSION_ORDER.get(outcome_session, 99):
            return None
    return row


def outcome_rows(
    calls_dir: pathlib.Path,
    snapshot_dir: pathlib.Path,
    shadow_dir: pathlib.Path,
    registry_path: pathlib.Path,
    as_of_date: dt.date | None,
    as_of_session: str | None,
) -> list[dict[str, Any]]:
    calls, _summary = evaluate_calls(calls_dir, snapshot_dir, [3, 5, 10, 20], [0, 1, 3], as_of_date, as_of_session)
    rows = []
    for record in calls:
        rows.append(
            {
                "source": "calls",
                "date": record.get("call_date"),
                "session": record.get("session"),
                "symbol": record.get("symbol"),
                "theme": record.get("theme"),
                "return_pct": as_float(record.get("return_pct")),
                "success": success_for_call(record),
                "verdict": record.get("verdict"),
            }
        )
    if registry_path.exists():
        shadow = build_evaluation(shadow_dir, registry_path, include_replay=False, as_of_date=as_of_date)
        for record in shadow.get("records", []):
            if record.get("counts_toward_forward_evidence") is not True:
                continue
            rows.append(
                {
                    "source": "shadow",
                    "date": record.get("base_date"),
                    "session": record.get("session") or "shadow",
                    "symbol": record.get("symbol"),
                    "theme": record.get("theme"),
                    "return_pct": as_float(record.get("net_return_pct")),
                    "success": success_for_shadow(record),
                    "verdict": "pass" if success_for_shadow(record) == 1.0 else "fail" if success_for_shadow(record) == 0.0 else "mixed",
                }
            )
    return rows


def stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [row for row in rows if row.get("success") is not None]
    returns = [row["return_pct"] for row in rows if row.get("return_pct") is not None]
    successes = [row["success"] for row in scored]
    return {
        "sample_count": len(rows),
        "scored_sample_count": len(scored),
        "hit_rate": round(statistics.fmean(successes), 3) if successes else None,
        "avg_return_pct": round(statistics.fmean(returns), 3) if returns else None,
        "median_return_pct": round(statistics.median(returns), 3) if returns else None,
    }


def grouped_stats(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key) or "missing")].append(row)
    return [{key: group, **stats(items)} for group, items in sorted(grouped.items())]


def attach_evidence(outcomes: list[dict[str, Any]], evidence: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    skipped = []
    for outcome in outcomes:
        symbol = str(outcome.get("symbol") or "")
        outcome_date = parse_date(outcome.get("date"))
        row = evidence_for_symbol(evidence, symbol, outcome_date, outcome.get("session"))
        if row is None:
            skipped.append({"symbol": symbol, "date": outcome.get("date"), "reason": "no_point_in_time_evidence"})
            continue
        total_score = as_float(row.get("total_score"))
        enriched = {
            **outcome,
            "nontechnical_total_score": total_score,
            "score_bucket": bucket_for_score(total_score),
            "event_risk": str(row.get("event_risk") or "unknown").lower(),
            "event_risk_bucket": "hard" if str(row.get("event_risk") or "unknown").lower() in EVENT_RISK_HARD else str(row.get("event_risk") or "unknown").lower(),
            "source_count": int(row.get("source_count") or 0),
        }
        for key in COMPONENT_KEYS:
            value = as_float(row.get(key))
            enriched[key] = value
            enriched[f"{key}_bucket"] = bucket_for_score(value)
        rows.append(enriched)
    return rows, skipped


def build_attribution(
    evidence_path: pathlib.Path,
    calls_dir: pathlib.Path,
    snapshot_dir: pathlib.Path,
    shadow_dir: pathlib.Path,
    registry_path: pathlib.Path,
    as_of_date: dt.date | None = None,
    as_of_session: str | None = None,
    min_bucket_samples: int = 5,
) -> dict[str, Any]:
    evidence = load_json(evidence_path)
    outcomes = outcome_rows(calls_dir, snapshot_dir, shadow_dir, registry_path, as_of_date, as_of_session)
    rows, skipped = attach_evidence(outcomes, evidence)
    bucket_sections = {"total_score": grouped_stats(rows, "score_bucket"), "event_risk": grouped_stats(rows, "event_risk_bucket")}
    for key in COMPONENT_KEYS:
        bucket_sections[key] = grouped_stats(rows, f"{key}_bucket")
    findings = []
    if len(rows) < min_bucket_samples:
        findings.append({"metric": "scored_attribution_rows", "actual": len(rows), "expected": f">= {min_bucket_samples}", "severity": "info"})
    for name, buckets in bucket_sections.items():
        for bucket in buckets:
            if 0 < bucket.get("scored_sample_count", 0) < min_bucket_samples:
                findings.append({"metric": f"bucket:{name}:{bucket.get(name) or bucket.get(name + '_bucket')}", "actual": bucket.get("scored_sample_count"), "expected": f">= {min_bucket_samples}", "severity": "info"})
    return {
        "generated_at": utc_now(),
        "as_of_date": as_of_date.isoformat() if as_of_date else None,
        "as_of_session": as_of_session,
        "research_only": True,
        "no_execution": True,
        "evidence_mode": "point_in_time_forward_attribution",
        "inputs": {
            "nontechnical_evidence": str(evidence_path),
            "calls_dir": str(calls_dir),
            "snapshot_dir": str(snapshot_dir),
            "shadow_dir": str(shadow_dir),
            "registry": str(registry_path),
        },
        "summary": {
            "outcome_count": len(outcomes),
            "attributed_sample_count": len(rows),
            "skipped_without_point_in_time_evidence": len(skipped),
            **stats(rows),
        },
        "buckets": bucket_sections,
        "records": rows,
        "skipped_records": skipped,
        "findings": findings,
    }


def write_markdown(path: pathlib.Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# Nontechnical Evidence Attribution",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"As-of: date=`{payload.get('as_of_date') or 'null'}`, session=`{payload.get('as_of_session') or 'null'}`",
        f"Research only: `{payload['research_only']}`; no execution: `{payload['no_execution']}`",
        "",
        "## Summary",
        f"- outcomes: `{summary['outcome_count']}`",
        f"- attributed samples: `{summary['attributed_sample_count']}`",
        f"- skipped without point-in-time evidence: `{summary['skipped_without_point_in_time_evidence']}`",
        f"- hit_rate: `{summary['hit_rate']}`",
        f"- avg_return_pct: `{summary['avg_return_pct']}`",
        "",
        "## Total Score Buckets",
    ]
    for row in payload["buckets"].get("total_score", []):
        lines.append(f"- `{row.get('score_bucket')}` samples={row.get('scored_sample_count')} hit_rate={row.get('hit_rate')} avg_return={row.get('avg_return_pct')}")
    lines.extend(["", "## Findings"])
    for finding in payload.get("findings", [])[:20]:
        lines.append(f"- `{finding.get('metric')}` actual={finding.get('actual')} expected={finding.get('expected')}")
    if not payload.get("findings"):
        lines.append("- No attribution findings.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate posterior attribution of nontechnical evidence fields.")
    parser.add_argument("--nontechnical-evidence", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.json"))
    parser.add_argument("--calls-dir", default=str(ROOT / "research" / "calls"))
    parser.add_argument("--snapshot-dir", default=str(ROOT / "data" / "snapshots"))
    parser.add_argument("--shadow-dir", default=str(ROOT / "research" / "shadow"))
    parser.add_argument("--registry", default=str(ROOT / "data" / "snapshots" / "registry.json"))
    parser.add_argument("--as-of-date", default=None)
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--min-bucket-samples", type=int, default=5)
    parser.add_argument("--output-json", default=str(ROOT / "research" / "evaluations" / "latest_nontechnical_attribution.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "evaluations" / "latest_nontechnical_attribution.md"))
    args = parser.parse_args()

    payload = build_attribution(
        resolve_path(args.nontechnical_evidence) or pathlib.Path(args.nontechnical_evidence),
        resolve_path(args.calls_dir) or pathlib.Path(args.calls_dir),
        resolve_path(args.snapshot_dir) or pathlib.Path(args.snapshot_dir),
        resolve_path(args.shadow_dir) or pathlib.Path(args.shadow_dir),
        resolve_path(args.registry) or pathlib.Path(args.registry),
        dt.date.fromisoformat(args.as_of_date) if args.as_of_date else None,
        args.as_of_session,
        args.min_bucket_samples,
    )
    output_json = resolve_path(args.output_json) or pathlib.Path(args.output_json)
    output_md = resolve_path(args.output_md) or pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(output_md, payload)
    print(f"Wrote nontechnical attribution: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
