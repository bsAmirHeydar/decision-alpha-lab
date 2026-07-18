feat(acl-os): implement ACL-10 promotion state machine

- verify the complete ACL-09 memory and planner package
- add closed state, transition and prerequisite registries
- preserve UNKNOWN, baseline and diagnostic isolation
- issue deterministic non-executing promotion-state decisions
- enforce multi-party approval and self-approval denial boundaries
- emit an empty runtime candidate manifest for the reference fixture
- add ACL-11 handoff, event ledger, provenance, tests and Obsidian documentation
