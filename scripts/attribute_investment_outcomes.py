#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
from collections import Counter
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
BULLISH_STATES = {"buy_candidate", "accumulate", "hold"}
BEARISH_STATES = {"trim", "sell_candidate", "avoid"}
ALLOWED_FINAL_STATES_BY_CAP = {
    "avoid": {"avoid"},
    "watch_only": {"watch_only", "avoid"},
    "buy_candidate": {"buy_candidate", "watch_only", "avoid"},
    "accumulate": {"accumulate", "buy_candidate", "watch_only", "avoid"},
    "hold": {"hold", "watch_only", "avoid"},
    "trim": {"trim", "watch_only", "avoid"},
    "sell_candidate": {"sell_candidate", "trim", "watch_only", "avoid"},
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return load_json(path)
    except json.JSONDecodeError as exc:
        return {"_artifact_error": f"invalid_json: {exc}"}


def artifact_stems(call_date: str, session: str) -> list[str]:
    stems = [f"{call_date}-{session}"]
    if session in {"historical", "close"}:
        stems.append(call_date)
    return stems


def first_existing(directory: pathlib.Path, stems: list[str], suffix: str) -> pathlib.Path | None:
    for stem in stems:
        path = directory / f"{stem}-{suffix}.json"
        if path.exists():
            return path
    return None


def recommendations_by_symbol(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = {}
    for item in payload.get("recommendations", []):
        if isinstance(item, dict) and item.get("symbol"):
            rows[str(item["symbol"])] = item
    return rows


def risk_by_symbol(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = {}
    for item in payload.get("verdicts", []):
        if isinstance(item, dict) and item.get("symbol"):
            rows[str(item["symbol"])] = item
    return rows


def ranking_rows(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for key in ("all_ranked", "actionable_candidates", "top_candidates", "diagnostic_candidates"):
        for item in payload.get(key, []):
            if isinstance(item, dict) and item.get("symbol"):
                row = rows.setdefault(str(item["symbol"]), dict(item))
                layers = row.setdefault("source_layers", [])
                if key not in layers:
                    layers.append(key)
    return rows


def top_theme_row(payload: dict[str, Any], theme: str | None) -> dict[str, Any] | None:
    if not theme:
        return None
    candidates = [row for row in payload.get("all_ranked", []) if isinstance(row, dict) and row.get("theme") == theme]
    if not candidates:
        return None
    return max(candidates, key=lambda row: as_float(row.get("score")))


def as_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def unique(values: list[str]) -> list[str]:
    seen = set()
    out = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def state_above(state: str | None, cap: str | None) -> bool:
    allowed = ALLOWED_FINAL_STATES_BY_CAP.get(str(cap))
    if allowed is None:
        return False
    return str(state) not in allowed


def classify_attribution(
    record: dict[str, Any],
    final_call: dict[str, Any] | None,
    draft_call: dict[str, Any] | None,
    risk_verdict: dict[str, Any] | None,
    ranking_row: dict[str, Any] | None,
    ranking: dict[str, Any],
) -> tuple[list[str], list[str]]:
    tags: list[str] = []
    evidence: list[str] = []
    verdict = str(record.get("verdict") or "")
    return_pct = as_float(record.get("return_pct"))
    learning = str(record.get("learning_tag") or "")
    final_state = str((final_call or {}).get("state") or record.get("state") or "unknown")
    draft_state = str((draft_call or {}).get("state") or "missing")
    risk_decision = str((risk_verdict or {}).get("risk_decision") or "missing")
    risk_cap = str((risk_verdict or {}).get("final_state_cap") or "missing")

    if learning == "symbol_selection_error":
        tags.append("ranking_selection_error")
        evidence.append(f"learning_tag=symbol_selection_error selected_vs_best_bps={record.get('selected_vs_best_bps')}")
    if record.get("same_theme_best_missed"):
        tags.append("same_theme_best_missed")
        evidence.append(f"same_theme_best_missed best={record.get('peer_best_symbol')} best_return={record.get('peer_best_return_pct')}")
    if learning in {"timing_unclear", "bullish_misread", "defensive_misread"} or verdict == "mixed":
        tags.append("timing_error")
        evidence.append(f"timing evidence verdict={verdict} return_pct={record.get('return_pct')}")
    if learning == "theme_error":
        tags.append("theme_error")
        evidence.append(f"theme_error peer_median_return_pct={record.get('peer_median_return_pct')}")

    if ranking_row:
        cost_passed = ranking_row.get("cost_gate_passed")
        qualified_action = ranking_row.get("qualified_for_action")
        net_edge = ranking_row.get("net_expected_edge_bps")
        peer_passed = ranking_row.get("same_theme_peer_evidence_passed")
        peer_decision = ranking_row.get("peer_relative_decision")
        evidence.append(f"ranking score={ranking_row.get('score')} cost_gate_passed={cost_passed} qualified_for_action={qualified_action} net_expected_edge_bps={net_edge} same_theme_peer_evidence_passed={peer_passed} peer_relative_decision={peer_decision}")
        if peer_passed is False and final_state in BULLISH_STATES:
            tags.append("ranking_selection_error")
            evidence.append("bullish final state lacked same-theme best-peer evidence")
        if cost_passed is True and draft_state in BULLISH_STATES and final_state in BULLISH_STATES and verdict == "fail":
            tags.append("cost_gate_too_loose")
        unrelated_veto = risk_decision == "veto" or bool(set(ranking_row.get("disqualifiers", [])) - {"cost_gate_failed"})
        if cost_passed is False and final_state in {"watch_only", "avoid"} and draft_state not in BEARISH_STATES and return_pct > 1.0 and not unrelated_veto:
            tags.append("cost_gate_too_strict")
        same_theme_leader = top_theme_row(ranking, record.get("theme"))
        if same_theme_leader and same_theme_leader.get("symbol") != record.get("symbol") and verdict == "fail":
            tags.append("ranking_selection_error")
            evidence.append(f"theme_leader={same_theme_leader.get('symbol')} leader_score={same_theme_leader.get('score')}")
    else:
        evidence.append("missing ranking artifact or row")

    if risk_verdict:
        risk_tags = [str(item) for item in risk_verdict.get("risk_tags", [])]
        evidence.append(f"risk_decision={risk_decision} final_state_cap={risk_cap} risk_tags={risk_tags}")
        risk_restricted = risk_decision in {"veto", "downgrade"}
        if final_state in BULLISH_STATES and verdict == "fail" and not risk_restricted and not state_above(final_state, risk_cap):
            tags.append("risk_veto_missed")
        if risk_restricted and return_pct < -0.5:
            tags.append("risk_veto_saved_loss")
        if risk_restricted and return_pct > 1.0:
            tags.append("risk_veto_too_strict")
        if "symbol_risk_veto" in risk_tags and return_pct > 1.0:
            tags.append("symbol_risk_memory_too_harsh")
    else:
        evidence.append("missing risk review artifact or verdict")

    if draft_call and final_call and final_state != draft_state:
        tags.append("llm_final_deviation")
        evidence.append(f"final_state={final_state} differs from draft_state={draft_state}")
    if risk_verdict and final_call and state_above(final_state, risk_cap):
        tags.append("llm_final_deviation")
        evidence.append(f"final_state={final_state} exceeds risk_cap={risk_cap}")

    return unique(tags), unique(evidence)


def build_attribution(records_payload: dict[str, Any], calls_dir: pathlib.Path, rankings_dir: pathlib.Path, risk_dir: pathlib.Path) -> dict[str, Any]:
    entries = []
    counter: Counter[str] = Counter()
    call_counter: Counter[str] = Counter()
    tag_call_keys: set[tuple[str, str]] = set()
    artifact_cache: dict[pathlib.Path, dict[str, Any]] = {}

    def cached(path: pathlib.Path | None) -> dict[str, Any]:
        if path is None:
            return {}
        if path not in artifact_cache:
            artifact_cache[path] = load_optional_json(path)
        return artifact_cache[path]

    for record in records_payload.get("records", []):
        call_date = str(record.get("call_date") or "")
        session = str(record.get("session") or "close")
        symbol = str(record.get("symbol") or "")
        stems = artifact_stems(call_date, session)
        final_payload = cached(first_existing(calls_dir, stems, "calls"))
        draft_payload = cached(first_existing(calls_dir, stems, "draft-policy"))
        risk_payload = cached(first_existing(risk_dir, stems, "risk-review"))
        ranking_payload = cached(first_existing(rankings_dir, stems, "ranking"))
        final_call = recommendations_by_symbol(final_payload).get(symbol)
        draft_call = recommendations_by_symbol(draft_payload).get(symbol)
        risk_verdict = risk_by_symbol(risk_payload).get(symbol)
        ranking_row = ranking_rows(ranking_payload).get(symbol)
        tags, evidence = classify_attribution(record, final_call, draft_call, risk_verdict, ranking_row, ranking_payload)
        counter.update(tags)
        call_key = f"{call_date}|{session}|{symbol}"
        for tag in tags:
            key = (tag, call_key)
            if key not in tag_call_keys:
                tag_call_keys.add(key)
                call_counter[tag] += 1
        entries.append(
            {
                "call_date": call_date,
                "session": session,
                "symbol": symbol,
                "window_days": record.get("window_days"),
                "final_state": (final_call or {}).get("state") or record.get("state"),
                "draft_state": (draft_call or {}).get("state"),
                "risk_decision": (risk_verdict or {}).get("risk_decision"),
                "risk_cap": (risk_verdict or {}).get("final_state_cap"),
                "verdict": record.get("verdict"),
                "return_pct": record.get("return_pct"),
                "learning_tag": record.get("learning_tag"),
                "attribution_tags": tags,
                "evidence": evidence,
            }
        )

    return {
        "generated_at": utc_now(),
        "source_records_generated_at": records_payload.get("generated_at"),
        "record_count": len(entries),
        "attribution_counts": dict(sorted(counter.items())),
        "attribution_call_counts": dict(sorted(call_counter.items())),
        "top_attribution_tags": [{"tag": tag, "count": count} for tag, count in counter.most_common(10)],
        "top_attribution_call_tags": [{"tag": tag, "count": count} for tag, count in call_counter.most_common(10)],
        "entries": entries,
    }


def write_markdown(path: pathlib.Path, result: dict[str, Any]) -> None:
    lines = [
        "# Investment Outcome Attribution",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Records: `{result['record_count']}`",
        "",
        "## Top Attribution Tags",
    ]
    if result["top_attribution_tags"]:
        lines.extend(f"- `{item['tag']}`: {item['count']}" for item in result["top_attribution_tags"])
    else:
        lines.append("- No attribution tags detected.")
    lines.extend(["", "## Recent Tagged Records"])
    tagged = [entry for entry in result["entries"] if entry.get("attribution_tags")]
    if tagged:
        for entry in tagged[-15:]:
            tags = ", ".join(entry["attribution_tags"])
            lines.append(
                f"- `{entry['call_date']}` `{entry['session']}` `{entry['symbol']}` T+{entry['window_days']}: "
                f"{entry['return_pct']}% `{entry['verdict']}` -> {tags}"
            )
    else:
        lines.append("- No tagged records in the latest attribution run.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Attribute HK investment posterior outcomes to deterministic policy layers.")
    parser.add_argument("--records-json", default=str(ROOT / "research" / "evaluations" / "latest_records.json"))
    parser.add_argument("--calls-dir", default=str(ROOT / "research" / "calls"))
    parser.add_argument("--rankings-dir", default=str(ROOT / "research" / "rankings"))
    parser.add_argument("--risk-dir", default=str(ROOT / "research" / "risk"))
    parser.add_argument("--output-json", default=str(ROOT / "research" / "evaluations" / "latest_attribution.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "evaluations" / "latest_attribution.md"))
    args = parser.parse_args()

    result = build_attribution(load_json(pathlib.Path(args.records_json)), pathlib.Path(args.calls_dir), pathlib.Path(args.rankings_dir), pathlib.Path(args.risk_dir))
    output_json = pathlib.Path(args.output_json)
    output_md = pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(output_md, result)
    print(f"Wrote investment attribution: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
