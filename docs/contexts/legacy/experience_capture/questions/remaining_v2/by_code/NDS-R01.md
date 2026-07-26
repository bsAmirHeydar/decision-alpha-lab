# NDS-R01 — Canonical NDS Object Model

## Why This Question Remains

The answered records define ontology boundaries, but the exact object model is still open.

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

- Define every core NDS object that must exist in v1: Hook, Rally, F-count, Node, Cycle, Scenario, Zone, Destination, Invalidation, Entry Family, and ExecutionIntent.
- For each object, specify required fields, optional fields, and forbidden fields.
- Separate deterministic anatomy objects from learnable policy objects.
- Define which objects can be nested across parent/current/child scales.
- Define which objects must be drawn on chart for audit.
- Define how every object should receive a stable ID.

## Expected Output

```text
A schema-ready object model for `canonical_state_packet_v1`.
```

## Answer Storage Convention

When answered, create a separate answer folder:

```text
docs/contexts/legacy/experience_capture/answers/NDS-R01/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

## Image Requirement

Use an image only if it clarifies the structure. If an image is provided, store it under the answer folder and mark all relevant NDS objects.
