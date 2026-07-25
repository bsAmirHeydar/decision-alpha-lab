# Install EXP0019 FP-I14

1. Extract the patch into the repository root.
2. Stage only paths from `EXP0019_FP_I14_FILE_INDEX.txt`.
3. Run Python tests and static validators.
4. Compile the production Indicator, Diagnostic EA, and FP-I14 Self-Test in MetaEditor.
5. Run the Self-Test, then run Indicator and Diagnostic EA on identical pair/config/history.
6. Export traces and compare them with `tools/exp0019/compare_fp_i14_traces.py`.
7. Do not enable paper or live execution; FP-I14 has runtime authority `NONE`.
