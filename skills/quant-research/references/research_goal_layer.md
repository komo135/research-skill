# research_goal_layer.md

The four-layer model (Research goal / Design hypothesis / Purpose / Hypothesis)
that gives every hypothesis — including derived hypotheses generated mid-cycle —
an explicit anchor in the research goal.

## When to read

- **Before initializing a new project** (Step 0 in `SKILL.md`) — the project
  README's research-goal sub-claim list and the design-hypothesis log in
  `decisions.md` must be set up under this model
- **Before opening a new Purpose / new notebook** — the Purpose's `target_sub_claim_id`
  is required, and is a 5th item of the cycle goal (see
  `cycle_purpose_and_goal.md`)
- **Whenever a derived H is generated mid-cycle** — to check that the derived
  H is anchored to a research-goal sub-claim, not just to the previous H's
  numeric observation
- **At Purpose closure** — when updating the research-goal sub-claim
  progress in `decisions.md`

## The four layers

```
[Research goal]               project README — the question the project exists to answer
      ↓
[Design hypothesis]           decisions.md — the prediction "Purpose A solves goal sub-claim X"
      ↓
[Purpose]                     notebook — one open-ended question, one cycle
      ↓
[Hypothesis]                  ## H<id> block inside the notebook — falsifiable claim
```

The hypothesis at the bottom layer is what `research_design.md` and
`hypothesis_cycles.md` operate on. The Purpose is what `experiment_protocol.md`
and `cycle_purpose_and_goal.md` operate on. **The two upper layers (Research
goal, Design hypothesis) are this file's scope.** Without them, derived
hypotheses become locally driven by the previous H's numeric observation
and lose their anchor in why the project is running at all.

## Layer 1 — Research goal

A research goal is the question the *project* exists to answer. It does not
change Purpose-by-Purpose. It is decomposed into **research-goal sub-claims**
the project will produce evidence for or against.

### Form

The project's `README.md` carries a research-goal sub-claim list with stable
IDs:

```markdown
## Research goal

[One-sentence high-level question. Example: "Does JP equity quality-factor
stacking yield a live-tradeable strategy?"]

### Sub-claims

| ID | Sub-claim | Status |
|---|---|---|
| G1.1 | Quality factor (some signal in the family) yields net-of-cost edge in TOPIX500 | not started |
| G1.2 | The signal survives realistic execution constraints (live-tradeable) | not started |
| G1.3 | The signal stacks with other quality factors without canceling | not started |
```

### Where it lives

- **Authoritative location**: `notebooks/<project-name>/README.md`
- **Reference forms** (read-only from elsewhere): notebook Purpose headers,
  `hypotheses.md` rows, `decisions.md` Purpose entries

### How sub-claim IDs work

- IDs are stable within a project (`G1.1`, `G1.2`, …, `G2.1`, …) and never
  reused after retirement
- IDs are referenced by `target_sub_claim_id` in `hypotheses.md` and by the
  Cycle goal's 5th item in each notebook
- A research goal with 0 sub-claims is too vague to commit to and is treated
  as "not yet decomposed" — Stage 0 territory; characterize the data /
  consumer first
- A research goal with > 6 sub-claims is too broad to test in one project —
  split into project-level sub-projects, each with its own README

### Anti-rationalization: "the research goal is obvious, I don't need sub-claims"

Implicit research goal = the failure mode this layer exists to prevent. The
act of writing sub-claims down is what forces "what would `live tradeable`
mean numerically?" into the open. A project without explicit sub-claims
produces Purposes whose results cannot be cross-referenced against the
upper question — exactly the symptom the four-layer model fixes.

## Layer 2 — Design hypothesis

A design hypothesis is the **prediction** that running a particular Purpose
will close one or more research-goal sub-claims. It is the bridge from the
upper question to the cycle's `target_sub_claim_id`.

### Form

A design hypothesis is recorded in `decisions.md` at two moments:

1. **Before a Purpose opens** — in the Purpose entry's "Design hypothesis at
   open" line:

   ```markdown
   - Design hypothesis at open: opening Purpose A (TOPIX500 quality factor
     net-of-cost) will close sub-claim G1.1 (`quality factor yields net edge`)
     to `confirmed` or `falsified` regardless of the per-H verdict pattern;
     it does NOT touch G1.2 or G1.3 directly.
   ```

2. **At Purpose closure** — in the Purpose entry's "Design hypothesis at
   close" line, with verification:

   ```markdown
   - Design hypothesis at close: prediction CONFIRMED.
     G1.1 advanced from `not started` to `confirmed` (H2 met the YES branch
     of the decision rule with WF mean = 0.41). G1.2 and G1.3 are unchanged,
     as predicted.
   ```

   Or — equally valid — the prediction can be **falsified**:

   ```markdown
   - Design hypothesis at close: prediction FALSIFIED. G1.1 is unchanged
     (Purpose A failed to produce a clean YES or NO; binding axis = `turnover`,
     which is closer to G1.2 territory than to G1.1). Re-evaluation: G1.2
     should be tackled before G1.1 can be re-attempted, since turnover-cap
     is in the live-tradeability layer.
   ```

