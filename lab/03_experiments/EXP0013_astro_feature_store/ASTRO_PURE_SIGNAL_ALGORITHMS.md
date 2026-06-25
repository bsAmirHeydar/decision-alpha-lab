# EXP0013 Pure Astro Signal Algorithms

This document describes the current pure astro signal layer introduced for the first astro-only execution families.

## Scope

This layer is intentionally narrow:

- no market features
- no price structure
- no ATR
- no volatility from price

Everything below is derived from the astro row plus the existing astro path and fractal metrics.

## Inputs

The signal layer reads:

- raw body state from `DAL_AstroMapRow`
- raw aspect state from `DAL_AstroMapRow`
- natal activation state when present
- path/fractal metrics from `DAL_AstroFractalPathMetrics.mqh`
- canonical astro language fields from the CSV row

## Core outputs

`DAL_AstroPureSignal` produces:

- `long_bias_score`
- `short_bias_score`
- `trend_score`
- `path_score`
- `friction_score`
- `volatility_score`
- `natal_activation_score`
- `entry_score`
- `exit_score`
- `regime_name`
- `direction_name`
- `entry_signal`
- `exit_signal`
- `astro_language`
- `astro_trade_key`
- `sect_name`
- `benefic_support_score`
- `malefic_pressure_score`
- `angular_power_score`
- `house_lift_score`
- `house_drag_score`

## Long bias

The current long bias is a weighted combination of:

- Mars impulse
- Jupiter support
- Moon flow
- Mars element impulse
- Mars modality drive

Interpretation:
This is the expansion / drive side of the doctrine.

## Short bias

The current short bias is a weighted combination of:

- Saturn resistance
- Mars-Saturn friction
- Moon pressure
- inverse Jupiter support
- Moon water-reactive emphasis

Interpretation:
This is the compression / resistance side of the doctrine.

## Trend score

`trend_score` is the absolute distance between long bias and short bias.

Interpretation:
High trend score means the doctrine is less ambivalent about directional emphasis.

## Path score

`path_score` currently uses the clean-path output of the fractal/path stack.

Interpretation:
Direction alone is not enough. The signal engine also wants to know whether the sky suggests a cleaner or dirtier path.

## Friction score

`friction_score` currently uses chop risk from the fractal/path stack.

Interpretation:
This is the drag side of the doctrine and is especially important for exits and reduced-confidence entries.

## Volatility score

`volatility_score` is the average of:

- breakout follow-through
- raw pressure
- raw transition

Interpretation:
This is the astro-native pressure/activation field, not market volatility.

## Natal activation score

When natal data exists, the signal layer reads a small set of transit-to-natal activations:

- `t_sun__n_sun`
- `t_moon__n_moon`
- `t_mars__n_saturn`
- `t_jupiter__n_mars`

Each one is scored by orb tightness and applying emphasis.

Interpretation:
This is the first resonance layer, not a full natal doctrine yet.

## Sect-aware doctrine

The signal layer now classifies each row as:

- `day` sect when the Sun is above the horizon
- `night` sect when the Sun is below the horizon

This sect state is then used to rebalance the doctrine:

- Sun / Jupiter / Saturn are weighted more constructively in day sect
- Moon / Venus / Mars are weighted more constructively in night sect

Interpretation:
This does not predict price. It sharpens which planetary voices are considered more native to the current sky condition.

## Benefic / malefic balance

The doctrine now carries two explicit pressure channels:

- `benefic_support_score`
- `malefic_pressure_score`

`benefic_support_score` currently reads:

- Venus dignity
- Jupiter dignity
- their house lift
- their sect favorability

`malefic_pressure_score` currently reads:

- Mars dignity
- Saturn dignity
- their drag-heavy house placement
- inverse sect favorability

Interpretation:
This gives the signal engine a direct blessing/pressure layer in astrological language instead of burying everything inside path or timing scores.

## House doctrine layer

The signal layer now adds a distinct house-context surface:

- `angular_power_score`
- `house_lift_score`
- `house_drag_score`

Current doctrine:

- houses `10 / 1 / 11 / 9 / 5` are treated as more elevating or releasing
- houses `12 / 8 / 6 / 4` are treated as more compressive or obstructive
- angular houses still carry the highest raw power

Interpretation:
This sharpens the older broad angularity model by separating power from directionality and from drag.

## Entry score

`entry_score` is a weighted combination of:

- stronger side of directional bias
- path score
- volatility score
- natal activation score

Interpretation:
An entry is promoted only when direction, path, and activation are aligned strongly enough.

## Exit score

`exit_score` is a weighted combination of:

- friction score
- pullback risk
- dirty-window score

Interpretation:
This is the current hazard stack. It says the sky has become less supportive for holding.

## Direction state

Rules:

- if long bias exceeds short bias by a fixed margin, direction is `long`
- if short bias exceeds long bias by a fixed margin, direction is `short`
- otherwise direction is `flat`

## Regime state

Rules:

- high path and low friction -> `clean`
- very high volatility field -> `volatile`
- high friction -> `frictional`
- otherwise -> `mixed`

## Entry state

Rules:

- `enter_long` when direction is long and entry score is high enough
- `enter_short` when direction is short and entry score is high enough
- otherwise `wait`

## Exit state

Rules:

- `exit_or_reduce` when the exit score crosses its hazard threshold
- otherwise `hold`

## Family behavior

### A0001

Uses the pure signal layer directly.

Best for:
- transit-only doctrine
- baseline directional testing

### A0002

Adds a natal activation gate on top of the same signal layer.

Best for:
- natal/inception studies
- resonance doctrine

### A0003

Reads friction as the primary organizing principle.

Best for:
- pressure doctrine
- adverse-path studies

## Current limitations

- body universe is still conservative
- natal activation pairs are still a starter set
- thresholds are still hand-authored and require validation
- MetaEditor compile verification has not yet been run inside this turn
- live order routing exists as `A0090`, but production safeguards and family promotion still require validation
- house doctrine is now active, but family-specific house meanings can still be sharpened further

## Next algorithmic expansions

- family-specific house meanings and cadence maps
- stronger natal house activation logic
- family-specific threshold configs
