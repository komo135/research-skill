# Result Analysis Subagent Prompt Template

Use this template when the `research` skill has completed or updated a plan's Actual execution and Planned vs Actual sections. Pass only the plan path as the starting context.

```text
Use the research-result-analysis skill.

Analyze this plan:
<plans/id_slug.md>

Treat the plan as the only starting context. Reconstruct necessary evidence yourself from referenced runs, run_manifest.json, logs/stdout.log, logs/stderr.log, scripts, configs, outputs, tables, figures, reports, and literature entries. Do not use parent-agent summaries, expected conclusions, private notes, or unstated expectations.

Return a `## Result analysis` section containing:
1. observations grounded in artifacts
2. interpretations separated from observations
3. alternatives not excluded
4. context_missing entries for missing or insufficient context
5. required additional analysis
6. claim-readiness assessment

Do not write final claims, decisions, or human-facing reports.
```

The parent research agent records the returned `## Result analysis` section in the plan before dispatching the research-review subagent. Do not analytically summarize, rewrite, or collapse the subagent's findings; only mechanical formatting fixes are allowed.
