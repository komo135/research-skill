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
`literature/papers.md`, `literature/differentiation.md`, `purposes/`,
`results/`, `decisions.md`, and `reproducibility/`. **One notebook = one
Purpose** (= one parent research thesis, written as a declarative
falsifiable claim about the world); one or more admissible falsifiable
Hypotheses (each tested by one experiment = one `## H<id>` block)
decompose the parent thesis as successive rounds inside it. New H
emerging during the run continues in the same notebook as long as the
Purpose is unchanged AND it satisfies admissibility (own falsifiable
claim, own stated purpose distinct from parent, meaningful research unit
— sensitivity sweeps and parameter-only follow-ons go in the robustness
battery, not the hypothesis log); only a Purpose change opens a new
notebook. The notebook closes with a Purpose-level verdict on the
parent thesis (supported / refuted / partial / refuted-as-stated) in
addition to per-H verdicts.
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
   `scripts/new_purpose.py` generates
   `purposes/pur_NNN_<purpose-slug>.py` from the template with the
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
| `new_purpose.py` | Generate a numbered Purpose notebook (one parent thesis per file) from the template |
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

- Version 0.13.0
- Two skills, two review layers, both required as co-gate.
- Notebook unit is one Purpose (open-ended investigation); per-Hypothesis
  verdict gates and result rows.
- R-side R&D protocol: Stage 0 (pre-hypothesis exploration), Step 1.5
  (hypothesis generation pathways), cross-H synthesis, exhaustion trigger,
  novelty / knowledge-advance gate.
- Adversarial-reviewer mechanism backed by Song (2026); see *References*.

### Changelog

**0.13.0** — Adds the **hypothesis ↔ experiment inversion counter**,
closing three structural failure modes (F23 / F24 / F25) in which the
skill's vocabulary and structure made the standard "the experiment
exists to test the hypothesis" direction look reversed: the Purpose
acted as an implicit parent hypothesis with no verdict gate, the
schema's `experiment_id` reassigned `experiment` to the Purpose
container (breaking the 1 hypothesis ↔ 1 experiment correspondence),
and the derived-hypothesis examples licensed 1-axis parameter sweeps
to occupy the hypothesis log. Validated by TDD over two RED fixtures
(notebook_N for the F23 + F25 chain pathology on EUR/USD H1
mean-reversion; notebook_O for the F24 vocabulary inversion on SP500
exit-rule design) and two GREEN counterparts.

