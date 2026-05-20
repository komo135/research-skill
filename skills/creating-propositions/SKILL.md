---
name: creating-propositions
description: Use when generating or managing research propositions before direct solutions, experiments, architectures, algorithms, or plans; when material must become proposition workspaces; when proposition states need split, merge, park, reopen, revise, support, contradiction, or under-specification decisions.
---

# Creating Propositions

This is the proposition workbench for `research`. When invoked, turn material into proposition workspace changes or return a precise blocker. Do not end with a theory of the protocol; end with files changed, state chosen, and the next research action.

Use the same context as `research`. Proposition generation depends on intake, scoping, EDA, observations, and prior proposition papers; do not use a fresh separate-context subagent.

## Inputs To Read

If this skill is invoked alone, first read `intake.md`, `literature/scoping.md`, root `observations.md`, and any existing `propositions/*/{proposition,analyses,decisions}.md`. If those files do not exist, return to `research` to create the project layout and intake.

Read only what is needed for the current proposition pass:

- `intake.md`: intent and uncertain question
- `literature/scoping.md`: existing work, comparators, known failures, gaps
- root `observations.md`: project-level observations from EDA/material
- `data/eda/` summaries when the observation depends on them
- prior `propositions/Pxxx/paper.md` files when running a later cycle
- existing `propositions/Pxxx/{proposition,observations,analyses,decisions}.md` when revising, splitting, parking, reopening, supporting, or contradicting

## Stop Outputs

Under pressure, stop with one of these concrete outputs instead of rationalizing through the blocker:

```text
Route: materialization
Missing material: <observation, comparator, trace, prior-work fact, measurement, split, evaluator, or paper>
Smallest next artifact: <data/raw/... | data/eda/... | observations.md | literature/scoping.md>
Promotion explicitly forbidden: proposition, hypothesis plan, method, architecture, evaluation, paper
Next handoff: research material acquisition
```

```text
Route: exploratory-probe
Probe needed: <concrete under-controlled check needed before the material is interpretable>
Smallest next artifact: <data/eda/<probe_slug>.md | generated table/figure | hypothesis experiments/runs/<run_id> if a plan already exists>
Promotion explicitly forbidden: proposition support, landmark-aspirant, final paper
Next handoff: research probe execution
```

```text
Route: materialization
Missing Bit: <the assumption or prior belief that is not yet identified>
Smallest next artifact: <scoping note, observation, comparator, or prior paper excerpt>
Promotion explicitly forbidden: proposition, derived-hypothesis slot, landmark-aspirant
Next handoff: research scoping/material acquisition
```

```text
Proposition action: opened | updated | split-needed | parked | blocked | closed
Path: propositions/Pxxx_slug/...
State: <9-state value>
Surprise: <one sentence>
Bit: <one sentence or missing>
Discriminating expected consequence: <one sentence or missing>
Ledger: <decision label and file>
Promotion explicitly forbidden: <hypothesis plan | support | paper | none>
Next research action: <material acquisition | new_hypothesis.py | split | paper | no R&D route>
```

## Proposition Pass

Follow this sequence.

1. State that direct solutions are not being proposed yet.
2. If route is not already established, choose whether this pass is `materialization`, `exploratory-probe`, `proposition-commit`, or `ambition-elevation`. If the route is `materialization` or `exploratory-probe`, return the route stop output and do not create or update a proposition.
3. Inventory material as facts, not interpretations.
4. If material is absent, return `Route: materialization`, name the smallest missing material, and stop.
5. Name the Surprise: what observation or prior-work tension is not explained by the default expectation?
6. Name the load-bearing Bit: what prior belief, common assumption, expected relation, or inherited premise does the Surprise violate?
7. If the Bit is missing, return a Bit/material-acquisition task and stop.
8. Run two to four relevant lenses to create candidate Flips.
9. Write one or more candidate propositions as Spark statements.
10. For each candidate, write the discriminating expected consequence, falsifier, and competing proposition.
11. Merge duplicates, split mixed propositions, park blocked ones, and kill candidates without a discriminator.
12. Choose Ambition: `landmark-aspirant` or `incremental-honest`; this is the Content Gate point for ambition.
13. Assign one 9-state status and write the correct decision ledger entry. Do not use `provisional open`, `provisional support`, or any provisional state escape.
14. Create or update `propositions/Pxxx_slug/{proposition,observations,analyses,decisions}.md`.
15. Return control to `research` with the next action.

