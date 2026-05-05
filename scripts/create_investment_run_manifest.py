#!/usr/bin/env python3

import argparse
import hashlib
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent


def file_metadata(path: pathlib.Path) -> dict[str, Any]:
    exists = path.exists()
    metadata: dict[str, Any] = {
        "path": str(path),
        "exists": exists,
        "sha256": None,
        "size_bytes": None,
    }
    if exists and path.is_file():
        content = path.read_bytes()
        metadata["sha256"] = hashlib.sha256(content).hexdigest()
        metadata["size_bytes"] = len(content)
    return metadata


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    run_id = f"{args.date}-{args.session}"
    files = {label: file_metadata(pathlib.Path(path)) for label, path in args.file}
    return {
        "run_id": run_id,
        "date": args.date,
        "session": args.session,
        "as_of_date": args.as_of_date or args.date,
        "as_of_session": args.as_of_session or args.session,
        "model": args.model,
        "provider": args.provider,
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an investment research run manifest with file checksums.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--session", required=True)
    parser.add_argument("--as-of-date", default=None)
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--file", action="append", nargs=2, metavar=("LABEL", "PATH"), default=[], help="Key input or output path to record; missing paths are allowed.")
    parser.add_argument("--runs-root", default=str(ROOT / "research" / "runs"))
    args = parser.parse_args()

    manifest = build_manifest(args)
    out_dir = pathlib.Path(args.runs_root) / manifest["run_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote investment run manifest: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
