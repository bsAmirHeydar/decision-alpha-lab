---
id: EXP0018-P05-IDENTITY
title: "P05 Identity, Deduplication, and Idempotency"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Identity

One P04 opportunity produces at most two P05 observation identities: one HIGH and one LOW. Reprocessing unchanged inputs produces identical IDs and identical states.

A duplicate observation ID inside one build is a critical error. Repeated timer callbacks with unchanged availability time do not emit new state-change events.
