# pr_promotion_gate.md

The Pure Research promotion checklist. Run this before declaring an
explanation `supported` (i.e., the project's claim has passed). Like
the R&D promotion gate, this is the highest bar: every load-bearing item must
pass with concrete evidence cited.

## When to read

- About to mark an E-row as `supported` in `explanation_ledger.md`
- Reviewing another agent's promotion claim
- Before the closing entry in `decisions.md` for an `answered`
  question

## Pre-conditions

The promotion gate may not start unless:

- PR/FAQ frozen and on file (`prfaq.md` + `prereg/prfaq.lock`)
- Pre-registration for the trial(s) backing the claim is frozen
  (`prereg/PR_<id>.md` + `prereg/PR_<id>.lock`)
- `prereg_diff.py` has been run with exit code 0 or 2 (no major
  deviations)
- IMRAD draft is producible per
  `references/pure_research/imrad_draft.md` § Sufficiency conditions
- Process review has run (`references/review/process_review.md`)
- Conclusion review has run (`references/review/conclusion_review.md`)

If any pre-condition is missing, state which one and stop.

## Checklist (every item required, evidence cited)

Format: `[ ] item — required evidence — citation`

### A. Pre-registration integrity

- [ ] PR/FAQ exists, frozen, hash matches `prereg/prfaq.lock`
  - Evidence: `prereg/prfaq.lock` SHA-256 == sha256sum of `prfaq.md`
- [ ] Pre-registration of the trial exists, frozen, hash matches
  `prereg/PR_<id>.lock`
  - Evidence: lock file vs file hash comparison
- [ ] Pre-registration timestamp predates trial execution timestamp
  - Evidence: `prereg/PR_<id>.lock` UTC timestamp vs trial result
    timestamp in `results.parquet`
- [ ] No undocumented load-bearing PR/FAQ amendments (claim, mechanism,
  scope, alternatives, evidence type, or promotion language)
  - Evidence: lock / git history reviewed against deviation entries
- [ ] No undocumented pre-registration amendments
  - Evidence: same check on `prereg/PR_<id>.md`; formatting-only changes do
    not count as amendments

### B. Deviation severity

- [ ] `prereg_diff.py` exit code is 0 or 2 (no major deviations)
  - Evidence: latest run output captured in `decisions.md`
- [ ] If exit code 2, all minor deviations are documented in
  `decisions.md` with rationale
  - Evidence: per-deviation `decisions.md` entry

### C. Discriminating test

- [ ] At least one discriminating test against ≥1 serious alternative
  was run
  - Evidence: trial notebook + the alternative E it discriminates
    against (cite both E-IDs)
- [ ] The alternative E-row is in terminal status (rejected /
  weakened / merged) by the trial
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
  `references/shared/multiple_testing.md` (Bonferroni / Romano-Wolf
  step-down / DSR / Harvey t > 3.0 hurdle for new factors)
  - Evidence: corrected p-value or t-statistic citation
- [ ] If single test, t-statistic ≥ 3.0 (Harvey-Liu-Zhu hurdle for new
  financial factors)
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
- [ ] Methods cites pre-reg hash; this hash matches the lock file
  (Section A check)
  - Evidence: hash citation in § 2.1

### G. Reproducibility (per cited trial)

- [ ] `reproducibility/data_hashes.txt` lists every data source used,
  with hash
- [ ] `reproducibility/uv.lock` exists and is the env used at
  promotion-eligible trial
- [ ] `reproducibility/seed.txt` lists random seeds; if multiple seeds
  used, all are recorded
- [ ] All shared infrastructure pins recorded in
  `reproducibility/shared_pins.txt`
- [ ] Reproducibility 3-tuple recorded for each cited trial via
  `scripts/reproducibility_stamp.py`

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

PR/FAQ hash: <SHA-256 from prereg/prfaq.lock>
Pre-reg hashes (cited trials): PR_<id1>: <hash>, PR_<id2>: <hash>, ...
prereg_diff status: exit 0 (clean) or exit 2 (minor deviations
                    documented in decisions.md entries Y, Z)

Supported claim: <one sentence, no stronger than evidence,
                  scope-explicit>
Mechanism: <causal mechanism, A4+>
Scope: <universe, period, regime, market structure preconditions>
Discriminating evidence:
  - vs E<id> (alternative): <evidence type + observation>
  - vs E_null: <evidence type + observation>
Negative claims (if any):
  - E<id>: rejected, mechanism: <...>, evidence: <...>

Multiple-testing correction: <method>, corrected statistic: <value>
Analysis tier: A<4 or 5>
Cold-eye check: <pass / specific reservations>

IMRAD draft: <path>
Reproducibility 3-tuple: data hash <...>, git commit <...>, env hash <...>

Future work: <derived sub-questions or sibling project candidates>
```

## Failure modes blocked by this gate

| Failure mode | Where caught |
|---|---|
| Promote without pre-registration | Section A: pre-reg integrity |
| Promote with major deviation that should have invalidated trial | Section B: prereg_diff exit code |
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
- `references/pure_research/preregistration.md` (deviation severity
  matrix consumed here)
- `references/pure_research/pr_workflow.md` (workflow rules; deviation
  matrix lives here)
- `references/pure_research/explanation_ledger_schema.md` (state
  object; promotion updates the Claims section)
- `references/pure_research/imrad_draft.md` (deliverable; sufficiency
  conditions checked in Section F)
- `references/shared/analysis_depth.md` (A4+ requirement for Section E)
- `references/shared/multiple_testing.md` (Section D)
- `references/shared/result_analysis.md` (terminal label prohibition
  for Section E)
- `references/review/process_review.md` (must run before this gate)
- `references/review/conclusion_review.md` (must run before this gate)
- `references/shared/reproducibility.md` (3-tuple specification)
