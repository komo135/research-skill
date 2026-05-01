# review_dimensions.md

Per-dimension specifications for the seven specialist reviewers. Each reviewer reads its
own section here and applies the checks listed; nothing else.

## How to read this file

Each dimension lists:

- **Scope**. One paragraph stating what the reviewer is responsible for and what is
  *out of scope* (which prevents reviewers from drifting into each other's lanes).
- **Inputs**. Files the reviewer should pull in before forming a judgment.
- **Checks**. The specific items to verify, each with a typical failure mode and the
  severity it warrants by default.
- **Effect-size sanity** (where relevant). Numeric guard rails to compare the
  experiment's reported metrics against the published frontier.

---

## 1. question — falsifiability, pre-registration, cycle hygiene

### Scope

Whether the question being asked is testable, whether the thresholds for
acceptance / rejection were genuinely fixed before the result was seen, and whether the
hypothesis-portfolio history shows honest cycles or post-hoc curation. Does NOT cover
universe / regime (that is `scope`) or method choice (that is `method`).

### Inputs

- The notebook's *Research design* cell
- `hypotheses.md` and its git history (was the hypothesis edited after results came in?)
- `decisions.md` (does the time-ordering of decisions corroborate pre-registration?)
- `purposes/INDEX.md` (the cycle history)

### Checks

| Check | Failure mode | Default severity |
|---|---|---|
| Question is a falsifiable comparison statement | "Does X work?" rather than "Does X beat baseline B by metric M with threshold T?" | high |
| Acceptance condition is a numeric threshold present in the design cell | "supported if Sharpe > X" not "supported if it looks good" | high |
| Threshold pre-registration corroborated by `hypotheses.md` git history | Threshold was added or changed *after* results were observed | high |
| `hypotheses.md` and `decisions.md` are git-tracked and committed | Untracked files cannot corroborate pre-registration; a self-asserted date with no commit hash is not an audit trail | high |
| Hypothesis was not silently rewritten to match the result | The hypothesis in the abstract differs in direction or strength from the original `hypotheses.md` entry | high |
| Cycle count is ≥ 3 (minimum) or ≥ 5 (standard) | Single-shot experiment carrying the weight of the claim | medium |
| Across cycles, the *best* result is not being cherry-picked into the abstract | pur_002 → pur_003 → pur_004 with monotonically improving Sharpe and only the best one declared `supported` is selection bias | medium |
| Derived hypotheses from prior cycles were classified run-now / next-session / drop, not silently dropped | Untriaged candidate hypotheses sitting in `hypotheses.md` | low |
| The "we did N hyperparameter trials and 1 of them passed" pattern is acknowledged in DSR trial counting | DSR computed with trial count = 1 | high (but `validation` reviewer owns the DSR computation itself; `question` only flags the trial-count *honesty*) |

### Notes

A monotonically improving sequence of cycle Sharpes is *evidence of selection*, not
*evidence of method working*. The reviewer must explicitly check that the trial count
fed into DSR includes every cycle and every hyperparameter combination tried, and must
flag if it does not.

---

## 2. scope — universe, period, regime, generalization range

### Scope

Whether the experiment's empirical scope is large enough that the conclusion in the
abstract is supportable. Single-instrument experiments concluding about an asset class
are the modal failure here. Does NOT cover validation discipline (that is `validation`)
or claim wording (that is `claim`).

### Inputs

- The *Research design* cell (universe, period)
- The orientation figure cell (what the data actually looks like)
- The conclusion cell ("we conclude that X about Y")

### Checks

| Check | Failure mode | Default severity |
|---|---|---|
| Universe has ≥ 3 instruments OR a defined cross-section | SPY-only experiment concluding about "equity index returns" | high |
| Universe diversity covers the claim's stated scope | "US equities" claim tested only on 14 large-cap tech | high |
| Period covers ≥ 2 distinct regime types relevant to the hypothesis | Bull-only window for a hypothesis that should also work in vol spikes | medium |
| Period length supports the metric variance | 2 years of daily bars to estimate a monthly-rebalance Sharpe | medium |
| The "Cannot conclude" section names which dimensions of generality were not tested | Notebook claims generality without listing the untested dimensions | high |
| Multi-instrument: per-instrument metrics are reported, not just pooled | Sharpe 1.5 pooled but driven by 1 of 14 names | medium |
| Cross-asset claims tested on multiple asset classes | "VIX-term-structure works for equities" tested only on SPY → no information about QQQ, futures, sector ETFs | high |
| The instruments chosen are representative of the claim, not the most favorable | Universe = "the 14 names that worked"; non-empty universe-selection bias | high |

### Effect-size sanity

- For 1-day-horizon equity prediction on liquid US ETFs, hit rate above 56 % across a
  decade is at the high end of the published literature; flag for additional scrutiny
  rather than rejection.
- For stat-arb on US equities at 1 bp costs, net Sharpe ≥ 3 is in the "you have a bug or
  a leak" range vs. the published frontier (Avellaneda-Lee net Sharpe ~1.0–1.5 on
  broader, less correlated universes).
