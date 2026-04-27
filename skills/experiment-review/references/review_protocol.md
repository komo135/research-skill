# review_protocol.md

Dispatch and aggregation mechanics for the experiment-review skill.

## Inputs the assistant must gather before dispatch

Before dispatching the eight reviewers, collect the following into a context bundle. The
seven specialist reviewers will each receive the same full bundle plus their dimension
scope. The eighth (adversarial cold-eye) reviewer will receive a *different* (minimum)
bundle — see the dedicated section below.

| Item | Purpose |
|---|---|
| Notebook path under review | The primary artifact |
| Project root path | To find `hypotheses.md`, `decisions.md`, `literature/`, `experiments/INDEX.md` |
| Design-cell content (extracted) | The pre-registered question, hypothesis, thresholds |
| Abstract-cell content (extracted) | The claim being evaluated |
| Conclusion / "Cannot conclude" section content (extracted) | Generality claims to triangulate |
| Cycle history (`experiments/INDEX.md` summary) | For `question` reviewer's cycle-honesty checks |
| Upstream feature-experiment paths, if any | For `method` reviewer's feature-hygiene checks |
| Bug-review entry from `decisions.md`, if present | So `validation` reviewer knows whether the prerequisite has been satisfied |

If any of these is missing, do not abort. Proceed and let the relevant dimension flag
"missing artifact" as a `high`-severity finding. Graceful degradation is required —
abort only if the notebook itself is missing or unreadable.

## Dispatch

The eight reviewers — seven specialists (question / scope / method / validation / claim /
literature / narrative) plus one adversarial cold-eye reviewer — are dispatched in a
single tool-call batch (all in one assistant turn). Parallelism is required, not
optional. Sequential dispatch is the single-agent-fallback pathway, not the standard
pathway.

The `narrative` reviewer needs the full notebook `.py` file plus the `quant-research`
skill's `references/notebook_narrative.md` and `references/marimo_cell_granularity.md`
(canonical specs). The other six specialists do not need those files; conversely,
`narrative` does not need `hypotheses.md` / `decisions.md` / `literature/` artifacts.
Tailor each specialist's input bundle accordingly to keep the brief tight.

The eighth (adversarial cold-eye) reviewer is structurally different — see the
dedicated section "Adversarial reviewer dispatch" below. Its bundle is intentionally
*minimum*: the `.py` file alone, with no other inputs. The asymmetry is the mechanism
that makes the layer add value over a single-bundle eighth specialist would.

Each reviewer's prompt has this structure:

```
You are a specialist reviewer in the experiment-review skill. Your dimension is
[dimension name].

Read these inputs:
- Notebook: <path>
- Project root: <path>
- Context bundle: <inline summary>
- Your scope and checklist: skills/experiment-review/references/review_dimensions.md
  (read only the section for [dimension name])
- Severity rubric: skills/experiment-review/references/severity_rubric.md

Apply the checklist for your dimension. For each check, decide pass / partial /
fail with concrete evidence. Return findings *only* — do not modify any file.

Specific items to chase (the parent assistant has already read the artifacts and
is pointing at concrete evidence — these are not exhaustive, just where to start):
- <specific item 1, with line / section pointer>
- <specific item 2>
- ...

Output schema (one entry per finding):
- severity: high | medium | low
  dimension: [your dimension name]
  where:    <notebook>:<cell-or-section>  (or "project-level")
  what:     <one-sentence statement>
  why:      <which check failed and what the evidence is>
  fix:      <concrete remediation or follow-up question>
  blocks_supported: yes | no  (read symmetrically for rejection notebooks —
                              see severity_rubric.md)

Do NOT deliver a narrative review — only the structured findings list. The
aggregation step turns those into the report.

Stay in your dimension. If you notice something in another dimension's scope, do
not address it; the relevant specialist will catch it. Crossing lanes weakens the
specialist effect.
```

### The "Specific items to chase" pattern

Including 3-7 dimension-specific chase items in each reviewer's prompt is *required*
when the parent assistant has already read the notebook and the project artifacts.
Without these pointers, reviewers consistently drift toward generic checklist
walkthroughs and miss notebook-specific evidence (the modal failure mode in baseline
testing). With the pointers, reviewers go directly to the load-bearing evidence and
return sharper findings.

The chase items are **observations, not conclusions** — phrase them as "X is the case;
apply check Y" rather than "X is wrong because Y". The reviewer decides severity and
formulates the finding. The parent assistant only points.

Example (for the validation reviewer, pointing at an embargo issue spotted in pre-read):

> "Check IS_END = 2022-12-31 23:55 UTC vs OOS_START = 2023-01-01 00:00 UTC; with
> fwd_ret horizon = 1 bar, is the embargo size adequate? Apply check 1."

Compare to the unhelpful version:

> "There is an embargo bug, find it."

The first prompts a finding; the second prompts a search.

## Adversarial reviewer dispatch

The eighth reviewer (adversarial cold-eye) is dispatched in the same batch as the
seven specialists, but with a *different* bundle and a *different* prompt.

**Bundle** (minimum, intentionally):

- The `.py` file under review (its full text)

**NOT in the bundle (deliberately withheld)**:

