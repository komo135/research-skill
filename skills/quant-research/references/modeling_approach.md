# modeling_approach.md

Selection guide for mathematical models / classical ML / deep learning / reinforcement
learning / foundation models, and category-specific failure modes.

## When to read

- Right after stating a new hypothesis (before deciding which model to use)
- When the current model is not behaving as expected and a category change is being
  considered

## Selection principle

"Use ML by default" or "use a math model by default" is not allowed as justification.
Choose based on the structure of the hypothesis.

| Hypothesis structure | Suitable category |
|---|---|
| Stochastic-process assumption holds (mean-reversion, jump-diffusion) | Math models (OU, jump-diffusion, Hawkes process) |
| Linear relationship + interpretability needed | Classical ML (linear, logistic, ridge / lasso) |
| Non-linear relationship + medium sample size | Tree-based (Random Forest, GBM, XGBoost, LightGBM) |
| High-dimensional or unstructured input (text, images, order book) | Deep learning (MLP, CNN, RNN, Transformer) |
| Time-series forecasting with long context | Transformers / foundation models (Chronos, TimesFM, Moirai) |
| Action-policy optimization (sizing, execution, rebalancing) | Reinforcement learning (DQN, PPO, SAC, Dec-POMDP) |
| Latent state (regime, hidden factor) | State-space models (HMM, Kalman, particle filter) |

## Failure modes by category

### Math models

| Failure | Check |
|---|---|
| Assumptions not verified (stationarity, normality, independence) | See `model_diagnostics.md` |
| Parameter estimates unstable | Window-length sensitivity, standard errors |
| Specification error | Residual diagnostics, Ljung-Box, ADF test |

### Classical ML

| Failure | Check |
|---|---|
| Data leakage (target seeps into features) | See `feature_construction.md` leakage check |
| Feature importance unstable across time | Rolling-window importance plot |
| Overfit (high dimension, low sample) | Learning curve, cross-validation, regularization |
| Class imbalance | Balanced sampling, class-weighted loss, PR curve |

### Deep learning

| Failure | Check |
|---|---|
| Overfit on small samples (financial data is often small) | Dropout, early stopping, careful augmentation |
| Selection bias from hyperparameter search | Record number of trials → Deflated Sharpe Ratio |
| Reproducibility (seed, RNG) | Fix seed, report mean over multiple seeds |
| Cost-vs-performance trade-off | Plot the cost / performance frontier |
| Lack of interpretability | SHAP, attention maps, integrated gradients |

### Reinforcement learning

| Failure | Check |
|---|---|
| Reward hacking | Visualize the learned policy, compare across reward functions |
| Sample inefficiency | Consider offline RL; verify simulator fidelity |
| Sim-to-real gap | Always evaluate on real (held-out) data |
| Local optima | Report distribution over multiple seeds |

### Foundation models

| Failure | Check |
|---|---|
| Using an outdated version | Confirm the latest version exists before implementation |
| Demoting a forecaster to a frozen feature extractor | Use the forecast distribution or the generative API directly |
| Generalization failure on financial data | Always compare zero-shot vs. fine-tuned |
| Inference cost | Cache embeddings, batch inference |

## How to justify the model choice

In each experiment notebook, write:

| Bad | Good |
|---|---|
| "It is fast and lightweight" | "Among public models A/B/C, only A exposes a `.embed()` API" |
| "It is famous" | "It exceeds SOTA on benchmark X by 3 percentage points" |
| "I just tried it" | "Hypothesis H requires structure in the time dimension, and Transformer captures that" |
| Naming an old version | "Confirmed the latest version → using the latest" |

## Hybrid approaches

Hybrid pipelines are common in practice. Examples:

- PCA factor decomposition → ML (GBM) on the residuals
- HMM regime classification → separate models per regime
- Kalman state estimation → RL policy on top

For hybrids, label which layer is math and which is ML, and run the corresponding
diagnostics on each layer.

## Always include baselines

A complex proposed model is meaningful only when it beats both:

- **Lower bound**: random / constant prediction / B&H
- **Hand-crafted upper bound**: simple feature set + linear model

A model that does not beat the hand-crafted upper bound is rarely worth its complexity.
