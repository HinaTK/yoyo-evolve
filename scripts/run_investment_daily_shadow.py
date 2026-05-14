#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import shlex
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from typing import Any, Callable


ROOT = pathlib.Path(__file__).resolve().parent.parent
VALID_SESSIONS = {"morning", "midday", "close", "historical"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_toml(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def shadow_variant_competition_id(root: pathlib.Path) -> str:
    config = read_toml(root / "config" / "shadow_variants.toml")
    return str(config.get("competition_id") or "shadow_variants")


def resolve_path(root: pathlib.Path, value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else root / path


def output_stem(date: str, session: str) -> str:
    return date if session == "historical" else f"{date}-{session}"


def close_report_stem(date: str, session: str) -> str:
    return date if session in {"close", "historical"} else f"{date}-{session}"


def default_snapshot_file(root: pathlib.Path, date: str, session: str) -> pathlib.Path:
    if session in {"morning", "midday"}:
        return root / "data" / "snapshots" / f"{date}-{session}.json"
    return root / "data" / "snapshots" / f"{date}.json"


def default_radar_snapshot_file(root: pathlib.Path, date: str, session: str, snapshot_file: pathlib.Path) -> pathlib.Path:
    if session == "historical":
        return snapshot_file
    if session in {"morning", "midday"}:
        return root / "data" / "snapshots" / f"{date}-{session}-radar.json"
    return root / "data" / "snapshots" / f"{date}-radar.json"


def default_evidence_mode(session: str) -> str:
    return "historical_replay" if session == "historical" else "forward_shadow"


def script_path(root: pathlib.Path, name: str) -> pathlib.Path:
    return root / "scripts" / name


def shell_quote_command(command: list[str | pathlib.Path]) -> str:
    return " ".join(shlex.quote(str(part)) for part in command)


def run_command(name: str, command: list[str | pathlib.Path], cwd: pathlib.Path, check: bool = True) -> int:
    print(f"-> {name}: {shell_quote_command(command)}")
    completed = subprocess.run([str(part) for part in command], cwd=str(cwd), check=False)
    if check and completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.returncode


def configured_symbol_risk_file(root: pathlib.Path, optimization: dict[str, Any]) -> pathlib.Path:
    return resolve_path(root, optimization.get("symbol_risk_memory")) or root / "research" / "experiments" / "symbol_risk_memory.json"


def configured_round_trip_bps(profile: dict[str, Any], optimization: dict[str, Any], active: dict[str, Any]) -> float:
    costs = profile.get("costs", {}) if isinstance(profile.get("costs"), dict) else {}
    active_gate = active.get("cost_gate", {}) if isinstance(active.get("cost_gate"), dict) else {}
    opt_safety = optimization.get("safety_invariants", {}) if isinstance(optimization.get("safety_invariants"), dict) else {}
    active_safety = active.get("safety_invariants", {}) if isinstance(active.get("safety_invariants"), dict) else {}
    value = float(costs.get("estimated_round_trip_bps", 35))
    if active_safety.get("forbid_cost_gate_reduction", True) and opt_safety.get("forbid_cost_gate_reduction", True):
        value = max(value, float(active_gate.get("estimated_round_trip_bps", value)), float(optimization.get("round_trip_bps", value)))
    return value


def configured_minimum_edge_bps(profile: dict[str, Any], optimization: dict[str, Any], active: dict[str, Any]) -> float:
    costs = profile.get("costs", {}) if isinstance(profile.get("costs"), dict) else {}
    active_gate = active.get("cost_gate", {}) if isinstance(active.get("cost_gate"), dict) else {}
    opt_safety = optimization.get("safety_invariants", {}) if isinstance(optimization.get("safety_invariants"), dict) else {}
    active_safety = active.get("safety_invariants", {}) if isinstance(active.get("safety_invariants"), dict) else {}
    value = float(costs.get("minimum_edge_bps", 100))
    if active_safety.get("forbid_edge_gate_reduction", True) and opt_safety.get("forbid_edge_gate_reduction", True):
        value = max(value, float(active_gate.get("minimum_edge_bps", value)), float(optimization.get("minimum_edge_bps", value)))
    return value


def ranking_cli_args(root: pathlib.Path) -> tuple[list[str], float]:
    profile = read_toml(root / "config" / "investment_profile.toml")
    optimization = read_toml(root / "config" / "optimization.toml")
    active = read_toml(root / "config" / "active_strategy.toml")
    ranking = profile.get("ranking", {}) if isinstance(profile.get("ranking"), dict) else {}
    round_trip_bps = configured_round_trip_bps(profile, optimization, active)
    minimum_edge_bps = configured_minimum_edge_bps(profile, optimization, active)
    diagnostic_top_n = optimization.get("diagnostic_top_n", optimization.get("top_n", ranking.get("diagnostic_top_n", 3)))
    return (
        [
            "--max-candidates",
            str(ranking.get("max_candidates", 8)),
            "--actionable-top-n",
            str(optimization.get("actionable_top_n", ranking.get("actionable_top_n", 1))),
            "--diagnostic-top-n",
            str(diagnostic_top_n),
            "--min-watch-score",
            str(ranking.get("min_watch_score", 45)),
            "--min-action-score",
            str(ranking.get("min_action_score", 65)),
            "--round-trip-bps",
            str(round_trip_bps),
            "--minimum-edge-bps",
            str(minimum_edge_bps),
        ],
        round_trip_bps,
    )


@dataclass
class DailyShadowOptions:
    root: pathlib.Path
    python_bin: str
    date: str
    session: str
    snapshot_file: pathlib.Path | None = None
    radar_snapshot_file: pathlib.Path | None = None
    ranking_file: pathlib.Path | None = None
    shadow_file: pathlib.Path | None = None
    evidence_mode: str | None = None
    force_snapshot: bool = False
    skip_fetch: bool = False
    skip_radar_fetch: bool = False
    skip_symbol_risk: bool = False
    run_optimization: bool = False
    evaluate_shadow: bool = True
    build_evidence_ledger: bool = True
    build_calibration_scorecard: bool = True
    run_variant_competition: bool = True
    build_close_report: bool = True
    calls_file: pathlib.Path | None = None
    risk_review_file: pathlib.Path | None = None
    include_replay: bool = False
    min_forward_shadow_days: int = 20
    summary_output: pathlib.Path | None = None
    dry_run: bool = False


def ensure_directories(root: pathlib.Path) -> None:
    for relative in [
        "data/snapshots",
        "research/rankings",
        "research/experiments",
        "research/shadow",
        "research/shadow_variants",
        "research/products/daily_close",
    ]:
        (root / relative).mkdir(parents=True, exist_ok=True)


def run_pipeline(options: DailyShadowOptions, runner: Callable[[str, list[str | pathlib.Path], pathlib.Path, bool], int] = run_command) -> dict[str, Any]:
    if options.session not in VALID_SESSIONS:
        raise SystemExit(f"Invalid session '{options.session}'. Use one of {sorted(VALID_SESSIONS)}")

    root = options.root.resolve()
    ensure_directories(root)
    stem = output_stem(options.date, options.session)
    snapshot_file = resolve_path(root, options.snapshot_file) or default_snapshot_file(root, options.date, options.session)
    radar_snapshot_file = resolve_path(root, options.radar_snapshot_file) or default_radar_snapshot_file(root, options.date, options.session, snapshot_file)
    ranking_file = resolve_path(root, options.ranking_file) or root / "research" / "rankings" / f"{stem}-ranking.json"
    shadow_file = resolve_path(root, options.shadow_file) or root / "research" / "shadow" / f"{stem}-shadow.json"
    calls_file = resolve_path(root, options.calls_file) or root / "research" / "calls" / f"{stem}-calls.json"
    risk_review_file = resolve_path(root, options.risk_review_file) or root / "research" / "risk" / f"{stem}-risk-review.json"
    evidence_mode = options.evidence_mode or default_evidence_mode(options.session)
    if evidence_mode not in {"forward_shadow", "historical_replay"}:
        raise SystemExit("evidence_mode must be forward_shadow or historical_replay")
    registry_file = root / "data" / "snapshots" / "registry.json"
    optimization_config = root / "config" / "optimization.toml"
    trade_universe_config = root / "config" / "trade_universe.toml"
    radar_config = root / "config" / "market_radar.toml"
    active_strategy_file = root / "config" / "active_strategy.toml"
    optimization = read_toml(optimization_config)
    symbol_risk_file = configured_symbol_risk_file(root, optimization)
    rank_args, round_trip_bps = ranking_cli_args(root)

    steps: list[dict[str, Any]] = []

    def call(name: str, command: list[str | pathlib.Path], check: bool = True) -> int:
        steps.append({"name": name, "command": [str(part) for part in command], "check": check})
        if options.dry_run:
            print(f"-> dry-run {name}: {shell_quote_command(command)}")
            return 0
        return runner(name, command, root, check)

    if options.skip_fetch:
        if not snapshot_file.exists():
            raise SystemExit(f"Missing snapshot file with --skip-fetch: {snapshot_file}")
    elif options.force_snapshot or not snapshot_file.exists():
        call(
            "fetch_trade_snapshot",
            [
                options.python_bin,
                script_path(root, "fetch_investment_data.py"),
                "--date",
                options.date,
                "--watchlist",
                trade_universe_config,
                "--output-file",
                snapshot_file,
            ],
        )

    if not options.skip_fetch and not options.skip_radar_fetch and radar_snapshot_file != snapshot_file and (options.force_snapshot or not radar_snapshot_file.exists()):
        call(
            "fetch_radar_snapshot",
            [
                options.python_bin,
                script_path(root, "fetch_investment_data.py"),
                "--date",
                options.date,
                "--watchlist",
                radar_config,
                "--output-file",
                radar_snapshot_file,
            ],
        )

    call(
        "build_snapshot_registry",
        [options.python_bin, script_path(root, "build_snapshot_registry.py"), "--snapshot-dir", root / "data" / "snapshots", "--output", registry_file],
    )

    if options.run_optimization and optimization_config.exists():
        call(
            "optimize_params",
            [options.python_bin, script_path(root, "optimize_investment_params.py"), "--config", optimization_config, "--as-of-date", options.date, "--session", options.session],
        )

    latest_evaluation = root / "research" / "evaluations" / "latest.json"
    if not options.skip_symbol_risk and latest_evaluation.exists():
        call(
            "build_symbol_risk_memory",
            [
                options.python_bin,
                script_path(root, "build_symbol_risk_memory.py"),
                "--latest-json",
                latest_evaluation,
                "--output",
                symbol_risk_file,
                "--as-of-date",
                options.date,
            ],
            check=False,
        )

    rank_command: list[str | pathlib.Path] = [
        options.python_bin,
        script_path(root, "rank_investment_universe.py"),
        "--snapshot",
        snapshot_file,
        "--output",
        ranking_file,
        "--strategy-config",
        active_strategy_file,
        *rank_args,
    ]
    if symbol_risk_file.exists():
        rank_command.extend(["--symbol-risk-json", symbol_risk_file])
    call("rank_universe", rank_command)

    call(
        "log_shadow",
        [
            options.python_bin,
            script_path(root, "log_investment_shadow.py"),
            "--ranking",
            ranking_file,
            "--snapshot",
            snapshot_file,
            "--date",
            options.date,
            "--session",
            options.session,
            "--output",
            shadow_file,
            "--evidence-mode",
            evidence_mode,
        ],
    )

    if options.evaluate_shadow:
        eval_json = root / "research" / "shadow" / ("latest_replay_evaluation.json" if options.include_replay else "latest_forward_evaluation.json")
        eval_md = root / "research" / "shadow" / ("latest_replay_evaluation.md" if options.include_replay else "latest_forward_evaluation.md")
        eval_command: list[str | pathlib.Path] = [
            options.python_bin,
            script_path(root, "evaluate_investment_shadow.py"),
            "--shadow-dir",
            root / "research" / "shadow",
            "--registry",
            registry_file,
            "--output-json",
            eval_json,
            "--output-md",
            eval_md,
            "--round-trip-bps",
            str(round_trip_bps),
            "--min-forward-shadow-days",
            str(options.min_forward_shadow_days),
            "--as-of-date",
            options.date,
        ]
        if options.include_replay:
            eval_command.append("--include-replay")
        call("evaluate_shadow", eval_command)

    if options.build_evidence_ledger:
        call(
            "build_evidence_ledger",
            [
                options.python_bin,
                script_path(root, "build_investment_evidence_ledger.py"),
                "--shadow-dir",
                root / "research" / "shadow",
                "--registry",
                registry_file,
                "--round-trip-bps",
                str(round_trip_bps),
                "--min-forward-shadow-days",
                str(options.min_forward_shadow_days),
                "--as-of-date",
                options.date,
            ],
        )

    if options.build_calibration_scorecard:
        call(
            "build_calibration_scorecard",
            [
                options.python_bin,
                script_path(root, "build_investment_calibration_scorecard.py"),
                "--calls-dir",
                root / "research" / "calls",
                "--snapshot-dir",
                root / "data" / "snapshots",
                "--shadow-dir",
                root / "research" / "shadow",
                "--registry",
                registry_file,
                "--as-of-date",
                options.date,
                "--as-of-session",
                options.session,
            ],
        )

    variant_competition_id = shadow_variant_competition_id(root)
    variant_competition_file = root / "research" / "shadow_variants" / variant_competition_id / "latest_variant_competition.json"
    if options.run_variant_competition:
        call(
            "run_shadow_variants",
            [
                options.python_bin,
                script_path(root, "run_investment_shadow_variants.py"),
                "--config",
                root / "config" / "shadow_variants.toml",
                "--ranking",
                ranking_file,
                "--snapshot",
                snapshot_file,
                "--registry",
                registry_file,
                "--output-dir",
                root / "research" / "shadow_variants",
                "--date",
                options.date,
                "--session",
                options.session,
                "--evidence-mode",
                evidence_mode,
                "--as-of-date",
                options.date,
                "--round-trip-bps",
                str(round_trip_bps),
            ],
        )

    if options.build_close_report and options.session == "close" and (options.dry_run or calls_file.exists()):
        call(
            "build_chinese_close_report",
            [
                options.python_bin,
                script_path(root, "build_chinese_daily_close_report.py"),
                "--date",
                options.date,
                "--session",
                options.session,
                "--calls",
                calls_file,
                "--ranking",
                ranking_file,
                "--risk-review",
                risk_review_file,
                "--evidence-ledger",
                root / "research" / "shadow" / "latest_evidence_ledger.json",
                "--calibration-scorecard",
                root / "research" / "evaluations" / "latest_calibration_scorecard.json",
                "--forward-evaluation",
                root / "research" / "shadow" / "latest_forward_evaluation.json",
                "--variant-competition",
                variant_competition_file,
                "--output-dir",
                root / "research" / "products" / "daily_close",
            ],
        )

    summary = {
        "generated_at": utc_now(),
        "date": options.date,
        "session": options.session,
        "evidence_mode": evidence_mode,
        "dry_run": options.dry_run,
        "paths": {
            "snapshot": str(snapshot_file),
            "radar_snapshot": str(radar_snapshot_file),
            "registry": str(registry_file),
            "ranking": str(ranking_file),
            "shadow": str(shadow_file),
            "shadow_variants": str(root / "research" / "shadow_variants"),
            "close_report": str(root / "research" / "products" / "daily_close" / f"{close_report_stem(options.date, options.session)}-close-report.md"),
            "symbol_risk_memory": str(symbol_risk_file),
        },
        "steps": steps,
    }
    summary_output = resolve_path(root, options.summary_output)
    if summary_output:
        summary_output.parent.mkdir(parents=True, exist_ok=True)
        summary_output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> DailyShadowOptions:
    parser = argparse.ArgumentParser(description="Run the deterministic investment snapshot -> ranking -> shadow evaluation pipeline without requiring bash.")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--python-bin", default=sys.executable)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--session", default="close", choices=sorted(VALID_SESSIONS))
    parser.add_argument("--snapshot-file", default=None)
    parser.add_argument("--radar-snapshot-file", default=None)
    parser.add_argument("--ranking-file", default=None)
    parser.add_argument("--shadow-file", default=None)
    parser.add_argument("--shadow-evidence-mode", choices=["forward_shadow", "historical_replay"], default=None)
    parser.add_argument("--force-snapshot", action="store_true")
    parser.add_argument("--skip-fetch", action="store_true", help="Use an existing trade snapshot instead of fetching quotes.")
    parser.add_argument("--skip-radar-fetch", action="store_true")
    parser.add_argument("--skip-symbol-risk", action="store_true")
    parser.add_argument("--run-optimization", action="store_true", help="Opt in to active-strategy optimization before ranking.")
    parser.add_argument("--skip-evaluation", action="store_true")
    parser.add_argument("--skip-evidence-ledger", action="store_true")
    parser.add_argument("--skip-calibration-scorecard", action="store_true")
    parser.add_argument("--skip-variant-competition", action="store_true")
    parser.add_argument("--skip-close-report", action="store_true")
    parser.add_argument("--calls-file", default=None)
    parser.add_argument("--risk-review-file", default=None)
    parser.add_argument("--include-replay", action="store_true", help="Diagnostic only: include historical replay logs in the shadow evaluation output.")
    parser.add_argument("--min-forward-shadow-days", type=int, default=20)
    parser.add_argument("--summary-output", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    return DailyShadowOptions(
        root=root,
        python_bin=args.python_bin,
        date=args.date,
        session=args.session,
        snapshot_file=resolve_path(root, args.snapshot_file),
        radar_snapshot_file=resolve_path(root, args.radar_snapshot_file),
        ranking_file=resolve_path(root, args.ranking_file),
        shadow_file=resolve_path(root, args.shadow_file),
        evidence_mode=args.shadow_evidence_mode,
        force_snapshot=args.force_snapshot,
        skip_fetch=args.skip_fetch,
        skip_radar_fetch=args.skip_radar_fetch,
        skip_symbol_risk=args.skip_symbol_risk,
        run_optimization=args.run_optimization,
        evaluate_shadow=not args.skip_evaluation,
        build_evidence_ledger=not args.skip_evidence_ledger,
        build_calibration_scorecard=not args.skip_calibration_scorecard,
        run_variant_competition=not args.skip_variant_competition,
        build_close_report=not args.skip_close_report,
        calls_file=resolve_path(root, args.calls_file),
        risk_review_file=resolve_path(root, args.risk_review_file),
        include_replay=args.include_replay,
        min_forward_shadow_days=args.min_forward_shadow_days,
        summary_output=resolve_path(root, args.summary_output),
        dry_run=args.dry_run,
    )


def main() -> int:
    summary = run_pipeline(parse_args())
    print(json.dumps({key: summary[key] for key in ["date", "session", "evidence_mode", "paths"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
