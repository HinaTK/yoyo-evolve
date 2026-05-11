#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import re
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "research" / "experiments" / "system_changes" / "latest_improvement_plan.json"
ATTRIBUTION_TASK_SPECS = {
    "risk_veto_too_strict": (
        "Calibrate risk veto strictness after saved-opportunity evidence",
        "Adjust deterministic risk-review thresholds or symbol-risk-memory expiry so risk caps stay protective without repeatedly blocking later winners.",
        ["python -m py_compile scripts/attribute_investment_outcomes.py scripts/generate_investment_risk_review.py", "python -m unittest tests/test_investment_level5_level6.py"],
    ),
    "cost_gate_too_strict": (
        "Diagnose overly strict cost gate opportunity loss",
        "Add diagnostics or parameter tests for cases where the cost gate blocks candidates that later clear the forward-return hurdle, without lowering production gates by default.",
        ["python scripts/backtest_investment_strategy.py", "python -m unittest tests/test_investment_level5_level6.py"],
    ),
    "risk_veto_missed": (
        "Add missing deterministic risk veto evidence",
        "Harden risk review tags so failed bullish calls expose the pre-call risk signal that should have capped or vetoed them.",
        ["python -m py_compile scripts/generate_investment_risk_review.py scripts/attribute_investment_outcomes.py", "python -m unittest tests/test_investment_level5_level6.py"],
    ),
    "cost_gate_too_loose": (
        "Tighten loose cost gate diagnostics",
        "Identify why cost-qualified bullish calls failed and add conservative diagnostics or tests before any candidate is upgraded.",
        ["python scripts/backtest_investment_strategy.py", "python -m unittest tests/test_investment_level5_level6.py"],
    ),
    "ranking_selection_error": (
        "Improve ranking selection attribution and peer checks",
        "Make ranking or recommendation evidence prefer same-theme leaders when posterior attribution repeatedly shows selected symbols lagged better-ranked peers.",
        ["python scripts/attribute_investment_outcomes.py", "python -m unittest tests/test_investment_level5_level6.py"],
    ),
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def error_pattern_count(memory_text: str, tag: str) -> int:
    phrase = tag.replace("_", "[- _]")
    return len(re.findall(phrase, memory_text, flags=re.IGNORECASE))


def add_task(tasks: list[dict[str, Any]], title: str, evidence: list[str], objective: str, validation: list[str]) -> None:
    if len(tasks) >= 3:
        return
    if any(task["title"] == title for task in tasks):
        return
    tasks.append({"id": f"investment_task_{len(tasks) + 1:02d}", "title": title, "evidence": evidence, "objective": objective, "validation": validation})


def attribution_count(attribution: dict[str, Any], tag: str) -> int:
    counts = attribution.get("attribution_call_counts", {}) or {}
    return as_int(counts.get(tag))


def add_attribution_tasks(tasks: list[dict[str, Any]], attribution: dict[str, Any]) -> None:
    record_count = as_int(attribution.get("record_count"))
    if not record_count:
        return
    for tag in ("risk_veto_too_strict", "cost_gate_too_strict", "risk_veto_missed", "cost_gate_too_loose", "ranking_selection_error"):
        count = attribution_count(attribution, tag)
        if count < 2:
            continue
        title, objective, validation = ATTRIBUTION_TASK_SPECS[tag]
        add_task(
            tasks,
            title,
            [f"attribution_tag={tag}", f"count={count}", f"record_count={record_count}"],
            objective,
            validation,
        )


def plan_tasks(evaluation: dict[str, Any], backtest: dict[str, Any], optimization: dict[str, Any], memory_text: str, attribution: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    eval_count = as_int(evaluation.get("evaluations"))
    learning_counts = evaluation.get("learning_counts", {}) or {}
    verdict_counts = evaluation.get("verdict_counts", {}) or {}
    fail_count = as_int(verdict_counts.get("fail"))
    pass_count = as_int(verdict_counts.get("pass"))
    total_decisive = fail_count + pass_count
    call_pass_rate = pass_count / total_decisive if total_decisive else 0.0
    backtest_summary = backtest.get("summary", {}) or {}
    if optimization.get("updated_active_strategy") is True:
        opt_active = optimization.get("champion", {}) or {}
    else:
        opt_active = optimization.get("baseline", {}) or {}
    opt_summary = opt_active.get("summary", {}) or backtest_summary
    sample_count = as_int(opt_summary.get("sample_count") or backtest_summary.get("sample_count"))
    sample_quality = str(opt_summary.get("sample_quality") or backtest_summary.get("sample_quality") or "")
    diagnostic_sample_count = as_int(opt_summary.get("diagnostic_sample_count") or backtest_summary.get("diagnostic_sample_count"))
    qualified_sample_count = as_int(opt_summary.get("qualified_sample_count") or backtest_summary.get("qualified_sample_count"))
    explicit_diagnostic_reporting = any(
        key in summary
        for summary in (opt_summary, backtest_summary)
        for key in ("promotable_sample_count", "diagnostic_layer_sample_count", "diagnostic_only_sample_count")
    )
    win_rate = as_float(opt_summary.get("win_rate") if opt_summary.get("win_rate") is not None else backtest_summary.get("win_rate"))
    adverse = as_float(opt_summary.get("max_adverse_pct") if opt_summary.get("max_adverse_pct") is not None else backtest_summary.get("max_adverse_pct"))
    adverse_breach_rate = as_float(
        opt_summary.get("adverse_breach_rate") if opt_summary.get("adverse_breach_rate") is not None else backtest_summary.get("adverse_breach_rate")
    )
    avg_net = as_float(backtest_summary.get("avg_net_return_pct"))
    avg_alpha = as_float(backtest_summary.get("avg_alpha_pct"))

    if sample_quality == "relaxed_fallback":
        add_task(
            tasks,
            "Align backtest candidate policy with production recommendation gates",
            [f"sample_quality={sample_quality}", f"strict_sample_count={opt_summary.get('strict_sample_count') or backtest_summary.get('strict_sample_count')}", f"relaxed_sample_count={opt_summary.get('relaxed_sample_count') or backtest_summary.get('relaxed_sample_count')}"],
            "Keep relaxed fallback useful for diagnostics while preventing below-threshold backtest samples from being confused with promotable production recommendations.",
            ["python -m py_compile scripts/backtest_investment_strategy.py scripts/optimize_investment_params.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    if diagnostic_sample_count > qualified_sample_count and diagnostic_sample_count >= 3 and not explicit_diagnostic_reporting:
        add_task(
            tasks,
            "Align diagnostic and qualified candidate reporting",
            [f"diagnostic_sample_count={diagnostic_sample_count}", f"qualified_sample_count={qualified_sample_count}"],
            "Ensure production prompts and backtests use the same qualified candidate gate, while diagnostic-only rows remain visibly non-promotable.",
            ["python scripts/backtest_investment_strategy.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    elif sample_count < 12:
        add_task(
            tasks,
            "Increase backtest sample coverage before promoting strategies",
            [f"latest_optimization sample_count={sample_count}", f"decision_reason={optimization.get('decision_reason', 'unknown')}"],
            "Improve the research backtest pipeline so parameter changes are judged on more mature historical samples or explicitly marked inconclusive when samples are thin.",
            ["python -m py_compile scripts/backtest_investment_strategy.py scripts/optimize_investment_params.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    if win_rate and win_rate < 0.45:
        add_task(
            tasks,
            "Reduce low win-rate candidate selection",
            [f"latest_optimization win_rate={win_rate}", f"latest_backtest avg_net_return_pct={avg_net}"],
            "Tighten research-only ranking or call qualification so weak technical setups remain watch_only instead of being upgraded.",
            ["python scripts/backtest_investment_strategy.py", "python scripts/optimize_investment_params.py"],
        )
    if adverse and adverse < -8.0:
        add_task(
            tasks,
            "Add adverse-move protection to research ranking",
            [f"latest_optimization max_adverse_pct={adverse}", f"latest_backtest avg_alpha_pct={avg_alpha}"],
            "Add or test drawdown-aware research filters without reducing cost, edge, or exposure gates.",
            ["python scripts/backtest_investment_strategy.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    if adverse_breach_rate and adverse_breach_rate > 0.25:
        add_task(
            tasks,
            "Add adverse breach-rate protection to research ranking",
            [f"latest_optimization adverse_breach_rate={adverse_breach_rate}", f"latest_optimization max_adverse_pct={adverse}"],
            "Penalize or gate research candidates that repeatedly breach adverse-move limits instead of relying only on the single worst drawdown.",
            ["python scripts/backtest_investment_strategy.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )

    symbol_errors = as_int(learning_counts.get("symbol_selection_error")) + error_pattern_count(memory_text, "symbol_selection_error")
    overconfidence = as_int(learning_counts.get("overconfidence")) + error_pattern_count(memory_text, "overconfidence")
    recent_selection_errors = evaluation.get("recent_selection_errors", []) or []
    same_theme_misses = sum(1 for item in recent_selection_errors if item.get("same_theme_best_missed"))
    if symbol_errors >= 3 and same_theme_misses:
        add_task(
            tasks,
            "Require same-theme best-peer evidence before symbol upgrades",
            [f"symbol_selection_error count={learning_counts.get('symbol_selection_error', 0)}", f"same_theme_best_missed={same_theme_misses}"],
            "Make ranking and recommendation prompts show whether the selected symbol beat the same-theme best peer before any watch candidate is upgraded.",
            ["python scripts/evaluate_investment_calls.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    elif symbol_errors >= 3:
        add_task(
            tasks,
            "Improve same-theme symbol selection evidence",
            [f"symbol_selection_error count={learning_counts.get('symbol_selection_error', 0)}", "memory contains repeated symbol-selection cautions"],
            "Make recommendations compare a selected symbol against same-theme peers before upgrading it.",
            ["python scripts/evaluate_investment_calls.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    if overconfidence >= 3:
        add_task(
            tasks,
            "Calibrate confidence after failed calls",
            [f"overconfidence count={learning_counts.get('overconfidence', 0)}", f"decisive call pass_rate={call_pass_rate:.3f}"],
            "Lower confidence or force extra evidence for states that recently failed with high confidence.",
            ["python scripts/evaluate_investment_calls.py", "python -m unittest tests/test_investment_level5_level6.py"],
        )
    if eval_count and backtest_summary and abs(call_pass_rate - as_float(backtest_summary.get("win_rate"))) > 0.2:
        add_task(
            tasks,
            "Reconcile calls evaluation and backtest metrics",
            [f"calls pass_rate={call_pass_rate:.3f}", f"backtest win_rate={backtest_summary.get('win_rate')}"],
            "Document and reduce metric-definition drift between posterior calls evaluation and ranking backtests.",
            ["python scripts/evaluate_investment_calls.py", "python scripts/backtest_investment_strategy.py"],
        )
    add_attribution_tasks(tasks, attribution or {})
    return tasks


def write_task_files(tasks: list[dict[str, Any]], plan_dir: pathlib.Path) -> None:
    plan_dir.mkdir(parents=True, exist_ok=True)
    for existing in plan_dir.glob("investment_task_*.md"):
        existing.unlink()
    for task in tasks:
        path = plan_dir / f"{task['id']}.md"
        lines = [f"# {task['title']}", "", "## Evidence"]
        lines.extend(f"- {item}" for item in task["evidence"])
        lines.extend(["", "## Objective", task["objective"], "", "## Constraints", "- Research-only: do not add automatic trading, execution venue integrations, trade placement, or execution hooks.", "- Do not loosen cost, edge, exposure, or as-of/future leakage safeguards.", "- Do not mutate historical files under data/snapshots.", "", "## Validation"])
        lines.extend(f"- `{item}`" for item in task["validation"])
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan evidence-based investment system improvement tasks.")
    parser.add_argument("--evaluations", default=str(ROOT / "research" / "evaluations" / "latest.json"))
    parser.add_argument("--backtest", default=str(ROOT / "research" / "experiments" / "latest_backtest.json"))
    parser.add_argument("--optimization", default=str(ROOT / "research" / "experiments" / "latest_optimization.json"))
    parser.add_argument("--attribution", default=str(ROOT / "research" / "evaluations" / "latest_attribution.json"))
    parser.add_argument("--memory", default=str(ROOT / "memory" / "investment_error_patterns.md"))
    parser.add_argument("--plan-dir", default=str(ROOT / "session_plan"))
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()

    evaluation = load_json(pathlib.Path(args.evaluations))
    backtest = load_json(pathlib.Path(args.backtest))
    optimization = load_json(pathlib.Path(args.optimization))
    attribution = load_json(pathlib.Path(args.attribution))
    memory_text = load_text(pathlib.Path(args.memory))
    tasks = plan_tasks(evaluation, backtest, optimization, memory_text, attribution)[:3]
    write_task_files(tasks, pathlib.Path(args.plan_dir))
    result = {
        "generated_at": utc_now(),
        "task_count": len(tasks),
        "attribution_summary": {
            "record_count": as_int(attribution.get("record_count")),
            "top_attribution_tags": attribution.get("top_attribution_tags", [])[:5] if isinstance(attribution.get("top_attribution_tags"), list) else [],
            "top_attribution_call_tags": attribution.get("top_attribution_call_tags", [])[:5] if isinstance(attribution.get("top_attribution_call_tags"), list) else [],
        },
        "tasks": tasks,
    }
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
