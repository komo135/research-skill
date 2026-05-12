# research-skill

A Claude Code and Codex plugin for agent-driven serious research and R&D.
It ships two public skills in one plugin:

- `research` - the generic base skill for disciplined, workstream-aware
  research across Capability / Technology Research (R&D-compatible) and
  Phenomenon / Mechanism Research (Pure Research-compatible), stage gates,
  result analysis, lightweight experiment tracking,
  reproducibility for claim-cited results, process review, and conclusion
  review.
- `quant-research` - a quantitative-finance adapter layered on top of
  `research` for financial machine learning, backtests, time-series validation,
  leakage checks, Sharpe/DSR review, transaction costs, and portfolio-oriented
  evidence.

The core rule is: prefer a precise unresolved state over a shallow conclusion.
Results create questions; questions drive analysis or further experiments; only
evidence that survives the relevant gate should change project state.

## Who this is for

Use this plugin when the work is more than ordinary fact lookup or ordinary
implementation:

- Capability / Technology Research work that establishes or improves a
  technical capability while explaining success conditions, failure
  conditions, and design alternatives.
- Phenomenon / Mechanism Research work that resolves a phenomenon,
  explanation, boundary condition, or claim.
- Quantitative-finance research where conclusions must survive replication,
  leakage checks, validation-design review, and cost-aware interpretation.

It is not a backtest engine, experiment tracker, or notebook framework. It is a
protocol layer that helps an agent decide what evidence is needed, what state
can change, and when a result is still only exploratory. Ordinary exploration
can be tracked with a short run note, tracker run, notebook note, or results
row; promotion-eligible, externally shared, or claim-cited results need
evidence citations and rerun guidance.

## Research Structure

The generic `research` skill separates the work into durable layers:

- Protocol layer: reusable rules, schemas, gates, review requirements, and
  promotion criteria.
- Project layer: final intent, decision context, current uncertainties,
  workstream list, cross-workstream dependencies, and durable decisions.
- Workstream layer: the local unit that selects a state object and gate.
- Project instance layer: concrete data, candidates, parameters, code, trial
  notebooks, generated reports, and local implementation decisions.
- Evidence artifacts: notebooks, result rows, tracker runs, lightweight run
  notes, figures, and claim-cited result records.
- State ledgers: capability maps, explanation ledgers, decision logs, and
  promotion records that cite evidence artifacts.

A project can contain multiple workstreams. The project itself is not Pure
Research or R&D; those names remain compatibility labels for workstream types.
Project decision gates cite child workstream gate results and do not re-score
TRL, support status, or A-tier. Optional R&D Program files coordinate multiple
projects or major workstreams but do not own truth, TRL, promotion, or claim
status.

## Repository Layout

```text
research-skill/
├── .agents/plugins/
│   └── marketplace.json
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── research/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   └── assets/
│   └── quant-research/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── README.md
└── LICENSE
```

The repository root is the plugin root for both Claude Code and Codex. The
Codex marketplace entry points to `"path": "."`, so `skills/` is the single
source of truth for distributed skills.

## Installation

### Claude Code: from a Git repository

```text
/plugin marketplace add https://github.com/komo135/research-skill
/plugin install research@research-skill
```

After installation the skills are available as `research` and `quant-research`.

### Claude Code: local development

```bash
claude --plugin-dir /path/to/research-skill
```

### Codex: from GitHub

```bash
codex plugin marketplace add https://github.com/komo135/research-skill
```

Enable the installed plugin in `~/.codex/config.toml`:

```toml
[plugins."research@research-skill"]
enabled = true
```

The installed Codex skills are exposed as `research` and `quant-research`.

## Usage Flow

1. Choose `research` for generic serious research or R&D. Choose
   `quant-research` only when the domain is financial ML, backtesting,
   time-series validation, portfolio research, or trading-system evidence.
2. Map the current research state: project intent, current uncertainties, the
   first workstream, its state object, and its gate.
3. Write the entry document before expensive claim-bearing work: reviewed
   charter and kill criteria for a capability workstream, or PR/FAQ plus
   pre-registration when a phenomenon workstream enters confirmatory research.
4. Run the smallest evidence-producing artifact that can answer the current
   workstream question.
5. Analyze the result before adding variants. A result should update a question,
   split an explanation, recycle a capability, add a dependent workstream, or
   justify a gate decision.
6. Promote only when the relevant process review and conclusion review axes
   pass for the load-bearing claim. Claim-bearing notebooks use the folded
   experiment review references inside `research/references/review/`.

## Bundled Helpers

