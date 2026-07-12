#property strict
#property version   "1.50"
#property description "NDS F2 Point-2 backtest with fixed F2-end or dynamic F3-flag-retest exit modes."

#include "../../Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh"

// Dedicated execution-only tester.
// Loaded path: canonical rates -> canonical nodes -> F1 -> F2 body -> order.
// Not loaded: Hook setup, Zone, CG, AI, F3, renderer, CSV, timer or custom prints.

input FP_NDSBacktestProfile InpF2BTProfile = FP_NDS_BACKTEST_PROFILE_FAST;
input bool InpF2BTAllowNonTesterDryRun = false;
input bool InpF2BTRunOnFirstTick = false;

// CUSTOM profile only.
input int  InpF2BTCustomBarsToScan = 420;
input int  InpF2BTCustomMinClosedBars = 140;
input bool InpF2BTCustomUseMultiScale = true;
input int  InpF2BTCustomSwingL1 = 2;
input int  InpF2BTCustomSwingL2 = 3;
input int  InpF2BTCustomSwingL3 = 5;
input int  InpF2BTCustomSwingL4 = 0;
input int  InpF2BTCustomSwingL5 = 0;
input int  InpF2BTCustomSwingL6 = 0;
input int  InpF2BTCustomSwingL7 = 0;
input int  InpF2BTCustomSwingL8 = 0;
input int  InpF2BTCustomMaxEvents = 900;

// Canonical F1/F2 anatomy.
input double InpF2BTBoundaryEpsilonPoints = 0.0;
input bool   InpF2BTRequireF2SizeGate = false;
input double InpF2BTF2MinParentSizeRatio = 1.0;
input double InpF2BTNDMinRetraceRatio = 0.50;
input bool   InpF2BTNDAllowBelowHalfCycle = false;

// F2 waist-break Point-2 execution.
input bool   InpF2BTTradeEnabled = true;
input bool   InpF2BTSendTesterOrders = true;
input bool   InpF2BTOneAttemptPerF2Body = true;
input bool   InpF2BTResetUsedSetupsOnInit = true;
input bool   InpF2BTCancelPendingIfTargetTouchedBeforeFill = true;
input int    InpF2BTMaxSetupAgeBars = 0;
input double InpF2BTEntryBehindF2WaistTicks = 1.0;
input double InpF2BTStopBehindF1WaistTicks = 1.0;



// Exit mode.
// FIXED_F2_FLAG_END: current behavior, broker TP at original F2 Leg2.
// F3_FLAG_RETEST: original F2 Leg2 remains the RR reference only. After F2
// confirms and price corrects away, TP is armed at the F2-confirm/F3-Leg1 node.
input FP_NDSF2ExitMode InpF2BTExitMode = FP_NDS_F2_EXIT_FIXED_F2_FLAG_END;
input double InpF2BTF3ExitCorrectionTicks = 1.0;
input bool   InpF2BTCloseAtMarketIfF3TargetAlreadyReached = true;

// Reward/Risk policy. RR always uses original F2 Leg2, even in F3 exit mode.
// RR = abs(F2_Leg2-Entry) / abs(Entry-SL).
// If the structural waist entry is below the minimum, the tester can move the
// pending entry farther behind the F2 waist until the requested RR is reached.
input bool   InpF2BTUseMinimumRewardRiskFilter = true;
input bool   InpF2BTAdjustEntryToMinimumRewardRisk = true;
input double InpF2BTMinimumRewardRisk = 1.0;

// Near-duplicate same-direction contexts. The overlap percentage is measured
// against the narrower executable stop corridor. Example: 80 means that if at
// least 80% of the narrower corridor is shared, only the wider setup survives.
input bool   InpF2BTUseStopSpaceOverlapDeduplication = true;
input double InpF2BTStopSpaceOverlapThresholdPercent = 80.0;

// Parallel context policy. Distinct F2 setup hashes are independent contexts.
// Separate same-symbol positions require a hedging account in MT5.
input bool InpF2BTAllowOppositeDirectionHedge = true;
input bool InpF2BTAllowSameDirectionMultipleContexts = true;
input int  InpF2BTMaxConcurrentManagedExposures = 0; // 0 = unlimited.

input FP_NDSHookTradeSizingMode InpF2BTSizingMode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
input double InpF2BTFixedVolume = 0.01;
input double InpF2BTRiskCash = 100.0;
input double InpF2BTCommissionPerLotRoundTurn = 0.0;
input bool   InpF2BTAllowMinLotIfRiskTooSmall = false;
input int    InpF2BTMaxDeviationPoints = 20;
input long   InpF2BTMagic = 310055;
input string InpF2BTCommentPrefix = "NDSF2WB";

