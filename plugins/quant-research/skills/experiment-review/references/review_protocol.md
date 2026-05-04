# review_protocol.md

Dispatch and aggregation mechanics for the experiment-review skill.

## Inputs the assistant must gather before dispatch

Before dispatching the four reviewers, collect the following into a context
bundle. The three specialist reviewers receive the shared bundle plus their own
group scope. The fourth reviewer, adversarial cold-eye, receives a different
minimum bundle.

| Item | Purpose |
|---|---|
| Notebook path under review | The primary artifact |
| Project root path | To find `hypotheses.md`, `decisions.md`, `literature/`, `purposes/INDEX.md` |
| Design-cell content (extracted) | The pre-registered question, hypothesis, thresholds |
| Abstract-cell content (extracted) | The claim being evaluated |
| Conclusion / "Cannot conclude" section content (extracted) | Generality claims to triangulate |
| Cycle history (`purposes/INDEX.md` summary) | For research-design cycle-honesty checks |
| Upstream feature-experiment paths, if any | For research-design feature-hygiene checks |
| Bug-review entry from `decisions.md`, if present | So evidence-sufficiency knows whether the prerequisite has been satisfied |

If any of these is missing, do not abort. Proceed and let the relevant reviewer
flag "missing artifact" as a `high`-severity finding. Graceful degradation is
required; abort only if the notebook itself is missing or unreadable.

## Per-reviewer input contract (efficiency-class, F21)

Each reviewer receives only its own grouped scope plus the shared artifacts
named below. Whole-file `review_dimensions.md` is not delivered to specialists.
Pre-extract the scope by section anchor (the `## N. <reviewer-name>` heading)
before dispatch. Anchor missing means the reviewer flags
`severity: high, dimension: <name>, what: missing input section §<N>`.

| # | Reviewer | Required scope (extract) | Required shared | NOT-receive |
|---|---|---|---|---|
| 1 | research-design | `review_dimensions.md` §1 (anchor `## 1. research-design`, question / scope / method) | `severity_rubric.md`, notebook .py, design-cell extract, `hypotheses.md`, `decisions.md`, `purposes/INDEX.md`, upstream feature notebook .py if named in design cell | `review_dimensions.md` outside §1, `literature/`, narrative refs, `bug_review.md`, other reviewers' findings |
| 2 | evidence-sufficiency | `review_dimensions.md` §2 (anchor `## 2. evidence-sufficiency`, validation / claim) | `severity_rubric.md`, notebook .py, design-cell extract, abstract-cell extract, conclusion / "Cannot conclude" extract, bug-review entry from `decisions.md` if present | `review_dimensions.md` outside §2, `literature/`, narrative refs, `hypotheses.md`, `bug_review.md` whole, other reviewers' findings |
| 3 | context-communication | `review_dimensions.md` §3 (anchor `## 3. context-communication`, literature / narrative) | `severity_rubric.md`, notebook .py, `literature/papers.md`, `literature/differentiation.md`, optional local notebook style guide if present | `review_dimensions.md` outside §3, `hypotheses.md`, `decisions.md`, `bug_review.md`, other reviewers' findings |
| 4 | adversarial (cold-eye) | `review_dimensions.md` §4 (anchor `## 4. adversarial`) — verbatim instruction only | notebook .py, `severity_rubric.md` (for output schema; not bias-inducing) | `review_dimensions.md` outside §4, `hypotheses.md`, `decisions.md`, `purposes/INDEX.md`, `literature/`, narrative refs, the three specialist findings, upstream feature notebooks, chat context |

**Section anchor as source of truth**: extraction reads the section by heading,
not by line range. A renamed or removed anchor surfaces a graceful-degradation
finding rather than being silently repaired.

**Adversary rule**: pre-extraction applies to the adversary too. It receives §4
only, no specialist scope, and no project context. The asymmetry is the
mechanism.

## Trigger-conditional dispatch on re-verify (efficiency-class, F22)

A typical H verdict='supported' attempt enters the gate multiple times: once on
initial pass, then again on each re-verify after fix reconciliation. The naive
contract, "fire all four every time", re-pays for unchanged surfaces. F22 splits
the dispatch into two cases.

### Initial pass

First time this H enters the gate, or first time in a new session without a
recorded clean baseline: **all 4 reviewers fire**.

### Re-verify pass

Triggered after the parent has applied fixes from a prior experiment-review
summary. The parent identifies which surface map entries the fixes touched and
fires only those specialist reviewers, plus adversarial whenever any specialist
re-fires.

