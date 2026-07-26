# 01 Concepts README

This package introduces the conceptual vocabulary of Flag Counting.

It answers:

- What is a node?
- What is L?
- What is a flag?
- What are F1, F2, and F3?
- What is ND/Hook?
- What is a sequence?
- What does it mean for a structure to be candidate, confirmed, completed, locked, invalidated, or rejected?
- Why must the detector be sequence-based rather than sliding-window-based?

## Files

- `CONCEPT_GLOSSARY.md`: short but precise vocabulary.
- `CONCEPT_TAXONOMY.md`: hierarchy of objects in the system.
- `INVARIANTS_AND_ASSUMPTIONS.md`: rules that must never be violated.

## Concept Map

```text
Candle High/Low
  -> Project Node Engine
    -> Node(L)
      -> Flag Body
        -> F1 / F2 / F3 Role
          -> Sequence Chain
            -> Rendering Object / Audit Object

Node Streams
  -> Hook Branch Engine
    -> Internal 1/2/3/4
      -> ND/Hook Event
      -> F Confirmation Input
      -> Next-F Origin Backfill Context
```

## Key Principle

The model is not looking for decorative shapes. It is building a sequence of owned structural phases.

A drawn line must answer all of these questions:

```text
Which chain owns it?
Which F-level is it?
Where is its origin?
Where is Leg1?
Where is the true Waist?
Where is Leg2?
What is its status?
Why is it still alive?
What would invalidate it?
What can it produce next?
```

If those questions cannot be answered, the object must not be drawn as a flag.
