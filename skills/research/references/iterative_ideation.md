# Iterative Ideation with Mandatory Executable Feedback

## Purpose

Single-pass ideation (Idea portfolio → promote one candidate) tends to lock in early picks even when minimal executable evaluation would dramatically re-rank the portfolio. This file adds an iterative protocol for domains where a minimal executable evaluator already exists and can be invoked from the agent's session.

**TDD-validated** (1 round of RED/GREEN): without mandatory executable invocation, agents simulate fitness from prior knowledge ("literary estimates dressed as measurements", self-quote from a RED-baseline agent) and proceed to single-pass-equivalent picks. With mandatory real shell / command-line execution + an EXPLICITLY FORBIDDEN self-simulation clause, agents either obtain real fitness or honestly mark candidates `killed` when their evaluator path does not exist.

## Skill role boundary

This protocol provides structured evolutionary feedback on candidates; the candidates themselves come from `references/ideation.md` and `references/assumption_audit.md` after substrate ids, generation operators, changed premises, and anti-vacuity checks are recorded. The protocol's value is preventing single-pass lock-in and forcing real-fitness ranking when an evaluator exists.

L3-L4 paradigm-shift generation remains structurally outside the skill's scope (see `SKILL.md`).

## Scope

**Required preconditions** (all three):
1. Plan category is `applied_research` or `experimental_development`
2. A minimal executable evaluator exists for the domain and is invocable through a real shell / command-line command (e.g., `quant-research/scripts/walk_forward.py` with a working CLI binding and accessible data)
3. The agent has command-line execution access and the per-candidate execution time fits within the session's time budget

**Out of scope**:
- `basic_research` plans in any mode (use `references/assumption_audit.md` alone; basic-research evaluators are typically observation-based, not script-based)
- Domains without an existing executable evaluator (run candidates as plain Idea portfolio → constraint-naming for the missing evaluator → ADJACENT plan to build the evaluator)
- Plans where data access is blocked (PARK with named constraint until data becomes available)

If preconditions are not met, do NOT invoke this protocol. Falling back to simulated fitness defeats the protocol's purpose; the single-pass Idea portfolio is honest in such cases.

## Protocol

### Cycle 0 — Standard ideation

Run normal `Idea portfolio` (de-anchoring + observation discovery + assumption_audit + hypothesis synthesis + quality-diversity). Produce 6 candidates.

Each candidate must have an **executable signature**: an explicit shell / command-line invocation (or sequence) that would evaluate it.

Example (quant):
```bash
python skills/quant-research/scripts/sanity_checks.py --signal <signal_def> --data <data_path>
python skills/quant-research/scripts/walk_forward.py --signal <signal_def> --folds 3 --window 6M
```

If a candidate cannot be expressed as a runnable command, PARK it with named constraint (per `assumption_audit.md` constraint-naming protocol). Do NOT proceed to evolutionary cycles with un-runnable candidates.

### Cycle N (N=1, 2) — Evolutionary update

#### Step 1 — MANDATORY real command-line execution (NOT simulation)

For each candidate, invoke the executable signature through a real shell / command-line runner. Capture `logs/stdout.log` and `logs/stderr.log`, update `run_manifest.json`, and persist the parseable fitness vector as a durable artifact such as `outputs/fitness.json`, `tables/fitness.csv`, or an `intermediate/` diagnostic. Parse fitness from the artifact, not from terminal scrollback. stdout is not evidence; a print-only evaluator run is not admissible feedback.

**Agent simulating fitness is EXPLICITLY FORBIDDEN.** Specifically forbidden:
- Estimating fitness from prior knowledge of mechanism ("Sharpe ≈ 1.5 based on the literature")
- Skipping the real command-line invocation because "the script presumably does X"
- Fabricating stand-in fitness numbers to keep the cycle alive
- Re-defining "executable signature" to mean "the script imports without error"
- Hand-coding a toy `run_pipeline` over synthetic returns to make the evaluator print numbers and laundering those as the candidate's fitness (the numbers would measure the toy, not the candidate)

