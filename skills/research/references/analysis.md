# Analysis

## Purpose

Analysis is the activity between **"the experiment ran"** and **"I have a load-bearing claim."** It is exploratory by nature, produces many intermediate artifacts, and has its own discipline distinct from planning, execution, and claim-recording.

Two flavors:

- **EDA (Exploratory Data Analysis)** — done before or during plan design, to understand what the data actually contains before committing to a plan
- **Result analysis** — done after experiments run, to interpret outputs and decide what (if anything) becomes a claim

Both have well-established methodology. The skill enforces structure for claims (see `claim_structure.md`) and decisions (see `iteration_loop.md`), but the analysis step that produces those claims has been left implicit until now. This reference fills that gap.

## EDA standard pass

The modern EDA pipeline derives from Tukey's *Exploratory Data Analysis* (1977) and Wickham's tidy-data restatement. The common core across authoritative sources:

1. **Tidy / shape check** — every variable a column, every observation a row. If the data is not in this shape, reshape before anything else ([Wickham, *Tidy Data*](https://vita.had.co.nz/papers/tidy-data.pdf))
2. **Per-variable distribution + missingness** — histogram, summary statistics resistant to skew/heavy tails (median + IQR, not just mean + SD per [Tukey 1977](https://www.consoleflare.com/blog/wp-content/uploads/2022/09/Exploratory-Data-Analysis-1977-John-Tukey.pdf))
3. **Outlier / re-expression decision** — identify outliers, decide whether to transform (log, Box-Cox), winsorize, or drop. Decision recorded in plan
4. **Pairwise covariation** — scatter / correlation / cross-tabs between variables of interest, before any model
5. **Class balance + temporal/group splits** — if the data has classes or groups, check imbalance. If temporal, check distribution shift across time
6. **Leakage probe** — actively look for train-test contamination, target proxies, future-information leak. [Kapoor & Narayanan 2023](https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9) catalogue 8 leakage types across 294 affected papers. This is non-optional for any claim-bearing ML work
7. **Time-series additions** — for temporal data: stationarity (visual run-sequence plot, Augmented Dickey-Fuller), autocorrelation (ACF/PACF). See `skills/quant-research/references/shared/time_series_validation.md` for design implications

The output of EDA is a **revised understanding of the variable space** that informs the Plan section of `plans/<id>.md`. Findings that look like results should be treated as exploratory and not claimed as confirmatory — see depth stop conditions below.

## Result analysis — claim disclosure floor

After experiments run, before a load-bearing claim is recorded, the result analysis must include a level of disclosure matched to the claim type. For ML/quant method claims, synthesising [Mitchell et al. 2019 Model Cards](https://arxiv.org/abs/1810.03993), [Gebru et al. 2021 Datasheets](https://cacm.acm.org/research/datasheets-for-datasets/), [Bouthillier et al. 2021 MLSys](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf), [Ribeiro et al. 2020 CheckList](https://aclanthology.org/2020.acl-main.442.pdf), and [Guo et al. 2017 calibration](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf), this is the floor:

| Disclosure | Required for | Standard reference |
|---|---|---|
| **Leakage probe passed** | Any claim-bearing ML result | Kapoor & Narayanan 2023 |
| **≥3 seeds with reported variance** | Any performance comparison claim | Bouthillier et al. 2021 |
| **Ablation of each claimed-novel component** | Any "method X works because of Y" claim | [Lipton & Steinhardt — Troubling Trends](https://queue.acm.org/detail.cfm?id=3328534) |
| **Slice / subgroup evaluation on standard axes** | Any claim that generalizes across populations | Ribeiro et al. 2020; Mitchell 2019 Sec. *Quantitative Analyses* |
| **Calibration check** (reliability diagram / ECE) | When confidence scores feed downstream decisions | Guo et al. 2017 |
| **Perturbation / robustness probe** | Any ML/quant claim of practical applicability | [Hendrycks robustness](https://danhendrycks.com/robustness/); [Taori et al. NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/file/d8330f857a17c53d217014ee776bfd50-Paper.pdf) |
| **Error analysis on a sample of failures** | Any claim that needs a mechanism | [Ng CS230 Section 8](https://cs230.stanford.edu/section/8/) |

Below the applicable floor, the result remains an exploratory observation, not a claim-bearing conclusion. If an applied-research plan declares `mode: confirmatory` but skips applicable items for its claim type, the missing analysis must be completed before promotion to a load-bearing claim, state-changing decision, or report.

For non-ML quantitative research, the same principle adapts:

- "Leakage" → information that should not have been available at the time of measurement
- "Slices" → the natural subgroups in your data (regimes, populations, conditions)
- "Calibration" → does your uncertainty quantification match observed frequencies
- "Perturbation" → robustness to changes in parameters, sampling, initial conditions
- "Ablation" → component-wise contribution analysis
- "Variance" → seed / replication / repetition variability

For stochastic systems, do not treat a single fixed seed as reproducibility. Report seed count, dispersion, and failed seeds when those affect the claim. A fixed seed is useful for debugging and audit, but the claim is supported by the distribution of outcomes.

## Analysis depth — when is it enough?

Three orthogonal stop criteria from the methodology literature:

### 1. Tukey's compromise: "do enough to see if there's something to see"

EDA is pre-confirmatory. The stop condition is **"a hypothesis worth testing has emerged"** or **"the variable space is now understood well enough to plan an experiment"** — NOT "all questions are answered." For EDA, going further when no new structure is emerging is wasted effort.

### 2. Depth-to-defend-the-claim

The Gelman & Loken "garden of forking paths" result: even without intentional p-hacking, every analytic branch beyond the claim inflates implicit multiple-testing error ([Gelman & Loken](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)). Practical consequence: **analysis should be scoped to the specific claim being made.** Branches beyond that scope are not "extra evidence"; they are exploratory work that should be labeled as such or preregistered separately.

If you find yourself running analysis #15 because you have not yet found anything significant, you have crossed from analysis into HARKing. Stop, record what you found, and either close the claim as exploratory or commit to a confirmatory preregistration on independent data.

### 3. Disclosure floor reached

For load-bearing claims, the applicable floor above is the minimum. For ML/quant method claims this may include leakage probe, variance, ablation, slice, calibration, perturbation, and error analysis. For other applied claims, use the analogous checks needed to rule out plausible alternatives and support the stated objective. Once the floor is reached AND no required item shows a failure, the claim is defensible. Below the floor, the claim is exploratory regardless of effect size.

### Composite stop rule

```
Analyzing for: EDA / exploratory mapping?
  Stop when: new structure is no longer emerging.

Analyzing for: load-bearing claim?
  Stop when: disclosure floor is met AND no item above showed a failure that
             would invalidate the claim.
  Continue beyond floor only if: a new alternative explanation appeared
             that requires investigation.

Analyzing for: terminal_kill?
  Stop when: each repairable cause (config, data, scope, dependency) has been
             ruled out with evidence.
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

Observations go into `plans/<id>.md` Observations section or into notebooks. They do not need claim_structure formatting.

### Stage 2: Interpretation

An explanation or mechanism proposed for the observation. Still preliminary — alternatives remain.

- "The divergence at epoch 12 suggests the peak learning rate after warmup exceeds the model's stability threshold at this batch size."
- "The 0.18 perplexity improvement may come from the sparse-attention variant OR from the 1.3% increase in active FLOPs."

Interpretations are draft claims. They appear in plan narrative (Methodology / Observations sections) but are not yet load-bearing.

### Stage 3: Claim

A load-bearing assertion, structured per `claim_structure.md`. Has evidence backing, alternatives explicitly listed, conditions stated. The agent has done the work to defend it.

The transition from interpretation to claim is where the disclosure floor applies. An interpretation becomes a claim only when:

- The evidence is anchored to specific artifacts (file:line, run, value)
- Alternative explanations have been actively considered (and listed if not excluded)
- The conditions under which the claim holds are stated precisely
- Exactly one fresh research-review subagent has recorded `PASS` for both analysis sufficiency and result reliability in `plans/<id>.md` Research review section

### Pearl's Ladder applies

[Pearl's Ladder of Causation](https://causalai.net/r60.pdf) sets a hard constraint: **you cannot answer a higher-rung question with lower-rung evidence.**

- **Rung 1 (Association)**: A diagnostic plot showing correlation between two variables
- **Rung 2 (Intervention)**: An ablation result — what happens when component X is removed
- **Rung 3 (Counterfactual)**: A claim about why something failed — "if we had used warmup=40 epochs, it would have converged"

A diagnostic plot is not sufficient warrant for a causal/counterfactual claim. The disciplined progression: observe → ablate → make a Rung 2 claim. Counterfactual (Rung 3) claims require additional causal structure (controlled intervention isolating the alleged mechanism).

In the iteration_loop, this maps to:
- Rung 1 observations may prompt REFINE (narrow the question to test a candidate cause)
- Rung 2 ablation results support confirmatory claims about component contribution
- Rung 3 counterfactual claims are rarely warranted from a single experiment program; they require a controlled study

## Category-specific weight

| Category | Analysis center of mass |
|---|---|
| **basic_research** | EDA + descriptive analysis often carry the main evidential weight. Observations are the primary output. Promotion to claim requires stated conditions, alternatives, and variance/replication when relevant. Mechanism description leans on Pearl Rung 2 evidence (controlled variation) |
| **applied_research** | General applied claims: evidence tied to the practical objective, stated conditions, plausible alternatives, and limitations. ML/quant method claims: apply the relevant floor for leakage, stochastic variance, comparator fairness, ablation for component-causality claims, slice/calibration/robustness/error analysis when applicable |
| **experimental_development** | EDA = profiling the input space. Result analysis = acceptance test deep-dive + performance distribution characterization. Variance across runs is required. Failure-mode catalog is the deliverable, not just "it works" |

## Where artifacts live

| Artifact | Where |
|---|---|
| EDA notebooks (before plan exists) | `experiments/<plan>/notebooks/eda_<n>.ipynb` once plan is created. If EDA precedes any plan, create a basic_research exploratory plan first — that is what EDA is |
| Result-analysis notebooks (after runs) | `experiments/<plan>/notebooks/analysis_<n>.ipynb` |
| Diagnostic plots used in reports | `reports/<id>/figures/` (copy/regenerate, not symlink — reports are self-contained snapshots) |
| Raw outputs analyzed | `experiments/<plan>/runs/<run_id>/outputs/` |
| Analysis summary that informs the plan | `plans/<id>.md` Observations section + Methodology section |

## Common failures

- **Treating analysis as optional.** Skipping result analysis and going directly from "the experiment ran" to "the method works" — missing the disclosure floor.
- **Observation/claim conflation.** Writing "the method is more stable" when the actual observation is "loss did not spike on this run." Stage discipline matters.
- **Endless analysis without claim.** Running analysis branch after branch without committing to a claim. Eventually some branch will look favorable; that is HARKing. Stop at the depth-to-defend-the-claim.
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
- [Pearl & Bareinboim — Three-Layer Causal Hierarchy](https://causalai.net/r60.pdf) — ladder of causation
- [Toulmin (1958) model](https://en.wikipedia.org/wiki/Stephen_Toulmin#The_Toulmin_model_of_argument) — claim staging foundation
