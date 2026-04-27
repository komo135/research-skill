# severity_rubric.md

Severity tags, the verdict calculation, and the rules for parking findings.

## Severity tags

| Severity | Meaning | Effect on the headline claim |
|---|---|---|
| **high** | Conclusion-blocking. The claim cannot stand as written until this is resolved or the claim is rewritten to no longer depend on it. | Blocks the claim until resolved or parked. |
| **medium** | Claim-narrowing. The claim must shrink in scope or strength to match the actual evidence. The technical result may stand; the abstract sentence does not. | Blocks the claim if it is not narrowed accordingly. |
| **low** | Improvement. The work would be stronger with this addressed; the conclusion does not change without it. | Does not block. Logged. |

## The `blocks_supported` field — symmetric semantics

Each finding carries a `blocks_supported` boolean. Read it symmetrically:

- For an experiment whose **headline claim is `verdict = "supported"`**, `blocks_supported = yes`
  means the supported verdict cannot stand as written until the finding is resolved.
- For an experiment whose **headline claim is `verdict = "rejected"`**, `blocks_supported = yes`
  means the *rejection itself* is preliminary as written — typically because the
  rejection's denominator is wrong (e.g. some alphas not actually evaluated), the
  rejection's scope is mis-stated (e.g. tested on G10 only, claim leaks to "FX"), or
  the rejection was reached on a contaminated PnL.
- For experiments at any other verdict tier (`partial`, `preliminary`), `blocks_supported`
  reads as "would block a future promotion to supported / would force a further narrowing".

**For rejection notebooks, the common trap is to mark all findings `blocks_supported: no`
because no supported verdict is on the table.** That collapses the field's discriminating
value and reads as "the rejection is final" — which is itself a claim about the rejection's
strength. If a finding implies the rejection statement bears more weight than the evidence
allows, mark `blocks_supported: yes`.

`blocks_supported` overrides the default severity mapping above when explicitly set by
the reviewer. Use this when a `medium` finding is, in this specific case, actually
load-bearing for the headline claim (e.g. a missing 2D surface for a strategy whose
*entire* claim is parameter robustness).

## Verdict calculation

Count findings by severity across all dimensions. Apply the rules in order; the first
matching rule wins.

| Verdict | Conditions | Position |
|---|---|---|
| **ready** | 0 high · ≤ 2 medium · any low | Strong enough for internal team review or external sharing. The claim as written is supported by the evidence presented. Equivalent to ≥ 80 % on the quant-research `research_quality_checklist.md`. |
| **partial** | 0 high · 3–6 medium · any low | The technical result is real, but the abstract claim must be narrowed. The author rewrites the abstract to match the demonstrated scope, then re-runs the review. |
| **partial** | 1 high · ≤ 3 medium · any low | A single high-severity gap. Either fix it, or rewrite the claim so it no longer depends on the gap, then re-run. |
| **preliminary** | 2+ high, OR 7+ medium | Preliminary screening, not a result. Multiple cycles of work are required before the headline claim can stand. |
| **not-yet-research** | The notebook fails the trigger eligibility — no claim, no thresholds, no comparison | This skill is not the right tool. Return the user to `quant-research`'s research-design step. |

The verdict is computed mechanically from the finding counts. Do not soften the verdict
because the work "feels" close to the next tier — feelings of closeness are exactly the
bias this skill is designed to neutralize.

### Reading the verdict for rejection notebooks

The verdict tiers above describe how warranted the *headline claim* is, regardless of
whether that claim is supported, rejected, parked, or otherwise. For a notebook whose
headline is `verdict = "rejected"`:

- **`ready`**: the rejection is well-supported and the rejection statement matches the
  evidence's scope. Future cycles may overturn the rejection with new evidence; this
  cycle's rejection stands.
- **`partial`**: the rejection is real but the rejection statement reaches further than
  the evidence allows (e.g. tested on G10 only but the rejection claim implicitly covers
  "FX"). Narrow the rejection's scope, then re-run.