If script execution fails (no data, missing args, runtime error, etc.), mark the candidate `killed` with the actual failure reason recorded. Do not fabricate a fallback fitness.

#### Step 2 — Fitness analysis

Analyze REAL fitness numbers from run artifacts, plus the `run_manifest.json`, relevant `logs/stdout.log` excerpts for debugging context, and the candidates' mechanism signatures. Keep the predeclared fitness vector separate from candidate prose so the analysis does not become a self-justifying narrative. Console output may point to files, but the durable artifact is the evidence.

The analysis records:
- Top-2 candidates by fitness vector dominance (primary metric, then variance, then turnover-adjusted variant)
- Mechanism signature of each top candidate (which data assumption / metric / evaluation protocol / horizon / gate axis values the candidate uses)

The predeclared fitness vector and durable artifacts are what reduce rubric leakage. Do not revise the rubric after seeing candidate identities or scores.

#### Step 3 — Mutation

For each top-2 candidate, produce 1 variant by changing exactly ONE mechanism axis from `{data assumption, signal metric, evaluation protocol, horizon, conditioning gate}`.

**Threshold tweaks, seed changes, and window-size sweeps are NOT mutations.** They are parameter sensitivity sweeps (use `sensitivity_grid.py` for those). Mutation requires changing an axis the candidate is built on, not a parameter within that axis.

#### Step 4 — Crossover

Combine mechanism elements from the 2 top candidates into 1 new candidate. The crossover candidate must define a single coherent mechanism that draws axis values from both parents — not a concatenation like "candidate uses both signal A and signal B".

Example (quant): if parent 1 uses `metric = dispersion-z, gate = sector-decile` and parent 2 uses `data = order-flow, gate = liquidity-top-200`, a crossover might be `metric = dispersion-z conditioned on order-flow imbalance gating, gate = sector-decile ∩ liquidity-top-200`. The mechanism reads as one signal, not two stapled together.

#### Step 5 — Wildcard

From the observation pool generated in Cycle 0's observation discovery pass, pick the candidate with maximum cosine distance to the current portfolio's mechanism signatures. This is the explicit anti-convergence injection.

Wildcard prevents the portfolio from collapsing toward a single mechanism family across cycles. If max-distance candidate already exists in the portfolio (rare but possible), pick the second-max.

#### Step 6 — Replacement

Next-cycle portfolio = top-2 (kept) + mutation-2 (one variant per top) + crossover-1 + wildcard-1 = **6 total**.

### Stopping

Stop iteration when ANY of:
- Cycle ≥ 2 AND primary-metric improvement vs previous cycle < epsilon (default ε domain-specific; for quant Sharpe-based: 0.1)
- Cycle = 3 (hard cap)
- Time budget exhausted (per-candidate command execution time × 6 × remaining cycles exceeds session budget)
- All candidates are marked `killed` in Cycle 1 (typically indicates scope precondition is not met — the executable evaluator does not actually exist or data is not accessible)

### Promotion

Cycle-final top candidate (by fitness vector dominance) is promoted to the plan's `Plan` section.

Record in `plans/<id>.md`:
- The executable signature (shell / command-line invocation) — for reproducibility
- The fitness vector and any confidence interval / variance
- The run directory and durable artifact path used for the fitness vector
- A one-sentence rationale for why this candidate dominated cycle-finals

**Fitness scores from intermediate cycles are run-local evidence, not project-level memory.** They must remain as durable artifacts inside the relevant run directories so the cycle is auditable, but they are NOT copied into `decisions.md` or `project_state.md`. Only the final promoted candidate's fitness becomes part of the durable plan narrative. This avoids back-leak that would contaminate the next plan's ideation while preserving auditability of the current cycle.

## Anti-failure-mode design (lessons from TDD)

