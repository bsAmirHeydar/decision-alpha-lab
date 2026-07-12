#property strict
#property version   "1.00"
#property description "NDS lightweight F2 waist limit backtest: F2 waist entry, F1 waist stop, F2 Leg2 target."

#include "../../Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh"

// ============================================================================
// NDS F2 WAIST LIMIT BACKTEST
// ----------------------------------------------------------------------------
// Trade source: confirmed canonical F2 only.
// Entry: below bullish F2 waist / above bearish F2 waist.
// Stop: exact canonical parent F1 waist.
// Target: exact canonical F2 Leg2 endpoint.
// Hook/Zone/AI are not execution inputs. The existing Phoenix detector remains
// the sole authority for canonical F1/F2 anatomy and lifecycle state.
// ============================================================================

// ------------------------------ Runtime profile -----------------------------
input FP_NDSBacktestProfile InpF2BTProfile = FP_NDS_BACKTEST_PROFILE_FAST;
input bool InpF2BTAllowNonTesterDryRun = false;
input bool InpF2BTRunOnFirstTick = false;
input bool InpF2BTPrintRunSummary = false;
input int  InpF2BTPrintEveryNRuns = 250;
input bool InpF2BTPrintSessionSummary = true;

// CUSTOM profile only.
input int  InpF2BTCustomBarsToScan = 800;
input int  InpF2BTCustomMinClosedBars = 160;
input bool InpF2BTCustomUseMultiScale = true;
input int  InpF2BTCustomSwingL1 = 2;
input int  InpF2BTCustomSwingL2 = 3;
input int  InpF2BTCustomSwingL3 = 5;
input int  InpF2BTCustomSwingL4 = 0;
input int  InpF2BTCustomSwingL5 = 0;
input int  InpF2BTCustomSwingL6 = 0;
input int  InpF2BTCustomSwingL7 = 0;
input int  InpF2BTCustomSwingL8 = 0;
input int  InpF2BTCustomMaxEvents = 1800;
input int  InpF2BTCustomMaxHooks = 1800;

// ------------------------------ Canonical F engine --------------------------
input bool   InpF2BTIncludePendingNodes = false;
input bool   InpF2BTRequireF1PhaseBoundary = true;
input bool   InpF2BTAllowF1FailOpenWhenNoHook = true;
input bool   InpF2BTEnforceSingleChainPerDirectionScale = false;
input bool   InpF2BTEnforceSingleChainPerDirectionGlobal = false;
input bool   InpF2BTAbsorbPreInternalExtensions = true;
input bool   InpF2BTHideSupersededParentStates = true;
input bool   InpF2BTStrictMainChartOwnership = true;
input int    InpF2BTOwnershipScoreMargin = 25;
input bool   InpF2BTOwnershipHideOrphans = true;
input bool   InpF2BTCanonicalStrictInvariants = true;
input bool   InpF2BTCanonicalHideUnresolvedOrphans = true;
input bool   InpF2BTHookMainRequiresVisibleF1 = false;
input bool   InpF2BTHookKeepUnseededVisibleForDebug = true;
input double InpF2BTBoundaryEpsilonPoints = 0.0;
input double InpF2BTF2MinParentSizeRatio = 1.0;
input double InpF2BTNDMinRetraceRatio = 0.50;
input bool   InpF2BTNDAllowBelowHalfCycle = false;

// ------------------------------ F2 execution --------------------------------
input bool   InpF2BTTradeEnabled = true;
input bool   InpF2BTSendTesterOrders = true;
input bool   InpF2BTRequireVisibleMain = true;
input bool   InpF2BTOneAttemptPerF2 = true;
input bool   InpF2BTResetUsedSetupsOnInit = true;
input int    InpF2BTMaxSetupAgeBars = 1;

// Bullish: Buy Limit = F2 waist - offset.
// Bearish: Sell Limit = F2 waist + offset.
input double InpF2BTEntryOffsetPoints = 1.0;

