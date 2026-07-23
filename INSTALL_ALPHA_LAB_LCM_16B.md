# Install Alpha Lab LCM-16B

Apply only to a clean repository that already contains LCM-16A. Verify the ZIP digest before extraction, overlay the exact indexed paths, materialize required Git LFS evidence, run package QA, direct tests, LCM-16A verification and Engineering Policy, then stage only `LCM_16B_FILE_INDEX.txt`.

The install validates the implementation package. It does not manufacture MetaEditor, Strategy Tester, terminal parity, external-consumer or human approval evidence.

After installation, external evidence may be assembled under a separate evidence directory using:

- `registry/legacy_context_migration/lcm_16b/templates/v1/external_evidence_bundle.template.json`
- `tools/strategy_factory/lcm/lcm_16b/capture_lcm16b_metaeditor.ps1`
- `python -m tools.strategy_factory.lcm.lcm_16b.cli evaluate-evidence ...`

External evidence outputs should be reviewed and committed separately from the implementation patch because they depend on the actual machine, terminal build, consumer scope and human approvals.
