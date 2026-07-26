---
title: Experience Extraction Pipeline
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Experience Extraction Pipeline

ACL-08 converts each preserved validation decision into one non-promotional experience record. The classification is mechanical: baseline reference, insufficient evidence, validation failure, reportable evidence or diagnostic exclusion. No natural-language model interprets market meaning.

Each record includes the exact source decision digest, gate digest, failed and unknown gates, reason codes, duplicate fingerprint and bounded evidence questions. It is explicitly marked `NOT_INGESTED`; ACL-09 owns memory admission, duplicate resolution and active planning.
