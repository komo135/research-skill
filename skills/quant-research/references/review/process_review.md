# process_review.md

Process review — was the discipline followed? This is the first of two
review axes (the other is `conclusion_review.md` for claim warrant).
Both must pass before any `matured` (R&D) or `supported` (Pure Research)
promotion.

## When to read

- Before running the promotion gate
  (`rd_promotion_gate.md` / `pr_promotion_gate.md`)
- Reviewing another agent's promotion claim
- Auditing a project mid-stream when "something feels off" about the
  process

## Purpose

Process review checks that the protocol was followed. It does not
check the conclusion — that's `conclusion_review.md`. The split is
deliberate: a buggy implementation can produce numbers that look
correct (caught by conclusion review), but a process violation
(skipped pre-registration, mid-trial goalpost shift) corrupts every
downstream check (caught here).

**Process review separates blocking violations from logged gaps**. A
load-bearing process violation blocks promotion; a non-load-bearing record gap
is logged and may narrow the claim or require cleanup, but does not by itself
kill promotion eligibility.

## How to run

This is an agent-self-executable checklist. The agent (or reviewer)
walks each item below and writes:

```
- [x] item — evidence: <file:line, hash, or specific observation>
- [ ] item — FAIL: <what's missing or violated>
- [ ] item — N/A (justify why)
```

"Looks good" / "obvious from context" / "I think this is OK" are forbidden.
Load-bearing passes require a specific citation. Lightweight process checks may
use a concise summary when they are not used to support promotion.

## Common pre-conditions (both modes)

These checks apply regardless of discipline:

- [ ] **Mode is explicitly declared** in `README.md` and matches the
  decisions log
  - Evidence: `README.md` Mode field + `decisions.md` first entry
- [ ] **No mode mixing**: project hasn't silently switched between
  R&D and Pure Research mid-stream
  - Evidence: `decisions.md` reviewed for any pivot — if pivoted, the
    pivot protocol per `SKILL.md` § First Decision was followed
    (suspend+restart or add secondary project, both with explicit
    `decisions.md` entry)
- [ ] **Session-end ritual followed for durable state changes**: sessions
  that changed ledgers, claims, gates, or promotion evidence have either a
  ledger row update or `no progress: <reason>` entry in `decisions.md`
  - Evidence: scan `decisions.md` for chronological coverage of state
    transitions; gaps are findings only when durable work occurred without a
    corresponding entry
- [ ] **Decision-log covers major project events**: `decisions.md`
  has entries for ALL major decision categories that should exist
  for this project's stage:
  - For R&D: Layer 1 closure entry, each Stage gate entry (per
    capability), any fired kill criterion (with A4 decomposition),
    every charter deviation, integration-test clearance
  - For Pure Research: PR/FAQ freeze entry, each pre-registration
    freeze, each `prereg_diff.py` exit code logged per trial, each
    explanation status transition, every PR/FAQ deviation
  - Evidence: per-category presence check; absence of expected
    entries is a process gap (not a violation, but flag)
  - Failure mode: `decisions.md` has 1 entry for kill relaxation but
    0 entries for Layer 1 closure / Stage gates / integration
    clearance — incomplete audit trail
- [ ] **Initial-day prohibitions respected**: no implementation /
  trial execution on day 1; only setup, scaffolding, charter / PR/FAQ
  - Evidence: review first 1-2 days' commits and decisions; flag any
    code execution that produced metrics before charter / pre-reg
    was frozen
- [ ] **Reproducibility 3-tuple stamped** on every promotion-eligible or claim-cited trial via `scripts/reproducibility_stamp.py`
  - Evidence: persisted JSON stamp record in `results.parquet`, the trial
    analysis section, or another durable run log showing data hash + git
    commit + env lock hash
- [ ] **Frozen artifacts not edited in place**: charter, PR/FAQ,
  pre-registration files have hash matching their `.lock` files
  - Evidence: `git log` + hash comparison

## R&D mode process audit

For R&D projects only. Check in this order:

### Charter (per `references/rd/rd_charter.md`)

- [ ] **Charter exists** at project root (`charter.md`)
  - Evidence: file path + size > 0
