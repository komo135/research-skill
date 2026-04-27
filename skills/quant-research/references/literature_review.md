# literature_review.md

Prior-work review at the start of a new research project. Prevents producing a degraded
reimplementation of an existing paper.

## When to read

- Initial setup of a new research project (before any implementation)
- Before adding a new hypothesis (to confirm it has not already been studied)

## Goal

Avoid the "degraded reimplementation" failure mode. Specifically:

- Avoid reinventing a known method under a different name
- Avoid inheriting known limitations (where prior work fails) without addressing them
- Make explicit how the new research differs from prior work

## Procedure

### 1. Collect 5-10 related papers

Reasonable starting points by topic:

| Topic | Venues / authors |
|---|---|
| Statistical arbitrage, pairs trading | Quantitative Finance; Avellaneda, Khandani-Lo, Lo-MacKinlay |
| Factor models | Journal of Financial Economics; Fama-French, Stambaugh |
| ML × finance | López de Prado, Quantitative Finance, JFDS |
| Time-series forecasting | NeurIPS / ICML time-series tracks; foundation models (Chronos, TimesFM) |
| RL × trading | NeurIPS, JMLR, AAMAS |
| HFT, market microstructure | Journal of Finance; Cont, Bouchaud |

Search strategy:

- arxiv.org (q-fin.* categories)
- SSRN
- Google Scholar — sort by citations on the topic's base terms
- Snowball back from recent papers' references to the canonical works

### 2. Record them in `literature/papers.md`

For each paper:

```markdown
## [Author (Year)] Title

- venue: ...
- citations: ...
- main claim: [one paragraph]
- method: [model type, data, validation]
- limitations (stated by the authors, or evident weaknesses):
- relation to this research: [use / compare / differentiate from / refute]
```

### 3. Build a differentiation matrix in `literature/differentiation.md`

| Aspect | Prior A | Prior B | This research |
|---|---|---|---|
| Data range | ... | ... | ... |
| Universe | ... | ... | ... |
| Method | ... | ... | ... |
| Evaluation metric | ... | ... | ... |
| Claim | ... | ... | ... |

The "this research" column must contain **at least one cell** that is clearly distinct from
the prior columns. That cell defines novelty. If no such cell exists, redesign the research.

## Levels of differentiation

| Level | Examples |
|---|---|
| Strong | New mathematical model / new ML architecture / new evaluation metric |
| Medium | Existing method applied to new data or universe / novel combination of known methods |
| Weak | Different parameters / different period / reimplementation of the same method |

A research project that only achieves "weak" tends to become a degraded reimplementation.
Aim for at least "medium".

## Warning signs

- A heavily cited paper (100+ citations) uses substantially the same method, and you have
  not noticed
- "This research is just an application of method X to data Y" with no further differentiation
- Prior work's known limitations (data leakage, overfit, selection bias) are inherited without
  remediation
- A method previously refuted in the literature is being revived without new justification

If any sign appears, redesign the research before proceeding.
