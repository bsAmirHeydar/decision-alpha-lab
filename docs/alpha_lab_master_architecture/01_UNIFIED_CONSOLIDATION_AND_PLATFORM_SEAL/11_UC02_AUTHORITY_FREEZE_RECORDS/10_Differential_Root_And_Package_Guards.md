---
id: UCPS-9DC93383AD7B
title: "Differential Root and Package Guards"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# Differential Root and Package Guards

## Why differential enforcement is required

The current repository contains substantial grandfathered root and package debt. Declaring the present tree compliant would be false, while rejecting every existing path would prevent controlled migration.

## Guard model

The UC-01 baseline freezes the existing root files, top-level directories and package surfaces. UC-02 permits canonical target roots but rejects new uncontrolled root files, parallel engines and nested product paths.

## Root rules

New phase-specific README, install, rollback, commit-message, file-index, hash, manifest, QA and inventory files at repository root are rejected. New release controls belong under `releases`.

## Package rules

New packages resembling Strategy Factory, UCEE, ACL-OS, SAED platform generations or another operating system are rejected. New consolidation, engineering and maintenance tools are allowed only under their bounded utility roots.

## Future tightening

UC-03 reduces grandfathered debt wave by wave. UC-07 changes the guard from differential enforcement to final topology enforcement.
