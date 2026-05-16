#!/usr/bin/env python3
"""Verify that a research run left durable evidence artifacts.

Checks:
- `run_manifest.json` exists, records a command, and has `status: completed`.
- `logs/stdout.log` and `logs/stderr.log` exist.
- At least one manifest-listed non-empty durable artifact exists outside stdout/stderr logs.

Exit code 0 if all checks pass, 1 if any issue is reported.

Usage:
    python check_run_artifacts.py <path_to_run_dir>
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any


DURABLE_DIRS = ["outputs", "intermediate", "tables", "figures"]
ROOT_ARTIFACTS = {"metrics.json", "metrics.jsonl", "diagnostics.json", "analysis_summary.md"}
IGNORED_NAMES = {"README.md", "run_manifest.json", "stdout.log", "stderr.log", ".gitkeep"}
TRANSCRIPT_PREFIXES = ("stdout", "stderr", "console", "terminal")


def load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    if not path.exists():
        return None, ["  Missing run_manifest.json"]
    try:
        return json.loads(path.read_text(encoding="utf-8")), issues
    except json.JSONDecodeError as exc:
        return None, [f"  run_manifest.json is not valid JSON: {exc}"]


def is_nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def has_nonempty_descendant(path: Path) -> bool:
    return path.is_dir() and any(child.is_file() and child.stat().st_size > 0 for child in path.rglob("*"))


def is_durable_location(relative_path: Path) -> bool:
    parts = relative_path.parts
    if not parts:
        return False
    return str(relative_path).replace("\\", "/") in ROOT_ARTIFACTS or parts[0] in DURABLE_DIRS


def is_console_transcript(relative_path: Path) -> bool:
    name = relative_path.name.lower()
    stem = relative_path.stem.lower()
    return name.endswith(".log") or stem.startswith(TRANSCRIPT_PREFIXES)


def check_manifest(run_dir: Path, manifest: dict[str, Any] | None) -> tuple[list[str], int]:
    if manifest is None:
        return [], 0

    issues: list[str] = []
    durable_count = 0
    command = manifest.get("command")
    status = str(manifest.get("status", "")).lower()
    if not command or not str(command).strip():
        issues.append("  run_manifest.json must record the executed command; initialized runs are not completed evidence")
    if status != "completed":
        issues.append("  run_manifest.json status must be 'completed' before the run can be used as evidence")

    for required in ["run_id", "plan", "status"]:
        if required not in manifest:
            issues.append(f"  run_manifest.json missing required field: '{required}'")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        issues.append("  run_manifest.json artifacts must list durable artifact paths")
        return issues, durable_count
    if not artifacts:
        issues.append("  run_manifest.json artifacts must list at least one durable artifact path")

    for artifact in artifacts:
        if not isinstance(artifact, str) or not artifact.strip():
            issues.append("  run_manifest.json artifacts must contain non-empty path strings")
            continue
        artifact_path = (run_dir / artifact).resolve()
        try:
            relative_path = artifact_path.relative_to(run_dir.resolve())
        except ValueError:
            issues.append(f"  Manifest artifact escapes run directory: '{artifact}'")
            continue
        if not is_durable_location(relative_path):
            issues.append(f"  Manifest artifact is not in a durable artifact location: '{artifact}'")
            continue
        if is_console_transcript(relative_path):
            issues.append(f"  Manifest artifact looks like a console transcript, not evidence: '{artifact}'")
            continue
        if not artifact_path.exists():
            issues.append(f"  Manifest artifact does not exist: '{artifact}'")
        elif artifact_path.is_file() and not is_nonempty_file(artifact_path):
            issues.append(f"  Manifest artifact is empty: '{artifact}'")
        elif artifact_path.is_dir() and not has_nonempty_descendant(artifact_path):
            issues.append(f"  Manifest artifact directory has no non-empty files: '{artifact}'")
        else:
            durable_count += 1

    return issues, durable_count


def check_logs(run_dir: Path) -> list[str]:
    issues = []
    for relative in ["logs/stdout.log", "logs/stderr.log"]:
        if not (run_dir / relative).exists():
            issues.append(f"  Missing log file: {relative}")
    return issues


def check_run(run_dir: Path) -> list[str]:
    issues: list[str] = []
    manifest, manifest_issues = load_manifest(run_dir / "run_manifest.json")
    issues.extend(manifest_issues)
    manifest_check_issues, durable_count = check_manifest(run_dir, manifest)
    issues.extend(manifest_check_issues)
    issues.extend(check_logs(run_dir))

    if durable_count == 0:
        issues.append("  No durable artifact found: No manifest-listed durable artifact. stdout is not evidence; write metrics, tables, figures, diagnostics, or intermediate outputs under the run directory")
    return issues


def main():
    parser = argparse.ArgumentParser(description="Verify a research run directory has durable artifacts.")
    parser.add_argument("run_dir", help="Path to experiments/<plan>/runs/<run_id>")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.exists() or not run_dir.is_dir():
        print(f"Error: run directory not found: {run_dir}", file=sys.stderr)
        sys.exit(1)

    issues = check_run(run_dir)

    print(f"Checking run artifacts: {run_dir}")
    if issues:
        print(f"\n{len(issues)} issue(s):")
        for issue in issues:
            print(issue)
        sys.exit(1)

    print("Run artifacts pass contract checks.")


if __name__ == "__main__":
    main()
