---
name: research-plan-review
description: Use when reviewing an R&D plan before execution, especially when a plan may be runnable but rests on a wrong premise, unsupported premise, unverified premise, or weak hypothesis validation method.
---

# Research Plan Review

## Overview

Independent review for a drafted research plan before execution. The plan path is the starting context; the reviewer checks whether execution should stop because the hypothesis rests on a broken premise or because the validation method cannot test the hypothesis.

This skill reviews research design only. Do not execute the plan, do not analyze results, and do not write final claims.

The `Execution recommendation` is a pre-execution design recommendation: whether the plan is safe to run as written, needs repair, or should be blocked before execution. It is not a claim-readiness verdict and must not use result-analysis readiness labels.

Plan review covers **pre-result commitments** only: question/objective, hypothesis type, hypothesis statement, prediction or expected observation, plan visual, evidence route, artifacts, planned discriminating test when the claim requires one, and stop / branch criteria. Mechanistic fields are required only when the hypothesis is mechanistic. Do not explain why an unobserved result happened. **Post-result explanations** belong to `research-result-analysis` after evidence exists.

## Review purpose

The purpose is to stop execution before research time is spent on a plan that should not run. This is a stop gate, not a general advice pass.

Review only two load-bearing questions:

1. **Premise check**: is the hypothesis built on a wrong premise, unsupported premise, unverified premise, contradicted project state, missing observation, or prior-work claim that is not actually grounded?
2. **Hypothesis validation method**: can the planned experiment, analysis, derivation, evaluator, comparator, or limiting-case check really validate the stated hypothesis type?

If either answer is no, return `block_execution`. Do not downgrade to `revise_before_execution` because the plan is mechanically runnable, cheap, deadline-driven, demo-visible, or easy to patch later.

## Workflow

1. **Read the plan**  
   Identify category, mode, Question / Objective, Idea portfolio when present, Prior-work grounding, Survey evidence, Citation-use map, Divergence checkpoint, and Plan. Prior-work grounding must cite `literature/papers.md` and `literature/positioning.md`, or record a retrieval-unavailable constraint with evidence.

2. **Check the premise first**  
   Ask whether the question/objective and hypothesis follow from the recorded observations, project state, known failures, constraints, prior work, and Divergence checkpoint. If the plan contradicts recorded project state or revives a closed/replaced route without new evidence, block execution. If a proxy metric has already been discredited for the stated objective, a plan using only that proxy is a wrong-premise plan.

3. **Check the hypothesis validation method**  
   Ask whether the plan can validate the stated hypothesis type, not merely measure a convenient proxy. Use the type decision procedure in `references/mechanistic_hypothesis_generation.md`: if the intended claim is only "A improves metric B over baseline C," the type is predictive / performance. Predictive / performance hypotheses need a fair comparator, evaluation protocol, primary measure, threshold, and leakage / variance / split policy when relevant. A mechanism hypothesis needs evidence that can bear on the proposed entities, activities, process, organization, or mechanism of action; its plan should include a planned discriminating test when the mechanism claim requires one. Causal / intervention hypotheses need an intervention, outcome, control/comparator, assumptions, and evidence route. Descriptive hypotheses need a defined variable space and measurement. The review must not turn a predictive / performance hypothesis into a mechanism study. For theoretical mode, check the derivation question, axioms / definitions / prior theorems, proposed derivation route, limiting-case checks, empirical sanity check if present, and named failure modes.

4. **Check the Plan visual**
   Plan must start with `### Plan visual`. If the section is missing, return `revise_before_execution` or `block_execution` depending on whether the missing visual affects the premise or validation method. If the plan contains an architecture, data flow, evaluation flow, mechanism, causal relation, system boundary, variable space, decision flow, or derivation dependency, require a Mermaid, PlantUML, ASCII, or durable linked figure/table visual that makes that structure inspectable. If it says `No diagram:`, accept it only when the reason explains why no visual would help.

5. **Check prior-work survey evidence**
   Block execution when Survey evidence is missing, left as `TBD`, or replaced by an unknown-prior-work constraint without search evidence or a retrieval-unavailable constraint. Retrieval-unavailable is not a survey bypass: block execution unless the plan records a verifiable signal with attempted source/tool, query or source ID when available, failure evidence, and claim-scope narrowing. Also block a bibliography without use mapping: each cited work must appear in the Citation-use map with a concrete role in the plan. A plan can use `revise_before_execution` for incomplete summaries, but absence of survey evidence or citation-use mapping is a pre-execution blocker because controls, comparators, baselines, claim scope, and often the premise itself are not grounded. Sub-field completion is not grounding sufficiency; filled fields must still substantively connect the cited work to the question, method, controls/comparators, evidence route, limitations, and claim scope.

