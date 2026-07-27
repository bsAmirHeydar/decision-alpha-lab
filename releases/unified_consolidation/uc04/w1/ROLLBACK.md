# Rollback

UC04-W1A is additive except for the UC-04 records MOC link. It modifies no production MQL5 consumer and creates no production shared engine.

Before commit, restore every path listed in `PATCH_FILE_INDEX.txt` from the current branch and remove paths that did not exist before the patch. After commit, revert the W1A commit as one unit.

After rollback, run Engineering Policy and the accepted UC04-W0 verifier with release controls skipped. Do not retain generated W1A registry records without their corresponding schemas, fixtures, reference artifacts and verifier.

Runtime evidence under `.alpha/runs/uc04w1/` is operator-local and is not part of the tracked patch.
