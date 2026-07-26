---
id: SAED-4FD7A87749
title: "P5 — Tight-Precision High-Hit Fixed"
type: architecture
status: canonical
domain: strategy-factory-setup-ai-edge-discovery
version: 1.0.0
created: 2026-07-13
updated: 2026-07-13
tags:
  - strategy-factory
  - setup-factory
  - ai-training
  - payoff-profile
  - p5
  - precision
---

# P5 — Tight-Precision High-Hit Fixed

## Mission

Maximize calibrated hit probability with a tight local invalidation and net reward of at least 1R. The source of advantage must be precise timing, not future leakage or optimistic execution.

## Suitable Triggers

- exact reclaim;
- sweep-and-close;
- lower-timeframe structural shift;
- point-2 or waist limit;
- rejection plus confirmation;
- immediate micro-breakout after Context completion.

## Sensitivities

This profile is extremely sensitive to spread, slippage, feed differences, timestamp alignment, bar ordering, stop levels and entry latency.

## Mandatory Stress

- spread multiples;
- one-tick and one-bar entry delay;
- cross-feed replay;
- stop-distance perturbation;
- price normalization;
- long/short side parity;
- broker stop-level checks;
- false precision analysis.

## Rejection Rule

A high historical hit rate with fragile entry-price sensitivity is not promoted.
