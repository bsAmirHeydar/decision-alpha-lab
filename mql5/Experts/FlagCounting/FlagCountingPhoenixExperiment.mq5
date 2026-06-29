#property strict
#property version   "18.20"
#property description "FlagCounting Phoenix: clean root rebuild of the flag-counting sequence engine."

#include "../../Include/FlagCountingPhoenix/FP_Audit.mqh"
#include "../../Include/FlagCountingPhoenix/FP_Timebase.mqh"
#include "../../Include/FlagCountingPhoenix/FP_ExportEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_ValidationEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_ReleaseEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_InterfaceEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_AcceptanceEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_AmbiguityEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_StaticQaEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_LicenseEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_StateGateEngine.mqh"

// ------------------------------ Data / redraw -------------------------------
// Level 01 canonical candle stream. InpBarsToScan means requested CLOSED bars
// when InpUseClosedBarsOnly=true. The loader copies one extra raw bar and drops
// the current forming live candle before any structural engine runs.
input int  InpBarsToScan = 5000;
input bool InpUseClosedBarsOnly = true;
input bool InpStrictTimebase = true;
input int  InpMinClosedBars = 200;
input int  InpSessionCacheDepth = 15;
input bool InpPrintTimebaseSanity = true;
input bool InpPrintTimebaseSamples = false;
input bool InpRedrawOnNewBarOnly = true;

// ------------------------------ Scales --------------------------------------
input bool InpUseMultiScale = true;
input int  InpSwingL1 = 2;
input int  InpSwingL2 = 3;
input int  InpSwingL3 = 5;
input int  InpSwingL4 = 8;
input long InpNodeModelSeed = 0;
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
input bool InpPrintReleaseSanity = true;
input bool InpPrintReleaseSamples = false;
input int  InpReleaseSampleLimit = 8;
input bool InpPrintInterfaceSanity = true;
input bool InpPrintInterfaceSamples = false;
input int  InpInterfaceSampleLimit = 8;

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
input string InpPhaseModelProfile = "";
input bool InpHideSupersededParentStates = true;
input bool InpCompactHookRendering = true;
input bool InpStrictMainChartOwnership = true;
input bool InpOwnershipAllowVisualSoftReset = true;
input int  InpOwnershipScoreMargin = 25;
input bool InpOwnershipHideOrphans = true;
input bool InpCanonicalStrictInvariants = true;
input bool InpCanonicalHideUnresolvedOrphans = true;
input bool InpHookMainRequiresVisibleF1 = false;
input bool InpHookKeepUnseededVisibleForDebug = true;
input bool InpF1ShowPostFlagCandidates = true;
input bool InpF1ShowLiveBodyCandidates = true;
input bool InpF2ShowSizeRejectedCandidates = true;
input bool InpF2ShowPostFlagCandidates = true;
input bool InpF2ShowLiveBodyCandidates = true;
input bool InpF3ShowORRejectedCandidates = true;
input bool InpF3ShowLiveBodyCandidates = true;

// ------------------------------ Rules ---------------------------------------
input int    InpMaxEvents = 6000;
input int    InpMaxHooks = 6000;
input int    InpMaxRootsPerScaleDirection = 0;
input double InpBoundaryEpsilonPoints = 0.0;
input long   InpBoundaryModelSeed = 0;
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
input long   InpValidationModelSeed = 0;
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

// ------------------------------ Release / debug / rollback ------------------
input FP_ReleaseProfile InpReleaseProfile = FP_RELEASE_PROFILE_NORMAL;
input long InpReleaseModelSeed = 0;
input string InpReleaseRunTag = "";
input string InpReleaseFolder = "FlagCountingPhoenix";
input bool   InpReleaseWriteManifest = true;
input bool   InpReleaseOverwriteLatest = true;
input bool   InpReleaseStrictGate = false;
input bool   InpReleaseRequireValidationOk = false;
input bool   InpReleaseRequireExportOk = false;
input bool   InpReleaseRequireRenderOk = true;
input bool   InpReleaseRequireNoRenderErrors = true;
input bool   InpReleaseRequireNoExportErrors = false;
input bool   InpReleaseRequireNoCanonicalFailures = true;
input bool   InpReleaseCleanObjectsForProfile = true;

// ------------------------------ Interface contracts -------------------------
input bool   InpInterfacePreflightEnabled = true;
input bool   InpInterfacePostflightEnabled = true;
input bool   InpInterfaceStrict = false;
input bool   InpInterfaceWriteCsv = false;
input bool   InpInterfaceOverwriteLatest = true;
input string InpInterfaceFolder = "FlagCountingPhoenix";
input string InpInterfaceRunTag = "";
input bool   InpInterfaceRequirePreflightOk = false;
input bool   InpInterfaceRequirePostflightOk = false;
input bool   InpInterfaceRequireResultPartition = true;
input bool   InpInterfaceRequirePublicIds = true;
input bool   InpInterfaceRequireParentContract = true;
input bool   InpInterfaceRequireCounterNonnegative = true;


