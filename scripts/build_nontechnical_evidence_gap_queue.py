#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "research" / "evidence" / "nontechnical"
COMPONENT_KEYS = (
    "fundamental_score",
    "valuation_score",
    "catalyst_score",
    "flow_score",
    "macro_score",
)
DEFAULT_WEIGHTS = {
    "fundamental_score": 0.30,
    "valuation_score": 0.20,
    "catalyst_score": 0.25,
    "flow_score": 0.15,
    "macro_score": 0.10,
}
DEFAULT_POLICY = {
    "max_staleness_days": 30,
    "min_total_score_for_action": 0.55,
    "block_unknown_event_risk": True,
}
DEFAULT_COMPONENT_MAX_STALENESS_DAYS = {
    "fundamental_score": 120,
    "valuation_score": 45,
    "catalyst_score": 30,
    "flow_score": 5,
    "macro_score": 14,
    "event_risk": 7,
}
SESSION_ORDER = {"morning": 0, "midday": 1, "close": 2, "historical": 2}
HARD_EVENT_RISKS = {"elevated", "earnings_gap", "regulatory", "policy", "suspension", "accounting", "quote_stale"}
DIRECT_GAP_REASONS = {
    "nontechnical_proxy_only",
    "nontechnical_source_missing",
    "event_risk_unknown",
    "nontechnical_evidence_missing",
    "nontechnical_evidence_date_missing",
    "nontechnical_evidence_from_future",
    "nontechnical_evidence_from_future_session",
    "nontechnical_evidence_stale",
    "nontechnical_component_missing",
    "nontechnical_score_missing",
    "nontechnical_score_below_action_min",
    "nontechnical_evidence_gate_blocked",
    "nontechnical_component_date_missing",
    "nontechnical_component_from_future",
    "nontechnical_component_stale",
    "event_risk_from_future",
    "event_risk_stale",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def as_float(value: Any, default: float | None = None) -> float | None:
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


def explicit_true(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() == "true")


def date_token(value: Any) -> str | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    if len(text) >= 8 and text[:8].isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    return None


def parse_date(value: Any) -> dt.date | None:
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
        if value and value not in seen:
            target.append(value)
            seen.add(value)


def evidence_symbols(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    raw_symbols = payload.get("symbols", {}) if isinstance(payload.get("symbols", {}), dict) else {}
    for symbol, row in raw_symbols.items():
        if isinstance(row, dict):
            rows[str(symbol)] = {"symbol": str(symbol), **row}
    raw_evidence = payload.get("evidence", []) if isinstance(payload.get("evidence", []), list) else []
    for row in raw_evidence:
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = dict(row)
    return rows


def row_reasons(row: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for key in ("nontechnical_evidence_flags", "action_disqualifiers", "disqualifiers", "qualification_flags"):
        values = row.get(key, [])
        if not isinstance(values, list):
            continue
        for value in values:
            reason = str(value or "").strip()
            if reason in DIRECT_GAP_REASONS or reason.startswith("event_risk_"):
                reasons.append(reason)
    return reasons


def ranking_symbols(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    layers = [
        ("actionable_candidates", 0),
        ("diagnostic_candidates", 1),
        ("top_candidates", 2),
        ("all_ranked", 3),
    ]
    symbols: dict[str, dict[str, Any]] = {}
    for layer, layer_priority in layers:
        raw_rows = payload.get(layer, []) if isinstance(payload.get(layer, []), list) else []
        for index, raw_row in enumerate(raw_rows):
            if not isinstance(raw_row, dict) or not raw_row.get("symbol"):
                continue
            symbol = str(raw_row["symbol"])
            meta = symbols.setdefault(
                symbol,
                {
                    "symbol": symbol,
                    "layers": [],
                    "layer_priority": layer_priority,
                    "rank_index": index,
                    "primary_row": raw_row,
                    "ranking_reasons": [],
                },
            )
            if layer not in meta["layers"]:
                meta["layers"].append(layer)
            if (layer_priority, index) < (meta.get("layer_priority", 99), meta.get("rank_index", 10**9)):
                meta["layer_priority"] = layer_priority
                meta["rank_index"] = index
                meta["primary_row"] = raw_row
            append_unique(meta["ranking_reasons"], row_reasons(raw_row))
    return symbols


def focus_fields(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key.startswith("focus_") and value is not None}


def first_value(*values: Any) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def profile_for(meta: dict[str, Any]) -> dict[str, Any]:
    primary = meta.get("primary_row", {}) if isinstance(meta.get("primary_row"), dict) else {}
    profile = primary.get("nontechnical_evidence", {}) if isinstance(primary.get("nontechnical_evidence"), dict) else {}
    return profile


def component_values(raw: dict[str, Any], profile: dict[str, Any]) -> dict[str, float | None]:
    nested = profile.get("components", {}) if isinstance(profile.get("components"), dict) else {}
    return {key: as_float(first_value(raw.get(key), nested.get(key)), None) for key in COMPONENT_KEYS}


def component_max_staleness_days(policy: dict[str, Any]) -> dict[str, int]:
    days = DEFAULT_COMPONENT_MAX_STALENESS_DAYS.copy()
    raw = policy.get("component_max_staleness_days", {}) if isinstance(policy.get("component_max_staleness_days"), dict) else {}
    for key, value in raw.items():
        if key in days:
            days[key] = int(value)
    return days


def component_as_of_dates(raw: dict[str, Any], profile: dict[str, Any]) -> dict[str, str | None]:
    raw_dates = raw.get("component_as_of_dates", {}) if isinstance(raw.get("component_as_of_dates"), dict) else {}
    profile_dates = profile.get("component_as_of_dates", {}) if isinstance(profile.get("component_as_of_dates"), dict) else {}
    has_component_dates = bool(raw_dates) or bool(profile_dates) or any(raw.get(f"{key}_as_of_date") is not None for key in COMPONENT_KEYS)
    if not has_component_dates:
        return {key: None for key in COMPONENT_KEYS}
    return {key: date_token(first_value(raw_dates.get(key), profile_dates.get(key), raw.get(f"{key}_as_of_date"), raw.get("as_of_date"), profile.get("as_of_date"))) for key in COMPONENT_KEYS}


def computed_total_score(components: dict[str, float | None], weights: dict[str, Any]) -> float | None:
    score_sum = 0.0
    weight_sum = 0.0
    for key in COMPONENT_KEYS:
        value = components.get(key)
        weight = as_float(weights.get(key), DEFAULT_WEIGHTS[key]) or 0.0
        if value is None:
            continue
        score_sum += max(0.0, min(1.0, value)) * weight
        weight_sum += weight
    return round(score_sum / weight_sum, 3) if weight_sum else None


def source_count_for(raw: dict[str, Any], profile: dict[str, Any], proxy_only: bool) -> int:
    if proxy_only:
        return 0
    if raw.get("source_count") is not None:
        return as_int(raw.get("source_count"), 0)
    if profile.get("source_count") is not None:
        return as_int(profile.get("source_count"), 0)
    sources = raw.get("sources")
    if isinstance(sources, list):
        return len(sources)
    return 0


def evidence_gap_reasons(
    raw: dict[str, Any] | None,
    profile: dict[str, Any],
    ranking_reasons: list[str],
    policy: dict[str, Any],
    weights: dict[str, Any],
    as_of_date: str,
    as_of_session: str | None,
) -> tuple[list[str], dict[str, Any]]:
    raw = raw or {}
    reasons: list[str] = []
    append_unique(reasons, ranking_reasons)

    evidence_mode = str(first_value(raw.get("evidence_mode"), profile.get("evidence_mode"), "") or "").strip()
    status = str(first_value(profile.get("status"), raw.get("status"), "") or "").strip().lower()
    proxy_only = evidence_mode in {"automatic_local_proxy", "proxy_only"} or explicit_true(raw.get("proxy_only")) or status == "proxy_only"
    event_risk = str(first_value(raw.get("event_risk"), profile.get("event_risk"), "unknown") or "unknown").lower()
    components = component_values(raw, profile)
    total_score = as_float(first_value(raw.get("total_score"), profile.get("total_score")), None)
    if total_score is None:
        total_score = computed_total_score(components, weights)
    source_count = source_count_for(raw, profile, proxy_only)
    proxy_source_count = as_int(first_value(raw.get("proxy_source_count"), profile.get("proxy_source_count")), 0)
    evidence_date_text = first_value(raw.get("as_of_date"), profile.get("as_of_date"))
    evidence_date = parse_date(evidence_date_text)
    report_date = parse_date(as_of_date)
    evidence_session = str(first_value(raw.get("as_of_session"), profile.get("as_of_session"), "") or "").lower() or None
    report_session = str(as_of_session or "").lower() or None
    component_dates = component_as_of_dates(raw, profile)
    component_ages: dict[str, int] = {}
    stale_components: list[str] = []
    missing_component_dates: list[str] = []
    max_component_days = component_max_staleness_days(policy)

    if not raw and not profile:
        reasons.append("nontechnical_evidence_missing")
    if status == "missing" or evidence_mode == "missing_fail_closed":
        reasons.append("nontechnical_evidence_missing")
    if proxy_only:
        reasons.append("nontechnical_proxy_only")
    if source_count <= 0:
        reasons.append("nontechnical_source_missing")
    if event_risk == "unknown":
        reasons.append("event_risk_unknown")
    elif event_risk in HARD_EVENT_RISKS:
        reasons.append(f"event_risk_{event_risk}")

    if evidence_date is None:
        reasons.append("nontechnical_evidence_date_missing")
    elif report_date is not None:
        age_days = (report_date - evidence_date).days
        if age_days < 0:
            reasons.append("nontechnical_evidence_from_future")
        elif not any(component_dates.values()) and age_days > int(policy.get("max_staleness_days", DEFAULT_POLICY["max_staleness_days"])):
            reasons.append("nontechnical_evidence_stale")
        elif age_days == 0 and evidence_session and report_session and SESSION_ORDER.get(evidence_session, 99) > SESSION_ORDER.get(report_session, 99):
            reasons.append("nontechnical_evidence_from_future_session")
    else:
        age_days = as_int(raw.get("age_days"), 0)
        if raw.get("age_days") is not None and age_days > int(policy.get("max_staleness_days", DEFAULT_POLICY["max_staleness_days"])):
            reasons.append("nontechnical_evidence_stale")

    if report_date is not None and any(component_dates.values()):
        for key, raw_date in component_dates.items():
            component_date = parse_date(raw_date)
            if component_date is None:
                missing_component_dates.append(key)
                continue
            age_days = (report_date - component_date).days
            component_ages[key] = age_days
            if age_days < 0:
                reasons.append("nontechnical_component_from_future")
            elif age_days > int(max_component_days.get(key, policy.get("max_staleness_days", DEFAULT_POLICY["max_staleness_days"]))):
                stale_components.append(key)
        if missing_component_dates:
            reasons.append("nontechnical_component_date_missing")
        if stale_components:
            reasons.append("nontechnical_component_stale")

    event_risk_as_of_date = date_token(first_value(raw.get("event_risk_as_of_date"), profile.get("event_risk_as_of_date"), raw.get("event_as_of_date"), raw.get("as_of_date"), profile.get("as_of_date")))
    event_risk_age_days = None
    if report_date is not None and event_risk_as_of_date is not None:
        event_risk_date = parse_date(event_risk_as_of_date)
        if event_risk_date is not None:
            event_risk_age_days = (report_date - event_risk_date).days
            if event_risk_age_days < 0:
                reasons.append("event_risk_from_future")
            elif event_risk_age_days > int(max_component_days.get("event_risk", policy.get("max_staleness_days", DEFAULT_POLICY["max_staleness_days"]))):
                reasons.append("event_risk_stale")

    missing_components = [key for key, value in components.items() if value is None]
    if missing_components:
        reasons.append("nontechnical_component_missing")
    if total_score is None:
        reasons.append("nontechnical_score_missing")
    elif total_score < float(policy.get("min_total_score_for_action", DEFAULT_POLICY["min_total_score_for_action"])):
        reasons.append("nontechnical_score_below_action_min")

    deduped: list[str] = []
    append_unique(deduped, reasons)
    profile_summary = {
        "status": "missing" if (status == "missing" or evidence_mode == "missing_fail_closed" or (not raw and not profile)) else "proxy_only" if proxy_only else "available",
        "evidence_mode": evidence_mode or None,
        "proxy_only": proxy_only,
        "source_count": source_count,
        "proxy_source_count": proxy_source_count if proxy_only else None,
        "event_risk": event_risk,
        "as_of_date": date_token(evidence_date_text),
        "as_of_session": evidence_session,
        "component_as_of_dates": component_dates,
        "component_age_days": component_ages,
        "stale_components": stale_components,
        "missing_component_dates": missing_component_dates,
        "event_risk_as_of_date": event_risk_as_of_date,
        "event_risk_age_days": event_risk_age_days,
        "total_score": total_score,
        "components": components,
        "missing_components": missing_components,
    }
    return deduped, profile_summary


def priority_bucket(meta: dict[str, Any], score: float | None) -> tuple[int, str]:
    primary = meta.get("primary_row", {}) if isinstance(meta.get("primary_row"), dict) else {}
    layers = set(meta.get("layers", []))
    if "actionable_candidates" in layers or primary.get("qualified_for_action") is True:
        return 0, "actionable_candidate"
    if {"diagnostic_candidates", "top_candidates"} & layers or primary.get("diagnostic_only") is True:
        return 1, "diagnostic_or_top_candidate"
    if primary.get("qualified_for_watch") is True:
        return 2, "qualified_for_watch"
    if score is not None:
        return 3, "ranked_by_score"
    if focus_fields(primary):
        return 4, "focus_symbol"
    return 5, "ledger_only"


def skeleton_row(entry: dict[str, Any], as_of_date: str, as_of_session: str | None) -> dict[str, Any]:
    row = {
        "symbol": entry.get("symbol"),
        "name": entry.get("name"),
        "kind": entry.get("kind"),
        "theme": entry.get("theme"),
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "evidence_mode": "manual_point_in_time",
        "event_risk": "unknown",
        "source_count": 0,
        "sources": [],
        "component_as_of_dates": {key: None for key in COMPONENT_KEYS},
        "event_risk_as_of_date": None,
        "notes": [
            "Placeholder only: manual/formal nontechnical evidence is required before this row can support action.",
            "Fill component scores and sources from reviewed evidence; do not treat this skeleton as actionable evidence.",
        ],
        "proxy_only": False,
        "manual_review_required": True,
        "research_only": True,
    }
    for key in COMPONENT_KEYS:
        row[key] = None
    row["total_score"] = None
    return row


def build_gap_queue(
    nontechnical_evidence_path: pathlib.Path | None,
    ranking_path: pathlib.Path | None,
    as_of_date: str,
    as_of_session: str | None = None,
) -> dict[str, Any]:
    evidence_payload = load_json(nontechnical_evidence_path)
    ranking_payload = load_json(ranking_path)
    ledger = evidence_symbols(evidence_payload)
    ranked = ranking_symbols(ranking_payload)
    policy = DEFAULT_POLICY.copy()
    if isinstance(evidence_payload.get("policy"), dict):
        policy.update(evidence_payload["policy"])
    weights = DEFAULT_WEIGHTS.copy()
    if isinstance(evidence_payload.get("weights"), dict):
        weights.update(evidence_payload["weights"])

    symbols: list[str] = []
    for symbol in ranked:
        if symbol not in symbols:
            symbols.append(symbol)
    for symbol in ledger:
        if symbol not in symbols:
            symbols.append(symbol)

    queue: list[dict[str, Any]] = []
    for symbol in symbols:
        raw = ledger.get(symbol)
        meta = ranked.get(symbol, {"symbol": symbol, "layers": [], "rank_index": 10**9, "ranking_reasons": [], "primary_row": {}})
        primary = meta.get("primary_row", {}) if isinstance(meta.get("primary_row"), dict) else {}
        profile = profile_for(meta)
        reasons, evidence_summary = evidence_gap_reasons(raw, profile, meta.get("ranking_reasons", []), policy, weights, as_of_date, as_of_session)
        if not reasons:
            continue
        score = as_float(primary.get("score"), None)
        group, bucket = priority_bucket(meta, score)
        entry = {
            "symbol": symbol,
            "name": first_value(primary.get("name"), (raw or {}).get("name")),
            "kind": first_value(primary.get("kind"), (raw or {}).get("kind")),
            "theme": first_value(primary.get("theme"), (raw or {}).get("theme")),
            "priority_bucket": bucket,
            "ranking_layers": meta.get("layers", []),
            "ranking_rank": None if meta.get("rank_index") == 10**9 else meta.get("rank_index"),
            "score": score,
            "qualified_for_action": primary.get("qualified_for_action"),
            "qualified_for_watch": primary.get("qualified_for_watch"),
            "diagnostic_only": primary.get("diagnostic_only"),
            "focus": focus_fields(primary),
            "gap_reasons": reasons,
            "evidence": evidence_summary,
            "notes": ["Manual/formal actionable nontechnical evidence is required before this symbol can clear the nontechnical evidence gate."],
            "_sort": (group, -(score if score is not None else -1.0), 0 if focus_fields(primary) else 1, meta.get("rank_index", 10**9), symbol),
        }
        queue.append(entry)

    queue.sort(key=lambda entry: entry["_sort"])
    for index, entry in enumerate(queue, start=1):
        entry["priority_rank"] = index
        entry.pop("_sort", None)
    skeleton = [skeleton_row(entry, as_of_date, as_of_session) for entry in queue]

    return {
        "generated_at": utc_now(),
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "research_only": True,
        "no_execution": True,
        "summary": {
            "ranking_symbol_count": len(ranked),
            "ledger_symbol_count": len(ledger),
            "queue_count": len(queue),
            "skeleton_count": len(skeleton),
            "proxy_only_count": sum(1 for entry in queue if "nontechnical_proxy_only" in entry["gap_reasons"]),
            "missing_count": sum(1 for entry in queue if "nontechnical_evidence_missing" in entry["gap_reasons"]),
            "source_missing_count": sum(1 for entry in queue if "nontechnical_source_missing" in entry["gap_reasons"]),
            "event_risk_unknown_count": sum(1 for entry in queue if "event_risk_unknown" in entry["gap_reasons"]),
            "stale_count": sum(1 for entry in queue if "nontechnical_evidence_stale" in entry["gap_reasons"]),
            "component_stale_count": sum(1 for entry in queue if "nontechnical_component_stale" in entry["gap_reasons"]),
            "event_risk_stale_count": sum(1 for entry in queue if "event_risk_stale" in entry["gap_reasons"]),
            "component_missing_count": sum(1 for entry in queue if "nontechnical_component_missing" in entry["gap_reasons"]),
            "date_issue_count": sum(1 for entry in queue if any(reason in entry["gap_reasons"] for reason in ("nontechnical_evidence_date_missing", "nontechnical_evidence_from_future", "nontechnical_evidence_from_future_session"))),
            "focus_or_action_relevant_count": sum(1 for entry in queue if entry.get("priority_bucket") != "ledger_only"),
        },
        "queue": queue,
        "skeleton": skeleton,
        "sources": {
            "nontechnical_evidence": str(nontechnical_evidence_path) if nontechnical_evidence_path else None,
            "ranking": str(ranking_path) if ranking_path else None,
        },
    }


def write_markdown(path: pathlib.Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# Nontechnical Actionable Evidence Gap Queue",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"As-of: `{payload['as_of_date']}` session=`{payload.get('as_of_session')}`",
        f"Research only: `{payload['research_only']}`; no execution: `{payload['no_execution']}`",
        "",
        "## Summary",
        f"- queue_count: `{summary['queue_count']}`",
        f"- proxy_only: `{summary['proxy_only_count']}`",
        f"- missing: `{summary['missing_count']}`",
        f"- source_missing: `{summary['source_missing_count']}`",
        f"- event_risk_unknown: `{summary['event_risk_unknown_count']}`",
        f"- stale: `{summary['stale_count']}`",
        f"- component_stale: `{summary.get('component_stale_count')}`",
        f"- event_risk_stale: `{summary.get('event_risk_stale_count')}`",
        f"- skeleton_rows: `{summary['skeleton_count']}`",
        "",
        "## Top Queue Items",
    ]
    for entry in payload.get("queue", [])[:20]:
        reasons = ", ".join(entry.get("gap_reasons", [])[:4])
        lines.append(f"- `{entry.get('priority_rank')}` `{entry.get('symbol')}` score=`{entry.get('score')}` bucket=`{entry.get('priority_bucket')}` reasons={reasons}")
    if not payload.get("queue"):
        lines.append("- No actionable nontechnical evidence gaps detected.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_skeleton_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    skeleton_payload = {
        "generated_at": payload["generated_at"],
        "as_of_date": payload["as_of_date"],
        "as_of_session": payload.get("as_of_session"),
        "research_only": True,
        "no_execution": True,
        "manual_review_required": True,
        "evidence": payload.get("skeleton", []),
    }
    path.write_text(json.dumps(skeleton_payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a queue of symbols that need actionable nontechnical evidence.")
    parser.add_argument("--nontechnical-evidence", default=str(DEFAULT_OUTPUT_DIR / "latest.json"))
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_DIR / "latest_actionable_gap_queue.json"))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_DIR / "latest_actionable_gap_queue.md"))
    parser.add_argument("--output-skeleton-json", default=str(DEFAULT_OUTPUT_DIR / "manual" / "actionable_gap_skeleton.json"))
    args = parser.parse_args()

    output_json = resolve_path(args.output_json) or pathlib.Path(args.output_json)
    output_md = resolve_path(args.output_md) or pathlib.Path(args.output_md)
    output_skeleton_json = resolve_path(args.output_skeleton_json) or pathlib.Path(args.output_skeleton_json)
    payload = build_gap_queue(resolve_path(args.nontechnical_evidence), resolve_path(args.ranking), args.as_of_date, args.as_of_session)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_skeleton_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(output_md, payload)
    write_skeleton_json(output_skeleton_json, payload)
    print(f"Wrote nontechnical evidence gap queue: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
