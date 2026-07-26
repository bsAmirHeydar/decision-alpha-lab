---
id: EXP0018-P05-PERFORMANCE
title: "P05 Performance and Refresh"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Performance

Classification is linear in the number of P04 resolutions and bounded by `maximum_observations_to_publish`. Each resolution creates at most two observations.

P04 source fingerprints now include source and availability time so open-period high/low changes propagate. P05 itself skips classification when the P04 fingerprint is unchanged.
