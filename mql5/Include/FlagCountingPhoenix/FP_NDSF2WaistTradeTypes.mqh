#ifndef __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#define __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"

#define FP_NDS_F2_WAIST_TRADE_VERSION "NDS-F2-WAIST-BREAK-12"
#define FP_NDS_F2_WAIST_TRADE_SCHEMA_VERSION "nds_f2_waist_break_point2_v12"



enum FP_NDSF2ExitMode
{
   // Existing behavior: broker TP is attached at the original F2 two-leg end.
   FP_NDS_F2_EXIT_FIXED_F2_FLAG_END = 0,

   // Dynamic behavior: the original F2 end remains the RR reference only.
   // After F2 confirms, its confirmation node becomes F3 Leg1. Once price
   // corrects away, TP is armed at that node for the F3 flag retest.
   FP_NDS_F2_EXIT_F3_FLAG_RETEST = 1,

   // Higher-timeframe dynamic behavior: keep the position open until the first
   // canonical same-direction F3 on the configured higher timeframe forms its
   // Leg1 and then its own Waist. The Waist is the correction gate; TP is armed
   // at the end of that exact higher-timeframe F3 Leg1.
   FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST = 2
};

bool FP_NDSF2ExitModeIsDynamic(const int exit_mode)
{
   return (exit_mode == FP_NDS_F2_EXIT_F3_FLAG_RETEST ||
           exit_mode == FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST);
}

bool FP_NDSF2ExitModeUsesEntryTimeframeF3(const int exit_mode)
{
   return (exit_mode == FP_NDS_F2_EXIT_F3_FLAG_RETEST);
}

bool FP_NDSF2ExitModeUsesHigherTimeframeF3(const int exit_mode)
{
   return (exit_mode == FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST);
}


enum FP_NDSF2DynamicExitStage
{
   FP_NDS_F2_DYN_EXIT_NONE = 0,
   FP_NDS_F2_DYN_EXIT_PENDING = 1,
   FP_NDS_F2_DYN_EXIT_WAIT_EXACT_CHILD_F3 = 2,
   FP_NDS_F2_DYN_EXIT_WAIT_EXACT_F3_WAIST = 3,
   FP_NDS_F2_DYN_EXIT_WAIT_EXACT_F3_RETEST = 4,
   FP_NDS_F2_DYN_EXIT_TP_ARMED = 5,
   FP_NDS_F2_DYN_EXIT_CLOSED = 6,
   FP_NDS_F2_DYN_EXIT_WAIT_HTF_F3_LEG1 = 7,
   FP_NDS_F2_DYN_EXIT_WAIT_HTF_F3_WAIST = 8,
   FP_NDS_F2_DYN_EXIT_WAIT_HTF_F3_RETEST = 9
};

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
   FP_NDS_F2_RUN_MULTI_ORDER_SENT = 8,
   FP_NDS_F2_RUN_PENDING_CANCELLED_HTF_FILTER = 9,
   FP_NDS_F2_RUN_PENDING_CANCELLED_SOURCE_LIFECYCLE = 10
};

struct FP_NDSF2WaistTradeConfig
{
   bool enabled;
   bool send_tester_orders;
   bool one_attempt_per_f2_body;
   bool reset_used_setups_on_init;
   bool require_f2_size_gate;
   // Local exact-F3 exit requires the source F2 to possess canonical F3-spawn
   // authority. Kept separate from the general entry size-gate input so the
   // dependency is explicit rather than hidden inside the exit mode.
   bool require_canonical_f3_spawn_for_local_exit;
   bool cancel_pending_if_target_touched_before_fill;
   // Optional safety cap only. -1 means the setup is lifecycle-owned and does
   // not expire merely because a fixed number of bars passed.
   int max_setup_age_bars;

   // A setup is consumed on an actual order fill, not merely when a pending
   // order is accepted. A cancelled pending order may be re-armed while the
   // same F2 body remains structurally valid.
   bool consume_attempt_on_fill;
   bool enable_funnel_diagnostics;