- For equity-factor research on monthly rebalance, IC > 0.10 deserves a flag.

These are guard rails, not verdicts. A pass on effect-size sanity does not vouch for the
result; a fail flags the result for the bug-review layer (the `quant-research` skill's
`bug_review.md`) before this skill's review can be considered conclusive.

### Frontier-uncovered cells

When the experiment operates in a frequency × asset-class combination for which there
is no published frontier (e.g. intraday cross-sectional FX, microsecond crypto, daily
emerging-market sovereign bonds), the absence is itself a finding under `literature`,
and effect-size sanity here cannot anchor against a prior number. In that case:

- Treat the result with extra skepticism — there is no external comparator to corroborate
  whether the reported effect size is plausible.
- Demand a stronger lower-bound (random-rank / shuffled-target) and upper-bound
  (hand-crafted strong baseline) inside this experiment, since they substitute for the
  missing external comparator.
- Flag "no published frontier exists for this cell" as a `medium` finding under
  `literature`, not as a pass-through. The author must acknowledge it in the abstract's
  scope statement.

A frontier-uncovered cell is *not* a free pass for any reported effect size. If anything
the bar for internal robustness rises.

---

## 3. method — model, baselines, features, hyperparameters

### Scope

Whether the modeling choices are defended on something other than fashion or
familiarity, whether the baselines tested make the proposed method's gain interpretable,
whether feature construction was a separate experiment with its own leak checks, and
whether hyperparameter trial counting is honest. Does NOT cover whether the validation
of those choices was correct (that is `validation`).

### Inputs

- The *Method* and *Baselines* sections of the notebook
- Upstream feature-experiment notebook(s)
- `references/modeling_approach.md` and `references/feature_construction.md` from the
  quant-research skill, if available

### Checks

| Check | Failure mode | Default severity |
|---|---|---|
| Model class choice has a substantive justification | "We used an LSTM because LSTMs are well-known" | medium |
| Lower-bound baseline reported (B&H / do-nothing / random) | No floor baseline | high |
| Hand-crafted *upper-bound* baseline reported (linear / logistic / GBT on the same features) | **The single most common gap in submitted experiments.** Without this, the LSTM-vs-momentum comparison cannot tell us whether the LSTM beats *anything but the weakest baseline* | high |
| The proposed method beats both baselines | Proposed beats the floor but not the upper bound | high |
| Feature construction has its own notebook with leak checks | Feature engineering and model fit in one notebook | medium |
| Hyperparameter trial count is documented | The trial count is implicit / unstated | medium |
| In walk-forward, hyperparameter retraining cadence is stated | Hyperparameters fixed on the early val window then frozen across all WF windows ⇒ hyperparameter leakage from early to late windows | medium |
| Model-selection trial count is fed honestly into DSR | Trial count = 1 reported for an experiment that obviously tried more | high |
| Latest version of the model class is used (or older version is justified) | Using a 2015-era LSTM design with no comment when 2024-era equivalents exist | low |

### Notes

The *missing upper-bound baseline* is the single highest-yield finding in this
dimension. A reviewer that returns no other findings but catches this one is
delivering substantial value. When in doubt, demand a logistic / GBT baseline on the
same feature set as the proposed method.

---

## 4. validation — split, embargo, power, discipline

### Scope

Whether the validation procedure is *sufficient*, not whether it is *correct*.
Correctness is `bug_review`'s territory. Sufficiency means: does the validation produce
a metric whose statistical power is consistent with the strength of the claim?

### Inputs

- The *Data and split* cell
- The *Robustness battery* cells
- The *Test-set evaluation* cell

### Checks

