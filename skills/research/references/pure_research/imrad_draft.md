# imrad_draft.md

The deliverable shape for Pure Research. An IMRAD-structured manuscript
draft (Introduction, Methods, Results, Discussion) is the proof that
the project's findings can be communicated to a critical reviewer. A
project cannot promote without a producible IMRAD draft.

## When to read

- Approaching the promotion gate for a Pure Research claim
- Generating a draft via `scripts/draft_imrad.py`
- Reviewing whether a draft meets sufficiency conditions
- Translating a `supported` E-row into communicable form

## Why IMRAD and not just "supported"

A "supported" status flag is a bookkeeping marker. It does not prove
the finding can be defended. The IMRAD draft proves it: by walking
through introduction, methods, results, and discussion, the agent
demonstrates that the explanation has a coherent narrative supported by
the actual evidence in the project.

A project that cannot produce a coherent IMRAD draft has not actually
supported its claim, regardless of what the explanation_ledger says.

## IMRAD structure

The draft has four sections, in order. Past tense for Methods and
Results; present tense for theory in Introduction and Discussion.

### Section 1: Introduction (~300-500 words)

Opens with the phenomenon, situates the research question in prior
work, states the gap, states the contribution.

```markdown
## 1. Introduction

[Paragraph 1: phenomenon]
The phenomenon under study is [...]. It matters because [...].

[Paragraph 2: prior work and its limits]
Prior work has established [...] (cite literature/papers.md §A, §B).
However, prior work has not addressed [the gap], specifically [...].

[Paragraph 3: this study's contribution]
This study tests or explores [research question, copied from PR/FAQ Part 1
headline + qualifications]. The planned Study Information, Hypotheses /
Exploratory Objective, Analysis Plan / Allowed Transformations, and
Transparent Changes policy are listed in `prereg/PR_<id>_<slug>.md`. The
discriminating or diagnostic evidence is [...].
```

The Introduction must:
- Cite ≥3 prior works (from `literature/papers.md`)
- State the research question matching the PR/FAQ
- Identify the pre-registration file used for the trial
- State the contribution in 1 sentence

### Section 2: Methods (~400-600 words)

How the trial was conducted, in enough detail that a different agent
could re-run it. Past tense throughout.

```markdown
## 2. Methods

### 2.1 Pre-registration
Study Information; Hypotheses / Exploratory Objective; Design Plan /
Exploration Scope; Analysis Plan / Allowed Transformations; Inference /
Decision Criteria or Selection or Follow-Up Criteria; Data Exclusion / Missing
Data Handling or Expected Outputs; and Transparent Changes policy. Available at
`prereg/PR_<id>_<slug>.md`.

### 2.2 Data
Source, period, frequency, and data version. Universe scope.

### 2.3 Sample
How data was split (train / val / test, holdout replication, repeated holdout, etc.).
Sample size (N) per split.

### 2.4 Test design
Primary metric or exploratory output. Secondary metrics. Threshold for
support / weaken / reject from Inference / Decision Criteria, or selection
criteria for exploratory work. Multiple-testing correction method when
applicable (Bonferroni / Romano-Wolf / domain-appropriate selection
correction).

### 2.5 Transparent Changes from pre-registration
Copy the report package Transparent Changes section. For each material
change, state what changed, why, and its effect on study results or
conclusions. If no material changes occurred, state "No material changes
from the preregistration."

### 2.6 Reproducibility
Data version, code commit, environment pin, and random seed(s).
```

Methods must:
- Identify the pre-registration file used for the trial
- Summarize Study Information, Hypotheses / Exploratory Objective, Analysis
  Plan / Allowed Transformations, Design Plan / Exploration Scope, Data
  Exclusion / Missing Data Handling or Expected Outputs, and Transparent Changes
- Provide reproducibility 3-tuple

### Section 3: Results (~300-500 words)

Observations only. No interpretation. Past tense. Numbers, tables,
figure references. No "the result suggests" language.

