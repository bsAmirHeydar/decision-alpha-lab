#property strict
#property version   "1.10"
#property description "NDS profile-aware Strategy Tester executable. Defaults to Hook 86.4 / Phase04 X-closed / x3-x4 / fixed 1R with full diagnostic funnel."

#include "../../Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh"

// ============================================================================
// NDS LIGHTWEIGHT BACKTEST EXECUTABLE
// ----------------------------------------------------------------------------
// This EA is intentionally isolated from the production visualization expert.
// It does not load rendering, license, UI, release, validation, paper-ledger,
// state-gate, broker-dry-run, or Obsidian-facing runtime layers.
// ============================================================================

// ------------------------------ Runtime profile -----------------------------
input FP_NDSBacktestProfile InpBTProfile = FP_NDS_BACKTEST_PROFILE_PARITY;
input bool InpBTAllowNonTesterDryRun = false;
input bool InpBTRunOnFirstTick = true;
input bool InpBTSkipHookRebuildWhilePositionOpen = true;
input bool InpBTPrintRunSummary = true;
input int  InpBTPrintEveryNRuns = 25;
input bool InpBTPrintSessionSummary = true;

// CUSTOM profile only. FAST and PARITY replace these values deterministically.
input int  InpBTCustomBarsToScan = 1200;
input int  InpBTCustomMinClosedBars = 200;
input bool InpBTCustomUseMultiScale = true;
input int  InpBTCustomSwingL1 = 2;
input int  InpBTCustomSwingL2 = 3;
input int  InpBTCustomSwingL3 = 5;
input int  InpBTCustomSwingL4 = 8;
input int  InpBTCustomSwingL5 = 0;
input int  InpBTCustomSwingL6 = 0;
input int  InpBTCustomSwingL7 = 0;
input int  InpBTCustomSwingL8 = 0;
input int  InpBTCustomMaxEvents = 2500;
input int  InpBTCustomMaxHooks = 2500;
input int  InpBTCustomHookScanBars = 1200;

// ------------------------------ Canonical F engine --------------------------
input bool   InpBTIncludePendingNodes = false;
input bool   InpBTRequireF1PhaseBoundary = true;
input bool   InpBTAllowF1FailOpenWhenNoHook = true;
input bool   InpBTEnforceSingleChainPerDirectionScale = false;
input bool   InpBTEnforceSingleChainPerDirectionGlobal = false;
input bool   InpBTAbsorbPreInternalExtensions = true;
input bool   InpBTHideSupersededParentStates = true;
input bool   InpBTStrictMainChartOwnership = true;
input int    InpBTOwnershipScoreMargin = 25;
input bool   InpBTOwnershipHideOrphans = true;
input bool   InpBTCanonicalStrictInvariants = true;
input bool   InpBTCanonicalHideUnresolvedOrphans = true;
input bool   InpBTHookMainRequiresVisibleF1 = false;
input bool   InpBTHookKeepUnseededVisibleForDebug = true;
input double InpBTBoundaryEpsilonPoints = 0.0;
input double InpBTF2MinParentSizeRatio = 1.0;
input double InpBTF3MinParentSizeRatio = 0.70;
input double InpBTF3Leg1LMinRatio = 0.80;
input double InpBTNDMinRetraceRatio = 0.50;
input bool   InpBTNDAllowBelowHalfCycle = false;

// ------------------------------ Hook validity -------------------------------
input FP_HookPhase02OriginPolicy InpBTHookOriginPolicy = FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X;
input bool   InpBTHookShowPositive = true;
input bool   InpBTHookShowNegative = true;
input bool   InpBTHookRequireConfirmedResolveNode = true;
input bool   InpBTHookDeathOnBoundaryTouch = true;
input bool   InpBTHookRequireNearDeathForSemanticArc = true;
input bool   InpBTHookSeedUsedNodesCannotRestart = true;
input bool   InpBTHookShowOnlyValidHooks = true;
input bool   InpBTHookValidOnlyRequireNearDeath = false;
input bool   InpBTHookValidF3RequireSameScale = false;
input bool   InpBTHookValidF3RequireOppositeDirection = true;
input bool   InpBTHookValidOnlyFallbackToStructural = false;
input FP_HookPostF3RecognitionMode InpBTHookPostF3RecognitionMode = FP_HOOK_POST_F3_STRUCTURAL_OR_GEOMETRIC_80;
input FP_HookPostF3SelectionPriority InpBTHookPostF3SelectionPriority = FP_HOOK_POST_F3_PRIORITY_STRUCTURAL_FIRST;
input bool   InpBTHookPostF3AllowDirectTerminalHook = true;
input bool   InpBTHookPostF3AllowDelayedReboundHook = true;
input int    InpBTHookPostF3MaxSearchBars = 180;
input int    InpBTHookPostF3TerminalToleranceBars = 3;
input int    InpBTHookPostF3TerminalTolerancePricePoints = 20;
input double InpBTHookPostF3GeometricMinCompletionPct = 80.0;
input double InpBTHookNearDeathRetraceThreshold = 0.50;
input int    InpBTHookMinXNodesToKeep = 1;
input int    InpBTHookMaxXNodesPerSequence = 4;
input int    InpBTHookMaxSequences = 3000;
input int    InpBTHookMaxNodes = 20000;

