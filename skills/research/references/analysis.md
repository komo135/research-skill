# Analysis

## Purpose

Analysis is the activity between **"the experiment ran"** and **"the parent workflow decides what to do with the result."** It is exploratory by nature, produces many intermediate artifacts, and has its own discipline distinct from planning, execution, claim-recording, and state updates.

For post-result explanation in the `research` protocol, result analysis is performed by a fresh separate-context result-analysis subagent using the `research-result-analysis` skill. The main research agent records Actual execution and Planned vs Actual, then passes only the plan path to the analysis subagent. This reference defines the explanation discipline that the subagent applies.

Two flavors:

- **EDA (Exploratory Data Analysis)** — done before or during plan design, to understand what the data actually contains before committing to a plan
- **Result analysis** — done after experiments run, to explain why the observed result happened before any downstream claim, decision, or next action is chosen

Both have well-established methodology. Claim structure (see `claim_structure.md`) and decisions (see `iteration_loop.md`) are downstream consumers of analysis. They must not be folded into result analysis itself.

## Result analysis explanation center

Result analysis asks why the result happened. It treats artifacts, tables, logs, traces, and summaries as material for explanation, not as a courtroom for deciding whether the result is valid or promotable. If execution procedure itself produced the result shape, include that as a generative explanation; do not stop at a procedure verdict.

A complete result analysis separates:

1. **Result shape** — aggregate movement, slices, seed or repetition variability, failures, anomalies, traces, and condition-specific effects.
2. **Explanatory contrast** — what part of the observed result needs explanation relative to the plan's expectation. This is not a pass/fail judgment.
3. **Factor decomposition** — data, representation, model/method, process/dynamics, resource/system, measurement/evaluator, and interaction factors that could have generated the result.
4. **Mechanism traces** — chains from starting condition through local process/activity and intermediate state to the result-producing step.
5. **Candidate explanations** — competing generative explanations for the same observed shape.
6. **Explained and unexplained result features** — what each explanation accounts for and what remains surprising.
7. **Discriminating analysis** — the ablation, slice, trace, perturbation, failure sample, limiting case, or theoretical check that would separate leading explanations.
8. **Open explanatory branches** — specific remaining why-branches, not generic caveats.

Mechanism explanations require more than aggregate association. Association-only patterns can motivate candidates, but they do not explain why the result happened until the analysis states a plausible generative chain and the result features that chain makes expected. A missed prediction requires especially careful decomposition, but the goal is still explanation, not a status label.

## Research script artifact contract

EDA and result-analysis scripts may print progress, but stdout is not evidence. A print-only script run leaves no audit trail for later analysis, review, or report writing. Every completed research script run must write durable artifact files under `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/runs/<run_id>/`:

- `run_manifest.json` records the command, `status: completed`, seed or material run condition, and manifest-listed artifact paths.
- `logs/stdout.log` and `logs/stderr.log` capture console output for debugging and provenance.
- `intermediate/` stores intermediate data, filtered slices, derived features, sampled records, or diagnostics needed to audit how the final observation was produced.
- `outputs/`, `tables/`, or `figures/` store metrics, tables, plots, predictions, traces, or other evidence that later claims and reports can cite.

Run `scripts/check_run_artifacts.py` before promoting observations from EDA or result analysis. The checker does not impose a full experiment-tracker schema; it only rejects terminal-only evidence by requiring at least one manifest-listed non-log durable artifact.

## EDA standard pass

The modern EDA pipeline derives from Tukey's *Exploratory Data Analysis* (1977) and Wickham's tidy-data restatement. The common core across authoritative sources:

