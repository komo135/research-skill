---
name: creating-propositions
description: Use when generating research propositions, parent propositions, explanatory hypotheses, mechanism hypotheses, or principle-level hypotheses before proposing direct solutions, experiments, architectures, algorithms, or plans.
---

# Creating Propositions

Use this skill before direct solutions. Its job is to turn material into questions, questions into parent propositions or intermediate hypotheses, and those propositions into conclusion states. It does not choose priorities, write plans, run experiments, or select the direct solution to build.

A parent proposition or intermediate hypothesis is the research unit above direct solutions. It explains a principle, mechanism, constraint, representation, boundary, invariant, or regime under which direct-solution hypotheses can later sit. In this skill, "intermediate hypothesis" means a falsifiable parent-level proposition, not a direct solution and not a separate formal state layer.

## Required Checklist

Create this checklist before proposing architectures, methods, algorithms, interventions, evaluations, experiments, or plans. The checklist must be visible in the answer, not only used internally:

- [ ] State that direct solutions are not being proposed yet.
- [ ] Collect observations or state that material is missing.
- [ ] Separate observed facts from interpretations.
- [ ] Run a proposition-generation lens pass over the material.
- [ ] Generate multiple questions from the observations and lens pass.
- [ ] Manage the questions: sharpen, merge, park, or kill them.
- [ ] Select questions that can become parent propositions or intermediate hypotheses.
- [ ] Write parent propositions or intermediate hypotheses that are not direct-solution hypotheses.
- [ ] List direct-solution hypothesis slots under each parent proposition or intermediate hypothesis.
- [ ] Write expected observations.
- [ ] Write falsifiers.
- [ ] Write competing propositions.
- [ ] Write the conclusion state and any missing discriminator or material need.
- [ ] Only then hand off to `research` if prioritization, formal state, planning, execution, or result analysis is needed.

If an item does not apply, write `Not applicable: <reason>`. Do not silently skip phases.

## Material Gate

No material means no proposition. If the user provides no observation, failure, success case, comparator, trace, workload shift, measurement, constraint, or theoretical tension, return the minimum material-acquisition need instead of inventing plausible propositions.

Use this shape:

```markdown
## Observations

- Observed fact:
- Source or basis:
- Expected / comparator:
- What makes this notable:
- Reliability:
- Missing material:
```

When material is absent:

- do not write parent propositions
- do not fill direct-solution slots
- write `Conclusion state: under-specified`
- list the smallest material that would unlock proposition creation
- do not hand off proposition artifacts; hand off only the material-acquisition need if another workflow must collect material

Do not write parent propositions in the observation phase.

## Observations

Separate facts from interpretations before asking questions.

Observed facts are measurements, failures, successes, traces, comparisons, constraints, workload changes, prior-work facts, or theoretical tensions. Interpretations are possible explanations of those facts.

Use this shape when useful:

```markdown
## Observations

### O001: <short label>

- Observed fact:
- Source or basis:
- Expected / comparator:
- What makes this notable:
- Reliability:
- Missing material:
- Interpretation candidates:
```

## Proposition-Generation Lenses

Successful papers often become useful because they convert a tension into a parent proposition before choosing the method. Do not copy paper names, method names, or a routing table. Simulate the underlying move.

Run a lens pass after observations and before questions. Use only lenses triggered by the material. Usually two to four lenses are enough; if only one fits, say why. A lens is a way to ask a better question, not an output to cite.

Use this shape:

```markdown
## Proposition-Generation Lens Pass

| Lens | Material trigger | Question it creates | Use decision |
|---|---|---|---|
| <lens> | <observation> | <question> | use / park / kill + reason |
```

### Lens Catalog

| Lens | Ask this | Parent proposition form | Later direct-solution slots may include |
|---|---|---|---|
| Expectation break | What should be possible, easier, monotonic, or preserved, but is not observed? | The failure is caused by a missing condition, not by the headline resource or capacity. | parameterization, training condition, protocol, runtime mechanism, evaluation discriminator |
| Mechanism necessity doubt | Which component is treated as necessary, but may only supply a smaller underlying function? | The necessary object is the function or mechanism, not the familiar component. | alternative mechanisms, reduced components, replacement abstractions |
| Representation shift | Is the hard object being represented in the wrong form? | Recasting the object as a residual, difference, log, trace, graph, invariant, state, declaration, or intermediate representation exposes an easier structure. | architecture choices, data structures, IRs, type representations, logging or state models |
| Constraint relocation | Where is the bottleneck located, and can it move to a boundary where it is cheaper or more parallel? | The constraint belongs at another layer, time, node, endpoint, compiler/runtime boundary, or evaluation boundary. | parallel forms, caching, precomputation, compilation, scheduling, protocol changes |
| Responsibility placement | Which layer or actor should own a repeated concern? | Correctness or performance improves when responsibility moves from ad hoc local code to the layer that has the needed global information. | runtimes, APIs, libraries, schedulers, type systems, protocols |
| Failure normalization | What repeated failure is being treated as exceptional noise? | The failure class is normal system input and must become an explicit premise, state, protocol, or contract. | recovery designs, idempotency, retries, checkpoints, uncertainty-aware APIs |
| Uncertainty exposure | What hidden uncertainty is being collapsed into a single value, decision, metric, or state? | Surfacing uncertainty changes the problem from guessing a value to managing a distribution, confidence, ambiguity, or risk. | calibrated outputs, confidence protocols, abstention, diagnostics, measurement designs |
| Minimal sufficient abstraction | What is the smallest abstraction that preserves the phenomenon while removing accidental detail? | A smaller interface or model captures the essential function and creates multiple solution paths. | DSLs, APIs, primitives, core calculus, reduced benchmark, minimal model |
| Invariant and relaxation | What property must be preserved, and what assumed condition can be relaxed? | The invariant, not the original mechanism, is the source of correctness or progress. | algorithms, proofs, protocols, type rules, consistency models, verification checks |
| Regime and scale shift | Does the phenomenon change across depth, data scale, workload, concurrency, latency, memory, or distribution shift? | The proposition is regime-conditioned; the mechanism holds only under specified scale or workload conditions. | scaling experiments, workload partitions, adaptive algorithms, conditional designs |
| Measurement mismatch | Is the observed result controlled by the wrong metric, proxy, comparator, or benchmark slice? | The apparent phenomenon is mediated by measurement or evaluation conditions. | new metrics, probes, stratified evaluation, counterfactual comparisons |

