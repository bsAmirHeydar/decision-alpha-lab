---
note_id: RTHP_MT5_AUTOMATION_28_CROSS_PLATFORM_GOVERNANCE
note_type: implementation_delivery
status: IMPLEMENTED_AND_TESTED
owner: RTHP_CONTEXT_ADAPTERS
---

# Cross-Platform Governance Hardening

## Scope

This delivery removes three host-specific false failures without modifying the central ACL engine or the Canonical RTHP Context.

## Central-engine snapshot policy

The RTHP engine-boundary snapshot now uses `TEXT_LF_CANONICAL_BINARY_RAW_V1`:

- known text files are hashed after CRLF and lone CR are normalized to LF;
- binary files remain raw-byte hashed;
- semantic text changes still alter the digest;
- protected engine prefixes remain unchanged.

The snapshot policy lives in the context-owned RTHP package. It does not change engine runtime behavior.

## ACL-03 source approval on Windows

ACL-03 approvals remain strict raw-byte approvals. The RTHP onboarding adapter creates an ephemeral LF-canonical mirror and passes that mirror to the unchanged central compiler.

Consequences:

- the approved Context directory is never rewritten;
- an EOL-only Windows checkout compiles to the approved digest;
- any semantic source change still triggers `ACL03_SOURCE_CHANGED_AFTER_APPROVAL`;
- central ACL-03 hashing and prerequisite logic remain untouched.

## Windows symlink capability

The ACL-03 symlink security test continues to prove that the source snapshot rejects symlinks. On Windows hosts lacking the required privilege (`WinError 1314`), only the test setup is skipped because the host cannot create the adversarial fixture. The production guard is not skipped or weakened.

## Boundary statement

- Central Engine modified: `false`
- Canonical Context modified: `false`
- Approval evidence regenerated: `false`
- Trading authority created: `false`

## Related notes

- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/17_Test_Strategy_Acceptance_Matrix_and_Definition_of_Done]]
- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/27_Holiday_and_Session_Aware_Gap_Classification]]
