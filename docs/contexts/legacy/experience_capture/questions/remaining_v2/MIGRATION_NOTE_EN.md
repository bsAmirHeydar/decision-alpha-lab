# Safe Migration Note

## What This Overlay Does

This overlay adds a new active remaining-question set:

```text
docs/contexts/legacy/experience_capture/questions/remaining_v2/
```

## What This Overlay Does Not Do

It does not delete:

```text
docs/contexts/legacy/experience_capture/answers/
```

It does not overwrite answered question files for:

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

## Why

The captured answers are the source of truth.

The goal is only to rewrite the remaining questions and extract unresolved ambiguities.
