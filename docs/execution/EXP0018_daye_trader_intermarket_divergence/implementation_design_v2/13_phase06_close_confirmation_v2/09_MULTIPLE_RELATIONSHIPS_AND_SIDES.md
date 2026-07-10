---
id: EXP0018-P06-MULTI
title: "P06 Multiple Relationships and Sides"
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

# Independence

Identity includes the P05 observation, which already includes relationship, current period, reference period, and HIGH/LOW side. Therefore:

- multiple relationship types may confirm in one host candle;
- HIGH and LOW can both confirm in one host candle;
- one invalidated candidate does not suppress another;
- major and minor relationships use the same confirmation law.
