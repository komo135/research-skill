# Research Ideation

This protocol governs divergent work for research ideas, research directions, hypothesis candidates, and next-experiment candidates. Its purpose is not to collect plausible one-line ideas. It forces candidates to be generated from observations, constraints, and explicit transformation operators, then kills candidates that cannot explain what changed or how they could be disconfirmed.

## Core rule

Do not read prior work first when the user is asking for research idea generation. Do not summarize prior work first either. Prior work is applied after raw candidates exist.

Raw seed output is not an accepted idea. A candidate is accepted into the portfolio only after it cites substrate ids, names the generation operator, states the changed premise, and survives the anti-vacuity gate. This is the difference between real ideation and post-hoc prose.

Prior-work grounding remains mandatory before execution. This file does not replace grounding. It creates an idea portfolio first, then uses grounding to prune, merge, park, or kill candidates before anything is promoted to a plan.

If anchors such as prior work names, SOTA methods, previous best approaches, the user's preferred method, or convenient dataset details are already visible, do not let them define the raw seed space. First prepare an anchor-stripped seed brief, record excluded anchors separately, and generate seed material only from substrate ids, constraints, and allowed generation operators.

## Protocol

### Idea substrate pass

Before accepting any candidate, build an idea substrate: named observations and constraints the candidate must work from. Each substrate item gets a stable id such as `S1`, `S2`, or `C1`.

Use at least three substrate items when available. If fewer than two real substrate items exist, do not invent ideas; ask for observations, run observation discovery, or open an ADJACENT plan to gather the missing substrate.

Allowed substrate sources:

- **Empirical observation** — a measured pattern, anomaly, capability gap, or observed phenomenon in the project or comparable evidence.
- **Failure-mode observation** — a reproducible error, instability, negative result, broken assumption, or evaluation failure.
- **Tension observation** — a conflict between results, theories, metrics, constraints, or expected and observed behavior.
- **Baseline observation** — what a simple baseline, standard comparator, or current approach already explains or fails to explain.
- **Constraint observation** — hard cost, time, compute, data-access, ethical, safety, or tool constraints that shape what can be tested now.
- **Literature observation** — a pattern abstracted from references, prior work, or historical exemplars without importing the named method as the default solution.
- **User/problem observation** — a durable fact about the user's problem, use context, constraints, or desired effect.

References can supply observations at this stage. The agent may read or use references to extract abstract observations, tensions, failure modes, baseline limits, or problem facts. This does not license literature-first anchoring: keep paper titles, SOTA systems, leaderboard winners, and named methods out of seed briefs and raw seed generation, and do not narrow the raw seed pool around them before seeds exist.

### De-anchoring pass

The de-anchoring pass separates anchor stripping and raw seed generation from the later operator and grounding work.

### Anchor-stripped seed brief

Prepare a seed brief that includes only:

- the problem or phenomenon to investigate
- the substrate ids and sanitized substrate descriptions
- observed failure modes
- the kind of change or effect to measure
- hard cost, time, compute, data-access, ethical, or safety constraints
- any required output shape, such as number of seeds or scoring format

The seed brief must exclude:

- prior work names, paper titles, author names, and lab names
- SOTA systems, leaderboard winners, and previous best approaches
- the user's preferred method, favored mechanism, or pet hypothesis
- convenient dataset names, benchmark names, or easy local artifacts unless they are unavoidable hard constraints
- implementation sketches that imply a known approach
- literature-summary language that would make ordinary extensions of existing work feel like the default path

If an excluded detail is also a genuine hard constraint, rewrite it at the constraint level rather than naming the anchor. For example, describe the data modality, scale, access limit, or evaluation requirement instead of naming a benchmark or dataset.

### Excluded-anchor ledger

Record the anchors intentionally excluded from raw seed generation:

- prior-work names, paper titles, author names, lab names
- SOTA systems, leaderboard winners, and previous best approaches
- the user's preferred method, favored mechanism, or pet hypothesis
- convenient dataset names, benchmark names, or easy local artifacts unless they are unavoidable hard constraints
- implementation sketches that imply a known approach

The ledger is not input to raw seed generation. It exists so later grounded pruning can check whether the portfolio collapsed back toward anchors.

### Hypothesis-generation handoff

When anchoring risk is high, the user explicitly asks for de-anchored hypotheses, or a fresh perspective would materially improve breadth, dispatch a fresh separate-context hypothesis-generation agent. This is allowed during ideation; it is not Plan review or Result analysis.

The anchor-stripped seed brief is the only generation brief. Pass substrate ids, sanitized substrate descriptions, hard constraints, required output shape, and the instruction to produce multiple working hypotheses from current observations. The Excluded-anchor ledger is not input to the generator. It remains with the main agent so the main agent can later audit anchor leakage.

