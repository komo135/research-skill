"""prereg_diff.py — Diff actual trial analysis against frozen pre-registration.

Implements the spec in `references/pure_research/preregistration.md` §
"prereg_diff output specification" and the deviation severity matrix in
`references/pure_research/pr_workflow.md` § "Deviation severity matrix".

The trial notebook produces an actual.yaml file with the same structured
fields as the pre-reg's expected.yaml. This script compares them.

Files expected:
    prereg/<id>.md            — frozen pre-reg markdown
    prereg/<id>.lock          — hash lock from prereg_freeze.py
    prereg/<id>.expected.yaml — structured expected values (written when
                                 the agent authors the pre-reg)
    prereg/<id>.actual.yaml   — structured actual values (written by the
                                 trial notebook)

Usage:
    python scripts/prereg_diff.py --id PR_001 [--project-dir <path>]

Output:
    Pretty-printed report listing each comparison + deviation classification.

Exit codes:
    0: clean (no deviations)
    1: major deviation detected (trial INVALIDATED, requires new pre-reg)
    2: minor deviations only (proceed with documentation in decisions.md)
    3: setup error (file missing, malformed YAML, hash mismatch)
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CHUNK = 65536


# ---------------------------------------------------------------------------
# Severity matrix (per pr_workflow.md, kept in sync with that reference)
# ---------------------------------------------------------------------------

# A deviation is keyed by category. Each category maps to a "major" or
# "minor" classification.

MAJOR_CATEGORIES = {
    "data_hash_mismatch",
    "sample_size_drift_over_10pct",
    "period_shift_over_1y",
    "period_shift_population_change",
    "test_statistic_family_change",
    "competing_explanation_added_post_hoc",
    "threshold_changed_after_data",
    "multiple_testing_count_under_reported",
    "imputation_method_power_change",
    "hypothesis_threshold_large_miss",  # primary metric > 10% from pre-reg threshold
    "prereg_hash_mismatch",  # pre-reg edited in place after lock
}

MINOR_CATEGORIES = {
    "parameter_within_10pct",
    "sample_size_drift_under_5pct",
    "imputation_method_equivalent",
    "test_statistic_within_family",
    "hypothesis_threshold_near_miss",  # primary metric within 10% of threshold
}


@dataclass
class Deviation:
    category: str
    detail: str
    severity: str = field(init=False)

    def __post_init__(self) -> None:
        if self.category in MAJOR_CATEGORIES:
            self.severity = "major"
        elif self.category in MINOR_CATEGORIES:
            self.severity = "minor"
        else:
            # Unknown category — default to major out of caution
            self.severity = "major"


# ---------------------------------------------------------------------------
# Tiny YAML reader (no external dependency for the simple cases we need)
# ---------------------------------------------------------------------------


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse a flat YAML file with simple key: value lines and nested dicts.

    Supports:
        key: value (str/int/float/bool)
        key: [a, b, c] (list of literals)
        key:
          subkey: subvalue
          ...
    Does NOT support: anchors, aliases, multi-line strings, complex types.
    For the structured pre-reg / actual schemas we use, this is enough.
    """
    out: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(0, out)]

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()

        # Pop stack to current indent
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        cur = stack[-1][1]

        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()

        if val == "":
            # Nested dict
            nested: dict[str, Any] = {}
            cur[key] = nested
            stack.append((indent + 2, nested))
        else:
            cur[key] = _parse_scalar(val)
    return out


