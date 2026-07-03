# SYS-R01 — Implementation Order to Shadow Mode

## Why This Question Remains

The next build path must avoid premature execution and follow NDS schemas.

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

- Which docs/schemas must be written before code?
- Which deterministic exporters must come before AI?
- Which labels must exist before training?
- Which simulator features must exist before paper mode?
- Which gates must exist before any broker bridge?
- What is the minimum viable path to Shadow Mode?

## Expected Output

```text
`nds_to_shadow_mode_roadmap_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/SYS-R01/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
