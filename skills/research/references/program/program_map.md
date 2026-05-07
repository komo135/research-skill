# program_map.md

Optional coordination map for multiple R&D and Pure Research projects.

## When to read

- Several projects share dependencies, milestones, or sequencing risk
- A Pure Research finding may feed an R&D project
- An R&D capability blocks another R&D target
- A user asks for program-level planning across research projects

## Boundary

The program map is a read-only coordination view over child project state. It
does not own TRL, analysis tier, promotion, or claim truth. It also does not
own kill decisions, support status, capability maturity, or research scope.

Child projects remain authoritative:

- R&D state lives in each child `capability_map.md` and `decisions.md`
- Pure Research state lives in each child `explanation_ledger.md`,
  pre-registration files, and `decisions.md`
- Promotion and support decisions are made only by the child project's gates
- Program notes cite child evidence; they do not reinterpret it

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

| Project | Discipline | Coordination concern | Next child gate | Authoritative source |
|---|---|---|---|---|
| <project> | R&D / Pure Research | <handoff, sequencing, or staffing concern> | <gate name + date/trigger> | <path + row/section> |

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

A Pure Research claim may be consumed by R&D only as an assumption,
requirement, dependency, scope condition, benchmark, or maintenance trigger.
The R&D project must cite the Pure Research source and state how the finding is
used in the R&D charter, capability dependency, benchmark, or maintenance
decision.

Do not copy the claim itself into the R&D ledger as if the R&D project proved
it. The R&D project consumes the boundary condition; the Pure Research project
owns the claim and its support status.

Handoff examples:

- Assumption: "Volatility-decay mechanism holds under scope S; cite Pure
  Research project P, Q/E row, and promotion decision."
- Requirement: "Capability C must preserve condition X because the source
  claim only applies under X."
- Dependency: "`dependent_on_research` blocks C until project P reaches the
  required tier."
- Scope: "R&D target excludes markets outside the Pure Research claim scope."
- Benchmark: "R&D final exam must beat the baseline implied by the finding."
- Maintenance trigger: "If the Pure Research claim is revised or parked,
  re-run R&D validation."

## Relationship / routing labels

Use these labels when a program map needs a compact relationship or routing
graph:

| Type | Meaning |
|---|---|
| `research_to_rd` | Pure Research claim consumed by an R&D project |
| `rd_to_rd` | R&D capability or project consumed by another R&D project |
| `rd_observation_to_research` | R&D observation motivates a new Pure Research project |
| `shared_infra` | Shared code, data pipeline, or tracker dependency |
| `integration` | Downstream system-integration dependency |

`rd_observation_to_research` is a routing label, not a shortcut around
pre-registration. The Pure Research child project still owns its PR/FAQ,
pre-registration, explanation ledger, and claim review.

## Operating rule

At program review time, read child ledgers first. If a coordination question
requires changing TRL, analysis tier, support status, scope, kill state, or
promotion, stop and perform that change inside the child project protocol.
