# Astro ML Tools

راهنمای کامل استفاده در این فایل است:

```text
lab/03_experiments/EXP0016_astro_meta_learner/README.md
```

ساده‌ترین دستور عملیاتی:

```powershell
.\tools\astro_ml\run_astro_ml_protocol_common.ps1 `
  -AstroCsvName "astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv" `
  -PriceCsvName "astro_ml_prices_NAS100_M1_20260622_to_now.csv" `
  -Asset NAS100 `
  -Timeframe M1 `
  -Preset sanity `
  -OpenAfter
```
