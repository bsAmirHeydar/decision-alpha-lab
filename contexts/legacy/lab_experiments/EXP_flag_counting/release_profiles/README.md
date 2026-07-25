# Phoenix Release Profiles

This folder documents the operational profiles implemented by Level 14.

## Profiles

| Profile | Purpose | Chart | CSV | Validation |
|---|---|---:|---:|---:|
| normal | Default run | yes | user input | user input |
| clean_main | Clean screenshot | yes | user input | user input |
| audit_export | Logic audit before chart trust | no | yes | no |
| validation | Regression/baseline run | yes | yes | yes |
| debug_max | Full diagnostic mode | noisy | yes | baseline |
| render_off | Headless CSV run | no | yes | optional |
| safe_rollback | Cleanup/recovery | no | no | no |

## Standard release run

```text
1. Compile fresh.
2. Set InpReleaseProfile = FP_RELEASE_PROFILE_CLEAN_MAIN.
3. Attach EA and inspect FP_LEVEL14.
4. If chart is suspicious, switch to FP_RELEASE_PROFILE_AUDIT_EXPORT and inspect latest_events.csv.
5. For regression, switch to FP_RELEASE_PROFILE_VALIDATION and fill expected min/max ranges.
```

## Recovery

```text
InpReleaseProfile = FP_RELEASE_PROFILE_SAFE_ROLLBACK
```

This suppresses detection/drawing and requests prefix cleanup. It is only for recovery.
