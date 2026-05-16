# R&D Plan File Schema

## Purpose

`plans/<plan_id>_<slug>.md` is the agent's working state for one R&D investigation. It contains the plan, the actual execution narrative, the comparison, the claims, and the decision. It is the durable record across sessions.

This is **not** a write-once preregistration document. It is a live narrative. Git history is the time-anchor — the initial plan commit is the "preregistration" moment; subsequent commits show the evolution and are themselves auditable. Git history is an audit trail, not a substitute for methodology; the plan still has to describe the method, data, evaluation protocol, and material conditions well enough for re-implementation.

Why one file instead of separate prereg + plan: separate files would impose redundant maintenance with no additional discipline. Git already proves the plan existed before the result. The agent's job is to keep the document honest, not to keep two synchronized documents.

## File template

```markdown
---
plan_id: <id>
slug: <short-kebab-case-slug>
category: basic_research | applied_research | experimental_development
mode: exploratory | confirmatory | milestone
status: planned | in_progress | completed | parked | killed | replaced
created_at: YYYY-MM-DD
created_commit: <git sha — auto-filled by new_plan.py>
last_updated: YYYY-MM-DD
---

# <Plan title>

## Question / Objective
<One paragraph stating what this plan investigates or builds.>

## Idea portfolio
<Optional except when the user asked for research ideas, research directions, hypothesis candidates, or "what should we try next." Summarize de-anchored candidates generated from a sanitized brief by a fresh de-anchoring subagent, transformation axes from `references/ideation.md`, grounded pruning, information-gain scoring, and the one candidate promoted into this plan.>

## Prior-work grounding
<Bounded but sufficient grounding for the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations. Cite `literature/papers.md` and `literature/positioning.md`. If prior work is genuinely unknown, record the named constraint and narrow or block relevant claims.>

## Divergence checkpoint
<Plan-time record of alternatives, anchoring risks, research positioning, disconfirming evidence, and why this plan commits to the chosen route.>

## Plan
<Mode-specific structure — see below.>

## Actual execution
<What was done. Updated as runs accumulate.>

## Planned vs Actual
<Differences between plan and execution, with reasoning. Empty if no deviation.>

## Research review
<Summary from exactly one research-review subagent, covering analysis sufficiency and result reliability. Required before Claims, state-changing Decision, or report.>

## Claims
<Load-bearing claims using the schema in claim_structure.md.>

## Decision
<One of NEXT_STEP / REFINE / ADJACENT / PARK / CLOSE — see iteration_loop.md.>

## References
- Runs: experiments/<plan_id>_<slug>/runs/...
- Related plans: <other plan IDs and their relationship>
- Related literature: <see literature/papers.md entries>
```

## Idea portfolio section

This section appears after `## Question / Objective` and before `## Prior-work grounding` when the user asks for research ideas, research directions, hypothesis candidates, or "what should we try next." It records the output of `references/ideation.md`, including the sanitized brief and fresh de-anchoring subagent used for raw candidate generation.

The section is optional for ordinary plans that begin with an already chosen objective. It is required for ideation tasks because prior-work-first planning can anchor the agent to the literature's safest extensions before raw candidates exist.

