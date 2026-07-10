---
id: EXP0018-P11-20_RESTART_AND_RECOVERY
title: "Restart and recovery"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Restart and recovery

A stopped run is restarted from cursor zero with the same inputs. Deterministic output identities allow replacement or comparison. Live P06/P07 checkpoints are not imported into replay because they represent a different runtime horizon. Partial replay checkpointing is deferred until it can serialize the entire reducer state without ambiguity.
