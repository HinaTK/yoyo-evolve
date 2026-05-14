#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import math
import pathlib
import statistics
import sys
from collections import Counter, defaultdict
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from evaluate_investment_calls import BEARISH_STATES, BULLISH_STATES, evaluate_calls, parse_date  # noqa: E402
from evaluate_investment_shadow import build_evaluation  # noqa: E402


CONFIDENCE_BUCKETS = [
    (0.0, 0.4, "0.00-0.40"),
    (0.4, 0.55, "0.40-0.55"),
    (0.55, 0.7, "0.55-0.70"),
    (0.7, 0.85, "0.70-0.85"),
    (0.85, 1.01, "0.85-1.00"),
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def confidence_bucket(value: float | None) -> str:
    if value is None:
        return "unknown"
    for low, high, label in CONFIDENCE_BUCKETS:
        if low <= value < high:
            return label
    return "unknown"


def success_for_call_record(record: dict[str, Any]) -> float | None:
    verdict = record.get("verdict")
    if verdict == "pass":
        return 1.0
    if verdict == "fail":
        return 0.0
    if verdict == "mixed":
        return 0.5
    return None


def confidence_for_shadow_record(record: dict[str, Any]) -> float | None:
    _ = record
    # Shadow records do not yet store an ex-ante confidence, so use a fixed
    # research-only prior instead of future outcome fields.
    return 0.65


def success_for_shadow_record(record: dict[str, Any]) -> float | None:
    net_return = as_float(record.get("net_return_pct"))
    adverse_breach = record.get("adverse_breach") is True
    if net_return is None:
        return None
    if adverse_breach:
        return 0.0
    if net_return > 0:
        return 1.0
    if net_return < 0:
        return 0.0
    return 0.5


def summarize_values(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"avg": None, "median": None, "min": None, "max": None}
    return {
        "avg": round(statistics.fmean(values), 3),
        "median": round(statistics.median(values), 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
    }


def build_bucket_stats(rows: list[dict[str, Any]], min_bucket_samples: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["confidence_bucket"]].append(row)

    stats = []
    for bucket in [label for *_bounds, label in CONFIDENCE_BUCKETS] + ["unknown"]:
        bucket_rows = grouped.get(bucket, [])
        scored_rows = [row for row in bucket_rows if row.get("confidence") is not None and row.get("success") is not None]
        successes = [row["success"] for row in scored_rows]
        confidences = [row["confidence"] for row in scored_rows]
        returns = [row["return_pct"] for row in bucket_rows if row.get("return_pct") is not None]
        if successes:
            hit_rate = statistics.fmean(successes)
            avg_confidence = statistics.fmean(confidences) if confidences else None
            calibration_error = abs(hit_rate - avg_confidence) if avg_confidence is not None else None
            brier = statistics.fmean((float(row["confidence"]) - float(row["success"])) ** 2 for row in scored_rows)
        else:
            hit_rate = None
            avg_confidence = None
            calibration_error = None
            brier = None
        stats.append(
            {
                "bucket": bucket,
                "sample_count": len(bucket_rows),
                "scored_sample_count": len(successes),
                "low_sample": len(successes) < min_bucket_samples,
                "avg_confidence": round(avg_confidence, 3) if avg_confidence is not None else None,
                "hit_rate": round(hit_rate, 3) if hit_rate is not None else None,
                "calibration_error": round(calibration_error, 3) if calibration_error is not None else None,
                "brier_score": round(brier, 3) if brier is not None else None,
                "return_stats": summarize_values(returns),
            }
        )
    return stats


def call_rows(evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for record in evaluations:
        success = success_for_call_record(record)
        confidence = as_float(record.get("confidence"))
        rows.append(
            {
                "source": "calls",
                "date": record.get("call_date"),
                "session": record.get("session"),
                "symbol": record.get("symbol"),
                "state": record.get("state"),
                "theme": record.get("theme"),
                "window_days": record.get("window_days"),
                "confidence": confidence,
                "confidence_bucket": confidence_bucket(confidence),
                "success": success,
                "return_pct": as_float(record.get("return_pct")),
                "verdict": record.get("verdict"),
                "learning_tag": record.get("learning_tag"),
            }
        )
    return rows


def shadow_rows(evaluation: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for record in evaluation.get("records", []):
        if record.get("counts_toward_forward_evidence") is not True:
            continue
        confidence = confidence_for_shadow_record(record)
        rows.append(
            {
                "source": "shadow",
                "date": record.get("base_date"),
                "session": "shadow",
                "symbol": record.get("symbol"),
                "state": "shadow_actionable",
                "theme": record.get("theme"),
                "window_days": None,
                "confidence": confidence,
                "confidence_bucket": confidence_bucket(confidence),
                "success": success_for_shadow_record(record),
                "return_pct": as_float(record.get("net_return_pct")),
                "verdict": None,
                "learning_tag": "adverse_breach" if record.get("adverse_breach") else None,
                "alpha_pct": record.get("alpha_pct"),
                "max_adverse_pct": record.get("max_adverse_pct"),
                "shadow_log": record.get("shadow_log"),
            }
        )
    return rows


def overall_stats(rows: list[dict[str, Any]], min_total_samples: int) -> dict[str, Any]:
    scored_rows = [row for row in rows if row.get("confidence") is not None and row.get("success") is not None]
    successes = [row["success"] for row in scored_rows]
    confidences = [row["confidence"] for row in scored_rows]
    returns = [row["return_pct"] for row in rows if row.get("return_pct") is not None]
    if successes:
        hit_rate = statistics.fmean(successes)
        avg_confidence = statistics.fmean(confidences) if confidences else None
        calibration_error = abs(hit_rate - avg_confidence) if avg_confidence is not None else None
        brier = statistics.fmean((float(row["confidence"]) - float(row["success"])) ** 2 for row in scored_rows)
    else:
        hit_rate = None
        avg_confidence = None
        calibration_error = None
        brier = None
    return {
        "sample_count": len(rows),
        "scored_sample_count": len(successes),
        "low_sample": len(successes) < min_total_samples,
        "avg_confidence": round(avg_confidence, 3) if avg_confidence is not None else None,
        "hit_rate": round(hit_rate, 3) if hit_rate is not None else None,
        "calibration_error": round(calibration_error, 3) if calibration_error is not None else None,
        "brier_score": round(brier, 3) if brier is not None else None,
        "return_stats": summarize_values(returns),
    }


def group_counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        value = row.get(key)
        if value:
            counts[str(value)] += 1
    return dict(sorted(counts.items()))


def build_scorecard(
    calls_dir: pathlib.Path,
    snapshot_dir: pathlib.Path,
    shadow_dir: pathlib.Path,
    registry_path: pathlib.Path,
    close_windows: list[int],
    intraday_windows: list[int],
    as_of_date: dt.date | None = None,
    as_of_session: str | None = None,
    min_total_samples: int = 30,
    min_bucket_samples: int = 5,
) -> dict[str, Any]:
    evaluations, call_summary = evaluate_calls(calls_dir, snapshot_dir, close_windows, intraday_windows, as_of_date, as_of_session)
    shadow_evaluation = build_evaluation(shadow_dir, registry_path, include_replay=False, as_of_date=as_of_date)
    rows = call_rows(evaluations) + shadow_rows(shadow_evaluation)
    findings = []
    overall = overall_stats(rows, min_total_samples)
    if overall["low_sample"]:
        findings.append({"metric": "scored_sample_count", "actual": overall["scored_sample_count"], "expected": f">= {min_total_samples}", "severity": "info"})
    for bucket in build_bucket_stats(rows, min_bucket_samples):
        if bucket["low_sample"] and bucket["scored_sample_count"] > 0:
            findings.append({"metric": f"bucket:{bucket['bucket']}", "actual": bucket["scored_sample_count"], "expected": f">= {min_bucket_samples}", "severity": "info"})

    return {
        "generated_at": utc_now(),
        "as_of_date": as_of_date.isoformat() if as_of_date else None,
        "as_of_session": as_of_session,
        "inputs": {
            "calls_dir": str(calls_dir),
            "snapshot_dir": str(snapshot_dir),
            "shadow_dir": str(shadow_dir),
            "registry": str(registry_path),
            "close_windows": close_windows,
            "intraday_windows": intraday_windows,
        },
        "thresholds": {"min_total_samples": min_total_samples, "min_bucket_samples": min_bucket_samples},
        "summary": {
            "call_record_count": len(evaluations),
            "shadow_record_count": len(shadow_rows(shadow_evaluation)),
            "combined_record_count": len(rows),
            "call_summary": call_summary,
            "shadow_summary": shadow_evaluation.get("summary", {}),
            "source_counts": group_counts(rows, "source"),
            "learning_counts": group_counts(rows, "learning_tag"),
        },
        "overall": overall,
        "confidence_buckets": build_bucket_stats(rows, min_bucket_samples),
        "findings": findings,
        "recent_records": rows[-50:],
    }


def write_markdown(path: pathlib.Path, scorecard: dict[str, Any]) -> None:
    overall = scorecard["overall"]
    lines = [
        "# Recommendation Calibration Scorecard",
        "",
        f"Generated: `{scorecard['generated_at']}`",
        f"As-of: date=`{scorecard.get('as_of_date') or 'null'}`, session=`{scorecard.get('as_of_session') or 'null'}`",
        "",
        "## Overall",
        f"- scored samples: `{overall['scored_sample_count']}`",
        f"- low sample: `{overall['low_sample']}`",
        f"- avg confidence: `{overall['avg_confidence']}`",
        f"- hit rate: `{overall['hit_rate']}`",
        f"- calibration error: `{overall['calibration_error']}`",
        f"- brier score: `{overall['brier_score']}`",
        f"- avg return: `{overall['return_stats']['avg']}`%",
        "",
        "## Confidence Buckets",
    ]
    for bucket in scorecard["confidence_buckets"]:
        lines.append(
            f"- `{bucket['bucket']}`: scored={bucket['scored_sample_count']}, low_sample={bucket['low_sample']}, "
            f"avg_conf={bucket['avg_confidence']}, hit={bucket['hit_rate']}, err={bucket['calibration_error']}, brier={bucket['brier_score']}"
        )

    lines.extend(["", "## Findings"])
    if scorecard["findings"]:
        for finding in scorecard["findings"]:
            lines.append(f"- `{finding['severity']}` `{finding['metric']}` actual `{finding['actual']}`, expected `{finding['expected']}`")
    else:
        lines.append("- no calibration findings")

    lines.extend(["", "## Recent Records"])
    for row in scorecard["recent_records"][-20:]:
        lines.append(
            f"- `{row['source']}` `{row['date']}` `{row['symbol']}` conf={row.get('confidence')} bucket=`{row['confidence_bucket']}` "
            f"success={row.get('success')} return={row.get('return_pct')} verdict={row.get('verdict')} learning={row.get('learning_tag')}"
        )
    if not scorecard["recent_records"]:
        lines.append("- no scored records yet")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a confidence calibration scorecard for investment recommendations and shadow records.")
    parser.add_argument("--calls-dir", default=str(ROOT / "research" / "calls"))
    parser.add_argument("--snapshot-dir", default=str(ROOT / "data" / "snapshots"))
    parser.add_argument("--shadow-dir", default=str(ROOT / "research" / "shadow"))
    parser.add_argument("--registry", default=str(ROOT / "data" / "snapshots" / "registry.json"))
    parser.add_argument("--output-json", default=str(ROOT / "research" / "evaluations" / "latest_calibration_scorecard.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "evaluations" / "latest_calibration_scorecard.md"))
    parser.add_argument("--windows", nargs="+", type=int, default=[3, 5, 10, 20])
    parser.add_argument("--intraday-windows", nargs="+", type=int, default=[0, 1, 3])
    parser.add_argument("--as-of-date", default=None)
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--min-total-samples", type=int, default=30)
    parser.add_argument("--min-bucket-samples", type=int, default=5)
    args = parser.parse_args()

    as_of_date = parse_date(args.as_of_date) if args.as_of_date else None
    scorecard = build_scorecard(
        pathlib.Path(args.calls_dir),
        pathlib.Path(args.snapshot_dir),
        pathlib.Path(args.shadow_dir),
        pathlib.Path(args.registry),
        args.windows,
        args.intraday_windows,
        as_of_date,
        args.as_of_session,
        args.min_total_samples,
        args.min_bucket_samples,
    )
    output_json = pathlib.Path(args.output_json)
    output_md = pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    write_markdown(output_md, scorecard)
    print(json.dumps(scorecard["overall"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
