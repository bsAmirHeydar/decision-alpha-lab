# Performance and Refresh

P08 is timer-driven and bounded by accepted uses × matching open charts. It does not rescan chart bars for detection. Source periods are already built by P03. Object verification uses deterministic names, avoiding full object-list searches for each line.

Chart redraw occurs only after create or repair, not every callback.
