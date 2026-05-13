# integration_patterns.md

R&D integration pattern — explicit decision about HOW capabilities are
integrated into the target. The choice affects Stage-Gate ordering,
capability `depends_on` semantics, when the user has a working version
to look at, and the project's risk profile.

## When to read

- Writing the charter (Heilmeier H8) — integration pattern must be
  declared
- Designing the capability map (Layer 2) — `depends_on` interpretation
  depends on the chosen pattern
- Stuck on "we have 4 K's at TRL-3 but no working version"
- Deciding when to integrate ("is this the right time to wire C1, C2,
  C3 together?")

## The principle

Bottom-up integration (build each K to TRL-6, integrate at the end) is
**not the only pattern**. In fact, in most modern software / ML R&D
practice, it is the worst default — it produces nothing visible to the
user for weeks or months and surfaces integration risks late.

The R&D charter MUST declare which integration pattern this project
uses, so that:

1. The Stage-Gate ordering (`references/rd/rd_stages.md`) is interpreted
   correctly per pattern
2. The capability `depends_on` graph is built correctly
3. The "no working version yet" anti-pattern is structurally avoided
   when possible
4. Integration risk surfaces early (Pattern 1 / 3) when the
   architecture is well-understood enough

## The 3 patterns

### Pattern 1: Vertical slice (framework-first)

Build an abstract framework with **baseline / stub implementations** of
each K first. End-to-end working from day 1. Then iteratively replace
each baseline with a real K implementation, measuring the delta per
replacement.

```
Day 1-2: framework + K1_baseline + K2_baseline + ... = working v0
Day N:   replace K1_baseline → K1_real (Stage-Gate cycle for K1),
         measure delta vs v0
Day N+M: replace K2_baseline → K2_real, measure delta
...
Final:   all K's at TRL-6, framework remains as the integration
         surface
```

**Strengths**:
- Working version exists from day 1 (high user / stakeholder confidence)
- Each K's contribution is measured by A/B (replace baseline, observe
  delta)
- Integration risk surfaces immediately (the first day shows whether
  the architecture works)

**Weaknesses**:
- The framework constrains K design (premature abstraction risk)
- A naive baseline can mask the real technical difficulty of the K
- **Critical failure mode**: framework interface assumed wrong → all
  K's must be redesigned

**Best when**:
- Architecture is well-understood (e.g., "decision system = signal +
  sizing + operation + risk", and the slot definitions are stable)
- K's are well-defined "slots" in a known architecture
- Baseline implementations exist (e.g., constant input, equal allocation,
  static cost model — these are real implementations, not stubs)

**Bad fit when**:
- The K's output shape is itself the research question (e.g., K =
  "regime classifier" where N regimes is the research result)
- The K's input requirements are research-dependent
- The architecture is fundamentally unknown (you don't know what
  framework to write)

### Pattern 2: Bottom-up (component-first)

