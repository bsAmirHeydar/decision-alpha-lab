# Alpha Lab Hook Validity Patch

This patch documents and organizes the Hook Validity Layer for the zone-centric antifragile strategy.

It is documentation-only. It does not modify execution logic, MQL5 behavior, Python research code, registry semantics, or production rules.

## Purpose

The goal is to prevent hook over-counting and fractal ambiguity. Because hooks can be detected at many nested scales, a raw hook detector can produce too many hook-like candidates. This patch defines which hooks are structurally valid and which ones are noise.

## Core Thesis

A hook is valid for zone generation only when it belongs to one of two families:

1. **Hook After Hook** — the new hook starts exactly from the terminal node of the previous hook.
2. **Hook After Opposing F3** — after an opposing F3 prints, the following hook becomes a valid reversal/transition structure.

All other hook-like formations are not reliable zone sources by default.

## Main Files

```text
docs/hook_validity/
├── HOOK-VAL-0001_Valid_Hook_Philosophy_and_Filtering_Policy.md
├── HOOK-VAL-0002_Hook_After_Hook_Chained_Node_Architecture.md
├── HOOK-VAL-0003_Hook_After_Opposing_F3_Architecture.md
├── HOOK-VAL-0004_Invalid_Hooks_and_Fractal_Noise_Control.md
├── HOOK-VAL-0005_Hook_Zone_Risk_Contract.md
└── HOOK-VAL-0006_Hook_Validation_Dataset_and_Learning_Policy.md

docs/obsidian_hook/
├── 00_mocs/
├── 01_concepts/
├── 02_policies/
├── 03_architecture/
├── 04_training/
├── 05_templates/
├── 06_canvases/
└── 07_indexes/
```

## Entry Point

Open this note in Obsidian:

```text
00_HOOK_VALIDITY_START_HERE.md
```
