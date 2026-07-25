# Installation and validation

Expand the ZIP at repository root, remove the ZIP, run `python tools/strategy_factory/saed_v4_19/run_saed_v4_19_full_qa.py`, run `python tools/strategy_factory/saed_v4_19/validate_saed_v4_19_delivery.py`, stage with `git add --pathspec-from-file=SAED_V4_19_FILE_INDEX.txt`, inspect `git diff --cached --check`, commit with `git commit -F COMMIT_MESSAGE.md`, and push.
