---
title: SAED V4-41 — Retirement Candidate Compilation
status: accepted-reference
version: 1.0.0
updated: 2026-07-17
phase: SAED_V4_41
tags: [saed-v4, v4-41, delivery]
---
# Retirement Candidate Compilation

## Purpose

This delivery defines **Retirement Candidate Compilation** as an implementation-grade slice of SAED V4-41 Continuous Surveillance and Retirement. It closes the reference roadmap by turning every immutable Context Cell, model generation, treatment universe, runtime bundle and route into a continuously observable, fail-closed and explicitly retireable governed object. No authority is inferred from deployment, connectivity, alert severity or control-plane reachability.

## Contract

The contract is closed-schema and known-time bounded. It binds policy version, metric identity, surveillance window, sample support, baseline value, current value, detector evidence, persistence, alert severity, decision trace, incident state, containment action, dependency impact, approvals, replacement, tombstone, archive and verification. Unknown fields, future-suffix evidence, missing fleet coverage, duplicate observations, cross-tenant impact, silent threshold changes, insufficient approvals or incomplete replacement fail closed.

## Engineering behavior

The reference implementation surveils 128 immutable Context Cells over twelve metric families and six ordered windows. Threshold, EWMA, CUSUM and Page-Hinkley mirrors feed a persistent-breach detector ensemble. Alert fusion produces CONTINUE, WATCH, RESTRICT, QUARANTINE or RETIRE_CANDIDATE without live side effects. Incidents are hash-chained. Retirement requires independent approvals, same-tenant replacement, dependency impact review, route revocation, immutable tombstone, evidence archive and post-retirement verification.

## Evidence and authority

All included observations and retirements are synthetic reference evidence. They demonstrate deterministic mechanics, not actual production telemetry, model decay, broker route revocation, MetaEditor parity, operational incident response or production authorization. Live orders, capital activation, automatic live actions, cross-tenant actions, silent threshold changes and reinstatement without a new qualification cycle remain prohibited.

## Closure

This phase closes the numbered SAED V4 reference roadmap. It hands the system to continuous operations and external qualification rather than inventing another architecture phase to bypass open operational gates.
