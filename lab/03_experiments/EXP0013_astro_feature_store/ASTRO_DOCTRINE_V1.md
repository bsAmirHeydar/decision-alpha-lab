# ASTRO Doctrine V1

This document freezes the first formal doctrine snapshot for the EXP0013 astro-only stack.

## Core doctrine

- zodiac mode: `tropical`
- body universe: `major7_outer_nodes`
- house system: `P` / Placidus
- aspect family: `major_ptolemaic_6deg`
- parallel orb limit: `1.0`
- doctrine id: `astro_only_doctrine_v1`
- schema version: `astro_feature_schema_v2`

## House semantics

- `H1`: emergence, activation, visible ignition
- `H2`: resources, accumulation, material consolidation
- `H3`: motion, messaging, local signal noise
- `H4`: root, base, reversal foundation
- `H5`: release, appetite, expressive impulse
- `H6`: correction, friction, maintenance drag
- `H7`: polarity, counterpart force, opposition field
- `H8`: compression, liquidation, hidden pressure
- `H9`: expansion, belief, directional thesis
- `H10`: execution peak, visibility, public action
- `H11`: continuation, support, follow-through
- `H12`: dissolution, exhaustion, invisible loss of force

## Aspect semantics

- `conjunction`: fusion and intensification
- `sextile`: cooperative release
- `square`: friction and forced action
- `trine`: clean flow
- `opposition`: polarity and externalization

## Signal discipline

The doctrine does not permit direct trade entry from a single symbol such as:

- one sign
- one aspect
- one house
- one natal hit

Instead, the minimum valid chain is:

1. macro field
2. meso gate
3. micro trigger
4. minute window
5. only then entry or exit language

## Threshold policy

Thresholds are family-specific and doctrine-owned. They are no longer treated as random local constants in each EA.

Current profile owner:
- `DAL_AstroFamilyThresholds.mqh`

The JSON mirror for the Python/build side lives in:
- `tools/astro_feature_builder/astro_config.example.json`
