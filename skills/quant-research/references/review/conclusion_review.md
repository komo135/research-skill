# conclusion_review.md

Conclusion review — are the conclusions warranted? This is the second
of two review axes (the first is `process_review.md` for discipline
audit). Both must pass before any `matured` (R&D) or `supported` (Pure
Research) promotion.

## When to read

- After `process_review.md` is clean
- Before running the promotion gate
  (`rd_promotion_gate.md` / `pr_promotion_gate.md`)
- Reviewing another agent's promotion claim

## Purpose

Conclusion review checks that the conclusions are supported by the
evidence. Process review (already run) verified that the protocol was
followed; this review checks whether the resulting numbers and
narrative actually justify the claim being made.

The split: process review catches "you didn't do the work right";
conclusion review catches "you did the work but the result doesn't
support what you're claiming". Both are common; both are necessary.

## How to run

Same checklist discipline as `process_review.md`. Load-bearing checks require
concrete evidence cited. "Looks good" is forbidden.

```
- [x] item — evidence: <file:line, hash, numeric value, or specific tool output>
- [ ] item — FAIL: <what's wrong>
- [ ] item — N/A (justify why)
```

## Pre-axis: Numeric red flag triggers ("too good to be true")

Before walking the 6 axes, scan the cited trial's metrics against the
following thresholds. A flagged metric does **not** by itself block
promotion — but it directs **extra scrutiny** to Axis 2 (Statistical
sufficiency) and Axis 4 (Analysis depth) for that specific metric.

| Flag | Threshold | Action if flagged |
|---|---|---|
| Test Sharpe (after costs) | > 3 | Axis 2: re-verify multiple-testing correction; Axis 4: A4+ explanation must address why such a high Sharpe is plausible |
| Walk-forward mean Sharpe | > 2 | Axis 2: bootstrap CI / DSR scrutiny; Axis 4: A4+ explanation of source |
| Information Coefficient (Spearman) on financial returns | > 0.10 | Axis 2: cross-sectional sample-size check; Axis 4: mechanism named |
| ML AUC on a return-sign target | > 0.65 | Axis 1: shuffled-target test mandatory; Axis 4: A4+ |
| Per-trade win rate | > 65% | Axis 2: per-trade variance + payoff asymmetry check |
| Max drawdown / annualized vol | < 0.5 | Axis 1: PnL reconciliation; Axis 4: A4+ on smoothness mechanism |
| Bootstrap 95% CI lower bound | > 1.5 (unusually tight) | Axis 2: bootstrap design (block size, resamples) check |
| Test metric outside bootstrap 95% CI | any direction | Axis 2: caught by "Bootstrap CI brackets the headline metric" — likely a bug |
| Headline Sharpe ≥ 2× walk-forward mean | any | Axis 2: caught by "Walk-forward and test consistent" — likely test-set leakage |

These thresholds are aggressive on purpose. If the metric is genuinely
real, the A4 analysis (Axis 4) should easily explain the mechanism;
if the analysis cannot, the metric is more likely a bug or selection
artifact than a real edge.

## The 6 axes

Each axis is a separate review pass. All 6 must clear for promotion.

### Axis 1: Implementation correctness

The numbers come from code that does what it claims to do.

- [ ] **Sanity checks pass** for the trial (relevant subset from
  `references/shared/sanity_checks.md`):
  - PnL reconciliation
  - Cost monotonicity (if cost-sensitive)
  - Sign-flip identity (if signal-based)
  - NaN / Inf scan
  - Time-shift placebo
  - Random-signal benchmark (mandatory)
  - Shuffled-target test (if ML)
  - Cross-instrument aggregation scan (if multi-symbol panel)
  - Embargo-existence check (if walk-forward / CV)
  - Whole-period statistic scan (rolling vs whole-period normalization)
  - Evidence: trial notebook § Sanity checks output, each check pass
    + observation
- [ ] **Look-ahead leak detected and resolved** via
  `scripts/leakage_check.py::lookahead_check`
  - Evidence: `leakage_check.py` output + clean status
- [ ] **No whole-period normalization / fitting / target encoding**
  - Evidence: code review notes; flagged patterns from
    `references/shared/sanity_checks.md` § 9
- [ ] **HMM / Kalman: filtering used (not smoothing) where causal
  signal needed**
  - Evidence: code review note
- [ ] **Cross-symbol operations have explicit `groupby('symbol')`
  on multi-instrument panels**
  - Evidence: code grep / review note
