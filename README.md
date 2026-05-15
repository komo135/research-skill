# research-skill

A Claude Code and Codex plugin providing two skills for **agent-driven R&D**:

- **`research`** — protocol skill for R&D work across the three Frascati categories: basic research (understanding phenomena, building baselines), applied research (achieving measurable objectives), and experimental development (building working systems). Enforces vocabulary, plan/claim structure, iteration discipline, analysis methodology, and human-readable reports.
- **`quant-research`** — domain extension layered on `research` for time-series and statistically rigorous quantitative R&D. Adds methodology for time-series cross-validation, multiple-testing corrections, leakage detection, and statistical robustness.

The core rule: **research-level reproducibility (someone can re-implement from your description) is enforced; experiment-level replicability (someone can rerun your exact code) is the agent's discretion.** This separation, following [Drummond (2009)](https://cogprints.org/7691/7/icmle09.pdf) and [Goodman et al. (2016)](https://www.science.org/doi/10.1126/scitranslmed.aaf5027), keeps agents focused on doing good research rather than on producing perfect env.lock files. Reports record material conditions, not environment locks: data identity, split dates, evaluation protocol, major model/tool versions, hardware class, external API/model version, or collection date only when those conditions affect interpretation.

## Who this is for

This plugin is for agents doing R&D work where:

- A claim needs to survive scrutiny — alternatives addressed, conditions stated, evidence cited
- Multiple sessions or agents will share project state — needs interoperable vocabulary
- A human will read the output and make a decision — needs Z39.18-style structured reports with real figures

Examples of work that triggers the skill:

- ML method research (architecture, training-procedure, evaluation studies)
- Phenomenon investigations in computational science (chaos systems, simulation experiments)
- Reference-baseline building (creating datasets, metrics, reference implementations for others to compare against)
- System/prototype development with quantitative acceptance criteria
- Quantitative-rigor extensions (time-series statistical evaluation, multiple-testing-aware claims)

It is NOT a backtest engine, experiment tracker, notebook framework, or env-lock manager. It is a **protocol layer** that enforces structure on the narrative — plans, claims, decisions, reports — while leaving the implementation to the agent.

## Core design (v2.0.3)

### R&D categories (Frascati 2015)

Every plan declares one of:

| Category | When | Default plan mode | Report shape |
|---|---|---|---|
| `basic_research` | Phenomenon investigation, baseline building, failure-mode catalog | `exploratory` | Phenomenon → Mechanism → Refined question |
| `applied_research` | Method achieving a target metric vs baselines | `confirmatory` | Method → Experiments → Results → Ablations |
| `experimental_development` | Working artifact + performance | `milestone` | System → Performance → Limits |

