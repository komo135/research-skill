# Research Ideation

This protocol governs divergent work for research ideas, research directions, hypothesis candidates, and next-experiment candidates. Its purpose is not to ignore prior work, but to prevent the candidate space from narrowing too early because prior work, familiar benchmarks, convenient datasets, or previous winning approaches were introduced before raw candidates existed.

## Core rule

Do not read prior work first when the user is asking for research idea generation. Do not summarize prior work first either. Prior work is applied after raw candidates exist.

Prior-work grounding remains mandatory before execution. This file does not replace grounding. It creates an idea portfolio first, then uses grounding to prune, merge, park, or kill candidates before anything is promoted to a plan.

If the main agent has already seen anchors such as prior work names, SOTA methods, previous best approaches, the user's preferred method, or convenient dataset details, the main agent must not generate raw candidates itself. The main agent must not generate raw candidates itself after seeing anchors. It must prepare a sanitized brief and dispatch a fresh de-anchoring subagent to generate the raw candidate set.

## Protocol

### De-anchoring pass

The de-anchoring pass separates sanitized brief preparation, fresh subagent dispatch, and raw candidate generation from the later grounding work.

### Sanitized brief preparation

The main agent prepares a brief for the de-anchoring subagent that includes only:

- the problem or phenomenon to investigate
- observed failure modes
- the kind of change or effect to measure
- hard cost, time, compute, data-access, ethical, or safety constraints
- any required output shape, such as number of candidates or scoring format

The sanitized brief must exclude:

- prior work names, paper titles, author names, and lab names
- SOTA systems, leaderboard winners, and previous best approaches
- the user's preferred method, favored mechanism, or pet hypothesis
- convenient dataset names, benchmark names, or easy local artifacts unless they are unavoidable hard constraints
- implementation sketches that imply a known approach
- literature-summary language that would make ordinary extensions of existing work feel like the default path

If an excluded detail is also a genuine hard constraint, rewrite it at the constraint level rather than naming the anchor. For example, describe the data modality, scale, access limit, or evaluation requirement instead of naming a benchmark or dataset.

### Fresh de-anchoring subagent pass

Dispatch a fresh de-anchoring subagent with only the sanitized brief. The subagent must not receive the main agent's prior-work notes, SOTA summary, previous favorite approach, user-preferred method, convenient dataset names, or earlier candidate list.

The subagent returns at least six raw ideas. Each raw idea may be one sentence. At this stage, do not reject candidates for reviewability, overlap with known work, ease of implementation, or fit with available datasets.

### Raw candidate generation

Raw candidate generation is owned by the fresh de-anchoring subagent, not by a main agent that has already seen anchors. The output is an unpruned candidate set that preserves breadth before transformation analysis and grounded pruning.

### Main-agent handoff

After raw candidates exist, the main agent resumes responsibility for the portfolio. The main agent may add clarifying labels, group similar candidates, and prepare them for transformation analysis, but it must preserve the raw candidate set before pruning.

The main agent applies grounded pruning only after this handoff. If the main agent needs additional raw candidates after seeing anchors, it must repeat the sanitized-brief and fresh-subagent process rather than generating the candidates directly.

### Transformation pass

For each raw idea, state what is being changed. Use one or more of these difference axes:

`method / mechanism / data assumption / metric / evaluation protocol / system design / problem framing`

Drop candidates that change none of these axes as mere parameter variations of an existing approach. Model size, thresholds, seeds, or extra sweeps alone do not count as transformations.

### Observation discovery pass

Observation is not yet a hypothesis. Before hypothesis synthesis, collect the observations that make each transformed candidate worth considering without treating those observations as explanations, claims, or proof.

Use observations from these sources, in this order:

- **Empirical observation** — a measured pattern, anomaly, capability gap, or observed phenomenon in the project or comparable evidence.
- **Literature observation** — a pattern abstracted from references, prior work, or historical exemplars without importing the named method as the default solution.
- **Failure-mode observation** — a reproducible error, instability, negative result, broken assumption, or evaluation failure.
- **Tension observation** — a conflict between results, theories, metrics, constraints, or expected and observed behavior.
- **Baseline observation** — what a simple baseline, standard comparator, or current approach already explains or fails to explain.
- **User/problem observation** — a durable fact about the user's problem, use context, constraints, or desired effect.

References can supply observations at this stage. The agent may read or use references to extract abstract observations, tensions, failure modes, baseline limits, or problem facts. This does not license literature-first anchoring: keep paper titles, SOTA systems, leaderboard winners, and named methods out of sanitized briefs and raw candidate generation, and do not narrow the raw portfolio around them before raw candidates exist.

