# pr_promotion_gate.md

The Phenomenon / Mechanism Research promotion checklist. Run this before
declaring an explanation `supported` (i.e., the workstream claim has passed).
Like the R&D Workstream external-claim review path, this is a high
bar: every load-bearing item must pass with concrete evidence cited.

## When to read

- About to mark an E-row as `supported` in `explanation_ledger.md`
- Reviewing another agent's promotion claim
- Before the closing entry in `decisions.md` for an `answered`
  question

## Pre-conditions

The promotion gate may not start unless:

- PR/FAQ exists in the selected workstream, has `Status: READY`, and is
  linked from the project state
- Pre-registration for the cited trial(s) exists and had `Status: READY`
  before execution
- Transparent Changes for the cited report package exist and no material
  change invalidates claim-cited use
- IMRAD draft is producible per
  `references/pure_research/imrad_draft.md` § Sufficiency conditions
- Process review has run (`references/review/process_review.md`)
- Conclusion review has run (`references/review/conclusion_review.md`)

If any pre-condition is missing, state which one and stop.

## Checklist (every item required, evidence cited)

Format: `[ ] item — required evidence — citation`

### A. Planning integrity

- [ ] PR/FAQ exists and scoped the trial before it ran
  - Evidence: `prfaq.md` plus any later material-change entries in
    `decisions.md` or report package Transparent Changes
- [ ] Pre-registration exists for every cited trial
  - Evidence: `prereg/PR_<id>_<slug>.md`
- [ ] Each cited trial was run under a reviewed pre-registration
  - Evidence: `Status: READY` in `prereg/PR_<id>_<slug>.md` and trial notes that
    cite the matching PR ID
- [ ] No undocumented load-bearing PR/FAQ amendments (claim, mechanism,
  scope, alternatives, evidence role, or promotion language)
  - Evidence: current file plus Transparent Changes or decision entries for
    any material changes
- [ ] No undocumented pre-registration amendments
  - Evidence: same check on `prereg/PR_<id>_<slug>.md`; formatting-only changes do
    not count as amendments

### B. Transparent Changes

- [ ] Report package includes `Transparent Changes` for every cited trial
  - Evidence: `results/reports/RPT_<id>_<slug>/report.md` states
    "No material changes from the preregistration." or lists material changes
- [ ] Any material change is documented with description, rationale, and
  effect on study results or conclusions
  - Evidence: per-change entries include `Description of change`,
    `Rationale`, and `Effect on study results or conclusions`
- [ ] No material change invalidates claim-cited use
  - Evidence: Transparent Changes and trial notes either preserve the
    confirmation target or narrow / rerun the claim before promotion

### C. Discriminating test

- [ ] At least one discriminating test against ≥1 serious alternative
  was run
  - Evidence: trial notebook + the alternative E it discriminates
    against (cite both E-IDs)
- [ ] The alternative E-row is resolved for this promotion: it is
  `rejected` or `merged` by the trial. weakened is not terminal; a
  weakened alternative remains live unless further evidence rejects,
  merges, parks, or otherwise resolves it.
  - Evidence: explanation_ledger row for the alternative + trial that
    moved it
- [ ] All sibling E-rows under the parent Q are also at terminal
  status (rejected / merged / stale / parked)
  - Evidence: list each sibling E-ID and its terminal status

### D. Multiple testing correction

- [ ] Trial count is honest (every distinct hypothesis / parameter
  combination tried across this project counts, not just the one
  being promoted)
  - Evidence: enumerate trial IDs and parameter combinations
- [ ] Multiple-testing correction applied per
  project-specific multiple-testing plan (Bonferroni / Romano-Wolf
  step-down / domain-appropriate selection correction hurdle for new factors)
  - Evidence: corrected p-value or t-statistic citation
- [ ] If single test, t-statistic ≥ 3.0 (Harvey-Liu-Zhu hurdle for new
  domain claims)
  - Evidence: t-statistic value

### E. Analysis depth

- [ ] Trial Analysis section reaches A4 minimum (mechanism named,
  alternatives excluded, scope precise, multiple sources of
  supporting evidence)
  - Evidence: cite the trial notebook's Analysis § 5.4 (Tier rating)
    and § 5.3 (Evidence weighing)
- [ ] No generic terminal labels in the explanation
  - Evidence: read the IMRAD Discussion section; flag any
    "noise / regime / cost / model is good / data was clean"
    pattern that lacks decomposition

### F. IMRAD draft

- [ ] All four sections (Introduction, Methods, Results, Discussion)
  exist and meet sufficiency conditions per
  `references/pure_research/imrad_draft.md`
  - Evidence: file path + per-section check
- [ ] Discussion reaches A4+ analysis depth
  - Evidence: cite Discussion § 4.1 mechanism + § 4.2 alternatives
