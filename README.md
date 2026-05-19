# research-skill

A Claude Code and Codex plugin providing four skills for **agent-driven R&D**:

- **`research`** — proposition-first protocol for R&D work across Frascati categories. It manages observations, analyses, Generated doubt, Working proposition, Expected consequence, Proposition status, Derived hypothesis, hypothesis plans, claims, decisions, and reports.
- **`research-plan-review`** — independent pre-execution review. It starts from a hypothesis plan path only and checks premise, proposition trace, validation method, plan visual, prior-work grounding, and blockers.
- **`research-result-analysis`** — independent post-execution analysis. It starts from a hypothesis plan path only, reconstructs evidence, explains what happened and why, and returns state-update inputs without writing final claims or decisions.
- **`quant-research`** — domain extension layered on `research` for time-series and statistically rigorous quantitative R&D.

The core rule: **research-level reproducibility is enforced; experiment-level replicability is the agent's discretion.** Reports record material conditions, not environment locks: data identity, split dates, evaluation protocol, major model/tool versions, hardware class, external API/model version, collection date, formal assumptions, and seed variability when they affect interpretation. Research scripts still need evidence: print-only output is incomplete and stdout is not evidence, so completed runs keep a manifest with `status: completed`, logs, and at least one manifest-listed durable artifact. Claim-to-artifact consistency checks are evidence-integrity checks rather than a replacement for methods reproducibility; experiment-level replicability infrastructure is not skill-enforced. Provenance or variability logs are useful but not substitutes for methods reproducibility.

## Core design

### Proposition-first lifecycle

```text
Situation question
→ observation / analysis
→ proposition P
→ expected observation E if P is true
→ compare observed O with E
→ decide whether P is contradicted or whether P's required condition is unrealized
→ if P remains live, derive hypothesis H that preserves, revises, splits from, or realizes a condition of P
→ predict what should happen if H is true
→ Hypothesis plan
→ Plan review
→ Execution
→ Result analysis
→ hypothesis status update
→ proposition status update
```

Question generation is not free-form ideation. It starts from material and a contrast:

- `expectation-break`
- `constraint-joint-fit`
- `required-component-doubt`
- `trace-meaning`
- `static-to-process`
- `analogy-transfer`
- `search-or-evaluation-bottleneck`
- `representation-change`

Each analysis records the Generated doubt, Working proposition, Expected consequence, observed match/break/missing condition, Proposition status, and only then a Derived hypothesis candidate. Material absence means no proposition or hypothesis: collect observations, measurements, constraints, comparators, traces, prior-work facts, theoretical tensions, or bottleneck evidence first.

The material-acquisition task should name the missing observation, comparator or expected reference, measurement or evidence form, minimal reproduction or trace, and next artifact to collect.

A contradicted proposition is not a plannable parent: record the contradiction, revise, split, or close the proposition, then derive the next hypothesis under the updated proposition.

Hypothesis candidates are typed; a derived hypothesis may be predictive / performance, mechanistic, causal / intervention, descriptive / characterization, theoretical, or mixed.

### Proposition status

Propositions are not claims. They are long-lived research state.

Statuses:

- `open`
- `supported`
- `contradicted`
- `unrealized-condition`
- `under-specified`
- `split-needed`
- `split`
- `closed`

Derived hypotheses use:

- `candidate`
- `ready-for-plan`
- `tested-supported`
- `tested-contradicted`
- `tested-partial`
- `tested-inconclusive`
- `parked`
- `killed`

## Project layout the skill produces

When an agent runs `scripts/new_project.py`:

```text
{project-root}/
├── README.md
├── project_state.md
├── decisions.md                         # project-wide decisions only
└── propositions/
    └── P001_slug/
        ├── proposition.md
        ├── observations.md
        ├── analyses.md
        ├── decisions.md                 # proposition decisions
        └── hypotheses/
            └── H001_slug/
                ├── hypothesis.md
                ├── plan.md              # hypothesis plan
                ├── experiments/
                │   ├── code/
                │   ├── configs/
                │   ├── notebooks/
                │   └── runs/
                ├── reports/
                └── decisions.md         # hypothesis decisions
```

`lib/`, `data/`, and `literature/` may exist when the project needs shared code, data, or project-level prior-work state, but the research lifecycle is organized by propositions and derived hypotheses.

## Bundled scripts

`skills/research/scripts/`:

| script | purpose |
|---|---|
| `new_project.py` | Initialize proposition-first project structure |
| `new_proposition.py` | Create `propositions/Pxxx_slug/` with proposition, observations, analyses, decisions, and hypotheses directory |
| `new_hypothesis.py` | Create `hypotheses/Hxxx_slug/` with hypothesis ledger, hypothesis plan, experiments, reports, and decisions |
| `new_run.py` | Create durable run evidence scaffold under a derived hypothesis |
| `check_run_artifacts.py` | Reject print-only runs and verify manifest/logs/non-log artifacts |
| `check_mechanism_hypothesis_record.py` | Legacy checker for older mechanism-record plans; current flow uses proposition analyses and hypothesis ledgers |
| `check_claims.py` | Verify claim record structure |
| `check_report.py` | Verify report contract |
| `draft_report.py` | Initialize a report under a derived hypothesis |

There is no standalone `new_plan.py`; top-level plans are the old lifecycle.

## Hypothesis plan

`propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md` contains:

- Proposition and hypothesis trace
- Prior-work grounding
- Divergence checkpoint
- Plan visual for architecture, data/evaluation flow, mechanism, system boundary, decision flow, or derivation structure
- Method and evidence route
- Plan review
- Actual execution
- Planned vs Actual
- Result analysis
- Claims
- Result feedback

The trace must include Situation question context, Generated doubt, Working proposition, Expected consequence, Proposition status, Derived hypothesis, and Hypothesis plan link. The plan may summarize proposition history but must not rewrite it.

Prior-work grounding uses `literature/{papers.md,positioning.md}` when project-level prior-work state is useful.

Mid-execution literature update: if an unfamiliar method, unexpected result, new comparator, contradiction with prior work, or missing-baseline signal appears, record the update before claim-bearing execution continues.

## Review and result gates

Before execution, `research-plan-review` checks wrong, unsupported, or unverified premise risk, the hypothesis validation method, and whether the plan actually tests the derived hypothesis produced by source analysis or drifted into a convenient different question. Broken premise or invalid validation method returns `block_execution`.

After execution, `research-result-analysis` explains what happened and why from the plan path and artifacts. It does not choose proposition decisions. The parent agent then updates:

1. `hypothesis.md`
2. hypothesis `decisions.md`
3. parent `proposition.md`
4. proposition `decisions.md`

## Reports

Reports are paper-grade standalone evidence artifacts under each derived hypothesis. They include Related Work, Theory / Formulation, Methods & Conditions, Results or Observations, Ablation / Sensitivity, Discussion, Limitations, and References. Sections that do not apply still appear with `Not applicable:` and a reason.

## Installation

### Claude Code

```text
/plugin marketplace add https://github.com/komo135/research-skill
/plugin install research@research-skill
```

### Codex

```bash
codex plugin marketplace add https://github.com/komo135/research-skill
```

Enable in `~/.codex/config.toml`:

```toml
[plugins."research@research-skill"]
enabled = true
```

## License

MIT. See [LICENSE](./LICENSE).
