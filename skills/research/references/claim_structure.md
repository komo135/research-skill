# Claim Structure

## Purpose

Every load-bearing claim in `propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md` and `propositions/Pxxx_slug/hypotheses/Hxxx_slug/reports/<id>_<slug>/report.md` uses an explicit, structured record. The structure does two jobs:

1. **It forces the agent to articulate what the claim actually rests on and what it does not exclude** — preventing claims that read confidently but are actually thin on evidence.
2. **It makes claims machine-checkable.** `scripts/check_claims.py` parses the structure and verifies required fields are present and non-empty where required.

The structure derives from Toulmin's argument model ([*The Uses of Argument*, 1958](https://en.wikipedia.org/wiki/Stephen_Toulmin#The_Toulmin_model_of_argument)) — claim, evidence, qualifier, rebuttal — adapted for research-state records.

## Why no numeric strength ladder

This skill does not use A0-A5, TRL, GRADE, or any other numbered scale. Those ladders mix multiple dimensions (causal strength, replication, generalization, scope) into a single number, and they invite agents to overclaim by self-rating high.

Instead, claim strength is read off the structural contents — specifically the contents of `alternatives_not_excluded` and `conditions_not_tested`. A claim with empty lists in both is a strong claim, and the burden is on the agent to justify those emptinesses. A claim with non-empty lists is, by its own admission, scoped or preliminary. The structure reports its own strength.

## Schema

```yaml
- claim: <one sentence with specific assertion>
  evidence: <file:line / numeric value / artifact path / citation>
  alternatives_not_excluded: [...]    # empty list [] claims exhaustion
  conditions_tested: <variable ranges, datasets, parameters>
  conditions_not_tested: [...]        # empty list [] claims full coverage
```

All five fields are required. Empty list `[]` is allowed for `alternatives_not_excluded` and `conditions_not_tested` — it asserts exhaustion and is open to challenge. A missing field is not the same as an empty list; missing fields cause `check_claims.py` to fail.

## Fields

### claim

One sentence stating the assertion. Specific enough that someone can decide whether it is true.

- ✗ Bad: "Our method is better."
- ✗ Bad: "Attention is useful."
- ✗ Bad: "The system works well."
- ✓ Good: "The proposed scrambled-Halton sampler reduces samples-to-converge by approximately 20% versus pseudo-random MC on the 12-D Gaussian mixture integrand at precision tolerance 1e-4 on 3 of 3 runs."

Specific = states *what* improved, *by how much*, *under what conditions*, *with what sample size*. Vague claims fail `check_claims.py`'s heuristic check.

### evidence

A pointer to the specific basis for the claim. This is an evidence-integrity anchor, not by itself a reproducibility guarantee: it lets a reviewer check that the reported value is connected to a concrete artifact, value, or citation, while the method and tested conditions still carry the reproducibility burden. Acceptable forms:

- **file:line** — `propositions/P001_phase-transition/hypotheses/H001_probe/experiments/runs/H001__003__seed42/outputs/metrics.json:L8`
- **Numeric value with provenance** — `mean BLEU 28.4 (SE 0.3) across 5 seeds, see Table 2 of reports/R02/report.md`
- **Artifact path** — `propositions/P001_phase-transition/hypotheses/H001_probe/experiments/runs/H001__005__seed0/outputs/convergence.csv`
- **Citation** — `Vaswani et al. 2017, Table 1`

Do not use vague evidence like "the experiments," "the data," or "as discussed above."

#### Statistical reporting minimum (when evidence is a numeric measurement)

A numeric `evidence` field for an empirical claim must specify at least:

- **Point estimate** — the mean, median, or other summary statistic, with units
- **Dispersion** — standard error, standard deviation, IQR, or confidence interval; **never a bare point estimate** for stochastic outcomes
- **Sample size (n)** — number of independent draws, seeds, folds, runs, or observations contributing to the estimate
- **Significance / effect size** — when the claim is comparative (e.g., "X is better than Y"), report effect size (Cohen's d, Δ%, IR difference, etc.) AND a significance criterion (p-value with correction for multiple testing, or confidence interval that excludes the null)

Examples of compliant evidence:

- Quant: `IR 1.12 (95% CI [0.78, 1.46], n=240 monthly returns, walk_forward 3 folds), Delta vs benchmark IR 0.42 (p<0.01 with Bonferroni correction across 18 tested signals); see propositions/P001_signal-quality/hypotheses/H001_walk-forward/experiments/runs/H001__005__seed0/outputs/walk_forward_results.csv`
- ML: `BLEU 28.4 (SE 0.3, n=5 seeds), Δ vs baseline 27.3 = 1.1 (Cohen's d 2.8, paired t-test p<0.001); see reports/R02/tables/translation_results.csv`
- Basic research: `phase transition observed at T_c = 2.27 +/- 0.05 (n=12 independent runs, sigma/sqrt(n) reported); see propositions/P001_phase-transition/hypotheses/H001_temperature-scan/experiments/runs/H001__012__seed0/outputs/transition_temps.csv`

Examples that fail the minimum:

- `IR 1.12` — no dispersion, no n
- `our method is better than baseline by 5%` — no significance, no n, no condition
- `Sharpe ≈ 1.5` — point estimate only; for stochastic outcomes this is not evidence

For non-stochastic outcomes (e.g., a closed-form derivation result, a deterministic algorithm output, a one-shot measurement that does not have a sampling distribution), say so explicitly: `evidence: deterministic output of f(x=3.7) = 12.49, no sampling distribution applicable, see lib/foo.py:L42`.

This minimum is a claim-recording requirement. Result analysis may explain why the numeric result happened, but the claim record is where numeric outputs must be reported with point estimate, dispersion, sample size, and comparison details.

### alternatives_not_excluded

A list of competing explanations or confounders that the current evidence has NOT ruled out. Examples:

- "The improvement may come from increased compute, not from the new component"
- "Seed_42 might be a lucky draw — only n=2 independent seeds run"
- "The baseline may have been under-trained"
- "The improvement is within the seed-to-seed noise band (std 0.3, observed gap 0.18)"

Empty list (`[]`) claims that no plausible alternatives remain — a strong assertion that should be supported by ablations, controls, or theoretical argument. If the agent writes `[]`, the agent is asserting exhaustion and accepts the audit burden.

### conditions_tested

Describe the variable ranges, datasets, and operating points under which the claim was verified. Be specific:

- "WMT 2014 EN-DE, beam size 4, model dim 512, 100k training steps, AdamW lr=1e-4 cosine schedule, batch size 32k tokens"
- "σ ∈ [5, 30] sampled at Δσ=0.5, ρ=28, β=8/3, T=200 time units after 50-unit transient discard, dt=0.01, rtol=1e-9"
- "Batch sizes 32, 128, 512, 2048 with 3 seeds each, ViT-B/16 on ImageNet, 90 epochs"

Vague descriptions like "standard setup" or "the same as before" fail. Be explicit; cross-session readers do not have your context.

### conditions_not_tested

A list of conditions, ranges, or settings outside what was tested but where the claim might be naturally extended. This is where over-generalization gets caught.

Examples:

- "Batch sizes above 2048"
- "Datasets other than WMT 2014 EN-DE and EN-FR"
- "σ outside [5, 30]"
- "Non-canonical ρ or β in the Lorenz system"

Empty list (`[]`) claims full coverage of the relevant condition space — also a strong assertion to justify.

## Reading claim strength

There is no numeric strength score. Strength is read off the structural contents:

| Pattern | Reading |
|---|---|
| Both lists empty and exhaustively reasoned | Strong claim; audit each emptiness explicitly |
| `alternatives_not_excluded` non-empty | Preliminary or scoped claim |
| `conditions_not_tested` non-empty | Scoped claim — boundary is stated |
| Both non-empty | Preliminary AND scoped — explicit limits on use |

The skill does not assign labels like "A4" or "supported." The structure itself communicates strength to a reader who can interpret it.

## When the structure is required

A claim is load-bearing — and therefore requires this structure — when:

- It appears in a derived-hypothesis report Summary, Results, or Conclusions section
- It triggers a proposition or hypothesis `decisions.md` entry when a state transition depends on it
- It is cited by another claim
- It is communicated externally (to a collaborator, a publication, a deployment decision)

Casual observations during exploratory work do not need the structure. The agent decides what is load-bearing. If unsure, structure it.

## Common failures

- **Vague claim text.** "Our method works." Fix: state the specific assertion with metric, magnitude, conditions.
- **Vague evidence.** "See the experiments." Fix: cite specific files, lines, values, or tables.
- **Both lists empty without justification.** Empty lists are claims about exhaustion. Make sure they are defensible — otherwise list what is actually not excluded or not tested.
- **conditions_tested too narrow for the claim.** "Tested on seed=42" + claim "method generally works" — the claim outruns the evidence. Either narrow the claim or test more conditions.
- **Splitting a single complex claim across many tiny ones.** Each claim record is at the granularity of an actual assertion, not a fragment. Coordinated claims that depend on each other should be one record.
- **Recording observations as claims.** "We saw X" is not a claim. A claim asserts something general; an observation reports a specific event. Use claims for assertions that drive decisions.

## Verification

`scripts/check_claims.py` parses the structure from hypothesis `plan.md` and report `report.md` files and reports:

- Missing fields
- Claim text that is vague (no metric, no specifics, no condition reference)
- Evidence pointers that don't resolve to existing files
- Suspicious patterns — e.g., empty `alternatives_not_excluded` for a claim that mentions "better than baseline" without an ablation citation

Run it before any external sharing or proposition/hypothesis `decisions.md` entry that depends on the claim. Run it before drafting a report.