```markdown
## 3. Results

### 3.1 Headline finding
[Single number with uncertainty band, e.g., "primary metric dropped
from 1.8 (95% CI [1.5, 2.1]) in 2010-2019 to 0.4 (95% CI
[0.1, 0.7]) in 2020-2024."]

### 3.2 Per-explanation observations
[For each hypothesis, competing explanation, or exploratory objective
enumerated in Methods, what was observed. Match against Methods § 2.1
Hypotheses / Exploratory Objective and Methods § 2.4 Analysis Plan /
Allowed Transformations.]

- **E1 (regime change)**: [observation, e.g., "Vol-of-vol metric
  remained stable across periods (rolling 60-day measurement-noise
  unchanged within ±5%)."]
- **E2 (crowding)**: [observation, e.g., "CFTC COT non-commercial
  vol-seller positioning grew 4× over 2020-2024; primary metric difference
  correlates r=0.62 with positioning growth."]
- **E_null**: [observation, e.g., "Bootstrap 95% CI on primary metric
  difference excludes 0 (lower bound -1.65, upper bound -1.05)."]

### 3.3 Robustness
[Sub-period breakdown, sub-universe replication, sensitivity to
parameter choice. Numbers only.]

### 3.4 Verification checks
[Pass / fail status of each relevant check from
generic verification or domain-adapter implementation checks.]
```

Results must:
- Match the Hypotheses / Exploratory Objective and the Analysis Plan /
  Allowed Transformations stated in Methods
- Include uncertainty bands or CIs on every numeric claim
- Pass the sanity check subset relevant to this trial type

### Section 4: Discussion (~400-700 words)

Interpretation, scope conditions, alternatives weighed, limitations,
future work. **A4+ analysis required** per `references/shared/analysis_depth.md`.

```markdown
## 4. Discussion

### 4.1 Interpretation
[The mechanism that the evidence supports. Cite Section 3
observations.]

The evidence supports E2 (crowding): [reasons, citing specific
observations]. The mechanism is [causal chain]. The scope is
[precise boundaries — universe, period, market structure
preconditions].

### 4.2 Alternatives weighed
[For each rejected / weakened E, explain why the evidence weakens
it. Not "we believe E1 is wrong" but "E1 predicted X, observation
showed Y, this evidence weakens E1 because..."]

### 4.3 Negative claims (if applicable)
[Any explanations that were rejected with discriminating evidence
become negative findings. Document them as negative claims with
the same A4+ analysis.]

### 4.4 Limitations
[Honest list. Sample size constraints, period dependence, scope
exclusions, assumptions of the test design. The reviewer will
identify these; better to name them upfront.]

### 4.5 Future work
[The next discriminating questions the finding suggests. May spawn
a sub-question Q-row in `explanation_ledger.md`, or a sibling
project.]
```

Discussion must:
- Reach analysis tier A4 minimum (mechanism named, alternatives
  excluded, scope precise, multiple sources of supporting evidence)
- For A5 promotion (assertion-level): demonstrate replication across
  instruments / periods / out-of-sample, plus an external prediction
  that holds
- Avoid generic terminal labels ("the data supported the hypothesis"
  without mechanism is forbidden — see `references/shared/result_analysis.md`)
- Document negative claims with the same rigor as positive claims

## Sufficiency conditions for promotion

The IMRAD draft is "producible" (sufficient for promotion review)
when:

- [ ] All four sections exist and meet length / content requirements
  above
- [ ] Methods identifies the pre-registration file and records Transparent
  Changes
- [ ] Results contains observations matching the Hypotheses / Exploratory
  Objective and Analysis Plan / Allowed Transformations in Methods
- [ ] Discussion reaches A4+ analysis depth
- [ ] No generic terminal labels in Discussion
- [ ] Negative claims (if any) are documented with mechanism and
  evidence
- [ ] Limitations section is honest (not "no significant limitations")
- [ ] Report provenance recorded for presented evidence

The promotion gate (`references/pure_research/pr_promotion_gate.md`)
checks each of these as part of the conclusion review.

## Lifecycle of the IMRAD draft

The IMRAD draft is **started early**, not at the end. Specifically:

- **After PR/FAQ**: Section 1 (Introduction) draft can be partially
  written from the PR/FAQ Part 1 (the press release becomes the
  contribution paragraph)
