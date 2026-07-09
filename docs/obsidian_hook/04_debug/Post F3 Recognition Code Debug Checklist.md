# Post F3 Recognition Code Debug Checklist

When the chart still selects the wrong post-F3 Hook, check:

1. Is the F3 terminal endpoint correct?
2. Is the Hook direction opposite the F3 direction?
3. Is the Hook origin inside `InpHookPostF3MaxSearchBars`?
4. Is the Hook direct or delayed?
5. If direct, are price and time tolerances too strict?
6. If delayed, is `InpHookPostF3AllowDelayedReboundHook` enabled?
7. If structural is missing, does the candidate have `x_count >= 2`?
8. If geometric is expected, is `InpHookPostF3RecognitionMode` set to `STRUCTURAL_OR_GEOMETRIC_80`?
9. Is `retracement_ratio * 100` above `InpHookPostF3GeometricMinCompletionPct`?
10. Does CSV show the expected `post_f3_subfamily`?
