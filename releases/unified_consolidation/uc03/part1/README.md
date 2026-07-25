# UC-03 Part 1 — Runtime-Head Resume Rescue

This package resumes a partially applied UC-03 Part 1 checkout.

It does not trust frozen source hashes from a different checkout. It preserves
actual working-tree bytes during every move, accepts already moved files,
preserves destination conflicts under `releases/history/conflicts/`, rewrites
active references, and generates `PATCH_FILE_INDEX.txt` from the real Git
worktree.