// ------------------------------ Acceptance matrix --------------------------
input bool   InpAcceptanceEnabled = true;
input FP_AcceptanceMode InpAcceptanceMode = FP_ACCEPTANCE_MODE_OBSERVE;
input bool   InpAcceptanceStrict = false;
input bool   InpAcceptanceWriteCsv = false;
input bool   InpAcceptanceOverwriteLatest = true;
input string InpAcceptanceFolder = "FlagCountingPhoenix";
input string InpAcceptanceRunTag = "";
input string InpAcceptanceCaseId = "manual";
input bool   InpAcceptanceRequireLevel01Ok = true;
input bool   InpAcceptanceRequireNoCanonicalFailures = true;
input bool   InpAcceptanceRequireExportOkWhenEnabled = true;
input bool   InpAcceptanceRequireRenderOkWhenEnabled = true;
input bool   InpAcceptanceRequireValidationOkWhenEnabled = true;
input bool   InpAcceptanceRequireReleaseGateWhenStrict = false;
input bool   InpAcceptanceRequireInterfacePreOkWhenEnabled = false;
input bool   InpAcceptanceRequireInterfacePostOkWhenEnabled = false;
input bool   InpAcceptanceRequireVisiblePartition = true;
input bool   InpAcceptanceRequireLockedF3IfExpected = true;
input int    InpAcceptanceExpectedMinVisibleEvents = -1;
input int    InpAcceptanceExpectedMinF1 = -1;
input int    InpAcceptanceExpectedMinF2 = -1;
input int    InpAcceptanceExpectedMinF3 = -1;
input int    InpAcceptanceExpectedMinLockedF3 = -1;
input bool   InpPrintAcceptanceSanity = true;
input bool   InpPrintAcceptanceSamples = false;
input int    InpAcceptanceSampleLimit = 8;

// ------------------------------ Ambiguity / decision lock -------------------
input bool   InpAmbiguityEnabled = true;
input FP_AmbiguityMode InpAmbiguityMode = FP_AMBIGUITY_MODE_OBSERVE;
input bool   InpAmbiguityStrict = false;
input bool   InpAmbiguityWriteCsv = false;
input bool   InpAmbiguityOverwriteLatest = true;
input string InpAmbiguityFolder = "FlagCountingPhoenix";
input string InpAmbiguityRunTag = "";
input string InpAmbiguityCaseId = "manual";
input bool   InpAmbiguityRequireDecisionLock = true;
input bool   InpAmbiguityRequireNoReleaseBlockers = false;
input bool   InpAmbiguityRequireCanonicalSource = true;
input bool   InpAmbiguityRequireClosedBarDefault = true;
input bool   InpAmbiguityRequireConfirmedFBodies = true;
input bool   InpAmbiguityRequireStrictRendererVisibility = true;
input bool   InpAmbiguityRequireCanonicalObjectNames = true;
input bool   InpAmbiguityRequireSeededHookMainChart = false;
input bool   InpAmbiguityRequireExportBeforeRenderer = true;
input bool   InpAmbiguityRequireValidationBeforeRelease = true;
input bool   InpAmbiguityRequireAcceptanceBeforeSummary = true;
input bool   InpAmbiguityRequireInterfacePassAlignment = false;
input bool   InpAmbiguityAllowFailOpenDiagnostic = true;
input bool   InpAmbiguityAllowCandidateDisplayDiagnostic = true;
input bool   InpAmbiguityAllowORRejectedF3Diagnostic = true;
input bool   InpAmbiguityAllowDebugUnseededHooks = true;
input bool   InpPrintAmbiguitySanity = true;
input bool   InpPrintAmbiguitySamples = false;
input int    InpAmbiguitySampleLimit = 8;

// ------------------------------ Static QA / compile hardening ---------------
input bool   InpStaticQaEnabled = true;
input FP_StaticQaMode InpStaticQaMode = FP_STATIC_QA_MODE_OBSERVE;
input bool   InpStaticQaStrict = false;
input bool   InpStaticQaWriteCsv = false;
input bool   InpStaticQaOverwriteLatest = true;
input string InpStaticQaFolder = "FlagCountingPhoenix";
input string InpStaticQaRunTag = "";
input string InpStaticQaCaseId = "manual";
input bool   InpStaticQaRequireContractVersion = true;
input bool   InpStaticQaRequireIdentityPass = true;
input bool   InpStaticQaRequireInterfaceContractAlignment = true;
input bool   InpStaticQaRequireRuntimePartitions = true;
input bool   InpStaticQaRequireNonnegativeCounters = true;
input bool   InpStaticQaRequireReportAlignment = true;
input bool   InpStaticQaRequireIoAlignment = true;
input bool   InpStaticQaRequireReleaseSafeDefaults = true;
input bool   InpStaticQaRequireStaticToolPresent = true;
input bool   InpStaticQaRequireZeroRuntimeBlockers = false;
input bool   InpStaticQaAllowObserveWarnings = true;
input bool   InpStaticQaAllowDisabledExport = true;
input bool   InpStaticQaAllowDisabledValidation = true;
input bool   InpStaticQaAllowDisabledRender = false;
input bool   InpPrintStaticQaSanity = true;
input bool   InpPrintStaticQaSamples = false;
input int    InpStaticQaSampleLimit = 8;