- The seven specialist reviewers' findings
- `literature/papers.md`, `literature/differentiation.md`
- `hypotheses.md`, `decisions.md`, `experiments/INDEX.md`
- Upstream feature notebook `.py` files (even if the design cell names them)
- Chat context, prior-cycle discussion, the parent assistant's scratchpad

**Prompt skeleton** (use the verbatim instruction in `review_dimensions.md` section 8):

```
You are a cold-eye external reviewer. The .py file you are about to read is the
only material you are given. Other materials are intentionally withheld — the goal
is to keep you from anchoring on priors that the same model shares with the author
or with other reviewers.

Read this notebook:
- Notebook: <path>
- Your scope and the two attack axes: skills/experiment-review/references/review_dimensions.md
  (read the section "8. adversarial — cold-eye standalone reading" only)
- Severity rubric: skills/experiment-review/references/severity_rubric.md

Output schema (one entry per finding):
- severity: high | medium | low
  dimension: adversarial
  where:    <notebook>:<cell-or-section>
  what:     <one-sentence statement>
  why:      <which axis (claim-warrant or standalone-readability) and what the evidence is>
  fix:      <concrete remediation or follow-up question>
  blocks_supported: yes | no
```

**Do NOT pass the adversarial reviewer the "Specific items to chase" pattern used
for specialists.** That pattern injects parent-assistant priors, which is exactly
the anchoring this reviewer is supposed to be free of. Let it find what it finds.

## Aggregation

After all eight reviewers return, the assistant produces a single review report at
`notebooks/<project>/reviews/exp_NNN_<ISO-date>.md` using the template in
`assets/review_report.md.template`. The aggregation steps:

1. Concatenate all findings, preserving severity and dimension tags.
2. Sort: `high` first, then `medium`, then `low`. Within each tier, group by
   dimension in the order question / scope / method / validation / claim / literature /
   narrative / adversarial.
3. Compute the overall verdict per `severity_rubric.md`.
4. Write the report.
5. **Optionally** append a one-line entry to the project's `decisions.md` linking the
   review report. This is **opt-in**, not automatic — appending modifies the user's
   research log and should only happen when the user has either explicitly authorized
   it or invoked this skill from inside a quant-research workflow that already writes
   to `decisions.md`. When in doubt, ask. If appending, the entry is:

   ```
   ### Experiment review for exp_NNN at <ISO timestamp>
   See notebooks/<project>/reviews/exp_NNN_<ISO-date>.md. Verdict: <verdict>.
   high: <count>, medium: <count>, low: <count>.
   ```

   The review report itself (in `reviews/`) is the canonical audit trail; the
   `decisions.md` line is a navigation breadcrumb, not the record.

## Single-agent fallback

When parallel dispatch is unavailable:

1. Run the eight dimensions sequentially in eight distinct passes.
2. Between passes, re-read the notebook from scratch — do not rely on stale notes from
   the previous pass. The point of fresh re-reads is to recover the narrowness benefit
   that parallel sub-agents get for free.
3. Treat each pass's output as if it came from a different reviewer. Do not let
   findings from one pass bias the next pass's check application.
4. The adversarial pass is run with the minimum bundle only — bundle asymmetry is
   preserved in fallback as well as in parallel. Do not give the adversarial pass
   access to earlier passes' findings; that collapses the asymmetry.
5. Aggregate the same way.

The fallback is genuinely worse than parallel dispatch — but eight focused sequential
passes are still substantially better than one mixed-scope pass. The failure mode is
collapsing the dimensions into "I read the notebook and here's what I think," which
is exactly the baseline this skill is designed to upgrade.

## When findings disagree

Two reviewers can produce overlapping or contradictory findings — for example, `scope`
and `claim` may both flag the SPY-only / "US equities" mismatch from different angles.
Both findings stay in the report; the aggregation does not deduplicate. Two reviewers
flagging the same gap from independent vantage points is *evidence*, not redundancy.

If two findings genuinely contradict (one says "this is sufficient," another says "this
is not"), log both verbatim and resolve by reading the underlying code or by raising as
a follow-up question to the user. Do not silently pick one.

## Output location and retention

`notebooks/<project>/reviews/` is part of the project — the review is itself a
research artifact. Reviews are committed alongside experiments. A history of reviews
across cycles becomes part of the project's audit trail and lets a later researcher see
how the conclusions evolved.

If `notebooks/<project>/reviews/` does not exist, create it.

## What the assistant does *not* do

- Do not modify the notebook under review during the review pass. Reviews recommend; the
  author decides.
- Do not run code from the notebook. Reviews are based on reading the artifacts, not on
  re-execution. Re-execution belongs in `bug_review`.
- Do not call this skill recursively on its own report. The review is the leaf.

## Trigger discipline

A "review" that delivers a narrative without:
- eight dimensions explicitly addressed (seven specialists + one adversarial),
- severity tags on every finding,
- an archived report at `notebooks/<project>/reviews/`,
- the adversarial reviewer running with the minimum bundle (not the full bundle),

…has not actually run this skill. Whatever it is, call it something else, do not
declare a review verdict, and do not let it block or unblock a `verdict = "supported"`.
