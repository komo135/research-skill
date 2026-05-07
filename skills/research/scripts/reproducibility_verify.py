"""reproducibility_verify.py — Re-verify a stamped trial.

Reads a stamp record (from reproducibility_stamp.py output, typically stored
in results/results.parquet or alongside the trial notebook) and verifies:
  - Current git HEAD matches the stamp's commit (warn if checked out elsewhere)
  - Current data file hashes match the stamp's data_hashes (warn on drift)
  - Current uv.lock hash matches the stamp's env_lock_hash (warn on drift)

Drift in any axis means the trial is no longer exactly reproducible from the
current environment. The original stamp still uniquely identifies the trial's
environment; a verifier would need to check out the stamped commit to
reproduce.

Usage:
    python scripts/reproducibility_verify.py --stamp-file <path-to-stamp.json>
    # OR
    python scripts/reproducibility_verify.py --project-dir <path> --trial-id trial_001 \\
        --git-commit <hash> --env-lock-hash <hash>

Exit codes:
    0: all axes match (trial reproduces from current state)
    1: drift on at least one axis (trial does NOT exactly reproduce; checkout needed)
    2: setup error (file missing, malformed input)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

CHUNK = 65536


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def get_current_git_commit(repo_dir: Path) -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git rev-parse failed: {e.stderr.strip()}") from e


def parse_data_hashes(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split(maxsplit=1)
        if len(parts) == 2:
            out[parts[0]] = parts[1]
    return out


def find_uv_lock(project_dir: Path) -> Path | None:
    for c in [
        project_dir / "reproducibility" / "uv.lock",
        project_dir / "uv.lock",
        project_dir.parent / "uv.lock",
    ]:
        if c.exists():
            return c
    return None


def verify(stamp: dict[str, Any]) -> tuple[bool, list[str]]:
    """Verify a stamp dict. Returns (all_match, messages)."""
    messages: list[str] = []
    project_dir = Path(stamp["project_dir"]).resolve()
    if not project_dir.exists():
        return False, [f"ERROR: project_dir from stamp does not exist: {project_dir}"]

    all_match = True

    # Git commit
    try:
        current_commit = get_current_git_commit(project_dir)
    except RuntimeError as e:
        return False, [f"ERROR: {e}"]

    expected_commit = stamp.get("git_commit", "")
    if current_commit == expected_commit:
        messages.append(f"OK: git commit matches ({current_commit[:16]}...)")
    else:
        all_match = False
        messages.append(
            f"DRIFT: git commit changed "
            f"(stamp={expected_commit[:16]}..., current={current_commit[:16]}...). "
            "To reproduce exactly, run: "
            f"git checkout {expected_commit}"
        )

    # Env lock hash
    expected_env_hash = stamp.get("env_lock_hash", "")
    uv_lock = find_uv_lock(project_dir)
    if uv_lock is None:
        all_match = False
        messages.append("DRIFT: uv.lock not found (was present at stamp time)")
    else:
        current_env_hash = compute_sha256(uv_lock)
        if current_env_hash == expected_env_hash:
            messages.append(f"OK: env_lock_hash matches ({current_env_hash[:16]}...)")
        else:
            all_match = False
            messages.append(
                f"DRIFT: uv.lock hash changed "
                f"(stamp={expected_env_hash[:16]}..., current={current_env_hash[:16]}...). "
                "Dependencies have shifted since stamp."
            )

    # Data hashes
    expected_data = stamp.get("data_hashes", {})
    if expected_data:
        current_hashes = parse_data_hashes(project_dir / "reproducibility" / "data_hashes.txt")
        for path_key, expected_hash in expected_data.items():
            current_hash = current_hashes.get(path_key)
            if current_hash is None:
                all_match = False
                messages.append(f"DRIFT: data file {path_key} no longer in data_hashes.txt")
            elif current_hash != expected_hash:
                all_match = False
                messages.append(
                    f"DRIFT: data file {path_key} hash changed "
                    f"(stamp={expected_hash[:16]}..., current={current_hash[:16]}...)"
                )
            else:
                messages.append(f"OK: data {path_key} matches ({current_hash[:16]}...)")

    return all_match, messages


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--stamp-file", type=Path, default=None,
                   help="JSON file with stamp record (output of reproducibility_stamp.py)")
    p.add_argument("--project-dir", type=Path, default=None,
                   help="explicit project_dir (used if --stamp-file not provided)")
    p.add_argument("--trial-id", default=None)
    p.add_argument("--git-commit", default=None)
    p.add_argument("--env-lock-hash", default=None)
    args = p.parse_args()

    if args.stamp_file:
        if not args.stamp_file.exists():
            print(f"ERROR: stamp file not found: {args.stamp_file}", file=sys.stderr)
            sys.exit(2)
        try:
            stamp = json.loads(args.stamp_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERROR: failed to parse stamp file: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        if not (args.project_dir and args.git_commit and args.env_lock_hash):
            print("ERROR: provide --stamp-file OR all of --project-dir + --git-commit + --env-lock-hash",
                  file=sys.stderr)
            sys.exit(2)
        stamp = {
            "project_dir": str(args.project_dir),
            "trial_id": args.trial_id or "unknown",
            "git_commit": args.git_commit,
            "env_lock_hash": args.env_lock_hash,
            "data_hashes": {},
        }

    all_match, messages = verify(stamp)
    print(f"=== reproducibility_verify for {stamp.get('trial_id', '?')} ===")
    for m in messages:
        print(m)

    if all_match:
        print("\n✅ All axes match — trial reproduces from current environment.")
        sys.exit(0)
    else:
        print("\n⚠️  Drift detected — trial does NOT exactly reproduce from current state.")
        print("    The original stamp still uniquely identifies the trial environment.")
        print("    To reproduce: check out the stamped commit and pin dependencies to the stamped uv.lock hash.")
        sys.exit(1)


if __name__ == "__main__":
    main()
