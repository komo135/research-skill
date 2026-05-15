# Report Format

## Purpose

Reports are for humans. They live under `reports/<id>_<slug>/` and are the artifact a reader uses to make a decision or understand what was done — without opening the agent's plans, runs, or code.

A report is a snapshot. Once written, it does not get retroactively rewritten when later work changes the picture. Subsequent work produces subsequent reports. Each report stands on its own.

## Why reports are not papers

The skill does not require paper-level formality (full Related Work survey, formal citations, LaTeX). Reports are summaries a non-author can act on. Two design consequences follow:

- **No environment locks or commit hashes in the prose.** Reports should describe material conditions, not environment locks: data identity, evaluation protocol, major tool/model versions, hardware class, external API/model version, or collection date only when those conditions could change the interpretation. A one-line pointer to `experiments/<plan>/runs/` is enough if a reader wants to dig into raw artifacts. This is methods reproducibility, not computational replicability.
- **No exhaustive citation lists.** Cite the directly relevant prior work (baselines, methods built on) — typically a handful, not dozens.

## Required structure

Every report has these sections, in this order. Category-specific shapes adjust the section contents but not the order.

1. **Summary**
2. **Background**
3. **Methods & Conditions** (basic and applied) / **System description** (experimental development)
4. **Results** (or Observations for basic research)
5. **Limitations**
6. **Next action**

## Section requirements

### Summary

One or two paragraphs. A reader who reads only this section should understand:

- What was investigated, built, or proposed
- What was found (the headline finding or numbers)
- What the next action is

If the report is for a decision, the recommended decision goes here.

### Background

What was known before, what motivated the work, what existing work or baseline this builds on. Brief — assume the reader has context but no specific knowledge of this plan.

Cite a handful of directly relevant prior works (from `literature/papers.md`). Do not pad with tangentially related citations.

### Methods & Conditions (basic / applied) | System description (development)

Substantive enough that another researcher could re-implement based on this prose. The contents vary by category — see "Category-specific shapes" below.

This is where research-level reproducibility lives. Methods reproducibility, in the sense of Goodman et al. (2016) — another researcher understanding what was done well enough to attempt the same study — is the contract. Computational replicability (rerunning exact code) is not.

**The plan is the canonical methods description; the report's Methods section is a human-readable summary, not a duplicate.**

The `plans/<id>.md` Methodology subsection holds the full re-implementation-level detail. The report's Methods & Conditions section should:

- Summarize the essence in a human-readable narrative
- Cite the plan for full detail: `See plans/<plan_id>.md (Methodology section) for full re-implementation detail`
- Cover the elements a non-author needs on first read (what was done, on what data, under what conditions)
- Not duplicate hyperparameter tables, full configuration listings, or per-run details that already live in the plan

Duplicating content between plan and report has no audit value — it just creates two places that can drift out of sync. The plan is the source of truth; the report is the human-facing communication.

Do NOT include environment locks or commit hashes in this section's prose. Include material conditions that affect interpretation, such as data split dates, evaluation protocol, hardware class, or external model/API version. Seed information is a variability disclosure, not a substitute for reporting variance; for stochastic results, report seed count, dispersion, and failures rather than relying on one fixed seed. A pointer at the end of the report ("Source artifacts: `experiments/01/runs/`") is sufficient for readers who want raw provenance.

### Results / Observations

What was observed, with at least one actual generated figure or table. **Placeholder figures are not acceptable.** If no figure makes sense, include a table; if no table makes sense, explain why and present numbers compactly in prose.

Numbers in this section should be traceable and verifiable against the cited artifacts. Mention sample size, variance, and any statistical setup that bears on interpretation.

For applied research: include a comparison table with baselines and the proposed method, variance across seeds, and ablation results.

For basic research: figures and tables showing the phenomenon across the explored variable space.

For experimental development: figures showing measured performance under stated conditions.

### Limitations

What alternatives remain plausible, what conditions were not tested, what could change the conclusions. This is where the `alternatives_not_excluded` and `conditions_not_tested` from the load-bearing claims surface to the reader.

