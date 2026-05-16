# Literature Review

## Purpose

Document what is already known about the research question before writing the Plan section, choosing controls/comparators, or making claims.

Every plan needs prior-work grounding. It is not optional just because no novelty claim is made. The plan-scoped job is bounded but sufficient: enough to support the plan's question/objective, inherited assumptions, method choice, controls/comparators/evaluation protocol, baselines/evaluation protocol when the claim requires them, and known limitations.

The job is to:

1. Know what is already established so you are not re-running prior work unknowingly
2. Identify assumptions inherited from prior approaches, prior data, or prior results
3. Cite the controls, comparators, baselines when applicable, and evaluation protocols the plan relies on
4. Record known limitations and claim scope before execution

## When to do this

- At the start of any new plan, before writing the Plan section
- Before choosing controls, comparators, baselines when applicable, evaluation protocol, or method family
- Before claiming a method is novel
- Before claiming a baseline does not exist
- When the agent encounters an unfamiliar method during execution

Comprehensive literature survey is required for strong external novelty, publication, `to our knowledge`, or `no baseline exists` claims. That is separate from the bounded but sufficient prior-work grounding every plan needs.

If prior work is genuinely unknown, record the named constraint in the plan and narrow or block relevant claims until the grounding is repaired. Do not treat absence of a novelty claim as permission to skip prior work.

## Files

- `literature/papers.md` — annotated list of relevant prior work
- `literature/positioning.md` — how this work stands on prior work

## papers.md format

```markdown
## <Author year — short title>

- Citation: <full bib reference or URL>
- Method / Finding: <one-paragraph summary, in your own words>
- Relevance: <why this matters for the current plan>
- Used as baseline: yes / no
```

Two paragraphs per entry maximum. Longer summaries belong in the agent's session notes, not in the project state. The point is to make the entry scannable when a future session is checking what was considered.

## positioning.md format

```markdown
# How this work stands on prior work

## <Prior approach A — cite papers.md entry>
- What it establishes: <summary>
- Inherited assumption: <what this plan carries forward>
- Baseline / protocol use: <whether this informs a baseline, control, metric, or evaluation setup>
- Known limitation: <limitation relevant to this plan>
- Position of this work: <replication / baseline strengthening / extension / new method / system / other>
- Claim scope: <what claims this grounding supports, narrows, or blocks>

## <Prior approach B>
- ...
```

Differences or novelty can be recorded in `literature/positioning.md` when claimed, but the primary purpose is grounding, inheritance, control/comparator choice when relevant, known limitations, and claim scope. If the work does not differ from prior approaches in a meaningful way, this is itself an important finding. Basic-research replication is valuable, but the report should be honest about being a replication.

## Common failures

- **Claiming novelty without literature search.** "To our knowledge" is not a search; it is an absence of search. If the agent has not actually searched, the claim of novelty is unsupported.
- **Listing tangentially related papers to look thorough.** Each entry should connect to the current plan, not pad a citation count.
- **Comparing against the wrong comparator.** If you compare to a weak or outdated comparator because stronger ones are hard to run, the comparison is biased; say so explicitly in `literature/positioning.md` and in the report.
- **Not updating papers.md mid-investigation.** When a new relevant paper appears during execution (e.g., the agent finds it while debugging), add it to `literature/papers.md` and update `literature/positioning.md` if relevant.
