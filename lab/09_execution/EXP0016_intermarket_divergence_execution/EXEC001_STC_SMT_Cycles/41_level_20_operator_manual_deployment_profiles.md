# Level 20 — Operator Manual and Deployment Profiles

## Scope

Level 20 is a documentation and deployment-control layer for `EXEC001_STC_SMT_Cycles`.

It does not add new signal logic, does not change SMT detection, does not change risk geometry, does not change paper outcomes, and does not send broker orders by itself. Its purpose is to make the existing Level 01 through Level 19 stack operable without ambiguity.

The strategy now has many independent safety switches. That is intentional, but it also means the operator needs a precise runbook. Level 20 defines that runbook.

## Why this layer exists

The STC strategy is not a simple indicator. It contains:

1. New York time conversion.
2. STC trading-day state.
3. M/W cycle classification.
4. Check-candle aggregation.
5. W high/low construction.
6. Previous-W reference matrix.
7. Touch-only hunt detection.
8. SMT candidate generation.
9. Signal confirmation and consumption.
10. No-late-entry protection.
11. Paper entry and risk modeling.
12. Paper outcome simulation.
13. Paper partial and hard-close simulation.
14. Restart persistence.
15. Visualization.
16. Paper-live alerts.
17. Magic-only broker scan.
18. Optional real auto-entry.
19. Optional real partial close.
20. Optional real hard-close finalizer.
21. Validation pack.

A single wrong input can turn a safe observer into a real trading engine. This manual separates runtime modes from transport switches so that deployment is explicit and auditable.

## Canonical operating principle

The strategy has three conceptual layers:

### 1. Research layer

This layer reads historical candles, builds STC state, detects SMT, plans paper entries, and produces reports. It must never touch broker positions.

### 2. Paper-live layer

This layer runs the same logic in live time and emits alerts and drawings. It can scan broker positions for audit, but it must not open or close real trades unless explicit overrides are enabled.

### 3. Auto-trade layer

This layer can convert confirmed signals into real market orders and can manage real partial and hard close actions. It must only manage positions with the configured STC magic number.

## Golden rules

1. `Symbol1` and `Symbol2` are both data symbols and execution symbols.
2. The chart symbol is not the strategy symbol. The EA may be attached to either Symbol1 or Symbol2, but the logic only uses the configured pair.
3. A duplicate EA instance for the same account, strategy, pair, and magic number must be blocked.
4. Only positions with `InpMagicNumber` are strategy-managed.
5. Manual or foreign positions must never be closed by the STC engine.
6. Real auto-entry must be off by default.
7. Real partial close must be off by default.
8. Real hard close finalizer must be off by default.
9. All real transports require explicit operator activation.
10. Validation must be checked before live deployment.

## Deployment readiness gates

Before any real trading profile is used, all of these must be true:

1. MetaEditor compilation succeeds with zero errors.
2. `stc_level19_validation_summary.csv` reports `PASS` or `PASS_WITH_WARNINGS` only for known non-fatal warnings.
3. New York time in the dashboard matches actual New York time.
4. The active M/W state on the chart matches the expected STC calendar.
5. `Symbol1` and `Symbol2` both have live quotes and M1 history.
6. The broker UTC offset input is correct for the broker server.
7. The configured magic number is unique to this deployment.
8. The output folder is writable.
9. Paper-live alerts have been observed for at least one full STC trading day.
10. No duplicate instance lock conflicts appear except the intended protection.
11. Broker position audit shows foreign positions are not managed.
12. The account is suitable for automated execution.

## Runtime modes

The strategy exposes three logical runtime modes.

### Research Backtest

Use this when the purpose is historical analysis, audit CSV generation, paper outcome simulation, and validation.

Expected behavior:

- No real orders.
- No real partial close.
- No real hard close.
- No live alert spam from historical backfill.
- Full CSV reporting.
- Optional drawings for visual audit.

### Paper Live

Use this for live monitoring without execution.

Expected behavior:

- New signals create alerts.
- Paper entries are generated.
- Paper outcomes are tracked.
- Drawings update.
- Broker positions may be scanned only for audit.
- No real entry unless explicitly overridden, which is not recommended for normal Paper Live.
- No real partial or hard close unless explicitly overridden.

### Auto Trade

Use this only after research and paper-live validation.

Expected behavior:

- Confirmed signals may become real market orders.
- Real entries use the same entry/SL/TP geometry as the paper plan.
- Real positions are tagged with the configured magic number.
- Real partial close can be enabled separately.
- Real hard close finalizer can be enabled separately.
- Foreign/manual positions remain untouched.

## Transport switches

Runtime mode alone is not enough. Real execution requires transport switches.

### Real auto-entry transport

Controlled by:

