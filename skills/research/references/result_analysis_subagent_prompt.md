# Result Analysis Subagent Prompt Template

Use this template after the `research` skill has completed or updated a plan's Actual execution and Planned vs Actual sections. Pass only the plan path as the starting context.

```text
Use the research-result-analysis skill.

Analyze this plan:
<plans/id_slug.md>

Treat the plan as the only starting context. Reconstruct necessary evidence yourself from referenced runs, run_manifest.json, logs/stdout.log, logs/stderr.log, scripts, configs, outputs, tables, figures, reports, and literature entries. Do not use parent-agent summaries, expected conclusions, private notes, or unstated expectations.

Return a `## Result analysis` section containing:
1. what happened, grounded in artifacts
2. candidate explanations for why the result happened
3. evidence for and against each explanation
4. procedure or artifact explanations, including execution mistakes, leakage, broken comparators, script defects, measurement artifacts, or missing evidence when relevant
5. alternatives still live
6. discriminating next analyses
7. context_missing entries for missing or insufficient context

Do not assess promotion readiness. Do not write final claims, decisions, iteration branches, deployment recommendations, or human-facing reports.
```

The parent research agent records the returned `## Result analysis` section before writing claims, decisions, or reports. Do not analytically summarize, rewrite, or collapse the subagent's findings; only mechanical formatting fixes are allowed.
