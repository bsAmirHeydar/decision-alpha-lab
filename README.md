# Decision Alpha Lab

**Hypothesis-driven systematic trading research, robustness analysis, and decision architecture.**

Decision Alpha Lab is a research environment for testing trading ideas **before they are allowed to become trading decisions**.

The central question is not simply whether a backtest is profitable. It is whether the underlying edge is understandable, whether its assumptions are durable, how it behaves across regimes, what can cause it to fail, and what level of capital—if any—should be trusted to it.

## If You Are Reviewing This Project

Start here:

1. **[Selected Research Findings](SELECTED_RESEARCH_FINDINGS.md)** — working conclusions, failure logic, and falsification conditions.
2. **[QA Report](QA_REPORT.json)** — current automated validation snapshot and unresolved blockers.
3. **[Current Program Status](docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/09_STATUS_AND_CONTROL/01_Current_Program_Status.md)** — current architecture/consolidation state and authority boundaries.
4. **[Architecture Program](docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/)** — deeper implementation and governance documentation.

## Evidence Snapshot

The published QA snapshot currently reports:

- **9,732 tests collected** across the repository;
- **0 pytest collection errors**;
- **166 targeted RTHP/consolidation tests passed** and **7 skipped**;
- engineering policy: **PASS**;
- UC04-W0 verifier: **PASS**;
- the full repository suite is explicitly marked **incomplete** because of four historical LFS-pointer blockers rather than being presented as fully green.

This distinction matters to the philosophy of the project: unresolved evidence is documented, not hidden behind a headline status.

## Research Model

The project separates four layers:

1. **Research assumptions** — why an edge should exist.
2. **Strategy logic** — how the idea is translated into objective rules.
3. **Risk & execution** — sizing, exposure, orders, costs, and portfolio interaction.
4. **Implementation authority** — ensuring research artifacts or AI-generated outputs do not gain execution or capital authority implicitly.

## Research Questions

Decision Alpha Lab is built around questions such as:

- Why should this edge exist?
- Is the edge structural, behavioral, execution-based, or sample-specific?
- Which hidden assumptions are embedded in the profitable period?
- What happens outside the original sample?
- How sensitive is the result to parameter changes?
- Does the edge survive across symbols, timeframes, and regimes?
- Is a drawdown expected behavior or evidence that the original hypothesis is failing?
- What is the effect of transaction costs, slippage, liquidity, and execution constraints?
- How should capital respond when confidence rises or falls?
- Which parts of the process should be automated, and which require human judgment?

## Validation Approach

The research process emphasizes:

- out-of-sample testing;
- walk-forward analysis;
- parameter sensitivity;
- cross-market validation;
- regime testing;
- stress testing;
- Monte Carlo analysis;
- failure-case analysis;
- drawdown interpretation;
- explicit separation of signal, execution, and risk logic.

## Selected Working Conclusions

The current research direction is summarized in [SELECTED_RESEARCH_FINDINGS.md](SELECTED_RESEARCH_FINDINGS.md). In short:

- trend-following has been more robust than many mean-reversion/counter-trend ideas in my own research universe;
- prediction-heavy systems often add hidden fragility and research-complexity cost;
- failure across markets, timeframes, and regimes is treated as evidence about hidden assumptions rather than an automatic reason to add parameters;
- capital suitability is evaluated through drawdown, recovery, payoff asymmetry, tail behavior, capacity, costs, portfolio interaction, and regime stability—not win rate alone.

These are working conclusions, not universal market claims, and each is written with conditions that could falsify it.

## Research Philosophy

A strong backtest is evidence, not proof.

The project prioritizes **robustness over optimization, mechanism over pattern-fitting, and survivability over headline returns**.

The goal is to identify strategies whose logic can still be defended when historical conditions change—and to reject strategies whose apparent edge disappears once hidden assumptions are exposed.

## Engineering Architecture

The repository contains substantial engineering work to make research **deterministic, reviewable, replayable, testable, and reversible**.

Research outputs and AI-generated artifacts are not allowed to acquire execution or capital authority implicitly. The architecture therefore uses explicit validation gates, evidence records, and authority boundaries rather than treating generated output as self-validating.

Canonical program documentation lives under:

`docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/`

## Status

Active research and platform-development project.

## Disclaimer

This repository documents research and experimental trading-system development. It is not financial advice and does not represent a claim of guaranteed profitability or audited investment performance.
