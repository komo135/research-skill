# Result Analysis Subagent Prompt Template

Use this template after the `research` skill has completed or updated a hypothesis plan's Actual execution and Planned vs Actual sections. Pass only the plan path as the starting context.

```text
Use the research-result-analysis skill.

Analyze this plan:
<propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md>

Treat the plan as the only starting context. Reconstruct necessary result material yourself from sibling hypothesis.md, referenced parent proposition files, referenced runs, run_manifest.json, logs/stdout.log, logs/stderr.log, scripts, configs, outputs, tables, figures, proposition paper.md when present, and literature entries. Do not use parent-agent summaries, expected conclusions, private notes, or unstated expectations.

Return a `## Result analysis` section that explains why the observed result happened. Include:
1. material used for explanation
2. result shape: aggregate, slice / condition, trace / process, and concentrated cases
3. explanatory contrast: planned expectation only as context for what needs explaining
4. factor decomposition across relevant data, representation, method, process, resource, measurement, change/intervention, control/barrier, and interaction factors
5. causal factor tree: proximate triggers, contributing factors, current root-cause candidates, why they are deeper than the trigger, and evidence boundary
6. mechanism traces for live candidate explanations
7. what each explanation explains and does not explain
8. interaction analysis when multiple factors combine
9. discriminators that would separate live explanations, without choosing a next action
10. open explanatory branches

For a missed prediction, decompose the error by slice, regime, horizon, sign, magnitude, residual autocorrelation, validation trajectory, and tail cases when available. Do not announce a root cause unless the explanation states why the proximate factor existed, dominated, or escaped the plan's controls and what rival explanation remains live. If the material does not support a root-cause conclusion, say no root cause is identified yet and name the discriminator.

If the user asks for a quick or concise answer, shorten each field but keep result shape, causal factor tree, at least one mechanism trace, root-cause evidence boundary, and discriminator.

Do not assess whether the result is good, bad, valid, supported, contradicted, claim-ready, promotion-ready, or decision-ready. Do not write final claims, proposition decisions, hypothesis decisions, state-update inputs, iteration branches, deployment recommendations, or human-facing paper prose.
```

The parent research agent records the returned `## Result analysis` section before writing claims, decisions, or papers. The parent updates `hypothesis.md`, hypothesis `decisions.md`, parent `proposition.md`, and proposition `decisions.md` only after separately reviewing the explanation. Do not analytically summarize, rewrite, collapse, or convert the subagent's findings into state labels; only mechanical formatting fixes are allowed.
