# Mechanistic Hypothesis Generation

This protocol governs research idea generation, research directions, hypothesis candidates, and "what should we try next" requests. It does not start from candidate ideas. It turns the current research situation into a falsifiable mechanism hypothesis, a competing hypothesis, a discriminating prediction, and a minimal test.

The output is not a Plan, not a claim, and not a substitute for the Divergence checkpoint. It is the pre-grounding mechanism record used before Prior-work grounding and the Plan section.

## Core rule

Do not start from candidate ideas. Do not create a candidate portfolio. Start with what is known, missing, measured, constrained, and comparable. A method name, paper name, analogy, metric swap, larger model, or "try Transformer" is an intervention fragment, not a mechanism hypothesis.

## Protocol

### Research situation diagnosis

Record:

- Available material: successes, failures or limits, lineage, evaluation or measurement, constraints, unknowns, observable quantities, comparators, and counterfactuals.
- Missing material: observations, reproduced failures, baselines, evaluator, measurement definitions, counterfactuals, prior-work grounding, or minimal model.
- Why hypothesis generation is allowed or blocked: if the material cannot support a discriminating prediction, park and define the next observation task.

When material is missing, do not fill the gap with a plausible idea. Return to observation collection, success-case search, failure reproduction, evaluator construction, measurement definition, comparator creation, counterfactual construction, or minimal-model work.

### Analysis lenses considered

Consider multiple lenses before adopting one. For each considered lens, write:

- Lens:
  - What it inspects:
  - What it may miss:
  - Use decision:

### Adopted analysis lenses

- Primary lens: choose exactly one.
- Auxiliary lenses: choose 0-2.
- Reason: explain what must be discriminated in this situation.

The constraint is deliberate: shallow coverage of every lens is weaker than a focused primary lens with limited auxiliaries.

## Lens catalog

### Success mechanism lens

Inspects why a success worked rather than only what worked. Useful for strong baselines, simple methods beating complex methods, or stable empirical successes.

Hypothesis rule: if the success mechanism is essential, direct it, purify it, extend it, or move it to a new condition, and predict what should change.

### Failure dynamics lens

Inspects where a process breaks: information flow, gradient flow, search, measurement, optimization, state persistence, data distribution, or decision coupling.

Hypothesis rule: if a process is broken, isolate, shorten, control, or re-represent that process, and predict which failure condition should improve.

### Lineage-difference lens

Inspects what changed across a sequence of methods, results, or theoretical steps.

Hypothesis rule: if several successful steps point in one direction, test the unfinished generalization or a meaningful reversal of that direction.

### Center-auxiliary inversion lens

Inspects whether a component treated as auxiliary is actually the main mechanism.

Hypothesis rule: if the auxiliary mechanism alone explains the observation, the former center can be reduced, removed, or given a narrower role.

### Problem-form transformation lens

Inspects whether a direct problem should be reframed as difference learning, pretraining, proxy objective, simplified problem, self-supervision, control, or a staged measurement problem.

Hypothesis rule: if the hard part is the learning signal or representation form, changing the problem form should improve the search space or expose the mechanism.

### Measurement and evaluation lens

Inspects what the evaluator promotes, hides, or over-optimizes. It is primary when benchmark wins conflict with operational failures or tail risk.

Hypothesis rule: if the evaluator hides the phenomenon, a new measure, slice, counterfactual evaluation, calibration view, or failure-condition evaluation can be the research object.

### Constraint relocation lens

Inspects where compute, data, labels, search, communication, memory, or measurement constraints concentrate.

Hypothesis rule: if a dominant constraint can be moved, relaxed, precomputed, decomposed, or made observable, a new method or system boundary may appear.

### Sparse-information lens

Use this when the domain has too little observation for direct hypothesis generation, such as quantum settings, rare events, or new measurement regimes. In this mode, park hypothesis generation until the record names observable quantities, invariants, symmetries, limits, minimal model, comparators or counterfactuals that can narrow the space.

Do not fill missing evidence with fashionable terms. For quantum or other sparse domains, the next research object may be "what observation would narrow the hypothesis space" rather than a committed mechanism hypothesis.

### Cross-domain mechanism transfer lens

Inspects abstract mechanisms from another domain without importing method names. Examples include search over an energy landscape, perturbation schedules, selection pressure, state transitions, feedback control, or conservation-like constraints.

Hypothesis rule: if the problem structure is isomorphic, transfer the mechanism, not the named method. Always expose differences in observable quantities, controllability, scale, and objective function.

## From analysis to record

Every adopted analysis must be converted to:

- Observation: what was observed, including success, failure, limit, constraint, or measurement mismatch.
- Mechanistic analysis: which process explains the observation: information flow, gradient flow, search, measurement, representation, constraint, state transition, or decision coupling.
- Mechanism hypothesis: if the explanation is correct, what causes what, under which conditions, and what should change.
- Competing hypothesis: another mechanism that explains the same observation.
- Discriminating prediction: the different outcome expected under the mechanism hypothesis versus the competing hypothesis.
- Minimal test: the smallest experiment, analysis, counterexample, simplified model, measurement, evaluator, or derivation check that separates them.