static datetime g_f2_bt_last_open_bar = 0;
static FP_NDSBacktestRuntimeConfig g_f2_bt_runtime_cfg;
static FP_Config g_f2_bt_detector_cfg;
static FP_NDSF2WaistTradeConfig g_f2_bt_trade_cfg;

bool FP_NDSF2BTIsTesterRuntime()
{
   return ((bool)MQLInfoInteger(MQL_TESTER) ||
           (bool)MQLInfoInteger(MQL_OPTIMIZATION) ||
           (bool)MQLInfoInteger(MQL_VISUAL_MODE));
}

void FP_LoadNDSF2BacktestRuntimeConfig(FP_NDSBacktestRuntimeConfig &cfg)
{
   FP_ResetNDSBacktestRuntimeConfig(cfg);
   cfg.profile = InpF2BTProfile;
   cfg.requested_bars = InpF2BTCustomBarsToScan;
   cfg.min_closed_bars = InpF2BTCustomMinClosedBars;
   cfg.use_closed_bars_only = true;
   cfg.strict_timebase = true;
   cfg.use_multi_scale = InpF2BTCustomUseMultiScale;
   cfg.scale_l1 = InpF2BTCustomSwingL1;
   cfg.scale_l2 = InpF2BTCustomSwingL2;
   cfg.scale_l3 = InpF2BTCustomSwingL3;
   cfg.scale_l4 = InpF2BTCustomSwingL4;
   cfg.scale_l5 = InpF2BTCustomSwingL5;
   cfg.scale_l6 = InpF2BTCustomSwingL6;
   cfg.scale_l7 = InpF2BTCustomSwingL7;
   cfg.scale_l8 = InpF2BTCustomSwingL8;
   cfg.max_events = InpF2BTCustomMaxEvents;
   cfg.max_hooks = 0;
   cfg.run_on_first_tick = InpF2BTRunOnFirstTick;
   cfg.print_run_summary = false;
   FP_NDSF2BacktestApplyProfile(cfg);
}

void FP_LoadNDSF2DetectorConfig(const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                FP_Config &cfg)
{
   FP_DefaultConfig(cfg);
   cfg.include_pending_nodes = false;
   cfg.scan_hooks = false;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = false;

   // The dedicated detector uses raw canonical origin nodes as F1 seed authority.
   cfg.require_f1_phase_boundary = false;
   cfg.allow_f1_fail_open_when_no_hook = true;
   cfg.enforce_single_chain_per_direction_scale = false;
   cfg.enforce_single_chain_per_direction_global = false;
   cfg.absorb_pre_internal_extensions = true;
   cfg.hide_superseded_parent_states = false;
   cfg.strict_main_chart_ownership = false;
   cfg.ownership_hide_orphans = false;
   cfg.canonical_strict_invariants = false;
   cfg.canonical_hide_unresolved_orphans = false;

   cfg.show_invalidated_in_audit = false;
   cfg.keep_confirmed_f1f2_after_boundary_hit = false;
   cfg.f1_show_post_flag_candidates = false;
   cfg.f1_show_live_body_candidates = false;

   // This setup must receive body-complete, unconfirmed F2 events. Confirmation
   // is the target event and would be too late for entry.
   cfg.f2_show_size_rejected_candidates = !InpF2BTRequireF2SizeGate;
   cfg.f2_show_post_flag_candidates = true;
   cfg.f2_show_live_body_candidates = true;
   cfg.f3_show_or_rejected_candidates = false;
   cfg.f3_show_live_body_candidates = false;

   cfg.max_events = runtime_cfg.max_events;
   cfg.max_hooks = 0;
   cfg.max_roots_per_scale_direction = 0;
   cfg.context_symbol = _Symbol;
   cfg.context_timeframe = EnumToString(_Period);
   cfg.identity_generation_pass = "nds_f2_waist_break_point2_v6";
   cfg.identity_config_hash = "f2_wb2_v6";

   cfg.boundary_epsilon_points = InpF2BTBoundaryEpsilonPoints;
   cfg.f2_min_parent_size_ratio = InpF2BTF2MinParentSizeRatio;
   cfg.nd_min_retrace_ratio = InpF2BTNDMinRetraceRatio;
   cfg.nd_allow_below_half_cycle = InpF2BTNDAllowBelowHalfCycle;
   cfg.verbose_logs = false;

   cfg.print_node_sanity = false;
   cfg.print_node_samples = false;
   cfg.print_identity_sanity = false;
   cfg.print_identity_samples = false;
   cfg.print_hook_sanity = false;
   cfg.print_hook_samples = false;
   cfg.print_body_sanity = false;
   cfg.print_body_samples = false;
   cfg.print_internal_sanity = false;
   cfg.print_internal_samples = false;
   cfg.print_f1_sanity = false;
   cfg.print_f1_samples = false;
   cfg.print_f2_sanity = false;
   cfg.print_f2_samples = false;
   cfg.print_f3_sanity = false;
   cfg.print_f3_samples = false;
   cfg.print_ownership_sanity = false;
   cfg.print_ownership_samples = false;
   cfg.print_canonical_sanity = false;
   cfg.print_canonical_samples = false;
}

