# Label Stacking

## Purpose

When all sequences are shown, label collision is unavoidable unless labels are stacked deterministically.

## Anchor Rule

Peak labels should be above peaks.

Valley labels should be below valleys.

This applies to F labels, internal numbers, ND labels, and origin markers when tied to a high/low node.

## Stack Buckets

Group labels by approximate chart location:

```text
time bucket
price-side bucket: peak | valley
node id if available
```

Do not randomly offset each label.

## Order Within Stack

Near price to far from price:

1. older sequence first;
2. higher F-level first within same sequence age if needed;
3. confirmed before candidate;
4. ND/internal labels after owning F label unless specifically anchored to same node;
5. deterministic id as final tie-breaker.

The user preference is:

```text
older should be closer
```

## Peak Placement

For a high/peak anchor:

```text
base_y = node price + vertical padding
stack direction = upward
```

## Valley Placement

For a low/valley anchor:

```text
base_y = node price - vertical padding
stack direction = downward
```

## Vertical Step

Use ATR, chart scale, or fixed point distance.

Recommended input:

```text
InpLabelStackStepPoints
InpLabelBasePaddingPoints
```

## Avoid Huge Distance

If labels become too far from price due to too many labels, do not randomize.

Options:

- increase stack step compression;
- reduce font size;
- group exact duplicate geometry labels if explicitly enabled;
- show full details in tooltip/panel while keeping label short.

Do not move labels arbitrarily across the chart.

## Label Identity

Every label object name should include logical id:

```text
FCN_F_LABEL_<chain_id>_<f_id>
FCN_NUM_LABEL_<hook_id>_<number>
FCN_ND_LABEL_<hook_id>
FCN_ORIGIN_<f_id>
```
