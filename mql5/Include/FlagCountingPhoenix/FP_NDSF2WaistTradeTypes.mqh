#ifndef __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"

#define FP_NDS_F2_WAIST_TRADE_VERSION "NDS-F2-WAIST-02"
#define FP_NDS_F2_WAIST_TRADE_SCHEMA_VERSION "nds_f2_waist_limit_v2"

enum FP_NDSF2WaistRunResult
{
   FP_NDS_F2_RUN_IDLE = 0,
   FP_NDS_F2_RUN_PAPER = 1,
   FP_NDS_F2_RUN_ORDER_SENT = 2,
   FP_NDS_F2_RUN_PENDING_HELD = 3,
   FP_NDS_F2_RUN_POSITION_HELD = 4,
   FP_NDS_F2_RUN_BLOCKED = 5,
   FP_NDS_F2_RUN_ERROR = 6
};

struct FP_NDSF2WaistTradeConfig
{
   bool enabled;
   bool send_tester_orders;
   bool one_attempt_per_f2;
   bool reset_used_setups_on_init;
   int max_setup_age_bars;

   FP_NDSHookTradeSizingMode sizing_mode;
   double fixed_volume;
   double risk_cash;
   double commission_per_lot_round_turn;
   bool allow_min_lot_if_risk_too_small;

   double entry_offset_ticks;
   int max_deviation_points;
   long magic;
   string comment_prefix;
};

struct FP_NDSF2WaistTradeSetup
{
   bool eligible;
   int direction;
   int scale_L;
   int f1_event_id;
   int f2_event_id;
   int sequence_id;
   int availability_index;
   int age_bars;
   datetime availability_time;

   double f1_waist_price;
   double f2_waist_price;
   double f2_leg2_price;
   double entry_price;
   double stop_price;
   double target_price;
   double volume;

   long setup_hash;
   string broker_comment;
};

void FP_ResetNDSF2WaistTradeConfig(FP_NDSF2WaistTradeConfig &cfg)
{
   cfg.enabled = true;
   cfg.send_tester_orders = true;
   cfg.one_attempt_per_f2 = true;
   cfg.reset_used_setups_on_init = false;
   cfg.max_setup_age_bars = 0;

   cfg.sizing_mode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
   cfg.fixed_volume = 0.01;
   cfg.risk_cash = 100.0;
   cfg.commission_per_lot_round_turn = 0.0;
   cfg.allow_min_lot_if_risk_too_small = false;

   cfg.entry_offset_ticks = 1.0;
   cfg.max_deviation_points = 20;
   cfg.magic = 310055;
   cfg.comment_prefix = "NDSF2";
}

void FP_ResetNDSF2WaistTradeSetup(FP_NDSF2WaistTradeSetup &s)
{
   s.eligible = false;
   s.direction = FP_DIR_NONE;
   s.scale_L = 0;
   s.f1_event_id = -1;
   s.f2_event_id = -1;
   s.sequence_id = -1;
   s.availability_index = -1;
   s.age_bars = -1;
   s.availability_time = 0;
   s.f1_waist_price = 0.0;
   s.f2_waist_price = 0.0;
   s.f2_leg2_price = 0.0;
   s.entry_price = 0.0;
   s.stop_price = 0.0;
   s.target_price = 0.0;
   s.volume = 0.0;
   s.setup_hash = 0;
   s.broker_comment = "";
}

#endif // __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
