# Rollback

This patch is additive or bounded-recovery work and grants no deletion authority.

To roll back before commit, restore every path in `PATCH_FILE_INDEX.txt` from the current branch and remove paths that did not exist before the patch. To roll back after commit, revert the UC04-W0 commit as one unit.

After rollback, run the accepted UC-03 Part 3 verifier and migration-continuity verifier. Do not selectively retain generated ACL03 or registry digest changes without their corresponding path-recovery code and amendments.
