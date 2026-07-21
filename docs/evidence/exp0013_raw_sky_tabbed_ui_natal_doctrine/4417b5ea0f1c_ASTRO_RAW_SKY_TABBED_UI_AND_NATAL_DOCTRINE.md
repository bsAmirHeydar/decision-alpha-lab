# EXP0013 Raw Sky Tabbed UI and Natal Doctrine

This patch cleans the raw sky dashboard by turning the UI into a tabbed cockpit.

## Why the previous raw dashboard was cluttered

The previous version tried to show too many layers at the same time:

- bodies
- outer bodies
- aspects
- houses
- metrics
- dignity
- diagnostics
- orb strip

That is useful for debugging, but bad for actual live reading.

## V14 UI principle

The dashboard now uses a strict separation:

```text
Header = status and navigation only
Main panel = one active analytical layer
Side panel = diagnostics only
```

Instead of showing everything at once, the raw data is accessible through tabs:

- OVERVIEW
- BODIES
- ASPECTS
- HOUSES
- METRICS
- MINIMIZE
- RELOAD

## Sections

### OVERVIEW

A compact snapshot:

- Sun / Moon
- Mercury / Venus
- Mars / Jupiter
- Saturn
- Moon phase
- ASC / MC if houses are available
- canonical metrics
- tightest aspects

Use this for the first glance.

### BODIES

The full planetary table:

- body
- zodiac position
- speed and direct/retrograde state
- declination
- house placement

This is the raw sky map at the candle time.

### ASPECTS

Aspect geometry sorted by tightest orb:

- pair
- aspect type
- orb
- applying/separating
- exact angular distance

This is the cleanest mathematical part of the sky-state layer.

### HOUSES

Only valid if the CSV was generated with a fixed research location:

- house system
- latitude/longitude
- ASC
- MC
- house cusps
- body house placement

Do not compare house features across different locations unless location itself is part of the hypothesis.

### METRICS

Canonical raw features only:

- Moon phase bucket
- Moon phase angle
- illumination proxy
- retrograde count/list
- out-of-bounds declination count/list
- tight aspects count
- applying aspect count
- traditional essential dignity categories

No market interpretation is made inside this layer.

## How to analyze astrology without pseudo-interpretation

The correct research order is:

```text
1. Raw sky state
2. Canonical astro features
3. Market outcome labels
4. Conditional distribution tests
5. Only then: interpretation
```

Do not start with:

```text
Saturn means X, therefore price will do Y.
```

Start with:

```text
When Saturn is retrograde / angular / in hard applying aspect / in a certain dignity,
how does the distribution of MAE_R, pullback_depth_R, path_efficiency,
volatility expansion, and follow-through change?
```

## Transit-only vs Natal + Transit

### Transit-only

Transit-only means:

```text
What is the sky state at this candle?
```

It is valid for global timing, sky weather, and event-state research.
It does not need a natal chart.

Useful for:

- general market timing
- global macro sky-state
- volatility conditions
- phase/aspect clustering
- path-quality conditioning

### Natal + Transit

Natal + transit means:

```text
How does the current sky activate the birth chart / inception chart of the asset, market, contract, exchange, or system?
```

This is a different model and requires a fixed natal anchor.

Possible natal anchors:

- asset launch date
- exchange founding/opening chart
- contract first-trade timestamp
- ETF listing chart
- currency regime inception
- gold futures contract reference chart
- broker/instrument data genesis if the research is broker-specific

### For markets

Transit-only is not wrong. It is the baseline.

But if we want a serious classical/financial astrology model, the stronger architecture is:

```text
Layer 1: Transit-only sky weather
Layer 2: Natal chart of the instrument/market
Layer 3: Transit-to-natal activations
Layer 4: Progressed/directed layers only if justified later
```

## Recommended next step

Do not immediately add interpretive scores.

First add natal support as a separate optional feature store:

```text
natal_body_lon
natal_house_cusps
transit_to_natal_aspects
transit_planet_to_natal_angle
orb
applying/separating
natal house activated
```

Then test whether natal activation features improve distributional separation beyond transit-only features.
