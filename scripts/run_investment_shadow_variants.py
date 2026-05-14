#!/usr/bin/env python3

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import statistics
import sys
import tomllib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from backtest_investment_strategy import EXPERIMENTAL_EXIT_RULES, EXPERIMENTAL_RISK_FILTERS, load_json, registry_entries  # noqa: E402
from evaluate_investment_shadow import as_float, outcome_for_candidate, parse_date, performance_summary  # noqa: E402
from log_investment_shadow import DEFAULT_SHADOW_HORIZON_DAYS, build_shadow_log, file_metadata  # noqa: E402


DEFAULT_CONFIG = ROOT / "config" / "shadow_variants.toml"
DEFAULT_OUTPUT_DIR = ROOT / "research" / "shadow_variants"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_toml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def sha256_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def resolve_path(value: str | pathlib.Path | None, root: pathlib.Path = ROOT) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else root / path


def validate_variant(raw: dict[str, Any]) -> dict[str, Any]:
    variant_id = str(raw.get("id") or "").strip()
    if not variant_id:
        raise ValueError("variant id is required")
    risk_filter = str(raw.get("risk_filter") or "off")
    exit_rule = str(raw.get("exit_rule") or "off")
    if risk_filter not in EXPERIMENTAL_RISK_FILTERS:
        raise ValueError(f"variant {variant_id}: invalid risk_filter {risk_filter!r}")
    if exit_rule not in EXPERIMENTAL_EXIT_RULES:
        raise ValueError(f"variant {variant_id}: invalid exit_rule {exit_rule!r}")
    stop_loss_pct = float(raw.get("stop_loss_pct", -4.0))
    if exit_rule != "off" and stop_loss_pct >= 0:
        raise ValueError(f"variant {variant_id}: stop_loss_pct must be negative")
    horizon_days = int(raw.get("horizon_days") or DEFAULT_SHADOW_HORIZON_DAYS)
    if horizon_days <= 0:
        raise ValueError(f"variant {variant_id}: horizon_days must be positive")
    return {
        "id": variant_id,
        "label": str(raw.get("label") or variant_id),
        "risk_filter": risk_filter,
        "exit_rule": exit_rule,
        "stop_loss_pct": stop_loss_pct,
        "horizon_days": horizon_days,
    }


def load_variant_config(path: pathlib.Path) -> dict[str, Any]:
    data = read_toml(path)
    variants = [validate_variant(row) for row in data.get("variant", []) if isinstance(row, dict)]
    ids = [variant["id"] for variant in variants]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        raise ValueError(f"duplicate variant ids: {duplicates}")
    if not variants:
        raise ValueError("at least one shadow variant is required")
    return {
        "enabled": bool(data.get("enabled", True)),
        "competition_id": str(data.get("competition_id") or "shadow_variants"),
        "min_forward_shadow_days": int(data.get("min_forward_shadow_days") or 20),
        "variants": variants,
        "config_sha256": sha256_json(data),
    }


def variant_log_path(output_dir: pathlib.Path, competition_id: str, date: str, session: str, variant_id: str) -> pathlib.Path:
    return output_dir / competition_id / "logs" / f"{date}-{session}-{variant_id}-shadow.json"


def build_variant_log(
    ranking: dict[str, Any],
    ranking_path: pathlib.Path,
    snapshot_path: pathlib.Path | None,
    date: str,
    session: str,
    competition_id: str,
    config_sha256: str,
    variant: dict[str, Any],
    evidence_mode: str,
) -> dict[str, Any]:
    log = build_shadow_log(
        ranking,
        ranking_path=ranking_path,
        snapshot_path=snapshot_path,
        date=date,
        session=session,
        risk_filter=variant["risk_filter"],
        exit_rule=variant["exit_rule"],
        stop_loss_pct=float(variant["stop_loss_pct"]),
        horizon_days=int(variant["horizon_days"]),
        evidence_mode=evidence_mode,
    )
    log["mode"] = "shadow_variant_competition"
    log["counts_toward_forward_evidence"] = False
    log["shadow_policy"].update(
        {
            "status": "variant_shadow_only",
            "variant_id": variant["id"],
            "variant_label": variant["label"],
            "competition_id": competition_id,
            "config_sha256": config_sha256,
            "counts_toward_forward_evidence": False,
            "readiness_gate_excluded": True,
        }
    )
    log["variant"] = variant | {"config_sha256": config_sha256, "competition_id": competition_id}
    return log