| Failure mode | F v2 design counter |
|---|---|
| **AlphaEvolve trap** (protocol silently selects for evaluator-rich problems across the project) | Scope restriction in this file: only applies when executable evaluator already exists. For domains without, use assumption_audit + ADJACENT-plan for evaluator construction. |
| **Rubric leakage** (gate criteria leak into ideation prompt) | Fitness is computed by command execution, persisted as a durable artifact, and parsed against a predeclared fitness vector (Step 2). Main agent prompt has no PASS criteria. |
| **Self-simulation** (agent estimates fitness from prior) | Cycle N Step 1 explicitly forbids simulation. Candidate-level `killed` classification is mandatory if execution fails. TDD GREEN-run agent rejected 3 named rationalization paths under this clause. |
| **Back-leak via durable state** | Intermediate fitness artifacts stay in run directories; only final promoted candidate's fitness goes to durable plan record. |
| **Friction overflow** | Hard cap: 2-3 cycles × 6 candidates × 1 evaluator call <= 18 command-line executions per plan. |
| **Mutation as parameter sweep** | Step 3 explicitly requires axis change; threshold/seed/window tweaks are disallowed. |
| **Wildcard as control** | Step 5 mandates max-cosine-distance heuristic, not random. |

## Common failures

- **Invoking the protocol when no executable evaluator exists**: scope violation. Symptom: every candidate is marked `killed` in Cycle 1 (TDD GREEN run reproduced this exactly when the quant-research scripts turned out to be CLI-less). The honest deliverable is "the harness does not exist, ADJACENT plan needed to build it" — not fabricated fitness.
- **Synthesizing toy data to keep command execution alive**: the toy `run_pipeline` returns real Sharpe numbers, but they measure the toy, not the candidate. This is the most seductive failure mode and is explicitly named in Cycle N Step 1's forbidden list.
- **Print-only evaluator scripts**: a command that only prints metrics has not produced valid feedback. Use `scripts/check_run_artifacts.py`; if no durable artifact exists, mark the candidate blocked or killed rather than ranking it from stdout.
- **Re-defining "executable signature" loosely**: e.g., counting `python script.py` (no args, exits silently) as evaluation. The signature must produce a parseable fitness output.
- **Mutation-as-parameter-tweak**: agent produces variants that change a threshold from 2.0 to 2.5. This is sensitivity_grid territory, not mutation.
- **Changing Step 2 after seeing scores**: revising the fitness vector after candidate identities or scores are known re-introduces rubric leakage. Predeclare the vector, persist artifacts, and then parse.
- **Crossover as stapling**: "candidate uses both signal A and signal B" is not a mechanism-coherent crossover. The crossover must define a single coherent mechanism.

## Relationship to other reference files

- `references/ideation.md` — provides Cycle 0 (de-anchoring + observation discovery + hypothesis synthesis + quality-diversity). This file picks up after quality-diversity pass.
- `references/assumption_audit.md` — runs during Cycle 0 (between observation discovery and hypothesis synthesis). The constraint-naming protocol handles candidates that cannot be expressed as runnable commands (PARK with named constraint).
- `references/claim_structure.md` — the promoted candidate's eventual claim uses the existing 5-field schema. Statistical reporting minimum applies to the fitness numbers reported in evidence.
- `quant-research/scripts/*.py` — the executable evaluators referenced for the quant domain. **Note**: as of the TDD run, these scripts are libraries without CLI bindings. A separate plan / PR is needed to add CLI entry points for them to be usable as F v2 evaluators. Until that work lands, F v2 cannot be invoked for quant-research applied plans; use single-pass ideation with assumption_audit instead.

## Sources

- TDD validation: 1 round of RED (F v1, simulation allowed) vs GREEN (F v2, real command-line execution mandatory) on intraday equity mean-reversion ideation case
  - RED agent produced 18 literary-estimate fitness values, self-quoted as "literary estimates dressed as measurements"
  - GREEN agent invoked the command-line evaluator path 11 times, captured real "no_CLI/no_data" failure, marked all candidates `killed`, and explicitly rejected 3 rationalization paths
- Empirical basis: Si 2024/2025 (Ideation-Execution Gap), AlphaEvolve / Google Co-Scientist (evaluator-grounded evolutionary search). F is a markdown-skill protocolization of the evaluator-grounded approach for domains where minimal executable evaluator exists.
- Design basis: evaluator-grounded evolution is retained only after `references/ideation.md` has produced substrate/operator/anti-vacuity candidates and only when a real executable evaluator exists.
