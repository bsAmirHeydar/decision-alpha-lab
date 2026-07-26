# Structural Hook vs Geometric Cycle Policy

The user wants two possible post-F3 recognition modes.

## Mode 1 — Structural only

Only Hooks with full nodes, sequences, and closed terminal state are shown.

This is strict and cleaner.

## Mode 2 — Structural or 80% geometric

A post-F3 cycle can be accepted if it reaches the configured 80% completion threshold, even if no full sequence was produced.

This mode is useful for studying small post-F3 cycles.

## Hard rule

Geometric cycles must never cause all raw sequences to appear.

Valid-only rendering still draws only selected valid families.
