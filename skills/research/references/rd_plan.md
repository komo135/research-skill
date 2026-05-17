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

## Mechanism hypothesis record
<Optional except when the user asked for research ideas, research directions, hypothesis candidates, or "what should we try next." Record the mechanistic generation contract from `references/mechanistic_hypothesis_generation.md`: research situation diagnosis, analysis lenses considered, adopted analysis lenses, mechanistic analysis, and a Mechanism hypothesis record with hypothesis, competing hypothesis, discriminating prediction, minimal test, required evidence, Decision, and Reason. This section does not replace Survey evidence.>

## Prior-work grounding
<Bounded but sufficient grounding from a plan-scoped literature survey for the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations. Cite `literature/papers.md` and `literature/positioning.md`. Record search date, queries/sources, selection rationale, negative findings, any retrieval-unavailable constraint, and a citation-use map that states how each cited work is used in the plan. If prior work is genuinely unknown after the survey, record the named constraint and narrow or block relevant claims.>

## Divergence checkpoint
<Plan-time record of alternatives, anchoring risks, research positioning, disconfirming evidence, and why this plan commits to the chosen route.>

## Plan
<Mode-specific structure — see below.>

## Plan review
<Returned section from a fresh separate-context plan-review subagent using `research-plan-review`. The plan path is the only starting context. Required before execution.>

## Actual execution
<What was done. Updated as runs accumulate. Record any mid-execution literature update when an unfamiliar method, unexpected result, new comparator, contradiction with prior work, or missing-baseline signal appears.>

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

## Mechanism hypothesis record section

This section appears after `## Question / Objective` and before `## Prior-work grounding` when the user asks for research ideas, research directions, hypothesis candidates, or "what should we try next." It records the output of `references/mechanistic_hypothesis_generation.md`.

The section is optional for ordinary plans that begin with an already chosen objective. It is required for ideation tasks because the user-visible contract is no longer a list of candidates. The contract is: diagnose the research situation, compare analysis lenses, adopt one primary lens plus 0-2 auxiliaries, convert the analysis into a mechanism hypothesis, separate a competing hypothesis, define a discriminating prediction and minimal test, then decide `commit / park / kill`.

This section does not replace Survey evidence. A `commit` decision is not final until Survey evidence exists; section order is not permission to finalize commit before Survey evidence.

```markdown
## Mechanism hypothesis record

<Not applicable: objective already chosen. If this plan began from research ideas, research directions, hypothesis candidates, or "what should we try next," use `references/mechanistic_hypothesis_generation.md` and record the full contract below. This section is required when the plan began from research ideas, research directions, hypothesis candidates, or "what should we try next." This does not replace Survey evidence.>

### Research situation diagnosis
- Available material: <successes, failures or limits, lineage, evaluation or measurement, constraints, unknowns, observable quantities, comparators, and counterfactuals>
- Missing material: <observations, reproduced failures, baselines, evaluator, measurement definitions, counterfactuals, prior-work grounding, or minimal model>
- Why hypothesis generation is allowed or blocked: <allowed because material supports a discriminating prediction / hypothesis generation is blocked because named material is missing>

### Analysis lenses considered
- Lens: <Success mechanism / Failure dynamics / Lineage-difference / Center-auxiliary inversion / Problem-form transformation / Measurement and evaluation / Constraint relocation / Sparse-information / Cross-domain mechanism transfer>
  - What it would inspect: <process, evidence, or constraint inspected>
  - What it may miss: <blind spot of this lens>
  - Use decision: <primary / auxiliary / not used with reason>

### Adopted analysis lenses
- Primary lens: <exactly one lens>
- Auxiliary lenses: <0-2 lenses, or None with reason>
- Reason: <why these lenses best separate the live explanations>

### Mechanistic analysis
- Observation: <success, failure, limit, constraint, or measurement mismatch>
- Analysis lens used: <primary lens plus auxiliaries when used>
- Mechanistic interpretation: <information flow, gradient flow, search, measurement, representation, constraint, state transition, or decision-coupling explanation>
- Assumptions exposed: <load-bearing assumptions required for this interpretation>
- What would be different if this interpretation is true: <observable contrast>

### Mechanism hypothesis record
- Hypothesis: <cause, condition, and expected change>
- Competing hypothesis: <another mechanism explaining the same observation>
- Discriminating prediction: <how outcomes differ between hypothesis and competing hypothesis>
- Minimal test: <smallest experiment, analysis, counterexample, simplified model, measurement, evaluator, or derivation check>
- Required evidence: <artifact, comparison, measurement, survey evidence, or observation required before plan execution claims advance>
- Decision: <commit / park / kill>
- Reason: <why this decision follows>
```

