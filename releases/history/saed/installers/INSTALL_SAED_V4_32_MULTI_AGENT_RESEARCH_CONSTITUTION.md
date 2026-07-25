# Install SAED V4-32

1. Place the ZIP in the repository root.
2. Expand it into the repository root with overwrite enabled.
3. Remove the ZIP.
4. Run `python tools/strategy_factory/saed_v4_32/run_saed_v4_32_full_qa.py`.
5. Run `python tools/strategy_factory/saed_v4_32/validate_saed_v4_32_delivery.py`.
6. Stage with `SAED_V4_32_FILE_INDEX.txt`, inspect the staged diff, commit with `COMMIT_MESSAGE.md`, and push.
