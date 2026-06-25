# Astro Execution

This folder contains astro-only Expert Advisors for EXP0013.

## Contract

- They read the deterministic astro CSV through `DAL_AstroExcelCandleReader.mqh`.
- They use `DAL_AstroPureAstrologySignals.mqh`.
- They can journal paper actions through `DAL_AstroExecutionJournal.mqh`.
- They do not use market-structure, indicators, ATR, volume, or execution-family context.
- They emit pure astrology entry and exit language from transit, natal activation, and doctrinal astro metrics.
- They now read a hierarchical timing stack: macro field -> meso gate -> micro trigger -> minute window.
- They can load doctrine-owned threshold defaults from `DAL_AstroFamilyThresholds.mqh`.

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

### A0090 - Live Order Shell

File:
`A0090_AstroOrderShell.mq5`

Idea:

- read the same pure astro signal layer
- convert the astro state machine into optional broker actions
- preserve the same paper journal and doctrine trail while routing orders

Best use:

- final promotion shell after a family passes paper validation

## Usage

1. Build a deterministic CSV with `tools/astro_feature_builder/astro_feature_builder.py`.
2. If natal logic is required, include natal inputs during CSV generation.
3. Put the CSV where MQL5 can read it.
4. Run `A0001`, `A0002`, or `A0003` first and inspect the paper journal CSV.
5. Or generate the same paper journal research-side with `tools/astro_validation/astro_paper_family_runner.py`.
6. Validate the journal with `tools/astro_validation/astro_signal_validator.py`.
7. Promote a family into `A0090` only after the paper layer is stable.

## Important note

`A0001`, `A0002`, and `A0003` are still paper-first executors.

`A0090` includes broker routing, but it is disabled by default through `InpEnableLiveOrders=false` so the astro-only layer can still be audited before real execution is promoted.