If a step does not apply, write `Not applicable: <reason>` in the artifact. Do not silently skip it.

## Material Gate

Material can be an observation, failure, success case, comparator, trace, workload shift, measurement, constraint, prior-work fact, theoretical tension, EDA finding, or prior proposition paper.

No material means no proposition, no derived-hypothesis slot, and no architecture/method/evaluation proposal. The correct output is a material-acquisition need with the target artifact path, such as `data/raw/...`, `data/eda/...`, root `observations.md`, or `literature/scoping.md`.

Missing split identity, comparator, baseline, evaluator, discriminator, or measurement cannot be moved into a plan as an "Assumption." If the missing item controls what observation would separate this proposition from its competitor, route to `materialization` or `exploratory-probe`.

Use `unrealized-condition` only after the proposition is already grounded enough to commit: Surprise, Bit, expected consequence, falsifier, and competitor are present, but a required condition, representation, measurement, or evaluator must still be built to test it. Do not use `unrealized-condition` merely to avoid admitting material absence.

## Abductive Engine

Write this chain into `analyses.md` in this order:

```text
Surprise -> Bit -> Flip -> Spark -> discriminating expected consequence -> falsifier + competitor -> 9-state decision
```

- `Surprise`: the observation or prior-work tension.
- `Bit`: the prior belief or inherited premise violated by the Surprise.
- `Flip`: a lens-driven inversion of the Bit.
- `Spark`: the proposition as a principle, mechanism, constraint, representation, boundary, invariant, or regime.
- `Discriminating expected consequence`: what should be observed if the proposition is useful and not if the competitor is right.
- `Falsifier and competing proposition`: what would break it and what else could explain the material.
- `9-state decision`: the chosen status and why the next action follows.

"This is interesting" is not a Bit. If the Bit is not identifiable, stop and return the missing material.

## Lens Pass

Run only lenses triggered by material. Usually two to four lenses are enough. Do not dump the catalog. In `analyses.md`, record only selected lenses as `Lens / material signal / question asked / resulting Flip or Not applicable: <reason>`.

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

## Ambition And Content Gate

Every `proposition.md` includes:

```text
Ambition: landmark-aspirant | incremental-honest
```

Content Gate applies when committing a proposition, revising a proposition from `under-specified` to `open`, or choosing/retaining `landmark-aspirant`. It is not a reason to block material acquisition or exploratory probes.

Use `landmark-aspirant` only when all are credible:

- **Load-bearing Bit**: doubting the Bit is consequential. Show at least one proxy and name it concretely — the specific established line of work, paper, prediction, or system whose result reverses or needs rebuilding if the Bit were false. If you cannot name a concrete one, the Bit is not load-bearing; downgrade. Wide acceptance alone does not qualify: a universally true assumption has a trivial Flip and is not load-bearing. The test is whether the Flip is surprising and would force rework, not whether the Bit is commonly believed.
- **Reasonable attack**: the Flip is tractable and testable, not just "would be nice."
- **Significance**: who cares and what changes if supported.
- **Discriminating exam**: the expected consequence separates this proposition from a competitor.
- **Novelty grounding**: the Bit is grounded in scoping/prior work or prior proposition papers, and the Flip is not already the same result.

Use `incremental-honest` when the work is narrow but reproducible and useful. Choosing honest incremental scope over inflated significance is required, not a preference. If a Bit is trivial, universally true, or not actually contested, find the real Bit or downgrade to `incremental-honest`; do not dress weak content as landmark-level.

## Workspace Writes

Use `scripts/new_proposition.py` to open a new workspace:

```text
propositions/Pxxx_slug/
  proposition.md
  observations.md
  analyses.md
  decisions.md
  hypotheses/
```

