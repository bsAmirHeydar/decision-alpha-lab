# Install EXP0017 Phase 06 Hotfix006 — Minimal Line-Only Visual Mode

This patch turns Phase 06 visual output into a line-first, text-free chart language by default. It keeps dual-symbol drawing and historical backfill while suppressing text labels and visual clutter.

Compile after install:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Recommended cleanup before attaching EA:

```text
Delete all objects with prefix EXP0017_P06_
```
