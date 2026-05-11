# result_analysis.md

Decomposition patterns for trial results — applied symmetrically to
**failure** and **success**. Generic terminal labels ("noise", "regime",
"model is good") are forbidden as final claims; both sides must reach
mechanism-level explanations to count as research.

## When to read

- Writing the Analysis section of a trial notebook for Capability /
  Technology Research or Phenomenon / Mechanism Research
- Interpreting a failed or ambiguous trial
- Interpreting a positive / "successful" trial — the same rigor applies
- About to write "the result was X because Y" in any deliverable

## The principle

A failure with the explanation "the model failed because of noise" is
A1 with a generic terminal label — not research.

A success with the explanation "the model worked because GBM is good
at variance" is **also A1 with a generic terminal label — not research
either**.

The same decomposition discipline applies to both. The skill enforces
this symmetry because agents (and humans) systematically apply rigor
to failure but skim past success.

After decomposition, route the result back to the selected workstream state
object: Phenomenon / Mechanism Research updates Q/E state in
`explanation_ledger.md`; Capability / Technology Research updates capability
state in `capability_map.md`. Result writeups are evidence artifacts, not
state owners.

## Generic terminal labels — forbidden as final explanations

These labels are **starting points for decomposition, not endpoints**.
Using them as the final explanation is a protocol violation.

### Failure-side generic labels

| Label | Decomposition required |
|---|---|
| "noise" | Sample-size sufficient? Variance estimate? Noise distribution shape? Why this specific signal-to-noise pattern? |
| "data quality" | Which specific data field failed? At which timestamps? Magnitude of bad-data fraction? Pattern (random vs systematic)? |
| "sample size" | Power analysis at observed effect size? What N would be sufficient? Why is N insufficient *for this specific test*? |
| "regime" | Which regime characteristics (vol, correlation, momentum)? Threshold values that distinguish? When did the regime begin/end? |
| "overfitting" | Which parameters were over-tuned? In-sample vs out-of-sample diff magnitude? Number of degrees of freedom vs sample size? |
| "cost" | Effect before cost or constraint? Resource usage? Exposure duration? Break-even threshold? Whether impact is uniform or context-dependent? |
| "model weakness" | Which specific assumption is violated? Which alternative model class would address this? Why this model was selected initially? |
| "operating context changed" | What specifically changed? When? Measurable on which axis? |

### Success-side generic labels (commonly skipped)

| Label | Decomposition required |
|---|---|
| "model was good" | Which model components drove the result? Feature importance distribution? Comparative test against simpler model? |
| "model captured variance" | Which dimensions of variance specifically? Which decomposition (PCA, sector, factor)? Where does it fail? |
| "context was favorable" | Which context characteristics? Threshold values? Why did the method align with those characteristics specifically? |
| "feature was strong" | Which feature? Standalone IC? Marginal contribution above baseline? Stability across sub-periods? |
| "data was clean" | Which preprocessing fixed which issue? Magnitude of cleaning effect? What if cleaning was undone? |
| "method is sound" | Which causal mechanism produces the effect? What would falsify it? |
| "training worked" | Which training-loop properties (loss curve shape, gradient norms, generalization gap)? |
| "effect was strong" | Effect magnitude in absolute terms (not "strong"). Comparison to known benchmarks. Decay rate. |

## Symmetric decomposition pattern

For both success and failure, walk through these steps:

### 1. State the observation precisely

Numerical, with uncertainty bands. No qualifiers like "good" or "bad".

- Bad: "The model worked well."
- Good: "Held-out agreement delta = 0.045 (bootstrap 95% CI
  [0.022, 0.068]) on benchmark cohort C, 2018-2024."

### 2. Decompose into ≥3 candidate mechanisms

Why this observation? List multiple candidate causal mechanisms.

For success:
- Bad (1 candidate): "GBM captured non-linear feature interactions."
- Good (3 candidates):
  - (a) GBM captured a specific non-linear interaction between
    momentum and volume features
  - (b) The 2018-2024 OOS period happened to favor cross-sectional
    strategies due to higher idiosyncratic dispersion
  - (c) Survivorship bias in the universe filter inflated apparent IC

For failure:
- Bad (1 candidate): "The model didn't generalize."
- Good (3 candidates):
  - (a) Distribution shift between train and OOS periods (covariate
    drift)
  - (b) Hyperparameter selection was overfit to validation data
  - (c) The signal genuinely decayed due to crowding / regime change

### 3. Evidence weighing per candidate

For each candidate, list supporting and weakening evidence with type
(numerical / structural-argument / literature-reference /
null-result-of-X).

The discipline that prevents narrative drift: **structural-argument
alone cannot support an A4 claim**. At least one numerical evidence is
required.

### 4. Eliminate or weaken candidates

For each non-primary candidate, what specific test or evidence weakens
it? If you cannot weaken a candidate with current data, the analysis
remains at A2 (≥1 alternative identified but not discriminated) and
needs more work.

### 5. State what remains

After elimination, which candidate(s) survive? If multiple survive,
the analysis is at A3 (preliminary) at best. If one candidate survives
with mechanism + scope + multiple evidence sources, it reaches A4.

## Cost / resource decomposition (failure-side specific)

A common failure-side anti-pattern: "cost or constraints killed the result."
This is a generic label. Decomposition required:

