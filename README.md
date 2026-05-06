# quant-research-skill

A Claude Code and Codex plugin for **agent-driven quantitative finance
research**. The `quant-research` skill now starts by choosing one of two modes:

- **R&D / technology establishment** — for establishing a technical capability.
  The skill decomposes the target technology into small capabilities, assigns a
  maturity level, and assesses capability progress by citing neutral evidence
  artifacts from trials and results.
- **Pure Research** — for paper-like research and phenomenon understanding.
  The skill prioritizes prior-work review, competing explanations, failed-trial
  analysis, and research-state updates over fast conclusions.

The core rule is: **prefer a precise unresolved state over a shallow
conclusion**. Hypothesis quality management is intentionally lighter and more
stateful than the previous protocol. Evidence artifacts can be complete without
moving research state; ledgers decide whether an artifact supports a transition.

The separate `experiment-review` skill remains available for promotion moments:
declaring a claim `supported`, external sharing, deployment recommendation,
closing a research line, or making a major direction decision.

The skills cover both **mathematical-model research** (Ornstein–Uhlenbeck,
state-space, PCA, factor models, regression) and **machine-learning research**
(classical ML, deep learning, reinforcement learning, foundation models like
Chronos / TimesFM / Moirai) — the lifecycle and the review layers are the same;
only the modeling step differs.

> Writing a paper is not the goal of this plugin. Producing research that
> *could* be written up as a paper is.

## Who this is for

You, if all of the following are true:

- You drive a research workflow with Claude Code (or another Claude Agent SDK
  harness) rather than typing every cell yourself.
- You work on alpha factors, return prediction, regime detection, optimal
  execution, or any data → model → evaluation loop on financial time series.
- You have been burned by — or want to never be burned by — leakage,
  whole-period normalization, single-instrument generalization claims,
  test-set reuse, missing baselines, or unverified Sharpe.
- You are willing to use **marimo** as the notebook format. (See below for why.)

This plugin is **not** for:

- Pure implementation tasks (CRUD, refactors, bug fixes that have nothing to
  do with research).
- Notebook stages that have no claim to review yet (orientation, brainstorm).
  The review skill explicitly opts out at that stage.
- Projects that need a working backtest *engine* — this plugin is a research
  protocol, not a backtest engine. Pair it with whatever engine you prefer
  (your own pandas / numpy code, vectorbt, NautilusTrader, etc.).

## Why marimo, not Jupyter

marimo is a deliberate choice, not a default.

- **Notebooks are stored as `.py`.** Agents Read / Edit them as ordinary
  source files. `.ipynb` JSON + embedded outputs are noise that hurts agent
  comprehension and turns every diff into a metadata war.
- **Reactive dataflow graph.** A single global cannot be redefined across
  cells. This is mildly annoying for humans and an outright guardrail for
  agents — the notebook *cannot* enter the hidden-state regimes where most
  Jupyter-style leaks live.
- **`mo.ui` widgets.** The skill requires "the notebook must work as a
  self-contained communication artifact": prose interpretation, per-figure
  observations, at least one drill-down widget. marimo makes this natural;
  the equivalent in Jupyter (ipywidgets / voila) is heavyweight.
- **One cell = one fit / one evaluation.** This rule is enforceable in
  marimo because the dataflow graph already prevents cell-internal looping
  over models × features × targets without redefinition. The same rule in
  Jupyter is purely advisory and routinely violated.

If you want Jupyter, you will be fighting the skill, not using it.

## What you get, in one paragraph

Start a project → the skill scaffolds a folder with mode-specific protocol
state (`charter.md` + `capability_map.md` for R&D, or `prfaq.md` +
`explanation_ledger.md` for Pure Research), plus `decisions.md`,
`literature/`, `purposes/`, `results/`, `configs/`, `src/`, `tests/`, and
`reproducibility/`. Work begins by choosing R&D or Pure Research and keeping the
protocol layer separate from project-instance work. Trials and results are
evidence artifacts; R&D capability assessment and Pure Research explanation
assessment cite those artifacts from ledgers. Generated reports are snapshots;
durable state transitions live in the ledger and decision log.

For larger efforts, an optional R&D Program coordination layer can summarize
dependencies across child projects. It reads child gates and ledgers; it does
not own TRL, analysis tier, promotion, or claim truth.

## Quality management

Routine quality management is handled by four lightweight gates:

| Gate | Question |
|---|---|
| Entry | What live question, explanation, or capability does this update? |
| Design | What does success distinguish, and what does failure distinguish? |
| Interpretation | What can be said directly, and what competing explanations remain? |
| State update | Does a ledger assessment cite this artifact, and what transition is warranted? |

