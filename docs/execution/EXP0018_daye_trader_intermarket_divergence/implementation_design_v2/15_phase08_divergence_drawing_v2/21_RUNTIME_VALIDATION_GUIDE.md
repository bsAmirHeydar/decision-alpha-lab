# Runtime Validation Guide

1. Compile P07 and P08 with zero errors and warnings.
2. Open both broker-symbol charts.
3. Attach P08 to either chart.
4. Confirm P07 accepted-use count increases before expecting a line.
5. Check that line appears only on Hunter-symbol chart(s).
6. Verify major alias and minor no-label behavior.
7. Move or delete an owned line; confirm deterministic repair.
8. Trigger later reference retirement; confirm historical line remains.
9. Inspect `Ctrl+B` and confirm ownership prefix.
10. Enable CSV audit only for controlled diagnosis.
