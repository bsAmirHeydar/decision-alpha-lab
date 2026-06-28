# Level 16 — Real Auto Entry Router

## Status

Level 16 is the first layer that can convert an already-confirmed STC SMT signal into a real broker entry order. It does not change the strategy logic. It only mirrors the Level 08 paper entry geometry into broker orders when all safety gates are explicitly enabled.

The layer remains disabled by default.

## Non-negotiable locked rules preserved

The router preserves the existing STC rules:

- the EA uses only `Symbol1` and `Symbol2`;
- the chart symbol does not drive the strategy;
- SMT is structural per symbol;
- high-side SMT maps to a sell on the clean symbol;
- low-side SMT maps to a buy on the clean symbol;
- entry is attempted only at the next check-candle open after signal confirmation;
- no delayed entry is allowed after the grace window expires;
- Entry STC OFF creates audit rows only and no later real entry;
- simultaneous buy and sell in one check candle is forgotten;
- each M cycle allows at most three real entries across both symbols;
- with hedging OFF, direction lock applies only inside the current M;
- opposite directions may occur in different M cycles;
- SL is exactly the selected reference W level for the traded clean symbol;
- TP is Final Reward R from the raw SL distance;
- costs do not change SL or TP geometry;
- real positions are managed only by magic number.

## What Level 16 adds

Level 16 adds a real order router after the audit/paper pipeline:

1. The Level 06 SMT candidate engine builds candidates.
2. The Level 07 signal registry confirms and consumes signals.
3. The Level 08 paper entry model builds entry, SL, TP, risk, and volume.
4. Level 16 rebuilds the same candidate/signal/paper geometry for the newly closed check candle.
5. If all auto-trade safety gates pass, it sends real market orders using the clean symbol.
6. It attaches SL and TP to the broker order.
7. It records every allow/reject/send/fail state in `stc_level16_auto_entries.csv`.

## Safety gates

A real entry can be sent only when all of these are true:

- `InpRuntimeMode = STC_MODE_AUTO_TRADE`, unless paper-live override is explicitly enabled;
- `InpEnableRealAutoEntry = true`;
- `InpEntrySTC = true` at confirmation time;
- the signal belongs to a newly closed check candle;
- the entry check start is within `InpAutoEntryGraceSeconds`;
- pair data is complete;
- the paper plan is valid;
- risk distance is valid;
- volume is at or above broker minimum;
- the number of required split orders is not above `InpMaxAutoSplitOrders`;
- max-three-real-trades-per-M is not exceeded;
- hedging direction lock is not violated;
- if `InpAutoEntryRequiresBrokerManager=true`, the broker position manager must be enabled.

If any gate fails, no real order is sent and an audit row is written.

## New inputs

`InpEnableRealAutoEntry` defaults to `false`. This is the master switch for real entry orders.

`InpWriteAutoEntryAudit` controls `stc_level16_auto_entries.csv`.

`InpAutoEntryGraceSeconds` defines the maximum allowed delay after the entry check starts. If the EA was offline or late beyond this window, no real entry is sent.

`InpAutoEntryDeviationPoints` is the broker deviation used when sending market orders.

`InpMaxAutoSplitOrders` caps the number of split market orders used when calculated volume exceeds the broker maximum.

`InpAllowAutoEntryInPaperLive` is disabled by default. It exists only for controlled testing. Normal real entry requires `AUTO_TRADE` mode.

`InpAutoEntryRequiresBrokerManager` defaults to true. This keeps the real entry router dependent on the magic-only broker position manager layer.

`InpAutoEntryOrderCommentPrefix` is the order comment prefix. The router truncates comments to broker-safe length.

## Split order behavior

The owner decision says the EA should not internally cap volume, but broker min/max must be respected. Level 16 therefore behaves as follows:

- if calculated volume is below broker minimum, entry is rejected;
- if calculated volume is within broker limits, one order is sent;
- if calculated volume is above broker maximum, the router splits it into chunks;
- each chunk is normalized down to broker volume step;
- if required chunks exceed `InpMaxAutoSplitOrders`, entry is rejected;
- if one split chunk fails, the router stops sending further chunks and records the partial send state.

## Real order geometry

For BUY:

- market buy on the clean symbol;
- SL = selected reference W low for the clean symbol;
- TP = entry + FinalRewardR × risk distance.

For SELL:

- market sell on the clean symbol;
- SL = selected reference W high for the clean symbol;
- TP = entry - FinalRewardR × risk distance.

The router uses the same risk and volume model as Level 08.

## No late entry rule

The router baselines current-day history on init. It will not send historical entries after restart.

On every timer pulse, it processes only newly closed check candles. If the resulting entry moment is older than `InpAutoEntryGraceSeconds`, the row is rejected as late.

This preserves the owner rule: if the EA was off at the exact entry time, it must not enter later.

## Output

The new output file is:

`stc_level16_auto_entries.csv`

Important fields:

- `signal_check_index`
- `entry_check_index`
- `signal_id`
- `paper_trade_id`
- `auto_order_group_id`
- `direction`
- `trade_symbol`
- `entry_reference_price`
- `stop_price`
- `take_profit_price`
- `theoretical_volume`
- `requested_total_volume`
- `sent_total_volume`
- `planned_split_orders`
- `attempted_orders`
- `successful_orders`
- `transport_allowed`
- `grace_window_ok`
- `order_attempted`
- `any_order_succeeded`
- `last_retcode`
- `last_trade_comment`
- `auto_status`
- `rule_note`

## Acceptance criteria

Level 16 is accepted when:

- it compiles;
- real entry is impossible with default inputs;
- real entry is impossible in research mode;
- real entry is impossible in paper live unless explicitly overridden;
- real entry is possible in auto trade only when `InpEnableRealAutoEntry=true`;
- orders are sent only on Symbol1 or Symbol2;
- orders use the configured magic number;
- SL and TP match the Level 08 paper plan;
- late entries are rejected;
- max three real entries per M is enforced;
- direction lock is enforced only inside the current M;
- split orders obey broker max and user split limit;
- all attempts and rejections are audit logged.

## Still deferred

Level 16 does not yet implement real partial close from strategy state. It also does not replace Level 15 hard close logic, which already handles magic-only hard close when enabled. Future levels can extend the broker manager to match real positions back to specific signal IDs.
