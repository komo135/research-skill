# Project Layout

This is the generated project layout source of truth for the `research` skill.

```text
project-root/
├── intake.md
├── literature/
│   ├── scoping.md
│   ├── papers.md
│   └── positioning.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── eda/
├── observations.md
├── project_state.md
├── decisions.md
├── lib/
│   ├── data/
│   ├── eval/
│   ├── viz/
│   ├── utils/
│   └── tests/
└── propositions/
    └── P001_slug/
        ├── proposition.md
        ├── observations.md
        ├── analyses.md
        ├── decisions.md
        ├── paper.md
        └── hypotheses/
            └── H001_slug/
                ├── hypothesis.md
                ├── plan.md
                ├── experiments/
                │   ├── code/
                │   ├── configs/
                │   ├── notebooks/
                │   └── runs/
                └── decisions.md
```

Rules:

- Root `decisions.md` contains project structure, scope, and protocol decisions only.
- `creating-propositions` owns `propositions/Pxxx_slug/{proposition,observations,analyses,decisions}.md`.
- `research` owns `propositions/Pxxx_slug/paper.md` and `propositions/Pxxx_slug/hypotheses/Hxxx_slug/*`.
- Do not create top-level `plans/`, top-level `experiments/<id>/runs/`, `literature/differentiation.md`, or per-hypothesis `reports/`.
- Scoping literature in `literature/scoping.md` does not replace plan-scoped Survey evidence and Citation-use map.