```markdown
## Idea portfolio

### De-anchored candidates
- Generator: <fresh de-anchoring subagent identifier; sanitized brief only>
- <candidate>: <one sentence, generated before prior-work grounding>

### Transformation axes
- <candidate>: <method / mechanism / data assumption / metric / evaluation protocol / system design / problem framing>

### Hypothesis synthesis
- <candidate>:
  - Source observation: <observed phenomenon, failure mode, capability gap, empirical regularity, or theoretical tension>
  - Mechanism conjecture: <proposed mechanism that would explain the observation or make the intervention plausible>
  - Proposed intervention: <method, architecture, data change, metric change, evaluation change, system change, or framing change>
  - Predicted effect: <measurable effect expected if the mechanism conjecture is right>
  - Counter-hypothesis: <plausible alternative explanation under which the predicted effect should not appear>
  - Minimal disconfirming test: <smallest test, ablation, comparison, or observation that would reject, narrow, or park the candidate>

### Grounded pruning
- Advance: <candidate promoted toward a plan and why>
- Parked: <candidate blocked by missing survey, data, baseline, or condition>
- Killed: <candidate that is duplicate, untestable, too costly, or not falsifiable>
- Merged: <candidates collapsed into another candidate>

### Information-gain scoring
- <candidate>: <testability, measurement clarity, expected information gain, cost, prior-work distance, claim discipline>

### Pre-execution divergence review
- Portfolio breadth: <whether candidates are meaningfully distributed across transformation axes>
- Parameter sweep laundering: <whether any candidate is only a threshold, seed, model-size, or sweep variant>
- Anti-anchor check: <whether literature-first, prior-work-first, winning-approach, convenient-data, or user-preference anchors narrowed the portfolio too early>
- Required repair before promotion: <None, or candidate regeneration / merge / kill / park action>

### Promotion decision
- Promoted idea: <the single candidate that becomes this plan>
- Non-promoted ideas: <parked / killed / merged reasons; these are not claims>
```

## Prior-work grounding section

Every plan has first-class prior-work grounding before the Divergence checkpoint and before the Plan section. This is not optional just because no novelty claim is made. The grounding must be bounded but sufficient: enough to support the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations.

Use `literature/papers.md` for cited prior work and `literature/positioning.md` for how the work stands on prior work. `positioning.md` is where the plan records grounding, inheritance, control/comparator choice when relevant, known limitations, and claim scope. Differences or novelty can be recorded there when claimed, but novelty is not the default purpose.

If prior work is genuinely unknown, the plan must record a named constraint and narrow or block relevant claims until the grounding is repaired. Comprehensive literature survey is required for strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims; this is separate from the plan-scoped grounding every plan needs.

```markdown
## Prior-work grounding

### Grounding scope
- Question/objective supported by: <literature/papers.md entries and why they are relevant>
- Inherited assumptions: <assumptions carried from prior approaches, data, results, or systems>
- Method choice: <prior work or constraint motivating the selected method family>
- Controls/comparators/evaluation protocol: <baseline, control, metric, split, benchmark, acceptance-test source, or other evidence route>
- Known limitations: <limitations from prior work that constrain interpretation>

### Research positioning
- Positioning entry: <literature/positioning.md entry>
- Claim scope: <what this grounding supports, narrows, or blocks>
- Unknown prior-work constraint: <named constraint and affected claims; None if none>
```

## Divergence checkpoint section

```markdown
## Divergence checkpoint

### Approach portfolio
- Primary route: <the candidate approach selected for execution>
- Alternative A: <an approach based on a different principle, data assumption, evaluation target, or design>
- Alternative B: <another meaningfully different approach; simple threshold changes, extra seeds, and larger versions do not count>

### Anchoring audit
- Prior result / approach / dataset being imported: <what premise is being carried into this plan>
- Risk if the anchor is wrong: <what interpretation would break if that premise is false>
- Revalidation or control: <holdout / alternate period / placebo / control / condition change>

### Research positioning
- Contribution type: <question / mechanism / data / metric / evaluation protocol / method / system / replication / baseline strengthening>
- Positioning status: <literature/positioning.md entry and claim scope>
- External novelty / no-baseline claim: <None, or comprehensive literature survey reference before execution>

### Disconfirming evidence
- Stop, narrow, or pivot if: <observation that would force a narrower question, a different route, a pause, or closure>
- Branch if observed: <REFINE / ADJACENT / PARK / CLOSE>

### Commitment decision
- Chosen route and reason: <why this plan commits to this route now>
- Skipped divergence: <alternatives not explored because of time or resource limits; None if none>
- Effect on later claims: <how this limits later claims or narrows the tested conditions>
```

Do not pad the `Approach portfolio`. Different LSTM depths, thresholds on the same signal, or seeds on the same dataset are not different approaches. An alternative differs from the primary route in at least one of: method family, data assumption, evaluation target, mechanism, or system design.

