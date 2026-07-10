---
id: AIEOS2-C80D38133017
title: "Causal Time and Availability"
type: standard
status: active
domain: alpha-lab-standard
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - alpha-lab-standard
---
# Causal Time and Availability

Every time-dependent field declares event time, observation time, availability time, timezone, and decision cutoff. “Historical” does not mean “available at the time.”

A feature is legal for decision/model input only if its availability timestamp is at or before the sample’s decision timestamp. Full-day ranges, future extrema, final labels, and full-history rankings are common leakage sources.
