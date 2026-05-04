# bug_review.md (RETIRED)

This reference has been retired in the rebuild. Its 423-line, 6-reviewer
parallel-dispatch protocol is replaced by a slimmed two-axis review at:

- `references/review/process_review.md` — was the discipline followed?
- `references/review/conclusion_review.md` — are the conclusions warranted?
  - 6 axes: Implementation correctness / Statistical sufficiency /
    Claim discipline / Analysis depth (A4+) / Reproducibility / Cold-eye check
  - Pre-axis: numeric red flag triggers (the 9 "too good to be true" thresholds
    from the old bug_review.md, now used to direct scrutiny rather than dispatch
    reviews)

Coverage parity verified: see `.rebuild/regression_old_bug_review.md`
(35/35 bug patterns covered, 2 gaps patched in the new structure).

Do not consult this file for current protocol; the new review structure
covers all functionality with a simpler, agent-self-executable checklist.
