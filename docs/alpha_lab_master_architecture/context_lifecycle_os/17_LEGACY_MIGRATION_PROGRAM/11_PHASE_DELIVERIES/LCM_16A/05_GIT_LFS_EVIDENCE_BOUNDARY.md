# Git LFS evidence boundary

Two LCM-12A JSONL evidence files are stored through Git LFS. A source archive can contain only 133/134-byte pointer records instead of the 74 MB and 105 MB objects. In that state, LCM-12A is `BLOCKED`, not semantically failed.

A closure run must execute `git lfs pull` and prove both paths are materialized before counting LCM-12A as PASS.
