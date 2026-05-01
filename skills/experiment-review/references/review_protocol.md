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
| Project root path | To find `hypotheses.md`, `decisions.md`, `literature/`, `purposes/INDEX.md` |
| Design-cell content (extracted) | The pre-registered question, hypothesis, thresholds |
| Abstract-cell content (extracted) | The claim being evaluated |
| Conclusion / "Cannot conclude" section content (extracted) | Generality claims to triangulate |
| Cycle history (`purposes/INDEX.md` summary) | For `question` reviewer's cycle-honesty checks |
| Upstream feature-experiment paths, if any | For `method` reviewer's feature-hygiene checks |
| Bug-review entry from `decisions.md`, if present | So `validation` reviewer knows whether the prerequisite has been satisfied |

If any of these is missing, do not abort. Proceed and let the relevant dimension flag
"missing artifact" as a `high`-severity finding. Graceful degradation is required —
abort only if the notebook itself is missing or unreadable.

## Per-dimension input contract (efficiency-class, F21)

Each reviewer receives **only its own dimension scope** plus the shared
artifacts named below. Whole-file `review_dimensions.md` (489 lines) is
NOT delivered to specialists — that was the prior "whole file + read §i
only" pattern, which billed dead weight (~77-92 % of the file per
specialist) and diluted attention. Pre-extract the dimension scope by
**section anchor** (the `## N. <dimension-name>` heading) before
dispatch. Anchor missing → reviewer flags
`severity: high, dimension: <name>, what: missing input section §<N>`
per the graceful-degradation pattern; do not abort dispatch.

| # | Dimension | Required scope (extract) | Required shared | NOT-receive |
|---|---|---|---|---|
| 1 | question | `review_dimensions.md` §1 (anchor `## 1. question`, ~39 lines) | `severity_rubric.md`, notebook .py, design-cell extract, `hypotheses.md`, `decisions.md`, `purposes/INDEX.md` | `review_dimensions.md` outside §1, `literature/`, `notebook_narrative.md`, `marimo_cell_granularity.md`, `bug_review.md` |
| 2 | scope | `review_dimensions.md` §2 (anchor `## 2. scope`, ~63 lines) | `severity_rubric.md`, notebook .py, `hypotheses.md`, `decisions.md` | `review_dimensions.md` outside §2, `literature/`, narrative refs, `bug_review.md` |
| 3 | method | `review_dimensions.md` §3 (anchor `## 3. method`, ~40 lines) | `severity_rubric.md`, notebook .py, design-cell extract, upstream feature notebook .py if named in design cell | `review_dimensions.md` outside §3, `literature/`, narrative refs, `hypotheses.md` / `decisions.md`, `bug_review.md` |
| 4 | validation (sufficiency) | `review_dimensions.md` §4 (anchor `## 4. validation`, ~37 lines) | `severity_rubric.md`, notebook .py, design-cell extract, bug-review entry from `decisions.md` if present | `review_dimensions.md` outside §4, `literature/`, narrative refs, `hypotheses.md`, `bug_review.md` whole |
| 5 | claim | `review_dimensions.md` §5 (anchor `## 5. claim`, ~38 lines) | `severity_rubric.md`, notebook .py, abstract-cell extract, conclusion / "Cannot conclude" extract | `review_dimensions.md` outside §5, `literature/`, narrative refs, `hypotheses.md` / `decisions.md`, `bug_review.md` |
| 6 | literature | `review_dimensions.md` §6 (anchor `## 6. literature`, ~66 lines) | `severity_rubric.md`, notebook .py, `literature/papers.md`, `literature/differentiation.md` | `review_dimensions.md` outside §6, narrative refs, `hypotheses.md` / `decisions.md`, `bug_review.md` |
| 7 | narrative | `review_dimensions.md` §7 (anchor `## 7. narrative`, ~75 lines), `quant-research/references/notebook_narrative.md` whole, `quant-research/references/marimo_cell_granularity.md` whole | `severity_rubric.md`, notebook .py | `review_dimensions.md` outside §7, `hypotheses.md` / `decisions.md`, `literature/`, `bug_review.md` |
| 8 | adversarial (cold-eye) | `review_dimensions.md` §8 (anchor `## 8. adversarial`, ~112 lines) — verbatim instruction only | notebook .py, `severity_rubric.md` (for output schema; not bias-inducing) | `review_dimensions.md` outside §8, `hypotheses.md` / `decisions.md` / `purposes/INDEX.md`, `literature/papers.md` / `literature/differentiation.md`, `notebook_narrative.md` / `marimo_cell_granularity.md`, the seven specialists' findings, upstream feature notebook .py (even if named in design cell), chat context — full minimum-bundle NOT-input list per §8 in `review_dimensions.md` |

