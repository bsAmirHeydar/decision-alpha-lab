---
title: "LCM-10A — API Reference"
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
phase_id: LCM-10A
claim_ceiling: LCM_10A_REFERENCE_ONLY
---
# API Reference

## Purpose

The public API is the service build, package verification, installation verification, QA, schema validation, static validation and hash-ledger verification.

## Engineering contract

The service never imports legacy source modules or invokes broker APIs.

## Non-compensatory boundary

This artifact creates no promotion, runtime, live-order or capital authority. Missing evidence remains UNKNOWN, all legacy source bytes remain unchanged, and downstream use is restricted by the digest-bound LCM-10A handoff.
