---
title: RTHP MT5 Automation — Target Operator Experience
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, operator-experience, one-click]
---

# Target Operator Experience

## Primary operator flow

The normal production workflow must require only two symbol selections:

```text
Primary symbol:   <broker symbol A>
Secondary symbol: <broker symbol B>
```

The system then automatically:

1. discovers or opens the configured MT5 terminal;
2. validates connection and read access;
3. resolves both symbols and freezes metadata;
4. determines the maximum common valid M1 history under the selected research profile;
5. downloads closed M1 bars in bounded chunks;
6. validates quality and cross-symbol overlap;
7. writes immutable canonical source artifacts;
8. materializes RTHP cycles, references, touches, confirmations, occurrences, states, and price paths;
9. resolves data binding and hashes;
10. builds features, labels, dependence clusters, splits, and immutable batch artifacts;
11. delegates training to the existing trainer engines;
12. verifies the completed run.

## Target command

```powershell
python -m strategy_factory_rthp_mt5_activation_v1 run `
  --primary-symbol <BROKER_SYMBOL_A> `
  --secondary-symbol <BROKER_SYMBOL_B>
```

Optional overrides may exist for terminal path, account profile, date range, output root, and research profile, but they must not be required for the default path.

## Fail-closed operator prompts

The system may ask for one additional choice only when deterministic resolution is impossible, for example:

- more than one broker symbol matches the requested alias;
- more than one installed terminal is active with different servers;
- contract-roll policy is required but not registered;
- common history is below the minimum research threshold.

It must never guess through these ambiguities.
