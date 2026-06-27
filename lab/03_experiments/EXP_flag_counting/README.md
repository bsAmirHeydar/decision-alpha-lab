# EXP Flag Counting

This experiment studies the Flag Counting grammar as a market-state engine.

The experiment is no longer defined as a simple pattern scanner. It must evolve into a fractal multi-scale, multi-sequence state machine.

## Reference documents

- `docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3.md`
- `docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md`
- `docs/flag_counting/FLAG_COUNTING_GLOSSARY.md`

## Research objective

Build an engine that can classify each relevant movement region as:

- ND / Hook phase
- F1 root phase
- F2 continuation phase
- F3 terminal phase

and expose this state to strategy code and visual audit tools.

## Visual contract

Draw only clean accepted bodies:

- Origin -> Leg1 as a straight line.
- Leg1 -> Waist -> Leg2 as a smooth curve tangent to Waist.
- F1/F2/F3 label.
- Internal 1/2 numeric labels.

Debug layers may exist, but the default chart should not dump every rejected candidate.

## Engineering target

The experiment should produce a reusable module, not just one expert:

- node engine
- ND/Hook engine
- F body builder
- internal count engine
- continuation engine
- sequence registry
- conflict resolver
- state query API
- renderer
- audit logger
