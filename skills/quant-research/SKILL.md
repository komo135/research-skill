---
name: quant-research
description: Use as a domain extension when the main `research` skill is in use AND the work involves time-series data, statistical hypothesis testing, held-out evaluation, or any setting where overfitting and information leakage are first-order concerns. Triggers when designing time-series cross-validation, applying multiple-testing corrections, characterizing baselines with statistical rigor, checking for leakage between train/test/eval, or assessing robustness across regimes.
---

# Quant Research

A domain extension over the `research` skill for **time-series and statistically rigorous quantitative R&D**. The base `research` skill governs the protocol — categories, plans, claims, reports, iteration. This skill adds statistical methodology specific to settings where:

- The data has temporal order (no random shuffling)
- A method is selected from a search space (overfitting risk)
- Many hypotheses are tested in parallel (multiple-testing inflation)
- Held-out evaluation must avoid information leakage

## Relationship to `research`

This skill is **always used together with `research`**. It does not redefine plans, claims, decisions, or reports — those still follow the base skill. It adds **methodology references** and **executable utilities** for the statistical layer.

If you are starting a new R&D project, read `skills/research/SKILL.md` first. Come here when statistical rigor in the experiment design is a concern.

## Origin note

Several references and methods in this skill originated in quantitative finance research (e.g., Combinatorial Purged Cross-Validation from López de Prado 2018, multiple-testing corrections developed for strategy selection). The underlying statistical concepts — purged cross-validation, deflation of selected-best metrics, embargoed splits, walk-forward validation — apply to **any quantitative R&D involving time-series data or selected-best-of-N model evaluation**: epidemiology, climate modeling, ML benchmarking on temporal data, neuroscience, signal processing, system identification.

Treat the finance-origin examples in references as illustrative, not constraining. The methodology generalizes.

## What this skill adds

### Methodology references (`references/shared/`)

Read only the ones relevant to your current concern.

| Reference | When to read |
|---|---|
| `time_series_validation.md` | Designing data splits when time order matters; designing walk-forward or CPCV |
| `multiple_testing.md` | When > 1 hypothesis or > 1 model variant is tested and a best is selected |
| `feature_construction.md` | Designing features from time-series data; preventing leakage at feature stage |
| `modeling_approach.md` | Choosing model class for a time-series prediction task |
| `model_diagnostics.md` | Verifying model behavior beyond the headline metric |
| `prediction_to_decision.md` | Mapping a prediction to an actionable decision under uncertainty |
| `robustness_battery.md` | Battery of robustness checks: regime sensitivity, parameter sensitivity, perturbation |
| `sanity_checks.md` | Sanity tests that should pass before any claim is made (label balance, look-ahead, etc.) |

### Executable utilities (`scripts/`)

Domain-neutral implementations of common statistical tools:

| Script | Purpose |
|---|---|
| `purged_kfold.py` | Purged k-fold cross-validation for time-series with overlapping labels |
| `cpcv.py` | Combinatorial Purged Cross-Validation |
| `walk_forward.py` | Walk-forward (expanding or rolling) time-series validation |
| `multiple_testing.py` | Multiple-testing corrections (Bonferroni, BH, Romano-Wolf) |
| `leakage_check.py` | Detect train/test feature leakage and look-ahead bias |
| `sanity_checks.py` | Standard pre-claim sanity tests |
| `sensitivity_grid.py` | Parameter sensitivity grid for robustness battery |

These are utilities, not framework code. They produce neutral outputs (numbers, JSON, csv) that the agent records as artifacts under `propositions/Pxxx_slug/hypotheses/Hxxx_slug/experiments/runs/<run_id>/`. The base `research` skill governs how those artifacts become claims and reports.

## When to use this skill

Use the methodology references and scripts when:

- Designing the **plan** of a confirmatory applied-research project that involves a time-series benchmark — the plan section should cite the validation strategy
- Running an **experiment** where the agent selects the best of N model variants — the multiple-testing correction is part of the methodology
- Writing **Methods & Conditions** in a report for time-series work — the report must specify which validation protocol was used and why
- Writing **Limitations** when the validation has known biases (small held-out set, single regime, overlapping labels)

## When NOT to use this skill

- The work is not on time-series data and does not involve held-out statistical evaluation. The base `research` skill suffices.
- The agent is in early exploratory phase with no held-out claim being made. Statistical rigor matters most when claims are being made.
- The work is purely qualitative or focuses on system construction (experimental development) without statistical evaluation claims.

## Pitfalls this skill helps avoid

These are common failure modes in quantitative R&D that the base `research` skill alone does not directly address:

- **Random-shuffle CV on time-series data.** Information from the future leaks into training. Use `purged_kfold.py` or `walk_forward.py`.
- **Selecting the best of N strategies without correction.** The selected best's apparent significance is inflated. Use `multiple_testing.py` with an appropriate correction (Bonferroni for FWER, Benjamini-Hochberg for FDR, Romano-Wolf for dependent tests).
- **Overlapping labels in cross-validation.** Standard k-fold underestimates error when labels span multiple samples. Use purged CV with an embargo.
- **Feature leakage from the future.** Features that use information not available at prediction time inflate validation scores. Run `leakage_check.py`.
- **Single-regime claims.** A method that works in one regime may fail in another. Use `robustness_battery.md` to design a regime sensitivity sweep.
- **Sharpening claims under selection bias.** Reporting only the validation runs that succeeded, or only the strongest hyperparameter point. The agent should record ALL trial outcomes and apply the multiple-testing correction.

## Quick reference

| Concern | Read | Optionally run |
|---|---|---|
| "How do I split my time-series data?" | `references/shared/time_series_validation.md` | `scripts/walk_forward.py` or `scripts/purged_kfold.py` |
| "I'm comparing many model variants — how do I correct?" | `references/shared/multiple_testing.md` | `scripts/multiple_testing.py` |
| "Is there leakage in my pipeline?" | `references/shared/sanity_checks.md` | `scripts/leakage_check.py` |
| "How robust is this result to parameter changes?" | `references/shared/robustness_battery.md` | `scripts/sensitivity_grid.py` |
| "What features can I construct without future-info leak?" | `references/shared/feature_construction.md` | |
| "How do I diagnose model failures?" | `references/shared/model_diagnostics.md` | |

## Sources

- [López de Prado (2018) — Advances in Financial Machine Learning](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086) — CPCV, purged CV, embargo methodology (finance origin, broadly applicable)
- [Benjamini & Hochberg (1995) — Controlling the false discovery rate](https://www.jstor.org/stable/2346101) — FDR foundation
- [Romano & Wolf (2005) — Stepwise multiple testing as formalized data snooping](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2005.00615.x) — dependent-test correction