**Section anchor as source of truth** — extraction reads the section by
its `## N. <dimension>` heading anchor, not by line range. The
approximate line counts above are reader hints; line ranges shift when
other sections are edited, but anchors don't. A renamed or removed
anchor surfaces a `severity: high, dimension: <name>, what: missing
input section §<N>` finding from the affected reviewer (graceful
degradation), which is the correct signal for an out-of-sync contract —
silent recovery would mask a real protocol drift.

**Adversary rule**: pre-extraction applies to the adversary as well —
adversary receives §8 only (= 112 lines vs 489). The asymmetry is preserved:
**no §1-§7 specialist scope reaches the adversary**, exactly per the
existing minimum-bundle list. Pre-extraction tightens, not weakens, the
asymmetry.

The contract is **structured**, not prose advice. Tailoring is no longer
the parent assistant's discretion; it is a mechanical pre-dispatch
extraction step (see "Dispatch" below).

## Trigger-conditional dispatch on re-verify (efficiency-class, F22)

A typical H verdict='supported' attempt enters the gate multiple times:
once on initial pass, then again on each re-verify after fix
reconciliation. The naive contract — "fire all 8 every time" — re-pays
for unchanged surfaces. F22 splits the dispatch into two cases.

### Initial pass

First time this H enters the gate (= no prior clean review on this H in
the current session). **All 8 reviewers fire** as the full gate — the
input contract above is what each reviewer receives.

### Re-verify pass

Triggered after the parent has applied fixes from a prior experiment-review
inline summary and completed `quant-research/references/post_review_reconciliation.md`'s
Definition of Done for those fixes. The parent identifies **which surface
map entries the fixes touched** and fires only the dimensions whose
surface intersects.

**Adversary auto-fires on re-verify whenever any specialist re-fires** —
its standalone-readability + claim-warrant check is on the *current*
artifact and any change can affect either axis. If no specialist fires
(= no surface change at all), nothing is being re-verified and the prior
clean state stands.

### Surface map per reviewer

Each reviewer's surface = the union of cell categories / file types
whose change re-fires the dimension.

| # | Dimension | Surface (re-fire if any of these changed since last clean review) |
|---|---|---|
| 1 | question | H falsifiable statement, design cell, acceptance / rejection thresholds, cycle-hygiene markers (= prior cycle log changes affecting selection bias) |
| 2 | scope | universe declaration, period range, instrument list, regime declaration, cross-section size |
| 3 | method | model selection cell, baseline cells (especially the hand-crafted upper-bound), feature list, hyperparameter grid, retraining-cadence declaration |
| 4 | validation (sufficiency) | walk-forward window count, statistical-power claims, embargo-adequacy claims, CPCV setup statements |
| 5 | claim | abstract cell, verdict cell, conclusion / "Cannot conclude" cell, deployment-readiness language |
| 6 | literature | `literature/papers.md`, `literature/differentiation.md`, novelty / differentiation-tier claims in the notebook |
| 7 | narrative | any markdown cell in the notebook body, figure plan, per-figure observation cells, prose interpretation cells, helper-function docstrings |
| 8 | adversarial (cold-eye) | auto-fires whenever any specialist re-fires (= any change to the artifact); does not have its own surface map because its scope is the entire `.py` standalone |

### When in doubt, fire

Surface classification is the parent assistant's reasoning step. If a
fix doesn't fit any surface entry cleanly — or fits multiple ambiguously
— **default to firing the affected dimensions plus adversary**. The
gate's job is not to skip work but to skip *redundant* work; ambiguity
is not a redundancy signal.

### Cross-session boundary

The "last clean review" baseline is **session-local**. A researcher
returning to the same H next session has no in-context record of which
dimensions were verified clean — the new dispatch is an Initial pass.
Trigger-conditional savings come from the in-session iteration loop
(initial → fix → re-verify → fix → re-verify), which is the modal cost
profile.