Do not skip this checkpoint when the user asks to avoid exploration or to use only the previous approach. The final plan may still choose the user-requested route, but skipped divergence must be recorded under `Skipped divergence` and carried into the later Research review. If a hard constraint truly permits only one route, say so directly and narrow the later claim scope only after the later Research review records `PASS` for both analysis sufficiency and result reliability. Scope narrowing cannot rescue insufficient analysis or distorted results.

If the plan says novel, new method, publishable, to our knowledge, or no baseline exists, `Research positioning` must cite `literature/positioning.md` and the plan must point to a comprehensive literature survey before execution. Lack of a novelty claim never exempts the plan from bounded but sufficient prior-work grounding.

## Plan section by mode

### Mode: exploratory

Fix the boundaries, not the prediction. From Dirnagl (PLOS Biology 2020): exploratory work commits to the *space of investigation*, not to a point hypothesis.

```markdown
### Variable space
- <variable 1>: <range, justification>
- <variable 2>: ...

### Allowed transformations / procedures
- <list of analyses the agent may apply during exploration>
- <if useful: out-of-scope analyses to call out>

### Selection / follow-up criteria
- <what observations would trigger a deeper look>
- <what would trigger PARK or CLOSE>

### Expected output type
- <type of artifact: phenomenon description, refined question, characterized baseline, failure-mode catalog, theoretical insight>

### Out of scope
- <explicit list of things not to chase, to prevent scope creep>
```

### Mode: confirmatory

Fix the hypothesis or objective, primary evidence measure, and decision threshold. Include controls, comparators, or ablations when the planned claim requires them.

```markdown
### Hypothesis rationale
- Source observation: <observed phenomenon, failure mode, capability gap, empirical regularity, or theoretical tension>
- Mechanism conjecture: <proposed mechanism that would explain the observation or make the intervention plausible>
- Proposed intervention: <method, architecture, data change, metric change, evaluation change, system change, or framing change>
- Predicted effect: <measurable effect expected if the mechanism conjecture is right>
- Counter-hypothesis: <plausible alternative explanation under which the predicted effect should not appear>
- Minimal disconfirming test: <smallest test, ablation, comparison, or observation that would reject, narrow, or park the hypothesis>

### Hypothesis
- <one sentence statement of the prediction>

### Primary evidence measure
- <metric, observation, test result, or criterion; computation/assessment and units if applicable>

### Controls / comparators (if applicable)
- <control, comparator, or baseline name>: <description, source, version>
- <additional comparator>: ...

### Decision threshold
- <criterion for "hypothesis/objective supported"; quantitative when the evidence measure is numeric>
- <observation that would lead to rejection>

### Data / evaluation setup
- <specific datasets, materials, splits, evaluation protocol, or observation conditions>

### Compute / sample envelope
- <resource envelope: runs, samples, hardware time, deadline, or other execution constraint>

### Component checks planned (if applicable)
- <ablation or controlled intervention for individual contribution claims>
```

### Mode: milestone

Fix the acceptance criteria.

```markdown
### Functional milestones
- <feature 1>: <acceptance criterion>
- <feature 2>: ...

### Performance milestones
- <metric>: <threshold under stated conditions>

### Acceptance tests
- <list of scenarios the system must pass>

### Out of scope
- <explicit list of functionality not in this iteration>

### Compute / time envelope
- <resource envelope: runs, samples, hardware time, deadline, or other execution constraint>
```

## Actual execution section

Updated after work runs:

```markdown
### Runs
- <run_id>: <one-line summary, link to runs/<run_id>/>
- <run_id>: ...

### Methodology used
<Substantive description of what was done. Methods reproducibility — enough for someone else to re-implement based on this text. Include material conditions that affect interpretation: data identity, split dates, evaluation protocol, major model/tool versions, hardware class, external API/model version, collection date, and stochastic variability. These are material conditions, not env locks or commit hashes — run artifacts may carry audit pointers when useful.>

### Observations
<What was seen. Reference figures/tables in reports/<id>/figures/ if reports have been started.>
```

The Methodology subsection must be specific enough that a reader could re-implement. "We trained a Transformer" is not a methodology description. The architecture, training procedure, evaluation protocol, and data setup must be specific.

