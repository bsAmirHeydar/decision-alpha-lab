# Decision Alpha Lab

**A Python/MQL quantitative research framework for hypothesis-based systematic trading decisions.**

Decision Alpha Lab is a personal quantitative research laboratory for turning trading ideas into testable assumptions, measurable experiments, validation reports, and eventually execution-ready logic.

The project is built around one core principle: **a trading system should not be treated only as a black-box backtest.** Every edge depends on assumptions about market behavior. Those assumptions should be isolated, measured, challenged, validated, monitored, and only then translated into execution logic.

---

## Core Idea

Most strategy development starts with an idea, converts it directly into a trading rule, and then backtests the complete system. This creates a major problem: if the strategy later fails or enters a deep drawdown, it is hard to know whether the original edge is still alive or whether the underlying assumption has broken.

Decision Alpha Lab takes a different path:

1. Start with a market observation.
2. Convert the observation into a formal hypothesis.
3. Define measurable assumptions.
4. Build experiments around those assumptions.
5. Compare results against baselines and random controls.
6. Validate across symbols, timeframes, and market periods.
7. Monitor whether the edge remains valid over time.
8. Only then move toward execution logic.

---

## Current Research Theme

The current research program is focused on **structural highs and lows as decision nodes**.

The central hypothesis is that structurally defined highs and lows may contain statistically distinguishable information about future market behavior compared with arbitrary price locations.

The lab investigates questions such as:

- Do structural highs/lows behave differently from random locations?
- Do market reactions around structural nodes show measurable persistence, rejection, congestion, or breakout behavior?
- Can node revisitation and node consumption be measured objectively?
- Can structural node behavior help detect regime transitions?
- Can these concepts support systematic alpha extraction without overfitting?

---

## Architecture

The architecture separates research from execution.

### Python Research Layer

Python is used for:

- Data engineering
- Market data caching
- Feature extraction
- Structural node detection
- Statistical experiments
- Metric generation
- Backtesting and validation
- Research reports
- Edge monitoring

### MQL / MetaTrader Execution Layer

MQL5 / MetaTrader is intended for:

- Chart-based inspection
- Execution-style testing
- Broker-side integration
- Order management
- Trade logging
- Fail-safe execution procedures

**Design principle:** Python is the research brain; MQL is the execution layer.

---

## Repository Structure

```text
.
├── data/                         # Data documentation and dataset notes
├── docs/                         # Architecture, principles, glossary, roadmap
├── lab/
│   ├── 01_observation/            # Market observations
│   ├── 02_hypotheses/             # Formal hypotheses
│   ├── 03_experiments/            # Experiment definitions and reports
│   ├── 04_analysis/               # Analysis notes
│   ├── 05_validation/             # Validation reports
│   ├── 06_production/             # Signal-production candidates
│   ├── 07_monitoring/             # Edge monitoring metrics
│   ├── 08_archive/                # Failed / rejected / retired ideas
│   ├── 09_execution/              # Bridge, logging, MQL5 execution docs
│   ├── 10_infrastructure/         # CI, config, data, tests, utilities
│   └── core/                      # Core reusable components
├── papers/                        # Research notes and written papers
├── registry/                      # YAML registries for experiments, hypotheses, signals, validations
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

---

## Core Components

### `CP0000_market_data`

Market data infrastructure with:

- `MT5Connector` for MetaTrader 5 data access
- `MarketDataEngine` for cached market data retrieval
- `ParquetStore` for local Parquet-based storage
- MQL-style price accessors such as `iOpen`, `iHigh`, `iLow`, and `iClose`
- Sync logic that refreshes the latest candle while preserving historical cache integrity

### `CP0001_structural_nodes`

Structural node research component with:

- `L_Rule` structural high/low detector
- Confirmed/unconfirmed node handling
- Incremental rebuild logic
- Node caching by symbol, timeframe, and detector configuration
- Relative Territory Volatility metric (`M0001RTV`) for measuring behavior around structural nodes

---

## Research Workflow

```text
Observation → Hypothesis → Experiment → Analysis → Validation → Signal Candidate → Monitoring → Execution
```

This workflow is designed to prevent premature strategy deployment and reduce black-box overfitting.

---

## Key Research Objects

### Observation

A qualitative or practical market observation that deserves formal investigation.

### Hypothesis

A falsifiable claim derived from an observation.

### Experiment

A reproducible test designed to evaluate a hypothesis.

### Validation

A higher-standard review of whether an effect survives different markets, periods, parameters, and baselines.

### Signal Candidate

A validated research object that may eventually become trading logic.

### Monitoring

Ongoing measurement of whether the assumptions behind an edge remain valid.

---

## Why This Matters

If a trading system enters a deep drawdown, the important question is not only whether the backtest looked good. The deeper questions are:

- Is the underlying edge still valid?
- Has the market regime changed?
- Did the assumptions behind the strategy break down?
- Is the drawdown within expected behavior?
- Should the system continue, pause, or be redesigned?

Decision Alpha Lab is designed to make those questions measurable instead of emotional.

---

## Status

Active research project. The current focus is building the research architecture, improving the structural node research pipeline, documenting hypotheses, and expanding validation workflows.

---

## Disclaimer

This repository is for quantitative research and educational purposes only. It is not financial advice and does not provide trading recommendations.