If no specialist fires, nothing is being re-verified and the prior clean state
stands.

### Surface map per reviewer

| # | Reviewer | Surface (re-fire if any of these changed since last clean review) |
|---|---|---|
| 1 | research-design | H falsifiable statement, design cell, thresholds, cycle-hygiene markers, universe declaration, period range, instrument list, regime declaration, cross-section size, model selection cell, baseline cells, feature list, hyperparameter grid, retraining-cadence declaration |
| 2 | evidence-sufficiency | walk-forward window count, statistical-power claims, embargo-adequacy claims, CPCV setup statements, abstract cell, verdict cell, conclusion / "Cannot conclude" cell, deployment-readiness language |
| 3 | context-communication | `literature/papers.md`, `literature/differentiation.md`, novelty / differentiation-tier claims, any markdown cell, figure plan, per-figure observation cells, prose interpretation cells, helper-function docstrings |
| 4 | adversarial (cold-eye) | auto-fires whenever any specialist re-fires; no separate surface map because its scope is the full `.py` standalone |

### When in doubt, fire

Surface classification is the parent assistant's reasoning step. If a fix does
not fit any surface entry cleanly, or fits multiple ambiguously, default to
firing the affected candidates plus adversary. The gate skips redundant work,
not uncertain work.

### Cross-session boundary

The "last clean review" baseline is session-local. A researcher returning to
the same H next session has no in-context record of which reviewers were
verified clean, so the new dispatch is an Initial pass.

If a prior `decisions.md` entry explicitly states that reviewer set `{X, Y, Z}`
was verified clean against artifact state S, and the agent verifies the
relevant surfaces are unchanged from S, the agent may treat the next dispatch
as a re-verify. Without that attestation, treat as Initial.

## Dispatch

The four reviewers are dispatched in a single tool-call batch when sub-agents
are available:

1. `research-design`
2. `evidence-sufficiency`
3. `context-communication`
4. `adversarial`

Parallelism is required for the standard path. Sequential dispatch is the
single-agent fallback.

The adversarial reviewer is structurally different. Its bundle is intentionally
minimum: the `.py` file plus its own §4 instruction extract and severity rubric,
with no other inputs.

Each specialist prompt has this structure:

```
You are a specialist reviewer in the experiment-review skill. Your reviewer
group is [reviewer name].

Notebook under review (verbatim):
<verbatim notebook .py file body>

Severity rubric (verbatim):
<verbatim contents of severity_rubric.md>

Your scope and checklist (extracted from review_dimensions.md §[N], inline; the
rest of review_dimensions.md is NOT delivered):
<verbatim contents of review_dimensions.md §[N], extracted by section anchor>

Required shared artifacts for your reviewer group (per input contract, inline):
<e.g. abstract-cell extract, hypotheses.md content, literature/papers.md, ...>

Apply the checklist for your reviewer group. For each check, decide pass /
partial / fail with concrete evidence. Return findings only; do not modify any
file.

Specific items to chase (the parent assistant has already read the artifacts
and is pointing at concrete evidence; these are not exhaustive):
- <specific item 1, with line / section pointer>
- <specific item 2>
- ...

Output schema (one entry per finding):
- severity: high | medium | low
  dimension: research-design | evidence-sufficiency | context-communication
  subdimension: question | scope | method | validation | claim | literature | narrative
  where:    <notebook>:<cell-or-section>  (or "project-level")
  what:     <one-sentence statement>
  why:      <which check failed and what the evidence is>
  fix:      <concrete remediation or follow-up question>
  blocks_supported: yes | no
```

Do not deliver a narrative review; return only structured findings. Stay in
your reviewer group. If you notice something outside scope, ignore it; the
relevant group owns it.

### The "Specific items to chase" pattern

Including 3-7 reviewer-specific chase items is required when the parent
assistant has already read the notebook and project artifacts. The chase items
are observations, not conclusions. Phrase them as "X is the case; apply check Y"
rather than "X is wrong because Y".

## Adversarial reviewer dispatch

The fourth reviewer is dispatched in the same batch as the three specialists,
but with a different bundle and prompt.

**Bundle**:

- The `.py` file under review
- `severity_rubric.md`
- `review_dimensions.md` §4 only, pre-extracted by section anchor

NOT in the bundle: the three specialist findings, `literature/`,
`hypotheses.md`, `decisions.md`, `purposes/INDEX.md`, upstream feature
notebooks, chat context, prior-cycle discussion, or the parent assistant's
scratchpad.

