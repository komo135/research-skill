# outcome_reports.md

Use this reference when preregistered work produces a user-facing report. The
report is a readable outcome artifact, not a second state ledger and not a
complete archive of every intermediate file.

## Package shape

All preregistered work that produces a report uses:

```text
results/reports/
  RPT_<id>_<slug>/
    report.md
    report.pdf
    figures/
    tables/
    attachments/
```

`report.md` is the editable source. `report.pdf` is the provided report
artifact. Figures and tables that appear in the PDF should have source files in
`figures/` or `tables/`. Use `attachments/` only for small supporting files
needed to read the report. Do not copy large source data or intermediate
artifacts unless they are small and necessary.

Local paths may appear in `report.md` or the provenance appendix, but they
should not dominate the report. External tracker run IDs are optional and
should appear only when a tracker was actually used.

## Required sections

Every preregistered report includes:

1. Preregistration Reference
2. Summary
3. Plan-to-Result Table
4. Key Figures / Tables
5. Transparent Changes
6. Scope / Limitations

Optional section:

- Follow-up or next decision

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

## PDF provenance appendix

`report.pdf` should include the key figures and tables. It may include a short
provenance appendix:

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
