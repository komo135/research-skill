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
mode: exploratory | confirmatory | milestone | theoretical
status: planned | in_progress | completed | parked | killed | replaced
created_at: YYYY-MM-DD
created_commit: <git sha — auto-filled by new_plan.py>
last_updated: YYYY-MM-DD
---

# <Plan title>

## Question / Objective
<One paragraph stating what this plan investigates or builds.>

## Idea portfolio
<Optional except when the user asked for research ideas, research directions, hypothesis candidates, or "what should we try next." Record the substrate-driven ideation contract from `references/ideation.md`: idea substrate, de-anchored seed generation, hypothesis-generation handoff or a Not-used reason, main-agent intake, generation operators, assumption audit, anti-vacuity gate, evaluator feedback, grounded pruning, information-gain scoring, and the one candidate promoted into this plan. Raw seeds are not accepted ideas.>

## Prior-work grounding
<Bounded but sufficient grounding for the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations. Cite `literature/papers.md` and `literature/positioning.md`. If prior work is genuinely unknown, record the named constraint and narrow or block relevant claims.>

## Divergence checkpoint
<Plan-time record of alternatives, anchoring risks, research positioning, disconfirming evidence, and why this plan commits to the chosen route.>

## Plan
<Mode-specific structure — see below.>

## Plan review
<Returned section from a fresh separate-context plan-review subagent using `research-plan-review`. The plan path is the only starting context. Required before execution.>

## Actual execution
<What was done. Updated as runs accumulate.>

## Planned vs Actual
<Differences between plan and execution, with reasoning. Empty if no deviation.>

## Result analysis
<Returned section from a fresh separate-context result-analysis subagent using `research-result-analysis`. The plan path is the only starting context; missing evidence is recorded as `context_missing`. Explains what happened and why before Claims, state-changing Decision, or report.>

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

This section appears after `## Question / Objective` and before `## Prior-work grounding` when the user asks for research ideas, research directions, hypothesis candidates, or "what should we try next." It records the output of `references/ideation.md`, including the idea substrate, anchor-stripped seed brief, excluded-anchor ledger, hypothesis-generation handoff or a Not-used reason, main-agent intake, raw seed generation, generation operators, anti-vacuity gate, evaluator feedback, and promotion decision.

The section is optional for ordinary plans that begin with an already chosen objective. It is required for ideation tasks because prior-work-first planning can anchor the agent to the literature's safest extensions before raw seeds and substrate/operator candidates exist.

