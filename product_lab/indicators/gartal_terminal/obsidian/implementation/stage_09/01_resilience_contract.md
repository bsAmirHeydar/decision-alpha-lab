# 01 — Resilience Contract

## Responsibility

`GartalNewsResilience.mqh` decides whether a data source is usable. It does not know how to draw, alert, or parse events.

## Inputs

- raw calendar payload
- source configuration
- runtime diagnostics
- cache metadata

## Outputs

- source quality
- cache state
- sanity summary
- failover count
- readable dashboard diagnostics

## Non-Negotiable Rule

A payload may not enter the parser unless it passes `GT_CheckRawCalendarHealth()`.
