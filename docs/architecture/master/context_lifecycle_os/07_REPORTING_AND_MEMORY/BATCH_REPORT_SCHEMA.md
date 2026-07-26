---
title: Batch Report Schema
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-08, reporting]
---
# Batch Report Schema

The canonical Batch Report is a closed-schema machine artifact. It binds Report ID, Validation ID, Run ID, Batch ID, source and local claim ceilings, report block order, candidate count, decision counts, gate-status counts, unknown-gate frequency, candidate-report digests, limitations and authority denials.

Candidate pages are separate digest-bound artifacts. This prevents one oversized mutable document from becoming the evidence source and allows each candidate projection to be independently verified.