- **After pre-registration**: Section 2 (Methods) § 2.1 and § 2.4
  can be written from the pre-registration
- **After each trial**: Section 3 (Results) accumulates observations
- **Before promotion**: Section 4 (Discussion) is written, and all
  earlier sections are revised for coherence

This staged approach prevents the failure mode where the IMRAD draft
is treated as a write-up tax at the end. By starting it after PR/FAQ,
the IMRAD draft is a continuously updated artifact that surfaces
inconsistencies early.

## Tone and writing conventions

- **Past tense**: Methods (what was done), Results (what was
  observed)
- **Present tense**: Introduction (state of knowledge),
  Discussion (interpretation, theory)
- **Active voice** where it doesn't add wordiness, passive where
  conventional ("the model was trained on")
- **Specific numbers** instead of vague qualifiers ("primary metric 1.2"
  not "high primary metric")
- **Cite specific evidence** for every claim: "the model overfit
  (validation accuracy 0.45 vs train 0.92)" not "the model
  overfit"
- **No hedging without specifics**: "may apply more broadly"
  is a future-work statement, not a finding
- **Negative claims as positive statements**: "The data does not
  support E1 because [evidence]" is preferred to "It is unclear
  whether E1 holds"

## Generating the draft

`scripts/draft_imrad.py` produces a first draft from project artifacts:

```bash
python scripts/draft_imrad.py --project <project-name>
```

It reads:
- `prfaq.md` for Section 1 contribution
- `prereg/PR_<id>_<slug>.md` for Section 2 Study Information, Hypotheses /
  Exploratory Objective, Design Plan / Exploration Scope, Analysis Plan /
  Allowed Transformations, Data Exclusion / Missing Data Handling or Expected
  Outputs, and Transparent Changes
- `explanation_ledger.md` for Section 3 (per-explanation observations
  from `current_evidence_summary` of each E)
- `decisions.md` for state transitions and Transparent Changes entries
- `results/results.parquet` for headline metrics (filter by E-IDs
  with status `supported` or `rejected` for the active Q)
- `literature/papers.md` for Section 1 citations

The generated draft is a **starting point**, not a final manuscript.
The agent (or user) must:
- Add narrative paragraphs that the script cannot generate from
  structured data
- Reconcile any inconsistencies between artifacts (e.g., the PR/FAQ
  said one thing, the trial result says another — this gap must be
  addressed in the Discussion)
- Write the limitations and future work sections
- Verify the cited pre-registration file and reproducibility notes

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Discussion uses generic labels | "The model did well because GBM is good at variance" | Per `result_analysis.md`, decompose into mechanism-level claims |
| Methods skips Transparent Changes | Section 2.5 says "No material changes from the preregistration." but trial notes or the report package show material changes | Always list material changes, including rationale and effect |
| Results contains interpretation | "The primary metric declined, suggesting crowding" | Move to Discussion; Results is observation only |
| No negative claims when E was rejected | E2 status `rejected` in ledger but Discussion only discusses E1 supported | Add Discussion § 4.3 negative claim with same A4 rigor |
| Unrealistic limitations | "No significant limitations" | Identify ≥3 honest limitations |
| Pre-registration not cited | Section 1 doesn't mention the pre-registration file | Without the file citation, planning-integrity risk is high; cite it |
| IMRAD generated only at the end | First draft attempted at promotion gate, found to be incoherent | Start early per § Lifecycle |

## Relationship to other references

- Pre-conditions: `references/pure_research/prfaq.md` (drives § 1
  contribution), `references/pure_research/preregistration.md`
  (drives § 2 methods), `references/pure_research/explanation_ledger_schema.md`
  (drives § 3 results and § 4 discussion)
- Post-condition: `references/pure_research/pr_promotion_gate.md`
  (the promotion gate verifies the draft against sufficiency conditions
  here)
- Analysis depth requirement: `references/shared/analysis_depth.md`
  (A4 minimum for Discussion)
- Generic label prohibition: `references/shared/result_analysis.md`
- Generation: `scripts/draft_imrad.py` (Phase 5)
