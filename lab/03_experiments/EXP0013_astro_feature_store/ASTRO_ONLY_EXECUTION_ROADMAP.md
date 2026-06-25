# EXP0013 Astro-Only Execution Roadmap

This roadmap turns the current EXP0013 stack into a complete astro-only execution program.

## Phase 1 - Doctrine freeze

Goal:
Lock the astrological worldview so feature definitions stop drifting.

Tasks:

- choose tropical vs sidereal
- choose body universe
- choose house system
- choose orb family and max orb per class
- choose natal anchor families
- assign a doctrine id to each generated CSV

Deliverable:
`doctrine_v1` document plus config snapshot.

## Phase 2 - Raw data completion

Goal:
Capture every deterministic astro state we want to reason about.

Tasks:

- transit raw bodies
- natal raw bodies
- transit-to-transit aspects
- transit-to-natal aspects
- house cusps and angularity
- declination and OOB state
- parallels/contra-parallels
- ingress/station windows

Deliverable:
stable CSV schema with versioning.

## Phase 3 - Canonical astro language

Goal:
Translate raw numbers into explicit astro-native phrases.

Examples:

- `mars=direct_fast_fire_house10`
- `moon=waning_oob_house8`
- `t_mars__n_saturn=square_tight_applying`
- `jupiter_saturn=trine_close_separating`

Deliverable:
language builder functions and execution keys.

## Phase 4 - Astro metrics

Goal:
Create state metrics without market contamination.

Families:

- direction bias
- path cleanliness
- friction
- volatility pressure
- transition hazard
- natal resonance
- angular emphasis

Deliverable:
normalized scores and named regimes.

## Phase 5 - Strategy families

Goal:
Separate distinct astro execution ideas instead of blending them too early.

Families now in repo:

- `A0001` transit trend pulse
- `A0002` natal resonance
- `A0003` friction polarity

Candidate next families:

- moon timing window
- angular activation family
- station transition family
- benefic/malefic pressure family

Deliverable:
one README plus one config surface per family.

## Phase 6 - Entry/exit state machine

Goal:
Convert metrics into executable state.

State chain:

- wait
- armed
- enter
- hold
- reduce
- exit

Deliverable:
explicit rules with no discretionary interpretation.

## Phase 7 - Paper execution

Goal:
Run every family without sending orders.

Tasks:

- log every signal
- record entry score and exit score
- record hold duration
- record opposite-signal collisions

Deliverable:
signal journals for each family.

## Phase 8 - Validation

Goal:
Prove that a family is not storytelling.

Required tests:

- walk-forward
- shuffled baseline
- doctrine stability
- natal-anchor stability
- hold-duration sensitivity
- threshold sensitivity

Deliverable:
promotion or rejection decision per family.

## Phase 9 - Live execution

Goal:
Promote only validated families into order-sending EAs.

Tasks:

- wire paper family to order engine
- preserve astro-only signal layer
- keep full signal audit trail

Deliverable:
live-ready astro-only execution family.

## Current repo status

Already present:

- natal-aware Python builder
- live bridge with natal pass-through
- expanded MQL astro row schema
- raw/natal/signal tabs in dashboard
- pure astro signal layer
- three astro-only execution EAs

Still required:

- family-by-family validation reports from real journal runs
- compile artifact verification for the astro execution families

Now implemented in repo:

- doctrine id/version fields in builder, live bridge, CSV, and MQL reader
- declination parallels / contra-parallels and OOB state
- hierarchical timing doctrine from macro field to minute trigger
- doctrine-owned family threshold layer
- sect-aware doctrine context with benefic / malefic and house lift / drag
- explicit astro execution state machine
- paper execution journal schema and journal writers
- Python paper family runner under `tools/astro_validation/astro_paper_family_runner.py`
- validation tooling scaffold under `tools/astro_validation`
- batch family validation suite under `tools/astro_validation/astro_family_validation_suite.py`
- live order shell `A0090_AstroOrderShell.mq5`
- MetaEditor compile harness under `tools/compile_exp0013_astro_suite.ps1`
