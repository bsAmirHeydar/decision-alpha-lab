# Store Metric Repaint Contract

After every accepted filter click:

```mql5
GT_UpdateStoreMetrics(g_store, g_filters);
GT_RedrawAll();
```

This is required because dashboard cards depend on store pointers such as:

- `visible_count`
- `next_event_index`
- `next_high_index`

Without recalculation, the table might filter correctly but the next-event card could remain stale.