The generator must produce multiple working hypotheses, not a list of different methods. If the user requests web or literature, or if current observations are too narrow to supply mechanism breadth, retrieval is required unless access is unavailable; use it to import abstract observations, cross-domain mechanisms, or known failure patterns, not named approaches as anchors. Each hypothesis must include:

- Source observation: <substrate ids and observed phenomenon, failure mode, tension, baseline limit, or constraint>
- Mechanism conjecture: <what mechanism could explain the observation or make an intervention plausible>
- Predicted effect: <observable effect if the mechanism is right>
- Counter-hypothesis: <plausible alternative that predicts a different result>
- Minimal disconfirming test: <smallest observation, comparison, ablation, derivation check, or evaluator result that would kill or narrow it>
- Web or literature retrieval notes: <abstract observations, cross-domain mechanisms, or missing-context note; no paper-title or SOTA-method anchors in raw hypotheses>

A skipped Web/literature retrieval entry in this hypothesis-generation handoff does not satisfy or waive the plan-scoped literature survey. Before any candidate is promoted into a plan, the plan still needs Prior-work grounding with Survey evidence.

The generator should consider the opposite of the visible favorite, foreground assumptions that may be false, transfer mechanisms across domains only at the abstract mechanism level, and include at least one candidate that changes the measurement or evaluator when the current evaluator may hide the phenomenon.

### Raw candidate generation

Raw candidate generation is raw seed generation. The output is an unpruned seed set that preserves breadth before operator conversion, anti-vacuity, and grounded pruning.

Each raw seed may be one sentence. At this stage, do not reject seeds for reviewability, overlap with known work, ease of implementation, or fit with available datasets.

Apply grounded pruning only after raw seed generation, generation operator conversion, anti-vacuity, and evaluator feedback. If additional raw seeds are needed after anchors are visible, repeat the anchor-stripped seed brief and excluded-anchor ledger before generating them.

### Main-agent intake

Do not accept generator output as authority. The main research agent owns the portfolio and must convert the generator's output into research state.

For each generated hypothesis, record an intake decision:

- Authority check: <why this is seed material, not a claim, plan, or decision>
- Observation trace check: <substrate ids it truly traces to, or missing-substrate constraint>
- Mechanism review: <whether the mechanism is explanatory, merely a method swap, or post-hoc prose>
- Decision: <advance / park / kill / merge / regenerate>
- Next-plan action: <promote toward current plan / open ADJACENT evaluator-construction plan / gather substrate / run grounded pruning / no plan>

Regenerate when the output is only method names, parameter sweeps, literature extensions, benchmark-shaped ideas, or candidates with no mechanism. Park when the mechanism is plausible but substrate, evaluator, data, or prior-work grounding is missing. Kill candidates that cannot be disconfirmed or only restate the favorite approach. Merge candidates that share the same mechanism and minimal test.

### Transformation pass

Transformation is no longer a label-only exercise. It is implemented by the generation operator pass below. The old question "which axis changed?" remains useful, but an axis name alone is not enough.

### Generation operator pass

Convert raw seeds into candidates by applying explicit generation operators to the idea substrate. A candidate must cite at least two substrate ids unless the task genuinely has only one substrate item, in which case the candidate must record the missing-substrate constraint and cannot advance to execution.

For each candidate, record:

- Substrate ids: <S1, S2, ...>
- Operator: <one operator below>
- Changed premise: <what the candidate changes about the current framing>

Candidate difference is still summarized with the axis vocabulary `method / mechanism / data assumption / metric / evaluation protocol / system design / problem framing`, but the axis label is not enough without the operator and changed premise.

Allowed operators:

- **Assumption inversion** — foreground a load-bearing assumption and test the opposite.
- **Failure-mode exploitation** — treat a recurrent failure as signal about the mechanism rather than noise to suppress.
- **Bottleneck relocation** — move the limiting factor from model/method choice to data assumption, metric, evaluation protocol, or system boundary.
- **Mechanism transfer** — transfer an abstract mechanism from one substrate item to another without importing a named method as the solution.
- **Measurement reframing** — change what is measured so the latent mechanism becomes observable.
- **Counterfactual control** — define a comparison that would separate two plausible mechanisms.
- **Boundary-condition search** — ask where the current explanation should fail first.
- **Evaluator construction** — when the key missing piece is a test harness, promote an evaluator-building candidate instead of pretending to test the idea now.
- **Problem reframing** — change the unit of analysis, objective, or causal story, not just a parameter.

Threshold tweaks, lookback changes, seed changes, model-size changes, filter swaps, winsorization, and extra sweeps are not generation operators by themselves. They can appear later as sensitivity checks, but they do not count as new ideas.

### Observation discovery pass

