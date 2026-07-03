# TEST-R01 — Baseline, OOS, Ablation, and Negative Controls

## Why This Question Remains

No trained policy should be accepted without anti-overfit evidence.

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

- What is the rule-based baseline for each entry family?
- What naive/random baselines must be beaten?
- How should out-of-sample splits be designed?
- Which ablations are mandatory?
- Which negative controls should fail?
- What makes a result fragile or overfit?

## Expected Output

```text
`anti_overfit_test_protocol_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/TEST-R01/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
