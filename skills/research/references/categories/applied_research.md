# Applied Research

## When this category applies

Applied research is original investigation undertaken in order to acquire new knowledge, directed primarily towards a specific practical aim or objective (Frascati Manual, OECD 2015).

Classify by the objective, intended use, expected output, and uncertainty type, not by source. A plan can build on basic research and still remain basic if the primary purpose is characterization; it becomes applied research when the primary purpose is acquiring new knowledge for a specific practical aim or objective.

Pick applied research when:

- You have a specific practical aim or objective and need new knowledge to address it.
- You are determining possible uses for basic-research findings.
- You are giving operational form to an idea, method, model, or procedure.
- You are evaluating whether a method, procedure, or way of working supports the objective under stated conditions.

For ML/quant method claims, the practical objective is often operationalized with a target metric, comparator, and evaluation protocol. Baseline comparison is required when the claim is comparative. Ablation or controlled intervention is required when the claim says a component causes the improvement.

Do not pick applied research if the practical aim is not yet defined or if you are still trying to understand the phenomenon. Those are basic research first. In ML method work, applied research usually depends on a defined metric, relevant baselines, and stated conditions of evaluation.

## Typical outputs

- A method, procedure, or way of achieving the practical objective
- Evidence that the objective or success criterion was met or not met
- Possible uses for prior findings or a new operational form of an idea
- Scoped finding about the conditions where the method/procedure does or does not work
- Failure modes, sensitivity, or limitation characterization

## Default plan mode

`confirmatory`. Fix in advance:

- Primary evidence measure and how it is assessed
- Comparator, control, or baseline when the claim requires one
- Decision threshold (what evidence supports or rejects the objective)
- Data / evaluation setup
- Compute or sample envelope
- Ablations or controlled interventions when component-causality claims are planned

Exploratory mode is acceptable for early scoping (which architectures are even feasible) but the claim-bearing phase should be confirmatory. If you do exploratory work first and then switch to confirmatory, those are two separate plans — the exploratory plan informs the confirmatory plan but does not contribute its evidence directly.

`milestone` mode is appropriate only when the plan's main question is whether a working artifact meets operational criteria. Applied research can use working artifacts, but its main purpose is acquiring new knowledge for a stated practical aim or objective. When the plan makes an improvement claim, baseline comparison is part of the evidence for that claim.

## Completion conditions

Acceptable completion shapes:

- Stated practical objective or success criterion is met, with claims scoped to the conditions tested
- Stated practical objective or success criterion is not met, with an explicit negative result and diagnosis
- Method, model, or procedure works under specific conditions but not others — scoped claim
- Improvement over a comparator is demonstrated when an improvement claim was part of the objective
- Proposed improvement is not demonstrated, or is dominated by a simpler comparator — also a result; report it honestly

Not acceptable as completion:

- "Looks like it works" without an evaluable objective or success criterion
- "Probably better" without evidence tied to the stated objective
- Improvement claims without an appropriate comparator
- Improvement that disappears under reasonable perturbation (different seeds, different splits, slightly different hyperparameters)
- Improvement only on the specific evaluation the agent chose; failure on the standard evaluation glossed over

## Report shape

Applied research reports describe the practical objective, the method/procedure or operational form tested, the evaluation evidence, and the scoped finding. Use `assets/report/applied_research_report.md.template`.

1. **Summary** — what was tried, what was found, the headline evidence
2. **Background** — what prior work this builds on (cite a handful, not dozens)
3. **Method / Procedure** — substantive description of the proposed approach; enough for re-implementation
4. **Evaluation** — data, conditions, controls/comparators when applicable, and success criteria
5. **Results** — evidence with figures or tables; include uncertainty/variance when it affects interpretation
6. **Component or mechanism checks** — required when the claim attributes an effect to a component
7. **Limitations** — conditions not tested, failure modes, possible confounds

Methods description must be substantive. "We used a Transformer" is not a methods description. For ML/quant methods, architecture choices (heads, layers, hidden dim, position encoding), training details (optimizer, schedule, regularization), and evaluation protocol (beam size, length penalty, test set) must be specific enough that another researcher could re-implement and roughly reproduce. For non-ML applied work, describe the procedure, materials, conditions, and evaluation route at the same level of re-implementable detail.

## Claims in applied research

