# STC / SMT Offline License Patch

This archive contains a git patch only. Apply it from the root of `decision-alpha-lab`.

```bash
unzip -o stc_smt_offline_license_patch.zip -d _patch_stc_smt_license && \
rm stc_smt_offline_license_patch.zip && \
git apply _patch_stc_smt_license/stc_smt_offline_license.patch
```

Then review and commit:

```bash
git status
git diff --stat
git add .
git commit -m "Add offline licensing to STC SMT divergence cycles"
```