// ------------------------------ Level 19 - State Gate Dashboard -------------
input bool            InpStateGateEnabled             = true;
input ENUM_TIMEFRAMES InpStateGateTf1                 = PERIOD_M1;
input ENUM_TIMEFRAMES InpStateGateTf2                 = PERIOD_M10;
input ENUM_TIMEFRAMES InpStateGateTf3                 = PERIOD_H1;
input bool            InpStateGatePanelEnabled        = true;
input bool            InpStateGatePanelStartMinimized = false;
input ENUM_BASE_CORNER InpStateGatePanelCorner         = CORNER_LEFT_UPPER;
input int             InpStateGatePanelX              = 16;
input int             InpStateGatePanelY              = 24;
input int             InpStateGatePanelWidth          = 560;
input int             InpStateGatePanelFontSize       = 8;
input int             InpStateGatePanelRallyPreviewRows = 2;
input int             InpStateGatePanelHookPreviewRows  = 2;
input bool            InpStateGatePanelForceRightUpper  = false;
input bool            InpStateGatePanelForceLeftUpper   = true;
input bool            InpStateGatePanelCompactMode      = true;
input bool            InpStateGatePanelShowClosedBar    = true;
input bool            InpStateGatePanelShowRowCounts    = true;
input bool            InpStateGatePanelShowContractKey  = true;
input bool            InpStateGatePanelShowDiagnostics = true;
input int             InpStateGateMaxRallyRowsPerTf   = 6;
input int             InpStateGateMaxHookRowsPerTf    = 10;
input int             InpStateGateMaxExtremeCandidatesPerTf = 8;
input bool            InpStateGateShowIds             = true;
input bool            InpStateGateShowScaleL          = true;
input bool            InpStateGateExportCsv           = true;
input bool            InpStateGateExportOverwriteLatest = true;
input bool            InpStateGateExportContractCsv   = true;
input bool            InpStateGateExportDiagnosticsCsv = true;
input bool            InpStateGateExportPanelLinesCsv  = true;
input bool            InpStateGateExportEntryBridgeCsv = true;
input bool            InpStateGateExportExtremeCandidatesCsv = true;
input bool            InpStateGateExportMtfAlignmentCsv = true;
input bool            InpStateGateExportEntryGeometryCsv = true;
input bool            InpStateGateExportEntryIdeasCsv = true;
input bool            InpStateGateExportEntryDecisionsCsv = true;
input bool            InpStateGateExportPaperLedgerCsv = true;
input bool            InpStateGateExportPaperLifecycleCsv = true;
input bool            InpStateGateExportPaperResultsCsv = true;
input bool            InpStateGateExportPaperPortfolioCsv = true;
input bool            InpStateGateExportPaperRegimeCsv = true;
input bool            InpStateGateExportPaperFiltersCsv = true;
input bool            InpStateGateExportPaperPolicyCsv = true;
input bool            InpStateGateExportPersistentPaperTradesCsv = true;
input string          InpStateGateExportFolder        = "FlagCountingPhoenix";
input bool            InpStateGatePrintAudit          = true;

// ------------------------------ Rendering -----------------------------------
input string InpObjectPrefix = "DAL_FCP_";
input string InpRenderMemo = "";
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
input bool   InpDrawOnlyFlagSeedHooks = false;
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

FP_OfflineLicenseConfig g_fp_license_cfg;
FP_OfflineLicenseReport g_fp_license_report;
bool g_fp_license_ok = false;
datetime g_fp_license_next_check = 0;
FP_StateGateRuntime g_fp_state_gate_runtime;

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
   cfg.ownership_allow_visual_soft_reset = InpOwnershipAllowVisualSoftReset;
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
   cfg.identity_generation_pass = "phoenix_level18";
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
                              "_release" + FP_ReleaseProfileName(InpReleaseProfile) +
                              "_interface_pre" + FP_BoolName(InpInterfacePreflightEnabled) +
                              "_interface_post" + FP_BoolName(InpInterfacePostflightEnabled) +
                              "_acceptance" + FP_BoolName(InpAcceptanceEnabled) +
                              "_acceptance_mode" + FP_AcceptanceModeName(InpAcceptanceMode) +
                              "_ambiguity" + FP_BoolName(InpAmbiguityEnabled) +
                              "_ambiguity_mode" + FP_AmbiguityModeName(InpAmbiguityMode) +
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


void FP_LoadOfflineLicenseConfig(FP_OfflineLicenseConfig &cfg)
{
   FP_DefaultOfflineLicenseConfig(cfg);
   cfg.enabled = true;
   cfg.fail_closed = true;
   cfg.bind_account = true;
   cfg.bind_server = true;
   cfg.require_password = true;
   cfg.require_hidden_gates = true;
   cfg.require_expiry = true;
   cfg.product_id = FP_LICENSE_PRODUCT_ID;
   cfg.build_id = "phoenix_18_20";
   cfg.token = InpPhaseModelProfile;
   cfg.passphrase = InpRenderMemo;
   cfg.gate_a = InpNodeModelSeed;
   cfg.gate_b = InpBoundaryModelSeed;
   cfg.gate_c = InpValidationModelSeed;
   cfg.gate_d = InpReleaseModelSeed;
   cfg.check_interval_seconds = InpSessionCacheDepth * 60;
   if(cfg.check_interval_seconds < 60)
      cfg.check_interval_seconds = 60;
   cfg.print_sanity = true;
   cfg.print_samples = false;
}

