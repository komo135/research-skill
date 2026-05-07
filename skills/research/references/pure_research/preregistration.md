# preregistration.md

AEA-style Pre-Analysis Plan (PAP) — the hash-locked design freeze that
the trial must follow. Pre-registration is the single most effective
intervention against p-hacking and post-hoc rationalization, and it is
mandatory in this skill for every Pure Research trial that produces a
metric.

## When to read

- Designing a Pure Research trial (after PR/FAQ is frozen and targeted
  literature is done)
- Reviewing whether a deviation from pre-registration is acceptable
- Operating `scripts/prereg_freeze.py` or `scripts/prereg_diff.py`

## Purpose

Pre-registration freezes the **question, competing explanations, test
design, and expected outcomes** before any data is inspected. After the
trial, the actual analysis is diffed against the frozen pre-registration;
deviations are categorized by severity and either accepted (with
documentation) or trigger a fresh trial.

The mechanism: HARKing (Hypothesizing After Results are Known) and the
garden of forking paths are eliminated when the design is committed
before the data is touched. Without pre-registration, finding-driven
narrative shifts are undetectable.

AEA requires pre-registration for all field experiments submitted to its
journals since 2018. This skill applies the same standard to all Pure
Research trials.

## Required content

A pre-registration document (`prereg/PR_<id>.md`) must contain all of:

### 1. Question (one sentence)

The exact research question this trial answers. Identical to or a
sub-question of the PR/FAQ's framing.

> Example: "Did short-vol measured effect on public benchmark benchmark datasets
> materially decline in 2020-2024 versus 2010-2019, by primary metric
> over rolling 3-year windows?"

### 2. Competing explanations (≥2)

Enumerate the explanations the trial will discriminate between. **At
least two**, including one null/artifact explanation. For each, also
declare the **evidence type**: whether the predicted observation
constitutes causal proof or correlative evidence.

| Field | Required | Description |
|---|---|---|
| ID | yes | E1, E2, E_null, ... |
| Statement | yes | The explanation in 1 sentence |
| Mechanism | yes | The proposed causal chain |
| Expected observation | yes | What you would observe if this E is true (ex ante prediction) |
| Evidence type | yes | `causal` (the test would prove causation) / `correlative` (the test shows association but not direction) / `null-result` (test rules out the alternative without proving the primary) |
| If `correlative`: causation gap | yes | What additional test would establish causation? |

Why evidence type matters: a `correlative` test that "supports E2"
gives weaker grounds for promotion than a `causal` test. The promotion
gate (`pr_promotion_gate.md`) uses this field to gauge whether the
claim wording can be "X causes Y" or must be "X is associated with Y
under conditions Z".

> Example:
> - **E1 (regime change)**: The measurement-noise structure of the underlying
>   index changed (e.g., due to changes in equity-options market
>   structure), reducing the predictability that vol-carry strategies
>   exploit. Expected pattern: measurement-noise metrics shift across the two
>   periods. Evidence type: `correlative` (a shift in measurement-noise
>   alongside primary metric decay is association; causal proof would require
>   instrumental variables on options-market structure changes).
> - **E2 (crowding)**: Retail / non-commercial vol-seller positioning
>   grew, compressing the carry. Expected pattern: CFTC COT
>   non-commercial vol-seller positioning increases over 2020-2024;
>   carry decay correlates with positioning growth. Evidence type:
>   `correlative`. Causation gap: would need micro-level test of
>   bid-ask spread mechanics linking positioning growth to specific
>   carry compression episodes.
> - **E3 (null / measurement)**: The primary metric difference is sample
>   variance — a 5-year period in 2020-2024 happened to be unfavorable.
>   Expected pattern: bootstrap CI on the primary metric difference includes 0.
>   Evidence type: `null-result` (rejecting E3 strengthens the case for
>   E1 or E2 but does not by itself identify which).

### 3. Test design (data, sample, metric, threshold, multiple testing)

The exact methodology, in enough detail that a different agent could
re-run the test and get the same result.

```
Data: <source, hash if available, period, frequency>
Sample / split: <how data is split for the test, e.g., rolling 3-year
                 windows>
Metric: <primary metric (single number) + secondary metrics if needed>
Threshold: <success / failure / ambiguous boundaries on the primary
            metric>
Multiple testing: <how many distinct hypotheses or sub-strategies are
                   being tested in this trial; correction method
                   (Bonferroni / Romano-Wolf / domain-appropriate selection correction)>
```

> Example:
> - Data: public benchmark audit records, period 2010-01 through 2024-12,
>   data hash a3f8...
> - Sample: rolling 3-year primary metric windows, computed at month-end, no
>   look-ahead in label availability
> - Primary metric: difference between mean primary metric of windows ending
>   2010-2019 vs windows ending 2020-2024
> - Secondary: bootstrap 95% CI of the difference (block bootstrap,
>   block size = sqrt(n) per Politis & Romano 1994)
> - Threshold: support E1 or E2 if difference < -0.5 with 95% CI
>   excluding 0; support E3 if 95% CI includes 0
> - Multiple testing: 3 sub-strategies tested, Bonferroni-correct significance level
>   to 0.05/3 = 0.017

### 4. Expected diff under each explanation

For each competing explanation, predict the observation pattern that
would best support that explanation. **This forces ex ante prediction
and prevents post-hoc fitting**.

