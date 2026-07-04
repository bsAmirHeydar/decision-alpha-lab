# DATA-R01 — Canonical State Packet v1

## Purpose
چون rule engine، AI، backtest، shadow، paper و execution باید همه از یک زبان مشترک استفاده کنند. این زبان همان state packet استاندارد NDS است.

## Required Clarifications
- در هر لحظه، Node state باید چه فیلدهایی داشته باشد؟
- CycleHook state شامل چه چیزهایی باشد؟
- Sequence state، X/Y closure و Hook type چطور ذخیره شوند؟
- Context/position چطور وارد packet شود؟
- Zone candidates چطور ثبت شوند؟
- Scenario threads چطور ثبت شوند؟
- Entry extremes و ExecutionIntentها چطور وصل شوند؟
- Destinations و optionality چطور ذخیره شوند؟
- Risk state و pending orders چطور وارد packet شوند؟
- Parent-child fractal relations چطور استاندارد شوند؟

## Image Requirement
خیر. پاسخ متنی کافی است.

## Expected Derived Outputs
- `canonical_state_packet_v1.csv`
- `nds_state_schema_v1.csv`
- `state_packet_versioning_v1.csv`
