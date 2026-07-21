feat(lcm): implement LCM-06 migration framework and compatibility layer

- bind the framework to the exact LCM-05 topology handoff
- enforce a reference-only authority permit with no mutation or runtime powers
- register closed migration states, parity dimensions, adapter types and gates
- validate migration packets against source hashes, owners and known-time rules
- resolve canonical aliases and quarantine ambiguous identities deterministically
- normalize behavioral traces before hard and soft parity comparison
- block unknown evidence and prohibit hard-mismatch waivers
- define compatibility contracts for context, setup, treatment and visual adapters
- generate move-only plans and redirect previews without writing source changes
- validate quarantine readiness without moving legacy artifacts
- enforce non-compensatory deletion gates without deleting source files
- publish immutable events, provenance, receipt, manifest and LCM-07 handoff
- add schemas, policies, tests, MQL5 static contracts and Obsidian documentation

No legacy source movement, deletion, merge, semantic refactor, target
materialization, cutover, runtime authority, live-order authority or capital
authority is introduced.
