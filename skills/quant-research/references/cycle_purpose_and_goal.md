# cycle_purpose_and_goal.md

Why a research cycle is a cycle, what its goal is, and how to set that goal
so the rest of the protocol (H portfolio, stop conditions, failure routing)
is *derived* from it rather than improvised per Purpose.

## When to read

- **Before** writing the Purpose header of a new notebook (Step 2 in
  `SKILL.md`) — the five items defined here are pre-implementation
  required, alongside Purpose / Universe / data ranges
- Before adding the *first* H to a notebook (the H portfolio is decomposed
  from the goal defined here, not invented per H)
- Whenever you catch yourself asking "should I run another H?" — re-read
  the decision rule below; the answer is *there*, not in your H1 result

## Why a research cycle is a cycle (not a single experiment)

Research is not its own end-product. The flow is

```
research  →  durable knowledge  →  downstream R&D consumer  →  system / deliverable
```

A single experiment produces *evidence*. Evidence alone is too weak to
underwrite a downstream decision (deploy a strategy, ship a model, scope
the next research Purpose, allocate compute, write a paper section, set
portfolio sizing). A cycle — multiple H's tested under one Purpose with
cross-H synthesis — is the mechanism that elevates evidence to **knowledge
durable enough that the downstream consumer can act on it**.

This is the load-bearing claim: the cycle's existence is justified by the
downstream consumer it serves. A cycle that produces evidence no one
consumes is process-without-purpose; a single experiment that fully
answers a consumer's decision is not a "shortened cycle", it is a cycle
of length one — and is rare. Most consumers' decisions need 2-4 H's of
mutually-supporting evidence to be decidable.

## What the goal of a cycle is

> The goal of a cycle is the **knowledge output that closes the downstream
> consumer's decision gap.**

It is *not*:
- `verdict='supported'` on H1 (that is a sub-unit of the answer)
- A Pattern A / B / C / D / E synthesis label (that is the shape of the
  answer, not the answer)
- "Publication-grade evidence" in the abstract (publication is a
  consumer; "in the abstract" means no consumer)

These are forms in which the answer arrives. The goal itself is the
*decision-supporting knowledge artifact*.

## How to set the goal — five required items, before any code

At the top of every notebook, alongside the Purpose statement, five items
are mandatory. They are written *before* H1 is designed; they are what
H1's design is derived from.

The first four items (Consumer / Decision / Decision rule / Knowledge
output) define the *cycle's internal logic*. The fifth item
(`target_sub_claim_id`) anchors the cycle in the project's research goal
— the four-layer model in `references/research_goal_layer.md`. Without
the fifth item, the cycle's relationship to the project's running
question is implicit and the next Purpose's selection becomes invisible.