- **`preliminary`**: the rejection cannot stand as written. Common causes for rejection
  notebooks include: (a) the denominator is wrong because some pre-registered alphas
  were not actually evaluated, (b) the PnL the rejection was computed on was buggy or
  contaminated, (c) the rejection's mechanism-level scope (universe × frequency × cost
  model) was not the one the headline names, (d) baselines that would give the rejection
  comparative force are missing. The rejection may well end up confirmed once these are
  closed, but until then "rejected" is a stronger claim than the evidence makes.
- **`not-yet-research`**: there is no claim worth rejecting — the work is at orientation
  stage, return to `quant-research`.

A `preliminary` verdict on a rejection notebook is *not* a vote of confidence in the
hypothesis. It is a vote of insufficient confidence in the *rejection*. Most often the
right next step is the smallest set of changes that promotes the rejection from
`preliminary` to `partial` (typically: fix the denominator, add the missing baseline,
fix the embargo) rather than relitigating whether the hypothesis is true.

## Parking findings

A finding can be *parked* instead of fixed if and only if the author records, in
`decisions.md`:

1. Which finding is being parked (severity, dimension, what)
2. Why the fix is deferred (e.g. "multi-asset extension is the next cycle")
3. What the *narrowed* claim is, in the abstract, so the unfixed gap is acknowledged in
   the conclusion rather than ignored

A parked `high` finding does not unblock `verdict = "supported"`. A parked `high`
finding only allows the verdict to be set when the abstract has been rewritten to a
claim that no longer depends on the parked finding. Practical example: a SPY-only
universe with a `high` finding under `scope` cannot be parked while keeping a "US
equities" abstract; the abstract is rewritten to "SPY 2015–2024" and the parked finding
becomes the explicit "Cannot conclude: not tested on other instruments" entry.

Parked `medium` and `low` findings are recorded and the verdict still stands as
computed.

## Severity decisions in edge cases

### "The check passes in spirit but fails the letter"

A check that passes the *spirit* but fails the *letter* (e.g. "5 papers required, you
have 4 but they're high-quality") is `medium`, not `high`. Record the finding so future
cycles add the missing depth, but do not block the verdict on a hair-trigger letter
violation.

A check that passes the *letter* but fails the *spirit* (e.g. "5 papers, but all 5 are
blog posts unrelated to the research question") is `high`. The point of the check is
the spirit; the letter is just an enforcement handle.

### "The user explicitly opted out"

A user saying "skip the literature review for this internal cycle" makes it a `low`
finding logged for record, *if* the work is internal-only and not heading toward a
`supported` verdict on a portfolio-affecting claim. If it is heading there, the opt-out
is not honored — the literature review is a gate at that level.

### "The fix is large and the cycle is small"

This is the textbook case for a parked `medium` finding with a narrowed claim. The
review's job is not to demand every cycle be the last cycle. It is to ensure the claim
in the abstract matches the evidence in the cycle.

## What the verdict is not

- It is not a quality score on the *researcher*. It is a calibration of the *claim*
  against the *evidence*.
- It is not a deployment recommendation. A `ready` verdict says the work is
  internally consistent and well-positioned; deployment requires additional
  considerations (capital availability, capacity, ongoing monitoring) that are out of
  scope here.
- It is not stable across cycles. A `ready` verdict for cycle N can become `partial`
  in cycle N+1 if new evidence narrows the previously-supported claim.

## Anti-rationalizations

| "I want to soften this" | Don't |
|---|---|
| "It's just one missing baseline, not a big deal" | A missing upper-bound baseline is the modal cause of unwarranted ML claims. `high` stands. |
| "The DSR is 0.94 not 0.95, basically the same" | The threshold exists because the deflated-Sharpe distribution at 0.94 vs 0.95 corresponds to a meaningful shift in implied false-discovery rate. `high` stands. |
| "The user has done this kind of work before, they know what they're doing" | Authors are systematically blind to their own missing baselines. `high` stands. |
| "The numbers are good, surely something must be sound" | Good numbers on a wrong claim are exactly this skill's failure mode to prevent. `high` stands. |
