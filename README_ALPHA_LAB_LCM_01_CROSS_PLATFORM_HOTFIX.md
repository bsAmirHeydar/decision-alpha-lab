# Alpha Lab LCM-01 Cross-Platform Integrity Hotfix

This additive hotfix corrects false baseline hash mismatches caused exclusively by Git CRLF checkout conversion on Windows with `core.autocrlf=true`.

It preserves raw SHA-256 authority and permits a text file only when LF line-ending canonicalization reproduces the exact frozen baseline digest. It does not weaken binary verification or accept semantic text changes.
