# EXP0016 - Astro Meta Learner

## Purpose

EXP0016 is the professional learning layer above the rule-based astro system.
It does not assume that any planet is permanently bullish or bearish. It asks:

```text
Given the mechanical astro state at candle t, what did the market actually do after t?
```

Then it learns:

- direction
- clean path
- spike / hunt
- trap / reversal
- volatility expansion

## Core hypothesis

Astrology may be more useful as a state-description language than as a fixed rule system.
A learned model can discover when a normally bullish configuration becomes a trap, when pressure means clean short continuation, and when a configuration only implies volatility.

## Architecture

```text
Astro Feature CSV
+ Price Candle CSV
-> causal ML dataset
-> target labels per horizon
-> chronological train/test
-> walk-forward validation
-> saved model memory
-> feature importance + extracted rules
-> out-of-sample prediction
```

## Key principle

Feature at t must not contain future market information. Outcome labels use only bars after t.

## Main tools

```text
tools/astro_ml/build_astro_ml_dataset.py
tools/astro_ml/train_astro_meta_learner.py
tools/astro_ml/evaluate_walk_forward.py
tools/astro_ml/explain_astro_model.py
tools/astro_ml/predict_with_astro_memory.py
tools/astro_ml/query_astro_memory.py
mql5/Scripts/AstroML/ExportRatesForAstroML.mq5
```

## Memory output

```text
Common/Files/astro_ml/memory/<ASSET>/<TIMEFRAME>/
```

This memory folder stores trained models, metrics, predictions, explanations, and learned rules.

## Acceptance criteria

A learned astro model is only useful if it beats baselines out-of-sample and remains stable in walk-forward testing.

Minimum acceptance checks:

- walk-forward balanced accuracy above majority baseline
- no single feature dominates due to leakage
- results stable across different years/months
- untouched test period stays positive
- feature explanations make mechanical sense

## Failure criteria

Reject or downgrade the model if:

- it only works in random split
- walk-forward collapses
- test period is below baseline
- feature importance is dominated by future/outcome columns
- performance depends on one tiny period or one asset only
