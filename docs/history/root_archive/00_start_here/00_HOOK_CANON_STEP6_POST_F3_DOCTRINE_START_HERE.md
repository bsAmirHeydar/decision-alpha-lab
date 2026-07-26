# HOOK CANON STEP 6 — Post-F3 Hook Recognition Doctrine

This patch is documentation-only.

It corrects the missing doctrine around **what counts as the Hook after an F3**.

The current code can correctly detect the F3, but it can still select the wrong post-F3 Hook because the Canon did not yet distinguish:

1. direct terminal-origin Hook after F3
2. delayed rebound Hook after touching/reaching the F3 terminal side
3. structural Hook with full nodes/sequences
4. geometric 80% cycle Hook when no full structural sequence exists

No MQL5 code is changed in this patch.
