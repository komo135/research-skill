---
name: research-plan-review
description: Use when reviewing an R&D plan before execution, especially to test whether observations, hypotheses, predictions, controls, and discriminating analyses make the research design worth running.
---

# Research Plan Review

## Overview

Independent review for a drafted research plan before execution. The plan path is the starting context; the reviewer checks whether the design can answer the research question and separate plausible explanations.

This skill reviews design only. Do not execute the plan, do not analyze results, and do not write final claims.

The `Execution recommendation` is a pre-execution design recommendation: whether the plan is informative enough to run as written, needs repair, or should be blocked before execution. It is not a claim-readiness verdict and must not use result-analysis readiness labels.

## Workflow

1. **Read the plan**  
   Identify category, mode, Question / Objective, Idea portfolio when present, Prior-work grounding, Divergence checkpoint, and Plan.

2. **Review research design**  
   For applied research, check the chain from observation to mechanism hypothesis, proposed intervention, predicted measurable effect, counter-hypothesis, and discriminating test.  
   For basic research, check the principle, phenomenon, or structure to be understood; the observation or derivation route; the method for separating candidate explanations; and what would refine the question.  
   For experimental development, check that acceptance criteria also produce knowledge about why the system or process behaves as observed.
   For theoretical mode, check the derivation question, axioms / definitions / prior theorems, proposed derivation route, limiting-case checks, empirical sanity check if present, and named failure modes.

3. **Check discriminating power**  
   Ask whether the plan can separate the primary hypothesis from plausible alternatives, procedure defects, comparator issues, leakage, and measurement artifacts. A plan that can only show "metric went up" is not enough when the research objective asks why.

4. **Return**  
   Return a `## Plan review` section that names design strengths, blockers, required repairs, and whether the plan should execute as written.

## Output Shape

```markdown
## Plan review

### Reviewer
- Agent: <fresh separate-context plan-review subagent>
- Skill: research-plan-review
- Plan reviewed: <plan path>
- Reviewed at: <YYYY-MM-DD>

### Design summary
- <what the plan is trying to learn or build>

### Research-design checks
- Observation / phenomenon: <present / missing / weak, with rationale>
- Mechanism hypothesis or principle: <present / missing / weak, with rationale>
- Prediction or expected observation: <present / missing / weak, with rationale>
- Counter-hypothesis or alternative explanation: <present / missing / weak, with rationale>
- Discriminating test: <present / missing / weak, with rationale>

### Category-specific concerns
- <applied/basic/experimental-development issue that could make the plan uninformative>

### Required repairs before execution
- <None, or concrete plan edits needed before execution>

### Execution recommendation
- <execute_as_written / revise_before_execution / block_execution>: <rationale>
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Reviewing formatting instead of design | Review whether the plan can produce knowledge, not whether headings are filled. |
| Accepting metric movement as research | Require a mechanism hypothesis, principle, or explanation route when the objective asks why. |
| Ignoring alternatives | Name counter-hypotheses and procedure/artifact explanations before execution. |
| Doing the experiment | Stop at plan review; execution belongs to the parent research workflow. |