### Why this layer is required

Without an explicit design hypothesis, the act of choosing the next Purpose
is invisible:

- "Why open Purpose B = 3-factor extension after Purpose A succeeded?" — a
  question Purpose A's result alone cannot answer. The design hypothesis
  layer is where the answer lives ("Purpose A confirmed G1.1; G1.3 is the
  next sub-claim to attack; 3-factor extension tests G1.3")
- "Did Purpose A actually move the project forward?" — a question that
  collapses if no one wrote down what `move forward` means. The design
  hypothesis at close is where this is verified

### Where it lives

- **Authoritative location**: `decisions.md` Purpose entries (two lines —
  `at open` and `at close`)
- **Read-only references** elsewhere: notebook Purpose headers can name
  the `target_sub_claim_id` but do not restate the design hypothesis
  (= keep the notebook a research artifact, not a planning artifact —
  see `post_review_reconciliation.md`)

## Layer 3 — Purpose

A Purpose is the open-ended question one notebook investigates. The
Purpose's relationship to the research-goal layer is via **`target_sub_claim_id`**
— the cycle goal's 5th item (see `cycle_purpose_and_goal.md`).

A Purpose normally targets **1 sub-claim** as primary and may touch 1-2
others as secondary. A Purpose targeting > 3 sub-claims is too broad
(Pattern B in `cross_h_synthesis.md`); split.

## Layer 4 — Hypothesis

A Hypothesis is a falsifiable claim inside a notebook. Each H inherits its
`target_sub_claim_id` from the Purpose it serves, **and may additionally
declare a more specific sub-claim** if the Purpose's primary sub-claim
decomposes further. The H's row in `hypotheses.md` carries the
`target_sub_claim_id` column.

A derived H — one generated mid-cycle from H_n's result — inherits its
`target_sub_claim_id` from the parent H by default. Overriding is legal
but must be explicit ("H4 is derived from H3 but targets G1.2 rather than
G1.1, because the turnover finding shifted the question into the
live-tradeability layer"). The override is recorded in the row's `Reason`
column.

## The `target_sub_claim_id` link — operational rules

### When opening a Purpose

1. Read the project README's research-goal sub-claim list. Pick the
   primary sub-claim this Purpose will close (or attack — close to
   confirmed *or* falsified counts equally)
2. Write the `target_sub_claim_id` as the 5th item of the Cycle goal
   in the notebook header (see `cycle_purpose_and_goal.md`)
3. Write the design hypothesis at open in `decisions.md`

### When generating a derived H mid-cycle

1. Inherit `target_sub_claim_id` from the parent H by default
2. If the derived H reflects a shift in which sub-claim is being tested,
   override and record the reason in `hypotheses.md`'s `Reason` column
3. Do NOT write the override or the inheritance in the notebook body —
   the link lives in `hypotheses.md`

### When closing a Purpose

1. Apply the cycle's decision rule (Primary YES / Fallback NO with binding
   axis / KICK-UP — see `cycle_purpose_and_goal.md`)
2. Update the research-goal sub-claim status in `decisions.md`'s
   "Research-goal sub-claim progress update" section: each sub-claim
   the Purpose touched moves between {`not started`, `in progress`,
   `confirmed`, `falsified`}
3. Write the design hypothesis at close in `decisions.md`, marking the
   prediction CONFIRMED / FALSIFIED / PARTIAL
4. The next Purpose's selection is justified by which sub-claims are
   still `not started` or `in progress`, not by the previous Purpose's
   numeric observation alone

## What goes where (cheat sheet)

| Information | Lives in | Does NOT live in |
|---|---|---|
| Research goal + sub-claim list | `README.md` | Notebook body, `hypotheses.md`, `decisions.md` |
| Sub-claim status (not started / in progress / confirmed / falsified) | `decisions.md` Purpose entries | Notebook body, `hypotheses.md` |
| Design hypothesis (at open / at close) | `decisions.md` Purpose entries | Notebook body, `hypotheses.md` |
| Purpose's `target_sub_claim_id` | Notebook Cycle goal (5th item) | `decisions.md`'s Design hypothesis line restates it |
| H's `target_sub_claim_id` | `hypotheses.md` rows | Notebook body |
| H's `pathway` (1-6 from `hypothesis_generation.md`) | `hypotheses.md` rows | Notebook body |
| H's `parent_id` (for derived H) | `hypotheses.md` `Statement` column ("derived from H3") | Notebook body |
| H's classification (`planned-runnow` / `planned-nextsession` / `planned-drop` / etc.) | `hypotheses.md` `Status` column | Notebook body, `decisions.md` |
| H's falsifiable statement, abstract, observation, interpretation, verdict | Notebook body | `hypotheses.md` carries only the one-line statement |

The notebook body never carries `target_sub_claim_id` for individual H's,
classification states, or design-hypothesis prose. It does carry the
Purpose-level `target_sub_claim_id` (in the Cycle goal block, once) and
each H's research content (statement, evidence, interpretation, verdict).

## Failure patterns this model fixes

The patterns below appear when one or more of the four layers is collapsed
or implicit. The `quant-research` skill's RED test set documented them
under fixture IDs F15 / F16 (see `skill_tests/red_research_goal_layer/`).

### Pattern: derived H driven only by previous H's numeric observation

H1 returned a turnover problem; H2 was generated as "the natural next
step" (= add an independent axis). H2's anchor in the research goal is
not asked.

**Fix under this model**: H2's row in `hypotheses.md` must carry
`target_sub_claim_id`. If H2 still targets G1.1 (the same sub-claim H1
was attacking), the row inherits. If H2 actually shifts the question
into G1.2 territory (live tradeability — turnover-cap is closer to that
layer), the override is recorded in the `Reason` column. Either way, the
anchor is explicit.

### Pattern: next Purpose chosen by routing, not by sub-claim progress

Purpose A closed Primary YES; the researcher opens Purpose B = 3-factor
extension. The reason is "Sharpe might go higher with more factors". No
one asked which sub-claim B is attacking.

**Fix under this model**: B's design hypothesis at open in `decisions.md`
must name a `target_sub_claim_id`. If G1.1 is now `confirmed` and B
targets G1.3 (stacking), the design hypothesis says so explicitly. If B
re-targets G1.1 (= deeper exploration of an already-confirmed sub-claim),
the design hypothesis must justify why that's worth the trial-count cost
when G1.2 and G1.3 are still `not started`.

### Pattern: Purpose-level synthesis without research-goal distance update

`decisions.md`'s Purpose-level synthesis says "ROE × OCF margin works at
net 5 bp". The project-level question ("is JP equity quality factor
live-tradeable?") is unchanged.

**Fix under this model**: the Purpose entry's "Research-goal sub-claim
progress update" section is mandatory. Even when no sub-claim status
changed, the section is written ("G1.1: in progress — H2 met the YES
threshold but live-tradeability is not yet tested; G1.2: not started;
G1.3: not started"). The progress update is what the next Purpose's
design hypothesis reads.

## Anti-rationalizations

| Excuse | Reality |
|---|---|
| "The H's anchor in the research goal is obvious from context." | Then writing `target_sub_claim_id` costs nothing and removes the failure mode. Implicit anchors are the failure mode. |
| "I'll write the sub-claim status when I have time." | The status update is what justifies the next Purpose. Skipping it makes the next Purpose's design hypothesis vacuous. |
| "The design hypothesis is just paperwork; the cycle goal already covers it." | Cycle goal answers "what does this cycle output?" Design hypothesis answers "why this cycle, in what order, given the research goal?" — different question. |
| "If I write design hypotheses before Purposes, I'll be locked in." | The design hypothesis can be FALSIFIED at close — that is a legitimate research output, not a failure. Pre-commitment is what lets falsification be informative. |
| "Sub-claim IDs are over-engineering for a small project." | A project too small to need sub-claim IDs is one without 2+ Purposes. As soon as a 2nd Purpose opens, the question "why this one and not that one?" exists; the IDs are how that question gets answered. |
| "I have only one sub-claim, so the column is redundant." | Then every row's `target_sub_claim_id` says `G1.1` and the redundancy costs nothing. When a 2nd sub-claim is added later, the existing rows are already linked. |

## Compatibility with existing layers

This file does not invalidate `cycle_purpose_and_goal.md`,
`hypothesis_cycles.md`, `cross_h_synthesis.md`, or
`hypothesis_generation.md`. It adds the upper two layers above the
Purpose layer; the existing layers operate on Purpose and Hypothesis as
before. Specifically:

- The Cycle goal's 4 items (Consumer / Decision / Decision rule /
  Knowledge output) gain a 5th item (`target_sub_claim_id`); the
  semantics of the existing 4 are unchanged
- `hypothesis_cycles.md` routing (same notebook vs. new) is unchanged;
  the routing test is "Purpose continuity" and that is determined by
  `target_sub_claim_id` continuity in the same way it was determined by
  Purpose-statement continuity before
- `cross_h_synthesis.md` Pattern A-E mapping is unchanged; the new
  layer adds: at Purpose closure, the chosen Pattern's action is
  recorded with `target_sub_claim_id` impact
- `hypothesis_generation.md` Pathway 1-6 is orthogonal; an H declares
  `pathway` for its content origin and `target_sub_claim_id` for its
  anchor — both columns in `hypotheses.md`
