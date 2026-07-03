# EXT-R04 — Multi-Anchor Execution Policy

## Why This Question Remains

EXT-07 says each nearby L2 can be an opportunity, but execution must still decide what to do.

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

- Should all valid nearby anchors be logged?
- Should only one anchor be selected for order placement?
- When can layered entries be allowed?
- How should risk be split across multiple anchors?
- When should secondary anchors stay watchlist-only?
- When should one anchor replace another?

## Expected Output

```text
`multi_anchor_execution_policy_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/EXT-R04/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
