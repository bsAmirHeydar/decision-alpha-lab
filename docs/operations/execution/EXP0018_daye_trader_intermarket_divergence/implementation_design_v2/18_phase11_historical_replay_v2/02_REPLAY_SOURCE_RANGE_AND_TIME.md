---
id: EXP0018-P11-02_REPLAY_SOURCE_RANGE_AND_TIME
title: "Replay source range and time"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Replay source range and time

The operator supplies New York wall-time start and end boundaries. P01 resolves them to UTC using DST fold/gap policy. Replay requires a fixed manual broker UTC offset because the current broker offset cannot be projected backward safely. The canonical cursor is UTC and remains strictly increasing through spring and autumn DST transitions.
