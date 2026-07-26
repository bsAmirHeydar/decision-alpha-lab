# EXE-R01 — Order Type Policy by Entry Family

## Why This Question Remains

Extreme is limit-based, but other entries may not be.

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

- Which entry families are limit-only?
- Which entry families may use market order?
- Which entry families may use pending stop order?
- Which order types are forbidden?
- Should order type be hard rule or model policy?
- How should order type be represented in ExecutionIntent?

## Expected Output

```text
`entry_order_type_policy_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/contexts/legacy/experience_capture/answers/EXE-R01/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
