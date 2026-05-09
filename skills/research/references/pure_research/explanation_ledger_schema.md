# explanation_ledger_schema.md

`explanation_ledger.md` — the single state object for a Pure Research
project. Tracks research questions and the explanations that compete to
answer them. Claim-cited or promotion-relevant results update explanation rows;
ordinary exploratory runs may remain as lightweight run notes until they become
load-bearing.

## When to read

- Before adding a question or explanation row
- Updating a row after a trial result
- Before declaring a claim `supported`
- Reviewing whether a Pure Research project's state is still consistent

## Position in the project

`explanation_ledger.md` is the Pure Research counterpart to R&D's
`capability_map.md`. It sits at the project root and is the primary
state surface. Trials feed into it; the IMRAD draft is generated from
it; the promotion gate reads it.

## Two-level hierarchy

The ledger has **questions (Q-rows)** and **explanations (E-rows)**.
Explanations are children of questions. A question may have N
explanations competing to answer it.

```
Q1 (research question)
├── E1 (explanation, mechanism A)
├── E2 (explanation, mechanism B)
└── E_null (null / artifact explanation)
Q2 (sub-question, derived from Q1)
├── E3
└── E4
```

Claim-cited trials operate at the explanation level: a discriminating test
weakens, strengthens, or rejects specific E-rows. Exploratory probes may remain
outside the ledger until they are rerun, cited, or used for a durable state
change.

## Schema for Q-rows (questions)

| Field | Type | Required | Description |
|---|---|---|---|
| `ID` | `Q1`, `Q2`, ... | yes | Sequential, never reused |
| `parent_Q` | `Qk` \| empty | optional | If this is a sub-question derived from a parent |
| `question` | string (1 sentence) | yes | The research question, framed as an unknown to reduce |
| `why_it_matters` | string | yes | Why answering this changes downstream understanding or practice |
| `current_best_answer` | string | yes (updated as evidence accumulates) | Concise summary of what the evidence currently supports |
| `Status` | enum | yes | active / answered / split / merged / stale / parked |
| `next_discriminating_step` | string | yes (if active) | The smallest next test that would advance this question |

## Schema for E-rows (explanations)

| Field | Type | Required | Description |
|---|---|---|---|
| `ID` | `E1`, `E2`, ... | yes | Sequential across the project, never reused |
| `parent_Q` | `Qk` | yes | The question this explanation is a candidate answer to |
| `statement` | string (1 sentence) | yes | The explanation's claim |
| `mechanism` | string | yes | The causal mechanism the explanation proposes |
| `supports` | string | yes | What observable evidence would strengthen this E |
| `weakens` | string | yes | What observable evidence would weaken this E |
| `current_evidence_summary` | string | yes | Best one-paragraph summary of the evidence so far |
| `last_trial` | trial_id \| empty | optional | Most recent trial that updated this E |
| `Status` | enum | yes | active / weakened / rejected / merged / supported / parked |
| `next_discriminating_step` | string | yes (if active) | What test would best discriminate E vs the closest sibling |

## Status vocabulary

### Question status

- `active`: still being investigated; explanations are still in play
- `answered`: one explanation reached `supported`; question has a stable
  answer
- `split`: decomposed into sub-questions (children get new Q-IDs); the
  parent stays for traceability
- `merged`: absorbed into another question (record absorbing Q-ID)
- `stale`: no longer relevant after a scope change
- `parked`: deferred with a named unblock condition

### Explanation status

- `active`: still in play; evidence so far is not decisive
- `weakened`: discriminating evidence reduced support, but not rejected
- `rejected`: discriminating evidence contradicts the explanation; it
  no longer accounts for the observed pattern
- `merged`: absorbed into another explanation (often when two E's
  collapse into one mechanism)
- `supported`: passed the promotion gate; this E is the current best
  answer to the parent question (only one E per Q can be `supported`
  at a time)
- `parked`: deferred with a named unblock condition

Allowed transitions:

```
active → weakened (new evidence reduces support but doesn't rule out)
active → rejected (new evidence contradicts predicted observation)
active → merged (collapses into another E)
active → supported (passes promotion gate)
active → parked
weakened → active (new evidence revives)
weakened → rejected (further evidence contradicts)
weakened → parked
rejected → (terminal, but kept for traceability)
supported → weakened (new evidence emerges; supported is conditional)
supported → rejected (new evidence definitively contradicts)
parked → active
```

`rejected` is not strictly terminal — a rejected E can still be cited
as part of project history, but it should not be revived without a
fresh pre-registration that explicitly addresses the contradiction.

## Required ledger sections