- Effect magnitude before cost or constraint (specific number, not "small")
- Resource-use and exposure-duration distribution
- Break-even cost, latency, capacity, availability, or constraint threshold
- Whether the impact is uniform across the period or context-dependent
- Whether the favorable context can be identified ex ante
- Whether the result changes because the **implementation assumption**
  changed or because the **phenomenon is conditional**

A lower-cost or lower-constraint re-run is a sensitivity check on an existing
explanation, not a new hypothesis, unless it corresponds to a real documented
implementation context.

## Mechanism-level success decomposition (success-side specific)

A common success-side anti-pattern: "the model captured the variance
structure." This is a generic label. Decomposition required:

- **Which specific variance components** does the model capture
  (e.g., group, scale, context, or usage-intensity components)?
- **Marginal contribution** of each: ablate one feature at a time and
  measure the primary-metric change
- **Mechanism**: why is this specific component captured by this
  specific model architecture but not by a simpler baseline?
- **Scope**: in which populations / periods / contexts does the capture
  hold? Where does it break?
- **Comparative test**: does a simple baseline (linear model,
  rolling moving average, hand-crafted feature) achieve the same?
  If yes, the model's contribution is overstated.

## Required Failure / Ambiguity Analysis Block

For any miss / ambiguous result, write:

```markdown
## Failure / ambiguity analysis for <trial>

### Observed pattern
[Numbers and plots, stated without interpretation.]

### Immediate non-conclusions
[Things the result does NOT prove. Example: "agreement delta < 0.02 does NOT
prove the mechanism is absent — it could be context-conditional, the test
window may be unfavorable, or the threshold is too tight."]

### Candidate explanations (≥3)
| ID | Explanation | Evidence for | Evidence against | Test that would distinguish |
|---|---|---|---|---|
| E1 | ... | ... | ... | ... |

### Decomposition of any generic labels used
[If using labels like noise/regime/data quality, break into observable
sub-claims per the table above.]

### What became weaker
[Which explanation or hypothesis lost support, and why.]

### What remains alive
[Which explanations still survive.]

### Next smallest discriminating test
[Smallest next action that separates live explanations.]
```

## Required Success Analysis Block

The same structure applies to success — symmetry is the protocol's
defense against agent / human bias.

```markdown
## Success analysis for <trial>

### Observed pattern
[Numbers and plots, with uncertainty bands. No "good" qualifiers.]

### Immediate non-conclusions
[Things the result does NOT prove. Example: "primary metric improved out of
sample does NOT prove the method will hold in production; it could be context-
specific, sample-period favorable, or fragile to operational constraints."]

### Candidate mechanisms (≥3)
[Why did this work? List multiple candidate causal mechanisms.]

### Decomposition of any generic labels used
[If using labels like "model was good" or "data was clean", break
into observable sub-claims per the table above.]

### Evidence weighing per candidate
[Supporting + weakening evidence per candidate, with evidence type.]

### Mechanism that survives elimination
[After eliminating non-primary candidates, which survives? Cite the
discriminating evidence.]

### Scope precision
[Where this mechanism holds: population, period, context, operating
structure preconditions. Where it does NOT hold or is untested.]

### Next test that would falsify the mechanism
[The most useful next trial is one that could falsify the surviving
mechanism, not one that could confirm it further.]
```

## Prohibited endings

Both failure and success analysis must avoid:

- "The hypothesis was rejected because the data is noisy."
- "The model failed because the market regime changed."
- "The signal worked because the model is powerful."
- "Performance was good because of feature engineering."
- "More data is needed."
- "Try another parameter."
- "The result speaks for itself."

Allowed ending shapes:

- "E2 is weaker because observation O contradicts prediction P. E1
  and E3 remain active. The next discriminating test is T because
  it separates E1 from E3 on observable axis A."
- "Mechanism M survives elimination of alternatives X and Y by
  evidence Z. Scope: universe U, period P. The mechanism would be
  falsified by observation Q, which the next trial can test on data
  D."

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Generic label as terminal | "It failed because of noise" | Decompose per table; analysis is incomplete until mechanism level |
| Asymmetric rigor | Detailed failure analysis, "looks good" success analysis | Apply symmetric structure; force success decomposition |
| Single candidate mechanism | "GBM was the right model" | List ≥3 candidates including null/coincidence |
| Narrative as evidence | "The model clearly captured X" | Per `analysis_depth.md` § 5.3, narrative is not evidence; numerical required |
| Confirmation bias in next test | Next test designed to support the surviving mechanism | The most useful next test falsifies, not confirms |

## Relationship to other references

- `references/shared/analysis_depth.md` — A0-A5 tier system; this file
  describes the decomposition that advances from A0 to A4
- `references/rd/rd_promotion_gate.md` § C — generic terminal label
  prohibition for `matured` capabilities
- `references/pure_research/pr_promotion_gate.md` § E — same for
  `supported` claims
- `references/review/conclusion_review.md` — checks for generic labels
  on both sides as part of conclusion review
- `assets/rd/rd_trial.py.template` § 5 and
  `assets/pure_research/pr_trial.py.template` § 6 — Analysis section
  templates that operationalize this decomposition

## Migration note

This file extends the older failure-decomposition note into symmetric
success-and-failure analysis. The current version treats both outcomes under
the same analysis-depth standard.
