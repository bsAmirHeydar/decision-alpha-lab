# LCM-10A Rollback

LCM-10A is additive except for five authoritative roadmap/phase documents. It does not mutate legacy Treatment or execution sources.

Before commit, restore the repository with Git by removing only untracked paths listed in `LCM_10A_FILE_INDEX.txt` and restoring tracked modifications from `HEAD`. Review the path index before any removal.

After commit but before shared downstream work, use `git revert <LCM-10A-commit>` and push the revert. Do not use history rewriting on a shared branch.

Rollback must preserve:

- the accepted LCM-09B setup migration and handoff;
- all legacy source files and hashes;
- all pre-existing ACL/LCM registries;
- the prohibition on runtime, order and capital authority.