- `InpEnableRealAutoEntry`
- `InpAllowAutoEntryInPaperLive`
- `InpAutoEntryRequiresBrokerManager`

Normal production rule:

- Real auto-entry is allowed only in Auto Trade mode.
- Paper Live real-entry override should remain false except controlled experiments.

### Real partial transport

Controlled by:

- `InpEnableRealPartialClose`
- `InpAllowRealPartialInPaperLive`
- `InpRealPartialRequiresBrokerManager`

Normal production rule:

- Real partial close is allowed only in Auto Trade mode.
- Real partial must require Broker Position Manager.

### Real hard-close finalizer transport

Controlled by:

- `InpEnableRealHardCloseFinalizer`
- `InpAllowRealHardCloseFinalizerInPaperLive`
- `InpRealHardCloseFinalizerRequiresBrokerManager`

Normal production rule:

- Real hard close finalizer is allowed only in Auto Trade mode.
- It must close only matching magic-number positions on Symbol1/Symbol2.

## Recommended deployment profiles

Level 20 defines five operational profiles:

1. `RESEARCH_BACKTEST_FULL_AUDIT`
2. `PAPER_LIVE_OBSERVER`
3. `PAPER_LIVE_BROKER_AUDIT`
4. `AUTO_TRADE_ENTRY_ONLY_REHEARSAL`
5. `AUTO_TRADE_FULL_MANAGED`
6. `EMERGENCY_HARD_CLOSE_ONLY`

The detailed profile matrix is documented in `42_level_20_profile_matrix.md` and the profile-specific files under `deployment_profiles/`.

## Daily runbook

### Before 20:00 New York

1. Attach the EA to one chart only.
2. Set `Symbol1` and `Symbol2`.
3. Set broker UTC offset.
4. Set check candle timeframe.
5. Set risk percent and final reward.
6. Confirm runtime mode.
7. Confirm all real transport switches are intentionally set.
8. Confirm validation summary is acceptable.
9. Confirm output folder is writable.
10. Confirm duplicate instance lock is clean.

### During M1, M2, and M3

Monitor:

- dashboard time state;
- check candle audit;
- W level audit;
- reference hunt audit;
- SMT candidate audit;
- signal registry;
- paper entry plan;
- paper outcome;
- broker positions if broker manager is enabled;
- alert audit in paper live;
- auto-entry audit in auto trade.

Do not manually edit the CSV files while the EA is running.

### During gap zones

No new detection or entry is expected.

Managed positions may still hit SL or TP because broker-side SL/TP remains active. The EA must not create new STC signals in gap zones.

### At W4 end of M1 and M2

If partial is enabled:

- paper partial audit should appear;
- real partial should only appear if real partial transport is enabled;
- delayed partial recovery may occur if the EA was offline at the exact W4 boundary.

### At 15:30 New York

Hard close becomes the daily authority.

Expected behavior:

- paper hard-close audit is generated for unresolved paper positions;
- real hard-close finalizer may attempt close only if explicitly enabled;
- no M3 partial is required;
- after 15:30 no strategy-managed position should remain open if the finalizer is active and broker execution succeeds.

### After 15:30 and before 20:00

This is reset/no-entry territory. The operator should review:

- hard close actions;
- real hard close finalizer actions;
- unclosed position alerts;
- validation summary;
- daily reports.

## Incident response

### Wrong time state

If New York time or M/W state is wrong:

1. Disable real transports immediately.
2. Check broker UTC offset.
3. Restart the EA in Paper Live.
4. Verify validation TIME_MATRIX.
5. Do not enable Auto Trade until time state is correct.

### Duplicate instance warning

If duplicate instance lock appears:

1. Remove duplicate EA instances.
2. Keep only one chart running the strategy for the same pair/magic/account.
3. Restart the intended instance.

### Unexpected real order

If a real order appears unexpectedly:

1. Set `InpEnableRealAutoEntry=false`.
2. Set `InpEnableRealPartialClose=false`.
3. Set `InpEnableRealHardCloseFinalizer=false`.
4. Inspect `stc_level16_auto_entries.csv` and broker action logs.
5. Confirm runtime mode and transport overrides.

### Position remains open after 15:30

1. Check whether the position magic matches `InpMagicNumber`.
2. Check whether real hard close finalizer is enabled.
3. Check `stc_level18_real_hard_close_finalizer.csv`.
4. If max attempts are reached, manual review is required.

## Operator acceptance criteria

Level 20 is accepted when:

1. The operator can choose a deployment profile without guessing input intent.
2. Every real transport has a documented gate.
3. Paper Live can run without real execution.
4. Auto Trade Full Managed requires explicit real transport activation.
5. Emergency Hard Close Only can be configured without auto-entry.
6. The documentation clearly separates paper behavior from broker behavior.
7. The deployment plan is reproducible from a clean terminal restart.

