# prfaq.md

Amazon "Working Backwards" PR/FAQ — the entry document for a Phenomenon /
Mechanism Research workstream. Write the press release for the finding you
would publish if research succeeded, then anticipate the skeptical reviewer's
questions.

## When to read

- The very first step of any Phenomenon / Mechanism Research workstream, before literature
  search, pre-registration, or trial design
- When a Phenomenon / Mechanism Research workstream's question feels unfocused
- Before handing off from a Capability / Technology Research workstream to a
  Phenomenon / Mechanism Research workstream

## Purpose

The PR/FAQ forces the question to be **scoped before the search**. Without
a press release and the questions a skeptical reviewer would ask, the
literature search drifts, the pre-registration is premature, and the
trial design has no anchor.

The acid test: **if you cannot write a coherent PR/FAQ, the question is
not ready**. This is not a failure — it is a signal to refine the
question before investing in trials.

The PR/FAQ is a planning document. Once it has `Status: READY`, do not silently
rewrite load-bearing claims, mechanisms, scope, alternatives, evidence type, or
promotion language. Material changes after trial work begins are deviations and
belong in `decisions.md`.

## Two parts

### Part 1: Press Release (1 page maximum)

Imagine the finding has been completed and you are publishing it. Write
the press release as if announcing to a skeptical domain audience.
The format:

```markdown
**[Date] — [Headline that states the finding in 1 sentence]**

[Lead paragraph: what was found, in concrete terms. State the phenomenon,
the mechanism, and the scope conditions.]

[Supporting paragraph: the discriminating evidence — what alternative
explanations were ruled out, and how. Cite the type of evidence
(numerical / structural / null-result).]

[Implications paragraph: what changes downstream of this finding —
practitioners, theory, future research. Be honest about scope.]

[Closing: what was NOT shown — the limits of the finding, what next.]
```

Length: 200-400 words. **One page**, hard limit.

### Part 2: FAQ (skeptical questions)

Anticipate the questions a critical reviewer would ask. The FAQ is where
honesty about limitations and scope becomes structural. Typical
question categories:

- **Statistical sufficiency**: How was multiple testing handled? What is
  the effect size / uncertainty interval adjusted for the trial count?
- **Robustness**: What happens in different regimes / sub-periods /
  sub-universes?
- **Mechanism**: Why does this mechanism produce this effect? Walk
  through the causal chain.
- **Alternatives**: What competing explanations were considered? What
  evidence weakened them?
- **Replication**: Does this hold on independent data sources?
- **Scope**: Where does this NOT apply? Be explicit.
- **Practical implication**: If a practitioner used this, what would they
  do differently? At what cost?
- **HARKing risk**: Was the analysis planned before interpreting the result?
  State the planned design and any material deviations.

10-20 FAQ entries is typical. Each gets a 1-3 sentence answer.

## Good vs bad PR/FAQ

### Bad PR

> "We trained a transformer model on event-sequence data and found it
> predicts the target with high accuracy. The methodology is novel and
> applicable broadly."

Problems: no concrete finding, no scope, no mechanism, no alternatives
ruled out. This is an ML demo, not a research finding.

### Good PR

> **[2026-XX-XX] Measurement reliability in public benchmark datasets
> declined 80% in 2020-2024 vs 2010-2019 due to annotation drift,
> not model degradation.**
>
> Primary agreement score for measurement reliability reviews dropped from
> 1.8 (2010-2019) to 0.4 (2020-2024). Bootstrap
> 95% CI on the difference is [-1.65, -1.05], p < 0.01 after Bonferroni
> correction across 3 benchmark families.
>
> Independent review logs show the labeling rubric changed twice over
> 2020-2024. The measurement-noise stability test weakens the alternative
> explanation that the underlying task distribution changed fundamentally.
>
> Two subdomains confirm the pattern with directionally consistent decay
> magnitudes (-78% and -82% respectively).
>
> The finding suggests benchmark comparisons should not treat older and newer
> labels as interchangeable. It does NOT establish whether the drift will
> persist or whether the same effect appears in private datasets.

Why this is good: concrete metric, scope precise, alternative ruled out
with evidence type, replicated, limits stated explicitly.

### Bad FAQ

> **Q: Is this just data mining?**
> A: We don't think so.

Problem: hand-wave. Reviewer will press; this is a thin defense.

### Good FAQ