Generic helpers live under `skills/research/scripts/`:

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_trial.py` | Generate a numbered evidence artifact notebook |
| `aggregate_results.py` | Validate and append queryable evidence records |
| `draft_imrad.py` | Draft a manuscript-shaped research summary |
| `lit_fetch.py` | Fetch literature metadata into local research notes |

Finance adapters live under `skills/quant-research/scripts/`:

| script | purpose |
|---|---|
| `walk_forward.py` | Compute Sharpe distribution over rolling windows |
| `bootstrap_sharpe.py` | Block-bootstrap CI for per-trade Sharpe |
| `psr_dsr.py` | Probabilistic / Deflated Sharpe Ratio |
| `fee_sensitivity.py` | Fee sweep with break-even fee extraction |
| `sensitivity_grid.py` | 2D threshold sensitivity grid |
| `vol_targeted_size.py` | Position sizing with size proportional to inverse volatility |
| `purged_kfold.py` | Purged k-fold CV for time-series validation |
| `leakage_check.py` | Detect look-ahead bias and target leakage in features |
| `sanity_checks.py` | Programmatic finance-domain implementation checks |

## Migration from v1.0.x

The old plugin identity was `quant-research@quant-research-skill`. Starting in
v1.1.0, install `research@research-skill`. The old standalone
`experiment-review` skill is folded into the `research` review references.

## Status

Version 1.1.7 - keeps A4 rigor for load-bearing claims while allowing faster
exploratory go / no-go, park, deprioritize, and reject-for-now decisions.

<details>
<summary>Changelog</summary>

### v1.1.7 (current)

- Reserved A4+ for supported, matured, established, promoted, external-claim,
  deployment-recommendation, and terminal-kill decisions.
- Made A2-A3 sufficient for exploratory next-step, provisional go / no-go,
  park, deprioritize, and reject-for-now decisions that do not create a
  load-bearing claim.
- Scoped quant-research finance checks to claim-bearing and promotion-relevant
  decisions instead of making them blanket gates for exploratory work.

### v1.1.6

- Softened Capability / Technology Research entry guardrails: do not classify
  the whole project as that workstream, and do not ban non-load-bearing
  scaffold, interface probes, smoke tests, environment setup, or data plumbing.
- Kept the hard gate where it matters: promotion-relevant or claim-bearing
  implementation must wait until charter and kill criteria exist.
- Added regression coverage for the mixed-system pressure scenario that
  previously pushed agents toward overclassification and blanket
  implementation bans.

### v1.1.5

- Made the research entry workstream-aware: projects can contain multiple
  workstreams, while R&D and Pure Research remain compatibility labels for
  local state objects and gates.
- Added mixed project scaffolding and workstream-targeted trial generation;
  `--mode` now creates an initial workstream inside the mixed container rather
  than classifying the whole project.
- Limited implemented workstream labels to Capability / Technology Research
  and Phenomenon / Mechanism Research; evaluation, design, exploration, and
  engineering support remain activities inside a selected workstream.
- Added regression coverage so ignored `docs/superpowers/specs` files are not
  packaged as plugin artifacts.

### v1.1.4
- Clarified that Pure Research has separate exploratory and confirmatory
  workflows.
- Clarified that pre-registration is a confirmatory-research tool, not a
  hypothesis freeze or an automatic approach-failure trigger.
- Added per-file regression coverage for English-only Pure Research
  pre-registration docs/templates and `PR_<id>` vs current-state comparison.

### v1.1.3

- Removed registration-proof mechanisms: no hashes, frozen records, dated note
  references, registration logs, or history/timestamp comparisons for proving
  planning order.
- Kept the useful parts: reviewed planning documents, material deviation notes,
  and rerun guidance for promotion-eligible or claim-cited results.
- Added regression coverage to block reintroducing proof-artifact language.

### v1.1.2

- Relaxed tracking requirements: ordinary exploration may use
  lightweight run notes, tracker runs, notebook notes, or results rows.
- Limited strong evidence citations, rerun guidance, and decision-relevant run
  sets to promotion-eligible, externally shared, or claim-cited results.
- Changed process and conclusion review from full mandatory inventories to
  targeted lightweight review of load-bearing axes.

### v1.1.1

- Required user-facing outcome reports to include a plain-language decision,
  intuitive visual or tabular evidence, citations, scope/caveats, and next
  action.
- Added finance-specific report evidence examples such as equity/drawdown
  curves, fee sensitivity, regime performance, and deployment diagnostics.

### v1.1.0

- Renamed the project and plugin identity from the old quant-only package to
  `research-skill` / `research`.
- Added `skills/research` as the generic serious-research and R&D base skill.
- Reworked `skills/quant-research` into a finance adapter on top of
  `research`.
- Folded the old standalone `experiment-review` skill into
  `skills/research/references/review/`.

### v1.0.7

- Added an optional R&D Program coordination layer for portfolios that combine
  R&D capability establishment with Pure Research child projects.
- Added shared Result-to-Question and Result-to-Capability loops.
- Added right-sized rigor guidance and Program Map boundaries.

### v1.0.6

- Added selectable tracking backends.
- Required complete run inventory/export for external trackers.
  Superseded in v1.1.2 by decision-relevant run sets instead of complete
  inventory for every project.
- Kept local notes/parquet compatibility for existing projects.

### v1.0.5

- Decoupled evidence artifacts from research contracts.
- Standardized queryable evidence records across R&D and Pure Research.
- Removed capability or pre-registration requirements from neutral trial
  artifact creation.

### v1.0.4

- Relaxed kill and reproducibility gates so terminal claims require concrete
  evidence without overclaiming machine-verifiable reproducibility.

### v1.0.3

- Added the protocol-layer / project-instance-layer boundary contract.
- Added project-instance `configs/`, `src/`, and `tests/` areas.
- Made R&D and Pure Research trial notebooks neutral evidence artifacts.

### v1.0.2

- Made the repository root the Codex plugin root.
- Removed the stale duplicate plugin distribution copy.

### v1.0.0

- Rebuilt the protocol around R&D and Pure Research disciplines, A0-A5 analysis
  depth, reproducibility notes, and two-axis review.

</details>

## License

MIT. See [LICENSE](./LICENSE).
