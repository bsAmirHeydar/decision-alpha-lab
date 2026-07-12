#property strict
#property version   "1.10"
#property description "NDS fast F2 waist limit backtest: F2 waist entry, F1 waist stop, F2 Leg2 target."

#include "../../Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh"

// Execution-only tester. No Hook setup, Zone, AI, renderer, CSV, timer or custom
// runtime Print path is loaded.

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
input double InpF2BTF2MinParentSizeRatio = 1.0;
input double InpF2BTNDMinRetraceRatio = 0.50;
input bool   InpF2BTNDAllowBelowHalfCycle = false;

// Execution.
input bool   InpF2BTTradeEnabled = true;
input bool   InpF2BTSendTesterOrders = true;
input bool   InpF2BTOneAttemptPerF2 = true;
input bool   InpF2BTResetUsedSetupsOnInit = true;
input int    InpF2BTMaxSetupAgeBars = 0;
input double InpF2BTEntryOffsetTicks = 1.0;

input FP_NDSHookTradeSizingMode InpF2BTSizingMode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
input double InpF2BTFixedVolume = 0.01;
input double InpF2BTRiskCash = 100.0;
input double InpF2BTCommissionPerLotRoundTurn = 0.0;
input bool   InpF2BTAllowMinLotIfRiskTooSmall = false;
input int    InpF2BTMaxDeviationPoints = 20;
input long   InpF2BTMagic = 310055;
input string InpF2BTCommentPrefix = "NDSF2";

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

   // This setup is F-only. Raw canonical origin nodes are the F1 seed authority.
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
   cfg.f2_show_size_rejected_candidates = false;
   cfg.f2_show_post_flag_candidates = false;
   cfg.f2_show_live_body_candidates = false;
   cfg.f3_show_or_rejected_candidates = false;
   cfg.f3_show_live_body_candidates = false;

   cfg.max_events = runtime_cfg.max_events;
   cfg.max_hooks = 0;
   cfg.max_roots_per_scale_direction = 0;
   cfg.context_symbol = _Symbol;
   cfg.context_timeframe = EnumToString(_Period);
   cfg.identity_generation_pass = "nds_f2_fast_execution_v2";
   cfg.identity_config_hash = "f2_fast_v2";

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
   cfg.one_attempt_per_f2 = InpF2BTOneAttemptPerF2;
   cfg.reset_used_setups_on_init = InpF2BTResetUsedSetupsOnInit;
   cfg.max_setup_age_bars = InpF2BTMaxSetupAgeBars;
   cfg.entry_offset_ticks = InpF2BTEntryOffsetTicks;
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
   datetime open_bar = iTime(_Symbol, _Period, 0);
   if(open_bar <= 0 || open_bar == g_f2_bt_last_open_bar) return;
   g_f2_bt_last_open_bar = open_bar;
   FP_NDSF2BTRunOnce();
}
