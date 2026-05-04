---
name: experiment-review
description: Use when about to declare verdict='supported' on any experiment in a quant-research project (mandatory co-gate with bug_review; both must pass). Also use when the user asks for a review of a notebook / experiment / project, at end-of-research-cycle gates, before external sharing / publication / any deployment recommendation, and when inheriting a notebook that needs a fresh-eyes assessment. Asks whether the claim is warranted by what was actually tested — distinct from bug_review which asks whether the implementation is correct. Both layers required for verdict='supported'.
---

# Experiment Review

A review skill for quantitative-research experiment notebooks. It asks:
**is the conclusion warranted by what was actually tested?** This is
orthogonal to implementation correctness; `bug_review` answers whether
the code and numbers are contaminated.

## When to use

- A user asks for a review of a notebook, experiment, or project
- Before declaring `verdict = "supported"` on any experiment in a
  quant-research project
- End of a research cycle, before deciding the next cycle
- Before external sharing, publication, or deployment recommendation
- When inheriting a notebook and needing a fresh-eyes assessment

## When NOT to use

- The user wants implementation correctness checked. Use `bug_review`
  inside `quant-research` first. A clean experiment-review on top of a
  buggy implementation only creates confidence in contaminated evidence.
- The notebook is at orientation / brainstorm stage and no claim exists.
  Wait until there is a conclusion to review.

## Boundary against `bug_review`

Both layers are required for `verdict = "supported"`.

| | `bug_review` (in `quant-research`) | `experiment-review` |
|---|---|---|
| One-line | Are the code and numbers correct? | Is the claim warranted by the design? |
| Question answered | "Is the implementation contaminated?" | "Is the claim oversold relative to evidence?" |
| Looks at | Code, data, PnL series | Hypothesis, universe, baselines, claim, notebook artifact |
| Specialist coverage | leakage / pnl-accounting / validation correctness / statistics / code-correctness | question / scope / method / validation sufficiency / claim / literature / narrative |
| Adversarial bundle | code + reported numbers | `.py` file alone |
| Order | Precondition | Postcondition |
| Verdict gate | **Both must pass.** | **Both must pass.** |

The `validation` overlap is subtle:

- `bug_review` validation checks whether embargo / purging / splits are wired
  correctly.
- `experiment-review` validation checks whether the corrected validation design
  has enough power to support the claim.

## Core principle

**Four reviewer agents: three grouped specialists plus one adversarial
cold-eye reviewer.**

The specialist groups preserve the old coverage while reducing dispatch cost:

1. **research-design**: question, scope, and method
2. **evidence-sufficiency**: validation sufficiency and claim discipline
3. **context-communication**: literature coverage and notebook narrative
4. **adversarial**: `.py` file alone, with project context withheld

The first three reviewers share the relevant project bundle and read only their
own grouped section from `references/review_dimensions.md`. The adversarial
reviewer reads the notebook alone plus its own instruction section. Bundle
asymmetry is required because it removes the anchoring shared by the author and
the specialist reviewers.

## Coverage

The four reviewer agents cover these checks:

1. **research-design**
   - question: falsifiability, pre-registered thresholds, cycle hygiene,
     hypothesis-portfolio honesty
   - scope: universe, period, regime, generalization range
   - method: model choice, baselines, feature hygiene, hyperparameter trial
     accounting, retraining cadence
2. **evidence-sufficiency**
   - validation: walk-forward sample size, power, embargo adequacy, CPCV,
     test-set discipline
   - claim: conclusion calibration, overstatement, "cannot conclude" honesty,
     deployment-readiness gaps
3. **context-communication**
   - literature: coverage, novelty, differentiation depth, missed adjacent work
   - narrative: self-contained notebook quality, abstract, observations,
     interpretation, template residue
4. **adversarial**
   - claim-warrant under standalone reading
   - standalone readability for a third-party reader

Each reviewer returns severity-tagged findings. The assistant aggregates them
into one structured review delivered inline. The skill does not write a review
report file or modify `decisions.md`.

## Process

| Step | Action |
|---|---|
| 1 | Read the notebook(s) under review and the project's `hypotheses.md` / `decisions.md` / `literature/papers.md` / `literature/differentiation.md` |
| 2 | Verify a trigger fires; a direct review request or an upcoming `verdict = "supported"` decision is enough |
| 3 | Determine Initial vs Re-verify per `references/review_protocol.md`. Initial fires all 4 reviewers. Re-verify fires only touched specialist groups plus adversarial whenever any specialist re-fires |
| 4 | Pre-extract each reviewer's section from `references/review_dimensions.md` (specialists: §1-§3; adversary: §4). Whole-file `review_dimensions.md` is not delivered |
| 5 | Dispatch all selected reviewers in parallel via the assistant's sub-agent tool |
| 6 | Each reviewer returns findings in the schema below |
| 7 | Aggregate findings into a single inline review and compute the verdict per `references/severity_rubric.md` |

See `references/review_protocol.md` for dispatch, re-verify behavior, and the
single-agent fallback. See `references/review_dimensions.md` for the reviewer
checklists. See `references/severity_rubric.md` for severity and verdict
calculation.

## Finding schema

```
- severity: high | medium | low
  dimension: research-design | evidence-sufficiency | context-communication | adversarial
  subdimension: question | scope | method | validation | claim | literature | narrative | standalone
  where:    <notebook>:<cell-or-section>  (or "project-level")
  what:     <one-sentence statement of the issue>
  why:      <which rule / reference / convention is violated, or which evidence is missing>
  fix:      <concrete remediation or follow-up question>
  blocks_supported: yes | no
```

`blocks_supported = yes` on any finding makes a `verdict = "supported"`
decision a protocol violation until the finding is resolved or explicitly
parked with a recorded reason.

## Single-agent fallback

If parallel sub-agent dispatch is unavailable, run the four reviewer groups
sequentially in four distinct passes, clearing context or re-reading the
notebook from scratch between passes. Do not collapse the groups into one mixed
review. Run the adversarial pass with the minimum bundle only.

## Common rationalizations to resist

| Excuse | Reality |
|---|---|
| "The robustness battery passes, so the research is sound" | Robustness measures stability of an implemented PnL. It cannot tell you whether the design supports the claim. |
| "The user just wants quick feedback, not a full review" | If they asked for a review, run the protocol. Quick feedback is a different prompt. |
| "I read the notebook end-to-end; that's a review" | Single-pass reading consistently misses dimensions. Four focused passes keep attention narrow. |
| "The adversarial reviewer should also see the literature folder" | No. The asymmetry is the mechanism. A fully briefed adversary is no longer cold-eye. |
| "There's no decisions.md / hypotheses.md, so I can't follow the protocol" | Degrade gracefully: log the missing artifact as a finding and continue. |
| "The bug-review already ran" | Different question. `bug_review` checks correctness; experiment-review checks claim warrant. |
| "It's only a single experiment, full review is overkill" | A single experiment carrying a supported claim needs the gate most. |

## Red flags — the review is not actually being run

- A delivered review with no severity tags
- A delivered review covering fewer than four reviewer groups explicitly
- A delivered review that says "looks fine" without naming checked evidence
- The adversarial reviewer received project context, prior cycles, literature,
  decisions, hypotheses, or other reviewers' findings

## Failure mode this skill prevents

A clean implementation that produces a real number on a too-narrow universe,
with the wrong baseline, weak prior-work differentiation, and an overstated
deployment claim. The numbers can be real while the claim is unsupported.