bool FP_EnsureOfflineLicense(const bool force_check=false)
{
   datetime now = TimeCurrent();
   if(now <= 0)
      now = TimeTradeServer();
   if(!force_check && g_fp_license_ok && g_fp_license_next_check > 0 && now > 0 && now < g_fp_license_next_check)
      return true;

   FP_LoadOfflineLicenseConfig(g_fp_license_cfg);
   g_fp_license_ok = FP_CheckOfflineLicenseWithReport(g_fp_license_cfg, g_fp_license_report);
   if(g_fp_license_cfg.print_sanity || !g_fp_license_ok)
      FP_PrintOfflineLicenseReport("FP_LICENSE", g_fp_license_report);
   if(g_fp_license_cfg.print_samples && g_fp_license_ok)
      FP_PrintOfflineLicenseSamples("FP_LICENSE", g_fp_license_report);

   datetime checked = g_fp_license_report.checked_at;
   if(checked <= 0)
      checked = now;
   if(checked > 0)
   {
      int recheck_sec = g_fp_license_cfg.check_interval_seconds;
      if(recheck_sec < 60)
         recheck_sec = 60;
      g_fp_license_next_check = checked + recheck_sec;
   }
   else
   {
      g_fp_license_next_check = 0;
   }

   if(!g_fp_license_ok)
      Comment("FlagCounting Phoenix runtime inactive. Contact issuer.");
   else
      Comment("");
   return g_fp_license_ok;
}

void FP_LoadReleaseConfig(FP_ReleaseConfig &cfg)
{
   FP_DefaultReleaseConfig(cfg);
   cfg.profile = InpReleaseProfile;
   cfg.folder = InpReleaseFolder;
   cfg.run_tag = InpReleaseRunTag;
   cfg.write_manifest = InpReleaseWriteManifest;
   cfg.overwrite_latest = InpReleaseOverwriteLatest;
   cfg.strict_gate = InpReleaseStrictGate;
   cfg.require_validation_ok = InpReleaseRequireValidationOk;
   cfg.require_export_ok = InpReleaseRequireExportOk;
   cfg.require_render_ok = InpReleaseRequireRenderOk;
   cfg.require_no_render_errors = InpReleaseRequireNoRenderErrors;
   cfg.require_no_export_errors = InpReleaseRequireNoExportErrors;
   cfg.require_no_canonical_failures = InpReleaseRequireNoCanonicalFailures;
   cfg.clean_objects_for_profile = InpReleaseCleanObjectsForProfile;
   cfg.print_sanity = InpPrintReleaseSanity;
   cfg.print_samples = InpPrintReleaseSamples;
   cfg.sample_limit = InpReleaseSampleLimit;
}

void FP_LoadInterfaceConfig(FP_InterfaceConfig &cfg)
{
   FP_DefaultInterfaceConfig(cfg);
   cfg.preflight_enabled = InpInterfacePreflightEnabled;
   cfg.postflight_enabled = InpInterfacePostflightEnabled;
   cfg.strict = InpInterfaceStrict;
   cfg.write_csv = InpInterfaceWriteCsv;
   cfg.overwrite_latest = InpInterfaceOverwriteLatest;
   cfg.folder = InpInterfaceFolder;
   cfg.run_tag = InpInterfaceRunTag;
   cfg.require_preflight_ok = InpInterfaceRequirePreflightOk;
   cfg.require_postflight_ok = InpInterfaceRequirePostflightOk;
   cfg.require_result_partition = InpInterfaceRequireResultPartition;
   cfg.require_public_ids = InpInterfaceRequirePublicIds;
   cfg.require_parent_contract = InpInterfaceRequireParentContract;
   cfg.require_counter_nonnegative = InpInterfaceRequireCounterNonnegative;
   cfg.print_sanity = InpPrintInterfaceSanity;
   cfg.print_samples = InpPrintInterfaceSamples;
   cfg.sample_limit = InpInterfaceSampleLimit;
}

void FP_LoadAcceptanceConfig(FP_AcceptanceConfig &cfg)
{
   FP_DefaultAcceptanceConfig(cfg);
   cfg.enabled = InpAcceptanceEnabled;
   cfg.mode = InpAcceptanceMode;
   cfg.strict = InpAcceptanceStrict;
   cfg.write_csv = InpAcceptanceWriteCsv;
   cfg.overwrite_latest = InpAcceptanceOverwriteLatest;
   cfg.folder = InpAcceptanceFolder;
   cfg.run_tag = InpAcceptanceRunTag;
   cfg.case_id = InpAcceptanceCaseId;
   cfg.matrix_version = FP_ACCEPTANCE_CONTRACT_VERSION;
   cfg.require_level01_ok = InpAcceptanceRequireLevel01Ok;
   cfg.require_no_canonical_failures = InpAcceptanceRequireNoCanonicalFailures;
   cfg.require_export_ok_when_enabled = InpAcceptanceRequireExportOkWhenEnabled;
   cfg.require_render_ok_when_enabled = InpAcceptanceRequireRenderOkWhenEnabled;
   cfg.require_validation_ok_when_enabled = InpAcceptanceRequireValidationOkWhenEnabled;
   cfg.require_release_gate_when_strict = InpAcceptanceRequireReleaseGateWhenStrict;
   cfg.require_interface_pre_ok_when_enabled = InpAcceptanceRequireInterfacePreOkWhenEnabled;
   cfg.require_interface_post_ok_when_enabled = InpAcceptanceRequireInterfacePostOkWhenEnabled;
   cfg.require_visible_partition = InpAcceptanceRequireVisiblePartition;
   cfg.require_locked_f3_if_expected = InpAcceptanceRequireLockedF3IfExpected;
   cfg.expected_min_visible_events = InpAcceptanceExpectedMinVisibleEvents;
   cfg.expected_min_f1 = InpAcceptanceExpectedMinF1;
   cfg.expected_min_f2 = InpAcceptanceExpectedMinF2;
   cfg.expected_min_f3 = InpAcceptanceExpectedMinF3;
   cfg.expected_min_locked_f3 = InpAcceptanceExpectedMinLockedF3;
   cfg.print_sanity = InpPrintAcceptanceSanity;
   cfg.print_samples = InpPrintAcceptanceSamples;
   cfg.sample_limit = InpAcceptanceSampleLimit;
}

