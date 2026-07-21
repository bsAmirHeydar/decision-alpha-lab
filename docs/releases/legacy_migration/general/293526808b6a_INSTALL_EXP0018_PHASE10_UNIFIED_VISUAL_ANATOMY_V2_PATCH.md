# Install EXP0018 Phase 10 — Unified Visual Anatomy v2

## Scope

This root-relative patch adds the canonical one-EA chart-facing visual suite for EXP0018. It composes the existing P08 immutable divergence renderer with Daily, Session, subcycle, 22.5-minute micro-quarter, p4-tail, gap, TDO, TWO, optional extended True Open, optional provisional-week, labels and legend layers.

## Install

Expand the ZIP into the repository root, run the Phase 10 validator, and compile:

`mql5/Experts/DayeTrader/EXP0018_Daye_Visual_Anatomy.mq5`

## Runtime rule

Attach the unified Expert to one chart. Keep standalone P08 and P09 Experts for diagnostics only; do not attach multiple chart-facing EXP0018 Experts to the same chart.

## Compile gate

- 0 errors
- 0 warnings
- embedded P08 and P10 self-tests PASS
- SPX and NDX target charts open with exact broker symbol names

## Default visual profile

- divergence lines: on
- Daily frame/boundaries/label: on
- A/L/N/P boxes/boundaries/labels: on
- a1-p4 boxes/boundaries/labels: on
- 22.5-minute boundaries: on
- 22.5-minute labels: on
- 17:00-18:00 gap: on
- TDO: on
- TWO: on
- extended Session True Opens: off
- provisional weekly boundaries: off

## Safety

No order, risk, position, network, model or execution capability is added.
