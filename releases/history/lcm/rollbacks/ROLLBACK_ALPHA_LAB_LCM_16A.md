# Rollback Alpha Lab LCM-16A

Rollback to the commit immediately before the LCM-16A patch. Restore the bounded modified files from that commit and remove only paths listed in `LCM_16A_FILE_INDEX.txt` that did not exist before the patch. Do not delete LCM candidates, Git LFS objects, canonical targets, redirects or runtime state.

After rollback, verify LCM-15A, LCM-15B and LCM-15C directly and rerun Engineering Policy. A rollback does not authorize migration closure, deletion, runtime activation, live orders or capital.