- [ ] **Annualization factor matches bar frequency** (e.g., daily
  Sharpe × √252)
  - Evidence: per-metric annualization formula
- [ ] **No silent exception swallowing** (`try: ... except: pass` /
  `except Exception: pass` patterns) in trial code
  - Evidence: code grep for `except.*pass` patterns; if present, the
    exception handler must log or re-raise, not swallow silently
- [ ] **No off-by-one indexing / iloc-vs-loc confusion** in cited
  computations
  - Evidence: code review of slicing operations on time series;
    flag any `[:-1]` / `[1:]` / `iloc[i]` / `loc[i]` boundaries that
    affect the headline metric
- [ ] **Sort order enforced** before any `groupby` / `rolling` /
  `diff` operation on time series
  - Evidence: presence of explicit `sort_values('time')` or
    `sort_values(['symbol', 'time'])` before relevant operations

### Axis 2: Statistical sufficiency

The sample / power / multiple-testing correction is enough to support
the claim.

- [ ] **Sample size adequate** for the effect size being claimed
  - Evidence: power analysis or N + observed effect size + standard
    error citation
- [ ] **Bootstrap CI brackets the headline metric** (sanity check on
  the bootstrap)
  - Evidence: bootstrap CI bounds + headline value, headline within
    CI
- [ ] **Multiple-testing correction applied** per
  `references/shared/multiple_testing.md`:
  - Single test: Harvey-Liu-Zhu t > 3.0 hurdle
  - Hyperparameter sweep: DSR ≥ 0.95 with honest N
  - Cross-strategy comparison: Romano-Wolf step-down
  - Combined: PSR + the relevant correction(s)
  - Evidence: corrected statistic value + method + trial count
- [ ] **Trial count for correction is honest** (per
  `process_review.md` HARKing checklist)
- [ ] **Walk-forward / CPCV path count adequate** (n_paths ≥ 10 for
  CPCV)
  - Evidence: per-method n_paths value
- [ ] **Test set touched once**: per
  `references/shared/time_series_validation.md`, the test set was
  not touched during model selection
  - Evidence: code review + decision log

### Axis 3: Claim discipline

The promotion claim is phrased no stronger than the evidence, with
explicit scope.

- [ ] **Claim wording matches evidence type**: causal claims have
  causal evidence (per pre-reg `evidence_type` field for Pure
  Research); correlative claims use "associated with" not "causes"
  - Evidence: claim wording vs `evidence_type` declared in
    `preregistration.md` § 2 (Pure Research)
- [ ] **Scope is precise**: universe, period, regime, market structure
  preconditions named explicitly
  - Evidence: claim wording vs Methods § 2 (data scope) cross-check
- [ ] **No universal generalization beyond tested scope**: claim does
  not extrapolate to instruments / periods / regimes not tested
  - Evidence: read claim wording for "in general", "broadly", "always"
    patterns
- [ ] **Negative claims documented** if any explanation was rejected
  - Evidence: explanation_ledger Claims section includes rejected
    E's; IMRAD § 4.3 documents negative claim with same A4 rigor
- [ ] **IMRAD coherence**: abstract claim ≡ Discussion claim ≡
  Conclusion claim (no drift across sections)
  - Evidence: cross-section text comparison; flag any rephrasing
    that broadens or narrows scope
- [ ] **No undisclosed binarization / discretization**: e.g., AUC
  claim implies binary target; if regression target was binarized,
  the binarization is in Methods
  - Evidence: Methods § 2.3 / 2.4 cross-check

### Axis 4: Analysis depth (per CHARTER C13, the primary axis)

The analysis reaches A4 minimum (`references/shared/analysis_depth.md`).

- [ ] **Trial Analysis section all 5 sub-fields filled** (Observation
  / Decomposition / Evidence weighing / Tier rating / Gap to next
  tier)
  - Evidence: trial notebook § 5 (R&D) or § 6 (Pure Research)
- [ ] **Tier rating is A4 or higher** with justification
  - Evidence: § Tier rating + "why this tier and not the next"
    explanation
- [ ] **Mechanism is named** (specific causal chain, not generic
  "the model captures the signal")
  - Evidence: Discussion § 4.1 (PR) or capability A4 analysis (R&D)
- [ ] **Alternatives systematically excluded**: each non-primary
  candidate has a discriminating test or evidence that weakens it
  - Evidence: Evidence weighing table per candidate
