# AI-R01 — AI Model Role Registry

## Why This Question Remains

The AI layer needs role separation and authority limits.

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

- Which AI model should be built first?
- What is the role of ranker, veto, context power, ambiguity, anchor selector, width policy, and cancel/replace models?
- Which models are advisory only?
- Which models can veto?
- Which models can select an execution template?
- Which models must never send orders?

## Expected Output

```text
`ai_model_role_registry_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/contexts/legacy/experience_capture/answers/AI-R01/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
