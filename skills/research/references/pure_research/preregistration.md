# preregistration.md

Pre-registration is a lightweight, general planning and reporting discipline:
write the plan before work starts, run research or experiments against that
plan, disclose important changes transparently, and give the user a readable
outcome report. It is not an external registry, anti-tamper system, project
classification, or heavy report package for every local probe.

Pure Research-compatible workstreams still clearly separate exploratory
research from confirmatory research. The difference is that the pre-registration
artifact can now describe either path. Every pre-registration declares exactly
one type:

```yaml
preregistration_type: confirmatory | exploratory
```

Use the same filename pattern for both:

```text
prereg/PR_<id>_<slug>.md
```

## When to read

- Planning work that should be compared against a written plan later
- Deciding whether a pre-registration should be confirmatory or exploratory
- Reviewing whether a change from the plan was material
- Preparing a preregistered outcome report

## Purpose

Plan -> execute -> compare -> report:

- Plan: write or select the pre-registration before work starts.
- Execute: run the work against the written plan.
- Compare: compare actual execution and results against the pre-registration.
- Report: publish the plan-to-result table, transparent changes, evidence, and limitations.

Pre-registration is a plan, not a prison. Changes are allowed when they are
disclosed and interpreted honestly. A midstream pre-registration governs future
work or explicit reruns only; prior work is prior or exploratory evidence.
Report contracts apply to report packages and presented evidence, not to
research or experiments. A claim-to-artifact check is a reporting-side
requirement, not a continuous research tracking contract.

Pre-registration states the planned question, scope, data, variables, analysis
or exploration procedure, and interpretation boundary before execution. Before
execution, compare `PR_<id>_<slug>.md` against the current state: prior work,
available data, implementation constraints, analyst/data exposure, and current
question. The comparison is not only to follow the plan; it also checks whether
the current state has broken the plan's assumptions.

After the work, compare actual execution against the pre-registration and
publish material differences in the report's Transparent Changes section.
Changes are not automatic failures. The rule is disclosure: if a change was
made with knowledge of its effect on the outcome, say that the affected result
has weaker diagnostic value. If the original plan no longer answers the
intended question, say so plainly.

The mechanism: HARKing (Hypothesizing After Results are Known) and the garden
of forking paths are reduced when planned and unplanned work are separated.
Without that separation, finding-driven narrative shifts are too easy to
rationalize.

## Shared required content

Both confirmatory and exploratory preregistrations contain these sections:

- Question / objective
- Scope
- Data / input plan
- Variables / measures or inspection targets
- Planned procedure
- Expected outputs
- Decision / follow-up criteria
- Non-claim-bearing condition

The Non-claim-bearing condition states what would prevent outputs from being
used as claim-bearing evidence without a future preregistered rerun or
narrower report claim. Examples include data exposure before the plan was
ready, a plan-breaking scope change, a threshold or interpretation change
after seeing results, missing required evidence, or a procedure that no longer
answers the intended question.

### Study Information

Required fields:

- Title
- Description
- Preregistration type (`confirmatory` or `exploratory`)

Optional fields:

- Authors or responsible agent
- Related prior work
- Notes

### Sampling / Data Plan

Required fields:

- Existing data or data collection status
- Data source or procedure
- Sample size, data range, or planned observation scope
- Inclusion / exclusion rules

Optional fields:

- Sample size rationale
- Stopping rule
- Access constraints

### Variables / Measures

For a confirmatory preregistration, fix the variables used in the planned
analysis:

- Primary outcome / dependent variable
- Predictors / independent variables
- Covariates
- Manipulated or measured variables
- Indices, formulas, units, and aggregation

For an exploratory preregistration, define the variable space:

- Variables or measures to inspect
- Feature families or derived measures
- Allowed transformations
- Out-of-scope variables
- Selection or ranking criteria

## Confirmatory preregistration

Use a confirmatory preregistration when an exploratory result,
literature-derived prediction, or explicit research question is ready for a
reliability-raising test.

Required sections:

1. Study Information
2. Hypotheses
3. Design Plan
4. Sampling / Data Plan
5. Variables / Measures
6. Analysis Plan
7. Inference / Decision Criteria
8. Data Exclusion / Missing Data Handling
9. Transparent Changes Policy

Optional sections:

- Randomization
- Blinding
- Sample Size Rationale
- Stopping Rule
- Secondary Analyses
- Other Notes

The Analysis Plan must be specific enough for a reviewer to tell whether the
reported analysis followed the plan. If multiple tests or model variants are
planned, state how they will be interpreted together before execution.

### Confirmation target and initial approach

Confirmatory plans separate **purpose, question to resolve, and initial
approach**:

- **confirmation target**: the question, hypotheses or competing explanations,
  scope, primary metric, thresholds, and interpretation rules that determine
  what the work can claim.
- **initial approach**: the planned analysis method, estimator, data-acquisition
  route, implementation path, and operational choices used to answer the
  confirmation target.

The initial approach is not the confirmation target itself. Evidence, data
availability, or implementation constraints may justify changing the initial
approach, as long as the change does not alter the confirmation target,
threshold, scope, or interpretation. Such changes must be documented in
Transparent Changes, but they are not automatically hypothesis failure,
plan-breaking material changes, or grounds for a new PR. A new PR is not
required when the confirmation target is preserved.

