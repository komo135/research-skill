# Assumption Audit

## Purpose

This file extends `references/ideation.md` with a discipline that the base ideation protocol lacks: surfacing background assumptions of the reference model being challenged.

The base `Idea portfolio` pipeline audits anchors imported from prior work and preferred methods (via `De-anchoring pass` and `Divergence checkpoint.Anchoring audit`). It does not audit the *background assumptions of the model the candidate is challenging*. Those are different, and the difference matters for any candidate where the load-bearing constraint sits in the framing itself, not in the methods imported into it.

This file adds three sub-protocols invoked between `Observation discovery pass` and `Hypothesis synthesis pass`, plus a constraint-naming protocol that connects audited-but-unevaluable assumptions to the existing `plans/<id>.md` and `claim_structure.md` schemas.

## Skill role boundary

This file is one component of substrate-driven generation. The audit forces the agent to name what it is taking for granted so that candidates that invert a deep assumption get a fair seat in the portfolio. The accepted candidate still has to pass `references/ideation.md` with substrate ids, a generation operator, changed premise, anti-vacuity record, and evaluator feedback.

L3-L4 paradigm-shift generation remains outside any markdown-only guarantee. This audit can help produce bounded inversion candidates, but it must not be used as a substitute for substrate, evidence, or evaluator feedback.

## Sub-protocol 1a: Load-bearing assumption audit

Invoked between `Observation discovery pass` and `Hypothesis synthesis pass`.

Prompt the agent (or its de-anchoring subagent):

> "List the assumptions you are treating as background — the things you assume must be true for the current framing to even make sense. For each, ask: what happens if I foreground it and try the opposite? Which assumption, if false, would force the largest revision?
>
> Once you have named the load-bearing candidate, ask: is this assumption downstream of a deeper one? If yes (i.e., this assumption would automatically follow from a more foundational one being true), promote the deeper one and re-audit. Continue until the named load-bearing assumption is not downstream of anything else in scope."

Output: ≥3 named assumptions, one marked as **load-bearing** with one-sentence reason. The load-bearing assumption becomes a candidate for inversion in `Hypothesis synthesis pass.Source observation`.

### Why the downstream check

The initial intuition often picks a culturally-load-bearing assumption (e.g., "the field winsorizes outliers because outliers are contaminants"). A culturally-visible assumption may be a downstream effect of a deeper foundational one (e.g., "the population variance is finite"). The downstream check forces depth comparison: of two assumptions, the one whose inversion makes the other automatically irrelevant is the deeper one.

## Sub-protocol 1b: Blind-spot catalog

Drafted during `Assumption audit pass`, then finalized after `Anti-vacuity gate` identifies surviving candidates and before `Hypothesis synthesis pass`.

This is not a quota of adjacent topics. It is a candidate-scope control: a blind spot matters only if it could break a candidate's mechanism, narrow a claim, or force a repair before promotion.

Prompt:

> "For each surviving candidate, name one blind-spot area or `None with reason`: an adjacent knowledge area or missing result pattern that, if different from your current context, could break the candidate's mechanism or claim scope. For each candidate, state how it could break the mechanism, the claim-scope effect, and the required repair."

Output: a candidate-keyed catalog stored in `plans/<id>.md` under `Idea portfolio.Blind-spot catalog`. Each surviving candidate must record:

- `Blind-spot area`: adjacent knowledge area or missing result pattern, or `None with reason`
- `How it could break the mechanism`: the failure path if the blind spot is real
- `Claim-scope effect`: one of `conditions_not_tested: ...`, `narrowed_claim: ...`, `PARK: ...`, `ADJACENT: ...`, or `no_change: <reason>`
- `Required repair`: one of `retrieval: ...`, `user_input: ...`, `evaluator_construction: ...`, `narrow_conditions: ...`, or `none_with_reason: <reason>`

