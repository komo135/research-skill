# hypothesis_generation.md

How to go from "stuff in the world" to a candidate H statement that
meets `research_design.md`'s falsifiability requirements. Step 1.5,
between literature review and the hypothesis-portfolio entry.

## When to read

- About to write a new entry in `hypotheses.md`.
- About to add a `## H<id>` block inside an existing notebook.
- About to derive a new H from a prior H's verdict (in which case this
  reference owns *content*; `hypothesis_cycles.md` owns *routing*).

## Goal

Produce a candidate H whose **origin is documented** and whose
provenance **forecasts its differentiation tier**. An H without a
documented origin is treated as Stage-0-required (per
`pre_hypothesis_exploration.md`'s discipline) and routed back upstream.

## The fundamental rule

Every H declares **exactly one primary pathway**, listed below. When
multiple pathways apply, declare the primary by the priority rule and
list the others as *contributing*. An H with no declared pathway and
no documented origin defaults to Stage 0.

The pathway is not optional metadata — it determines which provenance
files the H must point to, which differentiation-tier expectation
applies, and which common failure modes apply when `experiment-review`
reads the H later.

## Pathways

### Pathway 1 — Data-driven (EDA → H)

**Trigger.** EDA finding from a Stage 0 run.

**See** `pre_hypothesis_exploration.md` for the full Stage 0 protocol;
this section does not duplicate it.

**Required citation.** A Phenomenon entry in `eda/findings.md` with
the entry id (P\<n\>) referenced from this H.

**Tier expectation.** Variable — set in Step 1 (literature review)
when the candidate's differentiation is checked against prior work.

**H template (structural form, parameters intentionally blank).**
"Conditional on the structural pattern P\<n\> observed in the
exploration set, the comparison [method A] vs. [baseline B] on out-of-
exploration data shows [direction] with effect size [≥ threshold] and
fee-adjusted PnL [≥ threshold]. Specific threshold values, lookback
windows, and ranges are set from the train split in Step 2 (Research
design), not from the exploration set."

### Pathway 2 — Literature-extension

**Trigger.** Re-test a published claim under a *new context* (universe,
period, frequency, asset class) without changing the method.

**Required citations.**
- The paper, with venue, year, and the *section / page* where the
  claim under extension appears (not just the title or abstract).
- A row in `literature/differentiation.md` showing exactly one cell
  ("this research" column) that differs from the paper's setup. That
  cell is the new context.

**Tier expectation.** Medium. (Strong is reserved for new methods or
new metrics — see Pathway 3 / 6 / `literature_review.md`.)

**Common failure modes and counters.**

| Failure | Counter |
|---|---|
| "I read the abstract, that's enough" | Pathway 2 requires citing section/page where the claim appears. Abstract-only reads default the H to ad-hoc with the higher tier hurdle. |
| "Same data, different ML model" | Same universe + same period + different model is a method comparison, not an extension. Either the universe/period/frequency must change (Pathway 2) or the question must change (Pathway 3, refutation). |
| "Multiple cells differ from the paper" | Pick the *primary* differentiator and list the others. An H that differs on every cell is not extension — it is a fresh research design and probably wants Pathway 6 (mechanism-driven). |

**H template.**
"Paper [Author, Year] showed claim Y on [their universe/period/freq].
This research tests whether Y holds on [your universe/period/freq] by
[method, identical to or near-identical to the paper], with acceptance
threshold [N from research_design.md table]. The differentiator vs.
the paper is [the single cell from differentiation.md]."

### Pathway 3 — Literature-refutation

**Trigger.** Test a paper's claim under stricter / more adversarial
conditions where the paper would be most likely to fail. The argument
"this is where the paper would fail" is made *a priori*, before
running.

**Required citations.**
- The paper, as in Pathway 2.
- An *a-priori* argument (in `literature/differentiation.md` or
  inline in the H block) explaining why the new condition is the
  regime in which the claim is most likely to fail.

**Tier expectation.** Strong on success (a published claim does not
hold under your stricter test); Medium on failure-to-refute (the claim
survives a stricter test, which itself is a contribution).

**Common failure modes and counters.**

| Failure | Counter |
|---|---|
| "I added one variation as a refutation" | A variation is not *a priori* a refutation. Refutation requires the variation be argued — *before running* — to be where the claim fails. Otherwise it is a sensitivity sweep. |
| "My refutation test is weaker than the paper's" | Silent confirmation, not refutation. The stricter-condition argument must be defensible: longer embargo, harder universe, more conservative fees, out-of-time window, etc. — and *stricter than the paper used*. |
| "I'm refuting but I haven't read the original conditions" | The strictness comparison requires knowing the paper's original conditions in detail. Default to reading the method section first or fall back to Pathway 2. |

**H template.**
"Paper [Author, Year] showed Y under conditions C_paper. This research
tests whether Y survives the stricter condition C_strict, where
C_strict differs from C_paper in [axis] in the direction argued *a
priori* most likely to surface a failure of Y. Acceptance: Y holds
under C_strict; rejection: Y fails."

### Pathway 4 — Failure-derived

**Trigger.** A specific failure axis of a rejected prior H, used to
derive a new H that addresses one (named) axis.

**Required inputs.**
- The parent H_n's row in `results.parquet`.
- A *failure-mode analysis entry* in `decisions.md` for H_n, naming
  the failure axis explicitly (leakage / regime mismatch / fee model /
  wrong horizon / wrong universe / wrong baseline / etc.).

**Tier expectation.** Variable. If the failure axis is novel (not in
prior work), this approaches Strong; if the axis is a standard
sensitivity, this is Weak — and a Weak Pathway-4 H is a parameter
sweep, not a research-grade derivative.

**Common failure modes and counters.**

| Failure | Counter |
|---|---|
| "H_{n+1} is just H_n with different parameters" | Parameter sweep. Either name a *different* intervention (Pathway 4 proper) or call it a sensitivity in H_n's robustness battery. |
| "I have a hunch about why H_n failed" | Without a failure-mode analysis entry naming the axis, you have a fresh ad-hoc H, not a derivative. Run the failure analysis first; *then* generate H_{n+1}. |
| "H_{n+1} addresses every failure mode at once" | Pathway 4 requires naming *one* axis and predicting the others remain unaddressed. An H claiming to fix everything cannot be falsified. |

**H template.**
"H_n was rejected; the failure-mode analysis names axis A as the
specific failure mode. H_{n+1} introduces intervention Z which targets
axis A. H_{n+1} preserves axes B, C, ... unchanged. Acceptance:
H_{n+1} survives the axis-A gate; rejection: H_{n+1} fails on the
axis-A gate or another axis surfaces."

**Routing (cross-reference).** Routing of H_{n+1} (same notebook vs.
new notebook) is owned by `hypothesis_cycles.md`. Pathway 4 owns the
*content*; cycles owns the *file placement*.

### Pathway 5 — Cross-asset / cross-regime extension

**Trigger.** A known phenomenon in market A → test in market B, or in
regime R within market A.

**Required citations.**
- *Source-market evidence*: a paper or a prior H in this project that
  supports the phenomenon in market A. "I'm pretty sure it works in
  equities" is not source-market evidence.
- *Transfer-mechanism argument*: why should (or shouldn't) the
  phenomenon transfer? Microstructure differences, agent populations,
  regulatory differences, liquidity differences. The transfer
  mechanism is the load-bearing part of the H.

**Tier expectation.** Medium.

**Common failure modes and counters.**

| Failure | Counter |
|---|---|
| "Phenomenon X works in equities, let me test in crypto, no source citation needed" | Pathway 5 requires source-market evidence (paper or prior H). "It's well-known" is not citation. Without source, the H defaults to Pathway 6 (mechanism-driven) and the mechanism must be written explicitly. |
| "I'll test in market B without re-checking that the phenomenon still holds in market A" | Source-market evidence may be stale. Confirm or reference a recent confirmation in market A; otherwise the cross-asset H is testing a phantom. |
| "The transfer is intuitive" | Intuition is not a transfer mechanism. Write the mechanism: structural reason X exists in A and (does/doesn't) exist in B. |

**H template.**
"Phenomenon X is documented in market A by [citation]. The transfer
mechanism Y argues that X should [transfer / not transfer / partially
transfer] to market B because [structural reason]. This research
tests whether X holds in market B with [acceptance threshold] for
confirmation and [rejection condition]."

### Pathway 6 — Mechanism-driven

**Trigger.** A causal mechanism (economic, microstructural,
behavioural) is hypothesized; the mechanism implies a specific
observable; the H tests that observable.

**Required input.**
- A *mechanism description*: at least one paragraph stating the
  causal model — cause → mechanism → observable. Argued from first
  principles or from a theory paper, *not retrofitted to data*.

**Tier expectation.** Strong (novel mechanism in a context where the
mechanism has not been tested) / Medium (well-known mechanism in a
new application).

**Common failure modes and counters.**

| Failure | Counter |
|---|---|
| "Data shows X → therefore mechanism Y must be at work" | Reverse fitting. Mechanism comes first; observable comes from mechanism. If the order is reversed, the H is data-driven (Pathway 1) and requires Stage 0 — not Pathway 6. |
| "Mechanism predicts something but I'll test something convenient" | The H must test the *specific* observable the mechanism predicts. Substituting a related-but-easier observable breaks the chain cause → observable. |
| "Mechanism is 'I think there's something there'" | Hand-waving. Causal description requires naming cause, mechanism, and predicted observable explicitly. Without all three, default to ad-hoc with the higher-tier hurdle. |

**H template.**
"Mechanism: [causal description — cause C, mechanism M, observable O].
Specific quantitative prediction: [the observable's predicted shape /
sign / magnitude region]. This research tests whether the prediction
holds, with [acceptance threshold] for confirmation and [rejection
condition] for falsification. Mechanism source: [first principles /
theory paper Author Year]."

## Pathway selection rule

When multiple pathways apply, declare a *primary* and list the others
as *contributing*. Priority for primary, when several fit:

1. Mechanism-driven (Pathway 6) — Strong tier potential
2. Literature-refutation (Pathway 3) — Strong tier on success
3. Literature-extension (Pathway 2) — Medium tier base
4. Cross-asset extension (Pathway 5) — Medium tier with mechanism
5. Failure-derived (Pathway 4) — variable
6. Data-driven (Pathway 1) — variable, defaults through Stage 0

Lower priority is not "worse" — most working H's are Pathway 1, 4, or
5. Priority resolves *which to declare primary* when several fit, on
the principle "use the strongest provenance available for the same H
content".

## Ad-hoc generation (escape hatch)

When no pathway clearly applies, the H is **ad-hoc**. Ad-hoc is legal
under three conditions, all required:

1. The *origin* is documented in `decisions.md` (researcher's
   intuition, conversation with X, half-formed observation, etc.) —
   this is the citation-equivalent for ad-hoc.
2. The differentiation matrix is filled out per `literature_review.md`
   regardless of the lack of source paper.
3. The H clears at least Medium tier in differentiation. Ad-hoc H's
   pay a higher hurdle — Weak-tier ad-hoc is rejected as a degraded
   reimplementation with no provenance.

Ad-hoc is **not** a Pathway 7 — it carries no fixed tier expectation
and faces a higher hurdle by design. Repeated ad-hoc generation
without a paying origin is the protocol-equivalent of unstructured
H-fishing and is the failure mode this taxonomy exists to prevent.

An H with no documented pathway *and* no documented ad-hoc origin
defaults to Stage 0 (Pathway 1 via `pre_hypothesis_exploration.md`),
where it earns its origin or it does not survive.

## Multi-pathway H

An H may legitimately combine pathways. Examples:

- Literature-extension + failure-derived: "Extending paper X to crypto,
  H1 was rejected; H2 is the same extension with the failure axis
  fixed."
- Mechanism-driven + cross-asset: "Mechanism Y predicts observable O;
  prior work confirmed O in equities; this H tests O in crypto under Y."
- Data-driven + mechanism-driven: "Stage 0 surfaced phenomenon P;
  Pathway 6 attaches mechanism Y to P, lifting the tier expectation."

When combining, declare a **primary** pathway and list **contributing**
pathways. The primary must independently meet its required-citation
rule — contributing pathways are *addenda*, not *substitutes*. Multi-
pathway provenance is stronger than single-pathway and may shift the
tier expectation up.

## Common loopholes (across pathways)

| Loophole | Counter |
|---|---|
| "I'll skip pathway declaration; the H is obvious" | An H without a declared pathway and without a documented ad-hoc origin defaults to Stage 0 (Pathway 1). "Obvious" is not a pathway. |
| "Multi-pathway lets me launder weak Pathway 5 provenance" | The primary pathway must independently meet its required-citation rule. If Pathway 5's source-market evidence is missing, calling Pathway 5 *contributing* and Pathway 6 *primary* still requires Pathway 6's mechanism description to stand alone. |
| "I'll claim Pathway 6 (mechanism) without writing the mechanism" | Pathway 6 requires an explicit cause → mechanism → observable description. Without it, default to ad-hoc. |
| "Pathway 2 (extension) but I read only the abstract" | Required citation is section/page where the claim appears. Abstract-only reads default to ad-hoc. |
| "Pathway 4 (failure-derived) but no failure-mode analysis ran" | Pathway 4 requires the failure-mode analysis entry in `decisions.md`. Run the analysis; only then is the H a Pathway-4 derivative. |
| "Pathway 5 (cross-asset) but the phenomenon is intuitive in market B" | "Intuitive" is not source-market evidence. Either provide a paper / prior H from market A *or* switch primary to Pathway 6 and write the mechanism. |
| "Reverse-fit a mechanism to data found in EDA" | Mechanism-first, observable-second. Data → mechanism is Pathway 1 (data-driven), not Pathway 6. Routing back through Stage 0 keeps the in-sample-selection guard intact. |

## Output

Each H entry in `hypotheses.md` carries a `pathway:` field with the
primary pathway name (e.g. `pathway: 2-literature-extension`) and a
`contributing_pathways:` list (possibly empty). The provenance
citations live where each pathway's required-citation rule says they
live:

- Pathway 1: `eda/findings.md` Phenomenon entry id
- Pathways 2 / 3 / 5: `literature/papers.md` paper id + section/page
- Pathway 4: parent H row id in `results.parquet` + failure-mode entry
  id in `decisions.md`
- Pathway 6: mechanism description stored in `decisions.md` (or a
  dedicated `theory/mechanisms.md` if the project accumulates many)
- Ad-hoc: origin description in `decisions.md`

After the pathway is declared and citations are in place, the H goes
through Step 2 (research design) where the falsifiable comparison
statement, numeric thresholds, and figure plan are written.
