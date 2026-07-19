# LCM-08C Rollback Runbook

LCM-08C is additive except for roadmap documentation status updates. No consumer, runtime configuration, source file, persistent state, order path or chart object is changed. Rollback removes only files listed in `LCM_08C_FILE_INDEX.txt` and restores modified documentation from the predecessor commit.

After rollback:

1. Verify the LCM-08B handoff digest remains `sha256:c5695d5a671b09723851df4989a8a617242b5a2a7518885040cfb0b986451381`.
2. Re-run LCM-08B package verification and tests.
3. Verify every source digest in the LCM-08A portfolio still matches.
4. Confirm no LCM-08C locator or handoff remains active.