Build each K to TRL-6 in isolation. Integrate at the end (one big
integration capability that depends on all K's).

```
Day 1-N1: K1 Stage-Gate cycle to TRL-6 (Scoping → De-risk → Build →
          Validate → Integrate-with-stub-environment)
Day N1-N2: K2 Stage-Gate cycle to TRL-6
...
Day final: integration capability runs (depends on all K's)
```

**Strengths**:
- Each K can be optimized without integration constraints
- Technical surprises in K stay isolated (don't break other K's)
- Phenomenon-oriented sibling workstreams may align with this when the
  target is truly establishing each technology before integration

**Weaknesses**:
- No working end-to-end until very late
- Integration surprises late (interfaces, data flow, latency
  interactions)
- User has nothing visible until integration capability matures
- Sunk cost bias: K1 polished to TRL-6 might not match what K2 / K3
  need from it; rework expensive

**Best when**:
- K's are genuinely independent technologies (e.g., K1 = "validation
  methodology paper-publishable on its own", K2 = "implementation engine
  paper-publishable on its own")
- Architecture is unknown and will be discovered through K
  characteristics
- K's have asymmetric difficulty — one K might fail, kill the project,
  and you don't want to have built the rest

**Bad fit when**:
- Target capability is a system, not a collection of technologies
- Time-to-working-version matters (stakeholder pressure, deployment
  deadline)
- K's interface to each other in non-trivial ways

### Pattern 3: Skeleton + spike (recommended default)

Build a **minimal end-to-end skeleton** with the simplest possible
implementations for each component. The skeleton is throwaway — its
purpose is to validate the architecture and surface integration
issues, NOT to be the framework. Then identify which components are
genuinely "research-worthy" K's; the rest stay as dependencies. Each
K then gets its own Stage-Gate cycle, replacing the skeleton's
component with the real implementation.

```
Day 1-3: skeleton (minimal end-to-end with naive components):
         simplest signal (e.g., constant or moving average), simplest
         sizing (equal weight), simplest cost (constant bp), single
         instrument, single period
Day 4:   review skeleton — which components are K (need research)
         vs dependency (use as-is)?
Day N:   K1 Stage-Gate cycle, replace skeleton component → K1_real,
         measure delta vs skeleton
Day N+M: K2 Stage-Gate cycle, replace another component, measure
         delta
...
Final:   all K's at TRL-6, skeleton was discarded long ago
```

**Strengths**:
- Working version exists by day 3 (between Pattern 1 and Pattern 2)
- Architecture validated early (integration risk surfaced on day 1)
- No framework record-in — skeleton is throwaway, not a permanent
  abstraction
- "Research-worthy" K identification done after seeing the skeleton
  work — separates "real research" from "engineering"
- Each K's value measurable by A/B vs skeleton baseline

**Weaknesses**:
- More rework than Pattern 1 if early architecture is wrong
  (skeleton itself thrown away)
- More commitment than Pattern 2 (you've built infrastructure that
  may need replacement)

**Best when**:
- Medium uncertainty: architecture's broad shape is known, specific
  components are research questions
- Project has time budget for ~3 days of skeleton work upfront
- Stakeholder confidence matters but time-to-final-product also
  matters

**Default for this skill**: when no specific reason to choose
Pattern 1 or Pattern 2, **Pattern 3 is recommended**. It avoids the
"no working version" anti-pattern of Pattern 2 and the "premature
framework" risk of Pattern 1.

## Decision tree (which pattern?)

```
Q1: Is the target architecture well-understood at the start?
    (Can you draw the system diagram with confidence?)
    → YES: continue to Q2
    → NO: Pattern 2 (bottom-up); architecture will emerge from K work

Q2: Can you write a meaningful baseline / stub for each K?
    (E.g., "constant signal" for a signal K, "equal weight" for a
    sizing K — not literally `pass`)
    → YES: continue to Q3
    → NO: Pattern 2

Q3: Are the K's interfaces stable (you know what each K's inputs and
    outputs are)?
    → YES: continue to Q4
    → NO: Pattern 3 (skeleton will validate interface assumptions
       cheaply)

Q4: Does stakeholder confidence / "show progress" matter?
    → YES: Pattern 1 (vertical slice, working v0 day 1)
    → NO: Pattern 2 (bottom-up, optimal per-K maturation)

Default if Q1-Q4 are unclear: **Pattern 3 (skeleton + spike)**.
It hedges between extremes.
```

## How each pattern maps to Stage-Gate

The 5 stages (Scoping → De-risk → Build → Validate → Integrate) are
defined in `references/rd/rd_stages.md`. The pattern affects the
**ordering** and **scope** of stages, not the stages themselves.

### Pattern 1 mapping

- **Project Scoping** (before any K Stage-Gate): design framework,
  define K interfaces, write baselines for each K
- **Per-K Stage-Gate**: full 5-stage cycle for each K, replacing the
  baseline with real implementation
- **Integrate stage per K**: replacement test (A/B vs baseline) → if
  delta is positive and meets criteria, K is `matured`
- **No final integration capability** — integration is continuous

### Pattern 2 mapping

- **Per-K Stage-Gate**: full 5-stage cycle in isolation; the K's
  Stage 5 (Integrate) is integration with stub upstream/downstream
- **Final integration capability** (`core_tech_id == integration`)
  runs Stage-Gate after all K's `matured`
- Promotion checks must use the declared integration pattern. Pattern 2
  requires final integration after all upstream K capabilities mature.

### Pattern 3 mapping

- **Skeleton phase** (before Layer 1 closure): build the minimal
  end-to-end version. This is **engineering work, not a Stage-Gate
  cycle** — record in `decisions.md` as "skeleton built, components:
  ..., next step: K identification"
- **K identification**: review the skeleton, identify which components
  are research-worthy (per `core_technologies.md` operational
  filter); other components stay as dependencies
- **Per-K Stage-Gate**: 5-stage cycle for each identified K, replacing
  the skeleton's component
- **Integrate stage per K**: replacement test (A/B vs skeleton's
  component) → if delta meets criteria, K is `matured`
- **Final integration capability** (optional): an end-to-end
  evaluation after all K's matured, often with non-skeleton conditions
  (multi-instrument, multi-regime). This is `core_tech_id ==
  integration` in capability_map.md.

## Capability map differences per pattern

The `depends_on` field in capability_map.md (Layer 2) takes different
shapes per pattern:

### Pattern 1
- Most C's depend on `framework` (a non-K capability) and on a
  baseline-stage capability for the same K
- `framework` capability is at TRL-6 from day 1 (built upfront)
- Each K's `Integrate` stage exit = "K_real replaces K_baseline in
  framework, A/B vs baseline meets criteria"

### Pattern 2
- C's under different K's are largely independent (`depends_on`
  empty within Layer 1)
- One `core_tech_id == integration` C with `depends_on = [all K's]`
- Integration C's `Integrate` stage exit = the entire system test

### Pattern 3
- C's under different K's are largely independent (similar to
  Pattern 2)
- Each K's `Integrate` stage = "K_real replaces skeleton's
  corresponding component in skeleton, A/B vs skeleton meets criteria"
- One optional `core_tech_id == integration` C for final end-to-end
  evaluation under realistic conditions

## When to switch patterns mid-project

**Don't, if avoidable.** Pattern switching mid-project is a major
deviation:

- Pattern 2 → Pattern 1 mid-project: requires building the framework
  retroactively, often after K's are already too far along; almost
  never works cleanly
- Pattern 3 → Pattern 2 mid-project: discard the skeleton, restart
  per-K isolated work — typically because the skeleton revealed the
  architecture is wrong (which is itself a finding)
- Pattern 1 → Pattern 3: if framework is failing, fall back to
  skeleton; framework becomes throwaway

If pattern switch is needed, file a deviation entry in `decisions.md`
naming:
- The trigger (specific observation that forced the switch)
- The new pattern
- What artifacts from the old pattern are kept / discarded
- Whether the K Stage-Gate cycles need to restart or can continue

## Anti-patterns

### Anti-pattern A: Missing integration pattern (no decision)

The project starts capability decomposition without explicitly
declaring an integration pattern. This blocks capability decomposition and
Stage-Gate work because `depends_on`, Stage 5, and promotion ordering cannot
be interpreted. Symptoms: 4 K's at TRL-3, no working end-to-end version,
stakeholder asking "what does it look like?".

**Fix**: charter must declare integration pattern (Heilmeier H8). If the
pattern is missing, stop and amend the charter before writing Layer 2 rows or
running Stage gates.

### Anti-pattern B: Pattern 1 with naive baselines that don't compile

Framework is built but baselines are literal `pass` statements or
return-zero functions. The "working v0" doesn't actually do anything;
it's an integration test of the framework, not a working system.
Stakeholders see "it runs" but nothing happens.

**Fix**: baselines must be real implementations (constant signal,
equal weight, static cost) that produce meaningful (if naive)
output. If you can't write a meaningful baseline, Pattern 1 is the
wrong choice — switch to Pattern 3 or Pattern 2.

### Anti-pattern C: Pattern 3 skeleton becomes the framework

The skeleton was supposed to be throwaway, but it's been around for
weeks and the team treats it as the framework. K's are now
constrained by the skeleton's interface decisions.

**Fix**: explicitly time-box the skeleton ("skeleton phase ends day
3, K identification done by day 5"). After K identification, the
skeleton is acknowledged as throwaway — when K's mature, the
skeleton's component is replaced AND the surrounding interface may
also change.

### Anti-pattern D: Pattern 2 with stakeholder pressure

Project chose Pattern 2 ("each K is its own technology, mature
independently"), but stakeholder is asking weekly for progress
demos. Team starts hacking together "demo wrappers" that show K's
in isolation. Demo wrappers consume time without contributing to K
maturation.

**Fix**: this is a sign Pattern 2 was the wrong choice. If
stakeholder confidence matters, switch to Pattern 1 or Pattern 3
(file the deviation).

## Worked example

**Target**: "Build a real-time signal decay detector for production
production signals."

### Pattern 1 (vertical slice) approach

Architecture is well-understood: decay detector = signal-history
buffer + change-point detection algorithm + alert dispatch.
Baselines:
- buffer: simple in-memory deque, last 30 days
- change-point: rolling Z-score on primary metric vs baseline mean, threshold
  alarm
- alert: print to stdout

Day 1: framework + 3 baselines = working v0 (alarms on stdout when
Z > 2). Already useful, even if naive.

Per-K Stage-Gate:
- K1 (sophisticated change-point detection: Bayesian online change
  point) replaces baseline — measure FPR / FNR delta vs Z-score
- K2 (multi-horizon decay characterization: 1d / 5d / 20d) replaces
  baseline — measure decay-window precision delta
- K3 (alert routing + suppression) replaces stdout — measure alert
  noise reduction

### Pattern 2 (bottom-up) approach

Treat the 3 components as 3 independent research projects:
- K1 (Bayesian online change point) developed to TRL-6 with
  paper-quality validation in isolation (synthetic data + real
  signal traces)
- K2 (multi-horizon decay characterization) similarly
- K3 (alert routing) similarly
- Final: integration test wires K1 → K2 → K3, evaluates on real
  operations-floor traffic

Risks: K1's Bayesian framework might output posterior distributions
that K2 expects as point estimates; integration interface mismatch
discovered at end.

### Pattern 3 (skeleton + spike) approach

Day 1-3: skeleton:
- Buffer: in-memory deque, last 30 days (1 hour to write)
- Change-point: rolling Z-score on primary metric (2 hours)
- Alert: print to stdout (5 minutes)
- Wire end-to-end: 4 hours
- Total: < 1 day

Day 4: review skeleton — observations:
- Z-score change-point gives too many false positives (10x expected) →
  K1 (sophisticated change-point) is research-worthy
- Single-horizon decay misses fast decays (< 5 days) → K2 (multi-
  horizon) is research-worthy
- stdout alerts are fine for v1 (alert routing is engineering, not
  research) → no K for alerts

K1 and K2 enter Stage-Gate cycles. K3 (alerts) stays as a dependency.
Skeleton is replaced piece by piece as K's mature.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| No pattern declared in charter | Missing integration pattern blocks Layer 2 and Stage-Gate interpretation | Charter H8 must declare pattern + reason |
| Pattern 1 with stub baselines | "v0 runs but does nothing" | Use real (if naive) baseline implementations |
| Pattern 3 skeleton treated as framework | Skeleton is months old, K's constrained by it | Time-box skeleton; treat as throwaway |
| Pattern 2 with stakeholder pressure | "Demo wrappers" being built that don't advance K's | Switch to Pattern 1 or 3 |
| Pattern switch without deviation | Silent shift mid-project | File deviation in decisions.md naming trigger |

## Relationship to other references

- `references/rd/rd_charter.md` § H8 — integration pattern is part of
  the final exam definition (see updated H8 in this file's session)
- `references/rd/rd_stages.md` — Stage interpretation differs per
  pattern (see § How each pattern maps to Stage-Gate above)
- `references/rd/capability_map_schema.md` — `depends_on` semantics
  differ per pattern (see § Capability map differences per pattern)
- `references/rd/rd_promotion_gate.md` § D — promotion is pattern-aware:
  Pattern 1 checks per-K baseline replacement, Pattern 2 checks final
  integration after upstream maturity, and Pattern 3 checks skeleton
  replacement plus any declared final integration capability
- `references/rd/core_technologies.md` § operational filter — for
  Pattern 3, the filter runs AFTER skeleton phase (you identify K's
  by reviewing the skeleton)