| Check | Failure mode | Default severity |
|---|---|---|
| Embargo size is documented and ≥ target horizon | Embargo missing or unstated | high |
| Walk-forward window count is sufficient for the conclusion strength | 8 windows over 10 years carrying a Sharpe-1.1 claim ⇒ implied SE on the mean is large enough that "1.1" and "0.4" may not be statistically distinguishable | medium |
| Walk-forward `pct_positive` is reported alongside the mean | Reporting only the mean hides the distribution shape | medium |
| Bootstrap CI is computed with block bootstrap, not i.i.d. | i.i.d. bootstrap on autocorrelated returns under-states uncertainty | medium |
| 2D threshold sensitivity surface present | Single peak instead of a plateau is the most common overfit signature | medium |
| Regime-conditional Sharpe present | Especially mandatory if the hypothesis is itself a regime claim ("X carries information about volatile periods") | high if hypothesis-implied, otherwise medium |
| DSR ≥ 0.95 with the *honest* trial count | Reported DSR computed with trial count = 1 when actual trial count is 20+ | high |
| Test set touched exactly once | Robustness battery + threshold surface + fee sweep all run on the same held-out test | high |
| Robustness battery run AFTER `bug_review` (the quant-research bug-review layer) | Battery run on a buggy PnL ⇒ all gates green and uniformly contaminated | high |

### Notes

A common subtle finding here: the user reports walk-forward over N windows but does not
state whether *hyperparameters* were re-selected per window or fixed on the first
window. If fixed, the later windows have hyperparameter information from the early
window — a soft test-set leak. Ask explicitly.

---

## 5. claim — conclusion vs. evidence calibration

### Scope

Whether the conclusion in the abstract is the conclusion the evidence actually
supports. The most common pathology: the *technical result* is real but the *abstract
sentence* claims more than what was tested. This dimension exists because authors are
systematically blind to their own overstatement.

### Inputs

- The abstract cell
- The interpretation cell (§8 in the experiment template)
- The conclusion / "Cannot conclude" section
- All the prior dimensions' findings, if available — `claim` triangulates against them

### Checks

| Check | Failure mode | Default severity |
|---|---|---|
| Abstract sentence's scope matches the universe / period / baseline tested | "Beats momentum on SPY 2015–2024" vs. abstract "consistently beats momentum on US equities" | high |
| "Cannot conclude" section enumerates the untested dimensions | Generality is asserted by silence | high |
| Deployment recommendation, if present, is supported by the testing scope | "Recommend deploying as overlay" without a logistic-baseline comparison or other-instrument validation | high |
| Implied portfolio math behind any deployment claim is named | "Overlay" claim without specifying sized to what / netted against what | medium |
| Effect size in the abstract matches the test-set effect size, not the in-sample | Quoting an in-sample number in the abstract | high |
| Verdict matches the *honest* DSR | `verdict = "supported"` with DSR < 0.95 after trial-count audit | high |
| Conclusion does not rebrand a fail as a "novel insight" | "We could not predict returns; this contributes to the literature on weak-form efficiency" without a counter-evidence design | medium |
| Conclusion does not rebrand a *local replication* (Weak-tier achievement) as a *novel finding* | Abstract says "this work shows that momentum predicts returns in US large-caps 2010-2024" framed as a contribution, when the H's pathway-forecasted tier was Medium and the achieved differentiation against Jegadeesh 1990 / Lehmann 1990 / Carhart 1997 is only the period extension — the work confirmed an established result; the abstract must say so | high |
| Forward-looking claims separated from backward-looking findings | Mixing "the model achieved Sharpe 1.4" with "we expect Sharpe 1.4 going forward" | medium |

### Notes

If `claim` produces no `high` findings, double-check the work. A clean-on-claim review
of an experiment that any other dimension flagged is rare; usually overstatement
co-occurs with at least one other gap.

---

## 6. literature — coverage, novelty, differentiation depth

### Scope

Whether the experiment is positioned against the relevant published frontier or against
a frontier of convenience, and whether the work *advances knowledge* given the cited
prior work or merely replicates it locally. Two questions live here, deliberately
labeled separately so that "right papers cited" (coverage) and "result adds something
new given those papers" (novelty) are not silently merged. Does NOT cover whether the
literature claims are *correct* (the reviewer is not adjudicating against the original
papers); only whether the *coverage and novelty* are sufficient.

### Inputs

