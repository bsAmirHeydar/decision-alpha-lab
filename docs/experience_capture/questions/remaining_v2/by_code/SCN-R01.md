# SCN-R01 — Context Power Scoring

## Why This Question Remains

You repeatedly mention that the system must understand which context has power.

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

- What makes one context stronger than another in NDS terms?
- How should parent, current, and child context be compared?
- When does parent context override a local entry?
- When can child/local structure weaken the parent view?
- What minimum reason vector is required before a context becomes tradable?
- Should context power be a score, class, or both?

## Expected Output

```text
`context_power_model_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/SCN-R01/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