6. **Return**
   Return a `## Plan review` section that names premise blockers, validation-method blockers, required repairs, and whether the plan should execute as written.

## Block Rules

Return `block_execution` when any of these are true:

- The hypothesis rests on a wrong, unsupported, or unverified premise.
- The question/objective does not follow from the recorded project state, observations, constraints, or prior-work grounding.
- The plan contradicts a previous `CLOSE: replaced`, `PARK`, or disconfirmed route without recording new evidence that reopens it.
- The stated objective depends on a proxy that the plan does not justify, or that prior project state has already discredited for that objective.
- The planned validation cannot test the stated hypothesis type, or it uses a proxy/comparator/evidence route that cannot support the claim.
- The Plan visual is missing or replaced by a weak `No diagram:` rationale in a plan whose architecture, data flow, evaluation flow, mechanism, system boundary, variable space, decision flow, or derivation dependency needs visual inspection.
- Survey evidence or Citation-use mapping is missing in a way that leaves the premise, comparator, evidence route, or claim scope ungrounded.

Return `revise_before_execution` only when the premise and validation route are basically sound and the required repair is concrete and local. A plan being mechanically runnable is not evidence that its premise or validation method is sound.

## Output Shape

```markdown
## Plan review

### Reviewer
- Agent: <fresh separate-context plan-review subagent>
- Skill: research-plan-review
- Plan reviewed: <plan path>
- Reviewed at: <YYYY-MM-DD>

### Design summary
- <what the plan is trying to learn or build, the hypothesis or principle under review, and the validation route>

### Research-design checks
- Premise check: <adequate / revise / block>: <whether the hypothesis rests on a wrong / unsupported / unverified premise, contradicted project state, discredited proxy, or ungrounded prior-work claim>
- Hypothesis validation method: <adequate / revise / block>: <whether the planned validation can test the stated hypothesis type without turning it into a different research question>
- Plan visual: <adequate / revise / block>: <whether architecture, data flow, evaluation flow, mechanism, system boundary, variable space, decision flow, or derivation dependency is inspectable>
- Prior-work survey evidence: <adequate / revise / block>: <missing Survey evidence or Citation-use map means block_execution unless a retrieval-unavailable constraint has a verifiable signal, attempted source/tool, failure evidence, and claim-scope narrowing>
- Stop decision: <continue / repair_before_execution / stop_execution>: <why the plan may run, must be repaired, or must stop>

### Category-specific concerns
- <only concerns that affect the premise check or hypothesis validation method; do not list non-blocking polish>

### Required repairs before execution
- <None, or concrete plan edits needed before execution>

### Execution recommendation
- <execute_as_written / revise_before_execution / block_execution>: <rationale>
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Reviewing formatting instead of the premise | Review whether the plan is built on a true and grounded premise, not whether headings are filled. |
| Treating filled fields as grounding | Sub-field completion is not grounding sufficiency; require a substantive citation-to-plan connection or return `block_execution`. |
| Accepting metric movement as research | For predictive / performance hypotheses, require a fair comparator, defined metric, threshold, and material validity checks. Require mechanism evidence only when the hypothesis claims a mechanism. |
| Turning performance plans into mechanism studies | Review the stated hypothesis type. Do not add why-it-worked decomposition unless the plan claims a mechanism. |
| Accepting prose-only plans for structured designs | Require a Plan visual when the plan has architecture, data flow, evaluation flow, mechanism, system boundary, variable space, decision flow, or derivation dependency. |
| Downgrading a broken premise because the plan can run | Mechanically runnable is not enough; wrong-premise plans get `block_execution`. |
| Nitpicking parameters while the premise is broken | Stop execution first; parameter advice is irrelevant when the premise fails. |
| Writing result analysis during plan review | Keep to pre-result commitments; post-result explanations require observed evidence. |
| Ignoring alternatives | Name counter-hypotheses and procedure/artifact risks before execution, not explanations for results that do not exist yet. |
| Doing the experiment | Stop at plan review; execution belongs to the parent research workflow. |