   // Exit policy. In either dynamic F3 mode, min-RR and entry repricing still use
   // the original F2 flag end because the eventual F3 retest node is unknown
   // at entry time.
   int exit_mode;
   ENUM_TIMEFRAMES higher_timeframe_f3_exit_timeframe;
   double f3_exit_correction_ticks;
   bool close_at_market_if_f3_target_already_reached;

   // Opportunity geometry filter. When adjustment is enabled, a setup below
   // the requested minimum is not rejected immediately: its pending entry is
   // moved farther behind the F2 waist, toward the fixed F1-waist stop, until
   // the normalized executable geometry provides at least min_reward_risk.
   bool use_min_reward_risk_filter;
   bool adjust_entry_to_min_reward_risk;
   double min_reward_risk;

   // Near-duplicate arbitration. Same-direction setups are treated as one
   // opportunity when the overlap of their executable stop corridors covers
   // at least stop_space_overlap_percent of the narrower corridor. The wider
   // corridor wins; opposite-direction hedge contexts are never deduplicated.
   bool use_stop_space_overlap_deduplication;
   double stop_space_overlap_percent;

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
   ENUM_TIMEFRAMES period;
   int f1_event_id;
   int f2_event_id;
   int sequence_id;
   int parent_sequence_id;
   int f2_parent_event_id;
   int f2_chain_index;

   // Snapshot of the existing Phoenix F2 body/lifecycle at the moment the
   // execution projection is armed. These fields do not redefine F2; they bind
   // the pending order to the exact canonical two-leg body version.
   string f2_body_id;
   int f2_body_status_at_arm;
   int f2_status_at_arm;
   int f2_lifecycle_status_at_arm;
   int f2_internal_count_at_arm;
   bool projected_waist_break_branch;

   int body_available_index;
   int age_bars;
   datetime body_available_time;

   // Stable structural identity required by the dynamic F3 exit manager.
   int f1_waist_node_id;
   int f2_origin_node_id;
   int f2_waist_node_id;
   int initial_f2_leg2_node_id;
   datetime f1_waist_time;
   datetime f2_origin_time;
   datetime f2_waist_time;
   datetime f2_leg2_time;

   // Structural anatomy:
   // point_1 = F2 waist
   // point_2 = first strict price penetration beyond F2 waist; the pending
   // limit is placed there in advance, so its fill is the executable Point 2.
   double point_1_price;
   double point_2_limit_price;
   double f2_origin_price;
   double parent_f1_waist_price;
   double f2_flag_end_price;

   // The projected Point-2 limit must sit beyond Phoenix boundary epsilon,
   // not merely one nominal tick behind the Waist.
   double canonical_break_epsilon_price;
   double canonical_point2_min_offset_price;

   double structural_entry_price;
   double entry_price;
   double stop_price;
   // target_price and rr_reference_target_price are the original F2 Leg2
   // endpoint. They remain the RR authority in all exit modes.
   double target_price;
   double rr_reference_target_price;

   // Fixed mode sends this TP with the pending order. Dynamic F3 mode sends
   // zero and arms a later TP after F2 confirmation plus correction.
   double initial_broker_take_profit_price;

   bool entry_adjusted_for_reward_risk;
   double risk_distance;
   double reward_distance;
   double reward_risk;
   double volume;

   long setup_hash;
   string broker_comment;
};

struct FP_NDSF2DynamicExitContext
{
   bool active;
   string symbol;
   ENUM_TIMEFRAMES period;
   long setup_hash;
   string broker_comment;
   int direction;
   int scale_L;

   // Exact source-lineage authority. Every dynamic exit is bound to the same
   // F1/F2 chain that created its own order; no latest/same-direction lookup is
   // allowed to service another position.
   int source_f1_event_id;
   int source_f2_event_id;
   int source_sequence_id;
   int source_parent_sequence_id;
   int source_f2_parent_event_id;
   int source_f2_chain_index;
   int source_f1_waist_node_id;
   int source_f2_origin_node_id;
   int source_f2_waist_node_id;
   int source_initial_f2_leg2_node_id;

