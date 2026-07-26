---
id: EXP0018-P05-EVENTS
title: "P05 State Events and Transitions"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Events

- `ENGINE_INITIALIZED`
- `STATUS_CHANGED`
- `STORE_READY`
- `STORE_DEGRADED`
- `SOURCE_UNAVAILABLE`
- `LATEST_OBSERVATION_ADVANCED`
- `OBSERVATION_STATE_CHANGED`
- `ONE_SIDED_HUNT_APPEARED`
- `DOUBLE_HUNT_APPEARED`

Events preserve event time, availability time, and processing time separately. They describe observations, not confirmed trades.
