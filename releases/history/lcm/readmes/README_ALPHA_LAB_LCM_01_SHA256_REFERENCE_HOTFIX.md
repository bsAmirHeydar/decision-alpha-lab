# Alpha Lab LCM-01 SHA-256 Reference Compatibility Hotfix

This additive hotfix corrects the LCM-01 cross-platform installation verifier so that it accepts both SHA-256 representations already used by Alpha Lab baseline manifests:

- bare digest: `<64 hexadecimal characters>`
- algorithm-qualified digest: `sha256:<64 hexadecimal characters>`

The verifier normalizes only the representation of the expected digest. It does not weaken content verification, text EOL normalization rules, path controls, symlink denial, binary byte equality, or fail-closed behavior.

## Corrected failure

The first cross-platform hotfix correctly handled CRLF/LF checkout equivalence but its focused fixtures used bare SHA-256 values. The production LCM-00 baseline manifest stores qualified values such as `sha256:8d4149...`. The parser rejected that valid representation before repository bytes could be checked.

## Scope

Changed runtime files:

- `tools/strategy_factory/lcm/lcm_01/cross_platform_integrity.py`
- `lab/11_strategy_factory/migration/tests_lcm_01/test_cross_platform_integrity_hotfix.py`

No survey artifact, baseline artifact, LCM-00 record, Context logic, Setup logic, execution authority, runtime authority, order authority, or capital authority is modified.
