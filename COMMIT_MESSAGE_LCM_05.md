feat(lcm): implement LCM-05 target topology and repository locator

- bind the phase to the exact LCM-04 characterization handoff
- register one canonical package root per artifact role and identity kind
- define a closed acyclic dependency-direction policy
- enforce authored versus generated authority boundaries
- map every classified artifact to a deterministic target outcome
- map every canonical identity to a target package root
- route unresolved identities to blocked quarantine proposals
- design root release and installer relocation without moving files
- select documentation successors without deletion authority
- validate root-relative Windows-safe collision-free target paths
- audit legacy dependency directions against the target architecture
- publish immutable events, provenance, receipt, manifest and LCM-06 handoff
- add schemas, policies, tests, MQL5 static contracts and Obsidian documentation

No legacy source movement, deletion, merge, semantic refactor, cutover,
runtime authority, live order authority or capital authority is introduced.