input FP_NDSHookTradeSizingMode InpF2BTSizingMode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
input double InpF2BTFixedVolume = 0.01;
input double InpF2BTRiskCash = 100.0;
input double InpF2BTCommissionPerLotRoundTurn = 0.0;
input bool   InpF2BTAllowMinLotIfRiskTooSmall = false;
input int    InpF2BTMaxDeviationPoints = 20;
input int    InpF2BTEntryLockTimeoutSeconds = 30;
input long   InpF2BTMagic = 310055;
input string InpF2BTCommentPrefix = "NDSF2";

static datetime g_f2_bt_last_open_bar = 0;
static FP_NDSBacktestRuntimeConfig g_f2_bt_runtime_cfg;
static FP_Config g_f2_bt_detector_cfg;
static FP_NDSF2WaistTradeConfig g_f2_bt_trade_cfg;
static FP_NDSF2WaistBacktestStats g_f2_bt_stats;

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
   cfg.max_hooks = InpF2BTCustomMaxHooks;
   cfg.run_on_first_tick = InpF2BTRunOnFirstTick;
   cfg.print_run_summary = InpF2BTPrintRunSummary;
   cfg.print_every_n_runs = InpF2BTPrintEveryNRuns;
   FP_NDSF2BacktestApplyProfile(cfg);
}

void FP_LoadNDSF2DetectorConfig(const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                FP_Config &cfg)
{
   FP_DefaultConfig(cfg);
   cfg.include_pending_nodes = InpF2BTIncludePendingNodes;

   // Hook branches are permitted only as the existing canonical F1 boundary
   // source inside Phoenix. No Hook Phase02 validity, Hook setup, Hook order,
   // Zone, AI, drawing, or Hook CSV layer is loaded by this executable.
   cfg.scan_hooks = true;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = false;
   cfg.show_invalidated_in_audit = false;
   cfg.keep_confirmed_f1f2_after_boundary_hit = false;

   cfg.require_f1_phase_boundary = InpF2BTRequireF1PhaseBoundary;
   cfg.allow_f1_fail_open_when_no_hook = InpF2BTAllowF1FailOpenWhenNoHook;
   cfg.enforce_single_chain_per_direction_scale = InpF2BTEnforceSingleChainPerDirectionScale;
   cfg.enforce_single_chain_per_direction_global = InpF2BTEnforceSingleChainPerDirectionGlobal;
   cfg.absorb_pre_internal_extensions = InpF2BTAbsorbPreInternalExtensions;
   cfg.hide_superseded_parent_states = InpF2BTHideSupersededParentStates;
   cfg.compact_hook_rendering = true;
   cfg.strict_main_chart_ownership = InpF2BTStrictMainChartOwnership;
   cfg.ownership_allow_visual_soft_reset = true;
   cfg.ownership_score_margin = InpF2BTOwnershipScoreMargin;
   cfg.ownership_hide_orphans = InpF2BTOwnershipHideOrphans;
   cfg.canonical_strict_invariants = InpF2BTCanonicalStrictInvariants;
   cfg.canonical_hide_unresolved_orphans = InpF2BTCanonicalHideUnresolvedOrphans;
   cfg.hook_main_requires_visible_f1 = InpF2BTHookMainRequiresVisibleF1;
   cfg.hook_keep_unseeded_visible_for_debug = InpF2BTHookKeepUnseededVisibleForDebug;

   cfg.f1_show_post_flag_candidates = false;
   cfg.f1_show_live_body_candidates = false;
   cfg.f2_show_size_rejected_candidates = false;
   cfg.f2_show_post_flag_candidates = false;
   cfg.f2_show_live_body_candidates = false;
   cfg.f3_show_or_rejected_candidates = false;
   cfg.f3_show_live_body_candidates = false;

   cfg.max_events = runtime_cfg.max_events;
   cfg.max_hooks = runtime_cfg.max_hooks;
   cfg.max_roots_per_scale_direction = 0;
   cfg.context_symbol = _Symbol;
   cfg.context_timeframe = EnumToString(_Period);
   cfg.identity_generation_pass = "nds_f2_waist_backtest_v1";
   cfg.identity_config_hash = "profile_" + FP_NDSBacktestProfileName(runtime_cfg.profile);

   cfg.boundary_epsilon_points = InpF2BTBoundaryEpsilonPoints;
   cfg.f2_min_parent_size_ratio = InpF2BTF2MinParentSizeRatio;
   cfg.f3_min_parent_size_ratio = 0.70;
   cfg.f3_leg1_L_min_ratio = 0.80;
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
   cfg.require_visible_main = InpF2BTRequireVisibleMain;
   cfg.one_attempt_per_f2 = InpF2BTOneAttemptPerF2;
   cfg.reset_used_setups_on_init = InpF2BTResetUsedSetupsOnInit;
   cfg.max_setup_age_bars = InpF2BTMaxSetupAgeBars;
   cfg.entry_offset_points = InpF2BTEntryOffsetPoints;
   cfg.sizing_mode = InpF2BTSizingMode;
   cfg.fixed_volume = InpF2BTFixedVolume;
   cfg.risk_cash = InpF2BTRiskCash;
   cfg.commission_per_lot_round_turn = InpF2BTCommissionPerLotRoundTurn;
   cfg.allow_min_lot_if_risk_too_small = InpF2BTAllowMinLotIfRiskTooSmall;
   cfg.max_deviation_points = InpF2BTMaxDeviationPoints;
   cfg.entry_lock_timeout_seconds = InpF2BTEntryLockTimeoutSeconds;
   cfg.magic = InpF2BTMagic;
   cfg.comment_prefix = InpF2BTCommentPrefix;
}

