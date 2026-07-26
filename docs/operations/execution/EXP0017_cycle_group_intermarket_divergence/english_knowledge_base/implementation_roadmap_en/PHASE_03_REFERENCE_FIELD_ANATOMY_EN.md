# Phase 03 — Reference Field Anatomy

## Purpose

Store all previous same-day cycle highs and lows per symbol, CG, and cycle.

## Input Contract

This phase consumes the completed state of all earlier phases. It must not redefine earlier doctrine.

## Output Contract

- Human-readable documentation.
- Obsidian concept notes and maps.
- Inspectable system state where code exists.
- No hidden assumptions.

## Validation

A phase is complete only when the Strategy Architect can inspect the output and confirm that the robot sees the same anatomy as the doctrine.

## Non-Goals

This phase must not create unapproved filters, priority rules, AI mutation, or execution authority unless that is explicitly the purpose of the phase and a promotion gate has been passed.
