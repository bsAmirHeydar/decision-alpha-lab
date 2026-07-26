# Install — LCM-01 SHA-256 Reference Compatibility Hotfix

Apply this patch from the repository root after commit `c891ff5a` or an equivalent installation of the first LCM-01 cross-platform hotfix.

The included PowerShell runner performs:

1. package verification;
2. installation verification;
3. Python compilation;
4. LCM-01 regression tests;
5. LCM-00 regression tests;
6. ACL-15 regression tests;
7. explicit Git staging;
8. commit and push.

The script stops on the first failure and does not commit a failed verification.