"Use Transformer", "change the evaluation metric", "make the model bigger", or "add attention" is not a mechanism hypothesis. It is an intervention fragment until it states why it should work, what should change, what competing explanation remains, and how the minimal test separates the explanations.

## Mechanism hypothesis record

Use this shape in plans when the plan began from research ideas, research directions, hypothesis candidates, or "what should we try next":

```markdown
## Research situation diagnosis
- Available material:
- Missing material:
- Why hypothesis generation is allowed or blocked:

## Analysis lenses considered
- Lens:
  - What it would inspect:
  - What it may miss:
  - Use decision:

## Adopted analysis lenses
- Primary lens:
- Auxiliary lenses:
- Reason:

## Mechanistic analysis
- Observation:
- Analysis lens used:
- Mechanistic interpretation:
- Assumptions exposed:
- What would be different if this interpretation is true:

## Mechanism hypothesis record
- Hypothesis:
- Competing hypothesis:
- Discriminating prediction:
- Minimal test:
- Required evidence:
- Decision: commit / park / kill
- Reason:
```

Decision meanings:

- `commit`: provisional decision that the mechanism hypothesis, competing hypothesis, discriminating prediction, minimal test, and required evidence are sufficient to proceed into survey-backed grounding and planning.
- `park`: observations, measurements, assumptions, comparators, evaluator, prior-work grounding, or required evidence are missing.
- `kill`: the mechanism is circular, unmeasurable, indistinguishable from a competing hypothesis, or only a restatement of known work.

Do not finalize commit before Survey evidence exists. A retrieval note made while generating the mechanism record does not satisfy or waive the plan-scoped literature survey. Survey evidence is still required before the Plan section. Section order is not permission to finalize commit before Survey evidence.

## Pressure handling

### Candidate-list pressure

If asked for 5, 10, 10 ideas, or many ideas, do not answer with a list. Under time pressure, return to diagnosis and produce at most mechanism records that satisfy the full output shape.

### Method-name pressure

If asked to use attention, Transformer, RNN, a larger model, a filter, or another named method, treat the method as an intervention fragment and ask what failure, success, measurement mismatch, or constraint it is supposed to explain.

### Paper-name pressure

If a user invokes ResNet, DenseNet, Transformer, GPT, LSTM, AlphaGo, AlphaFold, or another success, do not use the name as authority. Use only the extracted mechanism and state why the current problem has the same or different structure.

### Analogy pressure

If asked for annealing, adaptation, evolution, or another cross-domain analogy, decompose the analogy into abstract mechanisms and prerequisite differences. If the mapping cannot produce a discriminating prediction, kill or park it.

In all pressure cases, return to diagnosis before committing.

## Evaluator-grounded refinement

When a failed hypothesis has a minimal-test result, treat that failure as a new observation. Do not return to a new list of ideas.

Record:

- failed hypothesis:
- new observation:
- which mechanism explanation was ruled out:
- which explanations remain live:
- revised Mechanism hypothesis record:
- Decision: commit / park / kill

If executable feedback exists, it must leave durable artifacts. Print-only output is not evidence: completed evaluator runs need `run_manifest.json`, `logs/stdout.log`, `logs/stderr.log`, and at least one durable artifact under `outputs/`, `tables/`, `figures/`, or `intermediate/`. stdout is not evidence.

## Using successful papers

Successful papers are design samples for this skill, not a mandatory runtime task. Do not make a paper table mandatory at runtime. Extract analysis operations, then apply only the operations relevant to the current research situation.

- Architecture-shift samples: ResNet, DenseNet, Transformer, LSTM. Extract information flow, gradient flow, state persistence, dependency structure, and path design.
- Objective or pretraining-shift samples: GPT, BERT, word2vec, contrastive learning. Extract how direct task solving became representation learning, proxy objectives, or scale use.
- Measurement and evaluation-shift samples: BLEU, GLUE, ImageNet, CheckList, calibration, robustness work. Extract how measuring a different thing creates a different research problem.
- Constraint-breaking or systematization samples: MapReduce, CUDA deep learning, AlphaGo, AlphaFold. Extract how compute, search, data, system boundaries, or constraints were relocated.
- Theory and sparse-domain samples: quantum, statistical physics, information theory, optimization theory. Extract observable quantities, invariants, symmetries, limits, counterexamples, and simplified models.
- Cross-domain transfer samples: transfer abstract mechanisms, not method names.

Do not collapse them into one universal principle.

## Common failures

- Producing many candidate ideas before diagnosis.
- Treating a named method, paper, or analogy as the hypothesis.
- Committing under sparse information instead of defining observable quantities or a minimal model.
- Choosing one analysis lens mechanically without comparing what other lenses miss.
- Writing good commentary but failing to convert it into a mechanism hypothesis record.
- Treating performance improvement as enough when competing hypotheses remain live.
- Treating evaluator failure as a reason to generate new ideas instead of revising, parking, or killing the mechanism record.
