
# MT5 M1 Automatic Intake Handoff

The current Train Activation accepts local paired source artifacts. The production MT5 automation delivery adds an upstream, read-only acquisition layer that retrieves closed M1 bars, validates them, freezes immutable source bindings, and invokes this existing activation.

Authoritative roadmap:

- [[../RTHP_MT5_AUTOMATION/00_RTHP_MT5_AUTOMATION_MOC|RTHP MT5 Automatic M1 Data Acquisition and One-Click Train]]

Key boundary:

```text
MT5 acquisition and M1 quality = RTHP-owned adapter
RTHP materialization and train activation = existing RTHP-owned activation
training and validation = existing shared engines
central engine changes = none
```

Sub-M1 data and synthetic ticks are excluded from the canonical production path.