Heavy review still exists, but only for promotion moments: supported-claim
promotion, external sharing, deployment recommendation, research-line closure,
or major direction decisions.

Right-Sized Rigor sizes process weight to the research state being changed:
orientation and scaffolding can stay light, while `supported`, `matured`,
`established`, `promoted`, frozen artifacts, reproducibility, review, and
maintenance-plan requirements remain non-relaxed.

## Repository layout

```
quant-research-skill/
├── .agents/plugins/
│   └── marketplace.json       # Codex marketplace entry
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json            # Codex plugin manifest
├── skills/
│   ├── quant-research/
│   │   ├── SKILL.md           # entry point — research lifecycle
│   │   ├── references/        # protocols, loaded on demand
│   │   ├── scripts/           # reusable helpers (walk-forward, PSR, …)
│   │   └── assets/            # notebook + project templates
│   └── experiment-review/
│       ├── SKILL.md           # entry point — claim-warrant review
│       ├── references/        # 8 dimensions, severity rubric, dispatch protocol
│       └── assets/            # review report template
├── README.md
└── LICENSE
```

The repository root is the plugin root for both Claude Code and Codex. The
Codex marketplace entry points to `"path": "."`, so `skills/` is the single
source of truth for distributed skills.

## Installation

### Claude Code: from a Git repository

```text
/plugin marketplace add https://github.com/komo135/quant-research-skill
/plugin install quant-research@quant-research-skill
```

After installation the skills are referenced as
`/quant-research:quant-research` and `/quant-research:experiment-review`.

### Claude Code: local development

```bash
claude --plugin-dir /path/to/quant-research-skill
```

### Codex: from GitHub

```bash
codex plugin marketplace add https://github.com/komo135/quant-research-skill
```

Enable the installed plugin in `~/.codex/config.toml`:

```toml
[plugins."quant-research@quant-research-skill"]
enabled = true
```

The installed Codex skills are exposed as `quant-research` and
`experiment-review`.

## Usage flow

A typical research session:

1. **Bootstrap a project.** The skill scaffolds protocol/state artifacts,
   literature files, trial notebooks, generated-results folders,
   reproducibility files, and project-instance `configs/`, `src/`, and `tests/`
   placeholders.
2. **Choose mode.** R&D uses `charter.md` + `capability_map.md`; Pure Research
   uses `prfaq.md` + `explanation_ledger.md`.
3. **Keep boundaries clean.** Protocol docs define schemas, gates, statuses,
   and promotion rules. Concrete symbols, candidates, parameters, data paths,
   implementation, and generated reports stay in project-instance artifacts.
4. **Orient before testing.** Read prior work and the user's prior decisions.
5. **Run the smallest evidence-producing artifact.** Keep data splits and sanity
   checks visible.
6. **Analyze misses deeply.** Failed and ambiguous results must weaken, split,
   park, or retire rows rather than trigger a pile of new variants.
7. **Assess evidence before adding work.** If warranted, cite the artifact from
   `capability_map.md` or `explanation_ledger.md`, then record durable
   transitions in `decisions.md`.
8. **Promote only when warranted.** Run robustness / process / conclusion review /
   `experiment-review` when a result will become a supported claim or drive a
   high-impact decision.

