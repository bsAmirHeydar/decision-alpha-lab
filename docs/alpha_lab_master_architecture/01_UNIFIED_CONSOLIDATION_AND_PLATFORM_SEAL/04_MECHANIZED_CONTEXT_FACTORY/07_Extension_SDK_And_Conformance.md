---
id: UCPS-DF277E0980CE
title: "Extension SDK and Conformance"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Extension SDK and Conformance

## Extension types

Detector, Feature, Label, Treatment, Model, Data Adapter, Storage Adapter, Broker Adapter and Visualizer.

## Manifest

An extension declares ID, version, owner, type, capabilities, inputs, outputs, dependencies, deterministic behavior, resource needs, failure semantics, security scope and supported contract versions.

## Conformance

The SDK supplies contract tests, property tests, fixture runners, sandboxing, registration and compatibility checks. An extension is not loadable until conformance passes.

## Isolation

Extensions access shared services through public ports. Private imports, registry mutation, direct secret access and hidden network calls are prohibited.

## Lifecycle

Extensions have registration, active, deprecated, quarantined and retired states with explicit consumer and compatibility evidence.
