#property strict
#property version   "13.00"
#property description "FlagCounting Phoenix: clean root rebuild of the flag-counting sequence engine."

#include "../../Include/FlagCountingPhoenix/FP_Audit.mqh"
#include "../../Include/FlagCountingPhoenix/FP_Timebase.mqh"
#include "../../Include/FlagCountingPhoenix/FP_ExportEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_ValidationEngine.mqh"

// ------------------------------ Data / redraw -------------------------------
// Level 01 canonical candle stream. InpBarsToScan means requested CLOSED bars
// when InpUseClosedBarsOnly=true. The loader copies one extra raw bar and drops
// the current forming live candle before any structural engine runs.
input int  InpBarsToScan = 5000;
input bool InpUseClosedBarsOnly = true;
input bool InpStrictTimebase = true;
input int  InpMinClosedBars = 200;
input bool InpPrintTimebaseSanity = true;
input bool InpPrintTimebaseSamples = false;
input bool InpRedrawOnNewBarOnly = true;

// ------------------------------ Scales --------------------------------------
input bool InpUseMultiScale = true;
input int  InpSwingL1 = 2;
input int  InpSwingL2 = 3;
input int  InpSwingL3 = 5;
input int  InpSwingL4 = 8;
input int  InpSwingL5 = 13;
input int  InpSwingL6 = 21;
input int  InpSwingL7 = 34;
input int  InpSwingL8 = 55;
input bool InpIncludePendingNodes = false;
input bool InpPrintNodeSanity = true;
input bool InpPrintNodeSamples = false;
input int  InpNodeSampleLimit = 6;
input bool InpPrintIdentitySanity = true;
input bool InpPrintIdentitySamples = false;
input int  InpIdentitySampleLimit = 6;
input bool InpPrintHookSanity = true;
input bool InpPrintHookSamples = false;
input int  InpHookSampleLimit = 6;
input bool InpPrintBodySanity = true;
input bool InpPrintBodySamples = false;
input int  InpBodySampleLimit = 6;
input bool InpPrintInternalSanity = true;
input bool InpPrintInternalSamples = false;
input int  InpInternalSampleLimit = 6;
input bool InpPrintF1Sanity = true;
input bool InpPrintF1Samples = false;
input int  InpF1SampleLimit = 6;
input bool InpPrintF2Sanity = true;
input bool InpPrintF2Samples = false;
input int  InpF2SampleLimit = 6;
input bool InpPrintF3Sanity = true;
input bool InpPrintF3Samples = false;
input int  InpF3SampleLimit = 6;
input bool InpPrintOwnershipSanity = true;
input bool InpPrintOwnershipSamples = false;
input int  InpOwnershipSampleLimit = 8;
input bool InpPrintCanonicalSanity = true;
input bool InpPrintCanonicalSamples = false;
input int  InpCanonicalSampleLimit = 8;
input bool InpPrintExportSanity = true;
input bool InpPrintExportSamples = false;
input int  InpExportSampleLimit = 5;
input bool InpPrintRenderSanity = true;
input bool InpPrintRenderSamples = false;
input int  InpRenderSampleLimit = 8;
input bool InpPrintValidationSanity = true;
input bool InpPrintValidationSamples = false;
input int  InpValidationSampleLimit = 8;

// ------------------------------ Engine switches -----------------------------
input bool InpScanHooks = true;
input bool InpScanF1 = true;
input bool InpScanF2 = true;
input bool InpScanF3 = true;
input bool InpShowInvalidatedInAudit = false;
input bool InpKeepConfirmedF1F2AfterBoundaryHit = false;

// F1 phase boundary policy. Preferred mode is semantic gate with fail-open
// inspection. Set fail-open false only after Hook/ND coverage is verified.
input bool InpRequireF1PhaseBoundary = true;
input bool InpAllowF1FailOpenWhenNoHook = true;
input bool InpEnforceSingleChainPerDirectionScale = false;
input bool InpEnforceSingleChainPerDirectionGlobal = false;
input bool InpAbsorbPreInternalExtensions = true;
input bool InpHideSupersededParentStates = true;
input bool InpCompactHookRendering = true;
input bool InpStrictMainChartOwnership = true;
input int  InpOwnershipScoreMargin = 25;
input bool InpOwnershipHideOrphans = true;
input bool InpCanonicalStrictInvariants = true;
input bool InpCanonicalHideUnresolvedOrphans = true;
input bool InpHookMainRequiresVisibleF1 = true;
input bool InpHookKeepUnseededVisibleForDebug = false;
input bool InpF1ShowPostFlagCandidates = true;
input bool InpF1ShowLiveBodyCandidates = true;
input bool InpF2ShowSizeRejectedCandidates = false;
input bool InpF2ShowPostFlagCandidates = true;
input bool InpF2ShowLiveBodyCandidates = true;
input bool InpF3ShowORRejectedCandidates = false;
input bool InpF3ShowLiveBodyCandidates = true;

