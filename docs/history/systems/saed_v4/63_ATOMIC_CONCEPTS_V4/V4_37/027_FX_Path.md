---
title: "V4-37 Atomic Concept 027 — FX Path"
status: accepted-reference
phase: SAED_V4_37
version: 1.0.0
updated: 2026-07-17
tags: [saed-v4, v4-37, atomic-concept]
---
# SAED V4-37 Atomic Concept — FX Path

## Definition

**FX Path** is an atomic portfolio or execution-economics concept. It has one deterministic responsibility and a closed evidence shape so that economics can be audited independently from signal discovery, treatment selection and live execution.

## Invariants

The concept is known-time, content-addressed, currency-aware, executable-price-aware and bounded by frozen portfolio constraints. It cannot silently omit spread, fees, carry, impact, liquidity, dependence or concentration. It cannot route an order, activate capital, mutate UCEE, promote a model or authorize production.

## Validation

Golden fixtures, negative fixtures, mutation tests, accounting identities, exact replay, hash verification, schema closure, portfolio limits, stress scenarios, independent review and static MQL5 mirrors validate the concept. Repository evidence is explicitly separated from external MetaEditor, terminal, broker and live-capital evidence.

## Failure behavior

Invalid or incomplete evidence causes abstention, rejection, de-allocation or constraint reduction. The system preserves the baseline and emits a visible failure rather than manufacturing an executable decision.

## Claim ceiling

The concept supports a synthetic research-only reference implementation. It does not establish real market impact calibration, broker parity, prospective execution quality, production authorization or live-trading fitness.
