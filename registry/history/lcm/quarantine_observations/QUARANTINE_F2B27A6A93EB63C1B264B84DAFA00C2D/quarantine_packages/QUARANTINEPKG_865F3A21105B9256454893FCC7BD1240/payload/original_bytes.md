# EXP0013 Astro Raw Sky Radical Redesign

This patch removes the fake-looking interpretive layer from the live dashboard and turns the UI into a raw sky-map cockpit.

## Principle

The dashboard should not invent market meaning.
It should show the astronomical state cleanly and let research decide what has distributional value.

The new rule is:

```text
No narrative score.
No causal claim.
No subjective clean/dirty labels.
Raw sky first, statistical validation later.
```

## What the dashboard now shows

### 1) Bodies

For each body:

- zodiac sign
- degree inside sign
- ecliptic longitude
- speed in longitude
- direct / retrograde state
- declination
- house placement if houses are available

### 2) Signs

Signs are shown as exact zodiac placement, not as a market interpretation.

Example:

```text
Sun  04.12 Can
Mars 13.80 Vir
```

### 3) Aspects

Aspects are shown by geometry only:

- pair
- nearest aspect class
- orb
- applying / separating
- exact angle

The aspects card is sorted by tightest orb.

### 4) Houses

House calculation is optional and requires a location.
If the CSV was built without location, the dashboard explicitly says houses are unavailable.

To enable houses in the Python builder:

```powershell
python tools\astro_feature_builder\astro_feature_builder.py `
  --start-broker "2026-01-01 00:00:00" `
  --end-broker "2026-06-25 23:59:00" `
  --timeframe-minutes 1 `
  --broker-gmt-offset-hours 3 `
  --house-lat 40.7128 `
  --house-lon -74.0060 `
  --house-system P `
  --out-csv "lab\03_experiments\EXP0013_astro_feature_store\output\astro_live_mql.csv"
```

For live bridge:

```powershell
python tools\astro_live_bridge\astro_live_bridge.py `
  --common-files "C:\Users\ABN\AppData\Roaming\MetaQuotes\Terminal\Common\Files" `
  --output-name "astro_live_mql.csv" `
  --broker-gmt-offset-hours 3 `
  --timeframe-minutes 1 `
  --history-hours 48 `
  --future-hours 6 `
  --refresh-seconds 60 `
  --house-lat 40.7128 `
  --house-lon -74.0060 `
  --house-system P
```

## Location note for houses

Houses are not geocentric like zodiac longitude.
They require an observer location.
For market research, choose one location deliberately and keep it fixed in the experiment.
Examples:

- exchange location
- broker server reference location
- chosen mundane chart reference location

Do not change the location mid-test, because that creates a different feature store.

## Canonical raw metrics

The dashboard includes only geometric/categorical metrics:

- lunar phase angle
- moon illumination proxy
- retrograde count/list
- out-of-bounds declination count/list
- tight aspect counts by orb threshold
- applying aspect count
- traditional essential dignity categories for classical planets

These are not market predictions. They are raw astrological descriptors for later distribution testing.

## UI modes

- OVERVIEW
- BODIES
- ASPECTS
- HOUSES
- METRICS
- MINIMIZE / EXPAND
- ORB STRIP ON / OFF

## Important

This dashboard is a raw observational layer. It must be paired with statistical validation:

- MAE_R
- pullback_depth_R
- path_efficiency
- bars_to_target
- volatility expansion
- regime-specific conditional distributions