// ------------------------------ Rules ---------------------------------------
input int    InpMaxEvents = 6000;
input int    InpMaxHooks = 6000;
input int    InpMaxRootsPerScaleDirection = 0;
input double InpBoundaryEpsilonPoints = 0.0;
input double InpF2MinParentSizeRatio = 1.0;
input double InpF3MinParentSizeRatio = 0.70;
input double InpF3Leg1LMinRatio = 0.80;
input double InpNDMinRetraceRatio = 0.50;
input bool   InpNDAllowBelowHalfCycle = false;
input bool   InpVerboseAuditLogs = false;

// ------------------------------ Raw audit export ----------------------------
input bool   InpExportAuditFiles = false;
input string InpExportFolder = "FlagCountingPhoenix";
input string InpExportRunTag = "";
input bool   InpExportVisibleOnly = false;
input bool   InpExportEventsCsv = true;
input bool   InpExportHooksCsv = true;
input bool   InpExportSummaryCsv = true;
input bool   InpExportManifestCsv = true;
input bool   InpExportOverwriteLatest = true;
input int    InpExportMaxEvents = 0;
input int    InpExportMaxHooks = 0;

// ------------------------------ Validation ----------------------------------
input bool   InpValidationEnabled = false;
input string InpValidationCaseId = "manual";
input string InpValidationSuiteTag = "phoenix_level13";
input string InpValidationFolder = "FlagCountingPhoenix";
input bool   InpValidationWriteCsv = true;
input bool   InpValidationOverwriteLatest = true;
input bool   InpValidationStrict = true;
input bool   InpValidationBaselineMode = true;
input bool   InpValidationRequireExportOk = false;
input bool   InpValidationRequireRenderOk = true;
input bool   InpValidationRequireNoCanonicalFailures = true;
input bool   InpValidationRequireNoRenderErrors = true;
input bool   InpValidationRequireNoExportErrors = false;
input int    InpValidationExpectedMinBars = -1;
input int    InpValidationExpectedMaxBars = -1;
input int    InpValidationExpectedMinScales = -1;
input int    InpValidationExpectedMaxScales = -1;
input int    InpValidationExpectedMinRawNodes = -1;
input int    InpValidationExpectedMaxRawNodes = -1;
input int    InpValidationExpectedMinCanonicalNodes = -1;
input int    InpValidationExpectedMaxCanonicalNodes = -1;
input int    InpValidationExpectedMinHooks = -1;
input int    InpValidationExpectedMaxHooks = -1;
input int    InpValidationExpectedMinND = -1;
input int    InpValidationExpectedMaxND = -1;
input int    InpValidationExpectedMinEvents = -1;
input int    InpValidationExpectedMaxEvents = -1;
input int    InpValidationExpectedMinVisibleEvents = -1;
input int    InpValidationExpectedMaxVisibleEvents = -1;
input int    InpValidationExpectedMinHiddenEvents = -1;
input int    InpValidationExpectedMaxHiddenEvents = -1;
input int    InpValidationExpectedMinF1 = -1;
input int    InpValidationExpectedMaxF1 = -1;
input int    InpValidationExpectedMinF2 = -1;
input int    InpValidationExpectedMaxF2 = -1;
input int    InpValidationExpectedMinF3 = -1;
input int    InpValidationExpectedMaxF3 = -1;
input int    InpValidationExpectedMinLockedF3 = -1;
input int    InpValidationExpectedMaxLockedF3 = -1;

