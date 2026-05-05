"""reproducibility_stamp.py — Capture the 3-tuple (data hash + git commit + env lock)
for a promotion-eligible or claim-cited trial.

Per `references/shared/reproducibility.md` and CHARTER C12 / D-16 (uv).

Writes/updates files in <project_dir>/reproducibility/:
    data_hashes.txt       — SHA-256 of every data file used (merged with prior)
    env_lock_hash.txt     — SHA-256 of uv.lock at trial time
    seed.txt              — appends per-trial seed if --seed provided
    shared_pins.txt       — (manually maintained; this script does not auto-detect imports)

Also returns / prints a JSON-formatted stamp record with:
    trial_id, stamped_at (UTC ISO), git_commit, env_lock_hash, data_hashes, seed

The trial notebook or caller should capture this output and persist it to
results/results.parquet, its own analysis section, or another durable run log.

Usage:
    python scripts/reproducibility_stamp.py \\
        --project-dir notebooks/regime_aware_sizing \\
        --trial-id trial_001 \\
        --data-paths data/raw/spx_5min_2010_2024.parquet data/raw/vix_daily.parquet \\
        --seed 42

Exit codes:
    0: 3-tuple stamped successfully (working tree clean, all files exist)
    1: working tree dirty (uncommitted changes; commit first)
    2: data file missing
    3: uv.lock missing or stale
    4: not a git repository / git command failed
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CHUNK = 65536


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def get_git_state(repo_dir: Path) -> tuple[str, bool]:
    """Returns (commit_hash, is_dirty). Raises RuntimeError if not a git repo."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git rev-parse failed: {e.stderr.strip()}") from e
    except FileNotFoundError as e:
        raise RuntimeError("git command not available") from e

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return commit, bool(status)


def parse_data_hashes(path: Path) -> dict[str, str]:
    """Parse existing data_hashes.txt into a dict."""
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


def write_data_hashes(path: Path, mapping: dict[str, str]) -> None:
    lines = ["# format: <relative path>  <sha256>"]
    for k in sorted(mapping):
        lines.append(f"{k}  {mapping[k]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_uv_lock(project_dir: Path) -> Path:
    """Search for uv.lock in reproducibility/ first, then project_dir, then 1 level up."""
    candidates = [
        project_dir / "reproducibility" / "uv.lock",
        project_dir / "uv.lock",
        project_dir.parent / "uv.lock",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(
        "uv.lock not found in any of: "
        + ", ".join(str(c) for c in candidates)
        + " — run `uv lock` first."
    )


def stamp(
    project_dir: Path,
    trial_id: str,
    data_paths: list[Path],
    seed: int | None,
) -> dict[str, Any]:
    project_dir = project_dir.resolve()
    if not project_dir.exists():
        raise FileNotFoundError(f"project directory not found: {project_dir}")

    # Validate non-mutating preconditions before writing stamp artifacts.
    commit, is_dirty = get_git_state(project_dir)
    if is_dirty:
        raise RuntimeError(
            "Working tree is dirty (uncommitted changes). "
            "Commit changes first, then re-run reproducibility_stamp.py. "
            "Reproducibility requires that the analysis code at trial time "
            "is uniquely identified by a commit hash."
        )
    uv_lock = find_uv_lock(project_dir)
    env_hash = compute_sha256(uv_lock)

    # 1. Data hashes
    repro_dir = project_dir / "reproducibility"
    repro_dir.mkdir(parents=True, exist_ok=True)
    data_hashes_file = repro_dir / "data_hashes.txt"

    existing = parse_data_hashes(data_hashes_file)
    new_hashes: dict[str, str] = {}
    for p in data_paths:
        p = p.resolve()
        if not p.exists():
            raise FileNotFoundError(f"data file not found: {p}")
        # Store relative to project_dir parent (so path is portable across machines)
        try:
            key = str(p.relative_to(project_dir.parent))
        except ValueError:
            key = str(p)  # not under project_dir.parent — store absolute
        new_hashes[key] = compute_sha256(p)

    merged = {**existing, **new_hashes}
    write_data_hashes(data_hashes_file, merged)

    # 2. Env lock
    (repro_dir / "env_lock_hash.txt").write_text(env_hash + "\n", encoding="utf-8")

    # 3. Seed (append if provided)
    if seed is not None:
        seed_file = repro_dir / "seed.txt"
        existing_seeds = ""
        if seed_file.exists():
            existing_seeds = seed_file.read_text(encoding="utf-8")
            if not existing_seeds.endswith("\n"):
                existing_seeds += "\n"
        seed_file.write_text(existing_seeds + f"{trial_id}_seed  {seed}\n", encoding="utf-8")

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "trial_id": trial_id,
        "stamped_at": timestamp,
        "git_commit": commit,
        "env_lock_hash": env_hash,
        "env_lock_path": str(uv_lock),
        "data_hashes": new_hashes,
        "seed": seed,
        "project_dir": str(project_dir),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--trial-id", required=True)
    p.add_argument("--data-paths", nargs="*", default=[], type=Path)
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    try:
        result = stamp(args.project_dir, args.trial_id, args.data_paths, args.seed)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if "uv.lock" in str(e):
            sys.exit(3)
        sys.exit(2)
    except RuntimeError as e:
        msg = str(e).lower()
        if "dirty" in msg:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        if "git" in msg:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(4)
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(4)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
