#!/usr/bin/env python3

import argparse
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "research" / "products" / "daily_close"
STATE_RANK = {"avoid": 0, "watch_only": 1, "buy_candidate": 2, "hold": 2, "accumulate": 3, "trim": 1, "sell_candidate": 1}


def load_json(path: pathlib.Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def file_metadata(path: pathlib.Path | None) -> dict[str, Any]:
    return {"path": str(path) if path else None, "exists": bool(path and path.exists())}


def output_stem(date: str, session: str) -> str:
    return date if session in {"close", "historical"} else f"{date}-{session}"


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def require_close_session(calls: dict[str, Any] | None, session: str) -> None:
    actual = str((calls or {}).get("session") or session)
    if actual != "close":
        raise ValueError("Chinese daily close product requires session=close")


def date_value(value: Any) -> str | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return None


def assert_not_future(label: str, value: Any, report_date: str) -> None:
    parsed = date_value(value)
    if parsed and parsed > report_date:
        raise ValueError(f"{label} date {parsed} is after report date {report_date}")


def validate_source_dates(
    date: str,
    calls: dict[str, Any],
    ranking: dict[str, Any] | None,
    evidence_ledger: dict[str, Any] | None,
    calibration: dict[str, Any] | None,
    forward_eval: dict[str, Any] | None,
    variant_competition: dict[str, Any] | None,
) -> None:
    if date_value(calls.get("date")) != date:
        raise ValueError("calls date must match report date")
    if ranking is not None:
        assert_not_future("ranking as_of_date", ranking.get("as_of_date"), date)
    if evidence_ledger is not None:
        assert_not_future("evidence ledger as_of_date", evidence_ledger.get("as_of_date"), date)
    if calibration is not None:
        assert_not_future("calibration as_of_date", calibration.get("as_of_date"), date)
    if forward_eval is not None:
        thresholds = forward_eval.get("thresholds", {}) if isinstance(forward_eval.get("thresholds"), dict) else {}
        assert_not_future("forward evaluation as_of_date", thresholds.get("as_of_date"), date)
    if variant_competition is not None:
        assert_not_future("variant competition as_of_date", variant_competition.get("as_of_date") or variant_competition.get("date"), date)


def verdicts_by_symbol(risk_review: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    rows = {}
    for verdict in (risk_review or {}).get("verdicts", []):
        if isinstance(verdict, dict) and verdict.get("symbol"):
            rows[str(verdict["symbol"])] = verdict
    return rows


def summarize_recommendations(calls: dict[str, Any], risk_review: dict[str, Any] | None) -> list[dict[str, Any]]:
    verdicts = verdicts_by_symbol(risk_review)
    rows = []
    for rec in calls.get("recommendations", []):
        if not isinstance(rec, dict):
            continue
        symbol = str(rec.get("symbol") or "")
        verdict = verdicts.get(symbol, {})
        state = str(rec.get("state") or "avoid")
        cap = str(verdict.get("final_state_cap") or state)
        if risk_review is not None and not verdict:
            raise ValueError(f"missing risk review verdict for {symbol}")
        if STATE_RANK.get(state, 0) > STATE_RANK.get(cap, 0):
            raise ValueError(f"call state {state} exceeds risk review cap {cap} for {symbol}")
        rows.append(
            {
                "symbol": symbol,
                "state": state,
                "effective_state": cap if STATE_RANK.get(cap, 0) < STATE_RANK.get(state, 0) else state,
                "theme": rec.get("theme"),
                "confidence": rec.get("confidence"),
                "risk_cap": cap,
                "risk_decision": verdict.get("risk_decision"),
                "rationale": rec.get("rationale"),
                "risks": rec.get("risks", [])[:3] if isinstance(rec.get("risks"), list) else [],
                "invalidation": rec.get("invalidation"),
            }
        )
    return rows


def top_rows(ranking: dict[str, Any] | None, key: str, limit: int = 5) -> list[dict[str, Any]]:
    rows = (ranking or {}).get(key, [])
    return rows[:limit] if isinstance(rows, list) else []


def summary_get(data: dict[str, Any] | None, path: list[str], default: Any = None) -> Any:
    node: Any = data
    for key in path:
        if not isinstance(node, dict):
            return default
        node = node.get(key)
    return node if node is not None else default


def build_payload(
    date: str,
    session: str,
    calls: dict[str, Any],
    ranking: dict[str, Any] | None,
    risk_review: dict[str, Any] | None,
    evidence_ledger: dict[str, Any] | None,
    calibration: dict[str, Any] | None,
    forward_eval: dict[str, Any] | None,
    variant_competition: dict[str, Any] | None,
    sources: dict[str, pathlib.Path | None],
) -> dict[str, Any]:
    require_close_session(calls, session)
    validate_source_dates(date, calls, ranking, evidence_ledger, calibration, forward_eval, variant_competition)
    recommendations = summarize_recommendations(calls, risk_review)
    return {
        "date": date,
        "session": "close",
        "source_of_truth": "calls_json_with_risk_review_caps",
        "research_only": True,
        "no_execution": True,
        "recommendations": recommendations,
        "ranking": {
            "actionable_count": len((ranking or {}).get("actionable_candidates", [])) if isinstance((ranking or {}).get("actionable_candidates", []), list) else 0,
            "diagnostic_count": len((ranking or {}).get("diagnostic_candidates", [])) if isinstance((ranking or {}).get("diagnostic_candidates", []), list) else 0,
            "top_watch": top_rows(ranking, "top_candidates", 5),
        },
        "evidence": {
            "forward_shadow_logs": summary_get(evidence_ledger, ["summary", "forward_shadow_log_count"], summary_get(forward_eval, ["summary", "forward_shadow_log_count"])),
            "matured_forward_days": summary_get(evidence_ledger, ["shadow_evaluation_summary", "matured_forward_shadow_days"], summary_get(forward_eval, ["summary", "matured_forward_shadow_days"])),
            "forward_sample_count": summary_get(forward_eval, ["summary", "sample_count"], 0),
            "audit_passed": summary_get(evidence_ledger, ["audit_passed"]),
        },
        "calibration": {
            "sample_count": summary_get(calibration, ["summary", "combined_record_count"]),
            "scored_sample_count": summary_get(calibration, ["scorecard", "scored_sample_count"]),
            "hit_rate": summary_get(calibration, ["scorecard", "hit_rate"]),
            "brier_score": summary_get(calibration, ["scorecard", "brier_score"]),
            "calibration_error": summary_get(calibration, ["scorecard", "calibration_error"]),
        },
        "variants": {
            "competition_id": (variant_competition or {}).get("competition_id"),
            "scoreboard": (variant_competition or {}).get("scoreboard", [])[:3] if isinstance((variant_competition or {}).get("scoreboard", []), list) else [],
        },
        "sources": {name: file_metadata(path) for name, path in sources.items()},
    }


def render_markdown(payload: dict[str, Any]) -> str:
    recs = payload["recommendations"]
    buy_like = [row for row in recs if row.get("state") == "buy_candidate"]
    watch = [row for row in recs if row.get("state") == "watch_only"]
    avoid = [row for row in recs if row.get("state") == "avoid"]
    lines = [
        f"# {payload['date']} 收盘研究报告",
        "",
        "## 今日结论",
        f"- 研究模式：仅推荐研究；不执行交易、不修改组合。",
        f"- 行动候选：{len(buy_like)} 个；观察名单：{len(watch)} 个；回避/不行动：{len(avoid)} 个。",
        f"- 证据进度：forward logs={payload['evidence']['forward_shadow_logs']}，matured days={payload['evidence']['matured_forward_days']}，forward samples={payload['evidence']['forward_sample_count']}。",
        "",
        "## 重点标的表",
    ]
    if not recs:
        lines.append("- 今日没有结构化推荐。")
    for row in recs[:8]:
        lines.append(f"- `{row['symbol']}`：状态={row.get('state')}，主题={row.get('theme')}，置信度={row.get('confidence')}，风险上限={row.get('risk_cap') or 'n/a'}。")
        if row.get("rationale"):
            lines.append(f"  - 理由：{row['rationale']}")
        if row.get("risks"):
            lines.append(f"  - 风险：{'；'.join(str(item) for item in row['risks'])}")
        if row.get("invalidation"):
            lines.append(f"  - 失效条件：{row['invalidation']}")
    lines.extend(["", "## Gate 拒绝与观察重点"])
    for row in payload["ranking"]["top_watch"][:5]:
        disq = row.get("action_disqualifiers") or row.get("disqualifiers") or []
        lines.append(f"- `{row.get('symbol')}` score={row.get('score')} action={row.get('qualified_for_action')} watch={row.get('qualified_for_watch')} gates={disq[:3]}")
    lines.extend(
        [
            "",
            "## 影子证据与校准",
            f"- Evidence audit passed：{payload['evidence']['audit_passed']}。",
            f"- Calibration samples：{payload['calibration']['sample_count']}；hit_rate={payload['calibration']['hit_rate']}；Brier={payload['calibration']['brier_score']}；calibration_error={payload['calibration']['calibration_error']}。",
            "",
            "## Shadow 变体竞赛",
        ]
    )
    variants = payload["variants"].get("scoreboard") or []
    if not variants:
        lines.append("- 暂无可排名的 shadow-only 变体样本；继续累计 forward evidence。")
    for row in variants:
        lines.append(f"- #{row.get('diagnostic_rank')} `{row.get('variant_id')}` samples={row.get('sample_count')} avg_net={row.get('avg_net_return_pct')} alpha={row.get('avg_alpha_pct')} audit={row.get('no_execution_audit_passed')}")
    lines.extend(
        [
            "",
            "## 数据与限制",
            "- 本报告只整理 deterministic ranking、calls、risk review、shadow evidence 和 calibration scorecard。",
            "- 不把 historical replay 当作 forward evidence；不因 shadow 变体结果自动晋升 active strategy。",
            "- forward 样本不足时，所有结论只能作为研究观察。",
            "",
            "## 研究声明",
            "- 这不是投资建议或交易指令；系统不会自动下单，也不会假设真实持仓。",
        ]
    )
    return "\n".join(lines) + "\n"


def build_report(
    date: str,
    session: str,
    calls_path: pathlib.Path,
    ranking_path: pathlib.Path | None,
    risk_review_path: pathlib.Path | None,
    evidence_ledger_path: pathlib.Path | None,
    calibration_path: pathlib.Path | None,
    forward_eval_path: pathlib.Path | None,
    variant_competition_path: pathlib.Path | None,
    output_dir: pathlib.Path,
) -> dict[str, Any]:
    calls = load_json(calls_path)
    if calls is None:
        raise ValueError(f"missing calls file: {calls_path}")
    payload = build_payload(
        date,
        session,
        calls,
        load_json(ranking_path),
        load_json(risk_review_path),
        load_json(evidence_ledger_path),
        load_json(calibration_path),
        load_json(forward_eval_path),
        load_json(variant_competition_path),
        {
            "calls": calls_path,
            "ranking": ranking_path,
            "risk_review": risk_review_path,
            "evidence_ledger": evidence_ledger_path,
            "calibration_scorecard": calibration_path,
            "forward_evaluation": forward_eval_path,
            "variant_competition": variant_competition_path,
        },
    )
    stem = output_stem(date, session)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{stem}-close-report.json"
    md_path = output_dir / f"{stem}-close-report.md"
    latest_md = output_dir / "latest.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    markdown = render_markdown(payload)
    md_path.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "latest": str(latest_md), "payload": payload}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic Chinese daily close research product report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--session", default="close")
    parser.add_argument("--calls", required=True)
    parser.add_argument("--ranking", default=None)
    parser.add_argument("--risk-review", default=None)
    parser.add_argument("--evidence-ledger", default=str(ROOT / "research" / "shadow" / "latest_evidence_ledger.json"))
    parser.add_argument("--calibration-scorecard", default=str(ROOT / "research" / "evaluations" / "latest_calibration_scorecard.json"))
    parser.add_argument("--forward-evaluation", default=str(ROOT / "research" / "shadow" / "latest_forward_evaluation.json"))
    parser.add_argument("--variant-competition", default=None)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    result = build_report(
        args.date,
        args.session,
        resolve_path(args.calls) or pathlib.Path(args.calls),
        resolve_path(args.ranking),
        resolve_path(args.risk_review),
        resolve_path(args.evidence_ledger),
        resolve_path(args.calibration_scorecard),
        resolve_path(args.forward_evaluation),
        resolve_path(args.variant_competition),
        resolve_path(args.output_dir) or DEFAULT_OUTPUT_DIR,
    )
    print(json.dumps({key: result[key] for key in ["json", "markdown", "latest"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
