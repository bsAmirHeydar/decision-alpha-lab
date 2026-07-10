---
id: EXP0018-P11-10_HOST_BAR_RECONSTRUCTION
title: "Host-bar reconstruction"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Host-bar reconstruction

Host OHLC is rebuilt from the exact aligned base-bar pairs inside `[host_open, host_close)`. The expected base-bar count must be exact. This prevents a broker's pre-aggregated host candle from silently diverging from the source grid used by P03 and P05.