Observation is not yet a hypothesis. The Idea substrate pass is the durable output of observation discovery: it collects the observations that make each transformed candidate worth considering without treating those observations as explanations, claims, or proof.

Use observation sources in this order when building or reviewing the substrate:

- **Empirical observation** — a measured pattern, anomaly, capability gap, or observed phenomenon in the project or comparable evidence.
- **Literature observation** — a pattern abstracted from references, prior work, or historical exemplars without importing the named method as the default solution.
- **Failure-mode observation** — a reproducible error, instability, negative result, broken assumption, or evaluation failure.
- **Tension observation** — a conflict between results, theories, metrics, constraints, or expected and observed behavior.
- **Baseline observation** — what a simple baseline, standard comparator, or current approach already explains or fails to explain.
- **User/problem observation** — a durable fact about the user's problem, use context, constraints, or desired effect.

References can supply observations at this stage. References later ground candidates after raw seeds, generation operators, anti-vacuity records, and hypothesis rationales exist. In that later role, references test whether candidates duplicate known work, inherit known assumptions, require standard baselines, need different evaluation, should be merged, should be parked, or should be killed.

### Assumption audit pass

Before the anti-vacuity gate, run the assumption audit (see `references/assumption_audit.md`). This pass surfaces background assumptions of the reference model being challenged — distinct from the anchor audit in `Divergence checkpoint` which audits assumptions imported from prior approaches. The two are different and both are required.

The audit produces:
- A reference model challenged.
- At least three named assumptions considered.
- A load-bearing assumption with downstream-check applied so the named assumption is not downstream of a deeper one.
- An inversion candidate derived from that load-bearing assumption, or an explicit no-inversion reason.
- A blind-spot catalog prompt that is finalized after the anti-vacuity gate for surviving candidates, ties those candidates to mechanism failure paths, can narrow claim scope, and can trigger constraint-naming.
- Optional reference-class forecasting as an overconfidence check — not used during generation.

At least one candidate must use the load-bearing assumption or record why no inversion candidate is admissible under the task's constraints.

### Anti-vacuity gate

A candidate list is not enough. Before hypothesis synthesis, every candidate must pass the anti-vacuity gate. This gate exists to prevent the agent from rescuing a thin one-line idea with post-hoc prose; accepted candidates are not post-hoc prose.

For each candidate, record:

- Substrate ids: <at least two real substrate ids, or a named missing-substrate constraint>
- Changed premise: <what becomes false, weaker, conditional, or newly observable if the candidate is right>
- Mechanism conjecture: <why the changed premise would produce the predicted behavior>
- Predicted measurable effect: <what would change in an observable measure>
- Counter-hypothesis: <a plausible alternative explanation that predicts a different outcome under the minimal test>
- Minimal disconfirming test: <smallest observation, comparison, ablation, derivation check, or evaluator result that would kill or narrow the candidate>
- Verdict: <survives / killed>

Kill the candidate if any field is generic, circular, unavailable under the task constraints, or disconnected from the substrate ids. Do not patch the candidate by writing better prose. Generate a new candidate from the substrate or park the missing substrate/evaluator as a named constraint.

### Hypothesis synthesis pass

Only candidates that survive the anti-vacuity gate become hypotheses. Transform each surviving candidate into a falsifiable hypothesis rationale chain:

- Source observation: <substrate ids and the observed phenomenon, failure mode, capability gap, empirical regularity, or theoretical tension>
- Mechanism conjecture: <the proposed mechanism that would explain the observation or make the intervention plausible>
- Proposed intervention: <the method, architecture, data change, metric change, evaluation change, system change, or framing change to test>
- Predicted effect: <the measurable effect expected if the mechanism conjecture is right>
- Counter-hypothesis: <a plausible alternative explanation under which the intervention should not produce the predicted effect>
- Minimal disconfirming test: <the smallest test, ablation, comparison, derivation check, or observation that would force rejection, narrowing, or parking of the candidate>

Keep paper titles, author names, and named methods out of seed briefs and raw seed generation. After raw seeds exist, grounded and synthesis phases may use landmark papers and historical exemplars to abstract research patterns, not to narrow the raw portfolio in advance. Use names such as `Attention Is All You Need`, `ResNet`, `DQN`, and `Generative Pre-Training` only as compact examples of patterns: recasting an architecture around a different dependency mechanism, stabilizing deeper optimization through a structural path, converting sequential decision learning into a target/control problem, or testing whether generative pretraining supplies reusable representations.

### Quality-diversity pass

Do not select only the highest-scoring candidate. Keep at least one representative candidate for each meaningful difference axis, and merge similar candidates. The goal is not single-best optimization, but a portfolio of high-quality candidates across distinct niches.

The surviving portfolio should normally span at least three of these axes: `problem framing / mechanism / data assumption / metric / evaluation protocol / system design`. If the task constraints truly allow fewer axes, record the constraint and narrow later claims.

