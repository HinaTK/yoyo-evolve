#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess
from dataclasses import dataclass
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback is intentionally minimal.
    tomllib = None


ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "research" / "experiments" / "system_changes"

FALSE_LOCKS = {
    "recommendation_only": "recommendation_only must stay enabled",
    "research_only": "research_only must stay enabled",
}
FINAL_TRUE_INVARIANTS = {
    "forbid_automatic_trading",
    "forbid_cost_gate_reduction",
    "forbid_edge_gate_reduction",
    "forbid_history_tampering",
    "forbid_snapshot_mutation",
    "research_only",
}
NUMERIC_FLOORS = {
    "estimated_round_trip_bps",
    "minimum_edge_bps",
    "require_edge_over_cost_multiple",
}
NUMERIC_CEILINGS = {
    "max_single_position_pct",
    "max_theme_exposure_pct",
}
ANTI_LEAKAGE_FIELDS = ("future", "as_of", "as-of")
LOGIC_GUARDS = ("cost", "net_return", "benchmark", "evaluation", "evaluate")
TRADING_TERMS = [
    "br" + "oker",
    "br" + "okerage",
    "br" + "okerage_api",
    "interactive_" + "br" + "okers",
    "or" + "der_router",
    "place_" + "trade",
    "place_" + "or" + "der",
    "send_" + "or" + "der",
    "execute_buy",
    "execute_sell",
    "execution_enabled",
    "trade_execution",
    "trade_execution_enabled",
]


@dataclass
class DiffLine:
    path: str
    marker: str
    text: str


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_git(repo: pathlib.Path, args: list[str]) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def git_diff(repo: pathlib.Path, base_ref: str | None) -> tuple[list[str], str, list[str]]:
    if base_ref:
        names = run_git(repo, ["diff", "--name-only", base_ref, "--"]).splitlines()
        diff = run_git(repo, ["diff", "--unified=0", base_ref, "--"])
    else:
        names = []
        chunks = []
        for extra in ([], ["--cached"]):
            names.extend(run_git(repo, ["diff", "--name-only", *extra, "--"]).splitlines())
            chunks.append(run_git(repo, ["diff", "--unified=0", *extra, "--"]))
        diff = "\n".join(chunk for chunk in chunks if chunk)
    untracked = run_git(repo, ["ls-files", "--others", "--exclude-standard"]).splitlines()
    all_names = sorted({name.replace("\\", "/") for name in [*names, *untracked] if name})
    return all_names, diff, [name.replace("\\", "/") for name in untracked]


def parse_diff(diff_text: str) -> list[DiffLine]:
    current = ""
    lines: list[DiffLine] = []
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            target = raw[4:].strip()
            if target.startswith("b/"):
                target = target[2:]
            if target != "/dev/null":
                current = target.replace("\\", "/")
            continue
        if raw.startswith("--- "):
            continue
        if not current:
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            lines.append(DiffLine(current, "+", raw[1:]))
        elif raw.startswith("-") and not raw.startswith("---"):
            lines.append(DiffLine(current, "-", raw[1:]))
    return lines


def read_untracked_lines(repo: pathlib.Path, paths: list[str]) -> list[DiffLine]:
    out: list[DiffLine] = []
    for rel in paths:
        path = repo / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line in text.splitlines():
            out.append(DiffLine(rel, "+", line))
    return out


def stripped_code(line: str) -> str:
    text = line.strip()
    if text.startswith(("#", "//", "- ")):
        return ""
    return text


def is_logic_file(path: str) -> bool:
    return pathlib.PurePosixPath(path).suffix in {".py", ".sh", ".toml", ".json", ".yaml", ".yml"}


def is_guard_fixture_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return normalized == "scripts/evaluate_investment_system_change.py" or normalized.startswith("tests/")


def removes_named_guard(line: str) -> bool:
    return re.search(r"\b(?:future|as_of|as-of)[A-Za-z0-9_-]*\b\s*[:=]", line.lower()) is not None