> Example:
> - If E1 (task-distribution shift) true: measurement-noise metric increases
>   materially across the two periods (e.g., > 1 std dev shift).
>   Carry primary metric difference is largely explained by measurement-noise shift.
> - If E2 (annotation drift) true: audit-rubric change count increases > 2x;
>   primary metric difference correlates with rubric-change density
>   (r > 0.5 across rolling sub-periods).
> - If E3 (null) true: bootstrap CI on primary metric difference includes 0;
>   distribution of primary metric differences across random 5-year sub-periods
>   in 2010-2019 includes the observed 2020-2024 value.

### 5. Stop condition

The observable condition that ends the trial. Without a stop condition,
trials drift into "let's try one more thing" territory.

> Example: Trial ends when (a) all three explanations have been tested
> against their expected diff patterns, OR (b) the data quality is
> insufficient to discriminate (sample size in 2020-2024 too small,
> CFTC data unavailable for the period).

## Freezing the pre-registration

After the document is complete and reviewed:

```bash
python scripts/prereg_freeze.py --type prereg --id PR_<id> --path prereg/PR_<id>.md
```

This:
1. Computes SHA-256 of the file content
2. Writes `prereg/PR_<id>.lock` with hash + UTC timestamp + path
3. Records the freeze in `decisions.md` as a state transition

After freezing, the document **cannot be edited in place**. Any change
goes through the deviation severity matrix in
`references/pure_research/pr_workflow.md`.

## prereg_diff output specification

`scripts/prereg_diff.py` compares the actual trial output against the
frozen pre-registration. The output **must include** all of:

- **Pre-reg hash check**: actual `prereg/PR_<id>.md` hash matches
  `prereg/PR_<id>.lock` (proves no in-place edit happened)
- **Data hash match**: actual data source hash vs pre-reg-stated hash;
  any mismatch is a major deviation
- **Sample size match**: actual N vs pre-reg-expected N (with rounding
  tolerance); period / population shifts manifest here
- **Period match flag**: actual data period matches pre-reg period
  (start and end dates within tolerance, e.g., ±5 operational days)
- **Test statistic match**: actual statistic name matches pre-reg
  (e.g., Pearson vs Spearman is a major deviation)
- **Primary metric value vs pre-reg expected**: not an equality check
  (results genuinely differ from expectations) but the recorded
  expected value, for review
- **Multiple testing correction**: trial count actually used vs
  pre-reg-stated count; honest count is required for selection-adjusted statistic / Bonferroni

The script returns:
- exit code 0 if all checks pass (only acceptable: pre-reg-hash matches
  and the semantic checks pass, even if the metric value differs from
  expectation)
- exit code 1 if any **major** deviation detected (data hash mismatch,
  sample size > tolerance, period mismatch, test statistic changed,
  multiple testing count under-reported)
- exit code 2 if minor deviations only (proceed with documentation)

The promotion gate (`references/pure_research/pr_promotion_gate.md`)
requires `prereg_diff.py` to have been run with exit code 0 or 2 and
the deviation log on file.

## HARKing prevention discipline

Pre-registration is enforcement, not a suggestion. The following
patterns are explicitly prohibited:

- **Post-hoc pre-registration**: writing a pre-registration after the
  trial has run, claiming it was the plan all along. The hash-lock
  prevents this — `prereg_freeze.py` records the timestamp and
  refuses to backdate.
- **Multiple pre-registrations**: writing several pre-registrations
  with different test designs and only "registering" the one that
  the data supports. Detected by `validate_ledger.py` (any prereg
  not used by a trial that ran is flagged for review).
- **Trial-and-retry**: running a trial, ignoring the result, modifying
  the test design, and re-running. Each rerun is a new trial under a
  new pre-registration. The original trial's result is part of the
  trial count for multiple-testing correction.
- **Selective reporting**: running multiple secondary tests and
  reporting only those that support the finding. The pre-registration
  must enumerate all secondary tests; results must be reported for
  all of them, not just the favorable subset.
- **Goalpost shift**: changing thresholds after seeing the data
  ("the trial showed primary metric difference -0.4, just under the -0.5
  threshold; let's say -0.3 was the threshold"). Detected as a major
  deviation by `prereg_diff.py`.

The structural defense: anything that requires changing the
pre-registration after seeing the data is a deviation that must be
documented; if the deviation is "major" per the severity matrix, the
trial is invalidated and a new pre-registration is required.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Vague competing explanations | E1/E2 are paraphrases of each other | Each E must predict a distinct observable pattern |
| Single explanation only | "We will test if benchmark reliability decayed" without alternatives | Force ≥2 explanations + null |
| No expected diff predictions | "We'll compute primary metric and see" | Each E must have an ex ante predicted observation |
| Multiple testing under-reporting | "We tested one hypothesis" when 3 sub-strategies were swept | Honest trial count for selection-adjusted statistic / Bonferroni |
| No stop condition | Trial drifts indefinitely | Specific observable condition for trial end |
| Pre-reg post-trial | Hash timestamp falls after trial timestamp | `prereg_freeze.py` blocks; the pattern is detectable |

## Relationship to other references

- Pre-conditions for pre-registration: `references/pure_research/prfaq.md`
  (PR/FAQ frozen first) and `references/shared/literature_review.md`
  (targeted literature complete)
- After pre-registration freeze: trial may run. Post-trial,
  `references/pure_research/pr_workflow.md` § Deviation severity matrix
  decides what counts as minor vs major deviation.
- The promotion gate
  (`references/pure_research/pr_promotion_gate.md`) requires:
  - Pre-reg hash matches lock file
  - prereg_diff exit code 0 or 2
  - Deviation log on file
- project-specific multiple-testing plan for trial-count discipline
  (Romano-Wolf, Harvey t > 3.0, Bonferroni, selection-adjusted statistic).