Applied-research claims state how the work addressed a practical objective under specified conditions. A general form is: "method/procedure M supports objective O under conditions C, with evidence E." For this claim to be load-bearing:

- `evidence` must cite the specific observations, runs, measurements, or artifacts
- `alternatives_not_excluded` must list confounders not yet ruled out
- `conditions_tested` must specify the data, settings, materials, operating conditions, or compute regimes tested
- `conditions_not_tested` must explicitly call out generalization gaps

For ML/quant method claims, a comparative claim such as "method M exceeds baseline B by Δ" requires an appropriate comparator and fair comparison protocol. A component-causality claim such as "method M works because of component I" requires an ablation or controlled intervention; otherwise the claim should be scoped to the observed method behavior, not the cause of that behavior.

Example claim record:

```yaml
- claim: Replacing the standard MHA block with the proposed sparse-attention variant reduces validation perplexity by 0.18 (relative 2.1%) on WikiText-103 at the 350M-parameter scale across 3 seeds, with stable training.
  evidence: experiments/02_sparse_attn/runs/02__008__seed{0,1,2}/eval/wikitext103.json; figures/perplexity_vs_seed.png
  alternatives_not_excluded:
    - "Improvement may come from the 1.3% increase in active FLOPs at fixed parameter count"
    - "Only 3 seeds — std 0.07; the 0.18 gap is ~2.5σ but not >3σ"
    - "Sparse-attention variant got 40 hyperparameter trials vs 20 for MHA baseline"
  conditions_tested: "WikiText-103, 350M parameters, 100k steps, AdamW lr=1e-4 cosine, batch 1024, fp16"
  conditions_not_tested:
    - "Larger scales (>1B params)"
    - "Other domains (code, dialogue)"
    - "Longer training (>100k steps)"
```

## Analysis weight

For applied research, analysis must be sufficient for the stated practical objective and claim type. General applied claims need evidence tied to the objective, stated conditions, plausible alternatives, and limitations. ML/quant method claims use the applicable disclosure floor from `analysis.md`:

- Leakage probe passed
- ≥3 seeds with reported variance (Bouthillier et al. 2021)
- Ablation of each claimed-novel component
- Slice / subgroup evaluation on standard axes
- Calibration check if confidence scores feed downstream
- Perturbation / robustness probe
- Error analysis on a sample of failures

Run learning curves and loss curves for ML training claims — these often reveal training instabilities, overfitting, or insufficient capacity before they show up in headline metrics.

For component-causality claims, standard ablation patterns are one component removed at a time, or factorial design if interactions matter, with the full method and an appropriate comparator in the comparison set. For stochastic comparisons, single-seed ablations are not enough; variance across seeds is part of the result.

Pearl Rung 2 (intervention via ablation) is the standard warrant for "component X is responsible for the improvement." Diagnostic plots alone (Rung 1) do not support causal claims about why the method works.

## Pitfalls

- **No evaluable objective.** A specific practical aim still needs an evaluation route: a criterion, measurement, test, or decision rule that can show whether the objective was met.
- **Unsubstantiated improvement claim.** If you claim a method is better, faster, cheaper, safer, or more accurate, you need an appropriate comparator and a fair comparison protocol.
- **Single-seed comparative claims.** For stochastic comparisons, variance across seeds is part of the result. Run multiple seeds for claim-bearing comparisons.
- **Hyperparameter asymmetry.** If your method got more hyperparameter tuning than the comparator, the comparison is biased. Report tuning effort explicitly.
- **In-sample tuning.** Methods tuned on the test set are not tested. Use a validation split for tuning; test only at the end.
- **Metric shopping.** If the primary success criterion was not met, do not switch to a different criterion and present it as a success. If a secondary criterion is more relevant, REFINE the plan before any claim is made.
- **Compute apples-vs-oranges.** Comparing a 10× larger model to a smaller comparator tells you about scale, not about your method. Hold compute constant or report scaling curves.
- **Ablation theater.** Single-component ablations on isolated runs do not isolate causal contribution if the components interact. Report joint ablations when interactions matter.
- **Skipping the negative-result writeup.** A method that did not improve is still a result. Document it; the next agent should not re-run it.
- **Origin-only classification.** "This extends basic research" is not enough. The applied-research label requires new knowledge directed primarily toward a specific practical aim or objective. In ML method work, that practical aim is usually operationalized through a target metric and intended use; baseline comparison is required when the plan makes an improvement claim.
