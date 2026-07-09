# 05 — Sample Time Modes

## Purpose

Before Forex Factory integration, the sample tape must be able to validate every downstream assumption. Stage 03 adds sample anchoring modes.

## Modes

| Mode | Value | Meaning |
|---|---:|---|
| Broker | 0 | Sample HH:MM means broker chart time |
| Source | 1 | Sample HH:MM means source/calendar time and is converted |
| UTC | 2 | Sample HH:MM means UTC and is converted |

## Default

Broker mode remains default so UI testing is predictable.

## Why this matters

Stage 04/05/07 can test rendering and alert behavior without waiting for Forex Factory. Stage 08 can switch sample mode to source/UTC to test parser behavior against the same store contract.
