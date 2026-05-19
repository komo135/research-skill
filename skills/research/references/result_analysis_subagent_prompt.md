# Result Analysis Subagent Prompt Template

Use this template after the `research` skill has completed or updated a hypothesis plan's Actual execution and Planned vs Actual sections. Pass only the plan path as the starting context.

```text
Use the research-result-analysis skill.

Analyze this plan:
<propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md>

Treat the plan as the only starting context. Reconstruct necessary result material yourself from sibling hypothesis.md, referenced parent proposition files, referenced runs, run_manifest.json, logs/stdout.log, logs/stderr.log, scripts, configs, outputs, tables, figures, reports, and literature entries. Do not use parent-agent summaries, expected conclusions, private notes, or unstated expectations.

Return a `## Result analysis` section that explains why the observed result happened. Include:
1. material used for explanation
2. result shape: aggregate, slice / condition, trace / process, and concentrated cases
3. explanatory contrast: planned expectation only as context for what needs explaining
4. factor decomposition across relevant data, representation, method, process, resource, measurement, and interaction factors
5. mechanism traces for live candidate explanations
6. what each explanation explains and does not explain
7. interaction analysis when multiple factors combine
8. discriminators that would separate live explanations, without choosing a next action
9. open explanatory branches

Do not assess whether the result is good, bad, valid, supported, contradicted, claim-ready, promotion-ready, or decision-ready. Do not write final claims, proposition decisions, hypothesis decisions, state-update inputs, iteration branches, deployment recommendations, or human-facing reports.
```

The parent research agent records the returned `## Result analysis` section before writing claims, decisions, or reports. The parent updates `hypothesis.md`, hypothesis `decisions.md`, parent `proposition.md`, and proposition `decisions.md` only after separately reviewing the explanation. Do not analytically summarize, rewrite, collapse, or convert the subagent's findings into state labels; only mechanical formatting fixes are allowed.
