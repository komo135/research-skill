# experiment_protocol.md

Structure and rules for "one experiment = one notebook".

## When to read

- Starting a new experiment notebook
- Splitting an existing oversized notebook into experiments

## Why one experiment per notebook

Mixing experiments in one notebook causes:

- Global-variable collisions (`np`, `df`, `model`, etc.) — marimo specifically forbids
  redefining the same global across cells
- File bloat that hides the conclusion
- Loss of independent re-runnability — and therefore reproducibility
- Difficulty answering "what is the conclusion of this experiment?"

**One experiment** = one hypothesis tested + observation + generation of derived hypotheses.

## Notebook naming

```
notebooks/<project-name>/experiments/exp_<NNN>_<slug>.py
```

- `<NNN>`: zero-padded three-digit sequence number
- `<slug>`: alphanumeric and underscore, ~20 characters max
- Examples: `exp_001_data_universe.py`, `exp_002_pca_factor_screening.py`,
  `exp_003_signal_flip_exit.py`

The helper `scripts/new_experiment.py` generates the file with the next sequence number.

## Notebook structure

```
[Cell 1]  Imports
[Cell 2]  Markdown: research design (see research_design.md)
[Cell 3]  Markdown: upstream dependencies and input data
[Cell 4+] Data fetch and split
[Cell N+] Experiment body — one cell per fit / one cell per evaluation
[Cell M+] Markdown: observation and interpretation
[Cell M+] Markdown: conclusion (acceptance / rejection)
[Cell M+] Markdown: derived hypotheses (run-now / next-session / drop)
[Cell M+] Code: append to results/results.parquet
[Cell M+] Code: reminder to update hypotheses.md and decisions.md
```

The last two cells are not optional. Without them, cross-experiment aggregation does not
work.

## What belongs in a single notebook

- One central hypothesis under test
- Pre-processing that is local to that hypothesis (otherwise factor it out into an upstream
  notebook)
- Sensitivity analyses directly tied to the central hypothesis

## What does not belong in a single notebook

- A different central hypothesis — that goes in a separate notebook
- Heavy pre-processing reused across experiments — that goes in its own notebook with
  intermediate output saved to disk
- Project-wide summaries or paper drafts — those live under `results/` or in a separate
  `paper/` folder

## Upstream dependencies via files

When an experiment consumes an upstream experiment's output, pass it as a **file**:

- exp_002 saves `results/intermediate/pca_factors.parquet`
- exp_005 reads that parquet

Do not pass Python objects directly between notebooks. That pattern breaks reproducibility.

## Size guidance

- One notebook = one session's worth of work
- 10 to 30 cells is typical
- 200 to 500 lines

If the notebook exceeds these, split the experiment.

## Pre-flight checklist

Before starting a notebook:

- [ ] Used `scripts/new_experiment.py` to generate it
- [ ] The new sequence number was appended to `experiments/INDEX.md`
- [ ] The linked hypothesis ID exists in `hypotheses.md` (add it if not)
- [ ] Upstream dependencies are complete or running in parallel
- [ ] Acceptance / rejection conditions are written with numeric thresholds

## Completion checklist

Before closing the notebook:

- [ ] Conclusion cell exists (observation + interpretation + acceptance / rejection)
- [ ] "Derived hypotheses" cell exists with classification (run-now / next-session / drop)
- [ ] Result row appended to `results/results.parquet`
- [ ] Linked entry in `hypotheses.md` updated (in-progress → supported / rejected / parked)
- [ ] Time-ordered entry added to `decisions.md`
- [ ] One-line conclusion filled in `experiments/INDEX.md`
