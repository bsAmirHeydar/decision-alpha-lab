#ifndef __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"

#define FP_NDS_F2_WAIST_TRADE_VERSION "NDS-F2-WAIST-01"
#define FP_NDS_F2_WAIST_TRADE_SCHEMA_VERSION "nds_f2_waist_limit_v1"

enum FP_NDSF2WaistTradeAction
{
   FP_NDS_F2_ACTION_NONE = 0,
   FP_NDS_F2_ACTION_PAPER_LIMIT = 1,
   FP_NDS_F2_ACTION_LIMIT_SENT = 2,
   FP_NDS_F2_ACTION_PENDING_HELD = 3,
   FP_NDS_F2_ACTION_POSITION_HELD = 4,
   FP_NDS_F2_ACTION_BLOCKED = 5
};

struct FP_NDSF2WaistTradeConfig
{
   bool enabled;
   bool send_tester_orders;
   bool require_visible_main;
   bool one_attempt_per_f2;
   bool reset_used_setups_on_init;
   int max_setup_age_bars;

   FP_NDSHookTradeSizingMode sizing_mode;
   double fixed_volume;
   double risk_cash;
   double commission_per_lot_round_turn;
   bool allow_min_lot_if_risk_too_small;

   double entry_offset_points;
   int max_deviation_points;
   int entry_lock_timeout_seconds;
   long magic;
   string comment_prefix;
};

struct FP_NDSF2WaistTradeSetup
{
   bool available;
   bool eligible;
   bool already_used;
   string status;
   string reason;

   int f1_event_id;
   int f2_event_id;
   int sequence_id;
   int direction;
   int scale_L;
   datetime f2_confirm_time;

   double f1_waist_price;
   double f2_waist_price;
   double f2_leg2_price;
   double entry_price;
   double stop_price;
   double target_price;
   double volume;

   string setup_key;
   string broker_comment;
};

struct FP_NDSF2WaistTradeReport
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;

   bool attempted;
   bool ok;
   FP_NDSF2WaistTradeAction action;
   string status;
   string reason;

   int managed_pending_count;
   int managed_position_count;
   int foreign_symbol_position_count;
   ulong order_ticket;
   ulong position_ticket;

   FP_NDSF2WaistTradeSetup setup;
};

void FP_ResetNDSF2WaistTradeConfig(FP_NDSF2WaistTradeConfig &cfg)
{
   cfg.enabled = true;
   cfg.send_tester_orders = true;
   cfg.require_visible_main = true;
   cfg.one_attempt_per_f2 = true;
   cfg.reset_used_setups_on_init = false;
   cfg.max_setup_age_bars = 1;

   cfg.sizing_mode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
   cfg.fixed_volume = 0.01;
   cfg.risk_cash = 100.0;
   cfg.commission_per_lot_round_turn = 0.0;
   cfg.allow_min_lot_if_risk_too_small = false;

   cfg.entry_offset_points = 1.0;
   cfg.max_deviation_points = 20;
   cfg.entry_lock_timeout_seconds = 30;
   cfg.magic = 310055;
   cfg.comment_prefix = "NDSF2";
}

void FP_ResetNDSF2WaistTradeSetup(FP_NDSF2WaistTradeSetup &s)
{
   s.available = false;
   s.eligible = false;
   s.already_used = false;
   s.status = "RESET";
   s.reason = "reset";
   s.f1_event_id = -1;
   s.f2_event_id = -1;
   s.sequence_id = -1;
   s.direction = FP_DIR_NONE;
   s.scale_L = 0;
   s.f2_confirm_time = 0;
   s.f1_waist_price = 0.0;
   s.f2_waist_price = 0.0;
   s.f2_leg2_price = 0.0;
   s.entry_price = 0.0;
   s.stop_price = 0.0;
   s.target_price = 0.0;
   s.volume = 0.0;
   s.setup_key = "";
   s.broker_comment = "";
}

void FP_ResetNDSF2WaistTradeReport(FP_NDSF2WaistTradeReport &r)
{
   r.generated_at = TimeCurrent();
   r.version = FP_NDS_F2_WAIST_TRADE_VERSION;
   r.schema_version = FP_NDS_F2_WAIST_TRADE_SCHEMA_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.attempted = false;
   r.ok = false;
   r.action = FP_NDS_F2_ACTION_NONE;
   r.status = "RESET";
   r.reason = "reset";
   r.managed_pending_count = 0;
   r.managed_position_count = 0;
   r.foreign_symbol_position_count = 0;
   r.order_ticket = 0;
   r.position_ticket = 0;
   FP_ResetNDSF2WaistTradeSetup(r.setup);
}

#endif // __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
