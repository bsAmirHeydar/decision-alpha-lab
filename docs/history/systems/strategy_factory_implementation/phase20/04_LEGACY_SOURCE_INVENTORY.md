# Legacy Source Inventory

Primary source files:
- `CGT_Types.mqh`, `CGT_Time.mqh`
- `CGH_Types.mqh`, `CGH_HuntField.mqh`
- `CGD_Types.mqh`, `CGD_DivergenceField.mqh`
- `EXP0017_CG_Divergence_Anatomy.mq5`

The adapter intentionally invokes the same time and divergence classes instead of reproducing formulas. This reduces semantic drift and creates a measurable migration seam.