```markdown
## Idea portfolio

### Idea substrate
- S1: <empirical / failure-mode / tension / baseline / constraint / literature / user-problem observation>
- S2: <second substrate item>
- S3: <third substrate item when available>

### Generation operators
- <candidate>:
  - Substrate ids: <S1, S2, ...>
  - Operator: <assumption inversion / failure-mode exploitation / bottleneck relocation / mechanism transfer / measurement reframing / counterfactual control / boundary-condition search / evaluator construction / problem reframing>
  - Changed premise: <what this candidate changes about the current framing>

### De-anchored candidates
- Seed brief: <anchor-stripped brief with substrate ids only>
- Excluded-anchor ledger: <prior-work names, SOTA systems, previous best approaches, user-preferred methods, convenient datasets, or None>
- <candidate>: <raw seed generated before prior-work grounding; not accepted until operator + anti-vacuity gate pass>

### Hypothesis-generation handoff
- Agent: <fresh separate-context hypothesis-generation agent, or Not used with reason>
- Starting context: <anchor-stripped seed brief is the only generation brief; Excluded-anchor ledger is not input>
- Web/literature retrieval: <used for abstract observations or cross-domain mechanisms / skipped with reason>
- Output contract: <multiple working hypotheses with source observation, mechanism conjecture, predicted effect, counter-hypothesis, minimal disconfirming test, and retrieval notes>

### Main-agent intake
- Authority check: <generator output is seed material, not accepted authority, claim, plan, or decision>
- Observation trace check: <which substrate ids each hypothesis truly traces to, or missing-substrate constraint>
- Mechanism review: <whether each mechanism explains observations, merely swaps methods, or is post-hoc prose>
- Decision: <advance / park / kill / merge / regenerate for each hypothesis>
- Next-plan action: <promote toward current plan / open ADJACENT evaluator-construction plan / gather substrate / run grounded pruning / no plan>

### Assumption audit
- Reference model challenged: <model, framing, baseline story, or implicit premise being challenged>
- Assumptions considered: <at least three named assumptions>
- Load-bearing assumption: <assumption selected after downstream-check>
- Downstream-check result: <why it is not downstream of a deeper in-scope assumption>
- Inversion candidate or no-inversion reason: <candidate that uses the inversion, or why none is admissible>

### Anti-vacuity gate
- <candidate>:
  - Substrate ids: <at least two substrate ids, or named missing-substrate constraint>
  - Changed premise: <what becomes false, weaker, conditional, or newly observable if the candidate is right>
  - Mechanism conjecture: <why the changed premise would produce the predicted behavior>
  - Predicted measurable effect: <observable measure expected to change>
  - Counter-hypothesis: <alternative explanation with a different prediction under the minimal test>
  - Minimal disconfirming test: <smallest observation, comparison, ablation, derivation check, or evaluator result that would kill or narrow the candidate>
  - Verdict: <survives / killed; candidate is killed if any field is generic, circular, unavailable, or disconnected from substrate ids>

### Blind-spot catalog
- <candidate that survived anti-vacuity or was promoted>:
  - Blind-spot area: <adjacent knowledge area or missing result pattern, or None with reason>
  - How it could break the mechanism: <failure path if the blind spot is real>
  - Claim-scope effect: <conditions_not_tested: ... / narrowed_claim: ... / PARK: ... / ADJACENT: ... / no_change: reason>
  - Required repair: <retrieval: ... / user_input: ... / evaluator_construction: ... / narrow_conditions: ... / none_with_reason: reason>

### Hypothesis synthesis
- <candidate that survived anti-vacuity>:
  - Source observation: <substrate ids plus observed phenomenon, failure mode, capability gap, empirical regularity, or theoretical tension>
  - Mechanism conjecture: <proposed mechanism that would explain the observation or make the intervention plausible>
  - Proposed intervention: <method, architecture, data change, metric change, evaluation change, system change, or framing change>
  - Predicted effect: <measurable effect expected if the mechanism conjecture is right>
  - Counter-hypothesis: <plausible alternative explanation under which the predicted effect should not appear>
  - Minimal disconfirming test: <smallest test, ablation, comparison, derivation check, or observation that would reject, narrow, or park the candidate>

### Evaluator feedback
- Status: <Ran: executable evaluator / Skipped: named reason>
- Executable signature: <real command-line invocation or None if skipped>
- Artifact: <run directory plus durable artifact path; stdout alone is not evidence; None if skipped>
- Fitness vector: <parseable score vector and uncertainty/variance if available; None if skipped>
- Required evaluator or artifact: <what must exist before executable feedback is possible; None if ran>
- Killed candidates: <candidate ids and real failure reasons; None if none>
- Cycle-final winner: <candidate id and rationale; None if skipped>
- Effect on promotion: <PARK / ADJACENT evaluator-construction plan / theoretical-only scope / advance with narrowed claim>

### Grounded pruning
- Advance: <candidate promoted toward a plan and why>
- Parked: <candidate blocked by missing survey, data, baseline, or condition>
- Killed: <candidate that is duplicate, untestable, too costly, not falsifiable, or only a parameter sweep>
- Merged: <candidates collapsed into another candidate>

### Information-gain scoring
- <candidate>: <testability, measurement clarity, expected information gain, cost, prior-work distance, claim discipline>

### Pre-execution divergence review
- Portfolio breadth: <whether candidates are meaningfully distributed across generation operators and difference axes>
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

Do not skip this checkpoint when the user asks to avoid exploration or to use only the previous approach. The final plan may still choose the user-requested route, but skipped divergence must be recorded under `Skipped divergence` and carried into Plan review. If a hard constraint truly permits only one route, say so directly and narrow the later claim scope to that constraint. Scope narrowing cannot rescue a weak design; the Plan review can block execution until the design is repaired.

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

### Mode: theoretical

For pure conceptual / derivational work where the claim rests on a formal derivation rather than empirical observation (e.g., a new closed-form result, a proof of equivalence between two formulations, a derived bound). Use this mode for `basic_research` plans with `mode: theoretical` and for any applied / experimental_development plan whose primary contribution is a mathematical or algorithmic derivation rather than an empirical result.

Empirical verification (when it exists) is treated as a secondary check (limiting-case match), not as the primary evidence.

```markdown
### Derivation question
- <one sentence stating what is to be proved, derived, bounded, or characterized>

### Axioms / definitions / prior theorems used
- <axiom or definition 1>: <statement, source if from external work>
- <axiom or definition 2>: ...
- <prior theorem 1>: <statement, source>
- <prior theorem 2>: ...

