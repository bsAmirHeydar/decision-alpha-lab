# System Architecture

Decision Alpha Lab follows a strict separation between research and execution.

## Python

Responsible for:

- Data engineering
- Feature extraction
- Structural node analysis
- Energy estimation
- Regime detection
- Machine learning
- Backtesting
- Alpha validation

## MQL5

Responsible for:

- Signal execution
- Broker communication
- Order management
- Trade logging
- Fail-safe procedures

## Design Principle

Python is the brain.

MQL5 is the execution layer.

Research logic must never reside inside the execution engine.