- [ ] **Multiple sources of supporting evidence** (≥2 independent
  observations or evidence types per A4 definition)
  - Evidence: evidence weighing table shows ≥2 entries with type
    `numerical`
- [ ] **Evidence type per claim**: each supporting evidence labeled
  numerical / structural-argument / literature-reference /
  null-result-of-X
  - Evidence: § 5.3 / 6.3 columns
- [ ] **Structural-argument alone does not support A4**: at least one
  numerical evidence is cited per supporting candidate
  - Evidence: count of numerical evidence ≥ 1 per supported candidate
- [ ] **No generic terminal labels** in success or failure
  explanation: "noise / regime / cost / model is good / data was
  clean" patterns absent or decomposed per
  `references/shared/result_analysis.md`
  - Evidence: text scan of Discussion / Analysis sections; flag any
    of the prohibited labels not followed by mechanism-level
    decomposition

### Axis 5: Reproducibility

The trial can be re-run.

- [ ] **3-tuple recorded** for promotion-eligible or claim-cited trial(s) per
  `references/shared/reproducibility.md`:
  - Data hash in `reproducibility/data_hashes.txt`
  - Git commit in `results.parquet`
  - Env lock hash in `reproducibility/env_lock_hash.txt`
  - Evidence: file existence + content
- [ ] **Random seed recorded** and (for stochastic algorithms)
  multiple seeds reported
  - Evidence: `reproducibility/seed.txt` + per-seed result mean ±
    std (for DL / RL)
- [ ] **Shared infrastructure pins** recorded if `shared/` is used
  - Evidence: `reproducibility/shared_pins.txt`
- [ ] **Working tree was clean** at trial time (no uncommitted
  changes)
  - Evidence: `reproducibility_stamp.py` exit 0 logged in
    `decisions.md`
- [ ] **No hardcoded paths** that would break on a different machine
  - Evidence: code review note

### Axis 6: Cold-eye check (adversarial pass)

Read the artifact alone, with author narrative withheld, and try to
falsify the claim.

This is the **only** axis that uses material withheld from the rest of
the review. The agent reading the IMRAD draft (Pure Research) or the
capability promotion writeup (R&D) does so without `decisions.md`,
without `explanation_ledger.md` / `capability_map.md`, without prior
session context. The agent reads the artifact alone — same model, but
deliberately deprived of the priors that would anchor on the author's
framing.

The mechanism is from Cross-Context Review (Song, arxiv 2603.12123):
fresh-session review with minimum context outperforms same-session
review on code review (+4.7 F1). The asymmetry is the value.

**Pre-condition: artifact must exist and be self-contained**

Before attempting cold-eye reading, verify:

- [ ] **Artifact file exists**: the IMRAD draft (`imrad_draft.md`)
  for Pure Research, OR the capability promotion writeup in
  `decisions.md` plus the cited trial notebooks for R&D
  - Evidence: file path + content size > 0
- [ ] **Artifact is self-contained**: a cold reader can understand
  the claim, the evidence, and the mechanism without consulting
  `explanation_ledger.md` / `capability_map.md` / `decisions.md`
  cross-references for basic understanding
  - Evidence: read first 2 sections; if cold reader needs to "go
    look up what C5 is" or "go check explanation_ledger to see what
    E2 says", artifact failed self-containment
  - Failure mode: artifact is a 3-line summary referencing 5 other
    files
  - **If artifact-incomplete, the cold-eye check is BLOCKED until
    the artifact is rewritten to be self-contained.** Do not attempt
    cold-eye check on an incomplete artifact and pretend it passed.

Procedure (after artifact-completeness verified):

1. **Read the artifact alone**: the IMRAD draft (Pure Research) OR
   the capability promotion writeup section of `decisions.md` + the
   relevant trial notebooks (R&D). Do NOT read other files in the
   project.
2. **Adopt the working hypothesis**: "this claim is wrong; what
   evidence in the artifact, if reinterpreted, could support an
   alternative?"
3. **List ≥1 falsifying interpretation**: a coherent reading of the
   evidence that supports a different conclusion than the claim
4. **Test the falsifying interpretation**: is it ruled out by other
   evidence in the artifact? If not, the claim is "supported within
   project narrative" but not "supported as defensible externally"
   — promotion is blocked

Cold-eye check items:

