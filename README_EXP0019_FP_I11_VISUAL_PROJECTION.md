# EXP0019 Faerie Protocol — FP-I11 Visual Projection

This patch implements the complete chart-object projection layer for the Faerie Protocol indicator.

It adds deterministic rendering for sessions, weeks, references, hunts, roles, candidates, confirmed signals, invalidations, weekly context, WW suppression, quota suppression, quota winners, and health. The renderer consumes semantic evidence from FP-I03 through FP-I10 and has no semantic or trade authority.

## Primary entry points

- `mql5/Indicators/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Context.mq5`
- `mql5/Indicators/EXP0019/FaerieProtocolTests/EXP0019_FP_I11_VisualSelfTest.mq5`

## Local verification

Compile both indicators in MetaEditor, attach the self-test to a chart, verify every visual family, then attach the production indicator to two charts and confirm namespace isolation.
