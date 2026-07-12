#ifndef __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"

#define FP_NDS_F2_WAIST_TRADE_VERSION "NDS-F2-WAIST-BREAK-04"
#define FP_NDS_F2_WAIST_TRADE_SCHEMA_VERSION "nds_f2_waist_break_point2_v4"

enum FP_NDSF2WaistRunResult
{
   FP_NDS_F2_RUN_IDLE = 0,
   FP_NDS_F2_RUN_PAPER = 1,
   FP_NDS_F2_RUN_ORDER_SENT = 2,
   FP_NDS_F2_RUN_PENDING_HELD = 3,
   FP_NDS_F2_RUN_POSITION_HELD = 4,
   FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED = 5,
   FP_NDS_F2_RUN_BLOCKED = 6,
   FP_NDS_F2_RUN_ERROR = 7,
   FP_NDS_F2_RUN_MULTI_ORDER_SENT = 8
};

struct FP_NDSF2WaistTradeConfig
{
   bool enabled;
   bool send_tester_orders;
   bool one_attempt_per_f2_body;
   bool reset_used_setups_on_init;
   bool require_f2_size_gate;
   bool cancel_pending_if_target_touched_before_fill;
   int max_setup_age_bars;

   // Opportunity geometry filter.
   bool use_min_reward_risk_filter;
   double min_reward_risk;

   // Parallel-context policy. Distinct setup_hash values are distinct contexts.
   // Independent parallel positions require an MT5 hedging account. On netting
   // accounts, a second exposure is blocked to preserve per-context SL/TP.
   bool allow_opposite_direction_hedge;
   bool allow_same_direction_multiple_contexts;
   int max_concurrent_managed_exposures; // 0 = unlimited by strategy policy.

   FP_NDSHookTradeSizingMode sizing_mode;
   double fixed_volume;
   double risk_cash;
   double commission_per_lot_round_turn;
   bool allow_min_lot_if_risk_too_small;

   double entry_behind_f2_waist_ticks;
   double stop_behind_f1_waist_ticks;
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
   int body_available_index;
   int age_bars;
   datetime body_available_time;

   // Structural anatomy:
   // point_1 = F2 waist
   // point_2 = first strict price penetration beyond F2 waist; the pending
   // limit is placed there in advance, so its fill is the executable Point 2.
   double point_1_price;
   double point_2_limit_price;
   double parent_f1_waist_price;
   double f2_flag_end_price;

   double entry_price;
   double stop_price;
   double target_price;
   double risk_distance;
   double reward_distance;
   double reward_risk;
   double volume;

   long setup_hash;
   string broker_comment;
};

void FP_ResetNDSF2WaistTradeConfig(FP_NDSF2WaistTradeConfig &cfg)
{
   cfg.enabled = true;
   cfg.send_tester_orders = true;
   cfg.one_attempt_per_f2_body = true;
   cfg.reset_used_setups_on_init = false;
   cfg.require_f2_size_gate = false;
   cfg.cancel_pending_if_target_touched_before_fill = true;
   cfg.max_setup_age_bars = 0;

   cfg.use_min_reward_risk_filter = true;
   cfg.min_reward_risk = 1.0;
   cfg.allow_opposite_direction_hedge = true;
   cfg.allow_same_direction_multiple_contexts = true;
   cfg.max_concurrent_managed_exposures = 0;

   cfg.sizing_mode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
   cfg.fixed_volume = 0.01;
   cfg.risk_cash = 100.0;
   cfg.commission_per_lot_round_turn = 0.0;
   cfg.allow_min_lot_if_risk_too_small = false;

   cfg.entry_behind_f2_waist_ticks = 1.0;
   cfg.stop_behind_f1_waist_ticks = 1.0;
   cfg.max_deviation_points = 20;
   cfg.magic = 310055;
   cfg.comment_prefix = "NDSF2WB";
}

void FP_ResetNDSF2WaistTradeSetup(FP_NDSF2WaistTradeSetup &s)
{
   s.eligible = false;
   s.direction = FP_DIR_NONE;
   s.scale_L = 0;
   s.f1_event_id = -1;
   s.f2_event_id = -1;
   s.sequence_id = -1;
   s.body_available_index = -1;
   s.age_bars = -1;
   s.body_available_time = 0;
   s.point_1_price = 0.0;
   s.point_2_limit_price = 0.0;
   s.parent_f1_waist_price = 0.0;
   s.f2_flag_end_price = 0.0;
   s.entry_price = 0.0;
   s.stop_price = 0.0;
   s.target_price = 0.0;
   s.risk_distance = 0.0;
   s.reward_distance = 0.0;
   s.reward_risk = 0.0;
   s.volume = 0.0;
   s.setup_hash = 0;
   s.broker_comment = "";
}

#endif // __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
