---
name: creating-propositions
description: Use when generating or managing research propositions before direct solutions, experiments, architectures, algorithms, or plans; when material must become proposition workspaces; when proposition states need split, merge, park, reopen, revise, support, contradiction, or under-specification decisions.
---

# Creating Propositions

Turn research material into proposition workspaces under `propositions/Pxxx_slug/`, then manage proposition state. This is an inline sub-skill of `research`: use the same context that contains intake, scoping, EDA, observations, and prior proposition papers. Do not use a separate fresh subagent for proposition generation.

## Required Checklist

Create this checklist before proposing architectures, methods, algorithms, interventions, evaluations, experiments, or plans:

- [ ] State that direct solutions are not being proposed yet.
- [ ] Confirm material exists, or return a material-acquisition need.
- [ ] Separate observed facts from interpretations.
- [ ] Name the Surprise.
- [ ] Name the load-bearing Bit the Surprise violates.
- [ ] Run a lens pass over the material.
- [ ] Generate and manage questions: sharpen, merge, park, or kill.
- [ ] Write proposition candidates with Ambition.
- [ ] Write expected observations, falsifiers, and competing propositions.
- [ ] Assign one 9-state proposition status.
- [ ] Create or update `propositions/Pxxx_slug/{proposition,observations,analyses,decisions}.md`.
- [ ] Only then hand back to `research` for prioritization, hypothesis planning, execution, result analysis, and papers.

If an item does not apply, write `Not applicable: <reason>`. Do not silently skip phases.

## Material Gate

No material means no proposition. Material can be an observation, failure, success case, comparator, trace, workload shift, measurement, constraint, prior-work fact, theoretical tension, EDA finding, or prior proposition paper.

When material is absent:

- do not write a proposition
- do not fill derived-hypothesis slots
- write `State: under-specified`
- list the smallest material that would unlock proposition creation
- hand off only the material-acquisition need

## Abductive Engine

Use this order:

1. **Surprise**: name the observation or prior-work tension.
2. **Bit**: name the prior belief, common assumption, expected relation, or inherited premise the Surprise violates.
3. **Flip**: use lenses as possible ways to flip the Bit into a proposition.
4. **Spark**: write the proposition as a principle, mechanism, constraint, representation, boundary, invariant, or regime.
5. **Discriminating expected consequence**: state what should be observed if the proposition is useful.
6. **Falsifier and competing proposition**: state what would break it and what else could explain the same material.
7. **9-state decision**: assign the current proposition state and record the decision.

If the Bit is not identifiable, do not make a proposition. Return a Bit/material-acquisition task. "This is interesting" is not enough.

## Ambition Lanes

Every `proposition.md` includes:

`Ambition: landmark-aspirant | incremental-honest`

Use `landmark-aspirant` only when the Bit is load-bearing, the Flip is a reasonable attack, significance is real, novelty is grounded, and the discriminating exam separates competitors. Use `incremental-honest` when the work is narrow but reproducible and useful. Prefer honest incremental scope over inflated significance.

## Content Gate

Before accepting a proposition, check:

- **Load-bearing Bit**: at least one proxy exists: what would need rebuilding if false, how widely the assumption holds, or a known failing prediction / counterexample.
- **Reasonable attack**: the Flip is tractable and testable, not just "would be nice."
- **Significance**: who cares and what changes if supported.
- **Discriminating exam**: the expected consequence separates this proposition from a competitor.
- **Novelty grounding**: the Bit is grounded in scoping/prior work or prior proposition papers, and the Flip is not already the same result.

Quality judgment is not a string checklist. If a Bit is trivial or not actually believed, find the real Bit or downgrade to `incremental-honest`. Do not dress weak content as landmark-level.

## Lens Pass

Run only lenses triggered by material. Usually two to four lenses are enough.