## Planned vs Actual section

If anything deviated from the plan, record it here. Deviations are not failures — undocumented deviations are.

```markdown
### Change 1: <short name>
- Description: <what changed>
- Rationale: <why>
- Effect on conclusions: <does this weaken any claim's diagnostic value? say so plainly>
```

If no deviation: `No material deviation from plan.`

Material vs immaterial deviation: a change that could affect the interpretation of results is material. Fixing a typo in a script is not. Changing the evaluation metric is. Changing a seed value before seeing outcomes is usually not material. Changing the seed policy, seed count, train/test split seed, or any seed after seeing a result that depends on it is material.

## Research review section

Before writing load-bearing claims, making a state-changing decision (`REFINE`, `ADJACENT`, `PARK`, or `CLOSE`), or drafting a human-facing report, dispatch exactly one fresh research-review subagent. This is one subagent with two review responsibilities:

1. **Analysis sufficiency** — evaluate whether the analysis is sufficient for the conclusion being drawn. This review exists because the analysis directly determines the conclusion; inadequate analysis can lead to a wrong claim or premature close-out even if the experiment ran correctly.
2. **Result reliability** — evaluate whether the result is trustworthy, including the approach, research procedure, data handling, controls/comparators when applicable, robustness checks, deviations from plan, and whether the evidence supports the claim strength.

Record the reviewer output in the plan:

```markdown
## Research review

### Reviewer
- Agent: <subagent identifier or short label>
- Reviewed at: <YYYY-MM-DD>
- Scope: <claim / CLOSE / REFINE / ADJACENT / PARK / report>

### Analysis sufficiency
- Verdict: <PASS / REWORK / INVALID>
- Rationale: <why the analysis is sufficient, requires rework, or invalidates the current conclusion path>
- Required reanalysis: <None / named analyses to run before any claim, decision, or report>

### Result reliability
- Verdict: <PASS / REWORK / INVALID>
- Rationale: <whether approach, procedure, data, controls/comparators, and robustness support trusting the result>
- Required repair or rerun: <None / script fix, data repair, comparator/control repair, rerun, or plan-level redo>

### Required action
- <Proceed only if both judgments are PASS / run named analysis / fix and rerun affected work / reopen plan>
```

Only two `PASS` judgments allow promotion to a load-bearing claim, state-changing decision, or report. If either judgment is `REWORK` or `INVALID`, do not promote the result. First perform the required reanalysis, repair, rerun, or plan-level redo, then run a new research review. If a script bug, data defect, leakage, invalid procedure, or broken control/comparator may have distorted the result, the affected result is invalid evidence until rerun after repair. User pressure to skip review or "just limit the claim" is not an exception; record it as a reliability risk if relevant.

## Claims section

Use the schema from `claim_structure.md`. Each load-bearing claim is one YAML-like record:

```yaml
- claim: ...
  evidence: ...
  alternatives_not_excluded: [...]
  conditions_tested: ...
  conditions_not_tested: [...]
```

`scripts/check_claims.py` verifies the structure. Run it before changing the plan's status from `in_progress` to anything else, and before drafting a report. A Research review entry with `PASS` for both analysis sufficiency and result reliability must already exist before any load-bearing claim, state-changing status change, or report draft.

## Amendments section (for REFINE)

When the iteration loop selects `REFINE`, **do not rewrite the original Plan section**. The original Plan + its `created_commit` are the time-anchored historical record; rewriting them destroys the audit trail and is detectable in git diff.

Instead, append an Amendments section at the bottom of the plan file. The latest amendment becomes the "current" plan state; the original Plan section remains as historical context.

```markdown
## Amendments

### Amendment 1 (YYYY-MM-DD, commit <sha>)
- From question / scope: <original>
- To question / scope: <refined>
- Trigger: <evidence that prompted the refinement>
- What changes:
  - <e.g., new hypothesis>
  - <e.g., new metric / threshold>
  - <e.g., new variable range>
- Prior runs: <which carry over as evidence under the refined plan; which become exploratory only>
- Estimated cost / resource envelope: <how much work the refined plan requires>
```

