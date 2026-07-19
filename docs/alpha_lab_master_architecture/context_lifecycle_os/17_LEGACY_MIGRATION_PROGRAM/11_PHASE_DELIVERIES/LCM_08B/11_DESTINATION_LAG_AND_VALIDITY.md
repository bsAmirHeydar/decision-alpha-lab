---
title: "LCM-08B — 11 Destination Lag And Validity"
status: accepted-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, lcm-08b, pilot-migration]
phase_id: LCM-08B
---
# Destination Lag and Validity

If origin triggers, destination is checked inclusively from evaluation through the lag endpoint. A destination trigger suppresses the occurrence. Otherwise validity begins at the lag endpoint and extends by at least one bar. Late destination confirmation is observed only after valid-from and through valid-until.
