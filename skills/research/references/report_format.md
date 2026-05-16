# Report Format

## Purpose

Reports are for humans. They live under `reports/<id>_<slug>/` and are the standalone evidence artifact a reader uses to make a decision or understand what was done — without opening the agent's plans, runs, or code.

A report is a snapshot. Once written, it does not get retroactively rewritten when later work changes the picture. Subsequent work produces subsequent reports. Each report stands on its own.

## Paper-grade reports, not venue manuscripts

The skill requires a **paper-grade report**: the evidence standard should be high enough that a non-author can evaluate the question, method, result, limitations, and next action from the report alone. It is not a venue manuscript: no LaTeX, venue-specific formatting, exhaustive survey, or publication packaging is required.

Two design consequences follow:

- **No environment locks or commit hashes in the prose.** Reports should describe material conditions, not environment locks: data identity, evaluation protocol, major tool/model versions, hardware class, external API/model version, or collection date only when those conditions could change the interpretation. A one-line pointer to `experiments/<plan>/runs/` is enough if a reader wants to dig into raw artifacts. This is methods reproducibility, not computational replicability.
- **No exhaustive citation lists.** Cite the directly relevant prior work (methods, resources, controls, comparators, or foundations used) — typically a handful, not dozens. The Related Work section must position the work, not pad a bibliography.

## Required structure

Every report has these sections, in this order. Category-specific shapes adjust the section contents but not the order. Sections that do not apply still appear with a short `Not applicable:` rationale; they are not silently omitted.

1. **Summary**
2. **Background**
3. **Related Work**
4. **Theory / Formulation** (required for `basic_research` with `mode: theoretical` and for any applied / experimental_development report whose claim rests on a mathematical or algorithmic derivation; otherwise include `Not applicable:`)
5. **Methods & Conditions** (basic and applied) / **System description** (experimental development)
6. **Results** (or Observations for basic research)
7. **Ablation / Sensitivity**
8. **Discussion**
9. **Limitations**
10. **Next action**
11. **References**

## Section requirements

### Summary

One or two paragraphs. A reader who reads only this section should understand:

- What was investigated, built, or proposed
- What was found (the headline finding or numbers)
- What the next action is

If the report is for a decision, the recommended decision goes here.

### Background

What was known before, what motivated the work, and what existing work, resource, control, or comparator this builds on. Brief — assume the reader has context but no specific knowledge of this plan.

Cite a handful of directly relevant prior works (from `literature/papers.md`). Do not pad with tangentially related citations.

### Related Work

Required in every paper-grade report. When `literature/positioning.md` for this plan contains substantive prior-work comparison (e.g., the plan claims novelty, replication, baseline-strengthening, or method-family transition), summarize that positioning. If the plan makes no prior-work comparison, include a short `Not applicable:` rationale and still cite the plan-scoped grounding in Background.

