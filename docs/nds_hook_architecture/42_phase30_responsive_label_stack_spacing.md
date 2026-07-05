# Phase 30 — Responsive Label Stack Spacing

## Problem

Fixed label offsets and fixed stack-step distances become visually wrong across timeframes:

- on smaller timeframes they can be too wide;
- on larger timeframes they can be too tight;
- crowded Hook zones need spacing that adapts to the local candle scale.

## Goal

Make Hook/branch label stacking responsive instead of relying on one dry absolute number.

## What changed

### 1) Dynamic spacing from local candle range

The label renderer now estimates the average candle range around the anchor node using a configurable local lookback window.

From that local range it derives:

- base offset distance from the node;
- per-stack vertical step distance.

### 2) Clamp bounds

Responsive values are clamped between configurable minima and maxima so spacing does not become absurdly tiny or huge.

### 3) Manual values remain floors

The existing fixed-point settings still exist, but now they act as floor values. If the responsive estimate is larger, the renderer uses the larger value.

## New config knobs

- `responsive_label_offsets`
- `responsive_label_lookback_bars`
- `responsive_label_min_offset_points`
- `responsive_label_max_offset_points`
- `responsive_label_min_step_points`
- `responsive_label_max_step_points`
- `responsive_label_offset_range_ratio`
- `responsive_label_step_range_ratio`

## Result

Label stacks above peaks and below valleys scale more naturally with timeframe and local market volatility.