void FP_LoadAmbiguityConfig(FP_AmbiguityConfig &cfg)
{
   FP_DefaultAmbiguityConfig(cfg);
   cfg.enabled = InpAmbiguityEnabled;
   cfg.mode = InpAmbiguityMode;
   cfg.strict = InpAmbiguityStrict;
   cfg.write_csv = InpAmbiguityWriteCsv;
   cfg.overwrite_latest = InpAmbiguityOverwriteLatest;
   cfg.folder = InpAmbiguityFolder;
   cfg.run_tag = InpAmbiguityRunTag;
   cfg.case_id = InpAmbiguityCaseId;
   cfg.require_decision_lock = InpAmbiguityRequireDecisionLock;
   cfg.require_no_release_blockers = InpAmbiguityRequireNoReleaseBlockers;
   cfg.require_canonical_source = InpAmbiguityRequireCanonicalSource;
   cfg.require_closed_bar_default = InpAmbiguityRequireClosedBarDefault;
   cfg.require_confirmed_f_bodies = InpAmbiguityRequireConfirmedFBodies;
   cfg.require_strict_renderer_visibility = InpAmbiguityRequireStrictRendererVisibility;
   cfg.require_canonical_object_names = InpAmbiguityRequireCanonicalObjectNames;
   cfg.require_seeded_hook_main_chart = InpAmbiguityRequireSeededHookMainChart;
   cfg.require_export_before_renderer = InpAmbiguityRequireExportBeforeRenderer;
   cfg.require_validation_before_release = InpAmbiguityRequireValidationBeforeRelease;
   cfg.require_acceptance_before_summary = InpAmbiguityRequireAcceptanceBeforeSummary;
   cfg.require_interface_pass_alignment = InpAmbiguityRequireInterfacePassAlignment;
   cfg.allow_fail_open_diagnostic = InpAmbiguityAllowFailOpenDiagnostic;
   cfg.allow_candidate_display_diagnostic = InpAmbiguityAllowCandidateDisplayDiagnostic;
   cfg.allow_or_rejected_f3_diagnostic = InpAmbiguityAllowORRejectedF3Diagnostic;
   cfg.allow_debug_unseeded_hooks = InpAmbiguityAllowDebugUnseededHooks;
   cfg.print_sanity = InpPrintAmbiguitySanity;
   cfg.print_samples = InpPrintAmbiguitySamples;
   cfg.sample_limit = InpAmbiguitySampleLimit;
}

void FP_LoadStaticQaConfig(FP_StaticQaConfig &cfg)
{
   FP_DefaultStaticQaConfig(cfg);
   cfg.enabled = InpStaticQaEnabled;
   cfg.mode = InpStaticQaMode;
   cfg.strict = InpStaticQaStrict;
   cfg.write_csv = InpStaticQaWriteCsv;
   cfg.overwrite_latest = InpStaticQaOverwriteLatest;
   cfg.folder = InpStaticQaFolder;
   cfg.run_tag = InpStaticQaRunTag;
   cfg.case_id = InpStaticQaCaseId;
   cfg.require_contract_version = InpStaticQaRequireContractVersion;
   cfg.require_identity_pass = InpStaticQaRequireIdentityPass;
   cfg.require_interface_contract_alignment = InpStaticQaRequireInterfaceContractAlignment;
   cfg.require_runtime_partitions = InpStaticQaRequireRuntimePartitions;
   cfg.require_nonnegative_counters = InpStaticQaRequireNonnegativeCounters;
   cfg.require_report_alignment = InpStaticQaRequireReportAlignment;
   cfg.require_io_alignment = InpStaticQaRequireIoAlignment;
   cfg.require_release_safe_defaults = InpStaticQaRequireReleaseSafeDefaults;
   cfg.require_static_tool_present = InpStaticQaRequireStaticToolPresent;
   cfg.require_zero_runtime_blockers = InpStaticQaRequireZeroRuntimeBlockers;
   cfg.allow_observe_warnings = InpStaticQaAllowObserveWarnings;
   cfg.allow_disabled_export = InpStaticQaAllowDisabledExport;
   cfg.allow_disabled_validation = InpStaticQaAllowDisabledValidation;
   cfg.allow_disabled_render = InpStaticQaAllowDisabledRender;
   cfg.print_sanity = InpPrintStaticQaSanity;
   cfg.print_samples = InpPrintStaticQaSamples;
   cfg.sample_limit = InpStaticQaSampleLimit;
}


