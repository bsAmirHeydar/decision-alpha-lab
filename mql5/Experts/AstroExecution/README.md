# Astro Execution

This folder contains astro-only Expert Advisors for EXP0013.

## Contract

- They read the deterministic astro CSV through `DAL_AstroExcelCandleReader.mqh`.
- They use `DAL_AstroPureAstrologySignals.mqh`.
- They do not use market-structure, indicators, ATR, volume, or execution-family context.
- They emit pure astrology entry and exit language from transit, natal activation, and doctrinal astro metrics.

## Execution families

### A0001 - Transit Trend Pulse

File:
`A0001_AstroTransitTrendPulse.mq5`

Idea:

- read the pure astro signal layer
- use transit direction bias and path quality
- produce a long/short/wait state from transit-only astro doctrine

Best use:

- baseline transit family
- no natal dependency

### A0002 - Natal Resonance

File:
`A0002_AstroNatalResonanceExecutor.mq5`

Idea:

- require natal-enabled CSV
- gate entry by transit-to-natal activation strength
- only promote the underlying astro direction when natal resonance is strong enough

Best use:

- asset inception or reference-chart models

### A0003 - Friction Polarity

File:
`A0003_AstroFrictionPolarityExecutor.mq5`

Idea:

- read pure astro friction metrics
- identify pressure windows where polarity is still directional
- produce friction-aware directional language and exit emphasis

Best use:

- dirty-path or pressure-dominated doctrine variants

## Usage

1. Build a deterministic CSV with `tools/astro_feature_builder/astro_feature_builder.py`.
2. If natal logic is required, include natal inputs during CSV generation.
3. Put the CSV where MQL5 can read it.
4. Attach one EA family at a time.
5. Audit the printed state before any order-sending logic is added.

## Important note

These EAs currently behave as signal executors and state printers.

They are intentionally separated from broker order logic so the astro-only layer can be audited before real execution is promoted.
