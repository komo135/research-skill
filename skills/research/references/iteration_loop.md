# Iteration Loop

## Purpose

After every interpreted result, the agent must select exactly one of five branches and log it. This forces explicit narrative continuity across sessions — the next agent reading `decisions.md` and `plans/<id>.md` knows what was concluded and what to do next.

This is a finite-state choice. "Diagnostic detour," "let me keep exploring," "continue with intent" are not branches in this vocabulary. Pick one of the five.

## The five branches

### NEXT_STEP

Continue the same plan. No question change, no scope change, no new uncertainty. The next planned step proceeds.

Use when:

- The result was expected and the plan's next step follows naturally
- One iteration of a planned sweep completes and the next iteration follows
- The plan has explicit sequential steps and the previous one passed its check

This is the only branch that does NOT require a new `decisions.md` entry. Routine forward progress on a written plan does not need to be logged each time. All other branches require an entry.

### REFINE

Narrow or change the question within the same plan. The plan ID stays; the plan's question, scope, or method changes prospectively.

Use when:

- The result showed the original question was ill-posed or too broad
- The result narrowed the interesting range to a sub-region
- The result revealed a confound that must be controlled before proceeding

Required `decisions.md` entry includes:

- What was the original question
- What is the refined question
- What evidence triggered the refinement
- Whether prior runs carry over as evidence under the refined question, or count as exploratory only

Update `plans/<id>.md` by **appending an Amendment to the Amendments section** — do not rewrite the original Plan section. The original Plan + `created_commit` are the time-anchored historical record. The latest amendment is the "current" plan state. See `rd_plan.md` Amendments section schema.

If the change is fundamental enough that it no longer reads as an amendment to the same question (different category, different mode, different objective), it is not REFINE — pick `ADJACENT` (new plan) or `CLOSE: replaced`.

### ADJACENT

Open a new related plan. A new question emerged that is distinct enough to warrant its own plan but is dependent on or motivated by this one.

Use when:

- The result raised a question that does not fit inside the current plan's scope
- A control experiment is needed that itself constitutes a research thread
- A baseline must be characterized before the main question can be answered (basic research opened by an applied plan)
- A failure mode discovered during development warrants its own investigation

Required `decisions.md` entry:

- The new plan ID and slug
- The dependency relationship (does this plan block the original? feed into it? run in parallel?)
- The triggering evidence

The original plan may continue (`NEXT_STEP` after this entry) or wait (`PARK` until adjacent resolves). Choose one explicitly.

### PARK

Pause the plan, with an explicit unblock condition.

Use when:

- The plan cannot proceed without external input (data not yet available, a dependency that must be built first)
- Compute/resource envelope is exhausted for this cycle and the plan resumes later
- A higher-priority plan needs resources

Required `decisions.md` entry:

- The named unblock condition (specific, testable — "data arrives" not "later")
- What state the plan is in: what has been done, what is pending
- Trigger that would prompt an unpark check

A parked plan is not abandoned. It is a deliberate pause with a resume contract. "PARK for now" without a stated unblock condition is forbidden — it converts into a soft `CLOSE: completed` without acknowledgment, which is dishonest.

### CLOSE

The plan is terminated. Three sub-cases — declare which one:

- **`CLOSE: completed`** — The plan answered its question for the declared scope. A report may follow.
- **`CLOSE: terminal_kill`** — Evidence accumulated showing the plan's objective is not achievable within the declared scope. Requires that the evidence has been audited (claim structure applied, alternatives addressed, repairable causes ruled out).
- **`CLOSE: replaced`** — The plan was superseded by another plan that subsumes it. Cite the replacement plan.

Required `decisions.md` entry:

- Sub-case (completed / terminal_kill / replaced)
- Final claim or conclusion (using claim_structure if load-bearing)
- Reference to report if produced
- Reference to replacement plan if applicable

`terminal_kill` is heavyweight. It claims the work is not achievable, which is a strong assertion. Rule out repairable causes first:

- Configuration error?
- Data defect?
- Scope error (the question was wrong, not the method)?
- Missing dependency that another plan could provide?

