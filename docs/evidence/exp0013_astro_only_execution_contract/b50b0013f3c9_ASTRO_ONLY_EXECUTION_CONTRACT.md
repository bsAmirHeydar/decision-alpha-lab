# EXP0013 Astro-Only Execution Contract

This document defines the purity rules for turning EXP0013 from an astro data store into an astro-only execution program.

## 1. Purity contract

Allowed inputs:

- transit planetary state
- natal or inception chart state
- transit-to-transit aspects
- transit-to-natal aspects
- houses, angles, and angularity
- declination, parallels, contra-parallels
- dignity, element, modality, retrograde, station, ingress
- moon phase and illumination

Forbidden inputs:

- price structure
- ATR
- market session filters
- volume
- indicator outputs
- support/resistance from market data
- any market-derived target/stop logic inside the pure astro signal engine

The pure astro layer must be explainable entirely in astrological language.

## 2. Time contract

Every row must be knowable at candle open.

- `broker_time` is the lookup key in MQL5.
- `utc_time` is already stored by Python.
- MQL5 must not apply a second time shift.
- Applying/separating must be derived from instantaneous planetary motion, not future bars.

## 3. Natal contract

Natal support is optional but must be fixed and explicit.

Required natal metadata:

- natal local datetime
- natal UTC offset
- natal latitude/longitude if houses are enabled
- natal house system
- natal label

Valid natal anchors:

- asset inception
- exchange inception
- contract first trade
- ETF listing chart
- research reference chart

The natal anchor is part of the doctrine. Changing the anchor means changing the model.

## 4. Doctrine contract

Before any execution result is trusted, the doctrine must be frozen:

- tropical or sidereal
- geocentric basis
- house system
- orb policy
- aspect family
- body universe
- natal anchor choice

These values must travel with the generated CSV or the run configuration.

## 5. Feature contract

The pipeline must preserve three levels:

- raw state
- canonical astro language
- execution key

Raw state is archival.
Canonical language is research-readable.
Execution key is compact enough for repeated live decisions.

## 6. Entry contract

An entry is valid only when it is produced by explicit astro state logic:

- direction state
- path state
- activation state
- confidence state

No discretionary interpretation is allowed at runtime.

## 7. Exit contract

Exits must also be astro-native.

Examples:

- direction collapse
- friction spike
- transition spike
- natal activation completion
- phase boundary regime shift
- station-window hazard

## 8. Validation contract

Pure astro does not mean unvalidated.

Required before promoting any family:

- walk-forward validation
- permutation/placebo baselines
- out-of-sample stability
- sample floor
- doctrine stability
- family-specific audit

## 9. Logging contract

Every signal must be auditable:

- row timestamp
- doctrine id
- natal label
- direction
- regime
- entry/exit signal
- astro key
- top contributing astro states

## 10. Production contract

The production path is:

1. deterministic CSV build
2. MQL row lookup
3. pure astro language
4. explicit entry/exit state
5. paper execution
6. live execution

Do not jump from a raw panel directly to real orders.
