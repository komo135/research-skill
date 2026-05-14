# outcome_reports.md

Use this reference when preregistered work produces a user-facing report. The
report is a readable outcome artifact, not a second state ledger and not a
complete archive of every intermediate file.

## Report quality contract

The report quality contract is reader-facing: a reader can identify the
decision, evidence, plan comparison, limitations, and next action without
opening notebooks or ledgers. Report contracts apply to report packages and
presented evidence, not to research or experiments. Evidence integrity checks
are a reporting-side requirement, not a continuous research tracking contract.

Use one of these decision labels: `supported`, `not supported`,
`inconclusive`, `decision deferred`, `exploratory only`, or `blocked`.

## Package shape

All preregistered or claim-bearing work that produces a formal report package
uses this package shape. Required core files and directories:

```text
results/reports/
  RPT_<id>_<slug>/
    report.md
    report.html
    figures/
    tables/
    attachments/
```

Required core directories may be empty when the report has no figures, tables,
or attachments.

Optional / situation-specific files:

```text
results/reports/
  RPT_<id>_<slug>/
    report.pdf
    provenance/
      manifest.json
      integrity_checks.md
      rerun.md
```

In plain terms, report.html is the primary readable artifact for L2/L3
reports; report.md is editable source; report.pdf is optional snapshot/export.
Use provenance/ for claim-bearing or L2/L3 reports. L2/L3 reports means
claim-bearing reports and state-promotion or terminal-decision report
packages; it is report package level, not analysis tier. In provenance/,
include `manifest.json`, `integrity_checks.md`, and `rerun.md`.
Figures and tables that appear in the readable report should have source files
in `figures/` or `tables/`. Use `attachments/` only for small supporting files
needed to read the report. Use `provenance/` for command logs, hashes, and
source pointers that support the report. Do not copy large source data or
intermediate artifacts unless they are small and necessary.

Local paths may appear in `report.md` or the provenance appendix, but they
should not dominate the report. External tracker run IDs are optional and
should appear only when a tracker was actually used.

## Required sections

Every formal report package for preregistered or claim-bearing work includes:

1. Executive Decision
2. Research Stage and Claim Boundary
3. Preregistration Reference
4. Plan-to-Result Table
5. Key Evidence
6. Evidence Integrity Checks
7. Transparent Changes
8. Reproducibility Capsule
9. Scope / Limitations / Alternative Explanations
10. Next Action

Confirmatory reports emphasize hypotheses, decision criteria, and whether the
planned analysis was completed. Exploratory reports emphasize scope, patterns,
diagnostics, and follow-up.

## Plan-to-Result Table

Use this table to map planned items to execution and evidence:

```text
planned_item | executed_as_planned | result_summary | evidence | notes
```

Evidence should point to a figure, table, appendix, local source artifact, or
citation. It does not require a tracker run ID.

## Evidence Integrity Checks

For each key numeric, boolean, categorical, and count claim in the report, add
a claim-to-artifact check row:

```text
claim_id | reported_value | cited_artifact_path | commit_or_hash | extraction_method | observed_source_value | comparison_status | generating_command_or_entrypoint
```

The check only covers claims presented in the report. It is not a requirement
to continuously track every research step. Failed, missing, or not run cannot
be treated as supported.

## Transparent Changes

If no material changes occurred:

```markdown
No material changes from the preregistration.
```

If material changes occurred, list each one:

```markdown
### Change <n>: <short name>
- Description of change:
- Rationale:
- Effect on study results or conclusions:
```

Effects should be honest about uncertainty. If a change was made with
knowledge of its effect on the outcome, the report says the affected result
has weaker diagnostic value. If the original plan no longer answers the
intended question, say so plainly.

## Provenance appendix

`report.html` should expose the key figures, tables, and provenance pointers.
An optional `report.pdf` snapshot/export may include the same short provenance
appendix:

```text
Preregistration: prereg/PR_<id>_<slug>.md
Report source: results/reports/RPT_<id>_<slug>/report.md
Figures: results/reports/RPT_<id>_<slug>/figures/
Tables: results/reports/RPT_<id>_<slug>/tables/
Source data or artifact: <path or citation>
External tracker run ID: <omit unless a tracker was actually used>
```

The appendix is for orientation. It should not replace the report's summary,
plan-to-result table, key evidence, Transparent Changes, or limitations.