## Bundled helper scripts

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_trial.py` | Generate a numbered evidence artifact notebook |
| `aggregate_results.py` | Append queryable evidence records to `results/results.parquet` |
| `walk_forward.py` | Compute Sharpe distribution over rolling windows |
| `bootstrap_sharpe.py` | Block-bootstrap CI for per-trade Sharpe |
| `psr_dsr.py` | Probabilistic / Deflated Sharpe Ratio |
| `fee_sensitivity.py` | Fee sweep with break-even fee extraction |
| `sensitivity_grid.py` | 2D threshold sensitivity grid |
| `vol_targeted_size.py` | Position sizing with size ∝ 1/volatility |
| `purged_kfold.py` | Purged k-fold CV (López de Prado) |
| `leakage_check.py` | Detect look-ahead bias and target leakage in features |
| `sanity_checks.py` | Programmatic bug-detection helpers used by the bug-review layer |

## A note on tone

The skill files use language like "MANDATORY", "protocol violation",
"downgrades to preliminary screening". This is intentional and applies
*within* the protocol — the layers exist precisely because the typical
failure mode is skipping them. You, the user, are always free to override
any of it: superpowers / project conventions take precedence over the
plugin. The strong tone is a guardrail for the agent, not a verdict on
your taste.

## References

The skill leans on a small number of well-known references:

- López de Prado, *Advances in Financial Machine Learning* (2018) — purged
  k-fold, embargo, CPCV, backtest overfitting.
- Bailey & López de Prado, *The Probabilistic Sharpe Ratio* (2012) and
  *The Deflated Sharpe Ratio* (2014).
- Bailey, Borwein, López de Prado, Zhu, *Pseudo-Mathematics and Financial
  Charlatanism* (2014).
- Politis & Romano, *Block Bootstrap* (1994).
- Avellaneda & Lee, *Statistical Arbitrage in the U.S. Equities Market*
  (Quantitative Finance, 2010) — reference example for math-driven
  research.
- Song, *Cross-Context Review: Improving LLM Output Quality by Separating
  Production and Review Sessions* (arxiv:2603.12123, 2026) — empirical
  basis for the adversarial reviewer's deliberately minimum context
  bundle. Reports +4.7 F1 for code-review specifically (CCR 40.7 % vs
  same-session self-review 36.0 %, Table 5).

## Status

- **Version 1.0.7** — optional R&D Program coordination plus explicit
  Result-to-Question / Result-to-Capability loops, still as a single skill with
  two review axes (process + conclusion).
- Two strict disciplines: R&D mode (Heilmeier charter → two-layer
  decomposition → Cooper Stage-Gate per capability) and Pure Research mode
  (PR/FAQ → AEA-style hash-locked pre-registration → explanation-pruning
  ledger → IMRAD draft).
- Analysis depth (A0–A5 tier) is the primary deliverable axis. Promotion
  requires A4 (estimation) minimum; A5 is assertion-level.
- Integration pattern (Pattern 1 vertical-slice / Pattern 2 bottom-up /
  Pattern 3 skeleton+spike, default) declared upfront in charter.

<details>
<summary>Changelog (click to expand)</summary>

### v1.0.7 (current)

- Added an optional R&D Program coordination layer for portfolios that combine
  R&D capability establishment with Pure Research child projects.
- Added shared Result-to-Question and Result-to-Capability loops so experiment
  outcomes promote follow-up questions, capability updates, and stop/continue
  decisions explicitly.
- Added right-sized rigor guidance and Program Map boundaries to prevent
  protocol files from absorbing project-instance facts such as active symbols,
  tuned parameters, or current PnL.

### v1.0.6

- Added selectable tracking/audit backends so agents can propose MLflow, W&B,
  Neptune, Trackio, TensorBoard, Sacred, DVC, local parquet/SQLite, or an
  organizational tracker instead of assuming custom helper scripts.
- External trackers now require a complete run inventory/export covering
  load-bearing, failed, sweep, model-selection, and promotion-eligible attempts,
  so multiple-testing and trial-count audits cannot ignore uncited runs.
- Review gates and scaffolds now accept local stamp/parquet or equivalent
  tracker records while preserving backwards compatibility for existing local
  stamp projects.

### v1.0.5

- Decoupled evidence artifacts from research contracts. R&D and Pure Research
  trial notebooks now produce neutral artifacts, while ledgers cite those
  artifacts during capability or explanation assessment.
- `aggregate_results.py` now validates queryable evidence records with the
  same required fields for both modes; mode-specific protocol identifiers live
  in ledger assessment entries.
- `new_trial.py` no longer requires capability, core-technology,
  pre-registration, question, or explanation identifiers to create an evidence
  artifact.

### v1.0.4

- Relaxed kill and reproducibility gates so terminal claims require concrete
  evidence without overclaiming machine-verifiable reproducibility.

### v1.0.3

- Added an explicit protocol-layer / project-instance-layer boundary contract
  to prevent reusable skill instructions from absorbing active research
  candidates, tuned parameters, PnL snapshots, or trial conclusions.
- New project scaffolds now include `configs/`, `src/`, and `tests/` as
  project-instance work areas, keeping concrete experiments out of protocol
  state files.
- Pure Research scaffolds now create `prereg/PR_001.md` and `new_trial.py`
  no longer falls back to retired `purpose.py.template` assets.
- R&D and Pure Research trial notebooks are evidence artifacts. Ledger files
  cite them during capability or explanation assessment instead of embedding
  protocol contracts in the generated notebook.

### v1.0.2

- Codex marketplace installation now uses the repository root as the plugin
  root (`source.path = "."`), matching the Claude plugin layout.
- Removed the stale `plugins/quant-research/` distribution copy. `skills/` is
  now the only distributed skill tree, preventing version numbers from pointing
  at old skill contents.

### v1.0.0

**Major rebuild.** A from-scratch redesign that replaces the previous 0.x
series. Not a backward-compatible patch.

What changed:

- **Single skill, two review axes.** The standalone `experiment-review`
  skill is removed; its functionality is folded into
  `references/review/conclusion_review.md` (claim-warrant axis) alongside
  the existing process audit. The previous 423-line `bug_review.md`
  protocol with 6-reviewer parallel dispatch is replaced by two
  agent-self-executable checklists totaling ~620 lines. Coverage parity
  verified (35/35 bug patterns from the old `bug_review.md`).
- **Two strict disciplines, no mode mixing.** R&D and Pure Research now
  have separate primary state objects (`capability_map.md` vs
  `explanation_ledger.md`), entry documents (Heilmeier charter vs PR/FAQ
  + pre-registration), promotion gates, and deliverable shapes (TRL-6
  capability vs IMRAD draft).
- **Heilmeier 8 questions as the R&D entry.** DARPA Heilmeier Catechism
  becomes the charter format. Without a frozen charter, capability
  decomposition is forbidden.
- **Two-layer R&D decomposition.** Layer 1 (Core Technologies,
  intellectual) sits above Layer 2 (Capabilities, operational). Each
  core technology is classified `永続型` (one-time) or `継続改善型`
  (continuous-improvement); the latter requires a maintenance plan at
  promotion.
- **Integration pattern declared in charter.** Pattern 1 (vertical
  slice / framework-first), Pattern 2 (bottom-up / component-first), or
  Pattern 3 (skeleton + spike, recommended default). Surfaces the
  "no working version yet" risk explicitly.
- **AEA-style pre-registration.** Pure Research trials are hash-locked
  before execution. Post-trial diff (`prereg_diff.py`) classifies
  deviations as minor (proceed with documentation) or major (trial
  invalidated, new pre-registration required).
- **Analysis depth tier A0–A5 is the primary deliverable.** Each trial
  has a 5-field Analysis section (Observation / Decomposition / Evidence
  weighing / Tier rating / Gap to next tier). `supported` / `matured`
  promotion requires A4 minimum. Generic terminal labels ("noise",
  "regime", "model is good") are forbidden as final claims; the rule
  applies symmetrically to success and failure.
- **Reproducibility as a 3-tuple.** Every promotion-eligible trial stamps
  `data hash + git commit + uv.lock hash` via
  `scripts/reproducibility_stamp.py`. The standardized environment is uv.
- **Bundled scripts (15 new + 6 audited).** New: `prereg_freeze`,
  `prereg_diff`, `reproducibility_stamp`, `reproducibility_verify`,
  `validate_ledger`, `charter_interview`, `draft_imrad`, `standup`,
  `render_capability_dag`, `render_explanation_dag`, `lit_fetch`,
  `cpcv`, `pbo`, `multiple_testing`, `regime_label`, `exit_compare`.
  Audited fixes in: `psr_dsr` (per-period vs annualized
  SR clarified), `bootstrap_sharpe` (Politis-Romano stationary bootstrap
  implemented; previous version cited it but ran moving-block bootstrap),
  `walk_forward` (true anchored / sliding refit; previous version was
  segment evaluation, renamed to `rolling_segment_sharpe`),
  `vol_targeted_size` (ATR → std conversion via √(π/2)), `sanity_checks`
  (random-signal benchmark gains a `signal_kind="normal"` option),
  `aggregate_results` (queryable evidence schema with `analysis_tier`).

Breaking changes from 0.x:

- `experiment-review` skill removed (functionality folded in).
- `references/bug_review.md`, `hypothesis_quality.md`, `research_state.md`,
  `research_modes.md`, `technology_decomposition.md`,
  `pure_research_protocol.md`, `failure_analysis.md` are replaced by
  files in `references/{rd,pure_research,shared,review}/`. Deprecation
  stubs at the old paths point to the new locations.
- `assets/research_state.md.template`, `hypotheses.md.template`,
  `purpose.py.template`, `README.md.template` are replaced by mode-specific
  templates in `assets/{rd,pure_research,shared}/`. Deprecation stubs at
  the old paths point to the new locations.
- `scripts/new_project.py` requires `--mode rd|pure-research`.
  `scripts/new_purpose.py` is superseded by `scripts/new_trial.py`
  (mode-aware).

Migration: existing 0.17 projects can continue to run on the deprecation
stubs; for new projects, run `scripts/new_project.py --mode <rd|pure-research>`.

</details>

## License

MIT. See [LICENSE](./LICENSE).
