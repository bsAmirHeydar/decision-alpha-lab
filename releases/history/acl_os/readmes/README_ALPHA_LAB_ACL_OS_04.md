# Alpha Lab ACL-OS ACL-04

ACL-04 implements the governed **Dual Setup Factory**. It consumes the immutable `ACL03_TO_ACL04` Context handoff, requires explicit ACL-00 and Search Authority, compiles human-authored and bounded AI-generated definitions into one canonical `ACL04_SETUP_POLICY_IR`, enforces Treatment and known-time boundaries, emits mandatory baselines, deduplicates behavioral equivalents, records complete search exposure and provenance, generates Obsidian projections, and hands a non-executable candidate universe to ACL-05.

## Claim ceiling

`SETUP_DEFINITION_REFERENCE_ONLY`

This patch does not establish alpha, backtest quality, execution readiness, broker parity, production authorization or capital authority.

## Primary entry points

- Python service: `tools/strategy_factory/acl_os/acl_04/service.py`
- CLI: `python -m tools.strategy_factory.acl_os.acl_04.cli`
- Full QA: `python -m tools.strategy_factory.acl_os.acl_04.run_acl_04_full_qa`
- Delivery validator: `python -m tools.strategy_factory.acl_os.acl_04.validate_acl_04_delivery`
- Canonical documentation: `docs/alpha_lab_master_architecture/context_lifecycle_os/04_SETUP_FACTORY/00_MOC.md`
- Phase delivery documentation: `docs/alpha_lab_master_architecture/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_04/00_MOC.md`
- Atomic concepts: `docs/alpha_lab_master_architecture/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_04/00_MOC.md`

## Accepted output

The reference factory produces content-addressed candidate artifacts, a canonical candidate set, deduplication evidence, an exposure ledger, a provenance graph, security evidence, generated Obsidian projections, an output manifest, a factory receipt and the immutable `ACL04_TO_ACL05` handoff.
