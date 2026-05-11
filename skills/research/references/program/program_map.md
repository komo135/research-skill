# program_map.md

Optional coordination map for multiple projects or major workstreams.

## When to read

- Several projects or major workstreams share dependencies, milestones, or
  sequencing risk
- A Phenomenon / Mechanism Research finding may feed a Capability /
  Technology Research workstream
- A capability blocks another capability, project, or downstream target
- A user asks for program-level planning across research projects

## Boundary

The program map is a read-only coordination view over child project and
workstream state. It does not own TRL, analysis tier, promotion, or claim truth.
It also does not own kill decisions, support status, capability maturity, or
research scope.

Child projects and workstreams remain authoritative:

- Capability / Technology Research state lives in each child
  `capability_map.md` and `decisions.md`
- Phenomenon / Mechanism Research state lives in each child
  `explanation_ledger.md`,
  pre-registration files, and `decisions.md`
- Promotion and support decisions are made only by the child workstream's gates
- Program notes cite child evidence; they do not reinterpret it

A program map is not required merely because one project contains both
phenomenon and capability workstreams. Mixed workstreams are a normal project
shape. Use this file when coordination across projects or large workstreams is
useful enough to justify a separate roadmap view.

## Allowed contents

A program map may contain:

- Project list and purpose
- Relationship/routing graph between child projects
- Coordination risks such as duplicated work, missing handoff, or blocked
  sequencing
- Upcoming child gate that needs attention
- Pointers to child ledger rows and decision entries

It may not contain:

- New TRL values or analysis-tier ratings
- Program-level promotion or support vocabulary
- Rewritten claim statements detached from the child ledger
- A second copy of child project ledgers
- Evidence-artifact metadata fields that scripts or templates must populate
- Project-instance facts such as active symbols, selected symbols, tuned
  parameters, current performance metrics, selected models, candidate features, or concrete
  experiment conclusions

## Minimal structure

```markdown
# Program map: <name>

## Projects

| Project / workstream | Label | Coordination concern | Next child gate | Authoritative source |
|---|---|---|---|---|
| <project or WS-id> | <capability / phenomenon / other> | <handoff, sequencing, or staffing concern> | <gate name + date/trigger> | <path + row/section> |

## Relationships / routing

| From | To | Label | Coordination question | Source |
|---|---|---|---|---|
| <child> | <child> | <relationship/routing label> | <what needs coordination> | <child decision or ledger row> |

## Coordination decisions

| Date | Decision | Child source cited |
|---|---|---|
| YYYY-MM-DD | <sequencing or staffing decision> | <path + row/section> |
```

## Research-to-Technology Handoff

A Phenomenon / Mechanism Research claim may be consumed by Capability /
Technology Research only as an assumption, requirement, dependency, scope
condition, benchmark, or maintenance trigger. The consuming workstream must
cite the source and state how the finding is used in the charter, capability
dependency, benchmark, or maintenance decision.

Do not copy the claim itself into the capability ledger as if the consuming
workstream proved it. The capability workstream consumes the boundary
condition; the phenomenon workstream owns the claim and its support status.

Handoff examples:

- Assumption: "Volatility-decay mechanism holds under scope S; cite
  phenomenon workstream P, Q/E row, and promotion decision."
- Requirement: "Capability C must preserve condition X because the source
  claim only applies under X."
- Dependency: "`dependent_on_research` blocks C until workstream P reaches the
  required tier."
- Scope: "Capability target excludes markets outside the phenomenon claim
  scope."
- Benchmark: "Capability final exam must beat the baseline implied by the
  finding."
- Maintenance trigger: "If the phenomenon claim is revised or parked, re-run
  capability validation."

## Relationship / routing labels

Use these labels when a program map needs a compact relationship or routing
graph:

| Type | Meaning |
|---|---|
| `research_to_rd` | Phenomenon claim consumed by a capability workstream or R&D-compatible project |
| `rd_to_rd` | Capability workstream or R&D-compatible project consumed by another capability target |
| `rd_observation_to_research` | Capability observation motivates a new phenomenon workstream |
| `shared_infra` | Shared code, data pipeline, or tracker dependency |
| `integration` | Downstream system-integration dependency |

`rd_observation_to_research` is a routing label, not a shortcut around
pre-registration. The Phenomenon / Mechanism Research workstream still owns its
PR/FAQ, pre-registration, explanation ledger, and claim review.

## Operating rule

At program review time, read child ledgers first. If a coordination question
requires changing TRL, analysis tier, support status, scope, kill state, or
promotion, stop and perform that change inside the child project protocol.
Project decision gates likewise cite child workstream gates; they do not
re-score TRL, support status, or A-tier.