If any of these apply, the right move is `REFINE` or `ADJACENT`, not `terminal_kill`. Two failed runs under an unclean plan is not a kill. Multiple failed runs under a clean plan with no plausible repair is.

## Choosing the branch

Decision flow:

```
Did the result change the plan's question, scope, or method?
├─ No   → NEXT_STEP (no decisions.md entry needed)
└─ Yes  → Is the change inside this plan or outside?
          ├─ Inside (narrowing, controlling a confound)  → REFINE
          └─ Outside (a separate question or dependency) → ADJACENT
                                                            (+ PARK the original if it must wait)

Did the result resolve the plan's question?
├─ Yes, positively                                       → CLOSE: completed
├─ Yes, negatively after ruling out repairable causes    → CLOSE: terminal_kill
└─ No, blocked on external dependency                    → PARK

Was the plan superseded?                                 → CLOSE: replaced
```

## Approach transition criteria

Use these criteria when deciding whether to stay with the current approach, refine it, open an adjacent plan, park it, or close it.

Stay with the current approach when the result leaves the question, mechanism conjecture, method family, data assumption, and evaluation target intact. Routine planned execution is `NEXT_STEP`; a prospective narrowing inside the same approach is `REFINE`.

Pick `REFINE` when the same research question and same mechanism conjecture still organize the work, but the result identifies a repairable cause, narrower scope, missing control, parameter range, or measurement adjustment. The intervention remains in the same method family and the same data assumption and evaluation target still define what would count as evidence.

Pick `ADJACENT` when the next useful move requires an alternative approach: a different mechanism conjecture, a different method family, a changed data assumption, or a changed evaluation target. This includes cases where the current result creates information gain by showing that another method principle, data regime, or evaluation target must be studied as its own plan.

Pick `PARK` when the current approach or alternative approach cannot be evaluated until an external unblock condition is met. Waiting for data access, a dependency, a completed adjacent baseline, or a resource window is a pause contract, not evidence for or against the approach.

Pick `CLOSE` when the plan has answered its question, has been replaced, or has exhausted useful information gain after repairable cause checks have been ruled out. A negative close requires evidence that failure is not explained by a configuration error, data defect, wrong scope, missing dependency, broken comparator, or other repairable cause. If the failure is repairable, use `REFINE`; if the repair requires a different mechanism, method family, data assumption, or evaluation target, use `ADJACENT`.

The branches are mutually exclusive within a single decision. A result can prompt sequential decisions in subsequent sessions, but each decisions.md entry is one branch.

## State-change logging format

Sessions that change durable state (any branch except `NEXT_STEP`) must update `decisions.md` with:

```markdown
## YYYY-MM-DD HH:MM <plan_id> <BRANCH>
- From: <previous state — question, scope, status>
- To: <new state>
- Trigger: <what evidence prompted this>
- Evidence: <file:line / claim ID / run reference>
- Next: <what the next session does>
```

The `Next` line is required. A decision without a next action is incomplete — the point of logging is that the next session can pick up.

Sessions with no durable change need no entry. Smoke tests, environment setup, orientation, debugging a script that did not affect any claim — these are not durable changes.

## Anti-patterns

- **"Continue and observe."** Not a branch. If the plan continues unchanged, it is `NEXT_STEP`. If it changes, it is `REFINE` or `ADJACENT`.
- **Implicit pivots.** Quietly redefining the question without a `decisions.md` entry. Always log `REFINE` or `ADJACENT`. Hidden pivots break interoperability across sessions.
- **Goalpost shift dressed as REFINE.** Changing success criteria after seeing a result to make the result look favorable. `REFINE` applies prospectively — prior runs are exploratory evidence under the old plan unless explicitly re-evaluated under the refined plan.
- **Premature terminal_kill.** Calling it dead because two seeds failed without ruling out repairable causes. Use `REFINE` to control the confound first.
- **Parking without an unblock condition.** "PARK for now" is meaningless. Name the specific testable trigger that would prompt unpark.
- **CLOSE without final claim.** A `CLOSE` entry that says "we did this thing" but does not state the actual conclusion is not a close — it is an abandonment.