**Prompt skeleton**:

```
You are a cold-eye external reviewer. The .py file you are about to read is the
only material you are given. Other materials are intentionally withheld so you
do not anchor on priors shared with the author or other reviewers.

Notebook under review (verbatim):
<verbatim notebook .py file body>

Severity rubric (verbatim):
<verbatim contents of severity_rubric.md>

Your scope and the two attack axes (extracted from review_dimensions.md §4,
inline; the rest of review_dimensions.md is NOT delivered):
<verbatim contents of review_dimensions.md §4, extracted by section anchor
"## 4. adversarial — cold-eye standalone reading">

Output schema (one entry per finding):
- severity: high | medium | low
  dimension: adversarial
  where:    <notebook>:<cell-or-section>
  what:     <one-sentence statement>
  why:      <which axis (claim-warrant or standalone-readability) and what the evidence is>
  fix:      <concrete remediation or follow-up question>
  blocks_supported: yes | no
```

Do not pass the adversarial reviewer the chase-item pattern used for
specialists. That injects parent-assistant priors.

## Aggregation

After all selected reviewers return, the assistant aggregates the findings into
a single structured review delivered inline. The skill does not write a review
report file and does not append to `decisions.md`.

1. Concatenate all findings, preserving severity, dimension, and subdimension
   tags.
2. Sort high, then medium, then low. Within each tier, group by reviewer order:
   research-design / evidence-sufficiency / context-communication /
   adversarial.
3. Compute the overall verdict per `severity_rubric.md`.
4. Return the aggregated review with verdict, finding counts, and every
   individual finding's full schema entry.
5. If the user wants a durable record, they can copy the inline review into
   `decisions.md`; the skill itself stays read-only.

## Anti-rationalizations (efficiency-class, F21 / F22)

| Excuse | Why it is wrong |
|---|---|
| "Whole-file `review_dimensions.md` is safer." | Each specialist group has a structured scope. Whole-file delivery dilutes attention and collapses the input contract. If another section is genuinely needed, update the contract. |
| "The adversary should also receive specialist context." | The asymmetry is the mechanism. Giving adversary access to project context makes it another same-prior reviewer, not a cold-eye reader. |
| "User asked for a comprehensive review, so safer to send whole files." | Comprehensive comes from running all four reviewer groups, not from each reviewer reading every reference whole. |
| "The fix is small, just re-fire all 4 to be safe." | The surface map exists to skip redundant work. Ambiguous fixes fire candidates plus adversary; clearly local fixes do not need the full set. |
| "I'm unsure which surface this touches, default to skipping." | Default is fire, not skip. Ambiguity is not a redundancy signal. |
| "Cross-session: I remember the prior verdict was clean." | Without an explicit recorded clean baseline and unchanged surfaces, cross-session is Initial. |

## Single-agent fallback

When parallel dispatch is unavailable:

1. Run the four reviewer groups sequentially in four distinct passes.
2. Between passes, re-read the notebook from scratch. Do not rely on stale notes
   from the previous pass.
3. Treat each pass's output as if it came from a different reviewer.
4. Run the adversarial pass with the minimum bundle only. Do not give it earlier
   pass findings.
5. F21 input pre-extraction and F22 trigger-conditional dispatch still apply.
6. Aggregate the same way.

The fallback is worse than parallel dispatch, but four focused passes are still
better than one mixed-scope pass.

## When findings disagree

Two reviewers can produce overlapping or contradictory findings. For example,
research-design may flag a SPY-only-to-US-equities leap as scope overreach while
evidence-sufficiency flags the same issue as claim overstatement. Keep both
findings. Independent vantage points are evidence, not redundancy.

If two findings genuinely contradict, log both verbatim and resolve by reading
the underlying artifact or by raising a follow-up question. Do not silently pick
the convenient one.

## Output location and retention

The review is delivered inline in the assistant's reply. The skill does not
create a `reviews/` folder, write any file, or modify `decisions.md`.

## What the assistant does not do

- Do not modify the notebook under review during the review pass.
- Do not run code from the notebook. Reviews are based on reading artifacts.
  Re-execution belongs in `bug_review`.
- Do not call this skill recursively on its own report.

## Trigger discipline

A "review" that delivers a narrative without:

- four reviewer groups explicitly addressed,
- severity tags on every finding,
- a clearly visible verdict line and finding counts,
- the adversarial reviewer running with the minimum bundle,

has not actually run this skill. Do not declare a review verdict from it.
