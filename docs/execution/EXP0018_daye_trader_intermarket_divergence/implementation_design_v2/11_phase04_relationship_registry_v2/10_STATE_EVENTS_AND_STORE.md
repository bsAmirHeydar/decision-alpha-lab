---
id: EXP0018-P04-STATE-EVENTS
title: "P04 State, Events, and Store"
type: state-contract
status: active
project: EXP0018
phase: P04
---
# State and Events

Store states include READY, SOURCE_UNAVAILABLE, INVALID_REGISTRY, and explicit unavailable resolution classes. Events include initialization, status change, store ready/degraded, source unavailable, and latest-ready-opportunity advanced.

The in-memory store supports deterministic export and query by opportunity ID. Chart objects are not used as state. P05 consumes the store through typed data, not through object names or chart scans.
