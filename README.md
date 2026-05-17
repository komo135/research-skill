# research-skill

A Claude Code and Codex plugin providing four skills for **agent-driven R&D**:

- **`research`** — protocol skill for R&D work across the three Frascati categories: basic research (new knowledge about underlying foundations without a particular application in view), applied research (new knowledge directed toward a specific practical aim or objective), and experimental development (new or improved products/processes plus additional knowledge). Enforces vocabulary, plan/claim structure, iteration discipline, analysis methodology, and human-readable reports.
- **`research-plan-review`** — independent plan-review skill used before execution. It starts from a plan path only and reviews the research design: mechanism hypothesis or principle, prediction or expected output, discriminating test, controls/comparators or limiting cases, evidence route, and execution blockers.
- **`research-result-analysis`** — independent result-analysis skill used by a fresh separate-context result-analysis subagent. It starts from a plan path only, reconstructs evidence from referenced artifacts, and explains what happened and why through candidate explanations, evidence for/against, procedure/artifact explanations, live alternatives, and discriminating next analyses without writing final claims or decisions.
- **`quant-research`** — domain extension layered on `research` for time-series and statistically rigorous quantitative R&D. Adds methodology for time-series cross-validation, multiple-testing corrections, leakage detection, and statistical robustness.

The core rule: **research-level reproducibility (someone can re-implement from your description) is enforced; experiment-level replicability (someone can rerun your exact code) is the agent's discretion.** This separation, following [Drummond (2009)](https://cogprints.org/7691/7/icmle09.pdf) and [Goodman et al. (2016)](https://www.science.org/doi/10.1126/scitranslmed.aaf5027), keeps agents focused on doing good research rather than on producing perfect env.lock files. Reports record material conditions, not environment locks: data identity, split dates, evaluation protocol, major model/tool versions, hardware class, external API/model version, or collection date only when those conditions affect interpretation. Research scripts still need evidence: stdout is not evidence, so completed runs keep a manifest with `status: completed`, logs, and at least one manifest-listed durable artifact.

## Who this is for

This plugin is for agents doing R&D work where:

- A claim needs to survive scrutiny — alternatives addressed, conditions stated, evidence cited
- Multiple sessions or agents will share project state — needs interoperable vocabulary
- A human will read the output and make a decision — needs Z39.18-style structured reports with real figures

Examples of work that triggers the skill:

- ML method research (architecture, training-procedure, evaluation studies)
- Phenomenon investigations in computational science (chaos systems, simulation experiments)
- Foundational measurement or resource characterization (datasets, metrics, reference implementations, or other reusable research objects)
- System/prototype development with quantitative acceptance criteria
- Quantitative-rigor extensions (time-series statistical evaluation, multiple-testing-aware claims)

It is NOT a backtest engine, experiment tracker, notebook framework, or env-lock manager. It is a **protocol layer** that enforces structure on the narrative — plans, claims, decisions, reports — while leaving the implementation to the agent.

## Core design (v2.6.2)

### R&D categories (Frascati 2015)

Every plan declares one of:

Agent-side R&D eligibility is a lightweight research-recording check. Work should be novel, creative, uncertain, systematic, and transferable and/or reproducible enough that another agent can understand and reuse the record.

| Category | When | Default plan mode | Report shape |
|---|---|---|---|
| `basic_research` | New knowledge about underlying foundations, without a particular application or use in view | `exploratory` | Phenomenon → Mechanism → Refined question |
| `applied_research` | New knowledge directed toward a specific practical aim or objective | `confirmatory` | Objective → Method/procedure → Evidence → Limits |
| `experimental_development` | Systematic work producing additional knowledge while creating or improving a product/process | `milestone` | System/process → Performance → Limits |

