---
name: experiment-review
description: REMOVED. This skill has been removed in plugin v1.0 (breaking change). Its claim-warrant review functionality is now provided by the quant-research skill's references/review/conclusion_review.md, which combines implementation correctness checks (formerly bug_review) and claim warrant checks (formerly experiment-review) into a single 6-axis review per CHARTER C9.
---

# Experiment Review (REMOVED)

This skill has been **removed** in plugin v1.0 as a breaking change.

Per CHARTER C9 / D-14 (`.rebuild/CHARTER.md`, `.rebuild/DECISIONS.md`):
the two-skill split (bug_review + experiment-review) has been replaced by a
single two-axis review inside the `quant-research` skill:

- `references/review/process_review.md` — was the discipline followed?
  (HARKing prevention, charter integrity, Layer 1 closure, capability
  ordering, etc.)
- `references/review/conclusion_review.md` — are the conclusions warranted?
  (6 axes: implementation correctness, statistical sufficiency, claim
  discipline, **analysis depth A4+**, reproducibility, cold-eye check)

Per D-25 regression matrix (`.rebuild/regression_old_bug_review.md`),
35/35 bug patterns from the old `bug_review.md` are covered by the new
review structure, plus the experiment-review functionality is folded
into Axis 3 (claim discipline) + Axis 6 (cold-eye check) + analysis
depth (Axis 4).

## Migration

If you previously called `/quant-research:experiment-review`:

→ Now run, in order:

1. `references/review/process_review.md` (was the discipline followed?)
2. `references/review/conclusion_review.md` (are the conclusions warranted?)

Both are agent-self-executable checklists (no parallel sub-agent dispatch
required). Promotion gates (`references/rd/rd_promotion_gate.md` and
`references/pure_research/pr_promotion_gate.md`) require both to pass
clean before any `matured` / `supported` claim.

## Why removed

The old design had:
- high-overhead parallel dispatch protocols in bug_review and experiment-review
- F21 input-contract management, F22 trigger-conditional re-verify

The active standalone `skills/experiment-review` compatibility source has since
been consolidated to 4 reviewer agents. This v1.0 package shim still points
users to the unified `quant-research` review checklists.

Total: 423 lines of bug_review + ~300 lines of experiment-review = ~720
lines of review protocol overhead, requiring agent-coordinated multi-agent
dispatch which is hard to verify and slow to run.

The new design: 2 self-executable checklists, ~620 lines total, agent
runs them sequentially in a single session. Coverage parity verified.

This skill file is preserved as a deprecation shim so anyone trying to
invoke `experiment-review` gets a clear migration message.