```markdown
### Consumer
[Concretely named. Example: "the next derived Purpose
(exp_004 — funding-rate signal at multi-day horizons)";
"the production strategy build for Q3 2026";
"my own next Purpose, scoped as 'lower-frequency variant
of this signal'"; "the literature-review section of paper-3
on intraday FX microstructure".
NOT acceptable: "the research community", "future
researchers", "myself someday", "the team".
A consumer that cannot be named in one phrase is not a consumer;
return to Stage 0.]

### Decision the consumer is currently blocked on
[One sentence stating the yes/no/pivot the consumer cannot make
without this cycle's output. Example:
"Whether to fund a 2-engineer-week production build of an
EUR/USD intraday mean-reversion strategy."
"Whether the next Purpose should pivot to multi-day horizons
or abandon funding-rate as an alpha source."
"Whether Chronos fine-tuning warrants a continued GPU budget
for the next quarter."]

### Decision rule (predicate the consumer commits to BEFORE the cycle runs)
[The falsifiable predicate the consumer applies to the cycle's
knowledge output to land their decision. Three branches are
mandatory:
- YES (go forward) condition: numeric / structural threshold
- NO (do not go forward) condition: numeric / structural threshold
- KICK-UP (return to upstream) condition: structural condition
  indicating the cycle's frame is the wrong layer
Example:
- YES: test PSR ≥ 0.95 net of 5 bp/side on ≥3 instruments AND
  walk-forward positive-rate ≥ 60% AND no `fee_model` /
  `regime_mismatch` binding axis from cross-H synthesis
- NO: bootstrap CI of headline metric straddles 0 on val and test,
  OR Pattern A binding axis is fee/regime AND cannot be redesigned
  inside this Purpose
- KICK-UP: bug_review surfaces an unresolvable upstream data /
  feature issue, OR the consumer's decision turns out to require
  an artifact this Purpose cannot produce (e.g. requires a
  capacity test that needs different data)
Writing the decision rule before the cycle runs is the
load-bearing discipline. Without it, "consumer can decide"
is rhetoric and sunk-cost re-enters as "one more H and they'll
really be able to decide".]

### Knowledge output (artifact that lets consumer apply the rule)
[What the cycle produces — the artifact onto which the decision rule
is applied. Typically a multi-row entry in `results.parquet` plus a
Purpose-level synthesis paragraph plus a headline figure.
Example: "Per-H rows for H1-H3 in results.parquet covering
(a) gross existence, (b) net-of-cost survival, (c) regime scoping,
plus a Purpose-level synthesis naming Pattern (A-E) and binding
axis (if any), plus the headline cumulative-PnL-with-baselines
figure. Together, these let the consumer apply the YES/NO/KICK-UP
predicate."]

### Target sub-claim id (research-goal anchor)
[The project README's research-goal sub-claim ID(s) this Purpose is
expected to advance — the link from this notebook to the project's
running question. Primary: 1 sub-claim. Secondary: 0-2 sub-claims.
A Purpose targeting > 3 sub-claims is too broad (Pattern B per
`cross_h_synthesis.md`); split before opening.
Example: "Primary G1.1 (`quality factor yields net edge in TOPIX500`).
Secondary: none — turnover / live-tradeability is G1.2 territory and
is left to a derived Purpose."
The Purpose's design hypothesis at open (in `decisions.md`) restates
this in prediction form ("opening this Purpose will close G1.1 to
confirmed or falsified"). Each H inside the notebook inherits this
`target_sub_claim_id` by default; an override is recorded in
`hypotheses.md`'s row Statement column with a one-phrase reason.
See `references/research_goal_layer.md` for the four-layer model.]
```

## How to plan the H portfolio — sub-claim decomposition

The H portfolio is **derived from the decision rule**, not chosen from a
fixed taxonomy. The procedure:

1. Read the YES branch of the decision rule. List every conjunct
   (each AND-clause, each "AND no … binding axis", each threshold) the
   consumer requires.
2. For each conjunct, ask: which falsifiable Hypothesis tests this
   conjunct? Some conjuncts share an H (one well-designed test can
   cover multiple conjuncts); some need their own.
3. Read the NO branch and the KICK-UP branch the same way. The H's
   that produce NO-supporting evidence (binding-axis identification)
   and KICK-UP-supporting evidence (upstream-issue identification)
   are usually the same H's by design — a well-designed H tells the
   consumer *both* whether the YES branch fired *and*, if not, which
   axis blocks it.
4. The portfolio is complete when every conjunct in YES, NO, KICK-UP
   has at least one H whose result speaks to it falsifiably.

**Do not pre-fix the H axes** (existence / cost / regime / scope as a
universal taxonomy). Different consumer-decisions decompose differently.
A decision rule that turns on "compute cost vs marginal Sharpe" needs an
H on compute scaling that a decision rule on "regime stability vs Sharpe"
does not. Freezing a taxonomy reintroduces the catalog problem the
consumer-decision frame was introduced to fix.

## The three closure forms are equivalent research outputs

The cycle ends when the consumer can apply the decision rule and land
one of three branches. **All three are publication-grade, durable
research outputs** — not success / failure / abort. This equivalence is
load-bearing: it is what prevents "produce YES" from quietly becoming
the goal (which reintroduces selection bias one layer up from the
Hypothesis level).

