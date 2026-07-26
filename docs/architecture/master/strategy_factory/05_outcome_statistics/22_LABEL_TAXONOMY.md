---
type: strategy-factory-document
status: canonical
title: "Label Taxonomy"
tags:
  - strategy-factory
---

# Label Taxonomy

A single win/loss label discards too much information. The factory supports multiple tasks without allowing labels to leak into features.

## Classification

Examples: filled, net positive, target before stop, tail achieved, survived initial risk, or acceptable path quality. Thresholds are versioned and chosen from trading objectives, not tuned repeatedly on the full sample.

## Regression

Predict net R, MFE, MAE, time to fill, holding time, or cost. Regression preserves magnitude and supports expected-value decisions but is sensitive to tails and should use robust diagnostics.

## Ranking

For each event, rank candidate policies. Ranking is often more useful than predicting whether the anatomy itself is valid because it directly selects entry/stop/exit geometry while retaining a skip option.

## Survival and competing risk

Model time until stop, target, expiry, or structural invalidation. Survival labels are appropriate when timing matters and censoring is common. Label end time must be explicit for purge.