void FP_LoadStateGateConfig(FP_StateGateConfig &cfg)
{
   FP_DefaultStateGateConfig(cfg);
   cfg.enabled = InpStateGateEnabled;
   cfg.tf1 = InpStateGateTf1;
   cfg.tf2 = InpStateGateTf2;
   cfg.tf3 = InpStateGateTf3;
   cfg.panel_enabled = InpStateGatePanelEnabled;
   cfg.panel_start_minimized = InpStateGatePanelStartMinimized;
   cfg.panel_corner = InpStateGatePanelCorner;
   cfg.panel_x = InpStateGatePanelX;
   cfg.panel_y = InpStateGatePanelY;
   cfg.panel_width = InpStateGatePanelWidth;
   cfg.panel_font_size = InpStateGatePanelFontSize;
   cfg.panel_rally_preview_rows_per_tf = InpStateGatePanelRallyPreviewRows;
   cfg.panel_hook_preview_rows_per_tf = InpStateGatePanelHookPreviewRows;
   cfg.panel_force_right_upper = InpStateGatePanelForceRightUpper;
   cfg.panel_force_left_upper = InpStateGatePanelForceLeftUpper;
   cfg.panel_compact_mode = InpStateGatePanelCompactMode;
   cfg.panel_show_closed_bar = InpStateGatePanelShowClosedBar;
   cfg.panel_show_row_counts = InpStateGatePanelShowRowCounts;
   cfg.panel_show_contract_key = InpStateGatePanelShowContractKey;
   cfg.panel_show_diagnostics = InpStateGatePanelShowDiagnostics;
   cfg.max_rally_rows_per_tf = InpStateGateMaxRallyRowsPerTf;
   cfg.max_hook_rows_per_tf = InpStateGateMaxHookRowsPerTf;
   cfg.max_extreme_candidates_per_tf = InpStateGateMaxExtremeCandidatesPerTf;
   cfg.show_ids = InpStateGateShowIds;
   cfg.show_scale_l = InpStateGateShowScaleL;
   cfg.export_csv = InpStateGateExportCsv;
   cfg.export_overwrite_latest = InpStateGateExportOverwriteLatest;
   cfg.export_contract_csv = InpStateGateExportContractCsv;
   cfg.export_diagnostics_csv = InpStateGateExportDiagnosticsCsv;
   cfg.export_panel_lines_csv = InpStateGateExportPanelLinesCsv;
   cfg.export_entry_bridge_csv = InpStateGateExportEntryBridgeCsv;
   cfg.export_extreme_candidates_csv = InpStateGateExportExtremeCandidatesCsv;
   cfg.export_mtf_alignment_csv = InpStateGateExportMtfAlignmentCsv;
   cfg.export_entry_geometry_csv = InpStateGateExportEntryGeometryCsv;
   cfg.export_entry_ideas_csv = InpStateGateExportEntryIdeasCsv;
   cfg.export_entry_decisions_csv = InpStateGateExportEntryDecisionsCsv;
   cfg.export_paper_ledger_csv = InpStateGateExportPaperLedgerCsv;
   cfg.export_paper_lifecycle_csv = InpStateGateExportPaperLifecycleCsv;
   cfg.export_paper_results_csv = InpStateGateExportPaperResultsCsv;
   cfg.export_paper_portfolio_csv = InpStateGateExportPaperPortfolioCsv;
   cfg.export_paper_regime_csv = InpStateGateExportPaperRegimeCsv;
   cfg.export_paper_filters_csv = InpStateGateExportPaperFiltersCsv;
   cfg.export_paper_policy_csv = InpStateGateExportPaperPolicyCsv;
   cfg.export_persistent_paper_trades_csv = InpStateGateExportPersistentPaperTradesCsv;
   cfg.export_folder = InpStateGateExportFolder;
   cfg.print_audit = InpStateGatePrintAudit;
   cfg.object_prefix = FP_STATE_GATE_DEFAULT_PREFIX;
}

