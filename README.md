# research-skill

A Claude Code and Codex plugin for agent-driven serious research and R&D.
It ships two public skills in one plugin:

- `research` - the generic base skill for disciplined R&D, Pure Research,
  stage gates, result analysis, reproducibility, process review, and conclusion
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

- R&D work that establishes or improves a technical capability.
- Pure Research work that resolves a phenomenon, explanation, or claim.
- Quantitative-finance research where conclusions must survive replication,
  leakage checks, validation-design review, and cost-aware interpretation.

It is not a backtest engine, experiment tracker, or notebook framework. It is a
protocol layer that helps an agent decide what evidence is needed, what state
can change, and when a result is still only exploratory.

## Research Structure

The generic `research` skill separates the work into durable layers:

- Protocol layer: reusable rules, schemas, gates, review requirements, and
  promotion criteria.
- Project instance layer: concrete data, candidates, parameters, code, trial
  notebooks, generated reports, and local decisions.
- Evidence artifacts: notebooks, result rows, run exports, figures, and stamps.
- State ledgers: capability maps, explanation ledgers, decision logs, and
  promotion records that cite evidence artifacts.

R&D mode focuses on establishing a capability. Pure Research mode focuses on
resolving a question or explanation. Optional R&D Program files coordinate
multiple child projects but do not own truth, TRL, promotion, or claim status.

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

1. Choose `research` for generic R&D or Pure Research. Choose
   `quant-research` only when the domain is financial ML, backtesting,
   time-series validation, portfolio research, or trading-system evidence.
2. Freeze the entry document before expensive work: an R&D charter for
   capability establishment, or PR/FAQ plus pre-registration for Pure Research.
3. Run the smallest evidence-producing artifact that can answer the current
   question.
4. Analyze the result before adding variants. A result should update a question,
   split an explanation, recycle a capability, or justify a gate decision.
5. Promote only when process review and conclusion review both pass. Claim-
   bearing notebooks use the folded experiment review references inside
   `research/references/review/`.

## Bundled Helpers

Generic helpers live under `skills/research/scripts/`:

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_trial.py` | Generate a numbered evidence artifact notebook |
| `aggregate_results.py` | Validate and append queryable evidence records |
| `reproducibility_stamp.py` | Emit a JSON stamp for promotion-eligible or claim-cited trials |
| `prereg_freeze.py` / `prereg_diff.py` | Freeze and compare pre-registration documents |
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

Version 1.1.0 - project renamed to `research-skill`, plugin identity renamed to
`research`, and the public skills split into generic `research` plus the
`quant-research` finance adapter.

<details>
<summary>Changelog</summary>

### v1.1.0 (current)

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

- Added selectable tracking and audit backends.
- Required complete run inventory/export for external trackers.
- Kept local stamp/parquet compatibility for existing projects.

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
  depth, reproducibility stamps, and two-axis review.

</details>

## License

MIT. See [LICENSE](./LICENSE).
