#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from evaluate_investment_shadow import build_evaluation, load_shadow_logs, shadow_candidates  # noqa: E402


FORWARD_MODE = "forward_shadow"
REPLAY_MODE = "historical_replay"
VALID_EVIDENCE_MODES = {FORWARD_MODE, REPLAY_MODE}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalized_path(path_text: str | pathlib.Path | None) -> str:
    if not path_text:
        return ""
    return str(pathlib.Path(path_text).resolve())


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_date(value: Any) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def audit_finding(path: pathlib.Path, severity: str, field: str, message: str) -> dict[str, Any]:
    return {"path": str(path), "severity": severity, "field": field, "message": message}


def source_artifact_ok(source: dict[str, Any], key: str) -> bool:
    artifact = source.get(key)
    return isinstance(artifact, dict) and artifact.get("exists") is True and bool(artifact.get("sha256"))


def source_as_of_date(source: dict[str, Any]) -> dt.date | None:
    value = source.get("as_of_date")
    return parse_date(value) if value else None


def audit_log(path: pathlib.Path, log: dict[str, Any]) -> list[dict[str, Any]]:
    findings = []
    evidence_mode = log.get("evidence_mode")
    counts_forward = log.get("counts_toward_forward_evidence") is True
    policy = log.get("shadow_policy") if isinstance(log.get("shadow_policy"), dict) else {}
    source = log.get("source") if isinstance(log.get("source"), dict) else {}

    for field in ["date", "session", "generated_at", "mode", "evidence_mode"]:
        if not log.get(field):
            findings.append(audit_finding(path, "critical", field, "missing required audit field"))
    if log.get("mode") != "shadow_logging":
        findings.append(audit_finding(path, "critical", "mode", "ledger only accepts shadow_logging records"))
    if evidence_mode not in VALID_EVIDENCE_MODES:
        findings.append(audit_finding(path, "critical", "evidence_mode", "unknown evidence mode"))
    if evidence_mode == REPLAY_MODE and counts_forward:
        findings.append(audit_finding(path, "critical", "counts_toward_forward_evidence", "historical replay must not count as forward evidence"))

    if evidence_mode == FORWARD_MODE:
        if str(log.get("session") or "") == "historical":
            findings.append(audit_finding(path, "critical", "session", "historical sessions cannot be forward evidence"))
        if not counts_forward:
            findings.append(audit_finding(path, "critical", "counts_toward_forward_evidence", "forward shadow logs must count toward forward evidence"))
        for field in ["no_execution", "no_portfolio_mutation", "production_ranking_unchanged"]:
            if policy.get(field) is not True:
                findings.append(audit_finding(path, "critical", f"shadow_policy.{field}", "forward shadow must preserve research-only safety policy"))
        for key in ["ranking", "snapshot"]:
            if not source_artifact_ok(source, key):
                findings.append(audit_finding(path, "critical", f"source.{key}", "forward shadow must retain existing source artifact hash"))
        log_date = parse_date(log.get("date"))
        as_of = source_as_of_date(source)
        if log_date is not None and as_of is not None and as_of != log_date:
            findings.append(audit_finding(path, "critical", "source.as_of_date", "source as_of_date must match forward shadow log date"))

    return findings


def index_outcomes(evaluation: dict[str, Any]) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    records = {}
    pending = {}
    for record in evaluation.get("records", []):
        key = (normalized_path(record.get("shadow_log")), str(record.get("symbol") or ""))
        records[key] = record
    for item in evaluation.get("pending_records", []):
        key = (normalized_path(item.get("shadow_log")), str(item.get("symbol") or ""))
        pending[key] = item
    return records, pending


