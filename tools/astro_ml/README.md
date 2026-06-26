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

---

# Human-Learning One-Command Protocol

Use this when you want the system to do the whole research loop itself:

```powershell
.\tools\astro_ml\run_astro_human_learning_protocol_common.ps1 `
  -Asset NAS100 `
  -Symbol NAS100 `
  -Timeframe M1 `
  -From "2026-06-22 00:00" `
  -To "2026-06-27 23:59" `
  -Preset sanity `
  -Horizons "30,60,120" `
  -OpenAfter
```

This does:

1. Fetch MT5 candles with `fetch_mt5_rates.py`.
2. Resolve/build astro features with `resolve_astro_feature_store.py`.
3. Build causal dataset with future outcomes.
4. Run the professional ML protocol.
5. Build skeptical cognitive memory with `build_cognitive_astro_memory.py`.

For multi-year research use `-Preset professional -RunWalkForward` and higher cognitive support thresholds.
