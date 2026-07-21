feat(lcm): complete setup package migration and reference factory binding

- bind LCM-09B to the exact accepted LCM-09A handoff and 60-identity freeze
- materialize one canonical fail-closed reference package for every frozen Setup identity
- implement deterministic Setup lifecycle evaluation with explicit no-trade and known-time guards
- add translation-only legacy evidence adapters that never execute legacy sources
- expose all migrated identities through a read-only ACL-04 legacy reference port
- preserve all owner, characterization, Context and Treatment blockers non-compensatorily
- publish blocked golden cases, restart checkpoints and parity dispositions without false PASS claims
- seed explicit Treatment capability dependencies for LCM-10A
- add closed schemas, policies, provenance, event ledger, hostile review and acceptance reports
- deny consumer cutover, source lifecycle changes, promotion, runtime, order and capital authority
- close LCM-09 and publish the bounded LCM-10A handoff
