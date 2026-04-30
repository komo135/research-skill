# quant-research-skill

A Claude Code plugin that bundles two protocol skills for **agent-driven quantitative
finance research**:

- `quant-research` — research lifecycle organised around one **Purpose** per
  notebook (an open-ended investigation), with one or more falsifiable
  **Hypotheses** tested as successive rounds inside it. Each H gets its own
  per-Hypothesis verdict gate, robustness battery, and result row. Includes
  a multi-agent **bug-review** layer (5 specialists + 1 adversarial cold-eye
  reviewer) that fires per Hypothesis on numeric red flags or before any
  `verdict = "supported"` decision. Headline-figure plan and reader takeaway
  are required pre-implementation items, not end-of-pipeline decoration.
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
`results/`, `decisions.md`, and `reproducibility/`. **One notebook = one
Purpose** (an open-ended investigation about the world); one or more
falsifiable Hypotheses are tested as successive `## H<id>` rounds inside
it. New H emerging during the run continues in the same notebook as long
as the Purpose is unchanged; only a Purpose change opens a new notebook.
The notebook template forces a *design cell* up front: Purpose, first
hypothesis (H1), universe (≥ 3 instruments or a cross-section),
acceptance / rejection thresholds, data range with embargo, **headline
figure plan**, and **reader takeaway** — the last two are required
pre-implementation items so the notebook is designed as a communication
artifact from the start, not retrofitted with charts at the end.
Validation is time-series only: time-ordered split, embargo ≥ target
horizon, walk-forward, and purged k-fold or CPCV for ML. Exits are a
first-class design choice — time-stop alone is rejected. When numeric red
flags fire (test Sharpe > 3, walk-forward mean > 2, ML AUC on return-sign
> 0.65, headline outside bootstrap 95 % CI, …), or before a
`verdict = "supported"` for any individual Hypothesis, the bug-review
layer dispatches six sub-agents in parallel; the adversarial sub-agent
gets a deliberately minimum bundle (code + headline numbers, no other
reviewers' findings, no `decisions.md`, no `hypotheses.md`). After
bug-review passes for that H and the robustness battery (sensitivity,
fee, bootstrap, PSR / DSR, regime conditional) is green, the
`experiment-review` skill dispatches eight sub-agents in parallel for the
claim-warrant review — its adversarial reviewer gets the `.py` file
alone, no other inputs. A H becomes *supported* only when both review
layers pass; one notebook can contain a mix of supported / rejected /
parked verdicts across its H rounds, synthesised in a Purpose-level
conclusion.

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
2. **Pick a Purpose and create the notebook for it.**
   `scripts/new_experiment.py` generates
   `experiments/exp_NNN_<purpose-slug>.py` from the template with the
   Purpose header, the headline-figure plan, the reader takeaway, and the
   first H block (H1) skeleton already in place — to be filled in before
   any code runs.
3. **Run H1 inside the notebook.** Cells run reactively in marimo. The
   skill enforces "one fit / one evaluation per cell", H-suffixed variable
   naming (`signal_h1`, `pnl_h1`), and the "self-contained communication
   artifact" rule via per-section *what & why* cells and per-figure
   *observation* cells.
4. **Run the robustness battery for H1**: threshold sensitivity grid, fee
   sensitivity sweep, walk-forward Sharpe distribution, block-bootstrap
   CI, PSR / DSR, regime-conditional metrics.
5. **Trigger bug-review for H1.** Either Claude detects a numeric red
   flag and fires it automatically, or you fire it manually before
   declaring H1's verdict. Six parallel sub-agents return severity-tagged
   findings. `high` / `medium` block H1's verdict until resolved.
6. **Trigger experiment-review for H1.** Eight parallel sub-agents return
   severity-tagged findings on hypothesis falsifiability, scope,
   methodology, validation sufficiency, claim calibration, literature
   coverage, notebook narrative, and an adversarial cold-eye pass.
7. **Aggregate H1's result.** Append a row to `results/results.parquet`
   for H1 (one row per Hypothesis, not per notebook) under the shared
   schema. The verdict is recorded in `decisions.md` for this Purpose's
   cycle entry, with H1 as a sub-bullet.
8. **Did a derived H emerge?** If yes and the Purpose is unchanged,
   continue inside the same notebook with a new `## H2` block (and repeat
   steps 3–7 for H2, then H3, …). If a new investigation reflects a new
   Purpose, open the next notebook (`exp_<NNN+1>_*.py`).
9. **Synthesise across H1…HN.** At the end of the notebook, write the
   Purpose-level conclusion (which H worked, which didn't, what the
   collective answer to the Purpose is) and the derived Purposes for
   future notebooks — the skill rejects the habit of stopping after one
   cycle.

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

- Version 0.8.1
- Two skills, two review layers, both required as co-gate.
- Notebook unit is one Purpose (open-ended investigation); per-Hypothesis
  verdict gates and result rows.
- R-side R&D protocol: Stage 0 (pre-hypothesis exploration), Step 1.5
  (hypothesis generation pathways), cross-H synthesis, exhaustion trigger,
  novelty / knowledge-advance gate.
- Adversarial-reviewer mechanism backed by Song (2026); see *References*.

### Changelog

**0.8.1** — Patch: closes meta-leak (F9–F11) loophole in the post-review
reconciliation pass. Reviewer vocabulary was already banned in 0.8.0 but
the reconciliation rules did not cover skill versioning, pivot history,
migration changelogs, reference-file attributions, or cross-skill API
tutorials leaking into the notebook body. Augments
`references/post_review_reconciliation.md`'s "本文に書かない語彙" table
with seven new categories (skill version numbers / compliance tags;
skill or process internal terms in body prose; reference-file
attributions; pivot / narrowing rationale sections; migration / upgrade
history; cross-skill / library API tutorials), adds four rationalization
counters covering the case where a user prompt directly asks for
migration / pivot / API-diff to be readable in the body (resolution:
preserve body cleanliness, route the requested information to git log /
README changelog / `decisions.md` / inline summary instead), extends the
why-quality self-test from three to four questions (4: skill / library /
process の固有名詞を全部マスクしたら、何が研究 claim として残るか), and
adds matching checklist items in `notebook_narrative.md`. Validated by
RED-GREEN-REFACTOR over three scenarios (skill upgrade migration /
mid-cycle pivot / cross-skill API change); F10 (pivot history) and F11
(cross-skill API tutorials) closed on the initial GREEN, F9 (skill
versioning) closed in REFACTOR after the user-instruction-override
loophole was patched.

**0.8.0** — Two complementary R-side protocol additions.

- **Cycle goal framed around the downstream consumer.** New
  `references/cycle_purpose_and_goal.md` defines the four pre-cycle items
  (Consumer / Decision / Decision rule / Knowledge output) that turn a
  Purpose into a contract with a named consumer.
  `references/research_design.md` embeds the four items into the Purpose
  header template and adds a per-H "sub-claim of the decision rule"
  mapping so the H portfolio is derived from the cycle's goal rather than
  improvised per Purpose. `references/hypothesis_cycles.md` separates
  **primary stops** (Primary YES / Fallback NO with binding axis /
  KICK-UP — the intended ways a cycle ends) from **emergency stops**
  (the N=5 / N=8 exhaustion-trigger machinery that fires when primary
  stops fail to fire), and the completion gate now requires every
  Purpose to land on a primary stop, not just satisfy the robustness
  battery on a `verdict='supported'` H.
- **Post-review reconciliation pass to keep the notebook coherent.** New
  `references/post_review_reconciliation.md` plus a Step 11b / Step 13b
  insertion in `quant-research/SKILL.md`, additions to
  `references/notebook_narrative.md` (body / audit / planning separation
  + chapter-numbering checklist + DoD pointer) and step 6 of
  `references/bug_review.md`'s dispatch protocol. Closes the
  observed-by-RED failure modes where a triggered review left the
  notebook with intercalary chapters (`§6a`, `§6b`, `§7b`, `Fig 2b`),
  reviewer vocabulary in the body (`leakage-reviewer`,
  `(literature dimension)`), edit-history language ("after bug_review
  fix", `~~2.4~~`), audit variables (`*_pre_fix`), and planning notes
  (`parked` / `follow-up` / `next-session`) leaking into the research
  artifact, and where numbers / figures / observation cells fell out of
  alignment because dependent cells were not re-executed. The pass
  enforces a 4-pattern placement decision (P1 in-place / P2 same-section
  re-compute / P3 `## Post-review addenda` / P4 new `## H<id>`),
  Definition of Done for re-execution and figure / observation
  alignment, and a top-to-bottom verification pass. Validated by
  RED-GREEN over 3 review-reflection scenarios (leakage / pnl-accounting
  / claim-warrant); 7 of 8 RED-observed failure modes eliminated, with
  F7 (cross-round cumulative consistency) documented as known residual
  to be exercised by sequential fixtures.

**0.7.0** — R-side R&D protocol added. Five interventions, validated
together by RED-GREEN-REFACTOR (5 RED + 5 GREEN + 16 loophole pressure
tests, all passing):

- **Stage 0 — pre-hypothesis exploration** (new
  `references/pre_hypothesis_exploration.md`, conditional on the
  data-without-candidate-phenomenon start state). Four mandatory
  protocol inventions: an exploration set (held-out 20 % default,
  never used in train / val / test), structural-only observations
  (existence, not parameter values), EDA → H provenance, and a
  stop rule.
- **Step 1.5 — hypothesis generation** (new
  `references/hypothesis_generation.md`). Six legal generation
  pathways — data-driven, literature-extension, literature-refutation,
  failure-derived, cross-asset extension, mechanism-driven — each
  with required citations, tier expectation, and a common-failure-mode
  table. Ad-hoc generation is a legal escape hatch with a higher
  differentiation hurdle.
- **Novelty / knowledge-advance gate** (edits to
  `experiment-review/references/review_dimensions.md`'s `literature`
  and `claim` dimensions, plus a 4th completion-gate condition in
  `quant-research/SKILL.md`). The literature dimension is split into
  coverage and novelty; novelty checks compare achieved differentiation
  tier against the H's pathway-forecasted tier. The claim dimension
  gains a symmetric "does not rebrand local replication as novel
  finding" check, addressing the prior asymmetry where only the
  underclaim direction was caught.
- **Cross-H learning** (new `references/cross_h_synthesis.md` plus
  6 schema fields in `results_db_schema.md`). Schema additions
  (`pathway`, `parent_hypothesis_id`, `verdict`, `failure_mode` with
  controlled vocabulary, `forecasted_tier`, `achieved_tier`) turn
  `results.parquet` into a queryable surface for cross-H meta-knowledge.
  The synthesis reference defines five recurring patterns (A: same
  axis fails everything; B: different axes, no convergence; C: Pareto
  re-allocation, not progress; D: monotonic improvement with
  selection caveat; E: one supported, others rejected on same axis)
  and prescribes the action for each.
- **Exhaustion trigger** (Exhaustion-criteria section in
  `references/hypothesis_cycles.md`). Hard trigger: 5 H tested under
  one Purpose without a four-gate-clean `verdict='supported'` →
  cross-H synthesis is mandatory before any H6 can be appended. Hard
  cap at N=8: the Purpose closes mechanically, further work opens a
  new Purpose with the previous synthesis as documented prior. Reset
  rule is gated on the same four-gate machinery as real verdicts so
  it cannot be escaped by a provisional `supported` label.

The five interventions compose end-to-end: Stage 0 produces a
candidate phenomenon; Step 1.5 declares its pathway and provenance;
the experiment runs; the novelty gate verifies achieved tier matches
forecast; multiple H's accumulate as queryable rows; cross-H synthesis
extracts the cluster's meta-finding; the exhaustion trigger forces
synthesis at the right moment and prevents sunk-cost iteration.

**0.6.0** — Notebook readability conventions added to
`notebook_narrative.md`: figures must be self-explanatory at figure-time
(intuitive at a glance, or with an embedded read-out — title naming the
quantity + comparison, annotation stating how to read the encoding, or a
one-line conclusion baked into the figure); when a sweep figure is paired
with an adopted configuration elsewhere in the notebook, that point is
marked on the figure. Helper functions defined in the notebook now require
docstrings stating intent, the responsibility split, args / returns with
producing / consuming cells, and side effects. Magic numbers concentrate
in a config cell at the top of each H block; downstream cells reference
the named constants, not raw literals. The notebook stays expressive
within the project's existing imports — no new external library
dependencies. Validated by RED-GREEN via subagent application scenarios
on a fresh quant-research notebook.

**0.5.0** — Notebook unit reframed from "1 hypothesis" to "1 Purpose"
(an open-ended investigation). Multiple Hypotheses serving the same
Purpose now live as successive `## H<id>` rounds inside one notebook;
verdicts and `results.parquet` rows are per-Hypothesis. Headline-figure
plan and reader takeaway promoted to required pre-implementation items
(no longer end-of-pipeline decoration). Both changes validated by
RED-GREEN-REFACTOR via subagent pressure scenarios.

**0.4.0** — Initial public release with `quant-research` and
`experiment-review` skills, multi-agent bug-review and claim-warrant
review layers, adversarial cold-eye reviewer with deliberately minimum
context bundle.

## License

MIT. See [LICENSE](./LICENSE).
