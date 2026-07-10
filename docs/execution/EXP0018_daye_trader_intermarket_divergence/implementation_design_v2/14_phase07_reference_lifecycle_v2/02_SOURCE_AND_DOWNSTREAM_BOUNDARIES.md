# Source and downstream boundaries

P07 consumes two read-only P06 surfaces:

1. immutable `DAYE_ConfirmationResult` records;
2. current P05 `DAYE_HuntObservation` records exported through P06 without granting P06 lifecycle authority.

P07 publishes:

- `DAYE_ReferenceLifecycleRecord` for current lifecycle truth;
- `DAYE_ReferenceUseRecord` for immutable historical confirmation evidence.

P08 draws only accepted use records. Retirement never deletes an accepted use. P11 replays the same transitions in chronological order. P12 audits every lifecycle decision.
