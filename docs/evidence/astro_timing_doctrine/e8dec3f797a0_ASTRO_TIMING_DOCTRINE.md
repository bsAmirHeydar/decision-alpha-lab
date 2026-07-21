# ASTRO Timing Doctrine

This layer turns the raw astro map into a pure timing hierarchy with no price dependency.

## Hierarchy

### 1. Macro field

Purpose:
- decide whether the sky supports a directional background
- identify whether the background is expansive, compressive, or transitional

Inputs:
- Jupiter/Saturn soft and hard geometry
- Sun/Jupiter and Sun/Saturn support or pressure
- slow-body station and ingress risk
- elemental expansion/compression balance
- structural angular emphasis

Outputs:
- `macro_direction`
- `macro_bias_score`
- `macro_alignment_score`
- `macro_context`

### 2. Meso gate

Purpose:
- decide whether the macro field is actually usable
- test whether the active planets are angular, resonant, and synchronized

Inputs:
- body angularity by house
- transit/natal resonance
- declination parallels and contra-parallels
- clean-path support vs chop

Outputs:
- `meso_gate_score`
- `meso_angularity_score`
- `meso_resonance_score`
- `meso_context`

### 3. Micro trigger

Purpose:
- decide whether the lunar / near-term layer is releasing or obstructing movement

Inputs:
- Moon tempo
- Moon flow vs Moon pressure
- Moon boundary stress
- Mercury station/noise
- micro cleanliness

Outputs:
- `micro_trigger_score`
- `micro_release_score`
- `micro_context`

### 4. Minute window

Purpose:
- isolate the actionable M1 timing window
- separate release windows from exhaustion windows

Inputs:
- `m1_clean_window`
- `m1_dirty_window`
- `micro_trigger_score`
- `micro_release_score`
- Moon/Mars declination interaction
- Mercury station drag

Outputs:
- `minute_window_score`
- `minute_exhaustion_score`
- `minute_context`
- `trigger_state`

## Trigger states

- `standby`: no directional timing chain
- `armed`: macro and meso are aligned, but minute release is incomplete
- `trigger_ready`: macro, meso, micro, and minute window all align
- `timing_exit`: exhaustion or distortion dominates the minute layer

## Signal translation

The pure signal stack now uses this order:

1. macro direction
2. meso gate
3. micro trigger
4. minute window
5. only then entry / exit language

This keeps the astro logic hierarchical instead of mixing all factors flatly into one score.
