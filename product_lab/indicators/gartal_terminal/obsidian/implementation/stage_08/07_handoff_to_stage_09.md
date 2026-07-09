# 07 — Handoff to Stage 09

Stage 09 should harden the data layer.

## Required Work

- cache expiry policy
- stale data banner
- last good source snapshot metadata
- rate-limit guard
- source drift detector
- parser checksum drift warning
- customer setup wizard
- local file freshness diagnostics

## Stage 08 Known Limits

- CSV parser is guarded placeholder
- HTML parser is guarded placeholder
- true live breaking headlines require another data feed
- source timezone still needs user/broker validation
