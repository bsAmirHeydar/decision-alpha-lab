---
title: "Compile DAG at Startup"
status: accepted
phase: 07
---
# Compile DAG at Startup

## Decision

Dependency resolution, cycle detection and graph hashing occur before runtime starts.

## Consequence

The central engine remains deterministic, auditable and reusable across future anatomy plugins.
