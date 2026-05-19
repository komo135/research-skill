# Experimental Development

## When this category applies

Experimental development is systematic work, drawing on knowledge gained from research and practical experience and producing additional knowledge, directed to producing new products or processes or improving existing products or processes (Frascati Manual, OECD 2015). In this agent skill, products and processes include research artifacts, tools, systems, services, workflows, and delivery practices used in the project.

Classify by the plan's intended output and acceptance uncertainty, not by source. Implementing a research paper is experimental development only when the primary deliverable is a new or improved functioning artifact/process plus the additional knowledge needed to make it work. If the primary purpose is new knowledge directed toward a specific practical objective, use applied research.

Pick experimental development when:

- You are building a system or prototype that has to function end-to-end.
- The success criterion is "it works" plus some performance threshold, not "we improved the metric."
- The work involves engineering decisions (architecture, dependencies, deployment shape) that are part of the deliverable.
- A user — possibly future-you — will run the artifact and rely on its behavior.

Examples: building a reference implementation of a published method, engineering a data pipeline for a domain that did not have one, prototyping an interactive tool, hardening a research codebase into something a non-author can run, implementing a non-trivial algorithm with correctness tests.

This is not "applied research with code." Applied research is organized around new knowledge for a specific practical aim or objective. Experimental development is organized around systematic work that creates or improves an artifact/process and records the additional knowledge needed for it to operate under stated conditions.

## Typical outputs

- Working prototype: executable system, library, tool
- Performance characterization: latency, throughput, accuracy under realistic load, resource consumption
- Operational documentation: how to use it, what fails, known edges
- Integration with existing systems
- Known-limitation catalog

## Default plan mode

`milestone`. Define:

- What "working" means (specific functional requirements)
- Performance thresholds the system must meet
- Test scenarios that constitute acceptance
- What is out of scope for this iteration

Milestone mode differs from confirmatory:

- Confirmatory fixes a hypothesis/objective, evidence measure, and decision threshold
- Milestone fixes acceptance criteria ("system handles input class A, latency under T ms, returns correct output on the regression suite under conditions C")

One plan still declares one mode. A milestone plan may include benchmark thresholds as acceptance criteria, but if the benchmark comparison becomes the load-bearing evidence for a methods claim, open a separate applied-research derived hypothesis with confirmatory mode instead of making the plan both milestone and confirmatory.

`exploratory` mode is sometimes appropriate for very early-stage development (figuring out what is even buildable). Switch to `milestone` once the shape of the system is clear.

## Completion conditions

Acceptable completion shapes:

- All milestones met under stated conditions
- Some milestones met, others explicitly deferred with reasoning
- System works for use case A but not B — scoped completion
- System cannot meet the milestones with available approach — negative result with diagnosis

Not acceptable as completion:

- "It runs on my machine" without acceptance test evidence
- Performance claims based on a single run
- Functional claims based on the happy path without testing edge cases
- "Works" without specifying what input space and conditions it works for

## Report shape

Use `assets/report/experimental_development_report.md.template`.

1. **Summary** — what was built and what it does
2. **Background** — what the artifact is for, what existed before, why this iteration
3. **System description** — architecture, key design decisions, deployment shape, dependencies (conceptual, not env-lock)
4. **Performance** — measured behavior under stated conditions, with figures
5. **Operational limits** — known failure modes, edge cases, resource boundaries
6. **Limitations** — conditions not tested, known failure modes, and resource boundaries

The "Methods" section of applied research becomes "System description" here. The artifact itself is the deliverable; design decisions get documented because anyone using or extending the artifact needs them.

## Claims in experimental development

Claims are typically of the form "system S handles input class X under conditions Y with performance Z." For the claim to be load-bearing:

- `evidence` must cite the acceptance tests and performance measurements
- `alternatives_not_excluded` lists confounders (cached state, lucky inputs, warm-start effects, single hardware configuration)
- `conditions_tested` specifies the input distribution and operating conditions tested
- `conditions_not_tested` calls out untested inputs, scales, or deployment regimes

Performance claims need variance across multiple runs, not single measurements. If a system "handles 1000 QPS" based on one trial, that is not a claim about the system's typical behavior.

Example claim record:

```yaml
- claim: The implemented inference server handles 850 requests/second median throughput at p99 latency under 120 ms on a single A100 for the 7B-parameter model under the regression test load.
  evidence: propositions/P001_serving-system/hypotheses/H001_load-test/experiments/runs/H001__012__seed0/outputs/loadtest_results.json; figures/latency_distribution.png
  alternatives_not_excluded:
    - "Single hardware tested (1× A100, no NUMA effects measured)"
    - "Synthetic request distribution (constant prompt length, may not reflect real load)"
    - "Warm-up effects: throughput in first 30s excluded; cold-start latency not characterized"
  conditions_tested: "A100 80GB, batch size autotune ∈ [1,32], prompt length 64 tokens, completion 32 tokens, request rate ramp 100→1500 QPS over 10 minutes"
  conditions_not_tested:
    - "Multi-GPU sharding"
    - "Variable prompt lengths"
    - "Sustained load >10 minutes (memory leak window)"
```

## Analysis weight

For experimental development, analysis takes two shapes — both required:

**Profiling** (EDA-equivalent): characterize the input space, expected load, edge inputs. This informs the acceptance test design. Without profiling, "it works" means only "it works on the inputs I happened to try."

**Acceptance test deep-dive**: after each milestone gate, run analysis on the test outputs:

- Performance distribution (median, p99, tail) — not point estimates
- Error / failure cases — what fails and why
- Resource consumption under load
- Behavior at edges of the declared input space

The claim-recording minimum for experimental development:

- Variance across multiple runs (single-run performance numbers are not characterization)
- Edge-case coverage in acceptance tests
- Operational limits explicitly probed (when does it break, not just "it works in the happy path")
- Failure-mode catalog as a first-class deliverable

Performance claims are distribution claims. Report the distribution, not a single number.

## Pitfalls

- **Confusing the prototype with the result.** The artifact existing is not the result; the artifact working under stated conditions is. "I built a system" without test evidence is not a completed milestone.
- **Demo-driven evaluation.** A demo on hand-picked inputs is not evidence the system works generally. Acceptance tests must cover the declared input space.
- **Skipping edge cases.** Most production failures are edge cases. Completion criteria should include edge-case scenarios.
- **Documentation debt.** A working artifact that nobody else can run is half-built. The System description in the report must let a non-author bring the artifact up.
- **Promoting development to a component-causality claim without evidence.** Claiming "system S works because of component I" requires an ablation or controlled intervention. Without that evidence, the claim is "system S works under stated conditions," not "component I is the reason."
- **Hidden infrastructure changes.** Modifying lib/ or shared infrastructure as part of development without recording it in the relevant project, proposition, or hypothesis `decisions.md` makes the change invisible to other hypotheses.
- **Single-run performance numbers.** Performance is a distribution. Report it as one.