def candidate_entry(path: pathlib.Path, log: dict[str, Any], candidate: dict[str, Any], records: dict[tuple[str, str], dict[str, Any]], pending: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any]:
    symbol = str(candidate.get("symbol") or "")
    key = (normalized_path(path), symbol)
    outcome = records.get(key)
    pending_outcome = pending.get(key)
    if outcome:
        status = "matured"
    elif pending_outcome:
        status = "pending"
    elif log.get("evidence_mode") != FORWARD_MODE or log.get("counts_toward_forward_evidence") is not True:
        status = "not_forward_evidence"
    else:
        status = "unmatched"

    return {
        "ledger_key": f"{log.get('date')}|{log.get('session')}|{symbol}",
        "shadow_log": str(path),
        "date": log.get("date"),
        "session": log.get("session"),
        "evidence_mode": log.get("evidence_mode"),
        "counts_toward_forward_evidence": log.get("counts_toward_forward_evidence") is True,
        "symbol": symbol,
        "market_family": candidate.get("market_family"),
        "theme": candidate.get("theme"),
        "score": candidate.get("score"),
        "confidence_proxy": round(float(candidate["score"]) / 100.0, 3) if as_float(candidate.get("score")) is not None else None,
        "latest_close": candidate.get("latest_close"),
        "planned_horizon_days": candidate.get("planned_horizon_days"),
        "stop_loss_pct": candidate.get("stop_loss_pct"),
        "benchmark_symbol": candidate.get("benchmark_symbol"),
        "source_layer": candidate.get("source_layer"),
        "outcome_status": status,
        "outcome": outcome,
        "pending": pending_outcome,
    }


