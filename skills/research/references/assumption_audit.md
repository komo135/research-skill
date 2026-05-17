# Assumption Audit

## Purpose

This file supports `references/mechanistic_hypothesis_generation.md` by surfacing background assumptions of the reference model, evaluator, or framing being challenged.

The audit is not a separate idea-generation protocol. It is used when a mechanism hypothesis depends on an assumption that may be load-bearing, hidden, or unevaluable under current evidence.

## Sub-protocol 1a: Load-bearing assumption audit

Use during research situation diagnosis or mechanistic analysis.

Prompt the agent:

> "List the assumptions you are treating as background. For each, ask what happens if it is false or inverted. Which assumption, if false, would force the largest revision? If that assumption is downstream of a deeper in-scope assumption, promote the deeper assumption and re-audit."

Output:

- At least three named assumptions considered.
- One load-bearing assumption with a one-sentence reason.
- Downstream-check result explaining why the chosen assumption is not downstream of a deeper in-scope assumption.
- Effect on the mechanism record: how the assumption changes the Hypothesis, Competing hypothesis, Discriminating prediction, Minimal test, Required evidence, or Decision.

## Sub-protocol 1b: Blind-spot catalog

Draft this when a mechanism hypothesis survives the first record pass or is being considered for `commit`.

This is not a quota of adjacent topics. It is a mechanism-scope control: a blind spot matters only if it could break a surviving candidate's mechanism, narrow a claim, or force repair before planning.

Prompt:

> "For each surviving candidate or mechanism record, name one blind-spot area or `None with reason`: an adjacent knowledge area or missing result pattern that, if different from the current context, could break the mechanism or claim scope. State how it could break the mechanism, the claim-scope effect, and the required repair."

Output fields:

- `Blind-spot area`: adjacent knowledge area or missing result pattern, or `None with reason`
- `How it could break the mechanism`: the failure path if the blind spot is real
- `Claim-scope effect`: one of `conditions_not_tested: ...`, `narrowed_claim: ...`, `PARK: ...`, `ADJACENT: ...`, or `no_change: <reason>`
- `Required repair`: one of `retrieval: ...`, `user_input: ...`, `evaluator_construction: ...`, `narrow_conditions: ...`, or `none_with_reason: <reason>`

The catalog is structurally honest: the agent admits what it might not know. It does not pretend to fix the gap. Where applicable it can prompt the user or a separate retrieval step outside this skill to supply missing material. A blind spot has no protocol value unless it changes the mechanism record, claim scope, constraint-naming, or required repair.

## Sub-protocol 1c: Reference-class forecasting

Use manually, not on every generation cycle. Invocation triggers:

- The main agent self-assesses overconfidence in a mechanism record.
- The user requests it explicitly.
- Result analysis or claim drafting exposes that the explanation is overconfident relative to evidence.

Prompt:

> "Name 3 historical attempts to solve a problem of similar shape. For each, note success/failure outcome and one named reason. State a calibrated base rate before committing the current mechanism."

No separate agent is required. Output is conversational unless the plan needs it for a scope decision.

## Constraint-naming protocol

When an audited assumption has no current evaluator, instrument, data, or derivation route, record this fact in existing plan fields:

1. In `Prior-work grounding.Unknown prior-work constraint` or `Divergence checkpoint.Disconfirming evidence`, as a named constraint with category-specific phrasing:
   - `basic_research` with `mode: theoretical`: "no decisive empirical evaluator available at the present state of knowledge"
   - `basic_research` with `mode: exploratory` or `mode: confirmatory`: "named observation requires <instrument/dataset> that is not currently accessible"
   - `applied_research`: "evaluator construction deferred to ADJACENT plan <id>"
   - `experimental_development`: "acceptance test deferred to milestone <name>"
2. In any resulting load-bearing claim, narrow `conditions_tested` to the regime actually tested and record the missing-evaluator regime as a `conditions_not_tested` entry referencing the plan-level named constraint.

## Common failures

- **Cultural-anchor pick**: naming "what the field does wrong" rather than the deeper assumption that justifies it. Re-audit until the named assumption is not downstream of anything in scope.
- **Audit-then-ignore**: naming a load-bearing assumption, then writing a mechanism record that never uses it. The assumption must change the Hypothesis, Competing hypothesis, Discriminating prediction, Minimal test, Required evidence, or Decision.
- **Blind spots as decoration**: naming adjacent areas without tying each survivor to a mechanism failure path, claim-scope effect, or required repair.
- **Reference-class during generation**: running forecasting as a forced filter before mechanism analysis. Use it as an overconfidence check, not as a generator.
- **Constraint-naming dishonest**: declaring a no-evaluator constraint to escape rigor rather than to scope a claim.

## Sources

- Empirical basis: Si 2024 / Si 2025 (Ideation-Execution Gap), Zhang 2025 (MAD overvaluation), Kadavath 2022 (calibration), Lin 2022 (verbalized uncertainty)
- Retained role: assumption audit supplies load-bearing assumption and inversion discipline for mechanistic hypothesis generation.
