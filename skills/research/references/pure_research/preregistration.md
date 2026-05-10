# preregistration.md

AEA-style Pre-Analysis Plan (PAP) — the planned design document that
the trial must follow. Pre-registration is the single most effective
intervention against p-hacking and post-hoc rationalization. In this skill it
is mandatory for Pure Research trials that may support a claim, promote an
explanation to `supported`, or be shared externally as load-bearing evidence.
Exploratory probes may remain lightweight, but must be rerun under a reviewed
pre-registration before they become claim-cited.

## When to read

- Designing a Pure Research trial (after PR/FAQ is ready and targeted
  literature is done)
- Reviewing whether a deviation from pre-registration is acceptable
- Running post-trial deviation review

## Purpose

Pre-registration states the **question, competing explanations, test design,
and expected outcomes** before any data is inspected. After the trial, compare
the actual analysis against the pre-registration and record material
deviations. Minor deviations can be carried forward; major deviations require a
fresh trial before the result can support a claim.

The mechanism: HARKing (Hypothesizing After Results are Known) and the garden
of forking paths are reduced when the design is written before the data is
touched. Without pre-registration, finding-driven narrative shifts are too easy
to rationalize.

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
Data: <source, reference if available, period, frequency>
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
> - Data: public benchmark review records, period 2010-01 through 2024-12,
>   data version a3f8...
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
> - If E2 (annotation drift) true: review-rubric change count increases > 2x;
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

## Reviewing the pre-registration

After the document is complete and reviewed:

1. Change `Status: DRAFT` to `Status: READY`.
2. Run the trial under that PR ID.
3. Do not silently change the plan after seeing data.

If a load-bearing change is needed after data inspection, record it as a
deviation and apply the severity matrix in
`references/pure_research/pr_workflow.md`. Major deviations require a new
pre-registration and a new trial.

## Post-trial comparison

After the trial, compare the actual trial artifact against the written
pre-registration and record only material differences. The comparison should
cover:

- the cited `prereg/PR_<id>.md`
- actual data source / version versus the planned data identity
- sample size, period, population, and split
- test statistic and primary metric definition
- multiple-testing count and correction
- any threshold, stop-condition, or competing-explanation changes

Classify deviations with `references/pure_research/pr_workflow.md`. Minor
deviations can be documented and carried forward. Major deviations invalidate
the claim-cited use of that trial; use a new pre-registration for the changed
question or design.

## HARKing prevention discipline

Pre-registration is enforcement, not a suggestion. The following
patterns are explicitly prohibited:

- **Post-hoc pre-registration**: writing a pre-registration after the
  trial has run, claiming it was the plan all along. Treat that trial as
  exploratory; it cannot be claim-cited without a fresh trial under a reviewed
  pre-registration.
- **Multiple pre-registrations**: writing several pre-registrations
  with different test designs and only using the one that the data supports.
  Treat unused alternatives as drafts or future-trial plans; do not use them to
  justify the completed trial.
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
  deviation by `deviation review`.

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
| Pre-reg post-trial | pre-registration was written after the result was known | Treat the trial as exploratory; rerun under a valid pre-registration before citing it |

## Relationship to other references

- Pre-conditions for pre-registration: `references/pure_research/prfaq.md`
  (PR/FAQ ready first) and `references/shared/literature_review.md`
  (targeted literature complete)
- After pre-registration review: trial may run. Post-trial,
  `references/pure_research/pr_workflow.md` § Deviation severity matrix
  decides what counts as minor vs major deviation.
- The promotion gate
  (`references/pure_research/pr_promotion_gate.md`) requires:
  - the cited pre-registration was ready before the trial
  - deviations are classified and major deviations are not used as claim-cited evidence
  - deviations are documented
- project-specific multiple-testing plan for trial-count discipline
  (Romano-Wolf, Harvey t > 3.0, Bonferroni, selection-adjusted statistic).