Do not hide limitations in an appendix. If a finding has a serious caveat, the reader needs to see it on first read. Limitations honestly stated do not weaken a report — they make it usable.

### Next action

One of:

- The agent's chosen iteration decision (`NEXT_STEP` / `REFINE` / `ADJACENT` / `PARK` / `CLOSE`)
- A specific request to the human reader (a decision they need to make, or input they need to provide)
- Both

A report without a next action is incomplete. Even `CLOSE: completed` is a next action ("no further work on this plan").

## Category-specific shapes

### Basic research

**Methods & Conditions** emphasizes the probe and the variables:

- What system or phenomenon was probed
- What was varied (with ranges and step sizes)
- What was held constant
- What was measured and how

**Observations** (rename Results to Observations for basic research): emphasizes patterns and characterizations, not point achievements.

A basic-research report often ends with a refined question, not a yes/no answer. That is normal — state the refined question clearly in Summary and Next action.

### Applied research

**Methods & Conditions** has paper-like depth:

- Proposed method — architecture, algorithm, training procedure, hyperparameters
- Baselines — what was compared against, with sources/versions
- Evaluation protocol — datasets, splits, metric computation
- Compute setup — hardware class and training duration when they are material conditions; env locks belong in raw provenance if needed

**Results** includes:

- Quantitative comparison vs baselines with variance across seeds (table preferred)
- Ablation table or figure showing component contributions
- Failure cases if relevant

The Methods section must be specific enough that someone could re-implement the method. "We used attention" is not sufficient. "We replaced the standard MHA block with a sparse-attention variant: queries attend to a learned set of K=32 prototype keys, value aggregation uses softmax-normalized attention scores. We applied this in all 12 layers of a 350M-parameter base." is sufficient.

### Experimental development

**System description** replaces Methods:

- Architecture / structural overview
- Key design decisions and the reasoning
- Interfaces / how the system is invoked
- What it depends on (conceptually — frameworks, classes of data — not env-lock specifics)

**Results** emphasizes:

- Functional acceptance — what scenarios pass
- Performance characterization
- Operational behavior under realistic conditions

## Figures and tables

Each report is self-contained. Figures live under `reports/<id>_<slug>/figures/`. Tables under `reports/<id>_<slug>/tables/`. The report references them by relative path:

```markdown
![Convergence trajectories per seed](figures/convergence_curves.png)
```

The figures **must actually exist**. Generating a real figure may require code that lives in `experiments/<plan>/code/` or `lib/viz/`. The skill does not specify how figures are generated — only that they exist when the report references them.

`scripts/check_report.py` verifies that referenced figures exist.

## Provenance pointer (optional, one line)

If the report's load-bearing numbers should be auditable to specific runs:

```markdown
Source artifacts: experiments/01_phase_transition/runs/, plan: plans/01_phase_transition.md
```

This is a pointer, not a reproducibility section. It tells the reader where to look if they want to dig into the underlying artifacts. Reproducibility comes from the methods and conditions being clear enough to re-implement; provenance points help audit what the agent actually ran.

Claim-to-artifact consistency is an evidence-integrity check, not a separate reproducibility theory. If a report states a numeric, boolean, categorical, or count result, the cited artifact should contain the value or enough information to recompute it. A failed artifact check means the report value is not usable evidence until corrected, even if the method description is otherwise reproducible.

## Common failures

- **Placeholder figures.** Generate the figure or remove the reference. A report with `![figure](figures/TODO.png)` fails the contract.
- **Methods section that does not enable re-implementation.** "We tuned hyperparameters" — what hyperparameters, on what objective, with what budget?
- **Hidden limitations.** Caveats relegated to a final paragraph the reader skips. Move them up or call them out in Summary.
- **Decision claimed but not labeled.** "We do not recommend X yet" without `REFINE` / `PARK` / `CLOSE`.
- **No actual numbers in Results.** Prose without measurements is not a research result.
- **Padding the Background or Discussion to look thorough.** Length is not the contract; clarity is.
- **Single-run claims in Results.** A single number with no variance is not characterized. Always include n and variance for performance claims.
- **Report longer than necessary.** A focused 2-page report beats an unfocused 10-page one. Length should follow content, not vice versa.