Categories are not a one-way pipeline ([Kline & Rosenberg 1986](https://fenix.iseg.ulisboa.pt/downloadFile/1407508027548318/Kline%20and%20Rosenberg%20(1986)%20An%20overview%20of%20innovation.pdf); [Stokes 1997](https://www.brookings.edu/books/pasteurs-quadrant/)). Cycling between them is normal.

Plan modes are `exploratory`, `confirmatory`, `milestone`, and `theoretical`. Theoretical mode is for derivational work where axioms, definitions, and limiting-case checks carry the evidence burden; it is a plan/report mode, not a fourth R&D category.

### Plan-Plan review-Execution-Result analysis-Claim cycle

```
1. new_plan.py creates plans/{id}_{slug}.md (mode-specific template)
2. Write Question / Objective. If ideating, write the Research ideation Idea portfolio before prior-work grounding.
3. For ideation work, run assumption audit before hypothesis synthesis; use iterative ideation only when its executable-evaluator preconditions hold.
4. Run a plan-scoped literature survey, then write Prior-work grounding and the Divergence checkpoint before the Plan section.
5. Write Plan section.
6. Plan review — dispatch a fresh separate-context plan-review subagent using `research-plan-review` and pass only the plan path. Repair blockers before execution.
7. git commit. (Plan plus Plan review are time-anchored.)
8. Execute. Save artifacts under experiments/{plan}/runs/{run_id}/, including run_manifest.json, logs, and at least one manifest-listed non-log durable artifact. Record a mid-execution literature update if an unfamiliar method, unexpected result, new comparator, contradiction with prior work, or missing-baseline signal appears.
9. Write Actual section + Planned-vs-Actual comparison.
10. Result analysis — dispatch a fresh separate-context result-analysis subagent using `research-result-analysis` and pass only the plan path. The subagent reconstructs evidence and decomposes why the result happened.
11. Claim — record only the load-bearing claims supported by the evidence and alternatives using the Toulmin-derived structure.
12. Pick one of 5 iteration branches: NEXT_STEP / REFINE / ADJACENT / PARK / CLOSE.
13. If human-facing, draft a report.
```

The timing boundary is explicit: Plan and Plan review record pre-result commitments such as predictions, measures, controls/comparators, planned discriminating test, evidence route, artifacts, and stop / branch criteria. They do not explain why an unobserved result happened. Result analysis records post-result explanations only after evidence exists.

### Prior-work grounding

Every new plan records first-class prior-work grounding before the Plan section. The required depth is bounded but sufficient: enough to support the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol when applicable, and known limitations. It is not optional just because no novelty claim is made.

Prior-work grounding starts with a plan-scoped literature survey before the Plan section. The plan records survey evidence: search date, queries or source names, selection rationale, negative findings, and any retrieval-unavailable constraint. Retrieval-unavailable is not a survey bypass; it needs attempted source/tool, failure evidence, and claim-scope narrowing. Unknown prior work is a post-survey constraint, not a reason to skip search.

Projects use `literature/{papers.md,positioning.md}`. `positioning.md` records how the work stands on prior work: grounding, inheritance, control/comparator choice when relevant, known limitations, and claim scope. Differences or novelty can be recorded there when claimed, but novelty is not the default purpose.

Plans also record a citation-use map: each cited work must name how it is used in the plan, such as question framing, mechanism prior, baseline, comparator, metric, evaluation protocol, theoretical foundation, limitation, contradictory evidence, or claim-scope boundary. The literature files keep the project-level role union; the plan's citation-use map is the plan-specific source of truth.

Comprehensive literature survey is required for strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims. That is separate from the plan-scoped prior-work grounding every plan needs.

### Research ideation

When a user asks for research ideas, research directions, hypothesis candidates, or "what should we try next," the `research` skill uses `references/ideation.md` to create an **Idea portfolio** before prior-work grounding. If anchors are already visible, it writes an anchor-stripped seed brief and an excluded-anchor ledger before raw seed generation. When anchoring risk is high, ideation may dispatch a fresh separate-context hypothesis-generation agent from that brief; the main agent then records intake instead of accepting the output as authority. Raw seeds are not accepted ideas. The portfolio must record substrate ids, hypothesis-generation handoff or a Not-used reason, main-agent intake, generation operators, changed premises, assumption audit, anti-vacuity gate results, blind-spot catalog entries tied to surviving candidates, evaluator feedback, grounded pruning, and information-gain scoring before one candidate can be promoted.

Only one candidate is promoted into a plan. Non-promoted ideas are recorded as `parked / killed / merged` and are not claims.

### Assumption audit and iterative ideation

v2.3.0 adds `references/assumption_audit.md` between observation discovery and hypothesis synthesis. It surfaces background assumptions of the reference model being challenged, separate from the Divergence checkpoint's anchoring audit on imported prior work. The audit records load-bearing assumptions, downstream checks, blind-spot catalog entries tied to candidate mechanisms and claim scope, reference-class forecasts, and named constraints for hypotheses that cannot currently be evaluated.

v2.4.0 adds `references/iterative_ideation.md` for applied and experimental-development plans with an existing executable evaluator. It uses real shell / command-line execution for candidate scoring, explicitly forbids self-simulated fitness, and updates candidates with mutation, crossover, and wildcard variants before grounded pruning.

Executable feedback must persist to run artifacts. A command that only prints a fitness number is not valid evaluator feedback until the run directory contains `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, and a durable artifact such as `outputs/fitness.json`, `tables/fitness.csv`, or an `intermediate/` diagnostic.

### Divergence checkpoint

Every plan now records a pre-execution checkpoint before committing to a route:

- Approach portfolio: the chosen approach plus meaningfully different alternatives
- Anchoring audit: prior results, prior approaches, or convenient datasets being imported as assumptions
- Research positioning: whether the work stands as a new question, mechanism, data, metric, evaluation protocol, method, system, replication, or baseline strengthening
- Disconfirming evidence: observations that would trigger REFINE / ADJACENT / PARK / CLOSE
- Commitment decision: why this route is selected now, and what skipped divergence limits later claims

This keeps agents from silently accepting "just improve last time's best approach" as a complete research plan.

### Plan review subagent

Before execution, the plan-review handoff uses `research-plan-review` and passes only the plan path. The reviewer checks the research design before any results exist: category/mode fit, mechanism hypothesis or principle, prediction or expected output, planned discriminating test, controls/comparators or limiting cases, evidence route, artifact plan, scope, and constraints. It returns `execute_as_written`, `revise_before_execution`, or `block_execution`.

This verdict asymmetry is intentional. Plan review happens before execution, so it may recommend whether the design is informative enough to run. Result analysis happens after evidence exists and before claims / decisions, so it explains what happened and why but does not assess claim readiness, deployment, or iteration decisions.

### Result analysis subagent

The result-analysis handoff uses `skills/research/references/result_analysis_subagent_prompt.md`. The prompt passes only the plan path; the subagent treats the plan as the only starting context and reconstructs necessary evidence from referenced artifacts. Parent-agent summaries, expected conclusions, and private execution notes are not inputs. Missing or ambiguous references are reported as `context_missing`.

The output is a `## Result analysis` section with evidence traced, what happened, candidate explanations, evidence for and against each explanation, procedure/artifact explanations, alternatives still live, and discriminating next analyses. It is not a claim record and not an iteration decision.

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
- The claim disclosure floor for ML/quant method claims: leakage / ≥3 seeds for stochastic comparisons / ablation for component-causality claims / slice / calibration / perturbation / error analysis when applicable (per [Mitchell et al. 2019 Model Cards](https://arxiv.org/abs/1810.03993), [Bouthillier 2021](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf), [Ribeiro 2020 CheckList](https://aclanthology.org/2020.acl-main.442.pdf))
- Depth stop conditions (Tukey's compromise, depth-to-defend-claim, disclosure floor)
- Observation → Interpretation → Claim staging with [Pearl's Ladder of Causation](https://causalai.net/r60.pdf)
- HARKing prevention via [Gelman-Loken Garden of Forking Paths](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)

For stochastic work, seed variability matters more than a single fixed seed. The skill asks agents to report seed count, dispersion, and failures when a claim depends on stochastic execution. Claim-to-artifact consistency checks are evidence-integrity checks: reported values must match the cited artifacts, but that is an audit of evidence honesty rather than a replacement for methods reproducibility.

### Reports for humans

Z39.18-derived, paper-grade report structure with required Summary, Background, Related Work, Methods & Conditions or System description, Results/Observations/Performance, Ablation / Sensitivity, Discussion, Limitations, Next action, and References sections. Sections that do not apply still appear with a short `Not applicable:` rationale. v2.4.0 adds Figure-as-argument guidance and a Statistical reporting minimum for numeric evidence. Figures must actually exist — `scripts/check_report.py` verifies references resolve and rejects numeric outcome sections that omit sample size, variance/dispersion, CI, effect size, significance, or an explicit non-applicability reason. Reports cite the plan for full re-implementation detail rather than duplicating Methods content.

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
│   │   │   ├── ideation.md
│   │   │   ├── iteration_loop.md
│   │   │   ├── result_analysis_subagent_prompt.md
│   │   │   ├── rd_plan.md
│   │   │   ├── report_format.md
│   │   │   └── literature_review.md
│   │   ├── assets/{project,plan,report}/*.template
│   │   └── scripts/{new_project,new_plan,new_run,check_run_artifacts,check_claims,check_report,draft_report}.py
│   ├── research-plan-review/
│   │   └── SKILL.md
│   ├── research-result-analysis/
│   │   ├── SKILL.md
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

After installation the skills are available as `research`, `research-plan-review`, `research-result-analysis`, and `quant-research`.

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
├── literature/{papers.md,positioning.md}
├── lib/                             # shared curated code (tests required)
├── experiments/{plan}/              # per-plan isolation
│   ├── code/ configs/ notebooks/
│   └── runs/{plan}__{n}__seed{N}/   # run_manifest, logs, and durable artifacts
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
| `new_run.py` | Create a run directory with manifest, logs, and artifact folders |
| `check_run_artifacts.py` | Reject print-only runs and verify manifest/logs/non-log artifacts |
| `check_idea_portfolio.py` | Verify Idea portfolio substrate/handoff/intake/operator/anti-vacuity/blind-spot/evaluator-feedback contract |
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

**Version 2.6.2** — clarifies the boundary between pre-result planning commitments and post-result explanations, while keeping prior-work grounding, plan-scoped literature survey evidence, citation-use mapping, independent plan review, explanation-centered result analysis, assumption audit, theoretical mode, paper-grade reports, and statistical reporting minimums.

<details>
<summary>Changelog</summary>

### v2.6.2 (current) — pre-result planning boundary

Clarifies that plans and plan review contain commitments made before results exist, while Result analysis contains explanations made after evidence exists.

**Added / changed**

- Defined pre-result commitments: question/objective, mechanism conjecture or principle, prediction or expected observation, primary measure, controls/comparators, planned discriminating test, evidence route, artifact plan, and stop / branch criteria.
- Defined post-result explanations: what happened, candidate explanations, evidence for/against, procedure / artifact explanations, alternatives still live, and discriminating next analyses.
- Replaced the detailed Result analysis form in plan templates with an explicit post-execution placeholder so agents do not fill why-analysis before results exist.
- Updated Plan review language to check whether a planned discriminating test can separate plausible alternatives without explaining an unobserved result.

### v2.6.1 — plan-scoped literature survey evidence

Makes prior-work grounding first-class in every research plan before execution.

**Added / changed**

- Required Survey evidence before the Plan section: search date, queries/sources, selection rationale, negative findings, and retrieval-unavailable constraints.
- Added a Citation-use map so each cited work states its concrete role in the plan, instead of appearing only in a bibliography.
- Defined `literature/papers.md` and `literature/positioning.md` `Used in plan as` fields as a project-level role union; the plan's Citation-use map is the plan-specific source of truth.
- Made retrieval-unavailable constraints verifiable: attempted source/tool, failure evidence, and claim-scope narrowing are required.
- Added Mid-execution literature updates for unfamiliar methods, unexpected results, new comparators, contradictions, or missing-baseline signals.
- Made missing or merely formal Survey evidence / Citation-use mapping a Plan review blocker.

### v2.6.0 — plan review and explanation-centered result analysis

Splits pre-execution design review and post-execution result analysis into the two mandatory fresh separate-context gates around execution. Ideation can also use a fresh hypothesis-generation handoff, but that output is seed material until main-agent intake, pruning, and plan promotion adjudicate it.

**Added / changed**

- Added `research-plan-review` for plan-path-only review before execution.
- Removed the post-result review gate from the active lifecycle.
- Removed the Codex-specific result-analysis agent definition; result-analysis is now skill / prompt-template driven across agent runtimes.
- Refocused `research-result-analysis` from readiness verdicts to explaining why the result happened: candidate explanations, evidence for/against, procedure/artifact explanations, live alternatives, and discriminating next analyses.
- Kept document checks as regression guards; behavioral quality is validated with pressure scenarios against the skills.
- Reworked ideation so de-anchored hypothesis generation uses an anchor-stripped seed brief, excluded-anchor ledger, optional fresh hypothesis-generation handoff, and explicit main-agent intake.

### v2.5.0 — independent result analysis quality gates

Split result analysis into a dedicated skill and made analysis quality explicitly reviewable in the previous lifecycle.

**Added / changed**

- Added `research-result-analysis` as a separate skill for fresh separate-context analysis from the plan path only.
- Added `skills/research/references/result_analysis_subagent_prompt.md` so the parent research skill passes only the plan path and records the returned `## Result analysis` section before the previous review gate.
- Added readiness verdicts: `ready`, `not_ready`, and `invalid_evidence`; superseded in v2.6.0 by explanation-centered analysis.
- Added an analysis quality gate: artifact-faithful, arithmetically checked, claim-fit checked, depth-calibrated, and reviewable.
- Clarified that readiness is not a release decision and must not be translated into ship, CLOSE, NEXT_STEP, REFINE, ADJACENT, or PARK.

### v2.4.0 — theoretical, iterative, report, and claim additions

Extends the v2 research protocol without adding new R&D categories.

**Added / changed**

- Added `theoretical` plan mode for derivational work using axioms, definitions, and limiting-case checks.
- Replaced raw one-line ideation with a substrate-driven generation contract: substrate ids, generation operators, changed premises, blind-spot entries, anti-vacuity gate, evaluator feedback, and `check_idea_portfolio.py`.
- Added iterative ideation for applied and experimental-development plans with executable evaluators: real shell / command-line execution is mandatory and self-simulated fitness is forbidden.
- Expanded report format with paper-grade Theory / Formulation, Related Work, Ablation / Sensitivity, Discussion, and References sections.
- Added Figure-as-argument guidance and a Statistical reporting minimum for numeric evidence.
- Clarified that theoretical support is a mode/report shape under the existing `basic_research`, `applied_research`, and `experimental_development` categories.

### v2.3.0 — assumption audit for challenged reference models

Adds a pre-synthesis audit for assumptions behind the reference model being challenged.

**Added / changed**

- Added `references/assumption_audit.md` between observation discovery and hypothesis synthesis.
- Distinguished background assumption audit from the Divergence checkpoint's anchoring audit on imported prior work.
- Added load-bearing assumption selection with downstream-check discipline.
- Added blind-spot catalog entries, manual reference-class forecasting, and constraint-naming for hypotheses with no current evaluator.

### v2.2.0 — Frascati definitions and research lifecycle

Clarifies R&D category definitions and makes hypothesis generation explicit.

**Added / changed**

- R&D category definitions now follow OECD Frascati Manual 2015 wording while remaining scoped to agent research work, not corporate activity.
- Added a research lifecycle from `Observation discovery` through `Decision`.
- Added `Observation discovery pass` before hypothesis synthesis, with observation sources including empirical, literature, failure-mode, tension, baseline, and user/problem observations.
- Split prior work into two roles: references can supply observations, then later ground candidates after raw candidates and hypothesis rationales exist.
- Added a hypothesis synthesis chain: source observation, mechanism conjecture, proposed intervention, predicted effect, counter-hypothesis, and minimal disconfirming test.
- Added approach transition criteria for staying with the current approach, `REFINE`, `ADJACENT`, `PARK`, and `CLOSE`.

### v2.1.0 — research ideation protocol

Adds a research ideation protocol that separates candidate generation from grounding and execution.

**Added / changed**

- Research ideation now starts with a de-anchored Idea portfolio before prior-work grounding.
- When anchors are already visible, the active protocol now uses an anchor-stripped seed brief and excluded-anchor ledger before raw seed generation; later versions require substrate/operator/anti-vacuity checks before a seed is accepted as a candidate.
- Prior-work grounding remains mandatory before execution; ideation produces candidates, not execution-ready plans.
- Only one candidate is promoted into a plan after grounding and information-gain scoring; non-promoted ideas are recorded as `parked / killed / merged` and are not claims.

### v2.0.4 — prior-work grounding and positioning

Reframes literature review from novelty/differentiation toward prior-work grounding for every plan.

**Changed**

- Every new plan now requires a Prior-work grounding section before the Plan section.
- Required grounding depth is bounded but sufficient for the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations.
- Replaced the project-level differentiation file with `literature/positioning.md`, focused on how the work stands on prior work.
- Comprehensive literature survey remains required for strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims, separate from plan-scoped grounding.
- Removed the no-novelty loophole for unknown prior work; unknown prior work must be recorded as a named constraint that narrows or blocks relevant claims.

### v2.0.3 — reproducibility vocabulary and multiple-testing fixes

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

- Required Divergence checkpoint before execution: approach portfolio, anchoring audit, research positioning, disconfirming evidence, and commitment decision.
- Required a single post-result review before load-bearing claims, state-changing decisions, or reports.
- Review verdicts were `PASS` / `REWORK` / `INVALID`; only `PASS` + `PASS` permitted promotion in that older lifecycle.
- `REWORK` requires named reanalysis, repair, or rerun before any claim, decision, or report.
- `INVALID` makes affected results unusable as evidence until repair, rerun, or research-plan redo.
- Quant time-series test-set reuse is treated as a reliability failure requiring protocol reopening and fresh evaluation, not a weaker writeup.

### v2.0.0 — agent-driven R&D redesign

Complete redesign. No backward compatibility with v1.x.

**Added**

- 3 Frascati categories first-class: `basic_research`, `applied_research`, `experimental_development`
- Plan modes initially: `exploratory`, `confirmatory`, `milestone`; v2.4.0 adds `theoretical`
- Iteration FSA with 5 explicit branches: `NEXT_STEP` / `REFINE` / `ADJACENT` / `PARK` / `CLOSE`
- Divergence checkpoint before execution to expose alternatives, anchoring risk, research positioning, and disconfirming evidence before committing to a plan
- Single post-result review before claim/decision/report promotion, covering analysis sufficiency and result reliability
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
