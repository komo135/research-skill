# Literature Review

## Purpose

Document what is already known about the research question before writing the Plan section, choosing controls/comparators, or making claims.

Every plan needs prior-work grounding. Every plan also needs a plan-scoped paper survey before writing the Plan section. The resulting Prior-work grounding is not optional just because no novelty claim is made. The plan-scoped job is bounded but sufficient: enough to support the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations.

Early baseline/comparator design has the same dependency at scoping time. Count a source by what it establishes, not by its label. Task-mechanics evidence such as files, target columns, metrics, splits, data availability, or submission format can contribute to scoping only when it also records existing approaches, baselines, comparators, evaluation conventions, or known failures. Before implementing a submit-able baseline, choosing a comparator, or describing a baseline as safe, record existing work, public baselines, competition writeups/notebooks/discussions when relevant, failed searches, and known limitations in `literature/scoping.md`. If that evidence is missing, the route is still `materialization`, not implementation.

The job is to:

1. Know what is already established so you are not re-running prior work unknowingly
2. Identify assumptions inherited from prior approaches, prior data, or prior results
3. Cite the controls, comparators, baselines when applicable, and evaluation protocols the plan relies on
4. Record known limitations and claim scope before execution

Record survey evidence in the plan:

- Search date
- Queries or source names used
- Selection rationale for included papers and excluded near misses
- Negative findings, such as missing baselines, failed comparator searches, or contradictions not found
- Retrieval-unavailable constraint when tools, access, or connectivity prevent the survey

Also record a citation-use map. It is not enough to list papers in `literature/papers.md`; the plan must say how each cited work is used. Use citations only when they support a specific role in the plan: question framing, mechanism prior, baseline, comparator, metric, dataset, evaluation protocol, theoretical foundation, known limitation, contradictory evidence, or claim-scope boundary.

Retrieval-unavailable is not a survey bypass. Use it only with a verifiable signal: attempted source/tool, query or source ID when available, failure evidence such as tool error, access denial, connectivity output, or blocked database access, and explicit claim-scope narrowing for the claims that depended on unavailable retrieval. Do not make novelty, no-baseline, comparator-completeness, or comprehensive-grounding claims from an unavailable survey.

`Used in plan as` in `literature/papers.md` and `literature/positioning.md` is a project-level role union: the set of roles a source has played across project plans. The plan-specific source of truth is the plan's `Citation-use map`. If the same paper is a baseline in one plan and a mechanism prior in another, keep both roles in the literature files and disambiguate the current plan's role only in the plan.

## When to do this

- At the start of any new plan, before writing the Plan section
- Before baseline/comparator design, including a "minimal" or submit-able baseline
- Before choosing controls, comparators, baselines when applicable, evaluation protocol, or method family
- Before claiming a method is novel
- Before claiming a baseline does not exist
- When the agent encounters an unfamiliar method during execution
- As a mid-execution literature update when an unfamiliar method, unexpected result, new comparator, contradiction with prior work, or missing-baseline signal appears during execution

Comprehensive literature survey is required for strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims. That is separate from the bounded but sufficient plan-scoped paper survey and prior-work grounding every plan needs.

If prior work is genuinely unknown after the plan-scoped paper survey, record the named constraint in the plan and narrow or block relevant claims until the grounding is repaired. Do not treat absence of a novelty claim as permission to skip prior work. If retrieval is unavailable, record the retrieval-unavailable constraint, retrieval-unavailable evidence, and claim-scope narrowing in the plan; do not silently replace the survey with guesses.

At scoping time, unknown prior work similarly narrows the next implementation step. Record attempted source/tool, query or source ID when available, failure evidence, and which baseline/comparator design decisions are blocked. Do not use "local-data-only" facts as a substitute for public baselines or competition writeups.

## Files

- `literature/papers.md` — annotated list of relevant prior work
- `literature/positioning.md` — how this work stands on prior work

## papers.md format

```markdown
## <Author year — short title>

- Citation: <full bib reference or URL>
- Method / Finding: <one-paragraph summary, in your own words>
- Relevance: <why this matters for the current plan>
- Used in plan as: <project-level role union: question framing / mechanism prior / baseline / comparator / metric / data / evaluation protocol / theoretical foundation / limitation / contradictory evidence / claim-scope boundary>
- Used as baseline: <yes / no; convenience flag only, not the plan-specific source of truth>
```

Two paragraphs per entry maximum. Longer summaries belong in the agent's session notes, not in the project state. The point is to make the entry scannable when a future session is checking what was considered.

## positioning.md format

```markdown
# How this work stands on prior work

## <Prior approach A — cite papers.md entry>
- What it establishes: <summary>
- Used in plan as: <project-level role union; use the plan's Citation-use map for the current plan-specific role>
- Inherited assumption: <what this plan carries forward>
- Baseline / protocol use: <whether this informs a baseline, control, metric, or evaluation setup>
- Known limitation: <limitation relevant to this plan>
- Position of this work: <replication / baseline strengthening / extension / new method / system / other>
- Claim scope: <what claims this grounding supports, narrows, or blocks>

## <Prior approach B>
- ...
```

Differences or novelty can be recorded in `literature/positioning.md` when claimed, but the primary purpose is grounding, inheritance, control/comparator choice when relevant, known limitations, and claim scope. If the work does not differ from prior approaches in a meaningful way, this is itself an important finding. Basic-research replication is valuable, but the paper should be honest about being a replication.

## During execution

A mid-execution literature update is required when execution reveals an unfamiliar method, unexpected result, new comparator, contradiction with prior work, or missing-baseline signal. Update `literature/papers.md`, update `literature/positioning.md`, and record the update in the plan's `Actual execution` section. If the update changes the method, comparator, metric, evaluation protocol, hypothesis, or claim scope, record the effect on plan and rerun Plan review before continuing claim-bearing execution.

## Common failures

- **Claiming novelty without literature search.** "To our knowledge" is not a search; it is an absence of search. If the agent has not actually searched, the claim of novelty is unsupported.
- **Bibliography without a citation-use map.** A list of papers is not grounding. Record how each cited work is used in the plan.
- **Listing tangentially related papers to look thorough.** Each entry should connect to the current plan, not pad a citation count.
- **Comparing against the wrong comparator.** If you compare to a weak or outdated comparator because stronger ones are hard to run, the comparison is biased; say so explicitly in `literature/positioning.md` and in the paper.
- **Not updating papers.md mid-investigation.** When a new relevant paper appears during execution (e.g., the agent finds it while debugging), add it to `literature/papers.md` and update `literature/positioning.md` if relevant.