### Evaluator feedback pass

Before grounded pruning, record whether the portfolio can receive external or executable feedback.

If an executable evaluator exists and the category is `applied_research` or `experimental_development`, invoke `references/iterative_ideation.md`. Record:

- Status: Ran: <evaluator name>
- Executable signature: <real command-line invocation or sequence>
- Artifact: <run directory plus durable artifact path; stdout alone is not evidence>
- Fitness vector: <parseable score vector and uncertainty/variance if available>
- Killed candidates: <candidate ids and real failure reasons>
- Cycle-final winner: <candidate id and why it dominated>

If no executable evaluator exists, do not simulate fitness. Record:

- Status: Skipped: <named reason>
- Required evaluator or artifact: <what must exist before executable feedback is possible>
- Effect on promotion: <PARK / ADJACENT evaluator-construction plan / theoretical-only scope / other narrowed promotion path>

For basic research, theoretical work, or domains without runnable evaluators, external feedback may be a derivation check, limiting case, counterexample search, expert-provided observation, or literature-grounded contradiction. The record must still name the feedback path or the missing constraint.

### Grounded pruning pass

Apply prior-work grounding here for the first time. Check existing research, standard baselines, known limitations, evaluation protocols, and whether a comprehensive literature survey is needed. Classify each candidate as one of:

- `advance`: can be promoted into a plan
- `parked`: lacks necessary conditions, data, survey work, evaluator, substrate, or baselines
- `killed`: duplicates known results, is a parameter sweep, cannot be measured, cannot be falsified, or exceeds cost constraints
- `merged`: collapses into the same claim or test path as another candidate

Do not finalize Grounded pruning or Promotion decision before Survey evidence exists. The plan template keeps the whole Idea portfolio before `## Prior-work grounding` to preserve the de-anchored generation narrative, but section order is not permission to finalize promotion before Survey evidence. Grounded pruning may remove most candidates. That is expected. The important constraint is that pruning happens after substrate/operator generation and anti-vacuity, not before them.

### Information-gain scoring

Do not choose by success probability alone. Score each surviving candidate briefly on:

- Testability: whether it can be falsified under current or explicitly named future conditions
- Measurement clarity: whether the required measurement is clear
- Expected information gain: what can be learned even if the idea fails
- Cost: the cost of the smallest useful experiment or derivation check
- Prior-work distance: whether it is more than a minor modification of existing work
- Claim discipline: whether value remains without making a strong novelty claim

### Pre-execution divergence review

Before execution, run one fresh review that attacks the portfolio breadth. Ask whether:

- one-line seeds were rescued by synthesis prose
- hypotheses trace to substrate ids
- changed premises are non-parameter transformations
- counter-hypotheses predict different outcomes
- candidates can be disconfirmed under current constraints or are honestly parked
- prior work collapsed the portfolio too aggressively

### Plan promotion

An idea portfolio is not a plan. Promote only one selected candidate to `plans/<id>_<slug>.md` after Survey evidence exists, then write `Prior-work grounding`, `Divergence checkpoint`, and `Plan` as usual.

Failed idea is not a claim. Non-promoted ideas are not claims. Failed ideas, parked candidates, killed candidates, and merged candidates must not be written as claims. Non-promoted ideas are recorded as `parked / killed / merged`. Claims are written only for results that have passed execution, result analysis, and claim-structure checks.

## Common failures

- **Six thin ideas.** "Generate six ideas" is not the goal. Seeds that cannot cite substrate ids, an operator, and a changed premise are not candidates.
- **Post-hoc synthesis.** Writing a mechanism after the fact to rescue a weak seed violates the anti-vacuity gate. Kill it and regenerate from substrate.
- **Literature-first ideation.** "The literature is large, so summarize it first" strengthens anchors. Generate raw seeds first through an anchor-stripped seed brief.
- **Anchor leakage.** If anchors are already visible, keep them out of the seed brief and raw seeds. Record them in the excluded-anchor ledger and check later whether grounded pruning pulled the portfolio back toward them.
- **Dataset convenience bias.** Naming an easy dataset too early can make the portfolio collapse into benchmark-shaped ideas. Include only true data constraints in the seed brief.
- **Safe-review bias.** Introducing "what would pass review" too early leaves only baseline strengthening. Reviewability belongs after the anti-vacuity gate.
- **Winning-approach gravity.** If the portfolio clusters around the previous best approach, use generation operators to force different changed premises.
- **Parameter-sweep laundering.** Lookbacks, thresholds, seeds, model size, and filter swaps are sensitivity checks, not ideas.
- **Novelty fetish.** Do not choose by novelty alone. Replication, baseline strengthening, evaluator construction, and failure-mode catalogs can advance if their information gain is high.
