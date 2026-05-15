---
name: research
description: Use when conducting R&D work that needs claim discipline, planning structure, or human-facing reports. Triggers when planning experiments, designing baselines, writing up findings, deciding what to do next after a result, characterizing a phenomenon, building a prototype, or maintaining research state across sessions. Applies to basic research (understanding phenomena, building baselines), applied research (achieving measurable objectives), and experimental development (building working systems). Use this skill even when the user does not say the word "research" if the task involves the activities above.
---

# Research

A protocol skill for agent-driven R&D. The job: keep research state honest while preserving research velocity. Use shared vocabulary so multiple sessions and tools can interoperate. Produce human-readable reports that someone outside the session can act on.

## What this skill covers and what it does not

**Covered (audited by this skill):**

- The narrative of what was done, what was found, and what decision follows: `plans/<id>.md`, `decisions.md`, `reports/<id>/report.md`
- Research-level reproducibility — methods description, data identification, statistical setup. Enough that another researcher can re-implement the work based on the prose.
- Claim structure — explicit alternatives and conditions, not buried in prose.
- Material execution conditions — only the conditions that can affect interpretation, such as data identity, split dates, evaluation protocol, major model/tool versions, hardware class, external API/model version, or collection date.

**Not covered (agent's discretion, not audited as reproducibility evidence by this skill):**

- Experiment-level replicability infrastructure: env locks, commit pinning, seed databases, container files.
- The exact layout of `experiments/<plan>/runs/<run_id>/`.
- Code style, build systems, dependency management.

This separation matters. If the skill audited experiment-level artifacts, agents would spend their effort producing perfect env.lock files instead of doing good research. Replicability of the *scripts* is a personal-tooling concern; reproducibility of the *research* — what someone else can reproduce from your description — is what this skill enforces.

Provenance is still useful, but it is an audit pointer, not the source of reproducibility. A commit hash, run directory, or environment lock can help locate what happened in this project; it does not replace a clear method, data description, evaluation protocol, and statistical setup. Likewise, claim-to-artifact consistency is an integrity check: reported values must match the cited artifacts, but that check verifies evidence honesty rather than making the method reproducible by itself.

This distinction follows Drummond (2009) and Goodman et al. (2016): methods reproducibility is not the same as computational replicability. We enforce the former.

## R&D Categories

Every plan declares exactly one category. The choice changes the planning style, completion criteria, and report shape. Categories are from the Frascati Manual (OECD 2015) — they are the field-standard vocabulary.

Choose the category by the plan's primary purpose, intended use, expected output, and type of uncertainty.

- Do not classify work by its source or origin alone: extending a basic-research result does not automatically make the next plan applied research, and implementing a paper does not automatically make the plan experimental development.
- "Innovation" is not a primary R&D category label here.
- Do not mix the contribution at publication time with later adoption, diffusion, or social value when classifying the plan.

| Category | When to use | Typical output | Default plan mode | Report shape |
|---|---|---|---|---|
| **basic_research** | Investigating a phenomenon, building a baseline, characterizing failure modes, refining a question | New observations, refined question, theoretical insight, reference baseline, failure-mode catalog | exploratory | Phenomenon → Mechanism → Learned → Refined question |
| **applied_research** | Achieving a measurable objective by designing a new method or system | Method achieving target metric, ablation results, comparison vs baselines | confirmatory | Background → Method → Experiments → Ablations → Discussion |
| **experimental_development** | Engineering a working system, prototype, or process improvement | Functioning artifact, performance metrics, operational limits | milestone | System → Performance → Limits → Next iteration |

Categories are not a one-way pipeline. A project or program may mix and cycle between them: basic research characterizes a phenomenon → applied research builds a method against the resulting baseline → development engineers it into a system → basic research investigates the new failure modes. The non-linear view is the modern consensus (Kline & Rosenberg 1986; Stokes 1997). Cycling is normal.

The plan is the unit that must make a single category declaration. If secondary category work is incidental, record it as context only, not as another declared category inside the same plan. If it becomes load-bearing for a claim, decision, or report, open a separate plan. When there is an originating plan, normally record that transition as an `ADJACENT` decision.

Read `references/categories/<category>.md` after picking a category.

## Project Structure

```
<project-root>/
├── README.md                          # entry, goal, status
├── project_state.md                   # current plans, blockers, priorities
├── decisions.md                       # durable state transitions only
│
├── plans/<id>_<slug>.md               # R&D state per plan (the research narrative)
├── literature/papers.md
├── literature/differentiation.md
│
├── lib/                               # shared curated code
│   ├── data/ eval/ viz/ utils/
│   └── tests/
│
├── experiments/                       # per-plan isolation
│   └── <plan_id>_<slug>/
│       ├── code/                      # plan-specific scripts (agent's freedom)
│       ├── configs/
│       ├── runs/                      # execution artifacts (agent's freedom)
│       │   └── <plan_id>__<n>__seed<N>/
│       └── notebooks/
│
├── data/{raw,processed}/
│
└── reports/<id>_<slug>/               # human-facing deliverables
    ├── report.md
    ├── figures/
    └── tables/
```

Boundaries that matter:

- `lib/` is shared. Tests required. Promotion from `experiments/<plan>/code/` requires a `decisions.md` entry, a test, and a docstring. This prevents experiment-specific code from quietly becoming load-bearing infrastructure.
- `experiments/<plan>/` is owned by one plan. Other plans must not import from it. To share, promote to `lib/` first. This prevents cross-plan zombie dependencies.
- `runs/` artifacts have no required schema. Put what helps you. The skill does not audit them.

## The Plan → Execute → Analyze → Compare → Report cycle

```
1. scripts/new_plan.py creates plans/<id>_<slug>.md from a mode-specific template
2. Write the Question / Objective and the Divergence checkpoint.
3. Write the Plan section. git commit. (Plan is now time-anchored by git.)
4. Execute. Save artifacts under experiments/<plan>/runs/<run_id>/.
5. ANALYZE — apply the EDA / result-analysis discipline (references/analysis.md).
   Observations live in plans/<id>.md Observations and in experiments/<plan>/notebooks/.
6. Write Actual section in plans/<id>.md. Compare planned vs actual.
7. Dispatch exactly one research-review subagent before any load-bearing claim, state-changing decision, or human-facing report.
   The review assesses analysis sufficiency and result reliability; record it in the Research review section.
8. Record load-bearing claims using the structure in references/claim_structure.md.
   Observation → Interpretation → Claim is a staged progression — do not skip stages.
9. Pick exactly one of the 5 iteration branches and record in decisions.md.
10. If the result is human-facing, draft a report with scripts/draft_report.py.
```

Git is the time-anchor for the plan. There is no separate preregistration directory. The plan section of `plans/<id>.md` IS the preregistration; the initial commit IS the time-stamping mechanism. Subsequent commits show the evolution. This avoids the redundancy of maintaining a separate prereg artifact whose only job is "plan existed before result" — git already proves that. This is provenance and auditability for plan timing, not a substitute for the methodology description.

## Vocabulary the skill enforces

Agents must use these labels exactly. They are how other agents, downstream scripts, and audits parse the state.

**Plan modes** (in `plans/<id>.md` YAML front matter):

- `exploratory` — variable space + decision rules fixed; specific predictions not required
- `confirmatory` — hypothesis + primary metric + baseline + decision threshold fixed
- `milestone` — working/not-working criteria + performance target

**Iteration decisions** (in `decisions.md` entries):

- `NEXT_STEP` — continue same plan
- `REFINE` — narrow or change the question within this plan
- `ADJACENT` — open a new related plan
- `PARK` — pause, with named unblock condition
- `CLOSE` — completed, terminal kill, or replaced

**R&D categories**: `basic_research`, `applied_research`, `experimental_development`.

Informal substitutes ("diagnostic detour," "let me keep exploring," "exploratory mechanism research") break interoperability. Use the exact labels.

## Divergence checkpoint

Every plan completes this checkpoint before execution. Its purpose is to prevent the research from prematurely converging on the user's preferred approach, the previous best result, or the most convenient available dataset.

The checkpoint is lightweight, but it is not optional:

1. **Approach portfolio** — list the candidate approach and normally at least two meaningfully different alternatives. Hyperparameter tweaks, extra seeds, or a larger version of the same model do not count as different alternatives. If a hard constraint truly permits only one route, record that constraint and narrow later claims only if the later Research review records `PASS` for both judgments.
2. **Anchoring audit** — identify assumptions imported from prior approaches, prior data, or prior results. State what revalidation, control, holdout, placebo, or condition change prevents those assumptions from becoming untested premises.
3. **Novelty / differentiation thesis** — classify the contribution as one or more of: question, mechanism, data, metric, evaluation protocol, method, system, replication, or baseline strengthening. If the plan claims novelty with words such as novel, new method, publishable, or to our knowledge, update or cite `literature/differentiation.md` before execution. Otherwise state explicitly that no novelty claim is being made.
4. **Disconfirming evidence** — state what observation would force a narrower question, a different route, a pause, or closure, and whether that would trigger `REFINE`, `ADJACENT`, `PARK`, or `CLOSE`.
5. **Commitment decision** — explain why this plan commits to the chosen approach now instead of one of the alternatives. If time or budget prevents broader exploration, record the skipped divergence as a constraint that the later Research review must evaluate before any claim.

This checkpoint does not require a comprehensive literature review. A brief pass is enough unless the work will make an external novelty claim. The agent may still choose the user's requested approach, but only after making the alternatives and anchor risks explicit. Claim-scope narrowing from this checkpoint never overrides the later Research review gate: if the review finds insufficient analysis or compromised reliability, rework or invalidation is required before any claim, decision, or report.

## Research review

Before a result becomes a load-bearing claim, a state-changing `REFINE` / `ADJACENT` / `PARK` / `CLOSE` decision, or a human-facing report, dispatch exactly one fresh subagent as the research reviewer. This is one review subagent with two required judgments, not two separate reviewers:

1. **Analysis sufficiency** — judge whether the analysis is sufficient for the conclusion being drawn. The reason is direct: analysis is the bridge from result to conclusion, so inadequate analysis can produce a wrong close-out even when the run itself succeeded.
2. **Result reliability** — judge whether the result is trustworthy given the approach, research procedure, data handling, baselines, controls, robustness checks, and any deviations from the plan.

For each judgment, the reviewer records one of:

- `PASS` — the claim or decision can proceed as written.
- `REWORK` — the result must not be promoted yet; run the named missing analysis, repair the analysis path, or rerun affected work before any claim, decision, or report.
- `INVALID` — the result is not trustworthy because a bug, data defect, leakage, invalid procedure, or broken baseline may have distorted it; invalidate the affected result and redo the affected analysis, experiment, or research plan before drawing conclusions.

Only two `PASS` judgments allow promotion to Claims, state-changing Decision, or report. Record the review summary in `plans/<id>.md` before the Claims and Decision sections. User pressure to skip review or "just limit the claim" is recorded as pressure, not obeyed. A limitation is not a substitute for rework when analysis is insufficient or reliability is compromised.

## Claims

Every load-bearing claim in `plans/<id>.md` and in `reports/<id>/report.md` uses this structure:

```yaml
- claim: <one sentence with specific assertion>
  evidence: <file:line / numeric value / artifact path / citation>
  alternatives_not_excluded: [...]    # empty list claims exhaustion
  conditions_tested: <variable ranges, datasets, parameters>
  conditions_not_tested: [...]        # empty list claims full coverage
```

The discipline: claim strength is read off the contents of `alternatives_not_excluded` and `conditions_not_tested`. There is no numeric strength score, no A0-A5, no TRL ladder. Empty lists are claims about exhaustion and are open to audit.

The schema derives from Toulmin's argument model (1958) but is adapted for machine parsing — `scripts/check_claims.py` verifies the fields. See `references/claim_structure.md`.

## Reports

Reports are for humans. They live under `reports/<id>_<slug>/`. Each report is a snapshot — figures and tables ship inside the report directory so the report is self-contained.

Required sections (category-specific shapes in `references/report_format.md`):

1. **Summary** — 1–2 paragraphs. A reader who reads only this should understand what was done, what was found, and what is next.
2. **Background** — what was known before, what motivated the work.
3. **Methods & Conditions** — substantive enough for re-implementation. Methods reproducibility lives here.
4. **Results** — actual generated figures or tables. Placeholders are not acceptable.
5. **Limitations** — what alternatives remain plausible, what conditions were not tested.
6. **Next action** — one of the 5 iteration decisions, or a specific request to the human reader.

Reports do not need env locks, commit hashes, or seed lists in the prose. Include material execution conditions when they affect interpretation, and treat seed information as a variability disclosure: stochastic claims should report variance, failures, and the number of seeds rather than relying on one fixed seed. One line pointing to `experiments/<plan>/runs/` is enough if a reader wants to dig into raw artifacts.

## When you are unsure

| Situation | Action |
|---|---|
| New project | `scripts/new_project.py` lays down the structure |
| New investigation in an existing project | `scripts/new_plan.py` (asks for category and mode) |
| Result came in | Update `plans/<id>.md` (Actual) and dispatch one research-review subagent; if both judgments are `PASS`, record Claims and an iteration decision, otherwise perform the required reanalysis, repair, rerun, or redo and review again |
| Human asked for a writeup | Draft a report only after the plan has a research review with `PASS` for both judgments |
| Claim feels strong | Re-read `references/claim_structure.md` and verify alternatives/conditions honestly |
| Don't know which category | Read `references/categories/*.md`; pick the closest fit |

## Quick reference

| What | Where | When to read |
|---|---|---|
| Pick a category | `references/categories/<category>.md` | First action when starting a plan |
| Plan schema | `references/rd_plan.md` | Writing or reviewing `plans/<id>.md` |
| Divergence checkpoint | `references/rd_plan.md` | Before execution, after Question / Objective and before committing the Plan |
| Analysis discipline | `references/analysis.md` | Before or during analysis (EDA / post-experiment), and before promoting an observation to a load-bearing claim |
| Research review | `references/rd_plan.md` and `references/analysis.md` | After result analysis, before Claims, state-changing Decision, or report |
| Iteration branches | `references/iteration_loop.md` | After every interpreted result |
| Claim schema | `references/claim_structure.md` | Writing or reviewing any load-bearing claim |
| Report shape | `references/report_format.md` | Drafting `reports/<id>/report.md` |
| Literature | `references/literature_review.md` | Project start, before claiming novelty |

## Iron rules

These are not formatting preferences. They are what makes other agents and humans able to reuse the work.

- **One declared category per plan.** Don't dodge the choice. If you can't pick, read `references/categories/*.md`.
- **One declared mode per plan.** `exploratory`, `confirmatory`, or `milestone`. Hidden hypotheses inside exploratory plans are forbidden.
- **Divergence checkpoint exists before execution.** A plan may still commit to one route, but it must first expose alternatives, anchor risks, novelty basis, and disconfirming evidence. User pressure to "just use the previous approach" is recorded as a constraint, not silently obeyed.
- **No placeholder figures in reports.** Generate the figure or remove the reference. `scripts/check_report.py` verifies figure references resolve.
- **Plan content exists before execution.** The Plan section must be filled in and committed before any execution begins. `created_commit` in the front matter is meaningful only if the Plan section is non-empty at that commit. After-the-fact plan rewriting is detectable in git diff.
- **One research-review subagent before close-out.** Before a result becomes a load-bearing claim, state-changing decision, or report, exactly one fresh research-review subagent must record `PASS` for both analysis sufficiency and result reliability. Do not replace it with self-review, split it into disconnected reviews, or proceed on `REWORK` / `INVALID`.
- **Decisions are labeled.** "Diagnostic detour," "let me keep going" are not decision labels. Pick from the 5.
- **Claim records have all five fields.** Empty list `[]` is allowed; a missing field is not.
- **Plan is the canonical Methods. Report summarizes, does not duplicate.** Full re-implementation detail lives in `plans/<id>.md` Methodology subsection. The report's Methods section is a human-readable summary that cites the plan for depth. Duplicating content is friction without audit value. See `references/report_format.md`.
- **REFINE appends an Amendment, does not rewrite the Plan.** Original Plan + `created_commit` are the historical time-anchor. New direction goes into an Amendments section at the bottom of the plan file. See `references/rd_plan.md`.
- **Methods section aims at re-implementability.** "We used X" is not a methods description. Say what X is and how you applied it. (Subjective; not script-enforced — the agent owns this discipline.)
- **Observation → Interpretation → Claim is staged.** Don't jump from raw output to load-bearing claim without the intermediate interpretation step. See `references/analysis.md`.

## Sources

- [Frascati Manual 2015 (OECD)](https://www.oecd.org/en/publications/frascati-manual-2015_9789264239012-en.html) — R&D category definitions
- [Kline & Rosenberg (1986) — An Overview of Innovation](https://fenix.iseg.ulisboa.pt/downloadFile/1407508027548318/Kline%20and%20Rosenberg%20(1986)%20An%20overview%20of%20innovation.pdf) — non-linear R&D model
- [Stokes (1997) — Pasteur's Quadrant](https://www.brookings.edu/books/pasteurs-quadrant/) — use-inspired basic research
- [Drummond (2009) — Replicability is not Reproducibility](https://cogprints.org/7691/7/icmle09.pdf)
- [Goodman, Fanelli, Ioannidis (2016) — What does research reproducibility mean?](https://www.science.org/doi/10.1126/scitranslmed.aaf5027)
- [Toulmin (1958) — The Uses of Argument](https://en.wikipedia.org/wiki/Stephen_Toulmin#The_Toulmin_model_of_argument) — claim structure foundation