| Lens | Ask this | Proposition form |
|---|---|---|
| Expectation break | What should be easier, monotonic, possible, or preserved, but is not? | A missing condition, not headline capacity, explains the failure. |
| Mechanism necessity doubt | Which component is treated as necessary but may supply a smaller function? | The necessary object is the function or mechanism, not the familiar component. |
| Representation shift | Is the hard object represented in the wrong form? | A residual, difference, trace, graph, invariant, state, or IR exposes structure. |
| Constraint relocation | Where is the bottleneck, and can it move to a cheaper boundary? | The constraint belongs at another layer, time, node, endpoint, or evaluation boundary. |
| Responsibility placement | Which layer or actor should own a repeated concern? | Correctness or performance improves when ownership moves to the layer with global information. |
| Failure normalization | What repeated failure is treated as exceptional noise? | The failure class is normal input and must become an explicit premise or protocol. |
| Uncertainty exposure | What hidden uncertainty is collapsed into one value or decision? | Surfacing uncertainty changes the problem into managing a distribution, confidence, ambiguity, or risk. |
| Minimal sufficient abstraction | What smallest abstraction preserves the phenomenon? | A smaller interface/model captures the essential function and opens solution paths. |
| Invariant and relaxation | What must be preserved, and what condition can be relaxed? | The invariant, not the original mechanism, is the source of correctness or progress. |
| Regime and scale shift | Does the phenomenon change across scale, workload, latency, memory, depth, concurrency, or distribution? | The proposition is regime-conditioned. |
| Measurement mismatch | Is the result controlled by the wrong metric, proxy, comparator, or slice? | The phenomenon is mediated by measurement/evaluation conditions. |

Do not dump the catalog. A lens is a question generator, not evidence.

## Proposition Workspace

Use `scripts/new_proposition.py` to open a workspace after the proposition passes the gate:

```text
propositions/Pxxx_slug/
  proposition.md
  observations.md
  analyses.md
  decisions.md
  hypotheses/
```

`creating-propositions` owns `proposition.md`, `observations.md`, `analyses.md`, and `decisions.md`. `research` owns `paper.md` and all hypothesis files.

## State Machine

Use one vocabulary:

| State | Meaning | Plan-ready |
|---|---|---|
| `open` | Live, newly opened or still being tested. | yes |
| `supported` | Evidence supports the proposition without claiming proof. | yes |
| `unrealized-condition` | The proposition may hold, but a condition, representation, measurement, or evaluator is missing. | yes |
| `under-specified` | No discriminating expected consequence yet. | no |
| `contradicted` | Material breaks the proposition itself. | no |
| `split-needed` | Multiple propositions are mixed. | no |
| `split` | Child propositions carry the work; parent is retired. | no |
| `parked` | Live but blocked by material, priority, access, or dependency. | no |
| `closed` | Terminal: resolved, merged, killed, or no longer useful. | no |

Do not use `rejected` or `inconclusive` as proposition states. A hypothesis result may be inconclusive while the proposition remains `open`; if the discriminator is too weak, move the proposition to `under-specified`.

## Decisions

Record project structure decisions in root `decisions.md`: `OPEN_PROPOSITION`, `SPLIT_PROPOSITION`, `MERGE_PROPOSITION`, `CHANGE_SCOPE`, `CHANGE_PROTOCOL`.

Record proposition state decisions in `propositions/Pxxx_slug/decisions.md`: `SUPPORT`, `CONTRADICT`, `UNREALIZED_CONDITION`, `UNDER_SPECIFY`, `SPLIT_NEEDED`, `PARK`, `UNPARK`, `REVISE`, `CLOSE`, `REOPEN`.

`closed -> open` requires `REOPEN` with the new material or reconsideration reason. `parked -> previous live state` requires `UNPARK` with the satisfied unblock condition.

## Red Flags

Stop and return to the checklist when you are about to:

- propose a named method, architecture, algorithm, runtime, experiment, or evaluation before a proposition exists
- generate propositions from no material
- name a Surprise without a Bit
- use a trivial Bit and call it landmark-level
- treat EDA correlation as a claim
- continue using old `plans/`, top-level `experiments/<id>/runs/`, or per-hypothesis `reports/`
- rank solution slots instead of creating proposition state
- let `research` directly edit proposition-owned files without switching to this discipline
- reopen a closed proposition without a recorded reason
