---
type: strategy-factory-document
status: canonical
title: "Multiple Testing and False-Discovery Control"
tags:
  - strategy-factory
---

# Multiple Testing and False-Discovery Control

The factory assumes many attractive results will appear by chance because it searches many anatomies, buckets, policies, targets, and models.

## Trial universe

Count all materially different tests, including abandoned ones. Group related tests into families. Benjamini-Hochberg controls false-discovery rate for exploratory screens; stricter family-wise controls may be used for narrow confirmation.

## Selection-aware reporting

Publish raw p-values, adjusted q-values, number of trials, selection metric, and whether the hypothesis was predeclared. A bucket that loses significance after correction is not deleted; it remains an exploratory lead.

## Economic filter

Correction is necessary but not sufficient. A statistically credible effect still needs positive net expectancy, stability, and execution capacity.