If the user explicitly attests in a prior `decisions.md` entry that
"dimensions {X, Y, Z} were verified clean against state S" and the
agent can verify the artifact's relevant surfaces are unchanged from S,
the agent may treat the next dispatch as a re-verify. Without that
attestation, treat as Initial.

## Dispatch

The eight reviewers — seven specialists (question / scope / method / validation / claim /
literature / narrative) plus one adversarial cold-eye reviewer — are dispatched in a
single tool-call batch (all in one assistant turn). Parallelism is required, not
optional. Sequential dispatch is the single-agent-fallback pathway, not the standard
pathway.

The eighth (adversarial cold-eye) reviewer is structurally different — see the
dedicated section "Adversarial reviewer dispatch" below. Its bundle is intentionally
*minimum*: the `.py` file alone plus its own §8 instruction extract, with no other
inputs. The asymmetry is the mechanism that makes the layer add value over a
single-bundle eighth specialist would.

Each reviewer's prompt has this structure:

```
You are a specialist reviewer in the experiment-review skill. Your dimension is
[dimension name].

Notebook under review (verbatim):
<verbatim notebook .py file body>

Severity rubric (verbatim):
<verbatim contents of severity_rubric.md>

Your scope and checklist (extracted from review_dimensions.md §[N], inline —
the rest of review_dimensions.md is NOT delivered):
<verbatim contents of review_dimensions.md §[N], extracted by section anchor
"## [N]. [dimension name]" before dispatch>

Required shared artifacts for your dimension (per input contract, inline):
<e.g. abstract-cell extract, hypotheses.md content, literature/papers.md, ...>

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

**Bundle** (minimum, intentionally — the source-of-truth is row 8 of the
"Per-dimension input contract" table above; this section restates the
shape for the dispatch step but does not duplicate the full NOT-input
list. If the contract row and this section diverge, the contract row
wins; update both):

- The `.py` file under review (its full text)
- `severity_rubric.md` (for the output schema's severity tagging — it
  does not bias the adversary's reading)
- `review_dimensions.md` §8 only (the verbatim adversary instruction +
  attack axes), pre-extracted by section anchor

NOT in the bundle: see contract row 8 above for the full list. The most
load-bearing exclusions are the seven specialist reviewers' findings,
all `literature/` artifacts, all `hypotheses.md` / `decisions.md` /
`purposes/INDEX.md` / upstream feature notebooks (even if named in
the design cell), and any chat / prior-cycle context.

**Prompt skeleton**:

```
You are a cold-eye external reviewer. The .py file you are about to read is the
only material you are given. Other materials are intentionally withheld — the goal
is to keep you from anchoring on priors that the same model shares with the author
or with other reviewers.

Notebook under review (verbatim):
<verbatim notebook .py file body>

Severity rubric (verbatim):
<verbatim contents of severity_rubric.md>

Your scope and the two attack axes (extracted from review_dimensions.md §8,
inline — the rest of review_dimensions.md is NOT delivered):
<verbatim contents of review_dimensions.md §8, extracted by section anchor
"## 8. adversarial — cold-eye standalone reading">

NOT delivered to you (deliberately withheld — see the NOT-input list in §8 above):
- The seven specialist reviewers' findings
- literature/papers.md, literature/differentiation.md
- hypotheses.md, decisions.md, purposes/INDEX.md
- Upstream feature notebook .py files (even if the design cell names them)
- Chat context, prior-cycle discussion, the parent assistant's scratchpad

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

After all eight reviewers return, the assistant aggregates the findings into a
single structured review **delivered inline in the assistant's reply**. The
skill does not write a review report file to disk and does not append to
`decisions.md`. The aggregation steps:

1. Concatenate all findings, preserving severity and dimension tags.
2. Sort: `high` first, then `medium`, then `low`. Within each tier, group by
   dimension in the order question / scope / method / validation / claim / literature /
   narrative / adversarial.
3. Compute the overall verdict per `severity_rubric.md`.
4. Return the aggregated review in the assistant's reply, with a clearly
   visible verdict line, finding counts (high / medium / low), and the
   per-finding entries grouped as above. The minimum reply must contain:
   verdict, counts, and every individual finding's full schema entry.
5. The skill does not modify any project file. If the user wants a durable
   record they can copy the inline review into `decisions.md` themselves.

### Anti-rationalizations (efficiency-class, F21 / F22)

