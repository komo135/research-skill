# Result Analysis Subagent Prompt Template

Use this template after the `research` skill has completed or updated a hypothesis plan's Actual execution and Planned vs Actual sections. Pass only the plan path as the starting context.

```text
Use the research-result-analysis skill.

Analyze this plan:
<propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md>

Treat the plan as the only starting context. Reconstruct necessary result material yourself from sibling hypothesis.md, referenced parent proposition files, referenced runs, run_manifest.json, logs/stdout.log, logs/stderr.log, scripts, configs, outputs, tables, figures, proposition paper.md when present, and literature entries. Do not use parent-agent summaries, expected conclusions, private notes, or unstated expectations.

Follow the skill workflow rather than treating this as a checklist. First reconstruct the material boundary, then build a result-feature ledger, select the explanatory target, choose the method route from the observed shape, and only then write causal-factor trees and mechanism traces. The detailed method catalog lives in `skills/research-result-analysis/references/analysis_workflow.md`.

Return a `## Result analysis` section that explains why the observed result happened. Include the selected method route, result shape, explanatory contrast, relevant factor decomposition, causal factor tree, mechanism traces, interaction analysis, discriminators, and open explanatory branches.

For an apparent prediction hit, explain whether the planned mechanism actually generated the result or whether slice mix, evaluator behavior, artifact composition, or interaction made the aggregate look right. For a missed prediction, decompose the error by slice, regime, horizon, sign, magnitude, residual autocorrelation, validation trajectory, and tail cases when available. Do not announce a root cause unless the explanation states why the proximate factor existed, dominated, or escaped the plan's controls and what rival explanation remains live. If the material does not support a root-cause conclusion, say no root cause is identified yet and name the discriminator.

If the user asks for a quick or concise answer, shorten each field but keep result shape, causal factor tree, at least one mechanism trace, root-cause evidence boundary, and discriminator.

Do not assess whether the result is good, bad, valid, supported, contradicted, claim-ready, promotion-ready, or decision-ready. Do not write final claims, proposition decisions, hypothesis decisions, state-update inputs, iteration branches, deployment recommendations, or human-facing paper prose.
```

The parent research agent records the returned `## Result analysis` section before writing claims, decisions, or papers. The parent updates `hypothesis.md`, hypothesis `decisions.md`, parent `proposition.md`, and proposition `decisions.md` only after separately reviewing the explanation. Do not analytically summarize, rewrite, collapse, or convert the subagent's findings into state labels; only mechanical formatting fixes are allowed.