// ------------------------------ Rendering -----------------------------------
input string InpObjectPrefix = "DAL_FCP_";
input bool   InpCleanObjectsOnInit = true;
input bool   InpCleanObjectsOnDeinit = true;
input int    InpMaxEventsToDraw = 1200;
input int    InpMaxHooksToDraw = 120;
input bool   InpDrawF1 = true;
input bool   InpDrawF2 = true;
input bool   InpDrawF3 = true;
input bool   InpDrawBullish = true;
input bool   InpDrawBearish = true;
input bool   InpDrawCandidates = true;
input bool   InpDrawConfirmed = true;
input bool   InpDrawLocked = true;
input bool   InpDrawInvalidated = false;
input bool   InpDrawHooks = true;
input bool   InpDrawOnlyFlagSeedHooks = true;
input bool   InpRenderStrictVisibility = true;
input bool   InpRenderUseCanonicalObjectNames = true;
input bool   InpRenderDeleteExistingByPrefix = true;
input bool   InpRenderDrawHookBack = true;
input bool   InpShowHookCountLabels = false;
input bool   InpDetailedLabels = false;
input bool   InpForceCleanMainChartLabels = true;
input bool   InpShowParentIds = false;
input bool   InpShowOriginLabels = false;
input bool   InpShowInternalLabels = false;
input bool   InpUseSequenceColorShades = true;
input int    InpFixedLineWidth = 1;
input int    InpCurveSegments = 32;
input int    InpLabelFontSize = 8;

input color InpBullishCandidateColor = clrDeepSkyBlue;
input color InpBullishConfirmedColor = clrLime;
input color InpBearishCandidateColor = clrOrange;
input color InpBearishConfirmedColor = clrTomato;
input color InpF3LockedColor = clrMagenta;
input color InpHookColor = clrGray;

static datetime g_fp_last_bar_time = 0;

bool FP_ShouldRedraw()
{
   datetime t = iTime(_Symbol, _Period, 0);
   if(!InpRedrawOnNewBarOnly) return true;
   if(t != g_fp_last_bar_time)
   {
      g_fp_last_bar_time = t;
      return true;
   }
   return false;
}