Categories are not a one-way pipeline ([Kline & Rosenberg 1986](https://fenix.iseg.ulisboa.pt/downloadFile/1407508027548318/Kline%20and%20Rosenberg%20(1986)%20An%20overview%20of%20innovation.pdf); [Stokes 1997](https://www.brookings.edu/books/pasteurs-quadrant/)). Cycling between them is normal.

### Plan-Execute-Analyze-Compare-Report cycle

```
1. new_plan.py creates plans/{id}_{slug}.md (mode-specific template)
2. Write Question / Objective and the Divergence checkpoint.
3. Write Plan section. git commit. (Plan is time-anchored.)
4. Execute. Save artifacts under experiments/{plan}/runs/{run_id}/.
5. ANALYZE — apply the discipline in references/analysis.md.
6. Write Actual section + Planned-vs-Actual comparison.
7. Dispatch exactly one research-review subagent to evaluate analysis sufficiency and result reliability.
8. Record load-bearing claims using the Toulmin-derived structure.
9. Pick one of 5 iteration branches: NEXT_STEP / REFINE / ADJACENT / PARK / CLOSE.
10. If human-facing, draft a report.
```

### Divergence checkpoint

Every plan now records a pre-execution checkpoint before committing to a route:

- Approach portfolio: the chosen approach plus meaningfully different alternatives
- Anchoring audit: prior results, prior approaches, or convenient datasets being imported as assumptions
- Novelty / differentiation thesis: whether the contribution is a new method, evaluation, data, system, replication, or baseline strengthening
- Disconfirming evidence: observations that would trigger REFINE / ADJACENT / PARK / CLOSE
- Commitment decision: why this route is selected now, and what skipped divergence limits later claims

This keeps agents from silently accepting "just improve last time's best approach" as a complete research plan.

### Research review

Before a result becomes a load-bearing claim, state-changing decision (`REFINE`, `ADJACENT`, `PARK`, or `CLOSE`), or report, the agent dispatches exactly one fresh research-review subagent. That reviewer must record a verdict for both:

- Analysis sufficiency: whether the analysis is adequate for the conclusion, because weak analysis can directly produce a wrong close-out.
- Result reliability: whether the result is trustworthy given the approach, research procedure, data handling, baselines, controls, robustness checks, and plan deviations.

The review records `PASS`, `REWORK`, or `INVALID` for each judgment in the plan's Research review section. Only two `PASS` judgments allow promotion. `REWORK` requires the named analysis, repair, or rerun before any claim, decision, or report; `INVALID` means the affected result is not evidence until the distorted work is redone.

### Claim structure (Toulmin-derived, no numeric ladder)

```yaml
- claim: (specific assertion with metric, magnitude, conditions)
  evidence: (file:line / value / artifact / citation)
  alternatives_not_excluded: [...]    # empty list claims exhaustion
  conditions_tested: (ranges, datasets, parameters)
  conditions_not_tested: [...]        # empty list claims full coverage
```

Strength is read off the contents of `alternatives_not_excluded` and `conditions_not_tested`. There is no A0-A5, no TRL, no GRADE — those single-number ladders conflate causal strength, scope, and replication into one digit and invite overclaim by self-rating.

### Analysis discipline (EDA + result analysis + depth stops)

`references/analysis.md` provides:

- The modern EDA standard pass (Tukey 1977 + Wickham): tidy → distribution → covariation → leakage probe
- The claim disclosure floor for ML: leakage / ≥3 seeds / ablation / slice / calibration / perturbation / error analysis (per [Mitchell et al. 2019 Model Cards](https://arxiv.org/abs/1810.03993), [Bouthillier 2021](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf), [Ribeiro 2020 CheckList](https://aclanthology.org/2020.acl-main.442.pdf))
- Depth stop conditions (Tukey's compromise, depth-to-defend-claim, disclosure floor)
- Observation → Interpretation → Claim staging with [Pearl's Ladder of Causation](https://causalai.net/r60.pdf)
- HARKing prevention via [Gelman-Loken Garden of Forking Paths](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)

For stochastic work, seed variability matters more than a single fixed seed. The skill asks agents to report seed count, dispersion, and failures when a claim depends on stochastic execution. Claim-to-artifact consistency checks are evidence-integrity checks: reported values must match the cited artifacts, but that is an audit of evidence honesty rather than a replacement for methods reproducibility.

### Reports for humans

Z39.18-derived, lightweight structure with required sections (Summary / Background / Methods & Conditions / Results / Limitations / Next action). Figures must actually exist — `scripts/check_report.py` verifies references resolve. Reports cite the plan for full re-implementation detail rather than duplicating Methods content.

## Repository Layout

```
research-skill/
├── .agents/plugins/marketplace.json
├── .claude-plugin/{plugin.json,marketplace.json}
├── .codex-plugin/plugin.json
├── skills/
│   ├── research/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── categories/{basic_research,applied_research,experimental_development}.md
│   │   │   ├── analysis.md
│   │   │   ├── claim_structure.md
│   │   │   ├── iteration_loop.md
│   │   │   ├── rd_plan.md
│   │   │   ├── report_format.md
│   │   │   └── literature_review.md
│   │   ├── assets/{project,plan,report}/*.template
│   │   └── scripts/{new_project,new_plan,new_run,check_claims,check_report,draft_report}.py
│   └── quant-research/
│       ├── SKILL.md
│       ├── references/shared/
│       └── scripts/
├── README.md
└── LICENSE
```

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

Enable in `~/.codex/config.toml`:

```toml
[plugins."research@research-skill"]
enabled = true
```

## Project layout the skill produces

When an agent runs `scripts/new_project.py` to initialize an R&D project:

```
{project-root}/
├── README.md, project_state.md, decisions.md
├── plans/{id}_{slug}.md            # research narrative (plan + actual + claims + decision)
├── literature/{papers.md,differentiation.md}
├── lib/                             # shared curated code (tests required)
├── experiments/{plan}/              # per-plan isolation
│   ├── code/ configs/ notebooks/
│   └── runs/{plan}__{n}__seed{N}/   # raw artifacts (no required schema)
├── data/{raw,processed}/
└── reports/{id}_{slug}/             # human-facing snapshots
    ├── report.md
    ├── figures/ tables/
```

`lib/` is curated and shared; `experiments/{plan}/code/` is the plan's free zone. Cross-plan imports are forbidden — promote to `lib/` with a `decisions.md` entry first.

## Bundled scripts

`skills/research/scripts/`:

| script | purpose |
|---|---|
| `new_project.py` | Initialize project directory with canonical layout |
| `new_plan.py` | Create a plan from mode-specific template, capture git SHA |
| `new_run.py` | Create a run directory with consistent naming |
| `check_claims.py` | Verify claim record structure (5 required fields, vagueness heuristics) |
| `check_report.py` | Verify report contract (figures resolve, required sections, non-placeholder) |
| `draft_report.py` | Initialize a report directory from a plan |

`skills/quant-research/scripts/`:

| script | purpose |
|---|---|
| `purged_kfold.py` | Purged k-fold CV for time-series with overlapping labels |
| `cpcv.py` | Combinatorial Purged Cross-Validation |
| `walk_forward.py` | Walk-forward time-series validation |
| `multiple_testing.py` | Bonferroni / Benjamini-Hochberg / Romano-Wolf corrections |
| `leakage_check.py` | Detect train/test feature leakage and look-ahead bias |
| `sanity_checks.py` | Standard pre-claim sanity tests |
| `sensitivity_grid.py` | Parameter sensitivity grid for robustness battery |

## Status

**Version 2.0.3** — clarifies methods reproducibility vs provenance/evidence-integrity and fixes multiple-testing correction behavior. Not backward compatible with v1.x.

<details>
<summary>Changelog</summary>

### v2.0.3 (current) — reproducibility vocabulary and multiple-testing fixes

Separates methods reproducibility from audit provenance and evidence-integrity checks, and fixes multiple-testing correction behavior in the quant-research extension.

**Changed**

- Reports and plans now describe material conditions that affect interpretation, not environment locks or commit hashes in prose.
- Provenance pointers and claim-to-artifact checks are framed as audit/evidence-integrity controls rather than sources of methods reproducibility.
- Fixed seeds are treated as debugging/audit aids; stochastic claims should report seed count, dispersion, and failed seeds when material.

**Fixed**

- Holm adjusted p-values are now monotone step-down values.
- Bonferroni, Holm, and Benjamini-Hochberg reject adjusted p-values equal to `alpha`.

### v2.0.2 — category boundary clarification

Clarifies how agents choose Frascati R&D categories without changing plugin identity.

**Changed**

- R&D categories are chosen by a plan's primary purpose, intended use, expected output, and uncertainty type, not by source or origin alone.
- `Innovation` is not treated as a primary R&D category label; publication-time contribution is separated from later adoption, diffusion, or social value.
- Project/program category mixing remains valid, while each plan still declares exactly one category and one mode.
- Experimental-development guidance now directs load-bearing methods claims to an `ADJACENT` applied-research plan with `confirmatory` mode.

### v2.0.1 — divergence and review gate hardening

Strengthens v2 research discipline without changing plugin identity.

**Added / changed**

- Required Divergence checkpoint before execution: approach portfolio, anchoring audit, novelty/differentiation thesis, disconfirming evidence, and commitment decision.
- Required single research-review subagent before load-bearing claims, state-changing decisions, or reports.
- Research review verdicts are `PASS` / `REWORK` / `INVALID`; only `PASS` + `PASS` permits promotion.
- `REWORK` requires named reanalysis, repair, or rerun before any claim, decision, or report.
- `INVALID` makes affected results unusable as evidence until repair, rerun, or research-plan redo.
- Quant time-series test-set reuse is treated as a reliability failure requiring protocol reopening and fresh evaluation, not a weaker writeup.

### v2.0.0 — agent-driven R&D redesign

Complete redesign. No backward compatibility with v1.x.

**Added**

- 3 Frascati categories first-class: `basic_research`, `applied_research`, `experimental_development`
- Plan modes: `exploratory`, `confirmatory`, `milestone`
- Iteration FSA with 5 explicit branches: `NEXT_STEP` / `REFINE` / `ADJACENT` / `PARK` / `CLOSE`
- Divergence checkpoint before execution to expose alternatives, anchoring risk, novelty basis, and disconfirming evidence before committing to a plan
- Single research-review subagent before claim/decision/report promotion, covering analysis sufficiency and result reliability
- Toulmin-derived claim structure (5 required fields, no numeric ladder)
- `references/analysis.md` covering EDA, result analysis, depth stop conditions, and Observation→Interpretation→Claim staging — backed by Tukey 1977, Wickham, Mitchell 2019 Model Cards, Gebru 2021 Datasheets, Ribeiro 2020 CheckList, Guo 2017 calibration, Bouthillier 2021 variance, Pearl Ladder of Causation, Gelman-Loken forking paths, Toulmin 1958
- Lightweight Amendment pattern: `REFINE` appends an Amendment rather than rewriting the Plan
- Plan-canonical Methods: report's Methods section summarizes and cites the plan rather than duplicating
- `scripts/check_report.py` verifying figure references resolve and required sections exist
- `lib/` vs `experiments/{plan}/code/` separation with explicit promotion contract
- Quant-research repositioned as time-series/statistical-rigor extension over `research`, applicable beyond finance

**Removed**

- Pure Research workstream (PR/FAQ, IMRAD, explanation_ledger) — Amazon-style business artifact not aligned with Frascati basic-research practice
- A0-A5 analysis depth ladder — homemade, not standard, conflated dimensions
- L2/L3 report classification — non-standard vocabulary
- Separate `prereg/` directory — preregistration internalized into `plans/{id}.md` with git as time-anchor
- Heavy `review/` pipeline — replaced by `check_claims.py` + `check_report.py` plus the iteration_loop FSA
- Finance-specific quant-research surface (Sharpe-derivative scripts, portfolio construction, trading-specific references)
- Experiment-level replicability infrastructure (env locks, commit pinning, seed databases) — explicitly the agent's discretion, not skill-enforced. When present, these are provenance or variability logs, not substitutes for methods reproducibility.

**Design rationale**

This release is the result of a TDD pass on the skill: pressure scenarios run against baseline (no skill) revealed systemic gaps in vocabulary use, claim structuring, and state-file maintenance; the new skill closes those gaps with minimum machinery. External methodology survey informed every non-trivial design choice — see citations throughout `references/`.

### v1.1.10 and earlier

See git history for the prior workstream-based design (`pure_research`, `review/`, `A0-A5`, etc.) — replaced wholesale in v2.0.0.

</details>

## License

MIT. See [LICENSE](./LICENSE).