void FP_Run()
{
   if(!FP_EnsureOfflineLicense(false))
      return;

   MqlRates rates[];

   FP_ReleaseConfig release_cfg;
   FP_LoadReleaseConfig(release_cfg);
   FP_ReleaseReport release_report;

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

   FP_Config cfg;
   FP_LoadConfig(cfg);

   FP_ExportConfig export_cfg;
   FP_LoadExportConfig(export_cfg);

   FP_RenderConfig render_cfg;
   FP_LoadRenderConfig(render_cfg);

   FP_ValidationConfig validation_cfg;
   FP_LoadValidationConfig(validation_cfg);

   FP_InterfaceConfig interface_cfg;
   FP_LoadInterfaceConfig(interface_cfg);

   FP_AcceptanceConfig acceptance_cfg;
   FP_LoadAcceptanceConfig(acceptance_cfg);

   FP_AmbiguityConfig ambiguity_cfg;
   FP_LoadAmbiguityConfig(ambiguity_cfg);

   FP_StaticQaConfig staticqa_cfg;
   FP_LoadStaticQaConfig(staticqa_cfg);

   FP_StateGateConfig state_gate_cfg;
   FP_LoadStateGateConfig(state_gate_cfg);

   FP_ReleaseApplyProfile(timebase_cfg, cfg, export_cfg, render_cfg, validation_cfg, release_cfg, release_report);
   if(release_cfg.print_sanity && release_report.overrides_applied > 0)
      FP_PrintReleaseReport("FP_LEVEL14_PRE", release_report);
   if(release_cfg.print_samples && release_report.overrides_applied > 0)
      FP_PrintReleaseSamples("FP_LEVEL14_PRE", release_report);

   FP_InterfaceReport interface_pre_report;
   FP_ResetInterfaceReport(interface_pre_report);
   string interface_pre_rows[];
   if(interface_cfg.preflight_enabled)
   {
      FP_RunInterfacePreflightWithReport(_Symbol, _Period, timebase_cfg, cfg, export_cfg, render_cfg, validation_cfg, release_cfg, interface_cfg, interface_pre_report, interface_pre_rows);
      if(interface_cfg.print_sanity)
         FP_PrintInterfaceReport("FP_LEVEL15_PRE", interface_pre_report);
      if(interface_cfg.print_samples)
         FP_PrintInterfaceSamples("FP_LEVEL15_PRE", interface_pre_report, interface_pre_rows, interface_cfg.sample_limit);
   }

   FP_TimebaseReport timebase_report;
   int copied = FP_LoadCanonicalRates(timebase_cfg, rates, timebase_report);

   if(timebase_cfg.print_sanity || !timebase_report.ok)
      FP_PrintTimebaseReport("FP_LEVEL01", timebase_report);
   if(timebase_cfg.print_samples)
      FP_PrintTimebaseSamples("FP_LEVEL01", rates, copied);

   if(!timebase_report.ok && timebase_cfg.strict_contract)
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

   FP_FlagEvent events[];
   FP_HookBranch hooks[];
   FP_DetectResult result;
   FP_DetectAllScales(rates, copied, scales, scale_count, cfg, events, hooks, result);
   if(interface_pre_report.attempted)
      FP_InterfaceApplyReportToResult(interface_pre_report, result);

   FP_ExportReport export_report;
   FP_ResetExportReport(export_report);
   if(export_cfg.enabled)
   {
      FP_ExportAuditWithReport(_Symbol, _Period, copied, scale_count, cfg, export_cfg, events, hooks, result, export_report);
      FP_ExportApplyReportToResult(export_report, result);
      if(export_cfg.print_sanity)
         FP_PrintExportReport("FP_LEVEL11_5", export_report);
      if(export_cfg.print_samples)
         FP_PrintExportSamples("FP_LEVEL11_5", export_report, events, hooks, export_cfg.sample_limit);
   }

   FP_RenderReport render_report;
   FP_ResetRenderReport(render_report);
   int drawn = FP_DrawAllWithReport(events, hooks, rates, copied, render_cfg, render_report);
   FP_RenderApplyReportToResult(render_report, result);
   if(render_cfg.print_sanity)
      FP_PrintRenderReport("FP_LEVEL12", render_report);
   if(render_cfg.print_samples)
      FP_PrintRenderSamples("FP_LEVEL12", render_report);

   FP_ValidationReport validation_report;
   FP_ResetValidationReport(validation_report);
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

   FP_FinalizeReleaseWithManifest(release_cfg, result, export_report, render_report, validation_report, release_report);
   FP_ReleaseApplyReportToResult(release_report, result);
   if(release_cfg.print_sanity)
      FP_PrintReleaseReport("FP_LEVEL14", release_report);
   if(release_cfg.print_samples)
      FP_PrintReleaseSamples("FP_LEVEL14", release_report);

   FP_InterfaceReport interface_post_report;
   FP_ResetInterfaceReport(interface_post_report);
   string interface_post_rows[];
   if(interface_cfg.postflight_enabled)
   {
      FP_RunInterfacePostflightWithReport(_Symbol, _Period, interface_cfg, events, hooks, result, interface_post_report, interface_post_rows);
      FP_InterfaceApplyReportToResult(interface_post_report, result);
      if(interface_cfg.print_sanity)
         FP_PrintInterfaceReport("FP_LEVEL15", interface_post_report);
      if(interface_cfg.print_samples)
         FP_PrintInterfaceSamples("FP_LEVEL15", interface_post_report, interface_post_rows, interface_cfg.sample_limit);
   }

   FP_AcceptanceReport acceptance_report;
   FP_ResetAcceptanceReport(acceptance_report);
   string acceptance_rows[];
   if(acceptance_cfg.enabled)
   {
      FP_RunAcceptanceWithReport(_Symbol, _Period, acceptance_cfg, timebase_report, result, export_report, render_report, validation_report, release_report, interface_pre_report, interface_post_report, acceptance_report, acceptance_rows);
      FP_AcceptanceApplyReportToResult(acceptance_report, result);
      if(acceptance_cfg.print_sanity)
         FP_PrintAcceptanceReport("FP_LEVEL16", acceptance_report);
      if(acceptance_cfg.print_samples)
         FP_PrintAcceptanceSamples("FP_LEVEL16", acceptance_report, acceptance_rows, acceptance_cfg.sample_limit);
   }

   FP_AmbiguityReport ambiguity_report;
   FP_ResetAmbiguityReport(ambiguity_report);
   string ambiguity_rows[];
   if(ambiguity_cfg.enabled)
   {
      FP_RunAmbiguityWithReport(_Symbol, _Period, ambiguity_cfg, timebase_cfg, cfg, export_cfg, render_cfg, validation_cfg, release_cfg, interface_cfg, acceptance_cfg, result, export_report, render_report, validation_report, release_report, interface_pre_report, interface_post_report, acceptance_report, ambiguity_report, ambiguity_rows);
      FP_AmbiguityApplyReportToResult(ambiguity_report, result);
      if(ambiguity_cfg.print_sanity)
         FP_PrintAmbiguityReport("FP_LEVEL17", ambiguity_report);
      if(ambiguity_cfg.print_samples)
         FP_PrintAmbiguitySamples("FP_LEVEL17", ambiguity_report, ambiguity_rows, ambiguity_cfg.sample_limit);
   }

   FP_StaticQaReport staticqa_report;
   FP_ResetStaticQaReport(staticqa_report);
   string staticqa_rows[];
   if(staticqa_cfg.enabled)
   {
      FP_RunStaticQaWithReport(_Symbol, _Period, staticqa_cfg, timebase_cfg, timebase_report, cfg, export_cfg, render_cfg, validation_cfg, release_cfg, interface_cfg, acceptance_cfg, ambiguity_cfg, result, export_report, render_report, validation_report, release_report, interface_post_report, acceptance_report, ambiguity_report, staticqa_report, staticqa_rows);
      FP_StaticQaApplyReportToResult(staticqa_report, result);
      if(staticqa_cfg.print_sanity)
         FP_PrintStaticQaReport("FP_LEVEL18", staticqa_report);
      if(staticqa_cfg.print_samples)
         FP_PrintStaticQaSamples("FP_LEVEL18", staticqa_report, staticqa_rows, staticqa_cfg.sample_limit);
   }

   FP_StateGateReport state_gate_report;
   FP_RunStateGatePhase24(_Symbol, _Period, state_gate_cfg, timebase_cfg, cfg, scales, scale_count, g_fp_state_gate_runtime, state_gate_report);
   if(state_gate_cfg.print_audit)
      FP_PrintStateGateReport("FP_LEVEL19_STATE_GATE", state_gate_report);
   if(state_gate_cfg.print_audit)
      FP_PrintStateGateSnapshotSamples("FP_LEVEL19_STATE_GATE_SAMPLE", g_fp_state_gate_runtime.snapshot, FP_STATE_GATE_TF_SLOTS);

   FP_PrintSummary(_Symbol, _Period, copied, scale_count, result, drawn);
   if(InpVerboseAuditLogs)
   {
      for(int i=0; i<ArraySize(events); i++) FP_PrintEventAudit(events[i]);
      for(int h=0; h<ArraySize(hooks); h++) FP_PrintHookAudit(hooks[h]);
   }
}