bool FP_NDSF2BTRunOnce()
{
   FP_NDSF2WaistBacktestReport report;
   bool ok = FP_RunNDSF2WaistBacktestCycle(_Symbol, _Period,
                                            g_f2_bt_runtime_cfg,
                                            g_f2_bt_detector_cfg,
                                            g_f2_bt_trade_cfg,
                                            report);
   FP_NDSF2BacktestUpdateStats(report, g_f2_bt_stats);

   bool transition = (report.trade_report.action == FP_NDS_F2_ACTION_LIMIT_SENT ||
                      report.trade_report.action == FP_NDS_F2_ACTION_PAPER_LIMIT);
   bool scheduled = (g_f2_bt_runtime_cfg.print_run_summary &&
                     (g_f2_bt_stats.runs == 1 ||
                      (g_f2_bt_stats.runs % (ulong)g_f2_bt_runtime_cfg.print_every_n_runs) == 0));
   bool unexpected = (!ok && report.status != "TIMEBASE_FAILED" && report.status != "NOT_ENOUGH_CLOSED_BARS");
   if(transition || scheduled || unexpected || g_f2_bt_stats.runs == 1)
      FP_PrintNDSF2BacktestRun("NDS_F2_BT", g_f2_bt_runtime_cfg, report);
   return ok;
}

int OnInit()
{
   if(!FP_NDSF2BTIsTesterRuntime() && !InpF2BTAllowNonTesterDryRun)
   {
      Print("NDS_F2_BT_INIT status=blocked reason=strategy_tester_required");
      return INIT_FAILED;
   }

   FP_LoadNDSF2BacktestRuntimeConfig(g_f2_bt_runtime_cfg);
   FP_LoadNDSF2DetectorConfig(g_f2_bt_runtime_cfg, g_f2_bt_detector_cfg);
   FP_LoadNDSF2TradeConfig(g_f2_bt_trade_cfg);
   FP_ResetNDSF2WaistBacktestStats(g_f2_bt_stats);

   if(g_f2_bt_trade_cfg.reset_used_setups_on_init)
      FP_NDSF2ResetUsedSetups(g_f2_bt_trade_cfg);

   g_f2_bt_last_open_bar = iTime(_Symbol, _Period, 0);
   Print("NDS_F2_BT_INIT status=ready version=", FP_NDS_F2_WAIST_BACKTEST_VERSION,
         " profile=", FP_NDSBacktestProfileName(g_f2_bt_runtime_cfg.profile),
         " contract=F2_confirmed_to_waist_limit_F1_waist_SL_F2_leg2_TP",
         " hooks_as_entry=false zones=false ai=false");

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

void OnDeinit(const int reason)
{
   if(InpF2BTPrintSessionSummary)
      FP_PrintNDSF2BacktestStats("NDS_F2_BT_SUMMARY", g_f2_bt_stats);
}
