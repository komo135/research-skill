---
name: research
description: Use when conducting R&D work that needs proposition state, claim discipline, planning structure, scoping literature, EDA, research papers, or maintained research state. Triggers when starting from an intent, generating hypotheses, planning experiments, designing baselines, writing findings, deciding what to do after a result, characterizing a phenomenon, building a prototype, or maintaining research state across sessions.
---

# Research

Agent workflow for proposition-first R&D. The top-level research unit is a **proposition**, not a standalone plan. A plan tests one derived hypothesis under one live proposition. `creating-propositions` owns proposition generation and proposition state files; this skill orchestrates intake, scoping, material/EDA, hypothesis lifecycle, evidence, claims, papers, and project decisions.

## Start From Intent

Research starts with an intent, not with a proposition.

```text
intent
-> intake.md
-> uncertain-in-outcome gate
-> scoping literature
-> material acquisition / EDA
-> root observations.md
-> inline creating-propositions
-> proposition workspace
-> derived hypothesis
-> plan review
-> execution evidence
-> result analysis
-> state updates
-> proposition-level paper
-> next-cycle scoping and observations
```

At intake, ask whether the outcome is uncertain. If the user only wants a known method implemented exactly as described, route it as implementation work and do not open a proposition or hypothesis lifecycle. If the user reframes toward an uncertain question, re-enter the workflow.

Material absence is not a dead end and not permission to invent. If there is no observation, failure, success case, constraint, measurement, comparator, repeated trace, prior-work fact, theoretical tension, or search/evaluation bottleneck, create a material-acquisition task that names the missing material and next artifact to collect.

## Project Layout

`references/project_layout.md` is the layout source of truth. Generated projects use:

```text
project-root/
├── intake.md
├── literature/
│   ├── scoping.md
│   ├── papers.md
│   └── positioning.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── eda/
├── observations.md
├── project_state.md
├── decisions.md
├── lib/{data,eval,viz,utils,tests}/
└── propositions/
    └── P001_slug/
        ├── proposition.md
        ├── observations.md
        ├── analyses.md
        ├── decisions.md
        ├── paper.md
        └── hypotheses/
            └── H001_slug/
                ├── hypothesis.md
                ├── plan.md
                ├── experiments/{code,configs,notebooks,runs}/
                └── decisions.md
```

Old top-level `plans/`, top-level `experiments/<id>/runs/`, `literature/differentiation.md`, and per-hypothesis `reports/` are not compatibility paths. Reject them except in explicit old-path rejection tests.

## Ownership

Use file ownership to avoid responsibility drift:

| Path | Owner discipline |
|---|---|
| `intake.md`, root `observations.md`, `literature/{scoping,papers,positioning}.md`, `data/{raw,processed,eda}/`, `project_state.md` | research |
| root `decisions.md` | research, project-level decisions only |
| `propositions/Pxxx/{proposition,observations,analyses,decisions}.md` | `creating-propositions` |
| `propositions/Pxxx/paper.md` | research |
| `propositions/Pxxx/hypotheses/Hxxx/*` | research |

Invoke `creating-propositions` inline in the same context after scoping/EDA material is available. Do not dispatch a fresh separate-context subagent for proposition generation; the material continuity matters more than independence. Use fresh separate-context agents only for adversarial `research-plan-review` and `research-result-analysis`.

## Proposition State Gate

Plan-ready proposition states are exactly `open`, `supported`, and `unrealized-condition`.

All states are:

`open`, `supported`, `unrealized-condition`, `under-specified`, `contradicted`, `split-needed`, `split`, `parked`, `closed`.

Blocked states route work:

- `under-specified`: acquire material or revise until a discriminating expected consequence exists.
- `contradicted`: record the contradiction, then revise, split, or close before planning.
- `split-needed`: split before planning.
- `split`: continue through child propositions.
- `parked`: satisfy the unblock condition before planning.
- `closed`: do not plan unless reopened with a recorded reason.

`closed -> open` is allowed only with a `REOPEN` entry in proposition `decisions.md` naming the new material or reconsideration basis. `parked -> previous live state` requires `UNPARK` and evidence that the unblock condition is satisfied.

## Decision Ledgers

Decision location is part of the protocol:

