# 08 — State and Data Model

## 1. Objective

This document defines the runtime state needed for the CG Intermarket Divergence EA.

The state model must be small, deterministic, and reset at the New York trading-day boundary.

## 2. Same-day state boundary

The EA only needs current-day state for new signal generation.

At each new New York trading day starting 18:00:

```text
clear signal registry
clear intraday divergence events
clear same-day duplicate keys
keep open position tracking only if positions still exist
```

Open positions should still be managed if they exist, but new entries must not use previous-day references.

## 3. CG configuration state

```cpp
struct CG_Config
{
   string name;
   int    duration_minutes;
   bool   trade_enabled;
   bool   draw_enabled;
   color  draw_color;
};
```

There should be exactly 21 configs in the baseline system.

## 4. Cycle context state

```cpp
struct CG_CycleContext
{
   string   trading_day_key;
   string   cg_name;
   int      duration_minutes;
   int      current_cycle_index;
   int      reference_cycle_index;
   datetime day_start_broker;
   datetime day_end_broker;
   datetime current_cycle_start_broker;
   datetime current_cycle_end_broker;
   datetime reference_cycle_start_broker;
   datetime reference_cycle_end_broker;
   bool     inside_trading_day;
   bool     has_reference_cycle;
   bool     current_cycle_is_final_partial;
};
```

## 5. Reference level state

```cpp
struct CG_ReferenceLevels
{
   bool   valid;
   string symbol_a;
   string symbol_b;
   double a_high;
   double a_low;
   double b_high;
   double b_low;
   int    a_bars_count;
   int    b_bars_count;
};
```

Invalid if:

- no bars for Symbol A;
- no bars for Symbol B;
- reference cycle not completed;
- symbol data unavailable.

## 6. Confirmation candle state

```cpp
struct CG_ConfirmationBar
{
   datetime bar_open_time_broker;
   datetime bar_close_time_broker;
   double   a_high;
   double   a_low;
   double   b_high;
   double   b_low;
   bool     valid;
};
```

The confirmation candle should be the last closed bar on the EA chart timeframe.

## 7. Hunt state

```cpp
struct CG_HuntState
{
   bool   a_high_hunt;
   bool   b_high_hunt;
   bool   a_low_hunt;
   bool   b_low_hunt;
   double a_high_touch_price;
   double b_high_touch_price;
   double a_low_touch_price;
   double b_low_touch_price;
   datetime a_high_first_touch_time;
   datetime b_high_first_touch_time;
   datetime a_low_first_touch_time;
   datetime b_low_first_touch_time;
};
```

First touch time is used for drawing.

## 8. Divergence event state

```cpp
struct CG_DivergenceEvent
{
   bool     valid;
   bool     conflict;
   string   signal_key;
   string   trading_day_key;
   string   cg_name;
   int      duration_minutes;
   int      current_cycle_index;
   int      reference_cycle_index;
   string   side; // BUY / SELL
   string   hunter_symbol;
   string   clean_symbol;
   string   trade_symbol;
   datetime confirmation_bar_open_time_broker;
   datetime confirmation_time_broker;
   datetime current_cycle_start_broker;
   datetime current_cycle_end_broker;
   datetime reference_cycle_start_broker;
   datetime reference_cycle_end_broker;
   double   hunter_reference_level;
   double   clean_reference_level;
   double   stop_loss;
   datetime scheduled_exit_time_broker;
   bool     trade_enabled;
   bool     draw_enabled;
   color    draw_color;
};
```

## 9. Signal registry state

The signal registry can use an in-memory string array for the first implementation.

```text
processed_signal_keys[]
```

Reset condition:

```text
new trading_day_key
```

Persistence is optional in first version because the user explicitly said same-day checking only and no previous-day state is needed for entry. However, if live trading is enabled, open position scheduled exits must still survive restart.

## 10. Position lifecycle state

Because the target is time-based, each trade needs a scheduled exit time.

MQL5 position comments can carry part of this data:

```text
EXP0017|cg_180m|20260709|cycle_2|exit_20260709_235900
```

But relying only on comments is fragile. A small CSV state file is recommended for live trading:

```text
MQL5/Files/EXP0017_CG_positions.csv
```

Columns:

```text
ticket,symbol,magic,signal_key,cg_name,side,entry_time,scheduled_exit_time,stop_loss,status
```

## 11. Audit files

Recommended logs:

```text
MQL5/Files/EXP0017_CG_signals.csv
MQL5/Files/EXP0017_CG_trades.csv
MQL5/Files/EXP0017_CG_errors.csv
```

Signal log columns:

```text
time,signal_key,trading_day,cg,side,hunter,clean,current_cycle,reference_cycle,hunter_ref,clean_ref,stop,scheduled_exit,trade_enabled,draw_enabled,result
```

Trade log columns:

```text
time,signal_key,symbol,side,entry,sl,lots,risk_percent,risk_money,scheduled_exit,retcode,comment
```

Error log columns:

```text
time,module,severity,code,message,signal_key,cg,symbol
```

## 12. Memory and performance

There are 21 CGs. On every new closed chart bar the EA may process all 21.

This is acceptable if:

- reference level calculation uses bounded time windows;
- only current-day data is scanned;
- duplicate keys are stored compactly;
- no expensive full-history scans occur on every tick.

The EA should not scan beyond the current trading day for signal generation.

