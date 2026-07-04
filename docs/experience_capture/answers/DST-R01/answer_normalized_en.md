# DST-R01 — Normalized Interpretation

## Core Claim

Destination logic in NDS is not fully frozen yet.

Destinations can emerge or become clearer through later structure, especially:

```text
F-countings that appear after the trade idea or entry
open one-and-two structures along the path
counting inside the higher Hook
```

The current objective is not to close profits too early.

The system should attempt to keep more of the profit open when structural potential remains.

Destination logic should therefore be treated as a trainable policy, not a fully hard-coded rule.

## Destination as Candidate, Not Fixed Truth

A Destination should initially be modeled as a candidate set, not as one fixed target.

Recommended canonical object:

```text
DestinationCandidateSet
```

Because the user explicitly says that destinations may become clear through later F-countings, the system should allow destinations to be updated, expanded, repriced, or reweighted as new structure forms.

## Destination Sources

Based on the answer, the first confirmed destination sources are:

```text
later F-counting
open one-and-two structures along the path
counting inside the higher Hook
```

These should become destination candidate families.

Suggested families:

```text
F_COUNTING_DESTINATION
OPEN_ONE_TWO_DESTINATION
HIGHER_HOOK_COUNTING_DESTINATION
PATH_STRUCTURE_DESTINATION
```

Other sources remain possible but should not be over-formalized without more evidence.

## Later F-Counting as Destination

A destination may become clearer after the position or scenario already exists.

This means destination logic is dynamic.

A system should be able to say:

```text
new F-counting appeared
destination candidate updated
destination weight changed
profit openness changed
```

This also means early exit logic must not assume that all destinations are known at the time of entry.

## Open One-and-Two in the Path

The answer confirms that open one-and-two structures along the path can contribute to destination logic.

Interpretation:

```text
open one-and-two = incomplete structure in the path that may later attract completion by a three
```

However, timing is not guaranteed.

Therefore, open one-and-two should be treated as a destination/magnet candidate, not as a timing signal.

Recommended state:

```text
OPEN_ONE_TWO_DESTINATION_CANDIDATE
```

## Counting Inside the Higher Hook

Destination can be derived using counting inside the higher Hook.

This creates a parent-child relation:

```text
higher Hook context
→ internal counting
→ destination candidate
```

This is consistent with NDS fractality.

The higher Hook provides the larger structural container, while lower/internal counts can identify possible destination areas.

## Profit Openness as Objective

The user states:

```text
the attempt is to hold more and keep profits open
```

This means destination logic should not be used only for early full exit.

It should support:

```text
holding more when potential remains
keeping runner/tail exposure
avoiding premature closure
updating destination candidates as structure develops
```

This links DST-R01 to DST-R02.

DST-R01 defines destination uncertainty and candidate formation.

DST-R02 defines exit policy and partial close logic.

## Destination Uncertainty

The user explicitly says:

```text
I still do not know much about destination.
It needs training.
```

Therefore, the correct architecture is not to pretend destination logic is solved.

The model should preserve uncertainty using fields such as:

```text
destination_confidence
destination_source
destination_trainable
destination_weight
destination_openness_score
```

Destination should be a learning target.

## Trainable Destination Policy

Destination policy should be trained and evaluated.

Possible training targets:

```text
which destination candidates are actually reached
which destination candidates are useful for exits
which candidates preserve profit openness
which candidates cause premature exits
which candidate families work per market/timeframe
how higher Hook counting affects destination quality
how open one-and-two candidates behave
```

## Machine-Readable Summary

```text
Destination is not fully hard-coded yet.

Confirmed destination sources:
  - later F-counting
  - open one-and-two structures in the path
  - counting inside the higher Hook

Destination logic should:
  - remain trainable
  - support candidate sets
  - update as new structure appears
  - preserve profit openness
  - avoid premature full exits
```

## Short Formal Statement

In NDS, destination logic is currently a trainable candidate-set problem rather than a fully fixed rule. Destinations may become clearer through F-countings that form later, through open one-and-two structures along the path, and through counting inside the higher Hook. The system should try to hold more and keep profits open when structural potential remains. Because destination behavior is not yet fully known, destination candidates should be logged, weighted, updated, and trained instead of being treated as a single certain target.