def _parse_scalar(s: str) -> Any:
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(x.strip()) for x in inner.split(",")]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    if s in ("null", "Null", "NULL", "~"):
        return None
    try:
        if "." in s or "e" in s.lower():
            return float(s)
        return int(s)
    except ValueError:
        return s


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_lock(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s:
            continue
        k, _, v = s.partition(":")
        out[k.strip()] = v.strip()
    return out


# ---------------------------------------------------------------------------
# Deviation detection
# ---------------------------------------------------------------------------


def diff_data_hashes(expected: dict[str, str], actual: dict[str, str]) -> list[Deviation]:
    devs: list[Deviation] = []
    for path, exp_hash in expected.items():
        act_hash = actual.get(path)
        if act_hash is None:
            devs.append(Deviation("data_hash_mismatch", f"{path}: missing in actual"))
        elif exp_hash != act_hash:
            devs.append(
                Deviation(
                    "data_hash_mismatch",
                    f"{path}: expected {exp_hash[:16]}... got {act_hash[:16]}...",
                )
            )
    return devs


def diff_sample_size(expected: int | None, actual: int | None) -> list[Deviation]:
    if expected is None or actual is None:
        return []
    if expected == 0:
        return []
    drift = abs(actual - expected) / expected
    if drift > 0.10:
        return [Deviation(
            "sample_size_drift_over_10pct",
            f"expected {expected}, actual {actual} ({drift:.1%} drift)",
        )]
    if drift > 0.05:
        return [Deviation(
            "sample_size_drift_under_5pct",  # actually 5-10% — minor
            f"expected {expected}, actual {actual} ({drift:.1%} drift)",
        )]
    if drift > 0:
        # < 5% — also minor
        return [Deviation(
            "sample_size_drift_under_5pct",
            f"expected {expected}, actual {actual} ({drift:.1%} drift)",
        )]
    return []


def diff_period(expected: dict | None, actual: dict | None) -> list[Deviation]:
    if not expected or not actual:
        return []
    devs: list[Deviation] = []
    for key in ("start", "end"):
        exp = expected.get(key)
        act = actual.get(key)
        if exp is None or act is None:
            continue
        if exp != act:
            # Treat any string difference as deviation; classification by magnitude
            # expected format YYYY-MM-DD; if year differs, major
            try:
                exp_year = int(str(exp)[:4])
                act_year = int(str(act)[:4])
                if abs(exp_year - act_year) >= 1:
                    devs.append(Deviation(
                        "period_shift_over_1y",
                        f"period.{key}: expected {exp}, actual {act} (≥ 1 year)",
                    ))
                else:
                    devs.append(Deviation(
                        "parameter_within_10pct",  # minor for sub-year drift
                        f"period.{key}: expected {exp}, actual {act}",
                    ))
            except (ValueError, TypeError):
                devs.append(Deviation(
                    "period_shift_over_1y",
                    f"period.{key}: expected {exp}, actual {act} (un-parseable, default major)",
                ))
    return devs


def diff_test_statistic(expected: str | None, actual: str | None) -> list[Deviation]:
    if not expected or not actual:
        return []
    if expected == actual:
        return []
    # Best-effort family detection: heuristic based on common names
    families = {
        "pearson": "correlation",
        "spearman": "correlation_rank",
        "kendall": "correlation_rank",
        "t-test": "mean_difference",
        "welch": "mean_difference",
        "bootstrap": "resample",
        "permutation": "resample",
        "wilcoxon": "rank_test",
        "mann-whitney": "rank_test",
    }
    exp_fam = families.get(expected.lower(), expected.lower())
    act_fam = families.get(actual.lower(), actual.lower())
    if exp_fam != act_fam:
        return [Deviation(
            "test_statistic_family_change",
            f"expected {expected} ({exp_fam}), actual {actual} ({act_fam})",
        )]
    return [Deviation(
        "test_statistic_within_family",
        f"expected {expected}, actual {actual} (same family {exp_fam})",
    )]


def diff_explanations(expected: list[str], actual: list[str]) -> list[Deviation]:
    if not expected:
        return []
    extra = [e for e in actual if e not in expected]
    if extra:
        return [Deviation(
            "competing_explanation_added_post_hoc",
            f"explanations not in pre-reg: {extra}",
        )]
    return []


def diff_threshold(
    expected_threshold: float | None,
    actual_value: float | None,
    threshold_direction: str = "greater",
) -> list[Deviation]:
    """Compare actual primary metric to pre-reg threshold.

    threshold_direction:
        "greater": expected actual > threshold (e.g., r > 0.6)
        "less":    expected actual < threshold (e.g., p < 0.05)
        "equal":   not used commonly; falls back to greater
    """
    if expected_threshold is None or actual_value is None:
        return []

    if threshold_direction == "less":
        passes = actual_value < expected_threshold
    else:
        passes = actual_value > expected_threshold

    if passes:
        return []

    # Did not pass threshold — classify miss magnitude
    if expected_threshold == 0:
        miss_pct = abs(actual_value)
    else:
        miss_pct = abs(actual_value - expected_threshold) / abs(expected_threshold)

    if miss_pct > 0.10:
        return [Deviation(
            "hypothesis_threshold_large_miss",
            f"threshold {expected_threshold} (direction: {threshold_direction}), "
            f"observed {actual_value} (miss {miss_pct:.1%})",
        )]
    return [Deviation(
        "hypothesis_threshold_near_miss",
        f"threshold {expected_threshold} (direction: {threshold_direction}), "
        f"observed {actual_value} (miss {miss_pct:.1%}; near-miss)",
    )]


def diff_multiple_testing(expected_n: int | None, actual_n: int | None) -> list[Deviation]:
    if expected_n is None or actual_n is None:
        return []
    if actual_n > expected_n:
        return [Deviation(
            "multiple_testing_count_under_reported",
            f"pre-reg N={expected_n}, actual N={actual_n} "
            f"({actual_n - expected_n} extra trials, correction must be re-computed)",
        )]
    return []


# ---------------------------------------------------------------------------
# Main diff orchestration
# ---------------------------------------------------------------------------


def run_diff(prereg_id: str, project_dir: Path) -> tuple[int, list[Deviation], list[str]]:
    """Returns (exit_code, deviations, info_messages)."""
    info: list[str] = []
    devs: list[Deviation] = []

    prereg_md = project_dir / "prereg" / f"{prereg_id}.md"
    lock_path = project_dir / "prereg" / f"{prereg_id}.lock"
    expected_path = project_dir / "prereg" / f"{prereg_id}.expected.yaml"
    actual_path = project_dir / "prereg" / f"{prereg_id}.actual.yaml"

    # 1. Pre-reg hash check
    if not lock_path.exists():
        return 3, [], [f"ERROR: lock file not found: {lock_path}"]
    if not prereg_md.exists():
        return 3, [], [f"ERROR: pre-reg markdown not found: {prereg_md}"]

    lock = parse_lock(lock_path)
    actual_md_hash = compute_sha256(prereg_md)
    if lock.get("sha256") != actual_md_hash:
        devs.append(Deviation(
            "prereg_hash_mismatch",
            f"pre-reg markdown sha256 changed since freeze "
            f"(lock={lock.get('sha256','?')[:16]}..., actual={actual_md_hash[:16]}...). "
            "Pre-reg was edited in place after freezing — this is a major deviation.",
        ))
    else:
        info.append(f"OK: pre-reg hash matches lock ({actual_md_hash[:16]}...)")

    # 2. expected vs actual structured comparison
    if not expected_path.exists():
        info.append(f"WARN: {expected_path} not found — skipping structured diff. "
                    f"Author the expected.yaml when freezing the pre-reg.")
        return _exit_code_for(devs), devs, info
    if not actual_path.exists():
        return 3, devs, info + [f"ERROR: trial actual.yaml not found: {actual_path}"]

    expected = parse_simple_yaml(expected_path.read_text(encoding="utf-8"))
    actual = parse_simple_yaml(actual_path.read_text(encoding="utf-8"))

    info.append(f"OK: read expected ({len(expected)} top-level keys) and actual ({len(actual)} top-level keys)")

    # Data hashes
    if "data_hashes" in expected:
        devs.extend(diff_data_hashes(
            expected.get("data_hashes", {}) or {},
            actual.get("data_hashes", {}) or {},
        ))

    # Sample size
    devs.extend(diff_sample_size(expected.get("sample_size"), actual.get("sample_size")))

    # Period
    devs.extend(diff_period(expected.get("period"), actual.get("period")))

    # Test statistic
    devs.extend(diff_test_statistic(
        expected.get("test_statistic"),
        actual.get("test_statistic"),
    ))

    # Explanations
    devs.extend(diff_explanations(
        expected.get("explanations", []) or [],
        actual.get("explanations", []) or [],
    ))

    # Multiple testing
    devs.extend(diff_multiple_testing(
        expected.get("multi_testing_n"),
        actual.get("multi_testing_n"),
    ))

    # Per-metric threshold check (if expected_thresholds provided)
    exp_thr = expected.get("primary_metric_threshold")
    exp_dir = expected.get("primary_metric_direction", "greater")
    act_val = actual.get("primary_metric_value")
    if exp_thr is not None and act_val is not None:
        devs.extend(diff_threshold(exp_thr, act_val, exp_dir))

    return _exit_code_for(devs), devs, info


def _exit_code_for(devs: list[Deviation]) -> int:
    if any(d.severity == "major" for d in devs):
        return 1
    if any(d.severity == "minor" for d in devs):
        return 2
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--id", required=True, help="pre-registration ID, e.g., PR_001")
    p.add_argument("--project-dir", default=Path("."), type=Path,
                   help="project root containing prereg/ folder")
    args = p.parse_args()

    code, devs, info = run_diff(args.id, args.project_dir)

    print(f"=== prereg_diff for {args.id} ===")
    for line in info:
        print(line)
    if not devs:
        print("\n✅ No deviations detected.")
    else:
        print(f"\nDeviations ({len(devs)}):")
        for d in devs:
            sev = "🔴 MAJOR" if d.severity == "major" else "🟡 minor"
            print(f"  {sev}: [{d.category}] {d.detail}")

    print(f"\nExit code: {code}")
    if code == 0:
        print("Status: CLEAN — proceed.")
    elif code == 1:
        print("Status: MAJOR DEVIATION — trial invalidated. File new pre-registration "
              "and add deviation entry to decisions.md per pr_workflow.md.")
    elif code == 2:
        print("Status: minor deviations only — document each in decisions.md and proceed.")
    else:
        print("Status: SETUP ERROR — fix the issue above and re-run.")

    sys.exit(code)


if __name__ == "__main__":
    main()