def has_bool_assignment(line: str, key: str, value: str) -> bool:
    pattern = rf"\b{re.escape(key)}\b\s*[:=]\s*{value}\b"
    return re.search(pattern, line.lower()) is not None


def has_enabled_auto_flag(line: str) -> bool:
    return re.search(r"\bautomatic_trading(?:_enabled)?\b\s*[:=]\s*true\b", line.lower()) is not None


def numeric_assignments(lines: list[DiffLine], marker: str) -> dict[str, list[float]]:
    keys = NUMERIC_FLOORS | NUMERIC_CEILINGS
    found: dict[str, list[float]] = {key: [] for key in keys}
    for item in lines:
        if item.marker != marker:
            continue
        text = stripped_code(item.text)
        if not text:
            continue
        for key in keys:
            match = re.search(rf"\b{re.escape(key)}\b\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", text)
            if match:
                found[key].append(float(match.group(1)))
    return found


def load_toml(path: pathlib.Path) -> dict[str, Any]:
    if tomllib is not None:
        return tomllib.loads(path.read_text(encoding="utf-8"))

    data: dict[str, Any] = {}
    current = data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]") and not line.startswith("[["):
            current = data
            for part in line[1:-1].split("."):
                current = current.setdefault(part.strip(), {})
            continue
        if "=" not in line:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        if value.lower() in {"true", "false"}:
            current[key] = value.lower() == "true"
        elif value.startswith('"') and value.endswith('"'):
            current[key] = value[1:-1]
        else:
            current[key] = value
    return data


def final_state_findings(repo: pathlib.Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    config_dir = repo / "config"
    if not config_dir.exists():
        return findings

    def add(path: str, message: str) -> None:
        findings.append({"severity": "fail", "path": path, "rule": "final_state_invariant", "message": message})

    portfolio_path = "config/portfolio.toml"
    path = repo / portfolio_path
    if not path.is_file():
        add(portfolio_path, "portfolio.toml must exist so recommendation-only mode can be verified.")
    else:
        try:
            data = load_toml(path)
            portfolio = data.get("portfolio", data)
            if portfolio.get("mode") != "recommendation_only":
                add(portfolio_path, "portfolio.mode must remain recommendation_only in the final repo state.")
        except Exception as exc:  # noqa: BLE001 - invariant checks should fail closed on malformed config.
            add(portfolio_path, f"Could not parse final portfolio TOML: {exc}")

    for rel in ("config/active_strategy.toml", "config/optimization.toml"):
        path = repo / rel
        if not path.is_file():
            add(rel, f"{rel} must exist so research-only safety invariants can be verified.")
            continue
        try:
            data = load_toml(path)
            invariants = data.get("safety_invariants", {})
            if invariants.get("automatic_trading_enabled") is not False:
                add(rel, "safety_invariants.automatic_trading_enabled must be false in the final repo state.")
            for key in sorted(FINAL_TRUE_INVARIANTS):
                if invariants.get(key) is not True:
                    add(rel, f"safety_invariants.{key} must be true in the final repo state.")
        except Exception as exc:  # noqa: BLE001 - invariant checks should fail closed on malformed config.
            add(rel, f"Could not parse final safety invariant TOML: {exc}")

    return findings


def evaluate_change(repo: pathlib.Path, changed_paths: list[str], diff_text: str, untracked_paths: list[str] | None = None) -> dict[str, Any]:
    lines = parse_diff(diff_text)
    if untracked_paths:
        lines.extend(read_untracked_lines(repo, untracked_paths))
    findings: list[dict[str, Any]] = []
    normalized_paths = [path.replace("\\", "/") for path in changed_paths]

    for path in normalized_paths:
        if path.startswith("data/snapshots/") and pathlib.PurePosixPath(path).name != "registry.json":
            findings.append({"severity": "fail", "path": path, "rule": "snapshot_history_immutable", "message": "Historical snapshot files under data/snapshots must not be changed."})

    removed_values = numeric_assignments(lines, "-")
    added_values = numeric_assignments(lines, "+")
    for key in sorted(NUMERIC_FLOORS):
        if removed_values[key] and added_values[key] and min(added_values[key]) < max(removed_values[key]):
            findings.append({"severity": "fail", "path": None, "rule": "risk_gate_not_lowered", "message": f"{key} decreased from {max(removed_values[key])} to {min(added_values[key])}."})
    for key in sorted(NUMERIC_CEILINGS):
        if removed_values[key] and added_values[key] and max(added_values[key]) > min(removed_values[key]):
            findings.append({"severity": "fail", "path": None, "rule": "risk_limit_not_increased", "message": f"{key} increased from {min(removed_values[key])} to {max(added_values[key])}."})

    for item in lines:
        text = stripped_code(item.text)
        lower = text.lower()
        if not text:
            continue
        if item.marker == "+":
            if not is_guard_fixture_path(item.path):
                if has_enabled_auto_flag(lower):
                    findings.append({"severity": "fail", "path": item.path, "rule": "automatic_trading_disabled", "message": "automatic_trading must not be enabled."})
                if re.search(r"\b(?:execution_enabled|trade_execution_enabled|broker_enabled)\b\s*[:=]\s*true\b", lower):
                    findings.append({"severity": "fail", "path": item.path, "rule": "automatic_execution_disabled", "message": "Execution enable flags must not be turned on."})
                for key, message in FALSE_LOCKS.items():
                    if has_bool_assignment(lower, key, "false"):
                        findings.append({"severity": "fail", "path": item.path, "rule": "research_only_mode", "message": message})
                for term in TRADING_TERMS:
                    if re.search(rf"\b{re.escape(term)}\b", lower):
                        findings.append({"severity": "fail", "path": item.path, "rule": "no_execution_terms", "message": "Automatic execution vocabulary is not allowed in investment system changes."})
        elif item.marker == "-" and is_logic_file(item.path):
            if any(field in lower for field in ANTI_LEAKAGE_FIELDS) and removes_named_guard(lower):
                findings.append({"severity": "fail", "path": item.path, "rule": "anti_leakage_fields_preserved", "message": "Future/as-of leakage guard fields must not be deleted."})
            if any(re.search(rf"\b{re.escape(term)}\b", lower) for term in LOGIC_GUARDS):
                findings.append({"severity": "fail", "path": item.path, "rule": "evaluation_logic_preserved", "message": "Cost/net return/benchmark/evaluation logic must not be removed."})

    findings.extend(final_state_findings(repo))

    passed = not any(item["severity"] == "fail" for item in findings)
    return {
        "generated_at": utc_now(),
        "passed": passed,
        "changed_paths": normalized_paths,
        "finding_count": len(findings),
        "findings": findings,
    }


def write_outputs(result: dict[str, Any], output_dir: pathlib.Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "latest_change_evaluation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    lines = ["# Investment System Change Evaluation", "", f"Generated: `{result['generated_at']}`", f"Passed: `{result['passed']}`", "", "## Changed Paths"]
    if result["changed_paths"]:
        lines.extend(f"- `{path}`" for path in result["changed_paths"])
    else:
        lines.append("- No changed paths detected.")
    lines.extend(["", "## Findings"])
    if result["findings"]:
        for item in result["findings"]:
            path = item.get("path") or "global"
            lines.append(f"- `{item['rule']}` `{path}`: {item['message']}")
    else:
        lines.append("- No invariant violations detected.")
    (output_dir / "latest_change_evaluation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate investment research system changes against non-negotiable invariants.")
    parser.add_argument("--repo", default=str(ROOT))
    parser.add_argument("--base-ref", default=None)
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    changed_paths, diff_text, untracked = git_diff(repo, args.base_ref)
    result = evaluate_change(repo, changed_paths, diff_text, untracked)
    write_outputs(result, pathlib.Path(args.output_dir))
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
