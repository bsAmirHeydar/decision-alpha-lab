# SCN-R04 — Layered Invalidation: Entry, Anchor, Zone, Scenario

## Why This Question Remains

EXT-06 defines anchor death, but broader scenario death still needs separation.

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

- When does only the entry candidate die?
- When does only the Extreme anchor die?
- When does the zone die?
- When does the whole scenario die?
- If child Extreme dies but parent scenario remains alive, should the system search for a new entry?
- What exact invalidation states must be logged?

## Expected Output

```text
`layered_invalidation_model_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/experience_capture/answers/SCN-R04/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
