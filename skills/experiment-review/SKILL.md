---
name: experiment-review
description: Use when about to declare verdict='supported' on any experiment in a quant-research project (mandatory co-gate with bug_review; both must pass). Also use when the user asks for a review of a notebook / experiment / project, at end-of-research-cycle gates, before external sharing / publication / any deployment recommendation, and when inheriting a notebook that needs a fresh-eyes assessment. Asks whether the claim is warranted by what was actually tested — distinct from bug_review which asks whether the implementation is correct. Both layers required for verdict='supported'.
---

# Experiment Review

A review skill for quantitative-research experiment notebooks. Asks the question
**"is the conclusion warranted by what was actually tested?"** — orthogonal to
the question "is the implementation correct?" (`bug_review` answers that one).

## When to use

- A user asks for a review of a notebook, experiment, or project
- About to declare `verdict = "supported"` on any experiment in a quant-research
  project — this skill complements `bug_review`; both must pass before that
  verdict
- End of a research cycle, before deciding what the next cycle is
- Before sharing the work externally, before publication, or before any
  deployment recommendation
- Inheriting a notebook from another researcher and needing a fresh-eyes
  assessment

## When NOT to use

- The user wants implementation correctness checked — use `bug_review` inside
  `quant-research` instead. Bug review is a *precondition* for this review,
  not a substitute. A clean experiment-review on top of a buggy implementation
  produces confidence in a claim about a contaminated PnL.
- The notebook is at orientation / brainstorm stage and no claim exists yet.
  Wait until there is a conclusion to review.

## Boundary against `bug_review`

Both layers are required for `verdict = "supported"`. They are distinct, complementary,
and intentionally not merged. The most common confusion is between the two `validation`
scopes — one in each layer.

| | `bug_review` (in `quant-research`) | `experiment-review` (this skill) |
|---|---|---|
| One-line | Are the code and numbers correct? | Is the claim warranted by the design? |
| Question answered | "Is the implementation contaminated?" | "Is the claim oversold relative to evidence?" |
| Looks at | Code, data, PnL series | Hypothesis, universe, baselines, claim, notebook artifact |
| Specialists | leakage / pnl-accounting / **validation (correctness: split, embargo, purging)** / statistics (metric arithmetic) / code-correctness | question / scope / method / **validation (sufficiency: walk-forward N, statistical power)** / claim / literature / narrative |
| Adversarial reviewer (minimum bundle) | code + reported numbers | `.py` file alone |
| Order | Precondition (run first) | Postcondition (run after robustness battery) |
| Verdict gate | **Both must pass.** | **Both must pass.** |

The `validation` overlap is the most subtle boundary. Rule of thumb:

- `bug_review`'s `validation` checks "is the embargo wired in correctly so no future
  information leaks across the split?" (correctness)
- `experiment-review`'s `validation` checks "given that the embargo is wired in
  correctly, does walk-forward over N=8 windows give a mean Sharpe whose standard
  error is small enough to distinguish 0.4 from 1.1?" (sufficiency / statistical
  power)
- A finding that is genuinely both — e.g. "embargo is too short AND walk-forward
  has too few windows" — should be flagged independently by both reviewers. Redundancy
  is harmless; a missed finding is not.

## Core principle

**Seven narrow specialist reviewers in parallel + one adversarial cold-eye reviewer
with a deliberately different (minimum) context bundle, in parallel.** Narrowness is
the mechanism that makes the seven specialists work. Bundle asymmetry is the mechanism
that makes the eighth (adversarial) reviewer work. Same model in all eight, but
specialists share the full bundle while the adversary sees only the `.py` file.