### Proposed derivation sketch
- <high-level chain of reasoning the derivation will follow>
- <key lemmas or sub-results expected>
- <techniques the derivation will rely on (e.g., induction on N, change of variables, fixed-point argument)>

### Predicted form of result
- <expected shape of the result: closed-form expression, asymptotic bound, equivalence statement, etc.>
- <units and scope where applicable>

### Limiting-case checks
- <known case 1 the result must reduce to>: <expected reduction>
- <known case 2>: ...
- These are the analog of "controls/comparators" for theoretical work; the derivation must recover known correct behavior in stated limits.

### Empirical sanity check (if applicable)
- <one observable consequence the derivation predicts that could be checked against existing data or simulation>
- <state explicitly if no such check is available; this triggers the assumption_audit constraint-naming protocol for the resulting claim>

### Failure modes to watch
- <derivation step where an assumption could silently fail>
- <known pathological case where the result might break>
- <symmetry or invariance that must be preserved and how it will be checked>

### Time / page envelope
- <budget for the derivation work itself; for long derivations, plan checkpoint reviews>
```

The Plan review subagent (`Plan review` section) is required for theoretical plans before execution, with adapted design criteria:
- **Derivation design** → "does the planned derivation route address the question with named axioms, definitions, prior theorems, and likely failure points?"
- **Discriminating checks** → "are limiting-case checks, counterexample searches, or empirical sanity checks sufficient to expose a broken derivation route?"

When no empirical evaluator exists, `Limitations` (in the eventual report) records this via the `references/assumption_audit.md` constraint-naming protocol (e.g., "no decisive empirical evaluator at the present state of knowledge").

## Plan review section

Before execution, dispatch a fresh separate-context plan-review subagent with the `research-plan-review` skill. Pass only the plan path as the starting context. The reviewer evaluates research design before any results exist.

Plan review may return an execution recommendation because it is a pre-execution design gate. That recommendation is not a claim-readiness verdict; readiness, claims, decisions, and reports remain outside plan review.

Record the subagent output in the plan:

```markdown
## Plan review

### Reviewer
- Agent: <fresh separate-context plan-review subagent>
- Skill: research-plan-review
- Plan reviewed: <plan path>
- Reviewed at: <YYYY-MM-DD>

### Design summary
- <one short paragraph describing the planned question/objective, mechanism or principle under investigation, predicted effect or output, and evidence route>

### Research-design checks
- Category/mode fit: <adequate / revise / block>: <reason>
- Mechanism hypothesis or principle: <adequate / revise / block>: <reason>
- Prediction or expected output: <adequate / revise / block>: <reason>
- Discriminating test: <adequate / revise / block>: <reason>
- Controls, comparators, or limiting cases: <adequate / revise / block / not applicable>: <reason>
- Evidence route and artifact plan: <adequate / revise / block>: <reason>
- Scope and constraints: <adequate / revise / block>: <reason>

### Category-specific concerns
- Basic research: <phenomenon, mechanism, or principle clarity; None if not applicable>
- Applied research: <practical objective, mechanism-to-intervention path, or evaluation concerns; None if not applicable>
- Experimental development: <acceptance criteria, system boundary, or operational evidence concerns; None if not applicable>

### Required repairs before execution
- <None, or concrete plan changes required before execution>

### Execution recommendation
- <execute_as_written / revise_before_execution / block_execution>: <rationale>
```

If the recommendation is `revise_before_execution` or `block_execution`, repair the plan and run a new Plan review before executing. The reviewer does not execute the plan, analyze results, write final claims, or choose the iteration branch.

## Actual execution section

Updated after work runs:

Research scripts must leave evidence, not just console text. A print-only execution is incomplete because stdout is not evidence. Each completed run should have a `run_manifest.json` with `status: completed` and manifest-listed artifacts, captured `logs/stdout.log` and `logs/stderr.log`, and at least one non-log durable artifact in `outputs/`, `tables/`, `figures/`, or `intermediate/`. Run `scripts/check_run_artifacts.py` before using a run as the basis for Observations, Result analysis, Claims, or a report.

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

## Result analysis section

Before Claims, a state-changing Decision, or report drafting, dispatch a fresh separate-context result-analysis subagent with the `research-result-analysis` skill. Use `references/result_analysis_subagent_prompt.md` and pass only the plan path as the starting context.

The analysis subagent reconstructs evidence from the plan's references: runs, `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, scripts, configs, outputs, tables, figures, reports, and literature entries. If evidence cannot be found or interpreted from those references, it records `context_missing` rather than relying on parent-agent summaries.