// ------------------------------ Executable contract -------------------------
input bool   InpBTTradeEnabled = true;
input bool   InpBTSendTesterOrders = true;
input FP_NDSHookTradeProfile InpBTTradeProfile = FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1;
input double InpBTHookEntryRatio = 0.864;
input int    InpBTHookEntryMinXCount = 3;
input int    InpBTHookEntryMaxXCount = 4;
input bool   InpBTRequireConfirmedTerminal = true;
input bool   InpBTRequireLevelUntouched = true;
input double InpBTFixedRewardR = 1.0;
input bool   InpBTAllowHookAfterHook = true;
input bool   InpBTAllowHookAfterF3 = true;
input bool   InpBTRequireClosedHook = true;
input bool   InpBTOneAttemptPerHook = true;
input bool   InpBTResetUsedSetupsOnInit = true;
input bool   InpBTCancelPendingOnDeath = true;
input bool   InpBTRequireFullF123AfterEntry = true;
input FP_NDSHookTradeSizingMode InpBTSizingMode = FP_NDS_HOOK_TRADE_SIZE_FIXED_VOLUME;
input double InpBTFixedVolume = 0.01;
input double InpBTRiskCash = 100.0;
input double InpBTCommissionPerLotRoundTurn = 0.0;
input bool   InpBTAllowMinLotIfRiskTooSmall = false;
input int    InpBTStopBufferPoints = 1;
input double InpBTStopSpreadMultiplier = 1.0;
input int    InpBTMaxDeviationPoints = 20;
input int    InpBTEntryLockTimeoutSeconds = 30;
input long   InpBTMagic = 310052;
input string InpBTCommentPrefix = "NDSBT";

static datetime g_nds_bt_last_open_bar = 0;
static FP_NDSBacktestRuntimeConfig g_nds_bt_runtime_cfg;
static FP_Config g_nds_bt_detector_cfg;
static FP_HookPhase01Config g_nds_bt_node_cfg;
static FP_HookPhase02Config g_nds_bt_hook_cfg;
static FP_NDSHookTradeConfig g_nds_bt_trade_cfg;
static FP_NDSBacktestSessionStats g_nds_bt_stats;

bool FP_NDSBTIsTesterRuntime()
{
   return ((bool)MQLInfoInteger(MQL_TESTER) ||
           (bool)MQLInfoInteger(MQL_OPTIMIZATION) ||
           (bool)MQLInfoInteger(MQL_VISUAL_MODE));
}

void FP_LoadNDSBacktestRuntimeConfig(FP_NDSBacktestRuntimeConfig &cfg)
{
   FP_ResetNDSBacktestRuntimeConfig(cfg);
   cfg.profile = InpBTProfile;
   cfg.requested_bars = InpBTCustomBarsToScan;
   cfg.min_closed_bars = InpBTCustomMinClosedBars;
   cfg.use_closed_bars_only = true;
   cfg.strict_timebase = true;
   cfg.use_multi_scale = InpBTCustomUseMultiScale;
   cfg.scale_l1 = InpBTCustomSwingL1;
   cfg.scale_l2 = InpBTCustomSwingL2;
   cfg.scale_l3 = InpBTCustomSwingL3;
   cfg.scale_l4 = InpBTCustomSwingL4;
   cfg.scale_l5 = InpBTCustomSwingL5;
   cfg.scale_l6 = InpBTCustomSwingL6;
   cfg.scale_l7 = InpBTCustomSwingL7;
   cfg.scale_l8 = InpBTCustomSwingL8;
   cfg.max_events = InpBTCustomMaxEvents;
   cfg.max_hooks = InpBTCustomMaxHooks;
   cfg.hook_scan_bars = InpBTCustomHookScanBars;
   cfg.run_on_first_tick = InpBTRunOnFirstTick;
   cfg.skip_hook_rebuild_while_position_open = InpBTSkipHookRebuildWhilePositionOpen;
   cfg.print_run_summary = InpBTPrintRunSummary;
   cfg.print_every_n_runs = InpBTPrintEveryNRuns;
   FP_NDSBacktestApplyProfile(cfg);
}

