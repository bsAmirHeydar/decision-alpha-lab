# 04 — Source Sanity & Drift Detection

## Guardrails

- `InpSourceMinRawBytes`
- `InpSourceMaxRawBytes`
- `InpSourceMinEventBlocks`
- `InpSourceRequireEventBlocks`

## Drift Symptoms

- zero `<event>` blocks
- missing `<country>` nodes
- missing `<title>` nodes
- missing `<impact>` nodes
- raw payload too small
- raw payload unexpectedly huge

## Decision

Sanity failure blocks parser execution and forces the fallback chain.
