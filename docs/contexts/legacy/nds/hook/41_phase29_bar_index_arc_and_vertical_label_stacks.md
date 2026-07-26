# Phase 29 — Bar-Index Arc Timing and Vertical Label Stacks

## Goal

Fix two visual issues in the minimal Hook view:

1. Hook envelope curves should be laid out by candle progression rather than naive wall-clock interpolation, so the arc follows chart bar spacing more faithfully and does not visually break across session gaps.
2. Hook/branch labels should stack in cleaner vertical columns above peaks and below valleys instead of colliding on top of each other.

## Changes

### 1) Arc timing aligned to bar index

The Hook envelope renderer now prefers bar-index aligned interpolation.

- start, crown, and end anchor times are converted to chart bar shifts
- the curve is sampled along bar progression between those anchors
- each short trend segment is anchored on actual chart bar times

This makes the gray Hook envelope follow the chart's candle cadence more closely.

### 2) Stronger label clustering

Label stacking is now clustered by:

- side (above peaks / below valleys)
- bar distance
- optional time distance fallback
- price proximity

This makes labels form more deterministic vertical stacks.

## New config knobs

- `label_time_cluster_bars`
- `cycle_arc_align_to_bar_index`

## Default profile updates

The minimal Hook profile now defaults to:

- bar-index aligned Hook arcs enabled
- label clustering by 2 bars
- a slightly wider price cluster window