void FP_LoadNDSBacktestDetectorConfig(const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                      FP_Config &cfg)
{
   FP_DefaultConfig(cfg);
   cfg.include_pending_nodes = InpBTIncludePendingNodes;
   cfg.scan_hooks = true;
   cfg.scan_f1 = true;
   cfg.scan_f2 = true;
   cfg.scan_f3 = true;
   cfg.show_invalidated_in_audit = false;
   cfg.keep_confirmed_f1f2_after_boundary_hit = false;

   cfg.require_f1_phase_boundary = InpBTRequireF1PhaseBoundary;
   cfg.allow_f1_fail_open_when_no_hook = InpBTAllowF1FailOpenWhenNoHook;
   cfg.enforce_single_chain_per_direction_scale = InpBTEnforceSingleChainPerDirectionScale;
   cfg.enforce_single_chain_per_direction_global = InpBTEnforceSingleChainPerDirectionGlobal;
   cfg.absorb_pre_internal_extensions = InpBTAbsorbPreInternalExtensions;
   cfg.hide_superseded_parent_states = InpBTHideSupersededParentStates;
   cfg.compact_hook_rendering = true;
   cfg.strict_main_chart_ownership = InpBTStrictMainChartOwnership;
   cfg.ownership_allow_visual_soft_reset = true;
   cfg.ownership_score_margin = InpBTOwnershipScoreMargin;
   cfg.ownership_hide_orphans = InpBTOwnershipHideOrphans;
   cfg.canonical_strict_invariants = InpBTCanonicalStrictInvariants;
   cfg.canonical_hide_unresolved_orphans = InpBTCanonicalHideUnresolvedOrphans;
   cfg.hook_main_requires_visible_f1 = InpBTHookMainRequiresVisibleF1;
   cfg.hook_keep_unseeded_visible_for_debug = InpBTHookKeepUnseededVisibleForDebug;

   cfg.f1_show_post_flag_candidates = true;
   cfg.f1_show_live_body_candidates = true;
   cfg.f2_show_size_rejected_candidates = true;
   cfg.f2_show_post_flag_candidates = true;
   cfg.f2_show_live_body_candidates = true;
   cfg.f3_show_or_rejected_candidates = true;
   cfg.f3_show_live_body_candidates = true;

   cfg.max_events = runtime_cfg.max_events;
   cfg.max_hooks = runtime_cfg.max_hooks;
   cfg.max_roots_per_scale_direction = 0;
   cfg.context_symbol = _Symbol;
   cfg.context_timeframe = EnumToString(_Period);
   cfg.identity_generation_pass = "nds_lightweight_backtest_v1";
   cfg.identity_config_hash = "profile_" + FP_NDSBacktestProfileName(runtime_cfg.profile);

   cfg.boundary_epsilon_points = InpBTBoundaryEpsilonPoints;
   cfg.f2_min_parent_size_ratio = InpBTF2MinParentSizeRatio;
   cfg.f3_min_parent_size_ratio = InpBTF3MinParentSizeRatio;
   cfg.f3_leg1_L_min_ratio = InpBTF3Leg1LMinRatio;
   cfg.nd_min_retrace_ratio = InpBTNDMinRetraceRatio;
   cfg.nd_allow_below_half_cycle = InpBTNDAllowBelowHalfCycle;
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

void FP_LoadNDSBacktestNodeConfig(const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                  FP_HookPhase01Config &cfg)
{
   FP_ResetHookPhase01Config(cfg);
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_HOOK_ONLY;
   cfg.show_peaks = true;
   cfg.show_valleys = true;
   cfg.draw_nodes = false;
   cfg.draw_labels = false;
   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;
   cfg.max_bars_to_scan = runtime_cfg.hook_scan_bars;
   cfg.max_nodes = InpBTHookMaxNodes;
   cfg.max_nodes_to_draw = 0;
}

void FP_LoadNDSBacktestHookConfig(const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                  FP_HookPhase02Config &cfg)
{
   FP_ResetHookPhase02Config(cfg);
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_HOOK_ONLY;
   cfg.origin_policy = InpBTHookOriginPolicy;
   cfg.show_positive = InpBTHookShowPositive;
   cfg.show_negative = InpBTHookShowNegative;

   cfg.draw_sequences = false;
   cfg.draw_origin = false;
   cfg.draw_x_nodes = false;
   cfg.draw_node_markers = false;
   cfg.draw_x_lines = false;
   cfg.draw_death_boundary = false;
   cfg.draw_cycle_arc = false;
   cfg.draw_sequence_count_label = false;
   cfg.draw_labels = false;
   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_bars_to_scan = runtime_cfg.hook_scan_bars;
   cfg.max_sequences = InpBTHookMaxSequences;
   cfg.max_sequences_to_draw = 0;
   cfg.require_confirmed_resolve_node = InpBTHookRequireConfirmedResolveNode;
   cfg.death_on_boundary_touch = InpBTHookDeathOnBoundaryTouch;
   cfg.require_near_death_for_semantic_arc = InpBTHookRequireNearDeathForSemanticArc;
   cfg.seed_used_nodes_cannot_restart = InpBTHookSeedUsedNodesCannotRestart;
   cfg.show_only_valid_hooks = InpBTHookShowOnlyValidHooks;
   cfg.valid_only_require_near_death = InpBTHookValidOnlyRequireNearDeath;
   cfg.valid_f3_require_same_scale = InpBTHookValidF3RequireSameScale;
   cfg.valid_f3_require_opposite_direction = InpBTHookValidF3RequireOppositeDirection;
   cfg.valid_only_fallback_to_structural = InpBTHookValidOnlyFallbackToStructural;
   cfg.post_f3_recognition_mode = InpBTHookPostF3RecognitionMode;
   cfg.post_f3_selection_priority = InpBTHookPostF3SelectionPriority;
   cfg.post_f3_allow_direct_terminal_hook = InpBTHookPostF3AllowDirectTerminalHook;
   cfg.post_f3_allow_delayed_rebound_hook = InpBTHookPostF3AllowDelayedReboundHook;
   cfg.post_f3_max_search_bars = InpBTHookPostF3MaxSearchBars;
   cfg.post_f3_terminal_tolerance_bars = InpBTHookPostF3TerminalToleranceBars;
   cfg.post_f3_terminal_tolerance_price_points = InpBTHookPostF3TerminalTolerancePricePoints;
   cfg.post_f3_geometric_min_completion_pct = InpBTHookPostF3GeometricMinCompletionPct;
   cfg.near_death_retrace_threshold = InpBTHookNearDeathRetraceThreshold;
   cfg.min_x_nodes_to_keep = InpBTHookMinXNodesToKeep;
   cfg.max_x_nodes_per_sequence = InpBTHookMaxXNodesPerSequence;
}

void FP_LoadNDSBacktestTradeConfig(FP_NDSHookTradeConfig &cfg)
{
   FP_ResetNDSHookTradeConfig(cfg);
   cfg.enabled = InpBTTradeEnabled;
   cfg.send_live_orders = InpBTSendTesterOrders;
   cfg.profile = InpBTTradeProfile;
   cfg.hook_entry_ratio = InpBTHookEntryRatio;
   cfg.hook_entry_min_x_count = InpBTHookEntryMinXCount;
   cfg.hook_entry_max_x_count = InpBTHookEntryMaxXCount;
   cfg.hook_entry_require_confirmed_terminal = InpBTRequireConfirmedTerminal;
   cfg.hook_entry_require_level_untouched = InpBTRequireLevelUntouched;
   cfg.fixed_reward_r = InpBTFixedRewardR;
   cfg.allow_hook_after_hook = InpBTAllowHookAfterHook;
   cfg.allow_hook_after_f3 = InpBTAllowHookAfterF3;
   cfg.require_closed_hook = InpBTRequireClosedHook;
   cfg.one_attempt_per_hook = InpBTOneAttemptPerHook;
   cfg.reset_used_setups_on_init = InpBTResetUsedSetupsOnInit;
   cfg.cancel_pending_on_death = InpBTCancelPendingOnDeath;
   cfg.require_full_f123_after_entry = InpBTRequireFullF123AfterEntry;
   cfg.sizing_mode = InpBTSizingMode;
   cfg.fixed_volume = InpBTFixedVolume;
   cfg.risk_cash = InpBTRiskCash;
   cfg.commission_per_lot_round_turn = InpBTCommissionPerLotRoundTurn;
   cfg.allow_min_lot_if_risk_too_small = InpBTAllowMinLotIfRiskTooSmall;
   cfg.stop_buffer_points = InpBTStopBufferPoints;
   cfg.stop_spread_multiplier = InpBTStopSpreadMultiplier;
   cfg.max_deviation_points = InpBTMaxDeviationPoints;
   cfg.entry_lock_timeout_seconds = InpBTEntryLockTimeoutSeconds;
   cfg.magic = InpBTMagic;
   cfg.comment_prefix = InpBTCommentPrefix;
   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.folder = "FlagCountingPhoenix";
}

bool FP_NDSBTRunOnce()
{
   FP_NDSBacktestRunReport report;
   bool ok = FP_RunNDSLightweightBacktestCycle(_Symbol, _Period,
                                                g_nds_bt_runtime_cfg,
                                                g_nds_bt_detector_cfg,
                                                g_nds_bt_node_cfg,
                                                g_nds_bt_hook_cfg,
                                                g_nds_bt_trade_cfg,
                                                report);
   FP_NDSBacktestUpdateStats(report, g_nds_bt_stats);

   bool scheduled_print = (g_nds_bt_runtime_cfg.print_run_summary &&
                           (g_nds_bt_stats.runs == 1 ||
                            (g_nds_bt_stats.runs % (ulong)g_nds_bt_runtime_cfg.print_every_n_runs) == 0));
   bool meaningful_transition = (report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT ||
                                 report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED ||
                                 report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_POSITION_CLOSED_F3);
   bool unexpected_failure = (!ok &&
                              report.status != "NOT_ENOUGH_CLOSED_BARS" &&
                              report.status != "TIMEBASE_FAILED");
   if(scheduled_print || meaningful_transition || unexpected_failure || g_nds_bt_stats.runs == 1)
      FP_PrintNDSBacktestRunReport("NDS_BT", g_nds_bt_runtime_cfg, report);

   return ok;
}

int OnInit()
{
   bool tester_runtime = FP_NDSBTIsTesterRuntime();
   if(!tester_runtime && !InpBTAllowNonTesterDryRun)
   {
      Print("NDS_BT_INIT status=blocked reason=backtest_executable_requires_strategy_tester");
      return INIT_FAILED;
   }

   FP_LoadNDSBacktestRuntimeConfig(g_nds_bt_runtime_cfg);
   FP_LoadNDSBacktestDetectorConfig(g_nds_bt_runtime_cfg, g_nds_bt_detector_cfg);
   FP_LoadNDSBacktestNodeConfig(g_nds_bt_runtime_cfg, g_nds_bt_node_cfg);
   FP_LoadNDSBacktestHookConfig(g_nds_bt_runtime_cfg, g_nds_bt_hook_cfg);
   FP_LoadNDSBacktestTradeConfig(g_nds_bt_trade_cfg);
   if(!tester_runtime)
      g_nds_bt_trade_cfg.send_live_orders = false;
   FP_ResetNDSBacktestSessionStats(g_nds_bt_stats);

   if(g_nds_bt_trade_cfg.reset_used_setups_on_init)
      FP_NDSHookTradeResetUsedSetups(g_nds_bt_trade_cfg);

   g_nds_bt_last_open_bar = (g_nds_bt_runtime_cfg.run_on_first_tick ? 0 : iTime(_Symbol, _Period, 0));

   Print("NDS_BT_INIT status=ready version=", FP_NDS_BACKTEST_VERSION,
         " runtime_profile=", FP_NDSBacktestProfileName(g_nds_bt_runtime_cfg.profile),
         " trade_profile=", FP_NDSHookTradeProfileName(g_nds_bt_trade_cfg.profile),
         " bars=", g_nds_bt_runtime_cfg.requested_bars,
         " hook_bars=", g_nds_bt_runtime_cfg.hook_scan_bars,
         " tester=", (tester_runtime ? "true" : "false"),
         " orders=", (g_nds_bt_trade_cfg.send_live_orders ? "enabled" : "paper_only"));
   return INIT_SUCCEEDED;
}

void OnTick()
{
   datetime current_open_bar = iTime(_Symbol, _Period, 0);
   if(current_open_bar <= 0)
      return;
   if(current_open_bar == g_nds_bt_last_open_bar)
      return;

   g_nds_bt_last_open_bar = current_open_bar;
   FP_NDSBTRunOnce();
}

void OnDeinit(const int reason)
{
   if(InpBTPrintSessionSummary)
      FP_PrintNDSBacktestSessionStats("NDS_BT_SESSION", g_nds_bt_stats);
}