void FP_LoadConfig(FP_Config &cfg)
{
   FP_DefaultConfig(cfg);
   cfg.include_pending_nodes = InpIncludePendingNodes;
   cfg.scan_hooks = InpScanHooks;
   cfg.scan_f1 = InpScanF1;
   cfg.scan_f2 = InpScanF2;
   cfg.scan_f3 = InpScanF3;
   cfg.show_invalidated_in_audit = InpShowInvalidatedInAudit;
   cfg.keep_confirmed_f1f2_after_boundary_hit = InpKeepConfirmedF1F2AfterBoundaryHit;

   cfg.require_f1_phase_boundary = InpRequireF1PhaseBoundary;
   cfg.allow_f1_fail_open_when_no_hook = InpAllowF1FailOpenWhenNoHook;
   cfg.enforce_single_chain_per_direction_scale = InpEnforceSingleChainPerDirectionScale;
   cfg.enforce_single_chain_per_direction_global = InpEnforceSingleChainPerDirectionGlobal;
   cfg.absorb_pre_internal_extensions = InpAbsorbPreInternalExtensions;
   cfg.hide_superseded_parent_states = InpHideSupersededParentStates;
   cfg.compact_hook_rendering = InpCompactHookRendering;
   cfg.strict_main_chart_ownership = InpStrictMainChartOwnership;
   cfg.print_ownership_sanity = InpPrintOwnershipSanity;
   cfg.print_ownership_samples = InpPrintOwnershipSamples;
   cfg.ownership_sample_limit = InpOwnershipSampleLimit;
   cfg.ownership_score_margin = InpOwnershipScoreMargin;
   cfg.ownership_hide_orphans = InpOwnershipHideOrphans;
   cfg.print_canonical_sanity = InpPrintCanonicalSanity;
   cfg.print_canonical_samples = InpPrintCanonicalSamples;
   cfg.canonical_sample_limit = InpCanonicalSampleLimit;
   cfg.canonical_strict_invariants = InpCanonicalStrictInvariants;
   cfg.canonical_hide_unresolved_orphans = InpCanonicalHideUnresolvedOrphans;
   cfg.print_hook_sanity = InpPrintHookSanity;
   cfg.print_hook_samples = InpPrintHookSamples;
   cfg.hook_sample_limit = InpHookSampleLimit;
   cfg.hook_main_requires_visible_f1 = InpHookMainRequiresVisibleF1;
   cfg.hook_keep_unseeded_visible_for_debug = InpHookKeepUnseededVisibleForDebug;
   cfg.print_body_sanity = InpPrintBodySanity;
   cfg.print_body_samples = InpPrintBodySamples;
   cfg.body_sample_limit = InpBodySampleLimit;
   cfg.print_internal_sanity = InpPrintInternalSanity;
   cfg.print_internal_samples = InpPrintInternalSamples;
   cfg.internal_sample_limit = InpInternalSampleLimit;
   cfg.print_f1_sanity = InpPrintF1Sanity;
   cfg.print_f1_samples = InpPrintF1Samples;
   cfg.f1_sample_limit = InpF1SampleLimit;
   cfg.f1_show_post_flag_candidates = InpF1ShowPostFlagCandidates;
   cfg.f1_show_live_body_candidates = InpF1ShowLiveBodyCandidates;
   cfg.print_f2_sanity = InpPrintF2Sanity;
   cfg.print_f2_samples = InpPrintF2Samples;
   cfg.f2_sample_limit = InpF2SampleLimit;
   cfg.f2_show_size_rejected_candidates = InpF2ShowSizeRejectedCandidates;
   cfg.f2_show_post_flag_candidates = InpF2ShowPostFlagCandidates;
   cfg.f2_show_live_body_candidates = InpF2ShowLiveBodyCandidates;
   cfg.print_f3_sanity = InpPrintF3Sanity;
   cfg.print_f3_samples = InpPrintF3Samples;
   cfg.f3_sample_limit = InpF3SampleLimit;
   cfg.f3_show_or_rejected_candidates = InpF3ShowORRejectedCandidates;
   cfg.f3_show_live_body_candidates = InpF3ShowLiveBodyCandidates;

   cfg.max_events = InpMaxEvents;
   cfg.max_hooks = InpMaxHooks;
   cfg.max_roots_per_scale_direction = InpMaxRootsPerScaleDirection;
   cfg.print_node_sanity = InpPrintNodeSanity;
   cfg.print_node_samples = InpPrintNodeSamples;
   cfg.node_sample_limit = InpNodeSampleLimit;
   cfg.context_symbol = _Symbol;
   cfg.context_timeframe = EnumToString(_Period);
   cfg.identity_generation_pass = "phoenix_level13";
   cfg.identity_config_hash = "eps" + DoubleToString(InpBoundaryEpsilonPoints, 2) +
                              "_f2" + DoubleToString(InpF2MinParentSizeRatio, 2) +
                              "_f3" + DoubleToString(InpF3MinParentSizeRatio, 2) +
                              "_hook" + FP_BoolName(InpScanHooks) +
                              "_hookseed" + FP_BoolName(InpHookMainRequiresVisibleF1) +
                              "_body" + FP_BoolName(InpPrintBodySanity) +
                              "_internal" + FP_BoolName(InpPrintInternalSanity) +
                              "_f1" + FP_BoolName(InpPrintF1Sanity) +
                              "_f1post" + FP_BoolName(InpF1ShowPostFlagCandidates) +
                              "_f1live" + FP_BoolName(InpF1ShowLiveBodyCandidates) +
                              "_f2" + FP_BoolName(InpPrintF2Sanity) +
                              "_f2size" + FP_BoolName(InpF2ShowSizeRejectedCandidates) +
                              "_f2post" + FP_BoolName(InpF2ShowPostFlagCandidates) +
                              "_f2live" + FP_BoolName(InpF2ShowLiveBodyCandidates) +
                              "_f3" + FP_BoolName(InpPrintF3Sanity) +
                              "_f3or" + FP_BoolName(InpF3ShowORRejectedCandidates) +
                              "_f3live" + FP_BoolName(InpF3ShowLiveBodyCandidates) +
                              "_own" + FP_BoolName(InpStrictMainChartOwnership) +
                              "_ownmargin" + IntegerToString(InpOwnershipScoreMargin) +
                              "_orphan" + FP_BoolName(InpOwnershipHideOrphans) +
                              "_canon" + FP_BoolName(InpPrintCanonicalSanity) +
                              "_canonstrict" + FP_BoolName(InpCanonicalStrictInvariants) +
                              "_canonorph" + FP_BoolName(InpCanonicalHideUnresolvedOrphans) +
                              "_export" + FP_BoolName(InpExportAuditFiles) +
                              "_exportvisible" + FP_BoolName(InpExportVisibleOnly) +
                              "_render" + FP_BoolName(InpPrintRenderSanity) +
                              "_rendercanon" + FP_BoolName(InpRenderUseCanonicalObjectNames) +
                              "_renderstrict" + FP_BoolName(InpRenderStrictVisibility) +
                              "_validation" + FP_BoolName(InpValidationEnabled) +
                              "_validationcase" + InpValidationCaseId +
                              "_failopen" + FP_BoolName(InpAllowF1FailOpenWhenNoHook);
   cfg.print_identity_sanity = InpPrintIdentitySanity;
   cfg.print_identity_samples = InpPrintIdentitySamples;
   cfg.identity_sample_limit = InpIdentitySampleLimit;
   cfg.boundary_epsilon_points = InpBoundaryEpsilonPoints;
   cfg.f2_min_parent_size_ratio = InpF2MinParentSizeRatio;
   cfg.f3_min_parent_size_ratio = InpF3MinParentSizeRatio;
   cfg.f3_leg1_L_min_ratio = InpF3Leg1LMinRatio;
   cfg.nd_min_retrace_ratio = InpNDMinRetraceRatio;
   cfg.nd_allow_below_half_cycle = InpNDAllowBelowHalfCycle;
   cfg.verbose_logs = InpVerboseAuditLogs;
}

