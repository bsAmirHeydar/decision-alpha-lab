# Rollback RTHP ACL-03 Patch

Use `git revert <commit>` to preserve append-only repository history. Do not manually edit generated ACL-03 artifacts. After a revert, the authoritative state returns to the prior ACL-02 package and the ACL-03 handoff must not be consumed.