| Excuse | Why it is wrong |
|---|---|
| "Whole-file `review_dimensions.md` is safer — what if the reviewer needs context outside §i?" | Cross-dimensional findings are caught by the *parallel ensemble*, not by each reviewer reading every section. The seven specialists in parallel are designed to overlap defensively at the dimension *level* (e.g. `claim` and `scope` independently catch the SPY-only-to-US-equities leap), not by sharing prose. The whole-file pattern bills 77-92 % dead weight per specialist and dilutes attention via lost-in-middle. |
| "The adversary should also receive `review_dimensions.md` §1-§7, in case there's overlapping context it would benefit from." | The asymmetry IS the mechanism. Giving adversary access to specialist scope (§1-§7) makes it an eighth specialist with the same priors, not a cold-eye reader. CCR (arxiv 2603.12123) showed the gain comes from minimum-context, not richer-context. The adversary receives §8 only — its instruction and attack axes — and nothing else from `review_dimensions.md`. |
| "Pre-extraction is brittle — what if the section anchor is renamed?" | Rename a `## N. <dimension>` heading and the dispatch surfaces a graceful-degradation finding (`severity: high, dimension: <name>, what: missing input section §<N>`). The skill does not silently swallow the rename. The brittleness is *desirable*: a renamed anchor without contract-side update is an actual bug, and the gate catches it. |
| "User asked for 'a comprehensive review', so safer to send whole files." | The contract names what each reviewer needs to do its dimension's job. "Comprehensive" comes from running all eight dimensions in parallel, not from each reviewer reading every reference whole. If a section outside §i is genuinely needed for a dimension, edit the contract, do not bypass it case-by-case. |
| "The narrative reviewer needs `notebook_narrative.md` and `marimo_cell_granularity.md` whole — they're already specialized to it, so no extraction needed." | True for those two refs (the entirety is `narrative` scope). `review_dimensions.md` §7, however, is one section out of eight in `review_dimensions.md` — pre-extract that one. The two `quant-research` references stay whole because they have no irrelevant sub-sections relative to the `narrative` dimension. |
| "The fix is small / cosmetic, just re-fire all 8 to be safe." (F22) | Re-firing all 8 on a fix that touched a single surface is the dead-weight pattern F22 exists to interrupt. The surface map determines re-fire — *any* fix lands on at least one surface, so the firing set is non-empty; cosmetic changes that genuinely touch nothing (e.g. an observation cell rephrasing) re-fire only narrative + adversary, not the full 8. "Just to be safe" is the exact rationalization the surface map replaces. |
| "I'm unsure which surface this fix touches, default to skipping the dispatch." (F22) | Default is *fire*, not skip. Surface ambiguity → fire the candidates plus adversary. The gate skips only when the parent can confidently classify the fix as not-touching a dimension's surface. Skipping under ambiguity is the failure mode; firing under ambiguity is the safety. |
| "Cross-session: I remember the prior verdict was clean, treat next dispatch as re-verify." (F22) | Without an attestation in `decisions.md` naming which dimensions were verified clean against which artifact state, cross-session is Initial. In-context memory of "I think it was clean" is anchoring on a prior session, not evidence the current artifact's surfaces match the prior clean state. |
| "The fix changed only the abstract wording; that's narrative + claim, but the underlying numbers are unchanged so I can skip both." (F22) | If the fix changes the abstract, the *claim* changes — `claim` reviewer must re-verify the new wording is supported by the (unchanged) evidence; `narrative` must re-verify the new wording satisfies its spec. Re-fire both + adversary. Wording-only changes are real surface changes for these dimensions. |

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
5. F21 (input contract pre-extraction) and F22 (trigger-conditional dispatch on
   re-verify) **both still apply in fallback**. Each sequential pass receives only
   its dimension scope (not whole-file `review_dimensions.md`); on a re-verify
   sequential run, only dimensions whose surface intersects the fixes execute.
6. Aggregate the same way.

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

The review is delivered **inline in the assistant's reply**. The skill does not
create a `reviews/` folder, does not write any file, and does not modify
`decisions.md`. If the user wants a durable record across cycles they can
manually copy the inline review into the project — the skill itself stays
read-only against the project tree.

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
- a clearly visible verdict line and finding counts in the reply,
- the adversarial reviewer running with the minimum bundle (not the full bundle),

…has not actually run this skill. Whatever it is, call it something else, do not
declare a review verdict, and do not let it block or unblock a `verdict = "supported"`.