- [ ] **Charter is frozen** (`prereg/charter.lock` exists, hash matches)
  - Evidence: `sha256sum charter.md` == content of `charter.lock`
- [ ] **All 8 Heilmeier questions answered** with concrete content
  (no `<REPLACE: ...>` markers, no `TBD`)
  - Evidence: regex scan against `<REPLACE` and `TBD`/`TODO`/`???`
- [ ] **H6 kill criteria are concrete and observable** (numeric or
  behavioral threshold, not "if it doesn't work")
  - Evidence: read each H6 entry; verify it names a specific metric
    + threshold + condition
- [ ] **H7 distinguishes one-time vs recurring cost**
  - Evidence: § 7 has both subsections filled (or "N/A — all
    永続型" justified)
- [ ] **H8 is lifecycle-aware**: if any K is `継続改善型`, final exam
  references the maintenance plan
  - Evidence: § 8 + Layer 1 lifecycle assignments cross-referenced

### Layer 1 (Core Technologies)

- [ ] **Layer 1 closed-for-work before any capability was written**
  per `references/rd/core_technologies.md` § Layer 1 closure
  - Evidence: `decisions.md` shows Layer 1 closure entry timestamped
    BEFORE any Section 2 row appears in `capability_map.md` git
    history
- [ ] **Operational filter applied per K**: each K's
  `decisions.md`-recorded justification names which Conditions 0-3
  it passes
  - Evidence: per-K justification in `decisions.md` or
    `capability_map.md` Section 1
- [ ] **No K is a dependency masquerading as core tech** (Condition 1
  failure)
  - Evidence: each K has a research question, not just "use X library"
- [ ] **No coupled K's** (Condition 2 failure — sibling K's that
  cannot be tested independently)
  - Evidence: per-K independence justification
- [ ] **Lifecycle (永続型 / 継続改善型) explicitly assigned per K**,
  not defaulted
  - Evidence: each K row has the field filled with rationale
- [ ] **Operational filter Condition 0 (merge test) applied**: no two
  K's with > 50% conceptual overlap in research question
  - Evidence: cross-K question comparison

### Layer 2 (Capabilities)

- [ ] **Every capability has `core_tech_id` set** (or `integration`)
  - Evidence: `validate_ledger.py` output
- [ ] **Capability granularity rule respected**: each capability
  sized for one test → one TRL transition
  - Evidence: per-capability `exit_criteria` is a single concrete
    observable
- [ ] **Kill criteria A4-anchored**: every fired kill has an A4
  decomposition in `decisions.md` (per
  `references/rd/capability_map_schema.md`)
  - Evidence: per-kill log entry has Observation / Decomposition /
    Evidence weighing / Tier rating / Gap
- [ ] **TRL skip not detected**: no single state-change advanced TRL
  by > 1
  - Evidence: `validate_ledger.py` TRL transition check
- [ ] **Stage gates ran in order**: Scoping → De-risk → Build →
  Validate → Integrate; no Stage gate ran while Layer 1 was
  incomplete
  - Evidence: `decisions.md` Stage gate entries timestamped vs Layer
    1 closure timestamp

### Capability maturity dependency ordering

- [ ] **For every capability C_i with `depends_on` upstream
  capabilities, the timestamp of C_i's `matured` transition is later
  than every upstream capability's `matured` timestamp**
  - Evidence: `results.parquet` or `decisions.md` matured timestamps
    per capability; for each dependency edge in
    `capability_map.md` Section 2 `depends_on` field, verify no
    time-reversal
  - Failure mode: C5 matured AFTER C6 (which depends on C5) — C6
    consumed an unmatured upstream
- [ ] **Integration test ran AFTER all upstream `matured` timestamps**
  (special case of dependency ordering applied to the integration
  capability)
  - Evidence: timestamp comparison from `results.parquet` or
    `decisions.md`

### Cross-project dependencies

- [ ] **Every `dependent_on_research` capability has the named Pure
  Research project at the required tier**
  - Evidence: cross-reference to source project's
    `explanation_ledger.md` Claims section

## Pure Research mode process audit

