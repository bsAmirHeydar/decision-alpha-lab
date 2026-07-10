#ifndef __FP_NDS_HOOK_TRADE_TYPES_MQH__
#define __FP_NDS_HOOK_TRADE_TYPES_MQH__
#property strict

#include "FP_NDSEntryTypes.mqh"

#define FP_NDS_HOOK_TRADE_VERSION "NDS-HOOK-TRADE-01"
#define FP_NDS_HOOK_TRADE_SCHEMA_VERSION "nds_hook_limit_f123_exit_v1"

enum FP_NDSHookTradeSizingMode
{
   FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME = 0,
   FP_NDS_HOOK_TRADE_SIZE_RISK_CASH = 1
};

enum FP_NDSHookTradeAction
{
   FP_NDS_HOOK_TRADE_ACTION_NONE = 0,
   FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT = 1,
   FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT = 2,
   FP_NDS_HOOK_TRADE_ACTION_PENDING_HELD = 3,
   FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD = 4,
   FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED = 5,
   FP_NDS_HOOK_TRADE_ACTION_POSITION_CLOSED_F3 = 6,
   FP_NDS_HOOK_TRADE_ACTION_BLOCKED = 7
};

struct FP_NDSHookTradeConfig
{
   bool enabled;
   bool send_live_orders;
   bool allow_hook_after_hook;
   bool allow_hook_after_f3;
   bool require_closed_hook;
   bool one_attempt_per_hook;
   bool reset_used_setups_on_init;
   bool cancel_pending_on_death;
   bool require_full_f123_after_entry;
   bool export_csv;
   bool print_summary;

   FP_NDSHookTradeSizingMode sizing_mode;
   double fixed_volume;
   double risk_cash;
   double commission_per_lot_round_turn;
   bool allow_min_lot_if_risk_too_small;

   int stop_buffer_points;
   double stop_spread_multiplier;
   int max_deviation_points;
   int entry_lock_timeout_seconds;
   long magic;
   string comment_prefix;
   string folder;
};

struct FP_NDSHookTradeSetup
{
   bool available;
   bool eligible;
   bool already_used;
   string status;
   string reason;

   int sequence_id;
   int direction;
   string direction_label;
   string family;
   bool valid_after_hook;
   bool valid_after_f3;
   datetime structure_time;
   double entry_price;
   double death_price;
   double stop_price;
   double volume;
   string setup_key;
   string broker_comment;
};

struct FP_NDSHookTradeExitSignal
{
   bool found;
   int event_id;
   int sequence_id;
   int direction;
   datetime f1_start_time;
   datetime f2_start_time;
   datetime f3_terminal_time;
   double f3_terminal_price;
   string reason;
};

struct FP_NDSHookTradeReport
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;

   bool attempted;
   bool ok;
   FP_NDSHookTradeAction action;
   string action_label;
   string status;
   string reason;

   int managed_pending_count;
   int managed_position_count;
   int foreign_symbol_position_count;
   ulong order_ticket;
   ulong position_ticket;
   ulong close_ticket;

   FP_NDSHookTradeSetup setup;
   FP_NDSHookTradeExitSignal exit_signal;
   string state_key;
};

void FP_ResetNDSHookTradeConfig(FP_NDSHookTradeConfig &cfg)
{
   cfg.enabled = false;
   cfg.send_live_orders = false;
   cfg.allow_hook_after_hook = true;
   cfg.allow_hook_after_f3 = true;
   cfg.require_closed_hook = true;
   cfg.one_attempt_per_hook = true;
   cfg.reset_used_setups_on_init = false;
   cfg.cancel_pending_on_death = true;
   cfg.require_full_f123_after_entry = true;
   cfg.export_csv = true;
   cfg.print_summary = true;

   cfg.sizing_mode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
   cfg.fixed_volume = 0.01;
   cfg.risk_cash = 100.0;
   cfg.commission_per_lot_round_turn = 0.0;
   cfg.allow_min_lot_if_risk_too_small = false;

   cfg.stop_buffer_points = 1;
   cfg.stop_spread_multiplier = 1.0;
   cfg.max_deviation_points = 20;
   cfg.entry_lock_timeout_seconds = 30;
   cfg.magic = 310052;
   cfg.comment_prefix = "NDSH";
   cfg.folder = "FlagCountingPhoenix";
}

void FP_ResetNDSHookTradeSetup(FP_NDSHookTradeSetup &s)
{
   s.available = false;
   s.eligible = false;
   s.already_used = false;
   s.status = "RESET";
   s.reason = "reset";
   s.sequence_id = -1;
   s.direction = FP_DIR_NONE;
   s.direction_label = "NONE";
   s.family = "NONE";
   s.valid_after_hook = false;
   s.valid_after_f3 = false;
   s.structure_time = 0;
   s.entry_price = 0.0;
   s.death_price = 0.0;
   s.stop_price = 0.0;
   s.volume = 0.0;
   s.setup_key = "";
   s.broker_comment = "";
}

void FP_ResetNDSHookTradeExitSignal(FP_NDSHookTradeExitSignal &x)
{
   x.found = false;
   x.event_id = -1;
   x.sequence_id = -1;
   x.direction = FP_DIR_NONE;
   x.f1_start_time = 0;
   x.f2_start_time = 0;
   x.f3_terminal_time = 0;
   x.f3_terminal_price = 0.0;
   x.reason = "none";
}

void FP_ResetNDSHookTradeReport(FP_NDSHookTradeReport &r)
{
   r.generated_at = TimeCurrent();
   r.version = FP_NDS_HOOK_TRADE_VERSION;
   r.schema_version = FP_NDS_HOOK_TRADE_SCHEMA_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.attempted = false;
   r.ok = false;
   r.action = FP_NDS_HOOK_TRADE_ACTION_NONE;
   r.action_label = "NONE";
   r.status = "RESET";
   r.reason = "reset";
   r.managed_pending_count = 0;
   r.managed_position_count = 0;
   r.foreign_symbol_position_count = 0;
   r.order_ticket = 0;
   r.position_ticket = 0;
   r.close_ticket = 0;
   FP_ResetNDSHookTradeSetup(r.setup);
   FP_ResetNDSHookTradeExitSignal(r.exit_signal);
   r.state_key = "";
}

#endif // __FP_NDS_HOOK_TRADE_TYPES_MQH__