Amendments stack. If a second REFINE happens, append "Amendment 2" — do not edit Amendment 1. Each amendment is itself a time-anchored record (the commit creating it is the time-stamp).

Use the amendment pattern rather than rewriting because:
- For small refinements (a 12-run study getting a 9-run follow-up sweep), rewriting the whole Plan section is friction tax with no audit value.
- The original Plan + Amendment 1 + Amendment 2 chain reads as the evolution of the question — which is the honest research record.
- A reviewer can compare Amendment N to original Plan via git diff or by reading both sections.

When the amendment changes are large enough that "amendment" feels like a stretch (the question is fundamentally different, the category changes, the mode changes), it is no longer REFINE — it is ADJACENT (open a new plan) or CLOSE: replaced.

## Decision section

Use exactly one of:

```markdown
### NEXT_STEP
<one sentence describing the next planned step>
```

```markdown
### REFINE
- From: <original question>
- To: <refined question>
- Trigger: <evidence>
- Prior runs: <carry over | exploratory only | re-run under new plan>
```

```markdown
### ADJACENT
- New plan: <new plan id>
- Relationship: <blocks / feeds into / parallel>
- Trigger: <evidence>
```

```markdown
### PARK
- Unblock condition: <named, specific, testable>
- Current state: <what is done, what is pending>
```

```markdown
### CLOSE: completed | terminal_kill | replaced
- Final claim or conclusion: <one sentence, or claim_structure record if load-bearing>
- Report: <link to reports/<id>/report.md if produced>
- Replaced by: <plan id, if replaced>
```

Mirror the entry in `decisions.md` for any branch except `NEXT_STEP`.

## Common failures

- **No `mode` declared.** Pick exploratory, confirmatory, or milestone before writing the Plan section.
- **Mode mismatch with category.** Applied research is usually confirmatory; basic research is usually exploratory; experimental development is usually milestone. Mismatches need justification in the Plan section.
- **Confirmatory plan with no decision threshold.** The whole point of confirmatory is the threshold. State it explicitly.
- **Exploratory plan with hidden hypothesis.** Writing "we expect X" without committing to a decision threshold converts exploration into informal confirmation. Either commit to confirmatory mode with an explicit threshold, or stay honestly exploratory with a variable space.
- **No Divergence checkpoint.** A plan that only follows the user's preferred route can still be well formatted and still be weak research. Fill the checkpoint before execution.
- **Literature-first ideation.** If the user asked for research ideas, do not summarize prior work before generating raw candidates. Use the Idea portfolio section, then apply Prior-work grounding.
- **Portfolio made of parameter tweaks.** Three thresholds of the same signal are not three approaches. Record them as one primary route with a sweep, then add real alternatives or explicitly narrow the claim scope only after the later Research review records `PASS` for both judgments.
- **Prior result treated as fact.** "Previous run was best" is an anchor, not a premise. Record what would revalidate it, what rework is required, or what claim condition remains only after the later Research review records `PASS` for both judgments.
- **Claim made before prior-work grounding.** If the plan says novel, new method, publishable, to our knowledge, or no baseline exists, cite or update `literature/positioning.md` and point to a comprehensive literature survey before execution. If the claim is not a novelty claim, the plan still needs bounded but sufficient prior-work grounding and must classify itself as replication, baseline strengthening, engineering, or another grounded position.
- **Closing without research review.** A self-check is not enough. Before Claims, state-changing Decision, or report, one fresh research-review subagent must record `PASS` for both analysis sufficiency and result reliability.
- **Splitting the two review questions across agents.** The requirement is one research-review subagent with both judgments, so the reviewer can connect analysis gaps to reliability and claim strength.
- **Updating the Plan section after execution.** Plans get amended prospectively via `REFINE`. After-the-fact plan rewriting destroys the time-anchor — git diff will show the rewrite and any reviewer will catch it. Use the Planned vs Actual section instead.
- **Methodology description too thin.** "We ran the experiments" is not a Methodology subsection. State the procedure, the parameters, the protocol.
