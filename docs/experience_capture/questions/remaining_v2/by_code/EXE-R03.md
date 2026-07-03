# EXE-R03 — Spread, Thin Stop, and Effective Risk

## Why This Question Remains

Very thin stops can be valuable, but spread can destroy the actual risk model.

## What Has Already Been Answered

Do not repeat or overwrite the captured answers.

Answered codes that must remain untouched:

```text
BASE-01
BASE-02
BASE-03
BASE-04
BASE-05
BASE-06
EXT-01
EXT-02
EXT-03
EXT-04
EXT-06
EXT-07
EXT-08
EXT-09
EXT-10
EXT-11
EXT-12
```

## Answer Requirements

- When is raw stop too close to spread?
- When should thin stops still be allowed?
- Should spread be hard veto, score penalty, or warning?
- Should spread policy differ by symbol or timeframe?
- How should effective risk after spread be calculated?
- How should this be simulated in backtest?

## Expected Output

```text
`spread_sanity_policy_v1` and `effective_risk_model_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/EXE-R03/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
