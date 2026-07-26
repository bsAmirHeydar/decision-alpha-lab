---
title: CH13 No Manual Preclassification Doctrine
project: EXP0017 Cycle Group Intermarket Divergence
chapter: 13
layer: strategy-architect answers
status: doctrine
---

# CH13 — No Manual Preclassification Doctrine

## 1. Definition

Manual preclassification means assigning quality, priority, weakness, strength, or trade preference to a signal before statistical evidence exists.

Chapter 13 rejects this at the base layer.

## 2. Forbidden preclassifications

Before statistical testing, the strategy must not say:

- this CG is stronger;
- this CG is weaker;
- this time window is superior;
- this time window is invalid;
- this symbol role is better;
- this symbol role is worse;
- buy is better than sell;
- sell is better than buy;
- near references are better;
- far references are better;
- fast reactions are better;
- deep hunts are better;
- shallow hunts are better;
- multi-CG overlap is better;
- isolated CG signals are better;
- high-volatility signals are better;
- low-volatility signals are better;
- news-time signals are worse;
- outside-cash signals are worse;
- cash-session signals are automatically executable with more risk.

These may become research hypotheses. They are not base laws.

## 3. Why this matters

If the project manually filters signals before collecting raw data, the statistics become contaminated.

The system would no longer measure the real edge of divergence. It would measure a human's prior opinion about divergence.

That is not acceptable for this project.

## 4. Base signal field

The base field includes all raw valid signals that satisfy:

- the correct intermarket divergence exists;
- the correct reference relationship exists;
- the signal has candle-close confirmation;
- the divergence is not invalidated by double hunt;
- the signal belongs to the current trading day.

Everything else is classification, not validity.

## 5. Preclassification versus postclassification

Preclassification is prohibited.

Postclassification is required.

| Layer | Meaning | Status |
|---|---|---|
| Preclassification | judging before data | prohibited |
| Description | recording signal attributes | required |
| Statistical classification | measuring outcomes by attribute | required |
| Rule creation | converting proven findings into rules | future phase |

## 6. Future exceptions

After testing, the strategy may eventually define:

- preferred CG families;
- weak CG families;
- preferred time windows;
- avoided time windows;
- symbol-role preferences;
- direction preferences;
- reference-distance filters;
- stop-pressure regimes;
- multi-CG confluence families;
- no-trade families.

But these are not allowed in the base layer.

## 7. Doctrine sentence

> Record every valid divergence first. Judge it only after the statistics can speak.