- [ ] **Cold-eye reading attempted** with minimum context (artifact
  alone)
  - Evidence: explicit statement of what was read and what was
    excluded
- [ ] **At least one falsifying interpretation identified**: state the
  alternative reading
  - Evidence: written alternative interpretation
- [ ] **Falsifying interpretation rebutted by artifact-internal
  evidence**: not by author narrative, not by additional context
  - Evidence: cited artifact passage that rebuts the alternative
- [ ] **If no internal rebuttal exists**: promotion blocked; the
  claim is artifact-incomplete (the IMRAD draft or capability
  writeup must be revised to include the rebuttal, OR the claim
  must be weakened to acknowledge the unresolved alternative)

## Outcome of conclusion review

- **All 6 axes pass with citations for load-bearing items** → conclusion review CLEAN;
  proceed to the promotion gate
  (`rd_promotion_gate.md` / `pr_promotion_gate.md`)
- **Any axis fails** → conclusion review FAILED; cannot proceed to
  promotion
- **Conclusion review report** written into `decisions.md`:

```markdown
## YYYY-MM-DD Conclusion review for promotion of <X>

Date: <YYYY-MM-DD HH:MM>
Reviewer: <agent / user>
Process review status: clean (per `decisions.md` entry on <date>)

### Axis 1: Implementation correctness
- [x] sanity checks pass — evidence: ...
- [x] ...

### Axis 2: Statistical sufficiency
- [x] sample size adequate — evidence: ...
- ...

### Axis 3: Claim discipline
...

### Axis 4: Analysis depth
- [x] tier A4+ — evidence: trial notebook § 5.4 = "A4 (justification: ...)"
- ...

### Axis 5: Reproducibility
...

### Axis 6: Cold-eye check
- [x] cold-eye reading attempted — read IMRAD draft alone, excluded explanation_ledger and decisions.md
- Falsifying interpretation considered: <alternative reading>
- Rebutted by: <artifact passage>

Sign-off: conclusion review clean / fail
```

## Common conclusion violations

| Violation | Symptom | Axis caught |
|---|---|---|
| Sanity check failure ignored | Random-signal benchmark passes (signal evaluator broken), trial result claimed anyway | Axis 1 |
| Single t > 2 from many trials | DSR not computed or computed with under-reported N | Axis 2 |
| "X causes Y" with correlative evidence | Pre-reg evidence_type field declares correlative; claim wording uses causal language | Axis 3 |
| Generic terminal label in success | "the model is good at variance capture" with no mechanism | Axis 4 (no terminal label) |
| Single-source A4 claim | One numerical evidence cited; A4 needs ≥2 | Axis 4 (multiple sources) |
| Structural-argument-only claim | "By construction the model must work because ..." with no measured number | Axis 4 (numerical required) |
| Stale env lock | uv.lock from a prior project state, not the current trial | Axis 5 |
| No falsifying interpretation attempted | Cold-eye check skipped or "looks good" | Axis 6 |
| Falsifying interpretation cannot be rebutted | Cold-eye check identifies an alternative; artifact has no internal rebuttal | Axis 6 — promotion blocked |

## Why both reviews are mandatory

Process review (`process_review.md`) catches **process violations**:
the agent skipped pre-registration, the charter was rewritten
mid-project, the integration test ran before upstream caps were
matured. These violations corrupt every downstream check; a clean
conclusion review on a corrupted process is a confidence in
contaminated evidence.

Conclusion review (`conclusion_review.md`) catches **claim violations**:
the analysis is at A2 but the claim is being made at A4 confidence,
the multiple-testing correction was skipped, the cold-eye reading
surfaces an unresolved alternative. These violations mean the result
doesn't support what's being claimed even when the process was
followed.

Both must pass; either alone is insufficient.

## Relationship to other references

- Pre-condition: `references/review/process_review.md` (must run
  first and be clean)
- Required by `references/rd/rd_promotion_gate.md` § Pre-conditions
  and `references/pure_research/pr_promotion_gate.md` § Pre-conditions
- Sanity checks: `references/shared/sanity_checks.md`
- Look-ahead checks: scripts/leakage_check.py
- Multiple testing: `references/shared/multiple_testing.md`
- Analysis depth: `references/shared/analysis_depth.md`
- Result analysis (no terminal labels): `references/shared/result_analysis.md`
- Reproducibility: `references/shared/reproducibility.md`
- Time-series validation: `references/shared/time_series_validation.md`