The catalog is structurally honest: the agent admits what it might not know. It does not pretend to fix the gap. Where applicable it can prompt the user or a separate retrieval step outside this skill to supply the missing material. A blind spot has no protocol value unless it changes promotion, claim scope, constraint-naming, or a required repair.

## Sub-protocol 1c: Reference-class forecasting (manual)

Invoked **manually**, not on every cycle. Invocation triggers:

- The main agent self-assesses overconfidence in a candidate (subjective)
- The user requests it explicitly
- The `research-review` subagent flags the candidate's claim as overconfident in its `Analysis sufficiency` rationale

Prompt:

> "Name 3 historical attempts to solve a problem of similar shape. For each, note success/failure outcome and one named reason. State a calibrated base rate before committing the current candidate."

No separate subagent for reference-class forecasting itself. No durable state file. Output is conversational and ephemeral.

Rationale: empirical evidence (Si 2024, Si 2025 Ideation-Execution Gap, Kadavath 2022, Lin 2022) shows reference-class forecasting and calibration discipline can suppress innovation when applied during generation. Use as overconfidence check, not as forced filter.

## Constraint-naming protocol

When an audited assumption has no current evaluator (the candidate hypothesis cannot be tested with available data, instruments, or theory), the agent must record this fact in **two existing places**:

1. In `plans/<id>.md` `Prior-work grounding.Unknown prior-work constraint` (or `Divergence checkpoint.Disconfirming evidence` if it concerns disconfirmability rather than literature), as a named constraint with category-specific default phrasing:
   - `basic_research` with `mode: theoretical` → "no decisive empirical evaluator available at the present state of knowledge"
   - `basic_research` with `mode: exploratory` or `mode: confirmatory` → "named observation requires <instrument/dataset> that is not currently accessible"
   - `applied_research` → "evaluator construction deferred to ADJACENT plan <id>" (open the adjacent plan for evaluator construction)
   - `experimental_development` → "acceptance test deferred to milestone <name>"
2. In any resulting load-bearing claim, narrow `conditions_tested` to the regime that actually was tested, and record the missing-evaluator regime as a `conditions_not_tested` entry referencing the plan-level named constraint by name.

This recovers honest scoping of candidates that lack immediate evaluators. The protocol uses two existing fields, not new ones.

## Common failures

- **Cultural-anchor pick**: agent names "what the field does wrong" as load-bearing (e.g., "outliers are contaminants") rather than the deeper assumption that justifies that practice (e.g., "the population variance is finite"). The downstream check in 1a is the explicit counter; re-audit until the named assumption is not downstream of anything in scope.
- **Audit-then-ignore**: agent runs 1a, names a load-bearing assumption, then proceeds to `Hypothesis synthesis pass` without including an inversion candidate in the synthesis. The audited assumption must enter `Hypothesis synthesis pass.Source observation` for at least one candidate.
- **Blind spots as decoration**: agent names adjacent areas but does not tie each survivor to a mechanism failure path, claim-scope effect, or required repair. The catalog has no effect unless used.
- **Reference-class during generation**: agent runs 1c during ideation (not as an overconfidence check). This suppresses innovation. 1c is post-hoc only.
- **Constraint-naming dishonest**: agent declares a no-evaluator constraint to escape rigor rather than to honestly scope a claim. The constraint phrasing is for cases where the evaluator genuinely does not exist; misuse degrades the protocol.

## Sources

- Empirical basis: Si 2024 / Si 2025 (Ideation-Execution Gap), Zhang 2025 (MAD overvaluation), Kadavath 2022 (calibration), Lin 2022 (verbalized uncertainty)
- Pressure-test summary: cross-domain paper injection, multi-agent paradigm debate, and evaluator-gate variants were rejected because they either reintroduced anchors, relied on unenforceable markdown self-restraint, or selected for evaluator-rich problems too early.
- Retained role: assumption audit supplies load-bearing assumption and inversion admission discipline; `references/ideation.md` turns that into a substrate/operator/anti-vacuity generation contract.