Threshold miss is result interpretation, not a plan-breaking material change:
if the observed value misses the pre-registered threshold, do not relabel that
miss as a plan change or create a new PR merely to rescue the result. Interpret it under the
pre-registered rules. A new PR is needed only for future work with a changed
confirmation target, threshold, scope, or interpretation.

## Exploratory preregistration

Use an exploratory preregistration when the work is allowed to inspect,
diagnose, rank, narrow, or generate candidate explanations while still needing
a prior scope and transparent report. Exploratory research does not have to be
followed by confirmatory research. It may end with a diagnostic map, candidate
explanations, a ranked pattern list, failure analysis, a narrowed question, or
a future confirmatory plan.

Required sections:

1. Study Information
2. Exploratory Objective
3. Exploration Scope
4. Sampling / Data Plan
5. Variables / Measures
6. Allowed Transformations / Procedures
7. Selection or Follow-Up Criteria
8. Expected Outputs
9. Transparent Changes Policy

Optional sections:

- Hypotheses or Expectations
- Constraints / Risks
- Trigger for Future Confirmatory Preregistration
- Other Notes

Expected Outputs is not a reporting plan. It states the kind of artifact the
exploration is expected to produce, such as a diagnostic map, candidate
explanations, ranked patterns, failure analysis, narrowed question, or future
confirmatory plan.

## Transparent Changes Policy

Every preregistered outcome report includes `Transparent Changes`.

If no material changes occurred:

```markdown
No material changes from the preregistration.
```

If material changes occurred, list each one:

```markdown
### Change <n>: <short name>
- Description of change:
- Rationale:
- Effect on study results or conclusions:
```

Effects should be honest about uncertainty. If a change was made with knowledge
of its effect on the outcome, the report must say that the affected result has
weaker diagnostic value. If the change means the original plan no longer
answers the intended question, the report says so plainly.

## Outcome report package

All preregistered or claim-bearing work that produces a formal report package
uses the same package shape. Required core files and directories:

```text
results/reports/
  RPT_<id>_<slug>/
    report.md
    report.html
    figures/
    tables/
    attachments/
```

Required core directories may be empty when the report has no figures, tables,
or attachments.

Optional / situation-specific files:

```text
results/reports/
  RPT_<id>_<slug>/
    report.pdf
    provenance/
      manifest.json
      integrity_checks.md
      rerun.md
```

`report.html` is the primary readable artifact for L2/L3 reports. `report.md`
is editable source. `report.pdf` is optional snapshot/export. Use
provenance/ for claim-bearing or L2/L3 reports. L2/L3 reports means
claim-bearing reports and state-promotion or terminal-decision report
packages; it is report package level, not analysis tier. In provenance/,
include `manifest.json`, `integrity_checks.md`, and `rerun.md`. Figures and
tables in the readable report should have source files under `figures/` or
`tables/`. Large source data and intermediate artifacts should not be copied
unless they are small and necessary. Local paths may appear in `report.md` or
a provenance appendix, but should not dominate the report. External tracker
run IDs are optional and appear only if a tracker was actually used.

Required report sections:

1. Executive Decision
2. Research Stage and Claim Boundary
3. Preregistration Reference
4. Plan-to-Result Table
5. Key Evidence
6. Evidence Integrity Checks
7. Transparent Changes
8. Reproducibility Capsule
9. Scope / Limitations / Alternative Explanations
10. Next Action

Confirmatory reports emphasize hypotheses, decision criteria, and completion
of the planned analysis. Exploratory reports emphasize scope, patterns,
diagnostics, and follow-up. The Plan-to-Result Table maps:

```text
planned_item | executed_as_planned | result_summary | evidence | notes
```

Evidence should point to a figure, table, appendix, or local source artifact.
It does not require a tracker run ID.

The PDF may include a short provenance appendix:

```text
Preregistration: prereg/PR_<id>_<slug>.md
Report source: results/reports/RPT_<id>_<slug>/report.md
Figures: results/reports/RPT_<id>_<slug>/figures/
Tables: results/reports/RPT_<id>_<slug>/tables/
Source data or artifact: <path or citation>
External tracker run ID: <omit unless a tracker was actually used>
```

## HARKing and goalpost discipline

Pre-registration is a transparency mechanism, not a promise that nothing will
change. The following patterns remain prohibited:

- **Post-hoc pre-registration**: writing a pre-registration after the work has
  run and claiming it was the plan all along. Treat that work as exploratory
  unless rerun under a valid plan.
- **Selective reporting**: running multiple secondary checks and reporting only
  the favorable subset.
- **Goalpost shift**: changing thresholds, scope, or interpretation after
  seeing results.
- **Hidden material change**: changing data, variables, procedures, or decision
  criteria without disclosing the description, rationale, and effect on study
  results or conclusions.

Changing thresholds after seeing results is plan-breaking. An initial-approach
change that preserves the confirmation target, threshold, scope, and
interpretation is not a plan-breaking material change. The policy requires
transparent changes, not automatic invalidation.

## Relationship to other references

- Workflow comparison and state-change rules:
  `references/pure_research/pr_workflow.md`
- Outcome report details and template:
  `references/shared/outcome_reports.md` and
  `assets/shared/outcome_report.md.template`
- PR/FAQ entry: `references/pure_research/prfaq.md`
- Promotion gate:
  `references/pure_research/pr_promotion_gate.md`