> **Q: Is this just data mining? How many strategies were tested before
> selecting this one?**
> A: This was a single pre-registered hypothesis, not a search. The
> pre-registration `prereg/PR_001.md` specified the test as "rolling 3-year
> primary metric with bootstrap CI on measurement reliability returns", with 3
> competing explanations
> (annotation drift, task-distribution shift, null). No alternative test designs were
> tried. The Bonferroni correction across the 3 sub-strategies
> (text, image, and tabular benchmark families) gives p < 0.01.

## How the PR/FAQ blocks downstream work

Without a reviewed PR/FAQ:

- **Literature search is unfocused**. You don't know what to search
  for; you'd browse "benchmark reliability" generally instead of
  "annotation drift + benchmark reliability + 2020s protocol change".
- **Pre-registration is premature**. You don't know what competing
  explanations to enumerate, what test to design, or what to predict
  under each explanation.
- **The promotion gate has no anchor**. The "discriminating test against
  ≥1 serious alternative passed" requirement is meaningless if the
  alternatives weren't named upfront.
- **HARKing risk is high**. Without a reviewed PR/FAQ, finding-driven
  rationalization is undetectable.

If the user pushes to "skip PR/FAQ and just look at the data", the
response is: looking at the data first is a shopping trip. Once you
have seen the data, the PR/FAQ you produce is an artifact of the data
you saw, not of the question you wanted to answer.

### Orientation search is allowed

Writing the PR/FAQ requires naming **mechanisms** and **alternatives**
upfront. For a researcher unfamiliar with the domain, this can create a
bootstrap problem: how do you name plausible mechanisms without first
reading the relevant literature?

**Light orientation search is allowed and expected** before PR/FAQ:

- Read 3-5 review papers / canonical references on the phenomenon
  (typically 30-60 minutes of reading)
- Browse abstracts to surface candidate mechanisms and known
  alternatives
- Note: this is **not** the targeted literature search of step 2
  (which happens after PR/FAQ scoping); it is prior-knowledge
  bootstrapping

The prohibition that remains in force during orientation search:

- **No data inspection** (no plot of the actual returns / regimes /
  metrics being studied)
- **No trial execution** (no model fits, no evidence-producing runs, no metric
  computed on real data)

The line: orientation search recalls **prior knowledge**; data
inspection produces **new knowledge** that would shape the PR/FAQ
post-hoc.

If you find yourself unable to write a coherent PR/FAQ even after
orientation search, that is itself a signal — the question may not be
ready, or the domain expertise required is missing.

## Reviewing the PR/FAQ

After Part 1 and Part 2 are complete and reviewed, change `Status: DRAFT` to
`Status: READY`.

After review, **do not silently rewrite `prfaq.md` for load-bearing changes**.
Any change requires a deviation entry in `decisions.md`. Frequent deviations
to PR/FAQ are a sign the question was not ready — next
project, spend more time on this step.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| PR has no concrete finding | "We will study benchmark reliability" (intent, not finding) | Re-write as if research succeeded; the PR is the post-success announcement |
| FAQ is shallow | 3-5 surface questions | Imagine a senior reviewer; what 15 questions would they ask? |
| Mechanism unstated | "primary metric declined" without explanation | Mechanism is part of the finding; if you can't state one, the question is not ready |
| Scope unstated | Universal claim ("the benchmark is unreliable") | Scope must be precise (public benchmark v2, review subset, 2020-2024) |
| HARKing-vulnerable PR | Question phrased to fit known data ("we found that 2020-2024 differs from 2010-2019") | Re-frame ex ante: was this prediction made before looking at the data? If not, the PR is post-hoc |

## Relationship to other references

- After PR/FAQ is ready → read `references/shared/literature_review.md`
  for targeted literature search (now scoped by the PR/FAQ).
- Then `references/pure_research/preregistration.md` for the formal
  pre-analysis plan (PAP), which formalizes the test design.
- Then `references/pure_research/explanation_ledger_schema.md` for the
  state object that tracks question / explanation pruning.
- The PR/FAQ feeds directly into `references/pure_research/imrad_draft.md`
  — the IMRAD draft's Discussion section answers the FAQ as a starting
  point.
- See `references/pure_research/pr_promotion_gate.md` for the
  pre-promotion checklist; the PR/FAQ being on file is a hard
  pre-condition.
