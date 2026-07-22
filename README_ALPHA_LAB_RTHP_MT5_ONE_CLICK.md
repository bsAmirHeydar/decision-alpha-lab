# Alpha Lab RTHP MT5 One-Click Implementation

This patch implements the context-owned, read-only MetaTrader 5 M1 acquisition and one-click RTHP research-training adapter.

## Operator path

```powershell
$env:PYTHONPATH = "lab\11_strategy_factory\python"
python -m strategy_factory_rthp_mt5_activation_v1 preflight-symbols --primary <PRIMARY> --secondary <SECONDARY>
python -m strategy_factory_rthp_mt5_activation_v1 run-symbols --primary <PRIMARY> --secondary <SECONDARY>
```

## Boundaries

- Closed M1 bars are the canonical floor.
- Sub-M1 data and raw ticks are excluded.
- No synthetic tick path or M1 intrabar ordering is created.
- The MT5 adapter is read-only.
- Central engines and Canonical RTHP Context 1.0.2 remain unchanged.
- A real terminal smoke run remains external evidence and is not claimed by this build.
