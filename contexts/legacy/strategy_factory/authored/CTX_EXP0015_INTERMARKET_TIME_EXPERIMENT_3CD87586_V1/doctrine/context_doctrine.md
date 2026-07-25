# Context Doctrine

The context observes an asymmetry between two time-aligned bar series. At an eligible evaluation bar, one symbol crosses or touches a selected historical reference while the destination symbol does not satisfy the same trigger inside a bounded destination-lag window. The result is a research context occurrence, not a trade instruction.

This migration preserves the exact legacy reference families, trigger predicates, alignment, duplicate-time policy, valid-window construction, late-destination annotation, event ordering, and string serialization. It does not assert that the legacy semantics are economically valid, timezone-complete, or production-ready.