1. **Tidy / shape check** — every variable a column, every observation a row. If the data is not in this shape, reshape before anything else ([Wickham, *Tidy Data*](https://vita.had.co.nz/papers/tidy-data.pdf))
2. **Per-variable distribution + missingness** — histogram, summary statistics resistant to skew/heavy tails (median + IQR, not just mean + SD per [Tukey 1977](https://www.consoleflare.com/blog/wp-content/uploads/2022/09/Exploratory-Data-Analysis-1977-John-Tukey.pdf))
3. **Outlier / re-expression decision** — identify outliers, decide whether to transform (log, Box-Cox), winsorize, or drop. Decision recorded in plan
4. **Pairwise covariation** — scatter / correlation / cross-tabs between variables of interest, before any model
5. **Class balance + temporal/group splits** — if the data has classes or groups, check imbalance. If temporal, check distribution shift across time
6. **Leakage probe** — actively look for train-test contamination, target proxies, future-information leak. [Kapoor & Narayanan 2023](https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9) catalogue 8 leakage types across 294 affected papers. This is non-optional for any claim-bearing ML work
7. **Time-series additions** — for temporal data: stationarity (visual run-sequence plot, Augmented Dickey-Fuller), autocorrelation (ACF/PACF). See `skills/quant-research/references/shared/time_series_validation.md` for design implications

The output of EDA is a **revised understanding of the variable space** that informs `observations.md`, `analyses.md`, and then the derived hypothesis plan under `propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md`. Findings that look like results should be treated as exploratory and not claimed as confirmatory — see depth stop conditions below.

## Result analysis explanation operations

After experiments run, result analysis should use the same families of operations that strong empirical papers use to understand where a result came from. These operations are not claim-readiness gates inside result analysis. They are ways to explain the result-producing process.

| Operation | What it explains | Standard reference |
|---|---|---|
| **Mechanism decomposition** | entities, activities, organization, and conditions that make the result occur | Machamer, Darden, and Craver 2000 |
| **Cause-effect trace** | the sequence of input differences, state differences, and intermediate effects that lead to the result | Zeller 2002 |
| **Variance-source analysis** | whether seeds, sampling, initialization, hyperparameters, or environment variation carry the observed shape | Bouthillier et al. 2021 |
| **Ablation / contribution analysis** | which component, rule, representation, or process step is responsible for a result feature | Lipton & Steinhardt 2018 |
| **Slice / behavioral analysis** | which capability, subgroup, input family, regime, or condition produces the aggregate pattern | Ribeiro et al. 2020 |
| **Model / workflow checking** | whether the model, computation, or analysis workflow itself creates the observed pattern | Gelman et al. 2020 |
| **Resource / measurement analysis** | whether performance, latency, or systems results come from measurement bias, contention, queues, memory, IO, or scheduling | Mytkowicz et al. 2009; Curtsinger & Berger 2015 |

For non-ML CS and quantitative research, adapt the same operations:

- "Slices" means natural subgroups, regimes, populations, conditions, or time blocks.
- "Ablation" means removing or isolating a component, assumption, feature, rule, or process step.
- "Variance" means repetition, seed, sampling, initialization, parameter, or environment variability.
- "Behavioral analysis" means checking which input or condition family creates the observed outcome.
- "Cause-effect trace" means tracing state transitions, transformations, intermediate variables, or proof steps.
- In PL, compiler, parser, and runtime work, trace AST, IR, type-state, control-flow, optimization pass, grammar rule, or recovery-state transitions.
- In systems and distributed work, trace queues, locks, message order, cache locality, scheduling, batching, resource contention, workload slice, and tail behavior.
- In security, verification, and formal-methods work, trace exploit paths, counterexamples, proof obligations, invariants, assumptions, and boundary conditions.

For stochastic systems, do not explain a result from a single fixed seed as if it revealed the whole process. A fixed seed can explain one trajectory, but the result-generating process may include seed, sampling, initialization, or environment variation.

## Analysis depth — when is it enough?

Three orthogonal stop criteria from the methodology literature:

### 1. Tukey's compromise: "do enough to see if there's something to see"

EDA is pre-confirmatory. The stop condition is **"a hypothesis worth testing has emerged"** or **"the variable space is now understood well enough to plan an experiment"** — NOT "all questions are answered." For EDA, going further when no new structure is emerging is wasted effort.

### 2. Depth-to-explain-the-result

Result analysis should be scoped to the observed result shape. Continue while a major result feature remains unexplained: an aggregate/slice mismatch, a time trace, a concentrated failure family, a state transition, a variance source, or a system interaction. Stop when the leading explanations account for the important result features and the remaining open branches are specific enough for the parent workflow to inspect.

The Gelman & Loken "garden of forking paths" result still matters: every extra branch chosen after seeing the result can become post-hoc story selection. The practical consequence is not "avoid analysis"; it is **make the explanatory target explicit**. If a branch does not explain a concrete result feature, do not add it.

### 3. Discriminator clarity

Analysis is deep enough when it names the discriminator that would separate live explanations: ablation, perturbation, slice, trace, failure sample, limiting case, state inspection, variance decomposition, or theoretical check. The result-analysis subagent does not choose that next action; it only leaves the explanatory branches inspectable.

### Composite stop rule

```
Analyzing for: EDA / exploratory mapping?
  Stop when: new structure is no longer emerging.

Analyzing a completed result?
  Stop when: important result features have plausible mechanism traces AND
             remaining open branches name specific discriminators.
  Continue when: an aggregate, slice, trace, anomaly, state transition,
             or interaction remains unexplained.

Analyzing for: terminal_kill?
  Stop when: the result-producing process is localized enough that the
             parent workflow can decide whether to repair, revise, split, or close.
```

## Observation → Interpretation → Claim staging

The progression from raw output to load-bearing claim has three stages. This maps to [Toulmin's 1958 argument structure](https://en.wikipedia.org/wiki/Stephen_Toulmin#The_Toulmin_model_of_argument) — and confusing the stages is the most common failure in agent-written research.

### Stage 1: Observation

A literal fact extracted from raw data or a run artifact. No interpretation.

- ✓ "Seed_2 at batch_size=512 diverged with loss spike at epoch 12."
- ✓ "Validation perplexity: 18.34 (mean across 3 seeds, std 0.07)."
- ✓ "The covariance matrix has condition number 1.2e6."
- ✗ "The model is unstable." ← This is already interpretation.
- ✗ "The method works better." ← Comparative interpretation.

Observations go into `propositions/Pxxx_slug/observations.md`, into the hypothesis plan's Actual execution section, or into notebooks. They do not need claim_structure formatting.

### Stage 2: Interpretation

An explanation or mechanism proposed for the observation. Still preliminary — alternatives remain.

- "The divergence at epoch 12 suggests the peak learning rate after warmup exceeds the model's stability threshold at this batch size."
- "The 0.18 perplexity improvement may come from the sparse-attention variant OR from the 1.3% increase in active FLOPs."

Interpretations are explanations in progress. They appear in plan narrative (Methodology / Observations sections) or Result analysis, but they are not yet load-bearing claims or state decisions.

### Stage 3: Claim

A load-bearing assertion, structured per `claim_structure.md`. Has evidence backing, alternatives explicitly listed, conditions stated. The agent has done the work to defend it.

The transition from interpretation to claim happens after Result analysis, in the parent workflow. An interpretation becomes a claim only when:

- The evidence is anchored to specific artifacts (file:line, run, value)
- Alternative explanations have been actively considered (and listed if not excluded)
- The conditions under which the claim holds are stated precisely
- A fresh separate-context result-analysis subagent using `research-result-analysis` has returned a `## Result analysis` section from the plan path only
- The claim is written only after mechanism traces, explained and unexplained result features, open explanatory branches, tested conditions, and missing conditions have been reconciled with `claim_structure.md`

### Pearl's Ladder applies

[Pearl's Ladder of Causation](https://causalai.net/r60.pdf) sets a hard constraint: **you cannot answer a higher-rung question with lower-rung evidence.**

- **Rung 1 (Association)**: A diagnostic plot showing correlation between two variables
- **Rung 2 (Intervention)**: An ablation result — what happens when component X is removed
- **Rung 3 (Counterfactual)**: A claim about why something failed — "if we had used warmup=40 epochs, it would have converged"

A diagnostic plot is not sufficient warrant for a causal/counterfactual claim. The disciplined progression: observe → ablate → make a Rung 2 claim. Counterfactual (Rung 3) claims require additional causal structure (controlled intervention isolating the alleged mechanism).

In the iteration_loop, this maps to:
- Rung 1 observations may mark the proposition `under-specified` and prompt a narrower derived hypothesis or material-acquisition step.
- Rung 2 ablation results support confirmatory claims about component contribution
- Rung 3 counterfactual claims are rarely warranted from a single experiment program; they require a controlled study

## Category-specific weight

| Category | Analysis center of mass |
|---|---|
| **basic_research** | EDA + descriptive analysis often carry the main explanatory weight. Result analysis should explain the phenomenon, mechanism, boundary condition, or surprising trace before the parent workflow writes any claim. |
| **applied_research** | Result analysis should explain how the practical objective interacted with method, data, evaluator, conditions, and constraints to produce the observed outcome. |
| **experimental_development** | Result analysis should explain the system/process behavior: acceptance-test shape, performance distribution, failure modes, resource contention, and interaction effects. Failure-mode catalog is often the deliverable, not just "it works". |

## Where artifacts live

| Artifact | Where |
|---|---|
| EDA notebooks (before plan exists) | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/notebooks/eda_<n>.ipynb` once a derived hypothesis exists; if EDA precedes a hypothesis, record material in `observations.md` and `analyses.md` first |
| Result-analysis notebooks (after runs) | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/notebooks/analysis_<n>.ipynb` |
| Diagnostic plots used in reports | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/reports/<id>/figures/` (copy/regenerate, not symlink — reports are self-contained snapshots) |
| Raw outputs analyzed | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/runs/<run_id>/outputs/` |
| Intermediate EDA/result-analysis evidence | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/runs/<run_id>/intermediate/` |
| Run manifest and logs | `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/runs/<run_id>/run_manifest.json`, `logs/stdout.log`, `logs/stderr.log` |
| Analysis summary that informs the plan | `observations.md` + `analyses.md` + hypothesis plan Methodology section |

## Common failures

- **Treating analysis as optional.** Skipping result analysis and going directly from "the experiment ran" to "the method works" without explaining why the result happened.
- **Print-only analysis.** A script that prints metrics and exits has produced no durable artifact; stdout is not evidence after the terminal scrollback is gone.
- **Observation/claim conflation.** Writing "the method is more stable" when the actual observation is "loss did not spike on this run." Stage discipline matters.
- **Endless analysis without an explanatory target.** Running analysis branch after branch without tying each branch to a concrete result feature. Stop at depth-to-explain-the-result.
- **HARKing from EDA.** Finding a pattern during EDA and writing the plan as if you had predicted it. Either commit to confirmatory mode on independent data, or label the work exploratory.
- **Diagnostic-as-causal.** Citing a correlation plot (Rung 1) as evidence for a causal/counterfactual claim (Rung 3). Requires ablation or controlled intervention.
- **Single-run analysis on stochastic outputs.** Drawing conclusions from one seed when results are seed-dependent. Use multiple seeds or replications for claim-bearing stochastic comparisons.
- **Skipping slice / subgroup analysis.** Reporting only aggregate metrics when the claim covers distinct subgroups. Hides failure modes that matter.
- **Cherry-picking the favorable analysis.** Doing many analyses, reporting only the supportive ones. This is selective reporting — disclose ALL analyses run, even those that did not support the claim.

## Sources

- [Tukey (1977) — Exploratory Data Analysis](https://www.consoleflare.com/blog/wp-content/uploads/2022/09/Exploratory-Data-Analysis-1977-John-Tukey.pdf) — foundation of EDA discipline
- [Wickham — R for Data Science Ch. 10 (EDA)](https://r4ds.hadley.nz/EDA.html) — modern EDA pipeline
- [Wickham — Tidy Data](https://vita.had.co.nz/papers/tidy-data.pdf) — data shape discipline
- [Kapoor & Narayanan (2023) — Leakage and the reproducibility crisis](https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9) — 8 leakage types, 294 affected papers
- [Mitchell et al. (2019) — Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) — disclosure checklist
- [Gebru et al. (2021) — Datasheets for Datasets](https://cacm.acm.org/research/datasheets-for-datasets/) — dataset disclosure
- [Ribeiro et al. (2020) — CheckList: Beyond Accuracy](https://aclanthology.org/2020.acl-main.442.pdf) — slice-based evaluation
- [Guo et al. (2017) — On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf) — calibration standard
- [Bouthillier et al. (2021) — Accounting for variance in machine learning benchmarks](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf) — variance protocol
- [Hendrycks robustness benchmarks](https://danhendrycks.com/robustness/); [Taori et al. NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/file/d8330f857a17c53d217014ee776bfd50-Paper.pdf) — perturbation probes
- [Lipton & Steinhardt — Troubling Trends in ML Scholarship](https://queue.acm.org/detail.cfm?id=3328534) — ablation as standard
- [Ng CS230 Section 8 — Error analysis](https://cs230.stanford.edu/section/8/)
- [Gelman & Loken — Garden of forking paths](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf) — implicit multiple-testing
- [Gelman et al. (2020) — Bayesian Workflow](https://arxiv.org/abs/2011.01808) — model checking, model understanding, and workflow troubleshooting
- [Machamer, Darden, and Craver (2000) — Thinking About Mechanisms](https://mechanism.ucsd.edu/bill/teaching/w10/machamer.darden.craver.pdf) — mechanism as organized entities and activities
- [Zeller (2002) — Isolating Cause-Effect Chains from Computer Programs](https://www.st.cs.uni-saarland.de/papers/fse2002/p201-zeller.pdf) — cause-effect tracing through state differences
- [Mytkowicz et al. (2009) — Producing Wrong Data Without Doing Anything Obviously Wrong](https://sape.inf.usi.ch/publications/asplos09) — systems measurement bias
- [Curtsinger & Berger (2015) — Coz: Finding Code that Counts with Causal Profiling](https://arxiv.org/abs/1608.03676) — causal profiling for performance explanations
- [Pearl & Bareinboim — Three-Layer Causal Hierarchy](https://causalai.net/r60.pdf) — ladder of causation
- [Toulmin (1958) model](https://en.wikipedia.org/wiki/Stephen_Toulmin#The_Toulmin_model_of_argument) — claim staging foundation