Do not use every lens. A long catalog dump is not question generation.

## Questions

A question is not a proposition. It names what should be doubted or explained.

Use this shape:

```markdown
## Questions

### Q001: <short label>

- Question:
- Triggering observation:
- Lens:
- Why this question matters:
- What this might explain:
- Current status: raw / sharpened / merged / parked / killed
- Status reason:
```

Question management is required:

- Sharpen questions that are tied to material and can produce a falsifiable parent proposition.
- Merge questions that differ only in wording.
- Park questions that need missing material.
- Kill questions contradicted by the material or too close to a direct solution.
- Do not promote every question.

## Parent Propositions / Intermediate Hypotheses

A parent proposition or intermediate hypothesis is not a direct solution. It is the proposition under which direct-solution hypotheses can sit.

Use this shape:

```markdown
## Parent Propositions / Intermediate Hypotheses

### P? <short label>

- Proposition:
- Proposition type: principle / mechanism / constraint / representation / boundary / invariant / regime / intermediate hypothesis
- Source question:
- Lens:
- Material it explains:
- Why this is not a direct-solution hypothesis:
- Direct-solution hypothesis slots:
- Expected observations:
- Falsifier:
- Competing proposition:
- Conclusion state: open / supported / rejected / inconclusive / under-specified / split-needed / parked
- Reason for conclusion state:
```

Direct-solution hypothesis slots may name kinds of solutions, such as architecture choices, algorithms, runtime designs, evaluation designs, data constructions, interventions, formal proof routes, or experiments. Do not recommend one slot as the next thing to try in this skill.

### Quality Gate

Before accepting a parent proposition or intermediate hypothesis, check that it:

- comes from observed material, not from material absence
- is not phrased as `Use <method>` or `Build <system>`
- can hold at least two plausible direct-solution slots, or else is marked `under-specified`
- explains a principle, mechanism, constraint, representation, boundary, invariant, regime, or intermediate hypothesis
- has expected observations that could be seen without assuming the favorite solution
- has a falsifier that could reject it
- has a competing proposition
- has a conclusion state

If it fails the gate, revise it back into a question or park it. If there is no observed material, stop at the material gate instead.

## Conclusion States

Always write the current state of each parent proposition or intermediate hypothesis:

| State | Meaning |
|---|---|
| `open` | Live enough to hold direct-solution hypothesis slots. |
| `supported` | Current material supports the proposition, without claiming proof. |
| `rejected` | Observation or falsifier breaks the proposition. |
| `inconclusive` | Material or discriminator is insufficient to support or reject. |
| `under-specified` | Terms, observations, comparators, or measurements are too weak. |
| `split-needed` | Multiple parent propositions are mixed together. |
| `parked` | Not actionable now, but not rejected. |

Avoid `proved` and `validated` unless the domain truly has formal proof. In empirical work, use `supported`.

## Optional Persistence

Normally return the work in the conversation. If the user asks to save it, only manage proposition-creation state:

```text
proposition_drafts/
  observations.md
  questions.md
  parent_propositions.md
  conclusions.md
```

Do not write into `propositions/Pxxx_.../` from this skill. Formal proposition state, prioritization, child-hypothesis selection, plans, execution, and result analysis belong to `research`.

## Handoff Boundary

There are two valid handoff shapes.

Material-acquisition handoff, used only when material is absent:

- material-acquisition need
- `Conclusion state: under-specified`
- no parent propositions or intermediate hypotheses
- no direct-solution hypothesis slots

Proposition handoff, used only after observed material exists:

- observations
- proposition-generation lens pass
- questions with status
- parent propositions or intermediate hypotheses
- direct-solution hypothesis slots
- expected observations
- falsifiers
- competing propositions
- conclusion states

`research` decides priority, formal state, child hypotheses, plans, execution, and result feedback. If there are multiple parent propositions, intermediate hypotheses, or direct-solution slots, do not rank or choose among them here; hand off the set with conclusion states.

## Red Flags

Stop and return to the checklist when you are about to:

- propose a named method, architecture, algorithm, runtime, experiment, or evaluation before a parent proposition exists
- recommend one direct-solution slot as the next thing to try
- rank multiple parent propositions or direct-solution slots instead of handing them off
- treat a direct-solution hypothesis as the parent proposition
- generate propositions from no material
- list many candidate ideas without question management
- use a famous paper or method name as authority instead of extracting the question and proposition
- dump every lens instead of selecting lenses triggered by material
- omit the lens pass, falsifiers, competing propositions, or conclusion states
