# marimo_cell_granularity.md

Cell-granularity rules for marimo notebooks.

## When to read

- Implementing experiments in marimo
- Considering looping over multiple models or hyperparameter settings

## Core rule

**One cell = one fit / one evaluation.**

Do not loop over models × features × targets in a single cell.

## Anti-pattern

```python
# Forbidden: 36 fits in one cell
for fname, X in FEATURES.items():
    for model in (LR, LGBM, MLP):
        for target in (T1, T2, T4):
            results.append(fit_and_score(...))
```

Problems:

- Cannot localize which combination failed
- Cannot re-run partial work
- Output is verbose and hard to read
- Defeats marimo's reactive re-execution

## Recommended

```python
# Cell N: F2_bolt × LGBM × T1_binary
s_va, s_te = fit_lgbm_classifier(F2_train, y1_train, F2_val, y1_val, F2_test)
row = run_one("F2_bolt", "LGBM", "T1_binary", s_va, s_te, TAU_GRID, "auc")
results.append(row)
save_results_partial(results)  # persist incrementally
print(row.to_dict())            # immediate visibility
```

The cell count grows, but each cell has a single responsibility and can be re-run
independently.

## Avoiding global-name collisions

marimo's dataflow graph forbids redefining the same global across cells:

```python
# Cell A
df = load_data_a()  # defines df

# Cell B
df = load_data_b()  # error: df is multiply defined
```

Avoidance options (in order of preference inside one notebook with multiple
H rounds):

1. **H-suffixed public names** for cross-cell variables that differ per
   round — `signal_h1`, `signal_h2`, `pnl_h1`, `pnl_h2`. This is the primary
   pattern that lets multi-Hypothesis notebooks coexist with marimo's
   dataflow rule. (See `references/experiment_protocol.md` for why
   multi-Hypothesis notebooks are the default unit.)
2. **Cell-private names** with a leading underscore (`_df`) for purely
   intra-cell intermediates that do not need to escape the cell.
3. Disambiguate with otherwise distinct names (`df_a`, `df_b`) when the
   variable is not naturally tied to an H round.

Splitting the file is **not** an avoidance option for global-name collisions
inside one Purpose. The above patterns make multi-Hypothesis notebooks work
without splitting.

## Sweep / grid-search structure

When sweeping multiple hyperparameters, the right structure is:

```python
# Cell M: one cell that builds the sweep table (one combined "evaluation")
_sweep = []
for _h in [4, 8, 12, 24]:
    for _thr in [-15, -20, -25]:
        _ent = make_entry(_thr)
        _ex = _ent.shift(_h)
        _pf = vbt.Portfolio.from_signals(close, _ent, _ex, ...)
        _sweep.append({"hold": _h, "thr": _thr, "sharpe": _pf.sharpe_ratio()})

sweep = pl.DataFrame(_sweep).sort(["hold", "thr"])
sweep
```

This is acceptable as one cell because the sweep itself is one evaluation. But:

- Loop variables must be cell-private (leading underscore)
- The aggregated result becomes a public named variable (`sweep`)
- After choosing the best from the sweep, the chosen configuration is re-run as its own
  separate cell (one fit / one evaluation)

## Per-H closing cells (one set per Hypothesis round)

At the end of each Hypothesis round inside the notebook, append a result row
for that H:

```python
# Per-H closing cell: append to results.parquet (see results_db_schema.md)
append_to_results_db(
    project="<name>",
    experiment_id="exp_005",     # the notebook = the Purpose
    hypothesis_id="H3",          # the individual H within the Purpose
    metrics={"sharpe": ..., "win_rate": ..., ...},
)
```

The append happens **per H**, not once at the bottom of the file.

## Final notebook reminder cell

After the last H round, a single reminder cell:

```python
print("REMINDER: update hypotheses.md and decisions.md")
print("  - Update hypothesis status for every H tested in this notebook")
print("  - Add derived hypotheses (same Purpose) and derived Purposes")
print("    (new notebooks) to hypotheses.md")
```

## Multi-fit exception

ML cross-validation (k-fold) fits the same model across folds, and one cell is correct:

```python
# OK: one model × five folds
cv_scores = cross_val_score(model, X, y, cv=PurgedKFold(...))
```

Multiple **models × multiple settings** is what should be split into multiple cells. One
**model × multiple folds** can be one cell.

## Cell-count guidance

There is no upper bound on cell count under the per-Purpose protocol. A
notebook with several H rounds legitimately runs 60-200 cells; size is
whatever the Purpose requires. The old "10-30 cells per notebook" guidance
applied to the prior one-H-per-notebook unit and no longer applies.

The lower bound still holds: each cell does one fit / one evaluation, so
even a single-H notebook will have on the order of 20-40 cells once
imports, data load, baselines, sanity checks, and robustness battery are
counted.

## Warning signs

- Loop with 10+ fits in one cell → split into multiple cells
- Same name overwritten across cells → use H-suffixed public names
  (`signal_h1`, `signal_h2`) or cell-private (`_`) names; do not split
  the file
- Cells cannot be re-run independently → save intermediates as named
  variables

## See also

- `references/notebook_narrative.md` — what the *content* of the cells must be
  (abstract / observation / interpretation cells, headline figures, `mo.ui`
  drill-down). Cell granularity is the mechanics; narrative is the message.