## Prior-work grounding section

Every plan has first-class prior-work grounding before the Divergence checkpoint and before the Plan section. This is not optional just because no novelty claim is made. The grounding must be bounded but sufficient: enough to support the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations.

Before writing the Plan section, perform a plan-scoped literature survey and record Survey evidence in this section. The survey does not need to be comprehensive unless the plan makes strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims, but it must leave enough evidence for a reviewer to see what was searched, what was selected, what was not found, and whether retrieval was unavailable.

Use `literature/papers.md` for cited prior work and `literature/positioning.md` for how the work stands on prior work. `positioning.md` is where the plan records grounding, inheritance, control/comparator choice when relevant, known limitations, and claim scope. Differences or novelty can be recorded there when claimed, but novelty is not the default purpose.

The Citation-use map is the plan-level bridge between the bibliography and the plan body. It must state how each cited work is used; a citation that has no role in the question, mechanism, baseline, comparator, metric, dataset, evaluation protocol, theoretical foundation, limitation, contradictory evidence, or claim-scope boundary should not be cited.

`Used in plan as` in `literature/papers.md` and `literature/positioning.md` is a project-level role union. The plan-specific source of truth is the plan's Citation-use map, because the same paper can be a baseline in one plan and a mechanism prior, metric, or claim-scope boundary in another.

Retrieval-unavailable is not a survey bypass. The plan may record retrieval as unavailable only with a verifiable signal: attempted source/tool, query or source ID when available, failure evidence such as tool error, access denial, connectivity output, or blocked database access, and explicit claim-scope narrowing. If prior work is genuinely unknown after the plan-scoped literature survey, the plan must record a named constraint and narrow or block relevant claims until the grounding is repaired. Comprehensive literature survey is required for strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims; this is separate from the plan-scoped grounding every plan needs.

