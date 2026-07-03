# EXE-R02 — Pending Order Cancel and Replace Policy

## Why This Question Remains

Execution needs cancel/replace logic without becoming random or over-mechanical.

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

- When should an unfilled pending order be cancelled?
- When should it be replaced deeper, closer, or not moved?
- What structural events force cancellation?
- What execution events suggest replacement?
- How should missed-limit data influence future policy?
- Should cancel/replace be rule-based first or AI-learned?

## Expected Output

```text
`cancel_replace_policy_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/EXE-R02/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