`explanation_ledger.md` has these required sections, in order:

```markdown
# Explanation Ledger — <project name>

## Mode
Pure Research. <One-sentence reason this is Pure Research not R&D.>

## Active questions
| ID | parent_Q | question | why_it_matters | current_best_answer | Status | next_discriminating_step |
|---|---|---|---|---|---|---|

## Explanations
| ID | parent_Q | statement | mechanism | supports | weakens | current_evidence_summary | last_trial | Status | next_discriminating_step |
|---|---|---|---|---|---|---|---|---|---|

## Claims (supported explanations only)
| Q-ID | E-ID | claim phrasing | scope conditions | promotion review date | IMRAD draft path |
|---|---|---|---|---|---|

## Retired / merged / stale
| ID | row type (Q/E) | new state | reason | date |
|---|---|---|---|---|
```

## State update discipline

Every claim-cited or promotion-relevant interpreted result should update at
least one row in the ledger when it changes support, scope, status, or the next
discriminating step. The update is one of:

1. An explanation's `current_evidence_summary` updates (new evidence
   accumulates without changing status)
2. An explanation transitions: active → weakened / rejected / merged /
   supported / parked
3. A question transitions: active → answered / split / merged
4. A new sub-question or explanation is added
5. The `next_discriminating_step` of an active row is refined (more
   precise test design after the most recent trial)

If exploratory work produces no state update, keep it in the trial artifact,
tracker, run note, or results row. Record `no progress: <reason>` in
`decisions.md` only when a named blocker prevents an intended durable state
transition.

## Promotion to `supported`

An explanation reaches `supported` only when **all** of:

- The Q's discriminating test against ≥1 serious alternative has been
  run under a frozen pre-registration
- `prereg_diff.py` exit code is 0 or 2 (no major deviations)
- Multiple testing correction is honest and applied per
  project-specific multiple-testing plan
- Analysis depth on the trial reaches A4 minimum (per
  `references/shared/analysis_depth.md`)
- A complete IMRAD draft is producible from the ledger + decisions +
  results (see `references/pure_research/imrad_draft.md`)
- Reproducibility 3-tuple recorded for the trial
- The promotion review (`references/pure_research/pr_promotion_gate.md`)
  passes

The phrasing in the `Claims` section must be **no stronger than the
evidence**. "We document a phenomenon X under conditions Y" is correct;
"X is true" is not.

## Negative claims are first-class

A `rejected` E-row is a research finding. A common pattern: a project
runs trials that progressively eliminate explanations, and the
deliverable is the documented elimination. These belong in the
`Claims` section as negative claims:

> Q1 / E2: rejected — "Regime-change explanation does not account for
> measurement reliability decay (measurement-noise stability test, p > 0.4 across
> period boundary, see trial_007)"

Negative claims have the same A4+ analysis-depth requirement as
positive `supported` claims.

## When a question is `answered`

A Q is `answered` when:

- One of its E's reached `supported` (the positive case), OR
- All of its E's reached `rejected` (the project established that no
  proposed explanation works — this is a real finding; the question
  is answered "none of the above", and a derived sub-question may be
  needed)

The `current_best_answer` field summarizes the answered state.
`answered` Q's are kept active in the ledger for traceability; do not
delete them.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Single explanation per Q | Only one E listed under each Q | Force ≥2 from PR/FAQ Part 2 (FAQ already enumerated alternatives) |
| Generic `supports` / `weakens` | "would support: yes; would weaken: no" | Each must name observable evidence type (numerical metric, structural argument, null result, literature ref) |
| Merging `supported` and `weakened` | Two E's both at status `weakened` indefinitely | At least one must transition to `rejected` or `supported` for the Q to progress |
| Adding new E mid-trial | Discovered alternative not in pre-reg | Counts as deviation; if major, requires new pre-reg |
| Skipping `parked` unblock | Row sits at `parked` for months without unblock | Re-evaluate; transition to `stale` if the unblock is unlikely |
| Promoting a row labeled `supported` while sibling E's not addressed | Sibling E's still at `active` | All siblings must reach a terminal state (rejected / merged / stale / parked) before the supported promotion |

## Relationship to other references

- Schema validated by `scripts/validate_ledger.py`
- Pre-registration drives explanation status changes — see
  `references/pure_research/preregistration.md`
- Promotion gate operates on this ledger — see
  `references/pure_research/pr_promotion_gate.md`
- IMRAD draft is generated from the ledger by
  `scripts/draft_imrad.py` per
  `references/pure_research/imrad_draft.md`
- Trial workflow per `references/pure_research/pr_workflow.md`