- `literature/papers.md`
- `literature/differentiation.md`
- The notebook's introduction / motivation cells
- The H's pathway declaration in `hypotheses.md` (the `pathway:` field
  introduced by the `quant-research` skill's `hypothesis_generation.md`
  Step 1.5) — used to read the *forecasted* tier the H committed to at
  generation time

### Coverage checks (did you cite the right prior work?)

| Check | Failure mode | Default severity |
|---|---|---|
| `literature/papers.md` has 5–10 entries with one-paragraph summaries | 4 entries, or 10 entries that are blog posts | high |
| `literature/differentiation.md` is a *matrix*, not a paragraph | One-sentence differentiation | high |
| The most relevant adjacent literature is cited, not just the most famous | Variance-risk-premium / VIX-term-structure literature missing for a VIX-features experiment | high |
| Prior work that previously refuted the method is acknowledged and addressed | A method previously refuted is revived without new justification | high |
| The published frontier's effect size on this question is named | The reviewer cannot tell whether reported Sharpe is at, above, or below the published net-of-cost frontier | medium |

### Novelty checks (does the conclusion advance knowledge given the cited work?)

| Check | Failure mode | Default severity |
|---|---|---|
| Achieved differentiation tier is at least Medium | Achieved tier is Weak (parameter / period changes only on a method documented in the cited papers) — this is a degraded reimplementation, not a research advance | high |
| Achieved tier matches or exceeds the H's *forecasted* tier from its declared pathway | H declared `pathway: 6-mechanism-driven` (Strong forecast) but the achieved differentiation matrix shows only Medium-tier difference — the pathway's promise was not met; either the achieved tier is the new claim or the H re-runs | high |
| The "what is new given the cited literature?" question has a one-paragraph answer in the introduction or interpretation cell | The notebook does not state what knowledge it adds that was not already in `literature/papers.md`; novelty is asserted by silence | high |
| For an H declaring Pathway 1 (Data-driven), the achieved tier is gated on the *achieved* differentiation, not on Pathway 1's "Variable" forecast | Researcher declared Pathway 1 to skirt a Strong-pathway forecast, then claimed novelty in the abstract | high |
| For an H declaring Pathway 2 (literature-extension), the achieved tier is at least Medium *and* the differentiator named in `differentiation.md` is genuinely different in the cell argued | Pathway-2 H whose only differentiator turns out to be a parameter retune of the cited paper | high |

### Notes