   datetime f1_waist_time;
   datetime f2_origin_time;
   datetime f2_waist_time;
   datetime initial_f2_leg2_time;
   double initial_f2_leg2_price;
   double reference_target_price;

   ulong order_ticket;
   ulong position_ticket;
   long position_identifier;
   int stage;
   int dynamic_exit_mode;
   ENUM_TIMEFRAMES dynamic_exit_timeframe;
   datetime position_open_time;

   // Exact child-F3 evidence. The target is taken from the Leg1 node of the
   // child whose parent_event_id is the bound source F2. The correction gate is
   // the Waist of that same child F3, not a shared tick-distance approximation.
   bool exact_child_f3_captured;
   int exact_child_f3_event_id;
   int exact_child_f3_parent_event_id;
   int exact_child_f3_sequence_id;
   int exact_child_f3_leg1_node_id;
   datetime exact_child_f3_leg1_time;
   double exact_child_f3_leg1_price;
   int exact_child_f3_waist_node_id;
   datetime exact_child_f3_waist_time;
   double exact_child_f3_waist_price;
   double dynamic_target_price;

   // Higher-timeframe F3 evidence. This is intentionally per trade. Each
   // position independently locks the first eligible canonical same-direction
   // HTF F3 Leg1 that becomes observable after that position opens. Even when
   // multiple positions legitimately share one HTF F3, every ticket carries
   // its own immutable identity and TP state.
   bool htf_f3_leg1_captured;
   int htf_f3_event_id;
   int htf_f3_sequence_id;
   int htf_f3_parent_sequence_id;
   int htf_f3_parent_event_id;
   int htf_f3_scale_L;
   int htf_f3_leg1_node_id;
   datetime htf_f3_leg1_time;
   double htf_f3_leg1_price;
   int htf_f3_waist_node_id;
   datetime htf_f3_waist_time;
   double htf_f3_waist_price;
   datetime htf_search_after_time;

   bool correction_seen;
   bool tp_armed;
};

void FP_ResetNDSF2DynamicExitContext(FP_NDSF2DynamicExitContext &ctx)
{
   ctx.active = false;
   ctx.symbol = "";
   ctx.period = PERIOD_CURRENT;
   ctx.setup_hash = 0;
   ctx.broker_comment = "";
   ctx.direction = FP_DIR_NONE;
   ctx.scale_L = 0;
   ctx.source_f1_event_id = -1;
   ctx.source_f2_event_id = -1;
   ctx.source_sequence_id = -1;
   ctx.source_parent_sequence_id = -1;
   ctx.source_f2_parent_event_id = -1;
   ctx.source_f2_chain_index = -1;
   ctx.source_f1_waist_node_id = -1;
   ctx.source_f2_origin_node_id = -1;
   ctx.source_f2_waist_node_id = -1;
   ctx.source_initial_f2_leg2_node_id = -1;
   ctx.f1_waist_time = 0;
   ctx.f2_origin_time = 0;
   ctx.f2_waist_time = 0;
   ctx.initial_f2_leg2_time = 0;
   ctx.initial_f2_leg2_price = 0.0;
   ctx.reference_target_price = 0.0;
   ctx.order_ticket = 0;
   ctx.position_ticket = 0;
   ctx.position_identifier = 0;
   ctx.stage = FP_NDS_F2_DYN_EXIT_NONE;
   ctx.dynamic_exit_mode = FP_NDS_F2_EXIT_FIXED_F2_FLAG_END;
   ctx.dynamic_exit_timeframe = PERIOD_CURRENT;
   ctx.position_open_time = 0;
   ctx.exact_child_f3_captured = false;
   ctx.exact_child_f3_event_id = -1;
   ctx.exact_child_f3_parent_event_id = -1;
   ctx.exact_child_f3_sequence_id = -1;
   ctx.exact_child_f3_leg1_node_id = -1;
   ctx.exact_child_f3_leg1_time = 0;
   ctx.exact_child_f3_leg1_price = 0.0;
   ctx.exact_child_f3_waist_node_id = -1;
   ctx.exact_child_f3_waist_time = 0;
   ctx.exact_child_f3_waist_price = 0.0;
   ctx.dynamic_target_price = 0.0;
   ctx.htf_f3_leg1_captured = false;
   ctx.htf_f3_event_id = -1;
   ctx.htf_f3_sequence_id = -1;
   ctx.htf_f3_parent_sequence_id = -1;
   ctx.htf_f3_parent_event_id = -1;
   ctx.htf_f3_scale_L = 0;
   ctx.htf_f3_leg1_node_id = -1;
   ctx.htf_f3_leg1_time = 0;
   ctx.htf_f3_leg1_price = 0.0;
   ctx.htf_f3_waist_node_id = -1;
   ctx.htf_f3_waist_time = 0;
   ctx.htf_f3_waist_price = 0.0;
   ctx.htf_search_after_time = 0;
   ctx.correction_seen = false;
   ctx.tp_armed = false;
}