- **F23 — Purpose-as-meta-hypothesis pretense.** SKILL.md L48 defined
  Purpose as "an open-ended question about the world" while L49 / L52
  gave Form / Examples that were Y/N propositions ("Does mean-reversion
  work on EUR/USD intraday?"); L96 explicitly excluded a Purpose-level
  verdict ("the notebook itself does not have a single verdict");
  cross_h_synthesis.md Pattern A / B's Action menu licensed
  carry-forward of the parent claim into a derived Purpose
  ("lower-frequency variants of the same signal") without first
  verdicting it. Counter rewrites the Purpose vs. Hypothesis table to
  declarative falsifiable form ("Mean-reversion at H1 frequency on
  EUR/USD generates risk-adjusted edge net of cost (≥ 0.5 test Sharpe
  with 1 bp/side fees)" instead of the question form), removes the
  L96 / L783-786 verdict-gate denial, adds a "Purpose-level closure
  gate (per Notebook)" section requiring supported / refuted / partial
  / refuted-as-stated at notebook close, and rewrites Pattern A / B
  Action menus + Handoff section to require parent-thesis verdict as
  precondition 0 before any derived Purpose may open. Anti-rationalization
  table gains entries on Purpose-verdict denial and threshold-variation
  rerun. The parent claim now has a place to die in writing; F23 was
  the load-bearing reason a 4 / 5-level hypothesis chain
  (Purpose-as-parent → H1 → derived H2 → derived H3 → derived Purpose
  with the same parent claim) could persist with no claim ever being
  rejected.

- **F24 — Experiment vocabulary inversion.** SKILL.md L653-655 defined
  `experiment_id (= the notebook = the Purpose)` with `hypothesis_id`
  as the H within it; folder `experiments/` and file
  `exp_NNN_<purpose-slug>.py` reinforced "experiment = container".
  Asked "what is H2's experiment?", the protocol-correct answer was
  "the apparatus shared with H1/H3 with exit_rule replaced", i.e.
  H2 had no experiment of its own. Counter renames the schema field to
  `purpose_id` (with prose explaining the prior name was a vocabulary
  inversion that conflated the notebook with an experiment, retired
  here), reattributes "experiment" to "the apparatus that tests one
  hypothesis" — each `## H<id>` block IS one experiment — and renames
  folder `experiments/` → `purposes/`, file prefix `exp_NNN_*.py` →
  `pur_NNN_*.py`, helper script `scripts/new_experiment.py` →
  `scripts/new_purpose.py`, asset
  `assets/experiment.py.template` → `assets/purpose.py.template`. The
  rename propagates through results_db_schema.md, hypothesis_cycles.md,
  cross_h_synthesis.md, experiment_protocol.md, research_design.md,
  marimo_cell_granularity.md, model_diagnostics.md,
  feature_construction.md, prediction_to_decision.md,
  cycle_purpose_and_goal.md, project layout templates
  (hypotheses.md.template, INDEX.md.template, decisions.md.template,
  README.md.template), and the experiment-review skill's
  references/review_protocol.md / review_dimensions.md. The
  1 hypothesis ↔ 1 experiment correspondence is restored; in a Purpose
  with N admissible H's, the notebook is a cluster of N experiments
  sharing an apparatus (apparatus = universe + split + baseline + fee
  model + entry rule), each H block replacing the apparatus slot the H
  is testing.

- **F25 — Derived hypothesis granularity licensing.** SKILL.md L63-71
  gave 5 derived-H types (sensitivity / parameter-sweep / failure-diagnosis
  / specialization / alternative formulation / follow-on layer) with no
  requirement that each derived H declare an own falsifiable claim
  distinct from the parent or an own stated purpose. The result: a
  rejected H1 spawned an H2 sensitivity variant whose claim was
  identical in shape and threshold to H1, then an H3 regime-conditioning
  variant on top of H2 — three rows in results.parquet for one research
  finding. Counter introduces a "Derived hypothesis admissibility"
  section in SKILL.md and an admissibility sub-step 0 in
  hypothesis_cycles.md routing rule, requiring all three of: (a) own
  falsifiable claim distinct from parent (different decision axis, not
  just tighter / looser threshold on the parent's axis), (b) own
  stated purpose written before the H runs (one sentence answering
  "what new question does this H answer that the parent did not?"),
  (c) meaningful research unit (not a 1-axis sweep over sizing /
  threshold / regime / lookback / cost / fee). Inadmissible patterns —
  sensitivity / parameter-sweep variant, follow-on layer that doesn't
  change the underlying claim, threshold-variation rerun, and
  diagnosis without an independent claim — are reclassified as Step 12
  robustness battery / Step 10 portfolio construction inside the
  parent H's section, not as new H<id>s in the hypothesis log. The
  hypothesis log now carries one row per meaningful research unit;
  parameter sweeps live in robustness as 2D / 3D grids inside the
  parent H, where they belong.

The change is independent of F1-F22. F23 cannot be reduced to F24
(renaming the schema field does not introduce a Purpose-level verdict
gate) and F25 cannot be reduced to F23 (adding Purpose-level verdict
does not require derived H to declare own claim / purpose / unit).
F24 remains independent of F23 / F25 — even with a Purpose-level
verdict and admissibility constraints in place, a schema field named
`experiment_id` would continue to signal "experiment = container" to
both agents and human readers.

Out of scope (recorded as future RED breadcrumbs in the GREEN
results): the design-hypothesis layer (decisions.md at-open prediction)
that may also act as an unverdicted parent claim is not addressed here
— it is structurally similar to F23 but lives at a different layer
and requires independent treatment. The research-goal sub-claim's
explicit `refuted` transition condition (when a Purpose-level
`refuted` verdict mechanically transitions a sub-claim to `falsified`)
is also not added here.

**0.12.0** — Adds **review dispatch efficiency** to the bug-review and
experiment-review layers, closing two efficiency-class failure modes
(F21 / F22) in which 14 sub-agents per H verdict='supported' attempt
billed dead weight on every dispatch and re-fired in full on every
re-verify after fix reconciliation. Quality machinery (narrowness /
bundle asymmetry / parallelism / trigger discipline before
verdict='supported') is left strictly unchanged; the savings come from
removing dead-weight reference sections (F21) and from skipping
re-verifies for dimensions whose surface map didn't intersect the
applied fixes (F22). Validated by TDD over an audit-type fixture
(matrix of 14 reviewer × N input file with section-level line counts,
plus iteration-profile agent-run counting).

- **F21 — Per-reviewer / per-dimension input contract.** New section in
  both `quant-research/references/bug_review.md` ("Per-reviewer input
  contract", 6 reviewer rows) and
  `experiment-review/references/review_protocol.md` ("Per-dimension input
  contract", 8 dimension rows). Each reviewer receives only its own
  dimension scope (extracted by section anchor — `### N. <reviewer-name>`
  for `bug_review.md`, `## N. <dimension>` for `review_dimensions.md`)
  plus the artifacts named in its required-shared column. Whole-file
  `bug_review.md` (300 lines) and whole-file `review_dimensions.md` (489
  lines) are no longer delivered to specialists — the prior "whole file +
  read §i only" pattern billed 77-96 % dead weight per specialist and
  diluted attention via lost-in-middle. Section anchors are the
  source-of-truth for extraction; line ranges are illustrative only and a
  renamed anchor surfaces a `severity: high, what: missing input section
  §<N>` graceful-degradation finding rather than silently breaking. The
  `experiment-review` SKILL.md Process table and the dispatch protocols
  in both files are updated to mandate pre-extraction. Adversary's
  extraction tightens, not weakens, the bundle asymmetry (§1-§7
  specialist scope is now physically excluded rather than relying on the
  "read only your section" formal rule). Raw input lines across 14
  reviewers drop from 23115 to 17629 (-24 %).
- **F22 — Trigger-conditional dispatch on re-verify.** New section in
  both protocol files ("Trigger-conditional dispatch on re-verify"). A
  typical H verdict='supported' attempt enters the gate multiple times
  (Initial → fix → Re-verify → fix → Re-verify → ...). The naive contract
  re-fired all 14 every round, billing surface-unchanged reviewers as
  dead reading. F22 splits dispatch into Initial (= all 14 fire) and
  Re-verify (= the parent identifies which surface map entries the fixes
  touched, fires only those specialists + adversary). Surface map covers
  6 + 8 dimensions: leakage on feature/signal/normalization/scaling/
  cross-section/factor cells; pnl-accounting on PnL/position/fee/
  turnover/sign cells; validation-correctness on split/embargo/
  walk-forward/CPCV/test-set cells; statistics on bootstrap/WF-summary/
  DSR/PSR/headline-metric cells; code-correctness as catch-all on any
  code change; question on H statement / design / thresholds / cycle
  hygiene; scope on universe/period/regime/cross-section; method on
  model/baselines/features/hyperparameters; validation-sufficiency on
  WF window count / power claims; claim on abstract/verdict/conclusion;
  literature on `literature/` files; narrative on any markdown / figure
  plan / observation cell; adversarial as auto-fire on any specialist
  re-fire. **When in doubt, fire** is the explicit default — surface
  ambiguity → fire candidates plus adversary, never skip. Cross-session
  defaults to Initial unless `decisions.md` carries an explicit
  attestation that named dimensions were verified clean against a named
  artifact state. Iteration profiles savings: -32 % at depth 2,
  -43 % at depth 3, -48 % at depth 4 (typical re-verify ≈ 5 reviewers
  out of 14).
- **F20 — considered, not adopted.** Prompt caching (= placing a
  byte-identical prefix at the front of all reviewer prompts so cache
  read costs replace cache write costs across the parallel batch) was
  drafted as a third lever and rejected. Claude Code's harness handles
  the underlying API call; skill text cannot mandate `cache_control`
  markers, and parallel sub-agent prefix-cache sharing is not a
  documented harness behavior. F-id taxonomy carries F20 as a gap with
  the rejection reason recorded in
  `skill_tests/red_review_dispatch_efficiency/RED_dispatch_efficiency_findings.md`,
  preserving the dead-end as a TDD breadcrumb for future maintainers.
- **Anti-rationalizations.** Each protocol file gains a F21/F22 block
  covering the natural excuses ("whole file is safer", "send adversary
  more context", "pre-extraction is brittle", "user wanted comprehensive",
  "narrative refs should also be extracted (counter)", "fix is small so
  re-fire all", "ambiguous surface so skip", "I remember it was clean so
  treat cross-session as re-verify", "wording-only fix is skip"). Single-
  agent fallback explicitly notes that F21 / F22 still apply
  sequentially — the fallback path inherits the savings.

The change is orthogonal to F1-F19 (all quality-class — body / reviewer-
vocab leakage, skill-version / migration leakage, 派生 H table leakage,
research-goal layer absence, carry-forward conjunct gate, research-subject
drift). F21 / F22 are the first efficiency-class entries in the F-id
sequence; they describe dead weight in dispatch process rather than
content drift, and are explicitly framed in the RED findings to avoid
collapsing them into the quality-class taxonomy.

**0.11.0** — Adds the **research-subject drift counter**, closing two
silence-licensed inversion paths (F18 / F19) in which the cycle's
de facto deliverable shifts from a market claim to an implementation
property — what was reported as "主体が研究ではなく実装 / コードに
なる、コードの正しさを確認するために研究 / 実験をしている". F18
fires when expected real data is unavailable and an agent silently
substitutes synthetic data, reframing the Purpose as a "pipeline-
correctness scaffold"; F19 fires when data IS available and the
per-H abstract's lead sentence describes the deliverable as
code / library / numerical correctness rather than the falsifiable
claim's answer. Validated by TDD over two hand-written fixtures
(Case L data unavailable + Case M abstract misframed) plus a
Phase-A artifact-scoring pass on the existing `green_exp_001.py`
that surfaced the failure mode in flagrant form before the fixture
was written.

- **Data availability gate.** New section in
  `references/experiment_protocol.md`. Rule: if the cycle's research
  subject is real-world behavior AND the expected real data is
  unavailable in the execution environment, the cycle is **BLOCKED**;
  synthetic substitution within an instantiated cycle is forbidden.
  Synthetic-data scaffolding outside the protocol (no Cycle goal, no
  verdict cell, no `results.parquet` row) is engineering work and
  remains permitted. The exception — synthetic data IS the research
  subject — applies only when the Decision rule's threshold is on a
  property of the estimator / algorithm itself (parameter recovery
  error, convergence rate, bias relative to a known DGP), not on a
  numeric metric on real returns (Sharpe / IC / drawdown / win rate /
  fee-adjusted PnL / turnover / tracking error). The mechanical
  reinforcement closes the most common rationalization loophole
  ("synthetic data as a known DGP for pipeline verification" — the
  metrics are on real-returns shape, not on estimator-recovery shape,
  so the exception does not apply). Forward path when BLOCKED: file
  as a structural finding in `decisions.md`, mark the cycle
  suspended, and pivot to a data-available cycle or return to
  project-portfolio re-prioritization. The BLOCKED state is itself
  a research output (the project's data-acquisition layer is
  surfaced as a binding constraint).
- **Per-H abstract format rule.** New sub-section in
  `references/notebook_narrative.md` 1b "Format rule — first sentence
  is the market claim, not the implementation". The first sentence
  of each H's abstract names the answer to the falsifiable comparison
  in the H's own terms (mechanism / market / regime / instrument);
  implementation / library / numerical correctness statements appear
  only in a clearly-bounded *Reproducibility note* at the end of the
  abstract or as a closing sentence — never as the lead. Rationale:
  the per-H abstract is what a reader scrolling the notebook reads
  first; if the lead is "the implementation is correct" or "the
  decomposition matches sklearn's reference", the reader's takeaway
  is the engineering deliverable, not the world's answer, and the
  cycle's de facto deliverable inverts. Five anti-rationalization
  entries cover the natural excuses ("showing implementation
  correctness increases verdict trust", "robustness battery passing
  is part of the claim", "library reconciliation is
  research-community-facing reproducibility", "the market claim is
  too narrow / tentative to lead with", "user prompt requested
  implementation details up front").
- **Template change.** `assets/experiment.py.template` H1 round now
  carries an explicit `### H1 abstract` slot, placed first in the
  H1 block (filled after H1 cells run), with the format rule and
  good / anti-pattern lead examples inline. The agent encounters
  the rule at template-fill time, not only at writing time.
- **No new completion gate, no new reference file.** The fix lives
  in two existing references plus a SKILL.md sub-step 2.5 and a
  Step 16 paragraph; SKILL.md's four-gate completion contract is
  unchanged. The format rule bites at three timings — generation
  via template, writing via reference, verification via the
  separate `experiment-review` skill's narrative-dimension reviewer
  reading `notebook_narrative.md`. New gate machinery (a 5th
  completion gate, a separately-dispatched reviewer) was rejected
  as unnecessary; the two-layer fix sits cleanly on the existing
  surface.

The change is orthogonal to F1–F17. F1–F8 (history / reviewer-vocab
leakage into body), F9–F11 (skill version / migration / cross-skill
API tutorials in body), F12–F14 (派生 H table leakage into the
notebook body), F15–F16 (research-goal layer absence), and F17
(carry-forward conjunct-contribution gate) all operate at different
layers of the protocol; F18 / F19 surface a previously-uncovered
inversion path in which the *named deliverable* of the cycle is not
what the protocol assumed it would be (substitution-on-missing-data
in F18; abstract framing on implementation property in F19). One
inversion path remains uncovered (reconciliation focus-pull in
`references/post_review_reconciliation.md`'s Definition of Done,
which is heavily weighted toward code-output alignment) and is
documented as a future RED phase in
`skill_tests/red_research_subject_drift/RED_research_subject_drift_findings.md`'s
"Scope 限界" section.

**0.10.0** — Adds the **carry-forward conjunct-contribution gate**
(sub-step 1.5 of `hypothesis_cycles.md`'s routing rule), closing the
F17 failure mode in which derived hypotheses were enumerated
bookkeeping-style without being asked how they advance the cycle goal's
decision rule. The previous routing rule decided where a derived H goes
by (1) Purpose continuity and (2) run-now / next-session / drop only —
nothing forced the question "which conjunct of the YES / NO / KICK-UP
branches does this carry-forward H close, and is that conjunct already
addressed by the parent H?" Result: a Pathway-4 sensitivity variant on
the same instrument as the parent could route through cleanly while a
multi-instrument YES-conjunct of the cycle goal remained untouched.
Validated by TDD over scenario L (mid-range parent on EUR/USD only +
RSI parameter-sweep H on the same EUR/USD + YES (b) ≥3-pair conjunct
unaddressed): the RED subagent flagged the binding gap as a side-note
but did not block the H ("not blocking H2: a tighter-threshold
sensitivity probe ... is a legitimate Pathway-4 step"); the GREEN
subagent rejects the candidate at the new gate and proposes a
replacement targeting the binding gap.

- **Sub-step 1.5 (conjunct contribution gate).** New section in
  `references/hypothesis_cycles.md`'s routing rule, fired on the
  same-notebook branch only (new-Purpose H's are gated against their
  own new cycle goal at the new notebook's open). Classifies the new
  H as **eligible** (unaddressed conjunct, or middle-range conjunct
  via a structurally different test — different exit, different
  feature, different fee model), **redundant** (parent already landed
  the conjunct per `cycle_purpose_and_goal.md`'s "Stop the cycle as
  soon as the rule fires" definition), or **freelance** (closes no
  conjunct of the decision rule). The verdict is reported inline in
  the assistant's reply; rejected-at-routing H's persist as a
  `planned-drop` row with the reject reason in the Statement column.
- **`closes_conjuncts` schema column.** New column in `hypotheses.md`
  rows. Enumerates the YES / NO / KICK-UP conjuncts the H tests,
  optionally annotated with structural progress (e.g. `YES_b (3/3
  instruments)`). It is the **cycle-goal-layer** counterpart to the
  **research-goal-layer** `target_sub_claim_id` column added in 0.9.0;
  the two layers are orthogonal and both anchor a derived H — one to
  the project's running research question, the other to the current
  cycle's decision rule.
- **Anti-rationalization table** of five excuses the gate is built to
  interrupt: "Pathway 4 makes it legitimate" (gate is goal-contribution,
  not generation provenance — Pathway is necessary but not sufficient),
  "I'll flag the binding gap as a design-hypothesis-at-open concern in
  `decisions.md` and proceed" (gate is a gate, not a flag — logging the
  gap is parallel work, not a substitute), "sub-step 1.5 will rarely
  fire" (true for the eligible majority; the gate exists to catch the
  minority of natural-looking Pathway-4 derivations that actually
  re-test landed conjuncts), "I'll write `closes_conjuncts = TBD`"
  (legal only for new-Purpose H's; for same-Purpose derived H's the
  cycle goal is already on the page), "if 1.5 keeps rejecting my H's,
  the cycle is stuck — I'll skip 1.5 once" (a series of rejects is the
  cross-H synthesis trigger, not an obstruction).
- **`planned-drop` sub-categorization.** The status keyword now covers
  three sub-categories (out-of-scope drop / rejected-at-routing /
  superseded). The Statement column's leading clause identifies which
  fired, so cross-H synthesis at Purpose closure can distinguish the
  three at the row level instead of collapsing them into one bucket.
- **Notebook-body H-id numbering rule.** H-ids are global and
  sequential across `hypotheses.md`, permanent at moment of
  consideration. H's that ran get one `## H<id>` block with the row id
  verbatim; H's that did not run (rejected-at-routing, out-of-scope
  drop, superseded) get no notebook block. Notebook H-id sequence may
  have gaps — those gaps are the audit trail of considered-but-not-run
  candidates and may not be renumbered away. Closes the previously
  open question of whether a routing-rejected H consumes an id, gets
  prime-suffixed, or is renumbered into the next available `## H<id>`
  slot — different agents had been answering this differently.
- **Back-references.** `cycle_purpose_and_goal.md`'s "How to plan the
  H portfolio" (initial-portfolio decomposition) now points forward to
  sub-step 1.5 as the carry-forward equivalent. `SKILL.md` step 2's
  existing per-H "sub-claim mapping" line now points forward to
  sub-step 1.5 as the carry-forward enforcement point — previously the
  mapping was a recording requirement only and did not flow into a
  routing decision.

The change is orthogonal to the F12–F16 family of failure modes that
0.9.0 closed: F12–F14 (派生 H table leakage into notebook body) is a
record-location problem; F15–F16 (research-goal layer absence) is a
project-level layer problem; F17 closed here is a cycle-internal
conjunct-mapping problem on the routing path. Each layer needs its
own counter; this release supplies the third.

**0.9.0** — Introduces a **four-layer model** (Research goal / Design
hypothesis / Purpose / Hypothesis) that anchors every derived hypothesis
to a project-level research-goal sub-claim, closes the F12–F16 family
of failure modes in derived-hypothesis routing and Purpose handoff.
Validated by TDD over five scenarios (run-now promotion / multi-round
table accumulation / new-Purpose handoff / derivation root-cause
absence / Purpose-close research-goal-distance absence).

- **Layered model.** New `references/research_goal_layer.md` adds the
  upper two layers above the existing Purpose / Hypothesis pair. The
  project README now carries a research-goal sub-claim list with stable
  IDs (`G1.1`, `G1.2`, …); each Purpose declares its
  `target_sub_claim_id` as the **5th item** of the cycle goal in
  `references/cycle_purpose_and_goal.md`; each H row in `hypotheses.md`
  carries its own `target_sub_claim_id` (inherited from the parent H by
  default, override recorded in the Statement column with reason).
- **Derived-hypothesis table template removed** from
  `references/hypothesis_cycles.md` (closes F12–F14). Per-H planning
  state (`planned-runnow` / `planned-nextsession` / `planned-drop`) is
  now recorded as a single source of truth in the `Status` column of
  `hypotheses.md` rather than as a `### Derived hypotheses` table in the
  notebook body. The cross-notebook handoff rule for derived Purposes
  is moved into a new section of `references/cross_h_synthesis.md`
  ("Handoff to the next notebook"): old-Purpose synthesis, Pattern
  labels, binding-axis prose, and `## Origin` sections are forbidden in
  the new notebook's body. Minimal cross-references conveying research
  content (e.g. comparison-series names in a Figure plan) remain
  permitted.
- **Design-hypothesis bookkeeping at Purpose closure** (closes F15–F16).
  `assets/decisions.md.template`'s Purpose entry gains three mandatory
  sections: **Design hypothesis at open** (the prediction "this Purpose
  closes such-and-such sub-claims"), **Research-goal sub-claim progress
  update** (the transition for every sub-claim this Purpose touched —
  unchanged sub-claims listed too, so the project's running state is
  fully visible), and **Design hypothesis at close** (CONFIRMED /
  FALSIFIED / PARTIAL). The next Purpose's selection is justified from
  the sub-claim status table in the project README, not from per-H
  numeric observations alone.
- **Schema extensions kept aligned across templates and helpers.**
  `assets/hypotheses.md.template` adds `target_sub_claim_id` and
  `pathway` columns; `assets/INDEX.md.template` adds
  `target_sub_claim_id` per notebook; `assets/experiment.py.template`'s
  Purpose header gains the Cycle goal 5-item block, the per-H result
  row gains `target_sub_claim_id` / `pathway` / `parent_hypothesis_id`,
  and the closing checklist is updated to drive the new bookkeeping;
  `references/results_db_schema.md` adds the `target_sub_claim_id`
  column to the per-H row schema; `scripts/aggregate_results.py`'s
  `REQUIRED_FIELDS` is extended accordingly. `SKILL.md` step 2 declares
  the Cycle goal as 5 items; step 14 documents the sub-claim progress
  update + design hypothesis at close as part of result aggregation.

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
