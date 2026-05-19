# Basic Research

## When this category applies

Basic research is experimental or theoretical work undertaken primarily to acquire new knowledge of the underlying foundations of phenomena and observable facts, without any particular application or use in view (Frascati Manual, OECD 2015).

Classify by the plan's primary purpose, intended use, and expected output, not by where the idea came from. Basic research can be pure or oriented. Oriented basic research may have broad fields of general interest or expected future possibilities, but it still does not pursue a specific practical use in the plan.

Pick basic research when:

- You want to understand a mechanism, not yet to optimize it.
- You need to characterize what a system does before anyone proposes to improve it.
- You are defining or characterizing a measurement, dataset, reference implementation, or other reusable research object as foundational knowledge.
- You are cataloging the failure modes of an existing method.
- Your research question is broad and you expect it to sharpen as evidence accumulates.

Do not force basic research into a confirmatory mold. The output is often a refined question, a characterized phenomenon, or a useful baseline — not a yes/no answer.

## Role in R&D classification

Basic research records work whose primary output is knowledge about foundations, mechanisms, observable facts, reference baselines, or better-posed questions. Its outputs may later support applied research or development, but later use does not retroactively define the category of the plan.

Examples include defining or characterizing a metric such as BLEU (Papineni et al. 2002), establishing a reference baseline such as ResNet ([He et al. 2016](https://arxiv.org/abs/1512.03385)), or characterizing scaling behavior ([Kaplan et al. 2020](https://arxiv.org/abs/2001.08361)) when the plan's immediate purpose is knowledge acquisition rather than a specific practical objective.

## Typical outputs

- New observations about a system's behavior under varying conditions
- A refined or sharpened research question
- A reference object — a metric definition, benchmark dataset, reference implementation, or characterization that others can inspect or reuse
- A mechanism description — what causes what
- A failure-mode catalog — where the system breaks and why
- A theoretical insight — a bound, a conservation law, a structural property

Basic research can end legitimately with "the question is now well-posed and method X is the right way to test it next" — without producing a final answer.

## Default plan mode

`exploratory`. Specify the variable space and decision rules, not a point prediction. The plan template under `assets/plan/rd_plan_exploratory.md.template` makes this explicit.

When `confirmatory` is appropriate for basic research:

- You are testing a specific theoretical prediction (e.g., a bound from theory)
- You have prior exploratory evidence pointing to a precise hypothesis worth confirming

`milestone` mode is rarely appropriate for basic research — the deliverable is usually knowledge, not a working artifact.

## Completion conditions

Acceptable completion shapes:

- Phenomenon is characterized within a stated scope
- Baseline is built and documented well enough for others to use it
- Question is refined into something that can be tested with a known method
- Failure modes are cataloged
- Theoretical claim is established with explicit conditions

Not required: a yes/no answer to the original question. If the original question turned out to be ill-posed, the deliverable is the better-posed version. Record `UNDER_SPECIFY` on the parent proposition when more formulation is needed, or proposition-level `CLOSE` when the refinement is itself the resolved goal.

## Report shape

Basic research reports emphasize what was learned, not what was decided. Structure:

1. **Summary** — what was investigated, what was learned
2. **Background** — what was known before, what motivated the investigation
3. **Methods & Conditions** — how the phenomenon was probed; what was varied, what was held constant, what was measured
4. **Observations** — what the data showed, with actual figures
5. **Mechanism / Interpretation** — what explains the observations (and what does not)
6. **Limitations** — what alternatives remain plausible, what conditions were not tested

Use `assets/report/basic_research_report.md.template`.

## Claims in basic research

Claims tend to be of the form "under conditions X, the system behaves Y." Always specify the conditions explicitly. The single biggest failure mode in basic research is generalizing beyond the conditions actually tested.

For each claim:

- `conditions_tested` field should describe the variable ranges precisely
- `conditions_not_tested` field should explicitly call out the regions the claim does not cover

Example of a well-scoped basic-research claim:

```yaml
- claim: For ρ=28, β=8/3, the Lorenz system's chaotic attractor exhibits qualitatively different lobe-switching statistics at σ < 12 versus σ > 20, with intermediate σ showing transitional regime.
  evidence: propositions/P001_lorenz-regimes/hypotheses/H001_sigma-scan/experiments/runs/H001__004__seed0/outputs/metrics.json:L20 (lobe-switching rates per sigma); figures/02_switching_rate_vs_sigma.png
  alternatives_not_excluded:
    - "Coarse σ grid (Δσ=0.5) may miss intermediate periodic windows"
    - "Trajectory length T=200 may be too short to capture rare lobe-switches at low σ"
  conditions_tested: "σ ∈ [5, 30], Δσ=0.5; ρ=28, β=8/3 (canonical); T=200 with 50-unit transient discard; dt=0.01; rtol=1e-9"
  conditions_not_tested:
    - "σ outside [5, 30]"
    - "Non-canonical ρ or β"
    - "Larger T for tail-event statistics"
```

## Analysis weight

For basic research, EDA and descriptive analysis often carry the main evidential weight because the plan's immediate purpose is knowledge acquisition, characterization, or question refinement. Apply the EDA standard pass from `analysis.md` thoroughly:

- Distribution checks, missingness, outliers, covariation
- For time-series basic research: stationarity, autocorrelation
- For mechanism research: controlled variation across one variable at a time, with the others held constant
- Leakage probe is less central (no train/test split needed if not training a model) but understand what the variables actually represent

The claim-recording minimum adapts: variance across replications is still required when claims are made. Ablations may not apply if there is no "method" to ablate — but **controlled variation** (changing one parameter, observing the effect) is the basic-research analog.

Observations are the primary output. Promote to claim sparingly — only when the observation is robust to the variations tested. See `analysis.md` for the staging discipline.

## Pitfalls

- **Treating basic research as failed when no decision is reached.** A characterized phenomenon and a refined question are valid completions.
- **Implicit confirmatory framing.** Writing "we wanted to find that X" before doing the work converts exploration into confirmation. Either commit to confirmatory mode and write a hypothesis explicitly, or stay exploratory and write a variable space.
- **Overclaiming generality.** A finding at σ ∈ [5, 10] is not a finding about all σ. `conditions_not_tested` must say so.
- **Building a reference object without documenting it.** A metric, dataset, reference implementation, or characterization that nobody else can inspect is not reusable research knowledge. The report's Methods section is where the object becomes a usable reference.
- **Inventing structure for the sake of inventing it.** Not every basic-research project produces a reusable baseline. Plenty of basic research only produces a refined question. That is still a completion.
- **Classifying by origin.** A plan is not applied research merely because it extends a prior basic-research result. If its primary purpose is still to understand, characterize, or refine the question, keep it basic research.