void FP_LoadExportConfig(FP_ExportConfig &cfg)
{
   FP_DefaultExportConfig(cfg);
   cfg.enabled = InpExportAuditFiles;
   cfg.export_events_csv = InpExportEventsCsv;
   cfg.export_hooks_csv = InpExportHooksCsv;
   cfg.export_summary_csv = InpExportSummaryCsv;
   cfg.export_manifest_csv = InpExportManifestCsv;
   cfg.visible_only = InpExportVisibleOnly;
   cfg.overwrite_latest = InpExportOverwriteLatest;
   cfg.folder = InpExportFolder;
   cfg.run_tag = InpExportRunTag;
   cfg.max_events = InpExportMaxEvents;
   cfg.max_hooks = InpExportMaxHooks;
   cfg.print_sanity = InpPrintExportSanity;
   cfg.print_samples = InpPrintExportSamples;
   cfg.sample_limit = InpExportSampleLimit;
}

void FP_LoadRenderConfig(FP_RenderConfig &cfg)
{
   FP_DefaultRenderConfig(cfg);
   cfg.prefix = InpObjectPrefix;
   cfg.max_events_to_draw = InpMaxEventsToDraw;
   cfg.max_hooks_to_draw = InpMaxHooksToDraw;
   cfg.draw_f1 = InpDrawF1;
   cfg.draw_f2 = InpDrawF2;
   cfg.draw_f3 = InpDrawF3;
   cfg.draw_bull = InpDrawBullish;
   cfg.draw_bear = InpDrawBearish;
   cfg.draw_candidates = InpDrawCandidates;
   cfg.draw_confirmed = InpDrawConfirmed;
   cfg.draw_locked = InpDrawLocked;
   cfg.draw_invalidated = InpDrawInvalidated;
   cfg.draw_hooks = InpDrawHooks;
   cfg.draw_only_flag_seed_hooks = InpDrawOnlyFlagSeedHooks;
   cfg.strict_visibility = InpRenderStrictVisibility;
   cfg.use_canonical_object_names = InpRenderUseCanonicalObjectNames;
   cfg.delete_existing_by_prefix = InpRenderDeleteExistingByPrefix;
   cfg.draw_hook_back = InpRenderDrawHookBack;
   cfg.show_hook_count_labels = (InpForceCleanMainChartLabels && !InpDetailedLabels ? false : InpShowHookCountLabels);
   cfg.detailed_labels = InpDetailedLabels;
   cfg.show_parent_ids = (InpForceCleanMainChartLabels && !InpDetailedLabels ? false : InpShowParentIds);
   cfg.show_origin_labels = (InpForceCleanMainChartLabels && !InpDetailedLabels ? false : InpShowOriginLabels);
   cfg.show_internal_labels = (InpForceCleanMainChartLabels && !InpDetailedLabels ? false : InpShowInternalLabels);
   cfg.use_sequence_color_shades = InpUseSequenceColorShades;
   cfg.fixed_line_width = InpFixedLineWidth;
   cfg.curve_segments = InpCurveSegments;
   cfg.label_font_size = InpLabelFontSize;
   cfg.bull_candidate = InpBullishCandidateColor;
   cfg.bull_confirmed = InpBullishConfirmedColor;
   cfg.bear_candidate = InpBearishCandidateColor;
   cfg.bear_confirmed = InpBearishConfirmedColor;
   cfg.f3_locked = InpF3LockedColor;
   cfg.hook_color = InpHookColor;
   cfg.print_sanity = InpPrintRenderSanity;
   cfg.print_samples = InpPrintRenderSamples;
   cfg.sample_limit = InpRenderSampleLimit;
}


