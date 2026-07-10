  ---
  id: EXP0018-CORE-OPTIONAL-BOUNDARY-V2
  title: "EXP0018 Core vs Optional Boundary v2"
  type: contract
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# مرز Core و Optional

## Core P00–P13

- ۲۲ رابطه Word
- A/L/N/P و a1..p4
- touch-only hunt با equality
- hunter/protected
- close confirmation
- first-sweep/reference retirement
- hunter-only immutable lines
- session boxes
- TWO/TDO
- historical replay، audit و QA

## Optional P14–P20

- TYO/TMO/TSO/TMSO و stacked opens
- DFR و projection
- انواع SSMT
- AMDX/XAMD و Golden Pocket به‌عنوان context
- news adapter
- triad/intermarket observer
- outcome study و promotion gate

## قانون dependency

```text
Core → Optional is allowed
Optional → Core is forbidden
```

Optional فقط می‌تواند eventهای Core را بخواند؛ نمی‌تواند Core signal را حذف، تأیید یا بازنویسی کند مگر پس از Phase 20 و ADR انسانی نسخه‌دار.