int OnInit()
{
   if(!FP_EnsureOfflineLicense(true))
      return INIT_FAILED;
   EventSetTimer(60);

   FP_ResetStateGateRuntime(g_fp_state_gate_runtime);
   FP_StateGateConfig init_state_gate_cfg;
   FP_LoadStateGateConfig(init_state_gate_cfg);
   FP_StateGatePanelCleanup(init_state_gate_cfg);

   FP_ReleaseConfig init_release_cfg;
   FP_LoadReleaseConfig(init_release_cfg);
   if(InpCleanObjectsOnInit || FP_ReleaseProfileWantsCleanup(init_release_cfg))
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
   g_fp_last_bar_time = 0;
   FP_Run();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   FP_StateGateConfig deinit_state_gate_cfg;
   FP_LoadStateGateConfig(deinit_state_gate_cfg);
   FP_StateGatePanelCleanup(deinit_state_gate_cfg);
   if(InpCleanObjectsOnDeinit)
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
}


void OnChartEvent(const int id,
                  const long &lparam,
                  const double &dparam,
                  const string &sparam)
{
   FP_StateGateConfig event_state_gate_cfg;
   FP_LoadStateGateConfig(event_state_gate_cfg);
   FP_StateGatePanelHandleChartEvent(event_state_gate_cfg, g_fp_state_gate_runtime, id, sparam);
}

void OnTick()
{
   if(!FP_EnsureOfflineLicense(false))
      return;
   if(FP_ShouldRedraw())
      FP_Run();
}

void FP_RunStateGateTimerOnly()
{
   FP_ReleaseConfig release_cfg;
   FP_LoadReleaseConfig(release_cfg);
   FP_ReleaseReport release_report;

   FP_TimebaseConfig timebase_cfg;
   FP_DefaultTimebaseConfig(timebase_cfg);
   timebase_cfg.symbol = _Symbol;
   timebase_cfg.period = _Period;
   timebase_cfg.requested_bars = InpBarsToScan;
   timebase_cfg.min_closed_bars = InpMinClosedBars;
   timebase_cfg.exclude_live_bar = InpUseClosedBarsOnly;
   timebase_cfg.require_ascending_time = true;
   timebase_cfg.strict_contract = InpStrictTimebase;
   timebase_cfg.print_sanity = false;
   timebase_cfg.print_samples = false;

   FP_Config cfg;
   FP_LoadConfig(cfg);

   FP_ExportConfig export_cfg;
   FP_LoadExportConfig(export_cfg);

   FP_RenderConfig render_cfg;
   FP_LoadRenderConfig(render_cfg);

   FP_ValidationConfig validation_cfg;
   FP_LoadValidationConfig(validation_cfg);

   FP_ReleaseApplyProfile(timebase_cfg, cfg, export_cfg, render_cfg, validation_cfg, release_cfg, release_report);

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

   FP_StateGateConfig timer_state_gate_cfg;
   FP_LoadStateGateConfig(timer_state_gate_cfg);
   FP_StateGateReport timer_state_gate_report;

   if(scale_count <= 0)
      FP_RunStateGatePhase2(_Symbol, _Period, timer_state_gate_cfg, g_fp_state_gate_runtime, timer_state_gate_report);
   else
      FP_RunStateGatePhase24(_Symbol, _Period, timer_state_gate_cfg, timebase_cfg, cfg, scales, scale_count, g_fp_state_gate_runtime, timer_state_gate_report);

   if(timer_state_gate_cfg.print_audit && (timer_state_gate_report.dirty_timeframes > 0 || timer_state_gate_report.file_errors > 0 || timer_state_gate_report.object_errors > 0))
      FP_PrintStateGateReport("FP_LEVEL19_STATE_GATE_TIMER", timer_state_gate_report);
}

void OnTimer()
{
   if(!FP_EnsureOfflineLicense(true))
      return;

   FP_RunStateGateTimerOnly();
}
