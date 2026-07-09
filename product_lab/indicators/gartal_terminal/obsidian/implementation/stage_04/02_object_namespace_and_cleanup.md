# Object Namespace and Cleanup

## Namespace

Stage 04 creates objects under:

```text
{InpObjectPrefix}TL_
```

Examples:

```text
GT_TL_VLINE_USD_...
GT_TL_LABEL_USD_...
GT_TL_ZONE_USD_...
```

## Why Separate Namespace

The dashboard uses `GT_DASH_` and the bottom tape uses `GT_TIMELINE_`. Timeline chart objects need independent cleanup because they are recreated whenever chart scale, filters, time window, or event data changes.

## Cleanup Rule

Every redraw deletes only `GT_TL_` objects, not dashboard or shell objects. This prevents stale event lines without flashing the dashboard panel.
