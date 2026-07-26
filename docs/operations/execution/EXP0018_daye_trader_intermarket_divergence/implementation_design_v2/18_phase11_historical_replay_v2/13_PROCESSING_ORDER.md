---
id: EXP0018-P11-13_PROCESSING_ORDER
title: "Processing order"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Processing order

At every cursor: build as-of periods; resolve relationships; classify hunts; update/open candidates; finalize candidates whose target close is due; admit confirmed results into lifecycle; then apply the current observations to surviving references. This ordering matches live P07's result-before-observation semantics.
