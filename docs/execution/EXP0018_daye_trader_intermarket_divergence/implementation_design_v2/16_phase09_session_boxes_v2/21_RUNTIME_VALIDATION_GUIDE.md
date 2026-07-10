# Runtime Validation Guide

1. Compile P09 with zero errors and zero warnings.
2. Open both exact broker-symbol charts.
3. Attach P09 with a verified broker UTC offset.
4. Confirm A/L/N/P boxes use expected times and colors.
5. Compare each box High/Low against source bars.
6. Observe an open session expand without duplication.
7. Move and delete one owned box; confirm repair/recreation.
8. Confirm foreign objects and P08 lines remain untouched.
9. Change timeframe and reattach; verify deterministic objects.
10. Inspect Object List and optional CSV ledger.