Then fill the files:

- `proposition.md`: statement, Ambition, current status, expected consequence, falsifier, competitor, content gate.
- `observations.md`: fact-level observations, evidence form, comparator or expected reference, missing material.
- `analyses.md`: Surprise/Bit/Flip/Spark chain, lens pass, candidate triage, derived hypothesis candidate when allowed.
- `decisions.md`: proposition state changes only.

`creating-propositions` owns those four files. `research` owns `paper.md` and all hypothesis files.

## State Router

Use one vocabulary:

| State | Meaning | Plan-ready |
|---|---|---|
| `open` | Live, newly opened or still being tested. | yes |
| `supported` | Evidence supports the proposition without claiming proof. | yes |
| `unrealized-condition` | The proposition is already discriminating, but a condition, representation, measurement, or evaluator must be realized before testing. | yes |
| `under-specified` | No discriminating expected consequence yet. | no |
| `contradicted` | Material breaks the proposition itself. | no |
| `split-needed` | Multiple propositions are mixed. | no |
| `split` | Child propositions carry the work; parent is retired. | no |
| `parked` | Live but blocked by material, priority, access, or dependency. | no |
| `closed` | Terminal: resolved, merged, killed, or no longer useful. | no |

Blocked state actions:

- `under-specified`: write the missing material or Bit needed to continue.
- `unrealized-condition`: plan only the work that realizes the named condition; do not treat missing discriminator-critical material as this state.
- `contradicted`: record why the proposition itself broke; revise, split, or close.
- `split-needed`: create child proposition plan before any hypothesis plan.
- `split`: continue only through children.
- `parked`: record unblock condition; do not create a hypothesis until `UNPARK`.
- `closed`: reopen only with new material or reconsideration basis.

Do not use `rejected` or `inconclusive` as proposition states. A hypothesis result may be inconclusive while the proposition remains `open`; if the discriminator is too weak, move the proposition to `under-specified`.

## Decision Ledgers

Record project structure decisions in root `decisions.md`: `OPEN_PROPOSITION`, `SPLIT_PROPOSITION`, `MERGE_PROPOSITION`, `CHANGE_SCOPE`, `CHANGE_PROTOCOL`.

Record proposition state decisions in `propositions/Pxxx_slug/decisions.md`: `SUPPORT`, `CONTRADICT`, `UNREALIZED_CONDITION`, `UNDER_SPECIFY`, `SPLIT_NEEDED`, `PARK`, `UNPARK`, `REVISE`, `CLOSE`, `REOPEN`.

`closed -> open` requires `REOPEN` with the new material or reconsideration reason. `parked -> previous live state` requires `UNPARK` with the satisfied unblock condition.

## Return Shape

End every proposition pass with:

```text
Route: <materialization | exploratory-probe | proposition-commit | ambition-elevation>
Proposition action: opened | updated | split-needed | parked | blocked | closed
Path: propositions/Pxxx_slug/...
State: <9-state value>
Ledger: <decision label and file>
Promotion explicitly forbidden: <hypothesis plan | support | paper | none>
Next research action: <material acquisition | new_hypothesis.py | split | paper | no R&D route>
```

## Red Flags

Stop and return to the procedure when you are about to:

- propose a named method, architecture, algorithm, runtime, experiment, or evaluation before a proposition exists
- generate propositions from no material
- call a missing discriminator, comparator, baseline, evaluator, or measurement an assumption so planning can proceed
- call a proposition `open` or `supported` only because it is provisional
- name a Surprise without a Bit
- use a trivial Bit and call it landmark-level
- assign `landmark-aspirant` without naming a concrete load-bearing referent
- treat EDA correlation as a claim
- continue using old `plans/`, top-level `experiments/<id>/runs/`, or per-hypothesis `reports/`
- rank solution slots instead of creating proposition state
- rank or pick a single best among multiple live propositions instead of handing off the set with their states; multiple propositions may stay live until evidence separates them
- let `research` directly edit proposition-owned files without switching to this discipline
- reopen a closed proposition without a recorded reason
