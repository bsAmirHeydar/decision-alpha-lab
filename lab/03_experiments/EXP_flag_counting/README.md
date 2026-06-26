# EXP_flag_counting — Unified F-counting experiment

This experiment replaces separate numbered F1/F2 modules with one integrated, reusable flag-counting module.

## Goal

Detect and visualize F-counting structures as a single grammar:

- F1: first flag structure from raw market nodes
- F2: continuation count that starts from the parent F1 internal `2`

## Core idea

F-counting is not a trade system yet. It is a structural counting experiment.

The detector outputs structured events containing:

```text
level: F1 or F2
direction: bullish or bearish
origin
leg1
waist
leg2
internal 1
internal 2
branch type
confirmation rebreak
status
```

## F2 rule

F2 starts from the parent F1 internal `2`:

```text
F2 origin = F1.N2
```

F2 can complete its branch either by normal internal `1/2` or by breaking its own waist:

```text
normal: leg2 -> 1 -> 2 -> leg2 rebreak
waist-break: 1 = F2 waist, 2 = node that breaks F2 waist
```

## Visual rule

Only the body is drawn:

```text
origin -> leg1
leg1 -> waist -> leg2
F1/F2 label
1 and 2 labels only
```

No lines are drawn after leg2.

## MQL5 entry point

```text
mql5/Experts/FlagCounting/FlagCountingExperiment.mq5
```