def log_entry(path: pathlib.Path, log: dict[str, Any], findings: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = shadow_candidates(log)
    policy = log.get("shadow_policy") if isinstance(log.get("shadow_policy"), dict) else {}
    source = log.get("source") if isinstance(log.get("source"), dict) else {}
    return {
        "path": str(path),
        "date": log.get("date"),
        "session": log.get("session"),
        "generated_at": log.get("generated_at"),
        "evidence_mode": log.get("evidence_mode"),
        "counts_toward_forward_evidence": log.get("counts_toward_forward_evidence") is True,
        "candidate_count": len(candidates),
        "status": "no_action" if not candidates else "has_candidates",
        "shadow_policy": policy,
        "source": source,
        "audit_findings": findings,
    }


def build_ledger(
    shadow_dir: pathlib.Path,
    registry_path: pathlib.Path,
    include_replay: bool = False,
    round_trip_bps: float = 35.0,
    max_adverse_limit_pct: float = -8.0,
    min_forward_shadow_days: int = 20,
    as_of_date: dt.date | None = None,
) -> dict[str, Any]:
    evaluation = build_evaluation(shadow_dir, registry_path, include_replay, round_trip_bps, max_adverse_limit_pct, min_forward_shadow_days, as_of_date)
    records, pending = index_outcomes(evaluation)
    logs = load_shadow_logs(shadow_dir)

    log_entries = []
    candidate_entries = []
    all_findings = []
    forward_log_count = 0
    replay_log_count = 0
    no_action_count = 0

    for path, log in logs:
        findings = audit_log(path, log)
        all_findings.extend(findings)
        log_entries.append(log_entry(path, log, findings))
        candidates = shadow_candidates(log)
        if log.get("evidence_mode") == FORWARD_MODE and log.get("counts_toward_forward_evidence") is True:
            forward_log_count += 1
        if log.get("evidence_mode") == REPLAY_MODE:
            replay_log_count += 1
        if not candidates:
            no_action_count += 1
        for candidate in candidates:
            if include_replay or (log.get("evidence_mode") == FORWARD_MODE and log.get("counts_toward_forward_evidence") is True):
                candidate_entries.append(candidate_entry(path, log, candidate, records, pending))

    critical_count = sum(1 for finding in all_findings if finding.get("severity") == "critical")
    matured_count = sum(1 for entry in candidate_entries if entry["outcome_status"] == "matured")
    pending_count = sum(1 for entry in candidate_entries if entry["outcome_status"] == "pending")
    unmatched_count = sum(1 for entry in candidate_entries if entry["outcome_status"] == "unmatched")

    return {
        "generated_at": utc_now(),
        "shadow_dir": str(shadow_dir),
        "registry": str(registry_path),
        "include_replay": include_replay,
        "as_of_date": as_of_date.isoformat() if as_of_date else None,
        "audit_passed": critical_count == 0,
        "summary": {
            "shadow_log_count": len(log_entries),
            "forward_shadow_log_count": forward_log_count,
            "historical_replay_log_count": replay_log_count,
            "no_action_log_count": no_action_count,
            "candidate_entry_count": len(candidate_entries),
            "matured_candidate_count": matured_count,
            "pending_candidate_count": pending_count,
            "unmatched_candidate_count": unmatched_count,
            "audit_finding_count": len(all_findings),
            "critical_audit_finding_count": critical_count,
        },
        "shadow_evaluation_summary": evaluation.get("summary", {}),
        "shadow_evaluation_gate": evaluation.get("gate", {}),
        "audit_findings": all_findings,
        "logs": log_entries,
        "candidate_entries": candidate_entries,
    }


def write_markdown(path: pathlib.Path, ledger: dict[str, Any]) -> None:
    summary = ledger["summary"]
    lines = [
        "# Forward Evidence Ledger",
        "",
        f"Generated: `{ledger['generated_at']}`",
        f"Audit passed: `{ledger['audit_passed']}`",
        f"Includes replay: `{ledger['include_replay']}`",
        "",
        "## Summary",
        f"- shadow logs: `{summary['shadow_log_count']}`",
        f"- forward shadow logs: `{summary['forward_shadow_log_count']}`",
        f"- historical replay logs: `{summary['historical_replay_log_count']}`",
        f"- no-action logs: `{summary['no_action_log_count']}`",
        f"- candidate entries: `{summary['candidate_entry_count']}`",
        f"- matured candidates: `{summary['matured_candidate_count']}`",
        f"- pending candidates: `{summary['pending_candidate_count']}`",
        f"- critical audit findings: `{summary['critical_audit_finding_count']}`",
        "",
        "## Audit Findings",
    ]
    if ledger["audit_findings"]:
        for finding in ledger["audit_findings"][:50]:
            lines.append(f"- `{finding['severity']}` `{finding['field']}` in `{finding['path']}`: {finding['message']}")
    else:
        lines.append("- no audit findings")

    lines.extend(["", "## Recent Forward Logs"])
    forward_logs = [entry for entry in ledger["logs"] if entry.get("counts_toward_forward_evidence")]
    for entry in forward_logs[-10:]:
        lines.append(f"- `{entry['date']}` `{entry['session']}` candidates={entry['candidate_count']} status=`{entry['status']}` path=`{entry['path']}`")
    if not forward_logs:
        lines.append("- no forward logs yet")

    lines.extend(["", "## Recent Candidate Entries"])
    for entry in ledger["candidate_entries"][-15:]:
        outcome = entry.get("outcome") or {}
        lines.append(
            f"- `{entry['date']}` `{entry['symbol']}` status=`{entry['outcome_status']}` "
            f"score={entry.get('score')} net={outcome.get('net_return_pct')} alpha={outcome.get('alpha_pct')} adverse={outcome.get('max_adverse_pct')}"
        )
    if not ledger["candidate_entries"]:
        lines.append("- no candidate entries yet")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an auditable forward evidence ledger from shadow investment logs.")
    parser.add_argument("--shadow-dir", default=str(ROOT / "research" / "shadow"))
    parser.add_argument("--registry", default=str(ROOT / "data" / "snapshots" / "registry.json"))
    parser.add_argument("--output-json", default=str(ROOT / "research" / "shadow" / "latest_evidence_ledger.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "shadow" / "latest_evidence_ledger.md"))
    parser.add_argument("--include-replay", action="store_true")
    parser.add_argument("--round-trip-bps", type=float, default=35.0)
    parser.add_argument("--max-adverse-limit-pct", type=float, default=-8.0)
    parser.add_argument("--min-forward-shadow-days", type=int, default=20)
    parser.add_argument("--as-of-date", default=None)
    args = parser.parse_args()

    ledger = build_ledger(
        pathlib.Path(args.shadow_dir),
        pathlib.Path(args.registry),
        args.include_replay,
        args.round_trip_bps,
        args.max_adverse_limit_pct,
        args.min_forward_shadow_days,
        parse_date(args.as_of_date) if args.as_of_date else None,
    )
    output_json = pathlib.Path(args.output_json)
    output_md = pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    write_markdown(output_md, ledger)
    print(json.dumps(ledger["summary"], indent=2))
    return 0 if ledger["audit_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
