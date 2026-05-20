# Workflow Redesign Inventory Decisions

Decision record for the 2026-05-20 research workflow layout redesign.

| Item | Decision | Rationale |
|---|---|---|
| `check_mechanism_hypothesis_record.py` | keep | It remains a legacy checker for older mechanism-record plans and current tests still protect its behavior. The current workflow uses proposition analyses and hypothesis ledgers. |
| `ideation.md`, `iterative_ideation.md`, `iteration_loop.md`, `mechanistic_hypothesis_generation.md` | keep with narrowed role | These references remain useful for hypothesis-level reasoning and categories, but proposition generation is owned by `creating-propositions`. |
| Old `Situation question` entry in `research/SKILL.md` | retire | Research now starts from intent, intake, uncertain-outcome gate, scoping, and material/EDA before proposition creation. |
| README `creating-propositions` description | update | It should describe proposition workspace ownership, not an upstream-only candidate generator. |
| `quant-research/SKILL.md` | update references only | It should not redefine layout or state, but must point to papers rather than reports. |
| Report templates and scripts | evolve to paper | Per-hypothesis reports are retired. Proposition resolution produces `propositions/Pxxx_slug/paper.md`, checked by `check_paper.py` and initialized by `draft_paper.py`. |
