# reproducibility.md

Rerun guidance and report provenance for claim-bearing report packages and
presented evidence. The goal is not cryptographic proof. The goal is that a
reviewer can tell which data snapshot, which code version, and which
environment pin produced the reported result.

## When to read

- Preparing a claim-bearing report package
- Reviewing a claim-bearing report package
- Deciding how a report, tracker, or local note should capture rerun guidance

## Principle

A load-bearing report claim must point to:

- The data snapshot used
- The code version used
- The dependency / environment pin used

Seeds, shared infrastructure references, and tracker run IDs are added when
they matter. Exploratory work may use lighter run notes. Report packages and
external claims need enough information for a reviewer to rerun or challenge
the presented evidence honestly.

## Rerun levels

| Level | Meaning | Typical evidence |
|---|---|---|
| Traceable | A run can be understood later | run note, parameters, metric, artifact link |
| Rerunnable | A run has enough information to repeat | data snapshot, code version, environment pin, seed |
| Reproduced | A rerun matched within tolerance | rerun note with tolerance |
| Validated | An independent reviewer or environment confirmed it | review note or external validation artifact |

## Recommended project files

Every project may keep a lightweight `reproducibility/` folder like:

```text
reproducibility/
├── data_versions.txt      # data files or tables used, with dated snapshot notes
├── shared_pins.txt        # shared modules and the commit refs used
├── uv.lock                # environment pin file, if Python
├── env_lock_ref.txt       # environment pin used by the reported evidence
└── seed.txt               # random seeds, if relevant
```

This is a convention, not a hard contract. Equivalent information may live in
MLflow, W&B, Neptune, Trackio, DVC, or another selected tracker if it is easy
for a reviewer to resolve.

## What to record

### 1. Data snapshot

Record enough to identify the data used:

- file path, table name, or dataset version
- period covered
- vendor or extraction date when relevant
- any preprocessing snapshot note if the raw data changes over time

### 2. Code version

Record the git commit used for the presented evidence. If the working tree was
dirty, say so explicitly and do not treat the result as claim-ready until rerun
from a clean state.

### 3. Environment pin

Record which dependency snapshot produced the presented evidence. For Python
projects that is often `uv.lock`; for other stacks it may be another lockfile
or exported environment description. The important part is that the reviewer
can recover the dependency state, and that `env_lock_ref.txt` or the
equivalent tracker field tells them which environment pin was actually used.

### 4. Seed and shared infrastructure

If the run is stochastic, record seeds. If the project uses `shared/`
infrastructure, record which shared modules and commit refs were used.

## Report provenance note

For each claim-bearing report package, keep or cite enough provenance for the
presented evidence:

- evidence or artifact ID
- data snapshot note
- git commit
- environment pin note
- seed where relevant
- run ID / artifact URI if a tracker is used

This can be captured in:

- the report package `provenance/` folder
- `results/results.parquet`
- a tracker run record
- a durable note in `decisions.md`
- a project-specific rerun note file

## Verification

To verify presented evidence later, a reviewer should be able to:

1. Find the evidence's data snapshot note
2. Check out the recorded commit
3. Restore the recorded environment pin
4. Reuse the recorded seed if relevant
5. Compare the rerun against the original result within an explicit tolerance

If one of those steps cannot be done, the claim may still be interesting, but
it is not fully rerunnable.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| No rerun guidance | Claim cites only a notebook path | Add data/code/env notes before using the result in a report package |
| Dirty working tree | Result exists but exact code state is unclear | Commit or rerun from a clean state |
| Moving data target | Vendor updates changed the underlying data | Record extraction date and snapshot note |
| Missing environment pin | Package versions drift across machines | Save or cite the environment pin |
| Single-seed stochastic result | Claimed stable result from one random seed | Re-run with multiple seeds and report spread |

## Cross-project use

When one project depends on another project's finding, cite the source evidence
and its rerun guidance in `decisions.md`. The consumer project should not
silently inherit the upstream claim without a reference to the upstream data,
code, and environment notes.

## Relationship to other references

- `references/review/process_review.md`
- `references/review/conclusion_review.md`
