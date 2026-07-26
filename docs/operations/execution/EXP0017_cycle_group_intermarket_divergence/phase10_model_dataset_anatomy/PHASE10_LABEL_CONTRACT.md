# Phase 10 — Label Contract

## Primary label

The selected `InpPrimaryLabelWindow` chooses one R outcome as `primary_r`.

Default:

```text
InpPrimaryLabelWindow = CGM_LABEL_CYCLE_END
```

## Label columns

- `label_class`: `WIN`, `LOSS`, or `FLAT`.
- `label_binary_win`: 1 if `WIN`, otherwise 0.
- `label_hit_1r`: 1 if MFE reached the configured one-R threshold.
- `label_stopped_intraday`: 1 if stop was hit intraday.
- `label_adverse_1r`: 1 if MAE reached the configured adverse-R threshold.

## Thresholds

Default:

```text
win_threshold_r = 0.0
loss_threshold_r = 0.0
one_r_threshold = 1.0
adverse_one_r_threshold = -1.0
```

## Leakage warning

`mfe_r`, `mae_r`, and forward-window outcomes are not pre-signal features. They are included so research tools can choose labels deliberately. A model-training export must separate features from labels before training.
