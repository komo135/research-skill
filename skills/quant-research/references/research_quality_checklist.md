# research_quality_checklist.md

Self-check before declaring research complete. Borrows reviewer-grade criteria. Applies to
research that does not target publication as well.

## When to read

- Just before declaring completion
- When the research feels "done" and you want to verify it
- When checking whether the work has reached publication-grade quality

## Structure

Eleven blocks. Each must satisfy its pass conditions; otherwise the work is downgraded
to **preliminary screening**.

## 1. Research design

- [ ] The question is a falsifiable comparison statement
- [ ] The hypothesis was fixed in advance and not rewritten in light of results
- [ ] Acceptance / rejection conditions are numeric thresholds
- [ ] Universe (3+ instruments or a defined cross-section) is stated

## 2. Literature

- [ ] 5-10 prior papers recorded in `literature/papers.md`
- [ ] Differentiation against prior work is in `literature/differentiation.md`
- [ ] Differentiation level is "medium" or higher (not just parameter / period changes)
- [ ] No method previously refuted by prior work is revived without new justification

## 3. Data and split

- [ ] Time-ordered split (train < val < test)
- [ ] Embargo set appropriately
- [ ] Test set was touched only once
- [ ] Purged k-fold or CPCV used (for ML research)
- [ ] Data hashes recorded in `reproducibility/data_hashes.txt`

## 4. Baselines

- [ ] Lower-bound baseline (do-nothing / B&H / random) reported
- [ ] Hand-crafted upper-bound baseline (linear model, etc.) reported
- [ ] Proposed method beats both

## 5. Model selection

- [ ] Model selection is justified concretely (not "lightweight" / "famous")
- [ ] Latest version is used (no outdated version adopted without reason)
- [ ] Math models: assumptions verified. ML models: overfit checks done.

## 6. Features and pre-processing

- [ ] Feature construction validated in its own experiment notebook
- [ ] Leakage checks (look-ahead, target) done
- [ ] Intermediate results saved to parquet (no Python-object handoff)

## 7. For strategy-style research

- [ ] At least three exit strategies compared in parallel (not time-stop alone)
- [ ] Position sizing is documented
- [ ] Hedging / market-neutralization is deliberate

## 8. Bug review (multi-agent)

See `references/bug_review.md` and `references/sanity_checks.md`.

- [ ] Programmatic sanity checks all green: random-signal benchmark, PnL reconciliation,
      cost monotonicity, sign-flip, NaN/Inf scan, time-shift placebo (and shuffled-target
      test for ML)
- [ ] Multi-agent review dispatched (5 specialists in parallel, or 5 sequential passes if
      parallel dispatch is unavailable)
- [ ] Every `high` / `medium` finding resolved or rejected with a recorded reason
- [ ] `decisions.md` contains the bug-review entry with trigger, reviewer IDs, findings,
      resolutions
- [ ] No `verdict = "supported"` was set before the bug-review entry exists

A pass on this block is required before any pass on Block 9 (Robustness). The robustness
gates measure overfitting and regime stability — not correctness — so a buggy PnL passes
them silently.

## 9. Robustness

`robustness_battery.md` items:

- [ ] 2D threshold sensitivity: ≥ 50 % cells positive
- [ ] Fee sensitivity: break-even fee reported
- [ ] Walk-forward Sharpe: mean > 0 and pct_positive ≥ 60 %
- [ ] Bootstrap CI: 95 % lower bound > 0 (or `p < 0.05`)
- [ ] Probabilistic / Deflated SR: PSR ≥ 0.95 and DSR ≥ 0.95
- [ ] Realistic cost (per-bar spread or slippage model): positive Sharpe maintained
- [ ] Regime-conditional: positive in 3+ regimes

## 10. Conclusion limits

- [ ] Conclusions are restricted to the observed range (no leap from "failed" to
  "no signal")
- [ ] "Cannot conclude" section names dimensions not tested (instruments, regime, sizing)
- [ ] "Next questions" classified into run-now / next-session / drop

## 11. Hypothesis cycles

- [ ] Cycle count ≥ 3 (minimum) or ≥ 5 (standard)
- [ ] `hypotheses.md` and `decisions.md` updated each cycle
- [ ] No untriaged candidate hypotheses remain
- [ ] All results aggregated into `results.parquet` under the common schema

## Pass-rate interpretation

| Pass rate | Position |
|---|---|
| 100 % (all blocks) | Publication-grade or production-grade |
| ≥ 80 % | Strong enough for internal team review |
| ≥ 60 % | Preliminary screening |
| < 60 % | Single experiment, not yet research |

## When a block fails

For each failed item, decide and record in `decisions.md`:

- "Will fix in the next cycle" — log the new hypothesis in `hypotheses.md`
- "Will not fix" — state the reason explicitly (e.g. "multi-asset deferred to next session;
  this report covers a single instrument only")

This makes the reasoning auditable later.

## Warning signs

- "Looks roughly fine" — replace each item with a concrete number
- Reporting only favorable results — surface the negative walk-forward windows too
- Avoiding robustness checks because "the sample is small" — produce confidence intervals
  via block bootstrap, which works under small samples
- Skipping DSR by under-reporting trial count — count honestly