void FP_LoadValidationConfig(FP_ValidationConfig &cfg)
{
   FP_DefaultValidationConfig(cfg);
   cfg.enabled = InpValidationEnabled;
   cfg.case_id = InpValidationCaseId;
   cfg.suite_tag = InpValidationSuiteTag;
   cfg.folder = InpValidationFolder;
   cfg.write_csv = InpValidationWriteCsv;
   cfg.overwrite_latest = InpValidationOverwriteLatest;
   cfg.strict = InpValidationStrict;
   cfg.baseline_mode = InpValidationBaselineMode;
   cfg.require_export_ok = InpValidationRequireExportOk;
   cfg.require_render_ok = InpValidationRequireRenderOk;
   cfg.require_no_canonical_failures = InpValidationRequireNoCanonicalFailures;
   cfg.require_no_render_errors = InpValidationRequireNoRenderErrors;
   cfg.require_no_export_errors = InpValidationRequireNoExportErrors;
   cfg.print_sanity = InpPrintValidationSanity;
   cfg.print_samples = InpPrintValidationSamples;
   cfg.sample_limit = InpValidationSampleLimit;

   cfg.expected_min_bars = InpValidationExpectedMinBars;
   cfg.expected_max_bars = InpValidationExpectedMaxBars;
   cfg.expected_min_scales = InpValidationExpectedMinScales;
   cfg.expected_max_scales = InpValidationExpectedMaxScales;
   cfg.expected_min_raw_nodes = InpValidationExpectedMinRawNodes;
   cfg.expected_max_raw_nodes = InpValidationExpectedMaxRawNodes;
   cfg.expected_min_canonical_nodes = InpValidationExpectedMinCanonicalNodes;
   cfg.expected_max_canonical_nodes = InpValidationExpectedMaxCanonicalNodes;
   cfg.expected_min_hooks = InpValidationExpectedMinHooks;
   cfg.expected_max_hooks = InpValidationExpectedMaxHooks;
   cfg.expected_min_nd = InpValidationExpectedMinND;
   cfg.expected_max_nd = InpValidationExpectedMaxND;
   cfg.expected_min_events = InpValidationExpectedMinEvents;
   cfg.expected_max_events = InpValidationExpectedMaxEvents;
   cfg.expected_min_visible_events = InpValidationExpectedMinVisibleEvents;
   cfg.expected_max_visible_events = InpValidationExpectedMaxVisibleEvents;
   cfg.expected_min_hidden_events = InpValidationExpectedMinHiddenEvents;
   cfg.expected_max_hidden_events = InpValidationExpectedMaxHiddenEvents;
   cfg.expected_min_f1 = InpValidationExpectedMinF1;
   cfg.expected_max_f1 = InpValidationExpectedMaxF1;
   cfg.expected_min_f2 = InpValidationExpectedMinF2;
   cfg.expected_max_f2 = InpValidationExpectedMaxF2;
   cfg.expected_min_f3 = InpValidationExpectedMinF3;
   cfg.expected_max_f3 = InpValidationExpectedMaxF3;
   cfg.expected_min_locked_f3 = InpValidationExpectedMinLockedF3;
   cfg.expected_max_locked_f3 = InpValidationExpectedMaxLockedF3;
}