def discover_variant_logs(output_dir: pathlib.Path, competition_id: str) -> list[tuple[pathlib.Path, dict[str, Any]]]:
    logs = []
    for path in sorted((output_dir / competition_id / "logs").glob("*-shadow.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and data.get("mode") == "shadow_variant_competition":
            logs.append((path, data))
    return logs


def summarize_variant_logs(
    logs: list[tuple[pathlib.Path, dict[str, Any]]],
    registry_path: pathlib.Path,
    as_of_date: dt.date | None,
    round_trip_bps: float,
    max_adverse_limit_pct: float = -8.0,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entries = registry_entries(load_json(registry_path), "trade") if registry_path.exists() else []
    if as_of_date is not None:
        entries = [entry for entry in entries if entry.get("_date") <= as_of_date]
    records_by_variant: dict[str, list[dict[str, Any]]] = {}
    rows: dict[str, dict[str, Any]] = {}
    skipped: list[dict[str, Any]] = []

    for path, log in logs:
        policy = log.get("shadow_policy") if isinstance(log.get("shadow_policy"), dict) else {}
        variant_id = str(policy.get("variant_id") or "unknown")
        row = rows.setdefault(
            variant_id,
            {
                "variant_id": variant_id,
                "variant_label": policy.get("variant_label") or variant_id,
                "competition_id": policy.get("competition_id"),
                "risk_filter": policy.get("risk_filter"),
                "exit_rule": policy.get("exit_rule"),
                "stop_loss_pct": policy.get("stop_loss_pct"),
                "horizon_days": policy.get("horizon_days"),
                "config_sha256": policy.get("config_sha256"),
                "log_count": 0,
                "forward_like_log_count": 0,
                "matured_forward_days": 0,
                "no_execution_audit_passed": True,
            },
        )
        date_text = str(log.get("date") or "")
        try:
            base_date = parse_date(date_text)
        except ValueError:
            skipped.append({"path": str(path), "variant_id": variant_id, "reason": "invalid_shadow_date"})
            continue
        if as_of_date is not None and base_date > as_of_date:
            skipped.append({"path": str(path), "variant_id": variant_id, "reason": "shadow_date_after_as_of"})
            continue

        row["log_count"] += 1
        if log.get("evidence_mode") == "forward_shadow":
            row["forward_like_log_count"] += 1
        if not (policy.get("no_execution") is True and policy.get("no_portfolio_mutation") is True and policy.get("production_ranking_unchanged") is True):
            row["no_execution_audit_passed"] = False
        horizon_days = int(policy.get("horizon_days") or DEFAULT_SHADOW_HORIZON_DAYS)
        matured = False
        for candidate in log.get("shadow_actionable_candidates", []) if isinstance(log.get("shadow_actionable_candidates"), list) else []:
            record, pending = outcome_for_candidate(candidate, base_date, entries, horizon_days, round_trip_bps, max_adverse_limit_pct)
            if record is not None:
                matured = True
                record["variant_id"] = variant_id
                record["shadow_log"] = str(path)
                records_by_variant.setdefault(variant_id, []).append(record)
            elif pending is not None:
                skipped.append({"path": str(path), "variant_id": variant_id, "reason": pending.get("reason"), "symbol": pending.get("symbol")})
        if matured:
            row["matured_forward_days"] += 1

    scoreboard = []
    for variant_id, row in rows.items():
        records = records_by_variant.get(variant_id, [])
        stats = performance_summary(records)
        returns = [value for value in (as_float(record.get("net_return_pct")) for record in records) if value is not None]
        row.update(stats)
        row["avg_net_return_pct"] = stats.get("avg_net_return_pct")
        row["sample_count"] = len(records)
        row["scoreboard_note"] = "insufficient_forward_samples" if len(records) < 20 else "diagnostic_only_no_promotion"
        row["pareto_rank_key"] = [
            0 if row["no_execution_audit_passed"] else 1,
            -(stats.get("avg_alpha_pct") or -999),
            stats.get("adverse_breach_rate") if stats.get("adverse_breach_rate") is not None else 999,
            -(statistics.fmean(returns) if returns else -999),
        ]
        scoreboard.append(row)
    scoreboard.sort(key=lambda row: row["pareto_rank_key"])
    for index, row in enumerate(scoreboard, start=1):
        row["diagnostic_rank"] = index
        row.pop("pareto_rank_key", None)
    return scoreboard, skipped


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Shadow Variant Competition",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Competition: `{result['competition_id']}`",
        f"As of: `{result.get('as_of_date')}`",
        "",
        "This is shadow-only research. It does not promote a strategy, execute orders, or mutate a portfolio.",
        "",
        "## Variants",
    ]
    for row in result["scoreboard"]:
        lines.append(
            f"- #{row['diagnostic_rank']} `{row['variant_id']}` logs={row['log_count']} samples={row.get('sample_count')} avg_net={row.get('avg_net_return_pct')} alpha={row.get('avg_alpha_pct')} adverse_breach={row.get('adverse_breach_rate')} audit={row.get('no_execution_audit_passed')}"
        )
    if result.get("skipped"):
        lines.extend(["", "## Skipped/Pending", f"- count: `{len(result['skipped'])}`"])
    return "\n".join(lines) + "\n"


def run_competition(
    config_path: pathlib.Path,
    ranking_path: pathlib.Path,
    snapshot_path: pathlib.Path | None,
    registry_path: pathlib.Path,
    output_dir: pathlib.Path,
    date: str | None,
    session: str | None,
    evidence_mode: str,
    as_of_date: dt.date | None,
    round_trip_bps: float,
    dry_run: bool = False,
) -> dict[str, Any]:
    config = load_variant_config(config_path)
    ranking = load_json(ranking_path)
    run_date = date or str(ranking.get("as_of_date") or dt.date.today().isoformat())
    run_session = session or str(ranking.get("as_of_session") or ranking.get("session") or "unknown")
    written: list[dict[str, Any]] = []
    if config["enabled"]:
        for variant in config["variants"]:
            path = variant_log_path(output_dir, config["competition_id"], run_date, run_session, variant["id"])
            written.append({"variant_id": variant["id"], "path": str(path), "dry_run": dry_run})
            if dry_run:
                continue
            log = build_variant_log(ranking, ranking_path, snapshot_path, run_date, run_session, config["competition_id"], config["config_sha256"], variant, evidence_mode)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(log, indent=2), encoding="utf-8")

    logs = discover_variant_logs(output_dir, config["competition_id"])
    if not dry_run:
        logs.extend((pathlib.Path(item["path"]), json.loads(pathlib.Path(item["path"]).read_text(encoding="utf-8"))) for item in written if pathlib.Path(item["path"]).exists())
        unique: dict[str, tuple[pathlib.Path, dict[str, Any]]] = {str(path): (path, log) for path, log in logs}
        logs = list(unique.values())
    scoreboard, skipped = summarize_variant_logs(logs, registry_path, as_of_date, round_trip_bps)
    result = {
        "generated_at": utc_now(),
        "competition_id": config["competition_id"],
        "config": file_metadata(config_path),
        "config_sha256": config["config_sha256"],
        "ranking": file_metadata(ranking_path),
        "snapshot": file_metadata(snapshot_path) if snapshot_path else None,
        "registry": file_metadata(registry_path),
        "date": run_date,
        "session": run_session,
        "as_of_date": as_of_date.isoformat() if as_of_date else None,
        "evidence_mode": evidence_mode,
        "dry_run": dry_run,
        "policy": {
            "mode": "shadow_variant_competition",
            "no_execution": True,
            "no_portfolio_mutation": True,
            "production_ranking_unchanged": True,
            "counts_toward_forward_evidence": False,
            "auto_promotion_enabled": False,
        },
        "written_logs": written,
        "scoreboard": scoreboard,
        "skipped": skipped,
    }
    if not dry_run:
        out_dir = output_dir / config["competition_id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "latest_variant_competition.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        (out_dir / "latest_variant_competition.md").write_text(render_markdown(result), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run shadow-only investment variant competition without strategy promotion.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--registry", default=str(ROOT / "data" / "snapshots" / "registry.json"))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--date", default=None)
    parser.add_argument("--session", default=None)
    parser.add_argument("--evidence-mode", choices=["forward_shadow", "historical_replay"], default="forward_shadow")
    parser.add_argument("--as-of-date", default=None)
    parser.add_argument("--round-trip-bps", type=float, default=35.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = run_competition(
        resolve_path(args.config) or DEFAULT_CONFIG,
        resolve_path(args.ranking) or pathlib.Path(args.ranking),
        resolve_path(args.snapshot) if args.snapshot else None,
        resolve_path(args.registry) or pathlib.Path(args.registry),
        resolve_path(args.output_dir) or DEFAULT_OUTPUT_DIR,
        args.date,
        args.session,
        args.evidence_mode,
        parse_date(args.as_of_date) if args.as_of_date else None,
        args.round_trip_bps,
        args.dry_run,
    )
    print(json.dumps({"competition_id": result["competition_id"], "dry_run": result["dry_run"], "written_logs": result["written_logs"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
