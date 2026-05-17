---
name: research-plan-review
description: Use when reviewing an R&D plan before execution, especially when a plan may be runnable but rests on a wrong premise, unsupported premise, unverified premise, or weak hypothesis validation method.
---

# Research Plan Review

## Overview

Independent review for a drafted research plan before execution. The plan path is the starting context; the reviewer checks whether execution should stop because the hypothesis rests on a broken premise or because the validation method cannot test the hypothesis.

This skill reviews research design only. Do not execute the plan, do not analyze results, and do not write final claims.

The `Execution recommendation` is a pre-execution design recommendation: whether the plan is safe to run as written, needs repair, or should be blocked before execution. It is not a claim-readiness verdict and must not use result-analysis readiness labels.

Plan review covers **pre-result commitments** only: question/objective, mechanism hypothesis or principle, prediction or expected observation, evidence route, planned discriminating test, artifacts, and stop / branch criteria. Do not explain why an unobserved result happened. **Post-result explanations** belong to `research-result-analysis` after evidence exists.

## Review purpose

The purpose is to stop execution before research time is spent on a plan that should not run. This is a stop gate, not a general advice pass.

Review only two load-bearing questions:

1. **Premise check**: is the hypothesis built on a wrong premise, unsupported premise, unverified premise, contradicted project state, missing observation, or prior-work claim that is not actually grounded?
2. **Hypothesis validation method**: can the planned experiment, analysis, derivation, evaluator, comparator, or limiting-case check really validate the hypothesis and distinguish it from plausible alternatives?

If either answer is no, return `block_execution`. Do not downgrade to `revise_before_execution` because the plan is mechanically runnable, cheap, deadline-driven, demo-visible, or easy to patch later.

## Workflow

1. **Read the plan**  
   Identify category, mode, Question / Objective, Idea portfolio when present, Prior-work grounding, Survey evidence, Citation-use map, Divergence checkpoint, and Plan. Prior-work grounding must cite `literature/papers.md` and `literature/positioning.md`, or record a retrieval-unavailable constraint with evidence.

2. **Check the premise first**  
   Ask whether the question/objective and hypothesis follow from the recorded observations, project state, known failures, constraints, prior work, and Divergence checkpoint. If the plan contradicts recorded project state or revives a closed/replaced route without new evidence, block execution. If a proxy metric has already been discredited for the stated objective, a plan using only that proxy is a wrong-premise plan.

3. **Check the hypothesis validation method**  
   Ask whether the plan can validate the hypothesis, not merely measure a convenient proxy. The planned validation must separate the hypothesis from plausible alternatives, procedure defects, comparator issues, leakage, measurement artifacts, and broken derivation assumptions through pre-specified observations, controls, or artifact checks. A plan that can only show "metric went up" is not enough when the hypothesis asks why. For theoretical mode, check the derivation question, axioms / definitions / prior theorems, proposed derivation route, limiting-case checks, empirical sanity check if present, and named failure modes.

4. **Check prior-work survey evidence**
   Block execution when Survey evidence is missing, left as `TBD`, or replaced by an unknown-prior-work constraint without search evidence or a retrieval-unavailable constraint. Retrieval-unavailable is not a survey bypass: block execution unless the plan records a verifiable signal with attempted source/tool, query or source ID when available, failure evidence, and claim-scope narrowing. Also block a bibliography without use mapping: each cited work must appear in the Citation-use map with a concrete role in the plan. A plan can use `revise_before_execution` for incomplete summaries, but absence of survey evidence or citation-use mapping is a pre-execution blocker because controls, comparators, baselines, claim scope, and often the premise itself are not grounded. Sub-field completion is not grounding sufficiency; filled fields must still substantively connect the cited work to the question, method, controls/comparators, evidence route, limitations, and claim scope.

5. **Return**
   Return a `## Plan review` section that names premise blockers, validation-method blockers, required repairs, and whether the plan should execute as written.

## Block Rules

Return `block_execution` when any of these are true:

- The hypothesis rests on a wrong, unsupported, or unverified premise.
- The question/objective does not follow from the recorded project state, observations, constraints, or prior-work grounding.
- The plan contradicts a previous `CLOSE: replaced`, `PARK`, or disconfirmed route without recording new evidence that reopens it.
- The stated objective depends on a proxy that the plan does not justify, or that prior project state has already discredited for that objective.
- The planned validation cannot distinguish the hypothesis from plausible alternatives, procedure defects, comparator issues, leakage, measurement artifacts, or derivation failure modes.
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
- Hypothesis validation method: <adequate / revise / block>: <whether the planned validation can test the hypothesis and distinguish it from plausible alternatives>
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
| Accepting metric movement as research | Require a hypothesis validation method that can distinguish the hypothesis from plausible alternatives. |
| Downgrading a broken premise because the plan can run | Mechanically runnable is not enough; wrong-premise plans get `block_execution`. |
| Nitpicking parameters while the premise is broken | Stop execution first; parameter advice is irrelevant when the premise fails. |
| Writing result analysis during plan review | Keep to pre-result commitments; post-result explanations require observed evidence. |
| Ignoring alternatives | Name counter-hypotheses and procedure/artifact risks before execution, not explanations for results that do not exist yet. |
| Doing the experiment | Stop at plan review; execution belongs to the parent research workflow. |