void FP_Run()
{
   MqlRates rates[];

   FP_TimebaseConfig timebase_cfg;
   FP_DefaultTimebaseConfig(timebase_cfg);
   timebase_cfg.symbol = _Symbol;
   timebase_cfg.period = _Period;
   timebase_cfg.requested_bars = InpBarsToScan;
   timebase_cfg.min_closed_bars = InpMinClosedBars;
   timebase_cfg.exclude_live_bar = InpUseClosedBarsOnly;
   timebase_cfg.require_ascending_time = true;
   timebase_cfg.strict_contract = InpStrictTimebase;
   timebase_cfg.print_sanity = InpPrintTimebaseSanity;
   timebase_cfg.print_samples = InpPrintTimebaseSamples;

   FP_TimebaseReport timebase_report;
   int copied = FP_LoadCanonicalRates(timebase_cfg, rates, timebase_report);

   if(InpPrintTimebaseSanity || !timebase_report.ok)
      FP_PrintTimebaseReport("FP_LEVEL01", timebase_report);
   if(InpPrintTimebaseSamples)
      FP_PrintTimebaseSamples("FP_LEVEL01", rates, copied);

   if(!timebase_report.ok && InpStrictTimebase)
   {
      Print("FP_SUMMARY status=timebase_failed reason=", timebase_report.reason,
            " bars=", copied,
            " status_detail=", timebase_report.status);
      return;
   }

   if(copied < InpMinClosedBars)
   {
      Print("FP_SUMMARY status=not_enough_closed_bars copied=", copied,
            " min=", InpMinClosedBars);
      return;
   }

   int scales[];
   int scale_count = FP_BuildScaleList(InpUseMultiScale,
                                       InpSwingL1,
                                       InpSwingL2,
                                       InpSwingL3,
                                       InpSwingL4,
                                       InpSwingL5,
                                       InpSwingL6,
                                       InpSwingL7,
                                       InpSwingL8,
                                       scales);
   if(scale_count <= 0)
   {
      Print("FP_SUMMARY status=no_scales");
      return;
   }

   FP_Config cfg;
   FP_LoadConfig(cfg);

   FP_FlagEvent events[];
   FP_HookBranch hooks[];
   FP_DetectResult result;
   FP_DetectAllScales(rates, copied, scales, scale_count, cfg, events, hooks, result);

   FP_ExportConfig export_cfg;
   FP_LoadExportConfig(export_cfg);
   FP_ExportReport export_report;
   if(export_cfg.enabled)
   {
      FP_ExportAuditWithReport(_Symbol, _Period, copied, scale_count, cfg, export_cfg, events, hooks, result, export_report);
      FP_ExportApplyReportToResult(export_report, result);
      if(export_cfg.print_sanity)
         FP_PrintExportReport("FP_LEVEL11_5", export_report);
      if(export_cfg.print_samples)
         FP_PrintExportSamples("FP_LEVEL11_5", export_report, events, hooks, export_cfg.sample_limit);
   }

   FP_RenderConfig render_cfg;
   FP_LoadRenderConfig(render_cfg);
   FP_RenderReport render_report;
   int drawn = FP_DrawAllWithReport(events, hooks, rates, copied, render_cfg, render_report);
   FP_RenderApplyReportToResult(render_report, result);
   if(render_cfg.print_sanity)
      FP_PrintRenderReport("FP_LEVEL12", render_report);
   if(render_cfg.print_samples)
      FP_PrintRenderSamples("FP_LEVEL12", render_report);

   FP_ValidationConfig validation_cfg;
   FP_LoadValidationConfig(validation_cfg);
   FP_ValidationReport validation_report;
   string validation_rows[];
   if(validation_cfg.enabled)
   {
      FP_RunValidationWithReport(_Symbol, _Period, copied, scale_count, validation_cfg, events, hooks, result, validation_report, validation_rows);
      FP_ValidationApplyReportToResult(validation_report, result);
      if(validation_cfg.print_sanity)
         FP_PrintValidationReport("FP_LEVEL13", validation_report);
      if(validation_cfg.print_samples)
         FP_PrintValidationSamples("FP_LEVEL13", validation_report, validation_rows, validation_cfg.sample_limit);
   }

   FP_PrintSummary(_Symbol, _Period, copied, scale_count, result, drawn);
   if(InpVerboseAuditLogs)
   {
      for(int i=0; i<ArraySize(events); i++) FP_PrintEventAudit(events[i]);
      for(int h=0; h<ArraySize(hooks); h++) FP_PrintHookAudit(hooks[h]);
   }
}

int OnInit()
{
   if(InpCleanObjectsOnInit)
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
   g_fp_last_bar_time = 0;
   FP_Run();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(InpCleanObjectsOnDeinit)
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
}

void OnTick()
{
   if(FP_ShouldRedraw())
      FP_Run();
}
