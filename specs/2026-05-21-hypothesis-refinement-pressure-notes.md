# Hypothesis Refinement Pressure Notes

- Date: 2026-05-21
- Scope: PR #52 revert follow-up; failed-hypothesis refinement should be guarded by subagent pressure scenarios, not by adding another stable workflow vocabulary to `SKILL.md`.
- Test admission classification: Documentation contract / skill pressure evidence. Do not add repository tests for this behavior unless a stable public artifact or script contract is introduced.

## Reverted Change

PR #52 added an explicit next-step classification for failed-hypothesis refinement and exposed it in the plugin manifests. That change is reverted as a public skill contract. The underlying failure mode remains important, but it should be managed through pressure testing and targeted skill wording only after fresh RED evidence shows the exact rationalization.

Do not reintroduce the reverted classification labels as string-search tests, manifest claims, or mandatory `SKILL.md` headings.

## Failure Mode To Pressure-Test

After a hypothesis fails or returns an inconclusive result, an agent may turn the failure cause itself into the next parent hypothesis. This is wrong when the proposed follow-up only repairs an evaluator, protocol, measurement, implementation, or side anomaly and does not explain how it would support, contradict, narrow, split, or realize the parent proposition.

Observed PR #52 RED evidence:

- P081 scenario: the agent treated evaluator-noise cleanup as a revised descriptive hypothesis and drifted away from the parent proposition's factuality/latency consequence.
- P014 anomaly scenario: the agent risked turning an interesting anomaly into the next hypothesis instead of preserving it as material for later scoping.

## Subagent Pressure Protocol

Use a fresh separate-context subagent. Give it only:

- the relevant skill content under test
- the scenario material
- the instruction to choose the next artifact or stop condition

Do not show the design notes, expected answer, or this file during RED. Record the subagent's actual rationalization verbatim. Patch skill text only if the failure is reproduced and the existing text does not already counter the rationalization.

## Expected Judgment

The subagent should allow a next parent hypothesis only when the proposed follow-up states how it can update the parent proposition. If the follow-up is evaluator repair, measurement cleanup, implementation repair, or protocol construction, it should produce a material/protocol artifact instead. If the follow-up is an interesting observation outside the parent proposition, it should preserve it as observation material for later scoping rather than opening a hypothesis under the current parent.

The guard is the adversarial review process and recorded RED/GREEN evidence, not a new durable label taxonomy.