The coverage / novelty split makes two distinct findings independently
visible. A coverage failure ("you missed paper X") and a novelty
failure ("given papers X and Y, your result is a local replication
not an advance") are different problems requiring different fixes.
Merging them produces under-informed feedback.

The literature dimension's most useful coverage finding remains "you
missed paper X" with a one-line explanation of why X is the relevant
adjacent work. The reviewer is not expected to be omniscient; they are
expected to ask "what is the literature on the *exact* mechanism this
experiment claims to exploit?" and verify it shows up in `papers.md`.

The literature dimension's most useful novelty finding is the
forecast-vs-achieved tier comparison. The pathway declaration commits
the researcher *before running* to a tier; the experiment either
delivers it or downgrades. A downgrade is not a moral failure — it is
the protocol's normal operation, and the right next move is usually to
narrow the abstract to match the achieved tier rather than to relitigate
the pathway choice.

---

## 7. narrative — notebook as a self-contained communication artifact

### Scope

Whether the notebook works as a communication artifact independent of its research
content. Orthogonal to the other six dimensions: a notebook can describe excellent
research badly, or describe weak research beautifully. This dimension judges only the
artifact, not the research it documents.

The canonical spec is the `quant-research` skill's `references/notebook_narrative.md`
(structural / narrative requirements) and `references/marimo_cell_granularity.md` (one
fit / one evaluation per cell). This reviewer applies those specs as a checklist; this
file does not duplicate them.

### Inputs

- The full notebook `.py` file under review
- The `quant-research` skill's `references/notebook_narrative.md`
- The `quant-research` skill's `references/marimo_cell_granularity.md`
- The notebook's parent project's `purposes/INDEX.md` entry (if any) — the one-line
  conclusion there should match the notebook's headline

### Checks

| Check | Failure mode | Default severity |
|---|---|---|
| Abstract cell at the top is filled in (no template residue, no `[fill in last]`, no `{{TITLE}}` / `{{HYP_ID}}` placeholders) | A reader who opens the `.py` file sees template stubs instead of the conclusion | high |
| Linked hypothesis ID is present and matches `hypotheses.md` | The notebook's claim cannot be located in the project's hypothesis portfolio | high |
| Each section has a "what & why" markdown cell stating what the section does and why it exists | Code cells only, no narrative — the reader cannot tell what the cell is for without running it | medium |
| Each headline figure has an *observation* markdown cell underneath stating what the figure shows | An empty observation = the figure is decoration; observation absent = the figure is illegible to a `.py`-only reader | medium |
| A prose *interpretation* cell exists before the programmatic verdict cell | Verdict is computed without prose explanation of why it is the right verdict | high |
| Headline figures use plotly / altair (or the project's specified equivalent), full width, height ≥ 450 px | Static matplotlib at default size hides detail and removes interactivity | medium |
| At least one `mo.ui` widget exists for evidence drill-down (and the widget does NOT select numbers that flow into `results.parquet`) | No drill-down; OR worse, an interactive widget feeds into the persisted result, breaking reproducibility | medium (no widget) / high (widget feeds results) |
| A "Cannot conclude" section exists and enumerates untested dimensions | Generality is asserted by silence | high |
| Update-reminders cell at the bottom is present and corresponding artifacts (`hypotheses.md` H{n} status, `decisions.md` entry, `purposes/INDEX.md` one-liner) are actually updated | The notebook says "remember to update X" but X is not updated — the audit trail is broken at the boundary | medium |
| Standalone-readability test: a reader who opens *only* the `.py` file (no marimo runtime, no chat context, no slides) can answer: what was investigated, why, how, and what was concluded | The `.py` file alone is insufficient — the notebook depends on out-of-file context to be understood | high |
| Cell granularity per `marimo_cell_granularity.md`: one fit / one evaluation per cell | A single cell loops over models × features × targets, hiding which configuration produced which number | medium |
| No unfilled `{{PLACEHOLDER}}` markers, no untouched copy-paste residue from the experiment template | Visible template artifacts indicate the notebook was generated but not curated | medium |
| Section numbering is consistent and contiguous (no §6 → §8 jumps without intent) | Suggests sections were inserted / removed without re-numbering — a small but corrosive signal of low-care | low |
| Abstract's headline figure reference (e.g. "see cell §X") points at an existing cell with that role | A pointer to a missing or wrong cell makes the abstract unverifiable | low |

### Severity guidance specific to this dimension

- An *unfilled abstract* is `high` regardless of how good the rest of the notebook is.
  The abstract is the load-bearing communication contract; without it the notebook
  cannot communicate its result to a `.py`-only reader.
- A *missing "Cannot conclude" section* is `high` — the silence about untested
  dimensions invites readers to over-generalize the result.
- *Empty observation cells under headline figures* is `medium` (not `high`) because the
  figures may still be self-explanatory to a domain reader; the gap is real but the
  result remains evaluable.
- *No `mo.ui` widget at all* is `medium`. A `mo.ui` widget that *feeds numbers into
  `results.parquet`* is `high` — that breaks reproducibility (the widget state at
  evaluation time is not pinned).

### Notes

This dimension exists because the `quant-research` skill *prescribes* notebook quality
(step 16 + `notebook_narrative.md`) but no other layer *verifies* it. Author self-
discipline is the modal failure point — abstract cells stay as template placeholders,
"Cannot conclude" sections get deferred to "later", `mo.ui` widgets get planned but not
implemented. This reviewer is the verification layer.

A common false-positive trap: marking findings `high` because the notebook does not
match the reviewer's *aesthetic* preferences (font sizes, colour schemes, prose tone).
The checks above are the only ones in scope. Aesthetic preferences are not findings.

A common false-negative trap: a notebook that *is* well-written but whose abstract
cell is filled with text describing a different experiment than the code actually
runs. This is the artifact-vs-content mismatch — flag it as `high`. The check is
"abstract is filled in", but its spirit is "abstract is filled in *with the right
content*".

---

## 8. adversarial — cold-eye standalone reading

### Scope

An independent reviewer that reads the `.py` file alone, on first sight, and attacks
along two axes. This reviewer differs from the seven specialists *not in topic but in
context bundle*: literature, decisions, hypotheses, the seven specialists' findings,
and even upstream feature notebooks are all withheld. The setup mimics the situation
"someone hands you this `.py` file and says: evaluate the experiment from this alone".

The asymmetry is the mechanism. Same model, same prompt rigor, *different bundle*.
Specialists supply the inside view (full context, narrow scope per dimension). The
adversarial reviewer supplies the outside view (no anchor on the author's narrative,
no anchor on the other reviewers' framings). Empirically, minimum-context review on
code yields qualitatively different findings than full-context review (Cross-Context
Review, arxiv 2603.12123, +4.7 F1 on code review).

This reviewer does NOT replace `narrative` (dimension 7). `narrative` checks
*spec compliance* (abstract cell filled in, observation cells present, etc.) against
the `quant-research` skill's `notebook_narrative.md`. The adversarial reviewer checks
*whether spec compliance actually communicates*. A notebook can satisfy every
`narrative` checkpoint and still fail this reviewer's standalone-readability test.

### Inputs

- The `.py` file under review (its full text)

### NOT inputs (deliberately withheld)

- The seven specialist reviewers' findings
- `literature/papers.md`, `literature/differentiation.md`
- `hypotheses.md`, `decisions.md`, `purposes/INDEX.md`
- Upstream feature notebook `.py` files (even if the design cell names them — the
  reviewer is meant to feel the pain that an external reader feels when handed a
  single-file artifact)
- Chat context, prior-cycle discussion, agent's own scratchpad

### Two axes of attack

**Axis 1 — claim warrant**

Does the abstract / verdict / headline numbers (Sharpe, universe, period) hold up on
the evidence visible in this `.py` file alone?

- A claim that requires "see also pur_001 / see slides / see the project README" to be
  supported is overstatement when the headline is read standalone — `high` finding.
- A number in the abstract that disagrees with the same number in a results cell —
  internal inconsistency, `high`.
- A "deployment recommendation" that depends on portfolio math not shown in the file —
  `high`.

**Axis 2 — standalone-readability (cold-read Turing test)**

Could a third party who reads only this `.py` file answer: what was investigated, why,
how, and what was concluded?

- An abstract cell is *present* but described an experiment whose code is not what was
  run — `high`.
- An observation cell is *present* but says only "Figure shows X" without explaining
  what X means or implies — `medium`.
- A "Cannot conclude" section is *present* but lists no actually-untested dimensions —
  `medium`.
- The interpretation cell uses jargon undefined within the file (e.g., references a
  literature term not introduced) — `low` to `medium` depending on how load-bearing the
  jargon is.

### Instruction (give to the reviewer agent verbatim)

> "You are an external cold reader. The `.py` file you are about to read is the only
> material you are given. Other materials (literature, hypotheses, decisions, prior
> cycles, the seven specialist reviewers' findings) are intentionally withheld — the
> goal is to keep you from anchoring on priors that the same model shares with the
> author or with other reviewers.
>
> Attack along two axes:
>
> 1. Claim warrant: does the abstract / verdict / headline figure hold up on the
>    evidence visible in this file alone? Anything that depends on external materials
>    is overstatement.
>
> 2. Standalone-readability: can you, reading this file alone, explain what was
>    investigated, why, how, and what was concluded? Things that look correct because
>    of context you would have outside this file should be flagged.
>
> Return findings in the standard severity-tagged schema."

### Severity guidance

- The two axes are *equally weighted* — overstatement (axis 1) is not automatically
  more severe than incommunicability (axis 2). A notebook with the right answer that
  no future reader can decode is a research artifact failure.
- Findings here can overlap with findings from `claim` and `narrative`. The overlap
  is intentional and is not noise: same finding from two reviewers with different
  bundles is *strong* evidence; different findings from the same area is *richer*
  evidence.

### Notes

The most common failure this reviewer catches that the seven specialists miss: a
result that *makes sense in context* (because the agent has been working on this
project for a while and shares the author's context) but that fails when handed to
a fresh reader. The seven specialists are not adversarial cold-readers; they are
domain specialists with full bundle. This reviewer fills that gap.

The most common false alarm this reviewer produces: flagging a notebook for *not
including* literature context that lives in the project's `literature/` folder.
The reviewer was deliberately not given access to that folder; "claim depends on
external material" is `high` only when the file's claim *requires* the external
material to be true, not when the file simply *omits* the external material from
its own narrative. (If the abstract says "X works" and the file alone shows X works
under the conditions tested, that is sufficient — even if the literature folder
contains the broader context.)