- [ ] Negative claims (rejected E's) documented in § 4.3 with same
  rigor as positive claims
  - Evidence: cite § 4.3
- [ ] Limitations honestly listed (≥3 specific limitations)
  - Evidence: cite § 4.4
- [ ] Methods cites the pre-registration file used by the cited trial
  (Section A check)
  - Evidence: file citation in § 2.1

### G. Reproducibility (presented evidence set)

- [ ] Data version, git commit, environment pin, and seed recorded for
  presented evidence in local run notes, report provenance, or tracker export
- [ ] All shared infrastructure pins recorded in
  `reproducibility/shared_pins.txt` or the tracker export
- [ ] Report provenance recorded for each cited evidence item via local note,
  results row, report provenance file, or equivalent external tracker record
- [ ] Presented evidence set covers the cited results, failed attempts, and
  parameter-sweep/model-selection runs used for trial-count and
  multiple-testing correction. Exploratory runs outside the claim family are
  not required.
- [ ] If an external tracker is used, `trial_id` resolves to a stable run ID
  and artifact URI containing the cited metrics, params, data version, git
  commit, environment pin, and seed

### H. Cold-eye check

This is the adversarial pass — the only check that uses material
withheld from the explanation_ledger and decisions.md. Read the IMRAD
draft cold, with the goal of producing at least one falsifying argument:

- [ ] Cold-eye reading attempted: read IMRAD draft alone (no
  explanation_ledger context, no author narrative); does the draft
  internally support the claim?
  - Evidence: cite specific IMRAD passages that pass / fail the
    independent reading
- [ ] At least one falsifying hypothesis attempted: assume the claim
  is wrong; what specific evidence in the draft, if reinterpreted,
  could support an alternative?
  - Evidence: state the falsifying hypothesis and whether evidence
    rebutted it

The cold-eye check is required for `supported` promotion. If a
plausible falsifying interpretation cannot be ruled out from the
draft alone, the claim is not yet supported (it is "supported within
project narrative", which is weaker than "supported as defensible
externally").

### I. Claim discipline

- [ ] Promotion claim phrased no stronger than evidence
  - Evidence: cite the proposed claim wording vs the supporting
    observation (must include scope conditions, must not generalize
    beyond tested scope)
- [ ] The `Claims` section in `explanation_ledger.md` is updated with
  the new `supported` row
  - Evidence: explanation_ledger Claims section row
- [ ] Scope conditions explicit (universe, period, regime, market
  structure preconditions)
  - Evidence: cite scope statement
- [ ] Negative claims (if any) added to `Claims` section
  - Evidence: explanation_ledger Claims section

## Promotion language

When a Pure Research claim promotes, the closing entry in `decisions.md`
uses this template:

```markdown
## YYYY-MM-DD Pure Research promotion (Q<id>: <Q-statement summary>)

PR/FAQ: prfaq.md
Pre-registrations (cited trials): PR_<id1>_<slug1>: prereg/PR_<id1>_<slug1>.md, PR_<id2>_<slug2>: prereg/PR_<id2>_<slug2>.md, ...
Transparent Changes: report package states "No material changes from the preregistration." or lists each Description of change, Rationale, and Effect on study results or conclusions

Supported claim: <one sentence, no stronger than evidence,
                  scope-explicit>
Mechanism: <causal mechanism, A4+>
Scope: <universe, period, regime, market structure preconditions>
Discriminating evidence:
  - vs E<id> (alternative): <evidence form + observation>
  - vs E_null: <evidence form + observation>
Negative claims (if any):
  - E<id>: rejected, mechanism: <...>, evidence: <...>

Multiple-testing correction: <method>, corrected statistic: <value>
Analysis tier: A<4 or 5>
Cold-eye check: <pass / specific reservations>

IMRAD draft: <path>
Report provenance: data version <...>, git commit <...>, environment pin <...>

Future work: <derived sub-questions or sibling project candidates>
```

## Failure modes blocked by this gate

| Failure mode | Where caught |
|---|---|
| Promote without pre-registration | Section A: pre-reg integrity |
| Promote with material change that should have invalidated confirmatory use under the original PR | Section B: Transparent Changes |
| Promote without discriminating test | Section C: discriminating test required |
| Sibling E's still active when promoting | Section C: all siblings must be terminal |
| Promote with single t > 2 from many trials (no multi-test correction) | Section D: trial count discipline |
| Promote with A2 analysis | Section E: A4 minimum |
| Promote with generic "regime change" explanation | Section E: no terminal labels |
| Promote without IMRAD draft | Section F: IMRAD producibility |
| Promote with wishful "no significant limitations" | Section F: ≥3 honest limitations |
| Promote with un-reproducible setup | Section G: 3-tuple recorded |
| Author narrative unchallenged | Section H: cold-eye check required |
| Claim broader than evidence | Section I: scope conditions explicit |

## Common failure modes during the gate

| Failure | Symptom | Fix |
|---|---|---|
| Skipping load-bearing items | "Mostly satisfies" or "obvious from context" | Each promotion-supporting item requires explicit citation |
| Citing other projects' work as evidence | "We found similar in another project" | Citation must be from this project's pre-reg + trials |
| Claiming supported on weakened E | E never reached `rejected`, just `weakened` | Run further discriminating test or accept that the alternative remains live |
| Skipping cold-eye check | "Looks good" | Cold-eye is structurally different; do the read |
| Claim wording too broad | "X is true" instead of "X holds under conditions Y" | Force scope conditions in the wording |
| Ignoring negative claims | E's that were rejected dropped from claim section | Negative claims are first-class; document them |

## Relationship to other references

- `references/pure_research/prfaq.md` (pre-condition for the gate)
- `references/pure_research/preregistration.md` (Transparent Changes policy)
- `references/pure_research/pr_workflow.md` (workflow rules; severity guidance
  for claim-cited confirmatory changes lives here)
- `references/pure_research/explanation_ledger_schema.md` (state
  object; promotion updates the Claims section)
- `references/pure_research/imrad_draft.md` (deliverable; sufficiency
  conditions checked in Section F)
- `references/shared/analysis_depth.md` (A4+ requirement for Section E)
- project-specific multiple-testing plan (Section D)
- `references/shared/result_analysis.md` (terminal label prohibition
  for Section E)
- `references/review/process_review.md` (must run before this gate)
- `references/review/conclusion_review.md` (must run before this gate)
- `references/shared/reproducibility.md` (3-tuple specification)