Record the subagent output in the plan. The analysis explains why the result happened; it does not assess readiness, write final claims, choose iteration decisions, or draft reports.

```markdown
## Result analysis

### Analyzer
- Agent: <fresh separate-context result-analysis subagent>
- Skill: research-result-analysis
- Only starting context: <this plan path>
- Analyzed at: <YYYY-MM-DD>

### Evidence traced
- Plan: <plan path>
- Runs and artifacts: <manifest/log/output/table/figure/script paths inspected>
- context_missing: <None, or missing/ambiguous plan references, artifacts, logs, scripts, metrics, comparators, or literature entries>

### What happened
- <artifact-grounded result summary, including values and deviations from the plan>

### Prediction comparison
- <planned prediction / threshold / expected condition versus observed value; note whether the prediction was met, missed, reversed, or only partly satisfied>

### Candidate explanations
- <explanation 1 for why the result happened>
  - Evidence for: <supporting artifacts, metrics, logs, or plan facts>
  - Evidence against: <contradicting artifacts, missing diagnostics, or observations that do not fit>
- <explanation 2>
  - Evidence for: <...>
  - Evidence against: <...>

### Failed prediction analysis
- Observed gap: <prediction, threshold, or expected condition versus observed result>
- Candidate failure explanations:
  - <candidate explanation for why the prediction missed>
    - Why this could explain the miss: <mechanism connecting evidence to the missed prediction>
    - Evidence for: <artifact-grounded support>
    - Evidence against: <artifact-grounded contradiction or weakness>
    - What would be true if this explanation is correct: <testable implication>
    - Missing discriminator: <smallest analysis that would separate this explanation from alternatives>
- Coverage check: <which lenses were considered: premise/mechanism, approach/intervention, procedure/artifact/data/comparator/implementation/measurement, evaluation/power/metric/scope. Do not force a category; record only live explanations above.>

### Procedure / artifact explanations
- <procedure defect, leakage path, broken comparator, missing artifact, data issue, plan deviation, or None with reason>

### Alternatives still live
- <plausible explanation, confound, comparator issue, missing control, untested condition, or theoretical gap still compatible with the evidence>

### Discriminating next analyses
- <analysis, check, rerun, or artifact reconstruction that would distinguish among explanations>
```

## Claims section

Use the schema from `claim_structure.md`. Each load-bearing claim is one YAML-like record:

```yaml
- claim: ...
  evidence: ...
  alternatives_not_excluded: [...]
  conditions_tested: ...
  conditions_not_tested: [...]
```

`scripts/check_claims.py` verifies the structure. Run it before changing the plan's status from `in_progress` to anything else, and before drafting a report. A Plan review section from `research-plan-review`, durable run artifacts, and a Result analysis section from `research-result-analysis` must already exist before any load-bearing claim, state-changing status change, or report draft.

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
- **Literature-first ideation.** If the user asked for research ideas, do not summarize prior work before generating raw seeds and substrate/operator candidates. Use the Idea portfolio section, then apply Prior-work grounding.
- **Portfolio made of parameter tweaks.** Three thresholds of the same signal are not three approaches. Record them as one primary route with a sweep, then add real alternatives or explicitly narrow the claim scope to the tested route.
- **Prior result treated as fact.** "Previous run was best" is an anchor, not a premise. Record what would revalidate it, what rework is required, or what claim condition remains after Result analysis explains the new outcome.
- **Claim made before prior-work grounding.** If the plan says novel, new method, publishable, to our knowledge, or no baseline exists, cite or update `literature/positioning.md` and point to a comprehensive literature survey before execution. If the claim is not a novelty claim, the plan still needs bounded but sufficient prior-work grounding and must classify itself as replication, baseline strengthening, engineering, or another grounded position.
- **Executing without Plan review.** A plan can be well formatted and still be a bad research design. Before execution, a fresh separate-context plan-review subagent using `research-plan-review` must review the plan path.
- **Closing without Result analysis.** Before Claims, state-changing Decision, or report, a fresh separate-context result-analysis subagent using `research-result-analysis` must explain what happened and why from the plan path and artifacts.
- **Treating result analysis as a decision gate.** Result analysis decomposes explanations; it does not write final claims, assess readiness, or choose the iteration branch.
- **Updating the Plan section after execution.** Plans get amended prospectively via `REFINE`. After-the-fact plan rewriting destroys the time-anchor — git diff will show the rewrite and any reviewer will catch it. Use the Planned vs Actual section instead.
- **Methodology description too thin.** "We ran the experiments" is not a Methodology subsection. State the procedure, the parameters, the protocol.
