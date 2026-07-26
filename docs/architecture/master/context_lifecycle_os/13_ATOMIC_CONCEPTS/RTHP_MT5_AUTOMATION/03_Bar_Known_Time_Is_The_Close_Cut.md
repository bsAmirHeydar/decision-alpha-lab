---
title: Bar Known Time Is the Close Cut
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, atomic-concept]
---
# Bar Known Time Is the Close Cut

A historical M1 bar is causally available no earlier than its close. Research replay uses bar close as the known-time cut, even if the artifact was downloaded later. Ingestion time is provenance and cannot be substituted for historical availability.
