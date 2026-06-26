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
- The pure signal layer now includes sect-aware doctrine context plus benefic / malefic and house lift / drag scores.

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

### A0004 - Sect Benefic Pressure

File:
`A0004_AstroSectBeneficPressureExecutor.mq5`

Idea:

- read the sect-aware doctrine layer directly
- require either benefic release with house lift dominance or malefic pressure with house drag dominance
- only promote entries when sect/doctrine pressure and the existing directional signal agree

Best use:

- sect-driven doctrine
- benefic vs malefic pressure studies
- house-lift / house-drag timing variants

### A0005 - Moon Timing Window

File:
`A0005_AstroMoonTimingWindowExecutor.mq5`

Idea:

- read the lunar phase bucket plus micro/minute release scores
- only allow entries when lunar phase and minute release are synchronized
- use waxing release for long-side timing and waning/full pressure for short-side timing

Best use:

- lunar timing studies
- minute-window release testing
- fast trigger filtering on top of the existing directional doctrine

### A0006 - Angular Activation

File:
`A0006_AstroAngularActivationExecutor.mq5`

Idea:

- read angular power together with the minute trigger window
- require the direction to be confirmed by house lift dominance for longs or house drag dominance for shorts
- only promote entries when angular release / pressure is active enough to move from broad doctrine into executable timing

Best use:

- angularity-driven timing studies
- macro-to-micro compression around angles and houses
- filtering directional doctrine into sharper entry windows

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
4. Run `A0001`, `A0002`, `A0003`, `A0004`, `A0005`, or `A0006` first and inspect the paper journal CSV.
5. Or generate the same paper journal research-side with `tools/astro_validation/astro_paper_family_runner.py`.
6. Batch the journals and validation reports with `tools/astro_validation/astro_family_validation_suite.py`.
7. Export multi-family entry / exit workbooks without Strategy Tester through `tools/astro_validation/astro_family_entry_exit_excel_suite.py`.
8. Validate any single journal with `tools/astro_validation/astro_signal_validator.py`.
9. Promote a family into `A0090` only after the paper layer is stable.

## Important note

`A0001`, `A0002`, `A0003`, `A0004`, `A0005`, and `A0006` are still paper-first executors.

`A0090` includes broker routing, but it is disabled by default through `InpEnableLiveOrders=false` so the astro-only layer can still be audited before real execution is promoted.