For Pure Research projects only. Check in this order:

### PR/FAQ (per `references/pure_research/prfaq.md`)

- [ ] **PR/FAQ exists** at project root (`prfaq.md`)
- [ ] **PR/FAQ is frozen** (`prereg/prfaq.lock` exists, hash matches)
- [ ] **Part 1 (Press Release) is concrete**: states the finding,
  mechanism, scope, alternatives ruled out, evidence type
  - Evidence: read Part 1; verify all 5 elements present
- [ ] **Part 2 (FAQ) has ≥10 entries** covering statistical sufficiency,
  robustness, mechanism, alternatives, replication, scope, practical
  implication, HARKing risk
  - Evidence: count Q's; verify topic coverage

### Targeted literature

- [ ] **Targeted literature search happened AFTER PR/FAQ freeze**
  (PR/FAQ scopes the search; reverse order risks unfocused search)
  - Evidence: `decisions.md` literature search entry timestamp vs
    `prfaq.lock` timestamp
- [ ] **Literature is genuinely targeted**: papers cited in
  `literature/papers.md` relate to the PR/FAQ question, not generic
  topic browsing
  - Evidence: per-paper `relation to this research` field is
    specific (not "background")

### Pre-registration

- [ ] **Pre-registration exists** for every cited trial
  (`prereg/PR_<id>.md` + `.lock`)
- [ ] **Pre-registration timestamp predates trial execution timestamp**
  - Evidence: `prereg/PR_<id>.lock` UTC vs trial result timestamp in
    `results.parquet`
- [ ] **≥2 competing explanations + null enumerated** per pre-reg
- [ ] **Each E has evidence type declared** (causal / correlative /
  null-result) per `references/pure_research/preregistration.md` § 2