void FP_ResetNDSF2WaistTradeConfig(FP_NDSF2WaistTradeConfig &cfg)
{
   cfg.enabled = true;
   cfg.send_tester_orders = true;
   cfg.one_attempt_per_f2_body = true;
   cfg.reset_used_setups_on_init = false;
   cfg.require_f2_size_gate = false;
   cfg.require_canonical_f3_spawn_for_local_exit = true;
   cfg.cancel_pending_if_target_touched_before_fill = true;
   cfg.max_setup_age_bars = -1;
   cfg.consume_attempt_on_fill = true;
   cfg.enable_funnel_diagnostics = false;
   cfg.exit_mode = FP_NDS_F2_EXIT_FIXED_F2_FLAG_END;
   cfg.higher_timeframe_f3_exit_timeframe = PERIOD_H1;
   cfg.f3_exit_correction_ticks = 1.0;
   cfg.close_at_market_if_f3_target_already_reached = true;

   cfg.use_min_reward_risk_filter = true;
   cfg.adjust_entry_to_min_reward_risk = true;
   cfg.min_reward_risk = 1.0;
   cfg.use_stop_space_overlap_deduplication = true;
   cfg.stop_space_overlap_percent = 80.0;
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
   s.period = PERIOD_CURRENT;
   s.f1_event_id = -1;
   s.f2_event_id = -1;
   s.sequence_id = -1;
   s.parent_sequence_id = -1;
   s.f2_parent_event_id = -1;
   s.f2_chain_index = -1;
   s.f2_body_id = "";
   s.f2_body_status_at_arm = FP_BODY_NONE;
   s.f2_status_at_arm = FP_STATUS_NONE;
   s.f2_lifecycle_status_at_arm = FP_F2_LC_NONE;
   s.f2_internal_count_at_arm = 0;
   s.projected_waist_break_branch = false;
   s.body_available_index = -1;
   s.age_bars = -1;
   s.body_available_time = 0;
   s.f1_waist_node_id = -1;
   s.f2_origin_node_id = -1;
   s.f2_waist_node_id = -1;
   s.initial_f2_leg2_node_id = -1;
   s.f1_waist_time = 0;
   s.f2_origin_time = 0;
   s.f2_waist_time = 0;
   s.f2_leg2_time = 0;
   s.point_1_price = 0.0;
   s.point_2_limit_price = 0.0;
   s.f2_origin_price = 0.0;
   s.parent_f1_waist_price = 0.0;
   s.f2_flag_end_price = 0.0;
   s.canonical_break_epsilon_price = 0.0;
   s.canonical_point2_min_offset_price = 0.0;
   s.structural_entry_price = 0.0;
   s.entry_price = 0.0;
   s.stop_price = 0.0;
   s.target_price = 0.0;
   s.rr_reference_target_price = 0.0;
   s.initial_broker_take_profit_price = 0.0;
   s.entry_adjusted_for_reward_risk = false;
   s.risk_distance = 0.0;
   s.reward_distance = 0.0;
   s.reward_risk = 0.0;
   s.volume = 0.0;
   s.setup_hash = 0;
   s.broker_comment = "";
}

#endif // __FP_NDS_F2_WAIST_TRADE_TYPES_MQH__