References later ground candidates after raw candidates and hypothesis rationales exist. In that later role, references test whether candidates duplicate known work, inherit known assumptions, require standard baselines, need different evaluation, should be merged, should be parked, or should be killed.

### Hypothesis synthesis pass

A candidate list is not enough. Before quality-diversity scoring or promotion, transform each candidate into a falsifiable hypothesis rationale chain:

- Source observation: <the observed phenomenon, failure mode, capability gap, empirical regularity, or theoretical tension that motivates the candidate>
- Mechanism conjecture: <the proposed mechanism that would explain the observation or make the intervention plausible>
- Proposed intervention: <the method, architecture, data change, metric change, evaluation change, system change, or framing change to test>
- Predicted effect: <the measurable effect expected if the mechanism conjecture is right>
- Counter-hypothesis: <a plausible alternative explanation under which the intervention should not produce the predicted effect>
- Minimal disconfirming test: <the smallest test, ablation, comparison, or observation that would force rejection, narrowing, or parking of the candidate>

Keep paper titles, author names, and named methods out of sanitized briefs and raw candidate generation. After raw candidates exist, grounded and synthesis phases may use landmark papers and historical exemplars to abstract research patterns, not to narrow the raw portfolio in advance. Use names such as `Attention Is All You Need`, `ResNet`, `DQN`, and `Generative Pre-Training` only as compact examples of patterns: recasting an architecture around a different dependency mechanism, stabilizing deeper optimization through a structural path, converting sequential decision learning into a target/control problem, or testing whether generative pretraining supplies reusable representations.

### Quality-diversity pass

Do not select only the highest-scoring candidate. Keep at least one representative candidate for each meaningful difference axis, and merge similar candidates. The goal is not single-best optimization, but a portfolio of high-quality candidates across distinct niches.

### Grounded pruning pass

Apply prior-work grounding here for the first time. Check existing research, standard baselines, known limitations, evaluation protocols, and whether a comprehensive literature survey is needed. Classify each candidate as one of:

- `advance`: can be promoted into a plan
- `parked`: lacks necessary conditions, data, survey work, or baselines
- `killed`: duplicates known results, cannot be measured, cannot be falsified, or exceeds cost constraints
- `merged`: collapses into the same claim as another candidate

Grounded pruning may remove most candidates. That is expected. The important constraint is that pruning happens after raw candidate generation, not before it.

### Information-gain scoring

Do not choose by success probability alone. Score each candidate briefly on:

- Testability: whether it can be falsified
- Measurement clarity: whether the required measurement is clear
- Expected information gain: what can be learned even if the idea fails
- Cost: the cost of the smallest useful experiment
- Prior-work distance: whether it is more than a minor modification of existing work
- Claim discipline: whether value remains without making a strong novelty claim

### Pre-execution divergence review

Before execution, run one fresh review that attacks the portfolio breadth. Ask whether the portfolio is semantically diverse, whether prior work collapsed it too aggressively, whether parameter sweeps are being counted as separate ideas, and whether the parked / killed / merged reasons are justified.

### Plan promotion

An idea portfolio is not a plan. Promote only one selected candidate to `plans/<id>_<slug>.md`, and write `Prior-work grounding`, `Divergence checkpoint`, and `Plan` as usual.

Failed idea is not a claim. Non-promoted ideas are not claims. Failed ideas, parked candidates, killed candidates, and merged candidates must not be written as claims. Claims are written only for results that have passed execution, analysis, and research review.

## Common failures

- **Literature-first ideation.** "The literature is large, so summarize it first" strengthens anchors. Generate raw candidates first through the sanitized-brief subagent path.
- **Main-agent anchor leakage.** If the main agent has seen anchors, it must not create the raw candidate list itself. It prepares the sanitized brief, dispatches the fresh de-anchoring subagent, and waits for raw candidates.
- **Dataset convenience bias.** Naming an easy dataset too early can make the portfolio collapse into benchmark-shaped ideas. Include only true data constraints in the sanitized brief.
- **Safe-review bias.** Introducing "what would pass review" too early leaves only baseline strengthening. Reviewability belongs in the grounded pruning pass.
- **Winning-approach gravity.** If the portfolio clusters around the previous best approach, use the transformation pass to force different axes of change.
- **Novelty fetish.** Do not choose by novelty alone. Replication, baseline strengthening, and failure-mode catalogs can advance if their information gain is high.
- **Portfolio laundering.** Do not count similar parameter sweeps as separate candidates. If the difference axis is the same, merge them.