Content:
- Summarize the position recorded in `literature/positioning.md` for the reader (do not duplicate the file's full content; cite it)
- Identify the prior approaches the current plan stands on, extends, contradicts, or replicates
- For each, state in one sentence: what they did, what is inherited, what is changed
- Cite all referenced works using consistent identifiers that match the References section at the end

This section exists because the plan-level positioning currently lives in `literature/positioning.md` (not visible to the report reader). The Related Work section surfaces it for the human-facing report so the reader can place the result in context without opening the plan.

### Theory / Formulation

Required for `basic_research` with `mode: theoretical` and for applied / experimental_development reports whose claim rests on a mathematical or algorithmic derivation that the reader needs to understand to interpret the result. Otherwise include `Not applicable:` with the reason.

Content:
- **Definitions**: notation, key objects, scope of validity
- **Assumptions**: axioms or modeling assumptions the derivation depends on (cross-reference any assumption_audit findings from `references/assumption_audit.md`)
- **Derivation / theorem statement**: the formal result, with proof sketch or full proof depending on length; for long proofs, summarize in the report and place the full proof in `experiments/<plan>/notebooks/proof_<n>.md` or an appendix
- **Limiting cases**: what known result the formulation reduces to in stated limits (this is the basic-theoretical analog of the applied "comparator" — show that the new formulation recovers known correct behavior)
- **Predictions**: what observable consequences follow (these become the Results section's tested claims for theoretical-applied reports; for pure-theoretical reports they become Observations or Future-work predictions)

For pure-theoretical work without empirical evaluator, this section IS the load-bearing evidence. The assumption_audit-derived constraint-naming (no decisive empirical evaluator at the present state of knowledge) belongs in Limitations, not here.

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

For applied research: include evidence tied to the stated practical objective. Use a comparison table when the claim is comparative, report variance/replication when stochastic variation affects interpretation, and include ablation or controlled-intervention results when the claim attributes an effect to a component.

For basic research: figures and tables showing the phenomenon across the explored variable space.

For experimental development: figures showing measured performance under stated conditions.

### Ablation / Sensitivity

Required as a section in every paper-grade report. When the claim attributes an effect to a specific component, or when robustness across parameters/conditions is part of the claim, this section carries the evidence. Otherwise include `Not applicable:` and state why no component-causality or robustness claim is made.

Content:
- **Ablation table**: each row removes (or replaces) one component of the claimed-effective method; primary metric is reported for each row alongside the full-method baseline. The reader should be able to read off which component contributes what.
- **Sensitivity grid** (when claim covers a range): primary metric across a grid of parameter / condition variations (e.g., for quant: see `skills/quant-research/scripts/sensitivity_grid.py`). Highlight regions where the claim holds and where it fails.
- **Failure cases**: at least one configuration where the method underperforms the comparator, with one-sentence explanation. A method that "works everywhere" without a stated boundary is over-claimed.

This section exists as an independent block (not embedded in `claim.evidence`) so the reader can audit component-causality and robustness without parsing claim records.

### Discussion

Required in every paper-grade report. When the report draws conclusions beyond raw numeric outcomes, this section carries mechanism interpretation, why-it-works, surprising findings, and contradicted expectations. For purely descriptive Observations sections, state `Not applicable:` and explain that no mechanism interpretation is claimed.

Content:
- **Mechanism interpretation**: why does the observed result occur? What plausible causal chain or structural reason explains it? Cross-reference any Theory section.
- **Surprises and contradicted expectations**: what was different from what the agent or the literature predicted? Name the prediction and the deviation explicitly.
- **Implications**: what does this result mean for the next plan, for the field, or for the downstream decision?
- **Pearl's-ladder honesty**: state at which rung (association / intervention / counterfactual) each interpretation lives. Do not promote correlation-level evidence to causal claims here.

Discussion is **distinct from Limitations**. Limitations record what was not tested or what alternatives remain plausible; Discussion records the agent's interpretation of what *was* observed. Both are required when applicable.

### Limitations

What alternatives remain plausible, what conditions were not tested, what could change the conclusions. This is where the `alternatives_not_excluded` and `conditions_not_tested` from the load-bearing claims surface to the reader.

Do not hide limitations in an appendix. If a finding has a serious caveat, the reader needs to see it on first read. Limitations honestly stated do not weaken a report — they make it usable.

### Next action

One of:

- The agent's chosen iteration decision (`NEXT_STEP` / `REFINE` / `ADJACENT` / `PARK` / `CLOSE`)
- A specific request to the human reader (a decision they need to make, or input they need to provide)
- Both

A report without a next action is incomplete. Even `CLOSE: completed` is a next action ("no further work on this plan").

### References

Required in every paper-grade report. Include at minimum the source plan and source artifacts; include one entry per prior work cited anywhere in the report body.

Content:
- One entry per work cited anywhere in the report body
- Consistent identifier scheme: cited in body as `[Author Year]` or `[Author Year, p.X]`; full bibliographic entry here
- Source: extract from `literature/papers.md` for this plan; do not invent entries
- Acceptable formats: APA, IEEE, or any format that is internally consistent within the report
- For arXiv preprints, include the arXiv ID
- For DOI-bearing publications, include the DOI

Do NOT pad. If only 3 works are actually cited, list 3 entries — not a "comprehensive bibliography of the field." The Related Work section's job is to position the work; References' job is to let the reader find each cited work.

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

- Practical objective and success criterion
- Proposed method or procedure — architecture, algorithm, training procedure, protocol, or operational form
- Controls/comparators — what was compared against, with sources/versions, when the claim is comparative
- Evaluation protocol — datasets, materials, splits, metric computation, or other evidence route
- Compute setup — hardware class and training duration when they are material conditions; env locks belong in raw provenance if needed

**Results** includes:

- Evidence that the practical objective or success criterion was met or not met
- Quantitative comparison with variance/replication when the claim is comparative and stochastic
- Ablation or controlled-intervention table/figure when component contribution is claimed
- Failure cases if relevant

The Methods section must be specific enough that someone could re-implement the method or procedure. "We used attention" is not sufficient for an ML method claim. "We replaced the standard MHA block with a sparse-attention variant: queries attend to a learned set of K=32 prototype keys, value aggregation uses softmax-normalized attention scores. We applied this in all 12 layers of a 350M-parameter base." is sufficient.

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

### Basic research — theoretical sub-mode

For `basic_research` plans with `mode: theoretical` (pure conceptual / derivational work without empirical evaluator, e.g., Einstein 1905, Shannon 1948, Turing 1936, Bell 1964 form factors), the report shape differs from probing basic research with `mode: exploratory` or `mode: confirmatory`:

**Theory / Formulation** is the primary load-bearing section (see Section requirements above).

**Methods & Conditions** is replaced by a brief **Derivation context** subsection:
- What conceptual frame was assumed (axioms, definitions, prior theorems used)
- What chain of reasoning was followed at high level (the full derivation lives in Theory / Formulation)
- What limiting cases were checked

**Observations** (replacing Results) focuses on:
- What the derivation predicts (testable consequences, even if no test exists yet)
- What known phenomena the formulation explains or unifies
- What the formulation contradicts (predictions inconsistent with established results — these must be flagged loudly)

**Limitations** carries any assumption-audit-derived constraint (e.g., "no decisive empirical evaluator at the present state of knowledge" recorded via `references/assumption_audit.md` constraint-naming protocol).

**Next action** for pure-theoretical reports often takes the form of a predicted observation or a derivation extension, not an executable next step.

## Figures and tables

Each report is self-contained. Figures live under `reports/<id>_<slug>/figures/`. Tables under `reports/<id>_<slug>/tables/`. The report references them by relative path:

```markdown
![Convergence trajectories per seed](figures/convergence_curves.png)
```

The figures **must actually exist**. Generating a real figure may require code that lives in `experiments/<plan>/code/` or `lib/viz/`. The skill does not specify how figures are generated — only that they exist when the report references them.

`scripts/check_report.py` verifies that referenced figures exist.

### Figure-as-argument convention

A figure is not just an illustration of a number stated in prose; for many results it IS the primary evidence (e.g., Watson-Crick's double helix diagram, Hubble's velocity-distance scatter). Treat the figure as a load-bearing argument and write it to that standard:

- **Self-standing caption**: the caption must convey the figure's claim without the reader having to read the surrounding prose. Bad: "Convergence curves." Good: "Validation perplexity by epoch for the sparse-attention variant (orange) vs. the dense-attention baseline (blue), 3 seeds each (shaded = ±1 SD); the variant converges in 28 epochs vs. baseline 92, with no degradation in final perplexity."
- **Axes, units, sample size, variance**: all four are required on any figure showing measured outcomes. A figure missing any of them is not a valid evidence carrier.
- **One claim per figure**: a figure that shows three unrelated things splits the reader's attention. If multiple claims belong together, use sub-panels and label them (a), (b), (c) with each panel having its own self-standing caption fragment.
- **Color and shape encoded for accessibility**: do not rely on color alone to distinguish groups (use line style or marker shape too). The figure must remain readable in grayscale.
- **Source traceability**: figure caption or filename includes a pointer to the artifact that generated it (e.g., `figures/convergence_curves.png` ← `experiments/02/runs/02__003/eval_metrics.csv` via `lib/viz/plot_convergence.py`). This makes claim-to-artifact consistency checkable.

When the figure is the primary evidence (not a decoration), the Results section's prose role shifts from "stating the number" to "guiding the reader through the figure" — what to look at first, what comparison to make, what magnitude is meaningful.

## Provenance pointer (optional, one line)

If the report's load-bearing numbers should be auditable to specific runs:

```markdown
Source artifacts: experiments/01_phase_transition/runs/, plan: plans/01_phase_transition.md
```

This is a pointer, not a reproducibility section. It tells the reader where to look if they want to dig into the underlying artifacts. Reproducibility comes from the methods and conditions being clear enough to re-implement; provenance points help audit what the agent actually ran.

Claim-to-artifact consistency is an evidence-integrity check, not a separate reproducibility theory. If a report states a numeric, boolean, categorical, or count result, the cited artifact should contain the value or enough information to recompute it. A failed artifact check means the report value is not usable evidence until corrected, even if the method description is otherwise reproducible.

## Common failures

- **Placeholder figures.** Generate the figure or remove the reference. A report with `![figure](figures/TODO.png)` fails the contract.
- **Methods section that does not enable re-implementation.** "We tuned hyperparameters" — what hyperparameters, on what objective, with what resource envelope?
- **Hidden limitations.** Caveats relegated to a final paragraph the reader skips. Move them up or call them out in Summary.
- **Decision claimed but not labeled.** "We do not recommend X yet" without `REFINE` / `PARK` / `CLOSE`.
- **No actual numbers in Results.** Prose without measurements is not a research result.
- **Padding the Background or Discussion to look thorough.** Length is not the contract; clarity is.
- **Single-run claims in Results.** A single number with no variance is not characterized. Always include n and variance for performance claims.
- **Report longer than necessary.** A focused 2-page report beats an unfocused 10-page one. Length should follow content, not vice versa.