- [ ] **Each E has ex ante predicted observation** (not just "we will
  measure X")
- [ ] **Multiple-testing correction method specified** in pre-reg
  § 3.5 with honest trial count

### Trial execution

- [ ] **`prereg_diff.py` ran with exit 0 or 2** (no major deviations)
  for every cited trial
  - Evidence: `decisions.md` records the exit code per trial
- [ ] **Major deviations triggered new pre-registration**: if any
  trial had a major deviation, the trial is marked frozen and a new
  pre-reg PR_<id+1> is on file
  - Evidence: per-major-deviation entry in `decisions.md`
- [ ] **Sanity checks ran before main test** in trial notebooks
  - Evidence: trial notebook § Sanity checks cell + pass status
- [ ] **No post-hoc explanation addition**: any post-trial candidate
  E's are clearly flagged as not-pre-registered and parked for
  future trials (per `pr_workflow.md`)
  - Evidence: trial notebook § 6.2 Decomposition flags

### HARKing prevention checklist

(Per D-19 / C2.13 — a focused subset of pre-reg discipline checks
specifically targeting Hypothesizing After Results are Known)

- [ ] **Pre-reg hash predates first data inspection** for the trial
  (no shopping trip)
  - Evidence: `prereg/PR_<id>.lock` timestamp vs first data-load
    log entry
- [ ] **No "alternative pre-registration" patterns**: no
  pre-registrations on file that were not used by an actual trial
  - Evidence: `validate_ledger.py` flags unused pre-regs
- [ ] **Test design byte-for-byte matches pre-reg**: trial notebook
  § Trial design (copied from frozen pre-reg) is identical to
  `prereg/PR_<id>.md` § 3
  - Evidence: text diff; any difference is a deviation that should
    appear in `prereg_diff.py` output
- [ ] **Threshold not changed after seeing data** (goalpost shifting)
  - Evidence: `prereg_diff.py` major-deviation row for "threshold
    changed after seeing data" is empty
- [ ] **All pre-registered secondary tests reported**, not just
  favorable ones
  - Evidence: trial notebook § 4 Observation lists every secondary
    test in pre-reg, with status (pass / fail / N/A with reason)
- [ ] **Multiple-testing trial count is honest** — includes prior
  trials in this project, not just the current one
  - Evidence: pre-reg § 3.5 trial count vs project trial count from
    `results.parquet`
- [ ] **No mid-trial competing E addition**: any new candidate E
  identified during analysis is parked for a future pre-registered
  trial, not added to the current trial's discrimination
  - Evidence: trial notebook § 6.2 marks post-hoc E's clearly

### Explanation ledger update

- [ ] **Every cited trial moved at least one ledger row**
  - Evidence: per-trial entry in `decisions.md` names the row that
    moved
- [ ] **No `weakened`/`rejected` E was re-opened to `active` without
  a new pre-registration** (per
  `references/pure_research/explanation_ledger_schema.md` allowed
  transitions)
  - Evidence: ledger transition history; any re-open requires new
    PR_<id> on file

### IMRAD draft

- [ ] **IMRAD draft started after PR/FAQ freeze** (not deferred to
  promotion review)
  - Evidence: `imrad_draft.md` first commit timestamp ≤ PR/FAQ
    freeze timestamp + ~1 week
- [ ] **Sections 1-2 (scaffolding) updated as pre-reg / literature
  evolved**; Sections 3-4 only filled after trials with required
  analysis depth
  - Evidence: `imrad_draft.md` git history shows incremental updates,
    not a single end-of-project commit
- [ ] **Methods § 2.5 lists every deviation** from pre-registration
  (or states "none")
  - Evidence: cross-reference with `prereg_diff.py` outputs

## Common process violations

| Violation | Symptom | Where caught |
|---|---|---|
| Mode mixing without pivot protocol | R&D ledger has Pure Research artifacts (PR/FAQ, prereg) without `decisions.md` pivot entry | Common pre-conditions § Mode mixing |
| Implementation on day 1 | Code commits before charter / PR/FAQ freeze | Common pre-conditions § Initial-day prohibitions |
| Charter rewritten mid-project | `git log charter.md` count > deviation entry count | R&D § Charter, no undocumented amendments |
| Layer 1 incomplete when Layer 2 work started | Section 2 rows in `capability_map.md` git history before Layer 1 closure entry | R&D § Layer 1 |
| TRL skip via single-update transition | TRL advances by > 1 in single state change | R&D § Layer 2 § TRL skip |
| Integration test ran before upstream matured | Integration timestamp earlier than upstream `matured` timestamps | R&D § Integration test ordering |
| Post-hoc pre-registration | `prereg/PR_<id>.lock` timestamp after trial result timestamp | PR § Pre-registration timestamp predates trial |
| Major deviation treated as minor | `prereg_diff.py` exit 1 followed by "we'll just document it" | PR § Trial execution § major deviations |
| HARKing via shopping trip | Data inspection before pre-reg lock | HARKing checklist § pre-reg hash predates inspection |
| Multiple-testing under-reporting | Headline DSR computed with low N when project ran many configurations | HARKing checklist § honest trial count |
| Generic terminal labels in conclusions | "model is good" / "regime suited" / "noise" patterns | Caught in `conclusion_review.md` analysis depth axis |

## Outcome of process review

- **All load-bearing checks pass with citations** → process review CLEAN; proceed
  to `conclusion_review.md`
- **Any load-bearing check fails or N/A without justification** → process
  review FAILED; cannot proceed to promotion until fixed or the claim is
  narrowed so it no longer depends on the failure
- **Process review report** written into `decisions.md` under section
  `## YYYY-MM-DD Process review for promotion of <X>`

The report includes:
- Date and reviewer (agent / user)
- Each check + status (pass / fail / N/A) + evidence citation
- Failed items + remediation plan or rejection of promotion
- Sign-off: process review clean / fail

## Relationship to other references

- Pre-condition for `references/review/conclusion_review.md` (must
  run before)
- Required by `references/rd/rd_promotion_gate.md` § Pre-conditions
  and `references/pure_research/pr_promotion_gate.md` § Pre-conditions
- Process discipline defined in
  `references/rd/rd_workflow.md`, `references/rd/rd_stages.md`,
  `references/rd/core_technologies.md`,
  `references/pure_research/pr_workflow.md`,
  `references/pure_research/preregistration.md`
- HARKing prevention discipline elaborated in
  `references/pure_research/preregistration.md` § HARKing prevention
  discipline
