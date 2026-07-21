# Rollback Alpha Lab LCM-12A

Before commit, remove only paths listed by `LCM_12A_FILE_INDEX.txt` that were added by the patch and restore any modified paths from Git. After commit, use a normal Git revert of the LCM-12A commit. Re-run the direct acceptance and package-verification tests. No document location or content restoration is required because LCM-12A performs no document move or deletion.
