---
id: EXP0018-P06-GEOMETRY
title: "P06 Hunter Host-Bar Geometry"
type: implementation-note
status: implemented
project: EXP0018
phase: P06
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - exp0018
  - p06
  - confirmation
---

# Geometry contract

A confirmed result carries the Hunter symbol host candle:

- open;
- high;
- low;
- close;
- UTC open and close;
- deterministic host-bar ID.

For HIGH-side confirmation, the future line endpoint is the Hunter host candle high. For LOW-side confirmation, it is the Hunter host candle low. P06 records geometry but does not draw.