```markdown
## Prior-work grounding

### Survey evidence
- Search date: <YYYY-MM-DD, or retrieval-unavailable constraint>
- Queries/sources: <queries, databases, search engines, seed papers, or retrieval-unavailable constraint>
- Selection rationale: <why included papers matter and what near misses were excluded>
- Negative findings: <missing baselines, failed comparator searches, contradictions not found, or None>
- Retrieval-unavailable constraint: <tool/access/connectivity failure and affected grounding or claims; None if survey ran>
- Retrieval-unavailable evidence: <attempted source/tool, query/source id when available, and failure evidence such as tool error, access denial, connectivity output, or blocked database access; None if survey ran>
- Claim-scope narrowing: <claims narrowed or blocked because retrieval was unavailable; None if survey ran>

### Citation-use map
- <literature/papers.md entry>:
  - Used for: <question framing / mechanism prior / baseline / comparator / metric / data / evaluation protocol / theoretical foundation / limitation / contradictory evidence / claim-scope boundary>
  - Plan dependency: <Question / Objective / Hypothesis rationale / Controls / Data setup / Decision threshold / Limitations / Claim scope>
  - How it is used: <specific sentence explaining what the plan borrows, tests, contrasts, or bounds>
  - Claim-scope effect: <supports / narrows / blocks which claims>

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

## Pre-result and post-result boundary

Plan sections record **pre-result commitments**: the research question or objective, mechanism conjecture or principle, prediction or expected observation, primary measure, controls/comparators, planned discriminating test, evidence route, artifact plan, and stop / branch criteria. Do not explain why an unobserved result happened. That is not available before execution.

Result analysis records **post-result explanations** after evidence exists: what happened, candidate explanations for the observed result, evidence for and against those explanations, procedure / artifact explanations, alternatives still live, and discriminating next analyses. Keep these out of the pre-execution Plan and Plan review.

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

Before execution, dispatch a fresh separate-context plan-review subagent with the `research-plan-review` skill. Pass only the plan path as the starting context. The reviewer evaluates research design before any results exist and acts as a stop gate for plans built on a wrong, unsupported, or unverified premise, or on a hypothesis validation method that cannot test the hypothesis.

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
- Premise check: <adequate / revise / block>: <whether the hypothesis rests on a wrong / unsupported / unverified premise, contradicted project state, discredited proxy, or ungrounded prior-work claim>
- Hypothesis validation method: <adequate / revise / block>: <whether the planned validation can test the hypothesis and distinguish it from plausible alternatives>
- Controls, comparators, or limiting cases: <adequate / revise / block / not applicable>: <reason>
- Evidence route and artifact plan: <adequate / revise / block>: <reason>
- Prior-work survey evidence: <adequate / revise / block>: <block if missing, placeholder-only, unsupported by Survey evidence, or unsupported by a verifiable retrieval-unavailable constraint with claim-scope narrowing>
- Scope and constraints: <adequate / revise / block>: <reason>
- Stop decision: <continue / repair_before_execution / stop_execution>: <why the plan may run, must be repaired, or must stop>

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

### Mid-execution literature updates
- <YYYY-MM-DD or None>:
  - Survey trigger: <unfamiliar method / unexpected result / new comparator / contradiction with prior work / missing-baseline signal / other>
  - Sources checked: <queries, papers, databases, or retrieval-unavailable constraint with attempted source/tool and failure evidence>
  - Literature files updated: <literature/papers.md and literature/positioning.md entries, or None with reason>
  - Effect on plan: <none / update limitations / change comparator / change metric / change evaluation protocol / amend plan / open ADJACENT plan>
  - Plan review: <not needed with reason / rerun Plan review before continuing claim-bearing execution>

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

Record the subagent output in the plan after evidence exists. The analysis explains why the result happened; it does not assess readiness, write final claims, choose iteration decisions, or draft reports. It is a post-result explanations section, not a source of pre-result commitments.

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
- **Literature-first hypothesis generation.** If the user asked for research ideas, do not summarize prior work as a substitute for diagnosis. Use the Mechanism hypothesis record section first, then apply Prior-work grounding before finalizing `commit`.
- **Portfolio made of parameter tweaks.** Three thresholds of the same signal are not three approaches. Record them as one primary route with a sweep, then add real alternatives or explicitly narrow the claim scope to the tested route.
- **Prior result treated as fact.** "Previous run was best" is an anchor, not a premise. Record what would revalidate it, what rework is required, or what claim condition remains after Result analysis explains the new outcome.
- **Claim made before prior-work grounding.** If the plan says novel, new method, publishable, to our knowledge, or no baseline exists, cite or update `literature/positioning.md` and point to a comprehensive literature survey before execution. If the claim is not a novelty claim, the plan still needs bounded but sufficient prior-work grounding and must classify itself as replication, baseline strengthening, engineering, or another grounded position.
- **Executing without Plan review.** A plan can be well formatted and still be a bad research design. Before execution, a fresh separate-context plan-review subagent using `research-plan-review` must review the plan path.
- **Closing without Result analysis.** Before Claims, state-changing Decision, or report, a fresh separate-context result-analysis subagent using `research-result-analysis` must explain what happened and why from the plan path and artifacts.
- **Treating result analysis as a decision gate.** Result analysis decomposes explanations; it does not write final claims, assess readiness, or choose the iteration branch.
- **Updating the Plan section after execution.** Plans get amended prospectively via `REFINE`. After-the-fact plan rewriting destroys the time-anchor — git diff will show the rewrite and any reviewer will catch it. Use the Planned vs Actual section instead.
- **Methodology description too thin.** "We ran the experiments" is not a Methodology subsection. State the procedure, the parameters, the protocol.
