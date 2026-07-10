# Handoff to P10, P11 and P12

P10 implements TWO/TDO through an independent anchor-line renderer. It must not overload P09 rectangles.

P11 reuses P01–P03 and P09 projection rules during chronological replay to rebuild complete history deterministically.

P12 may reconcile P09 audit rows with P03 period snapshots and chart objects. It must treat projection records, not pixels, as evidence.
