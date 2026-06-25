# EXP0013 Raw Sky V14 Compile Fix

This patch fixes the V14 `undeclared identifier` compile error in `EXP0013_AstroUnifiedDashboardEA.mq5`.

## Cause

The V14 tabbed raw-sky UI started using additional derived layout fields in `DAL_GetGrid()` and the tab renderers:

- `card_w`
- `diag_w`
- `col1_x`
- `col2_x`
- `col3_x`
- `row1_y`
- `row2_y`
- `row3_y`

But those fields were not declared inside the `DAL_UIGrid` struct.

## Fix

The missing fields were added to `DAL_UIGrid`.

No trading logic, astrology logic, or CSV contract was changed.
