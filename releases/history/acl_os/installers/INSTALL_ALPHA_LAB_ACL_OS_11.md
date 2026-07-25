# Install ACL-11 patch

Expand the patch at repository root. Stage only paths listed by `ACL_OS_11_FILE_INDEX.txt`, commit from `COMMIT_MESSAGE.md`, and push. The patch is root-relative and contains no deletion directive.

## Verification

Run the ACL-11 tests, direct ACL-10 regression, Python compileall and reference-output verifier. MetaEditor and MT5 verification remain external.
