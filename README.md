# quant-research-skill

A Claude Code plugin that bundles two protocol skills for **agent-driven quantitative
finance research**:

- `quant-research` — research lifecycle (hypothesis → notebook → validation →
  robustness battery), with a multi-agent **bug-review** layer (5 specialists +
  1 adversarial cold-eye reviewer) that fires on numeric red flags or before any
  `verdict = "supported"` decision.
- `experiment-review` — a separate, parallel-dispatched **claim-warrant review**
  (7 specialists + 1 adversarial cold-eye reviewer) that asks not "is the code
  correct?" but "is the conclusion warranted by what was actually tested?"

Both layers are required as a co-gate before a result can be declared
*supported*. They are intentionally not merged: they answer different questions
and their adversarial reviewers receive deliberately different minimum context
bundles, tuned to different failure modes.

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

Start a project → the skill scaffolds a folder with `hypotheses.md`,
`literature/papers.md`, `literature/differentiation.md`, `experiments/`,
`results/`, `decisions.md`, and `reproducibility/`. For each hypothesis,
one experiment = one notebook (no exceptions). The notebook template
forces a *design cell* up front: question, falsifiable hypothesis, universe
(≥ 3 instruments or a cross-section), acceptance / rejection thresholds,
data range with embargo. Validation is time-series only: time-ordered
split, embargo ≥ target horizon, walk-forward, and purged k-fold or CPCV
for ML. Exits are a first-class design choice — time-stop alone is
rejected. When numeric red flags fire (test Sharpe > 3, walk-forward mean
> 2, ML AUC on return-sign > 0.65, headline outside bootstrap 95 % CI,
…), or before a `verdict = "supported"`, the bug-review layer dispatches
six sub-agents in parallel; the adversarial sub-agent gets a deliberately
minimum bundle (code + headline numbers, no other reviewers' findings, no
`decisions.md`, no `hypotheses.md`). After bug-review passes and the
robustness battery (sensitivity, fee, bootstrap, PSR / DSR, regime
conditional) is green, the `experiment-review` skill dispatches eight
sub-agents in parallel for the claim-warrant review — its adversarial
reviewer gets the `.py` file alone, no other inputs. A result becomes
*supported* only when both review layers pass.

## The two review layers, side by side

|   | `bug_review` (in `quant-research`) | `experiment-review` (separate skill) |
|---|---|---|
| One-line | Are the code and numbers correct? | Is the claim warranted by the design? |
| Failure mode it prevents | Contaminated PnL passing all robustness gates | Real numbers that don't support the abstract's claim |
| Specialists | 5: leakage / pnl-accounting / **validation (correctness)** / statistics / code-correctness | 7: question / scope / method / **validation (sufficiency)** / claim / literature / narrative |
| Adversarial reviewer's minimum bundle | code + reported numbers | the `.py` file alone |
| Order | Precondition (run first) | Postcondition (run after robustness battery) |
| Verdict gate | **Both must pass.** | **Both must pass.** |

The `validation` overlap is the most subtle boundary: the bug-review version
checks "is the embargo wired in correctly?" (correctness), the
experiment-review version checks "is N=8 walk-forward windows enough power
to distinguish Sharpe 0.4 from 1.1?" (sufficiency). Genuine findings on
both axes are flagged independently by both.

The eighth (adversarial) reviewer in each layer is the same model as the
specialists, but with a deliberately *different* (minimum) context bundle.
The asymmetry is the mechanism — see the *References* section for the
empirical basis.

## Repository layout

```
quant-research-skill/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
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

## Installation

### From a Git repository (recommended)

```text
/plugin marketplace add https://github.com/komo135/quant-research-skill
/plugin install quant-research@quant-research-skill
```

After installation the skills are referenced as
`/quant-research:quant-research` and `/quant-research:experiment-review`.

### Local development

```bash
claude --plugin-dir /path/to/quant-research-skill
```

## Usage flow

A typical research session, end-to-end:

1. **Bootstrap a project.** Tell Claude what you want to investigate. The
   skill auto-activates; it runs `scripts/new_project.py` to scaffold the
   folder, asks you to fill `hypotheses.md` and `literature/`.
2. **Pick a hypothesis and create an experiment notebook.**
   `scripts/new_experiment.py` generates `experiments/exp_NNN_<slug>.py`
   from the template with the design-cell skeleton already in place.
3. **Iterate inside the notebook.** Cells run reactively in marimo. The
   skill enforces the "one fit / one evaluation per cell" rule and the
   "self-contained communication artifact" rule via per-section *what &
   why* cells and per-figure *observation* cells.
4. **Run the robustness battery** when the notebook is otherwise complete:
   threshold sensitivity grid, fee sensitivity sweep, walk-forward Sharpe
   distribution, block-bootstrap CI, PSR / DSR, regime-conditional metrics.
5. **Trigger bug-review.** Either Claude detects a numeric red flag and
   fires it automatically, or you fire it manually before declaring a
   verdict. Six parallel sub-agents return severity-tagged findings.
   `high` / `medium` block the verdict until resolved.
6. **Trigger experiment-review.** Eight parallel sub-agents return
   severity-tagged findings on hypothesis falsifiability, scope,
   methodology, validation sufficiency, claim calibration, literature
   coverage, notebook narrative, and an adversarial cold-eye pass.
7. **Aggregate the result.** The final notebook cell appends to
   `results/results.parquet` with a shared schema. The verdict is
   recorded in `decisions.md` with timestamps and reviewer agent IDs as
   the audit trail.
8. **Iterate cycles.** At the end of each notebook, classify derived
   hypotheses as "run now / next session / drop" — the skill rejects the
   habit of stopping after one cycle.

## Bundled helper scripts

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_experiment.py` | Generate a numbered experiment notebook from the template |
| `aggregate_results.py` | Append rows to `results/results.parquet` and query them |
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

- Version 0.4.0
- Two skills, two review layers, both required as co-gate.
- Adversarial-reviewer mechanism backed by Song (2026); see *References*.

## License

MIT. See [LICENSE](./LICENSE).