Six specialist dimensions cover **research quality** ("is the claim warranted by the
experimental design?"); the seventh covers **notebook quality** ("is the notebook
self-contained as a communication artifact?"). The two are orthogonal — a notebook can
describe excellent research badly, or describe weak research beautifully — so they
need separate specialist passes.

The eighth (adversarial) reviewer sits orthogonal to all seven specialists. Its job is
not "be the eighth specialist on a different topic" but "be the same model with
*different priors* — priors that come from having less context, not more topic
coverage". Empirically (Cross-Context Review, arxiv 2603.12123), minimum-context
review on code yields findings that full-context review of the same model
systematically misses. The mechanism is anchoring removal: the seven specialists all
read the same notebook, the same design cell, the same prior cycles, the same
literature folder; they share priors. The adversary, given only the `.py`, has to
reason from the artifact alone.

The eight dimensions:

1. **question** — falsifiability, pre-registered numeric thresholds, cycle
   hygiene, hypothesis-portfolio honesty, selection bias across cycles
2. **scope** — universe size and diversity, period coverage, regime coverage,
   generalization range, single-instrument leaps to "the asset class"
3. **method** — model choice justification, baseline strength (especially the
   *hand-crafted upper-bound* baseline — usually missing), feature-experiment
   hygiene, hyperparameter trial accounting, retraining cadence in
   walk-forward
4. **validation** — split correctness *in spirit* (sufficiency-of-power, not
   letter-of-correctness — letter-of-correctness lives in `bug_review`), embargo
   adequacy for the claim, walk-forward sample size and the implied statistical
   power of its mean metric, purged k-fold / CPCV adequacy, test-set discipline
5. **claim** — conclusion vs. evidence calibration, overstatement detection,
   "cannot conclude" honesty, deployment-readiness gap, the implied portfolio
   math behind any "deploy as overlay" claim
6. **literature** — paper-count floor, weak / medium / strong differentiation
   tier, *missed* prior work in the most relevant adjacent literature
   (variance-risk-premium, factor zoo, etc.), differentiation matrix
   completeness
7. **narrative** — notebook as a self-contained communication artifact (spec
   compliance): abstract cell filled in, per-section *what & why* cells,
   per-figure *observation* cells, prose interpretation before the programmatic
   verdict, "Cannot conclude" section present, headline figures plotly / altair
   full-width ≥ 450 px, at least one `mo.ui` drill-down widget that does NOT
   feed `results.parquet`, no template-placeholder residue. Canonical spec is
   the `quant-research` skill's `notebook_narrative.md` and
   `marimo_cell_granularity.md`. This dimension checks *spec compliance*.
8. **adversarial** (cold-eye) — `.py` file alone, no other inputs. Two axes:
   (a) does the abstract / verdict / headline number hold up on the evidence
   visible in this file alone (claim-warrant under standalone reading);
   (b) can a third-party reading this file alone explain what was investigated,
   why, how, and what was concluded (standalone-readability — *whether* spec
   compliance actually communicates, orthogonal to dimension 7's *whether*
   spec is met).

Each reviewer returns severity-tagged findings. Findings are aggregated into a
structured review report at
`notebooks/<project>/reviews/exp_NNN_<ISO-date>.md`.

## Process

| Step | Action |
|---|---|
| 1 | Read the notebook(s) under review and the project's `hypotheses.md` / `decisions.md` / `literature/papers.md` / `literature/differentiation.md` |
| 2 | Verify a trigger fires; a direct user request is itself a trigger; an upcoming `verdict = "supported"` decision in a quant-research session is itself a trigger |
| 3 | Prepare **two** context bundles: a full bundle for the seven specialists (notebook path, project root, design-cell content, prior cycle log, literature files) and a minimum bundle for the adversarial reviewer (the `.py` file alone — see dimension 8 in `references/review_dimensions.md` for the exact NOT-inputs list) |
| 4 | Dispatch all eight reviewers *in parallel* via the assistant's sub-agent tool. The seven specialists each get the full bundle plus their dimension scope from `references/review_dimensions.md`. The adversarial reviewer gets only the minimum bundle plus its instruction (also in `references/review_dimensions.md`) |
| 5 | Each reviewer returns findings in the schema below |
| 6 | Aggregate into `notebooks/<project>/reviews/exp_NNN_<ISO-date>.md` using `assets/review_report.md.template` |
| 7 | Compute the overall verdict per `references/severity_rubric.md`: ready / partial / preliminary / not-yet-research |
| 8 | If running inside a quant-research session, append a one-line entry to the project's `decisions.md` linking to the review report |

See `references/review_dimensions.md` for what each reviewer specifically
checks (dimensions 1–7 are specialists; dimension 8 is the adversarial cold-eye
reviewer with its own minimum bundle). See `references/review_protocol.md` for the
dispatch and aggregation mechanics, including the single-agent fallback. See
`references/severity_rubric.md` for severity tags and the verdict calculation.

**Bundle asymmetry is required, not optional.** Giving the adversarial reviewer the
full bundle "for fairness" collapses the mechanism that makes the layer work; the
adversary must remain context-starved.

## Finding schema

```
- severity: high | medium | low
  dimension: question | scope | method | validation | claim | literature | narrative | adversarial
  where:    <notebook>:<cell-or-section>  (or "project-level")
  what:     <one-sentence statement of the issue>
  why:      <which rule / reference / convention is violated, or which evidence is missing>
  fix:      <concrete remediation or follow-up question>
  blocks_supported: yes | no
```

`blocks_supported = yes` on any finding makes a `verdict = "supported"`
decision a protocol violation until that finding is resolved or explicitly
parked with a recorded reason.

## Single-agent fallback

If parallel sub-agent dispatch is unavailable (single-process platform,
sub-agent quota exhausted, etc.), run the eight dimensions sequentially in
eight distinct passes, clearing context (or at least re-reading the notebook
from scratch) between passes. Do not collapse dimensions — the failure mode
this skill is designed to prevent is exactly the single-pass review that
"covers everything" and ends up shallow on each axis. The adversarial pass
is run *with the minimum bundle only* even in the fallback — bundle asymmetry
is preserved sequentially as well as in parallel.

## Common rationalizations to resist

| Excuse | Reality |
|---|---|
| "The robustness battery passes, so the research is sound" | Robustness measures stability of an implemented PnL. It cannot tell you whether the *design* is sufficient to support the claim. A clean SPY-only walk-forward says nothing about generalization to QQQ. |
| "The user just wants quick feedback, not a full review" | If they wanted quick feedback they would not have asked for a review. Run the protocol. Quick feedback comes from a different prompt. |
| "I read the notebook end-to-end — that's a review" | Single-pass reading consistently misses dimensions. Seven narrow passes plus one cold-eye pass catches more even from one reader. |
| "The adversarial reviewer should also see the literature folder, that's only fair" | No. The asymmetry IS the mechanism. A fully-briefed adversary is just an eighth specialist; CCR (arxiv 2603.12123) showed minimum-context review on code yielded findings full-context review systematically missed. Restoring its context restores the same anchoring the seven specialists already share. |
| "There's no decisions.md / hypotheses.md, so I can't follow the protocol" | The protocol downgrades gracefully — log "missing artifact" as a `high`-severity finding under `question` and continue with the other dimensions. |
| "The bug-review already ran" | Different question. `bug_review` = is this *correct*; experiment-review = is the *claim warranted*. Both must pass for `verdict = "supported"`. |
| "The `quant-research` SKILL.md doesn't reference this skill, so it must be optional" | This skill IS the protocol gate at `verdict = "supported"`. If a `quant-research` SKILL.md you are reading does not invoke this skill before verdict, that SKILL.md is out of date relative to this gate — fall back to invoking this skill anyway, then flag the SKILL.md gap. (Captured RED-phase rationalization; do not let "SKILL.md = sole protocol" reasoning skip this layer.) |
| "It's only a single experiment, full review is overkill" | If you're declaring a verdict on a single experiment, the single experiment is being asked to bear the weight of the claim. That's exactly when this layer matters most. |
| "The user is the author and will know the misses" | Authors are systematically blind to their own missing baselines and over-extrapolated conclusions. That is the exact reason a fresh review pass exists. |

## Red flags — the review is not actually being run

- A delivered review with no severity tags
- A delivered review covering fewer than eight dimensions explicitly
- A delivered review with no archived report at `notebooks/<project>/reviews/`
- A delivered review that concludes "looks fine" without naming what was
  checked under each dimension and what evidence supported that judgment
- The adversarial reviewer was given the full bundle (literature, decisions,
  hypotheses, prior cycles, or other reviewers' findings) — that collapses the
  bundle asymmetry that makes the layer add value

## Failure mode this skill prevents

A clean implementation that produces a real number on a too-narrow universe,
with the wrong baseline, against weak prior-work differentiation, and that
gets written up as a deployable result. The numbers are real but the
**claim** is unsupported. This is the modal way quant research gets shipped
before it is ready.