| Closure | What the project carries forward |
|---|---|
| **Primary YES** | A characterized result (effect size, scope, robustness conditions) the consumer can deploy / build on. The H portfolio's positive evidence + scope statement. |
| **Fallback NO with binding axis** | The binding axis itself, as `failure_mode` controlled-vocabulary value, plus the conditions under which the binding fires. The next Purpose inherits this as documented prior — it knows where *not* to point. |
| **KICK-UP** | The structural reason the cycle's frame was wrong. The upstream consumer (often: the researcher's own decision about which Purpose to open next) inherits "this layer of the problem must be solved first". |

A NO-with-binding-axis is not a degraded YES; it is a full research
output addressed to the consumer. A KICK-UP is not failure to complete;
it is a research output that says "the question this cycle was given is
the wrong question for this consumer at this layer".

### KICK-UP is for frame mismatch only — NOT for scope mismatch or middle-range ambiguity

The most common drift is to use KICK-UP for any "the answer needs a
follow-on scoped cycle" case. That is wrong. KICK-UP is reserved for
**frame mismatch** — situations where the cycle's question is itself the
wrong question for this consumer at this layer. Examples:

- `bug_review` surfaces unresolvable upstream data contamination
  (e.g., funding-rate definition changed exchange-side mid-period; no
  embargo / window choice fixes it)
- `experiment-review`'s `scope` dimension finds that the consumer's
  decision actually requires an artifact this Purpose architecturally
  cannot produce (e.g., needs a capacity test that requires venue-side
  fill data this Purpose does not have)
- The Purpose's question turns out to depend on a prior question the
  Purpose cannot answer (e.g., "does signal X work?" depends on first
  characterizing a regime indicator the cycle did not include)

In all of these, the cycle's frame is structurally wrong; running more
H's inside the same frame cannot fix it. KICK-UP is the right closure
because the consumer cannot decide *until an upstream question is
solved*.

Cases that are NOT KICK-UP — they are **Fallback NO with scope-narrowing
follow-up** (a sub-form of Fallback NO):

- The signal exists in the cycle's frame but only inside a sub-scope
  (Pattern E) — the cycle answered the question; the consumer's NO
  branch fires for the broad scope and a derived Purpose tests the
  narrow scope
- A metric is in middle range (e.g., IC sits between the YES-floor and
  the NO-floor) — the cycle answered the question with insufficient
  evidence to clear the YES threshold but enough to rule out the
  NO-floor; the rule's NO branch fires with a "scoped follow-up"
  flag pointing at where to narrow
- Strong in-sample, unstable out-of-sample — the answer is "no, in this
  scope"; a derived Purpose may test stabilization techniques

The distinguishing question:

> **Can the cycle's frame, run with more H's, produce a decision?**
>
> If yes (more H's inside this frame can land YES, NO, or scoped NO) → not KICK-UP.
> If no (the frame must be replaced or supplemented before any H can decide) → KICK-UP.

When in doubt, choose Fallback NO with scope-narrowing rather than
KICK-UP. KICK-UP is the rarer closure; using it as a catch-all for
"the answer is unclear" hollows out the distinction.

The decision rule's KICK-UP branch should therefore name structural
preconditions only — "if `bug_review` finds data contamination of type
X" / "if upstream Purpose Y is found to be unresolved" / "if the
artifact this rule requires turns out to need data this Purpose cannot
produce" — not metric-range conditions.

### Stop the cycle as soon as the rule fires — do not run remaining YES-clause H's

The decision rule has a YES branch (multiple conjuncts, AND-joined) and
NO branch(es) (each typically one or two clauses). The cycle ends when
**any one** of the rule's branches lands — including any NO clause.
Specifically:

- **NO branch lands first**: if any NO clause is unambiguously satisfied
  by the H's run so far (e.g., H1 produces IC ≤ NO-floor with CI
  excluding YES-threshold; or H2 produces break-even fee < required
  with CI tight), **do not run the remaining unstarted YES-clause H's**.
  Go directly to cross-H synthesis and close on Fallback NO.