- Project `decisions.md`: `OPEN_PROPOSITION`, `SPLIT_PROPOSITION`, `MERGE_PROPOSITION`, `CHANGE_SCOPE`, `CHANGE_PROTOCOL`.
- Proposition `decisions.md`: `SUPPORT`, `CONTRADICT`, `UNREALIZED_CONDITION`, `UNDER_SPECIFY`, `SPLIT_NEEDED`, `PARK`, `UNPARK`, `REVISE`, `CLOSE`, `REOPEN`.
- Hypothesis `decisions.md`: `COMMIT`, `PARK`, `KILL`, `TESTED_SUPPORTED`, `TESTED_CONTRADICTED`, `TESTED_PARTIAL`, `TESTED_INCONCLUSIVE`, `REVISE`.

Scope changes and proposition state transitions may happen in one session, but record them in separate ledgers.

## Literature Layers

Scoping literature and hypothesis-specific grounding are non-substitutable.

- `literature/scoping.md`: before proposition creation, identify existing work, comparators, datasets, known failures, and whether the intent is already solved.
- Plan-scoped Prior-work grounding: before claim-bearing execution, ground the specific hypothesis, method, baseline, metric, and validation route. Include Survey evidence and Citation-use map even when scoping exists.

If scoping finds prior work that breaks the intended novelty claim, stop the novelty framing. Narrow, revise, replicate, or choose an honest boundary before planning.

## Hypothesis Lifecycle

Use `scripts/new_hypothesis.py` only after the parent proposition is plan-ready and the source analysis has a non-placeholder derived hypothesis candidate. The plan lives at `propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md`.

Every plan tests exactly one derived hypothesis and starts its Plan section with `### Plan visual` using Mermaid, PlantUML, ASCII, linked figure/table, or `No diagram:` with a reason. Plans contain pre-result commitments: proposition trace, hypothesis type, prediction, competitor, discriminator, primary measure, controls/comparators or limiting-case checks, evidence route, artifacts, material conditions, and stop/status criteria.

Every Plan section starts with `### Plan visual`. Do not require every derived hypothesis to be mechanistic. Hypothesis type may be `predictive / performance`, `mechanistic`, `causal / intervention`, `descriptive / characterization`, `theoretical`, or `mixed`.

Before execution, dispatch `research-plan-review` with only the plan path. After execution and Planned vs Actual, dispatch `research-result-analysis` with only the plan path. Result analysis explains why the observed result happened; it does not write final claims, state-update inputs, or decisions.

After result analysis, the parent agent updates:

1. `hypothesis.md`.
2. hypothesis `decisions.md`.
3. parent proposition state files via `creating-propositions` discipline.
4. proposition `decisions.md` when state changes.
5. project state.

## Evidence And Claims

Print-only output is not evidence. A completed run needs `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, and at least one manifest-listed durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`. Run `scripts/check_run_artifacts.py` before using a run as evidence.

Claims are evidence records, not proposition statuses:

```yaml
- claim: <one sentence with specific assertion>
  evidence: <file:line / numeric value / artifact path / citation>
  alternatives_not_excluded: [...]
  conditions_tested: <variable ranges, datasets, parameters>
  conditions_not_tested: [...]
```

Strength is read from alternatives and tested conditions. Empty lists claim exhaustion and are open to audit. Run `scripts/check_claims.py` before state-changing decisions or paper prose depends on the claim.

## Research Papers

Create `propositions/Pxxx_slug/paper.md` when a proposition reaches `supported` or `contradicted`. Do not postpone the paper because per-hypothesis notes exist, because the project may continue, or because a future summary seems easier. The resolution transition is the publication trigger.

The paper synthesizes across the proposition's hypotheses and must pass `scripts/check_paper.py`. Required paper-grade structure includes Related Work, Theory / Formulation, Methods & Conditions or System description, Results/Observations/Performance, Ablation / Sensitivity, Claim-to-result alignment, Discussion, Limitations, Reproducibility, and References. Numeric evidence needs sample size plus variance/dispersion, CI, effect size, significance, or an explicit non-applicability reason.

In the next cycle, treat the paper as material. Re-survey literature and extract observations from your own paper; own research is part of the Bit source for later propositions, not just external prior work.

## Capability Guard

This protocol should improve reasoning, not create paperwork. Keep labels subordinate to the actual contrast, expected consequence, discriminator, evidence, and decision. Do not turn EDA into a claim, do not inflate incremental results, and do not create hypotheses from absent material.