void FP_LoadNDSF2TradeConfig(FP_NDSF2WaistTradeConfig &cfg)
{
   FP_ResetNDSF2WaistTradeConfig(cfg);
   cfg.enabled = InpF2BTTradeEnabled;
   cfg.send_tester_orders = InpF2BTSendTesterOrders;
   cfg.one_attempt_per_f2_body = InpF2BTOneAttemptPerF2Body;
   cfg.reset_used_setups_on_init = InpF2BTResetUsedSetupsOnInit;
   cfg.require_f2_size_gate = InpF2BTRequireF2SizeGate;
   cfg.cancel_pending_if_target_touched_before_fill = InpF2BTCancelPendingIfTargetTouchedBeforeFill;
   cfg.max_setup_age_bars = InpF2BTMaxSetupAgeBars;
   cfg.exit_mode = InpF2BTExitMode;
   cfg.f3_exit_correction_ticks = InpF2BTF3ExitCorrectionTicks;
   cfg.close_at_market_if_f3_target_already_reached =
      InpF2BTCloseAtMarketIfF3TargetAlreadyReached;
   cfg.entry_behind_f2_waist_ticks = InpF2BTEntryBehindF2WaistTicks;
   cfg.stop_behind_f1_waist_ticks = InpF2BTStopBehindF1WaistTicks;
   cfg.use_min_reward_risk_filter = InpF2BTUseMinimumRewardRiskFilter;
   cfg.adjust_entry_to_min_reward_risk = InpF2BTAdjustEntryToMinimumRewardRisk;
   cfg.min_reward_risk = InpF2BTMinimumRewardRisk;
   cfg.use_stop_space_overlap_deduplication = InpF2BTUseStopSpaceOverlapDeduplication;
   cfg.stop_space_overlap_percent = InpF2BTStopSpaceOverlapThresholdPercent;
   cfg.allow_opposite_direction_hedge = InpF2BTAllowOppositeDirectionHedge;
   cfg.allow_same_direction_multiple_contexts = InpF2BTAllowSameDirectionMultipleContexts;
   cfg.max_concurrent_managed_exposures = InpF2BTMaxConcurrentManagedExposures;
   cfg.sizing_mode = InpF2BTSizingMode;
   cfg.fixed_volume = InpF2BTFixedVolume;
   cfg.risk_cash = InpF2BTRiskCash;
   cfg.commission_per_lot_round_turn = InpF2BTCommissionPerLotRoundTurn;
   cfg.allow_min_lot_if_risk_too_small = InpF2BTAllowMinLotIfRiskTooSmall;
   cfg.max_deviation_points = InpF2BTMaxDeviationPoints;
   cfg.magic = InpF2BTMagic;
   cfg.comment_prefix = InpF2BTCommentPrefix;
}

void FP_NDSF2BTRunOnce()
{
   FP_RunNDSF2WaistBacktestCycle(_Symbol, _Period,
                                 g_f2_bt_runtime_cfg,
                                 g_f2_bt_detector_cfg,
                                 g_f2_bt_trade_cfg);
}

int OnInit()
{
   if(!FP_NDSF2BTIsTesterRuntime() && !InpF2BTAllowNonTesterDryRun)
      return INIT_FAILED;

   FP_LoadNDSF2BacktestRuntimeConfig(g_f2_bt_runtime_cfg);
   FP_LoadNDSF2DetectorConfig(g_f2_bt_runtime_cfg, g_f2_bt_detector_cfg);
   FP_LoadNDSF2TradeConfig(g_f2_bt_trade_cfg);
   if(g_f2_bt_trade_cfg.reset_used_setups_on_init)
      FP_NDSF2ResetUsedSetups();

   g_f2_bt_last_open_bar = iTime(_Symbol, _Period, 0);
   if(g_f2_bt_runtime_cfg.run_on_first_tick)
      FP_NDSF2BTRunOnce();
   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Per-tick path is intentionally tiny: no detector, renderer, CSV or prints.
   // It only cancels consumed dynamic pending orders and manages the optional
   // F3-retest TP on already-open positions.
   FP_NDSF2ManageDynamicExitOnTick(_Symbol, _Period, g_f2_bt_trade_cfg);

   datetime open_bar = iTime(_Symbol, _Period, 0);
   if(open_bar <= 0 || open_bar == g_f2_bt_last_open_bar) return;
   g_f2_bt_last_open_bar = open_bar;
   FP_NDSF2BTRunOnce();
}