- **YES branch lands**: all YES-clause H's pass. Close on Primary YES.
- **KICK-UP precondition fires**: close on KICK-UP regardless of how
  many H's are run; the structural finding makes further H's
  uninformative.

The reason: continuing to run YES-clause H's after a NO clause has
landed is sunk-cost iteration disguised as thoroughness. The consumer
already has the evidence they need to apply NO; further H's add
multiple-testing inflation (worse DSR trial counts) and waste compute.

Concretely: if the decision rule is `YES = A AND B AND C; NO = (not A
with CI evidence) OR (B fails at the fee threshold)`, and H1 (testing
A) returns a clear NO on A, then H2 (testing B) and H3 (testing C) are
*not run*. Synthesis writes "NO, binding axis = A" and the cycle closes
at N=1.

**Do not use this rule to short-circuit weak NO evidence.** The NO
clause must be *unambiguously satisfied* — point estimate past the
NO-floor *and* CI excluding the YES-region. A point estimate in the
ambiguous middle is not a NO landing; it routes to the scoped-narrowing
form of NO (the cycle continues with the scoped follow-up if the rule
permits, or closes with "scope unclear, narrowing required" as the
Fallback NO).

The Pattern A-E synthesis in `cross_h_synthesis.md` produces *the shape*
of the answer; the closure form (YES / NO / KICK-UP) maps the shape onto
the consumer's decision rule. Every Pattern lands in one of the three
closures:

| Pattern (from cross_h_synthesis.md) | Maps to closure |
|---|---|
| D (monotonic improvement, latest H supported, all gates clean) | Primary YES |
| E (one H supported, others rejected on same axis) | Primary YES (with narrowed scope) |
| A (same axis fails everything) | Fallback NO; binding axis = the shared `failure_mode` |
| C (Pareto frontier, no convergence) | Fallback NO; binding axis = the trade-off itself |
| B (different axes, no convergence) | Often KICK-UP (the Purpose was the wrong scope; consumer's decision needs to be split first) |

## How existing protocol layers re-map onto this frame

The frame does not invalidate the existing protocol; it tells you what
the existing layers *are for*.

| Existing layer | Role under the consumer-decision frame |
|---|---|
| Per-H falsifiable statement (`research_design.md`) | The test that produces evidence for one sub-claim of the decision rule |
| Per-H verdict (supported / rejected / parked) | The sub-claim's evidence flag |
| `bug_review` (Step 11) | Confirms the per-H evidence is not contaminated, so the sub-claim flag is trustworthy |
| `experiment-review` (Step 13) | Confirms the per-H claim is warranted by design, so the sub-claim flag is *correctly stated* |
| Robustness battery (Step 12) | Confirms the per-H evidence holds under the perturbations the decision rule will encounter in deployment |
| Cross-H synthesis (`cross_h_synthesis.md`) | Combines sub-claim evidence into the final shape the decision rule is applied to |
| `hypothesis_cycles.md` routing | Decides whether the next sub-claim is in this notebook or a new Purpose |
| N=5 / N=8 exhaustion triggers | Emergency stop: cycle is consuming compute without converging on decision-grade knowledge — force synthesis and reconsider scope |

## Stop conditions — re-stated under this frame

A cycle ends when **any** of the following holds. Crucially: as soon as
*any* of (1)-(3) fires, **stop** — do not run remaining unstarted
H's, even if they were planned. Continuing past the firing of a closure
adds multiple-testing inflation and is the sunk-cost failure the frame
is designed to prevent.

1. **Primary YES achieved**: every sub-claim of the YES branch of the
   decision rule has evidence flags. Robustness battery + bug_review +
   experiment-review pass on the YES-supporting H's.
2. **Fallback NO landed (any sub-form)**:
   - **2a. NO clause unambiguously satisfied** at any point in the
     cycle (e.g., H1 produces metric past the NO-floor with CI
     excluding the YES-region) → stop, close on NO with the binding
     clause as the named axis. Do not run remaining YES-clause H's.
   - **2b. Cluster Pattern A** (shared `failure_mode` across rejected
     H's) → close on NO with the shared axis as binding.
   - **2c. Pareto frontier (Pattern C)** → close on NO with the
     trade-off itself as the durable finding.
   - **2d. Scope-narrowing NO (Pattern E)** → close on NO with a
     scoped follow-up Purpose proposed (the original cycle answered
     the broad-scope question; the narrowed scope is the next Purpose).
3. **KICK-UP triggered (structural frame mismatch only)**: a named
   structural finding makes the cycle's frame the wrong layer for the
   consumer's decision — typically `bug_review` surfaces unresolvable
   upstream contamination, or `experiment-review`'s `scope` dimension
   finds the consumer's decision requires an artifact this Purpose
   cannot produce. Ambiguous metric results, scope-narrowing, and
   middle-range partial signals are *not* KICK-UP — they are NO
   sub-forms (2d). KICK-UP is rare and requires a named structural
   precondition from the decision rule.
4. **Emergency stop (N=5 advisory / N=8 hard cap)**: the cycle has run
   long enough without (1)-(3) firing that further H's are unlikely to
   converge on decision-grade knowledge inside the current frame.
   Force cross-H synthesis; default to closure (2) per Pattern match
   or, only if a structural precondition is present, closure (3).

(1)-(3) are the *intended* closures. (4) is the emergency stop the
protocol provides for when the cycle is failing to converge — its role
is to prevent unbounded sunk-cost iteration, not to define the goal.

## Stage 0 compatibility

`pre_hypothesis_exploration.md` defines a stage where no H exists yet
and the start state is data-without-candidate-phenomenon. Stage 0 is
itself a cycle under this frame: its consumer is **the next-cycle that
will test the candidate H1 it produces**, its decision is "is this H
worth testing?", its decision rule is the differentiation-tier check
(≥ Medium per `hypothesis_generation.md`) plus EDA → H provenance.
Stage 0's knowledge output is the candidate H1 plus its provenance;
the next cycle is the consumer that applies the decision rule.

The "Consumer = self's next Purpose" escape hatch (legal under this
frame) covers exploratory research where the immediate consumer is the
researcher's own next Purpose. The constraint: the next Purpose must
be *nameable* in one phrase before this cycle starts. If you cannot
name what the next Purpose would be under either the YES or NO branch,
the consumer is not actually identified — return to Stage 0 and
characterize the data first.

## Anti-rationalizations

| Excuse | Reality |
|---|---|
| "The consumer is obvious; I don't need to write it." | Implicit consumer = the failure mode this whole frame exists to prevent. The act of writing the consumer down is what forces the decision rule into the open. |
| "I'll write the decision rule after I see H1's result." | Then it is not a decision rule, it is a post-hoc rationalization. The whole point of the rule is that it is committed before evidence arrives, so it cannot be moved to fit the result. |
| "My consumer is 'future researchers' / 'the field'." | Not a consumer. A consumer has a specific decision they will make on a specific timeline. "The field" makes no decisions. Replace with a specific paper section, derived Purpose, or production decision. |
| "The decision rule is restrictive — what if the answer falls outside YES / NO / KICK-UP?" | If the answer falls outside, that itself is the KICK-UP signal: the cycle's frame did not match the consumer's decision. The third branch exists precisely for this. |
| "I want to keep my options open; pre-committing to a rule narrows them." | Pre-commitment is the mechanism that makes any of the three closures legitimate research outputs. Without it, only YES feels like "real" output, and NO / KICK-UP get retroactively reframed as failure. |
| "N=5 hasn't fired, so I'll keep adding H's." | N=5 is the emergency stop. The intended stop is consumer-decision satisfaction. If the consumer can already decide (YES / NO / KICK-UP), close the cycle now — adding H's past that point is sunk cost the protocol is failing to interrupt. |
| "But this is exploratory research, the consumer can be vague." | Then the consumer is your next Purpose, and the next Purpose must be nameable. If even that is vague, the cycle is in Stage 0 territory — characterize data first, identify a candidate phenomenon, *then* set up a cycle whose consumer is the H1-test cycle. |
| "H1 landed clear NO, but I should still run H2 and H3 for completeness." | No. The NO branch landed; the consumer can apply the rule. Running H2/H3 anyway adds multiple-testing inflation (worse DSR trial counts) and wastes compute. Close at N=1, write the NO synthesis, propose follow-on Purposes if relevant. The "completeness" reflex is the same sunk-cost pattern N=5 exists to catch, just earlier. |
| "The H1 result was ambiguous — call it KICK-UP and move on." | Probably wrong. KICK-UP is for *structural frame mismatch* (the cycle's question is the wrong question), not for ambiguous metric ranges. Ambiguous results route to Fallback NO with scope-narrowing follow-up. KICK-UP requires a named structural finding (e.g., bug_review surfaces unresolvable upstream issue). |
| "The signal works in regime R only; that's a KICK-UP to a regime-conditional cycle." | No, that is Fallback NO with scope-narrowing (Pattern E). The cycle answered the original question (signal does not work broadly); the narrowed-scope cycle is a follow-on Purpose, not an upstream prerequisite. KICK-UP is reserved for cases where *no further H inside this frame can land a decision*. |

## Worked example (the funding-rate case from RED-3)

Pre-cycle:

```markdown
### Consumer
The next derived Purpose I will open after this notebook closes —
specifically, my own decision about whether to (a) keep iterating
on funding-rate signals at any horizon, (b) pivot to lower-frequency
funding strategies as a derived Purpose, or (c) abandon funding-rate
as an alpha source on this universe.

### Decision the consumer is currently blocked on
Whether the funding-rate signal on BTC perpetuals warrants further
research investment at all, and if so along which axis (horizon /
sizing / regime / capacity).

### Decision rule
- YES: at least one H supported with test PSR ≥ 0.95 net of 5 bp/side
  on BTC perp AND walk-forward positive-rate ≥ 60% AND no Pattern A
  binding axis. → Open next Purpose to characterize sizing / capacity.
- NO with binding axis = `fee_model`: ≥2 H rejected with `fee_model`
  shared as failure_mode AND break-even fee < 5 bp/side. → Open next
  Purpose at lower frequency.
- NO with binding axis = `regime_mismatch`: Pattern E surfaces, signal
  works only in low-vol regime. → Narrow abstract; open next Purpose
  scoped to that regime, or close lineage if low-vol regime is too
  rare.
- KICK-UP: bug_review surfaces unresolvable funding-history data
  contamination pre-2020. → Close cycle, open data-pipeline Purpose
  upstream.

### Knowledge output
Three rows in results.parquet (H1: core, H2: specification, H3:
regime-conditional) with verdict + failure_mode + achieved_tier;
Purpose-level synthesis paragraph naming Pattern (A-E); headline
cumulative-PnL figure with B&H + price-momentum upper baseline +
walk-forward Sharpe inset. Together: enough for the consumer to
apply the rule.
```

Now H1, H2, H3 in this notebook are no longer "axes I felt were
important"; each one closes a specific conjunct of the decision rule.
Cycle ends as soon as the consumer can apply one of YES / NO / KICK-UP
to the accumulated rows — N=5 is irrelevant if the rule fires at N=2.

## Failure patterns

- **Cycle started without consumer named** → return to this file before
  any code runs. The H1 you would have built is not aimed at anything
  yet
- **Decision rule has only YES and NO; no KICK-UP** → one of the most
  common omissions; without it, structural-frame failures get
  swallowed as ordinary rejections and the next Purpose inherits the
  wrong lesson
- **Cycle continues past consumer-decision satisfaction because "more
  evidence is better"** → it is not, under this frame: more evidence
  past decision satisfaction is sunk cost the protocol is meant to
  prevent. Close the cycle, propose follow-on Purposes if relevant,
  open the next notebook
- **H's added without a sub-claim mapping to the decision rule** → the
  H is not in the portfolio under this frame; it is freelance work
  serving no consumer. Either map it to a conjunct of the rule (and if
  necessary expand the rule to cover it, with justification in
  decisions.md) or drop the H
