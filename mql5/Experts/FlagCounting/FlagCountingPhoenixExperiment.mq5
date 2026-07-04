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
#include "../../Include/FlagCountingPhoenix/FP_EntryBridgeEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_PaperIntentEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_PaperLifecycleEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_PaperPerformanceEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_SafetyGateEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_BrokerDryRunEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_BrokerValidatorEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_BrokerRequestLedgerEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_BrokerRequestAuditEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_PaperBrokerAdapterEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_PaperBrokerLifecycleEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_NoSendContextEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_FinalDecisionStateEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_FinalCsvNormalizationEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_RuntimeHealthSummaryEngine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase01Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase03Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase04Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase05Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase06Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase07Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase08Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase09Engine.mqh"
#include "../../Include/FlagCountingPhoenix/FP_HookPhase10Engine.mqh"

// ------------------------------ NDS display mode ---------------------------
// FIRST visible input: choose exactly what the central expert should show.
// RALLY_ONLY preserves legacy F/Rally rendering and skips Hook phases by default.
// HOOK_ONLY suppresses Rally/F drawing and shows only the modular Hook layers.
// RALLY_AND_HOOK shows both families together for combined inspection.
input FP_NDSHookDisplayFamily InpNDSHookDisplayFamily = FP_NDS_HOOK_DISPLAY_HOOK_ONLY;

// ------------------------------ Data / redraw -------------------------------
// Level 01 canonical candle stream. InpBarsToScan means requested CLOSED bars
// when InpUseClosedBarsOnly=true. The loader copies one extra raw bar and drops
// the current forming live candle before any structural engine runs.
input int  InpBarsToScan = 5000;
input bool InpUseClosedBarsOnly = true;
input bool InpStrictTimebase = true;
input int  InpMinClosedBars = 200;
input int  InpSessionCacheDepth = 15;
input bool InpPrintTimebaseSanity = false;
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
input bool InpPrintNodeSanity = false;
input bool InpPrintNodeSamples = false;
input int  InpNodeSampleLimit = 6;
input bool InpPrintIdentitySanity = false;
input bool InpPrintIdentitySamples = false;
input int  InpIdentitySampleLimit = 6;
input bool InpPrintHookSanity = false;
input bool InpPrintHookSamples = false;
input int  InpHookSampleLimit = 6;
input bool InpPrintBodySanity = false;
input bool InpPrintBodySamples = false;
input int  InpBodySampleLimit = 6;
input bool InpPrintInternalSanity = false;
input bool InpPrintInternalSamples = false;
input int  InpInternalSampleLimit = 6;
input bool InpPrintF1Sanity = false;
input bool InpPrintF1Samples = false;
input int  InpF1SampleLimit = 6;
input bool InpPrintF2Sanity = false;
input bool InpPrintF2Samples = false;
input int  InpF2SampleLimit = 6;
input bool InpPrintF3Sanity = false;
input bool InpPrintF3Samples = false;
input int  InpF3SampleLimit = 6;
input bool InpPrintOwnershipSanity = false;
input bool InpPrintOwnershipSamples = false;
input int  InpOwnershipSampleLimit = 8;
input bool InpPrintCanonicalSanity = false;
input bool InpPrintCanonicalSamples = false;
input int  InpCanonicalSampleLimit = 8;
input bool InpPrintExportSanity = false;
input bool InpPrintExportSamples = false;
input int  InpExportSampleLimit = 5;
input bool InpPrintRenderSanity = false;
input bool InpPrintRenderSamples = false;
input int  InpRenderSampleLimit = 8;
input bool InpPrintValidationSanity = false;
input bool InpPrintValidationSamples = false;
input int  InpValidationSampleLimit = 8;
input bool InpPrintReleaseSanity = false;
input bool InpPrintReleaseSamples = false;
input int  InpReleaseSampleLimit = 8;
input bool InpPrintInterfaceSanity = false;
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
input bool   InpPrintFinalSummary = false;
input bool   InpPrintFailureSummaries = false;
input bool   InpPrintLicenseSanity = false;
input bool   InpPrintLicenseSamples = false;
input bool   InpPrintLicenseFailures = false;

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
input bool   InpPrintAcceptanceSanity = false;
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
input bool   InpPrintAmbiguitySanity = false;
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
input bool   InpPrintStaticQaSanity = false;
input bool   InpPrintStaticQaSamples = false;
input int    InpStaticQaSampleLimit = 8;

// ------------------------------ Rendering -----------------------------------
input string InpObjectPrefix = "DAL_FCP_";
input string InpRenderMemo = "";
input bool   InpCleanObjectsOnInit = true;
input bool   InpCleanObjectsOnDeinit = true;
input bool   InpCleanObjectsOnChartChange = true;
input bool   InpCleanObjectsOnRemove = true;
input bool   InpCleanObjectsOnRecompile = true;
input bool   InpCleanObjectsOnParameterChange = true;
input bool   InpCleanObjectsOnTemplateApply = true;
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

// ------------------------------ NDS Hook Phase 01 --------------------------
// Modular Hook/CycleHook node source adapter. It never sends orders and never
// mutates Rally/F-counting logic. Display-family is the first visible input of
// the expert and is shared by all Hook phases.
input bool   InpHookPhase01Enabled = true;
input bool   InpHookPhase01ShowPeaks = true;
input bool   InpHookPhase01ShowValleys = true;
input bool   InpHookPhase01DrawNodes = true;
input bool   InpHookPhase01DrawLabels = true;
input bool   InpHookPhase01ExportCsv = false;
input bool   InpHookPhase01PrintSummary = false;
input bool   InpHookPhase01PrintSamples = false;
input int    InpHookPhase01MaxBarsToScan = 0;
input int    InpHookPhase01MaxNodes = 20000;
input int    InpHookPhase01MaxNodesToDraw = 500;
input int    InpHookPhase01SampleLimit = 12;
input string InpHookPhase01Folder = "FlagCountingPhoenix";
input string InpHookPhase01ObjectPrefix = "DAL_HOOK_P01_";
input color  InpHookPhase01PeakColor = clrTomato;
input color  InpHookPhase01ValleyColor = clrDeepSkyBlue;
input color  InpHookPhase01LabelColor = clrSilver;
input int    InpHookPhase01MarkerWidth = 1;
input int    InpHookPhase01LabelFontSize = 7;

// ------------------------------ NDS Hook Phase 02 --------------------------
// Modular CycleHook / strict X-sequence builder. Phase 02 depends on the Phase
// 01 node source adapter and keeps Rally/F-counting untouched by default.
input bool   InpHookPhase02Enabled = true;
input FP_HookPhase02OriginPolicy InpHookPhase02OriginPolicy = FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X;
input bool   InpHookPhase02ShowPositive = true;
input bool   InpHookPhase02ShowNegative = true;
input bool   InpHookPhase02DrawSequences = true;
input bool   InpHookPhase02DrawOrigin = true;
input bool   InpHookPhase02DrawXNodes = true;
input bool   InpHookPhase02DrawXLines = true;
input bool   InpHookPhase02DrawDeathBoundary = true;
input bool   InpHookPhase02DrawCycleArc = true;
input bool   InpHookPhase02DrawSequenceCountLabel = true;
input bool   InpHookPhase02DrawLabels = true;
input bool   InpHookPhase02ExportCsv = false;
input bool   InpHookPhase02PrintSummary = false;
input bool   InpHookPhase02PrintSamples = false;
input int    InpHookPhase02MaxBarsToScan = 0;
input int    InpHookPhase02MaxSequences = 3000;
input int    InpHookPhase02MaxSequencesToDraw = 0;
input int    InpHookPhase02MinXCountToDraw = 2;
input int    InpHookPhase02ArcMinXCountToDraw = 2;
input FP_HookPhase02SequenceDrawMode InpHookPhase02SequenceDrawMode = FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION;
input int    InpHookPhase02SequenceDrawScaleL = 0;
input int    InpHookPhase02SequenceDrawDirection = 0;
input int    InpHookPhase02SequenceDrawSequenceId = -1;
input FP_HookPhase02NodeLabelMode InpHookPhase02NodeLabelMode = FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ONE_HIDE_ORIGIN;
input FP_HookPhase02CycleArcEndMode InpHookPhase02CycleArcEndMode = FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME;
input bool   InpHookPhase02UseSequencePaletteColors = false;
input bool   InpHookPhase02ColorOriginWithSequence = false;
input bool   InpHookPhase02ColorNodeLabelsWithSequence = false;
input bool   InpHookPhase02ColorNodeNumbersByIndex = true;
input bool   InpHookPhase02MinimalNumbersOnly = false;
input bool   InpHookPhase02UseMinimalNodeMarkers = false;
input bool   InpHookPhase02StackNodeLabelsOnCollisions = true;
input int    InpHookPhase02MinXNodesToKeep = 1;
input int    InpHookPhase02MaxXNodesPerSequence = 4;
input int    InpHookPhase02SampleLimit = 10;
input int    InpHookPhase02CycleArcSegments = 18;
input int    InpHookPhase02CycleArcMaxHeightPoints = 500;
input int    InpHookPhase02NodeNumberOffsetPoints = 22;
input int    InpHookPhase02NodeLabelStackStepPoints = 14;
input int    InpHookPhase02MinimalNodeMarkerArrowCode = 159;
input double InpHookPhase02CycleArcHeightRatio = 0.08;
input string InpHookPhase02Folder = "FlagCountingPhoenix";
input string InpHookPhase02ObjectPrefix = "DAL_HOOK_P02_";
input color  InpHookPhase02PositiveColor = clrDeepSkyBlue;
input color  InpHookPhase02NegativeColor = clrTomato;
input color  InpHookPhase02OriginColor = clrGold;
input color  InpHookPhase02DeathColor = clrDimGray;
input color  InpHookPhase02CycleArcColor = clrSlateGray;
input color  InpHookPhase02SequenceCountLabelColor = clrGold;
input color  InpHookPhase02LabelColor = clrSilver;
input int    InpHookPhase02LineWidth = 1;
input int    InpHookPhase02MarkerWidth = 1;
input int    InpHookPhase02LabelFontSize = 7;

// ------------------------------ NDS Hook Phase 03 --------------------------
// Modular Y-axis opposite Extreme extractor. Phase 03 depends on Phase 01 node
// source and Phase 02 X-sequence builder. It keeps Rally/F-counting untouched.
input bool   InpHookPhase03Enabled = true;
input bool   InpHookPhase03ShowPositive = true;
input bool   InpHookPhase03ShowNegative = true;
input bool   InpHookPhase03DrawYExtremes = true;
input bool   InpHookPhase03DrawYLines = true;
input bool   InpHookPhase03DrawXReference = false;
input bool   InpHookPhase03DrawLabels = true;
input bool   InpHookPhase03ExportCsv = false;
input bool   InpHookPhase03PrintSummary = false;
input bool   InpHookPhase03PrintSamples = false;
input int    InpHookPhase03MaxBarsToScan = 0;
input int    InpHookPhase03MaxSequences = 3000;
input int    InpHookPhase03MaxSequencesToDraw = 120;
input int    InpHookPhase03MinXNodesToKeep = 1;
input int    InpHookPhase03MaxXNodesPerSequence = 4;
input int    InpHookPhase03SampleLimit = 10;
input string InpHookPhase03Folder = "FlagCountingPhoenix";
input string InpHookPhase03ObjectPrefix = "DAL_HOOK_P03_";
input color  InpHookPhase03PositiveYColor = clrDodgerBlue;
input color  InpHookPhase03NegativeYColor = clrOrangeRed;
input color  InpHookPhase03XReferenceColor = clrDarkGray;
input color  InpHookPhase03LabelColor = clrSilver;
input int    InpHookPhase03LineWidth = 1;
input int    InpHookPhase03MarkerWidth = 1;
input int    InpHookPhase03LabelFontSize = 7;

// ------------------------------ NDS Hook Phase 04 --------------------------
// Modular lifecycle skeleton. Adds ND candidate, origin-return/death marker,
// and X-closure skeleton on top of Phase 03 Y-axis records.
input bool   InpHookPhase04Enabled = true;
input bool   InpHookPhase04ShowPositive = true;
input bool   InpHookPhase04ShowNegative = true;
input bool   InpHookPhase04DrawND = true;
input bool   InpHookPhase04DrawDeath = true;
input bool   InpHookPhase04DrawXClosure = true;
input bool   InpHookPhase04DrawThresholds = true;
input bool   InpHookPhase04DrawLabels = true;
input bool   InpHookPhase04ExportCsv = false;
input bool   InpHookPhase04PrintSummary = false;
input bool   InpHookPhase04PrintSamples = false;
input int    InpHookPhase04MaxBarsToScan = 0;
input int    InpHookPhase04MaxSequences = 3000;
input int    InpHookPhase04MaxSequencesToDraw = 120;
input int    InpHookPhase04MinXNodesToKeep = 1;
input int    InpHookPhase04MaxXNodesPerSequence = 4;
input int    InpHookPhase04MinXNodesForClosure = 3;
input int    InpHookPhase04SampleLimit = 10;
input double InpHookPhase04NDReturnRatio = 0.50;
input double InpHookPhase04ClosureRetraceRatio = 0.50;
input string InpHookPhase04Folder = "FlagCountingPhoenix";
input string InpHookPhase04ObjectPrefix = "DAL_HOOK_P04_";
input color  InpHookPhase04NDColor = clrMediumSpringGreen;
input color  InpHookPhase04DeathColor = clrRed;
input color  InpHookPhase04ClosureColor = clrViolet;
input color  InpHookPhase04ThresholdColor = clrSlateGray;
input color  InpHookPhase04LabelColor = clrSilver;
input int    InpHookPhase04LineWidth = 1;
input int    InpHookPhase04MarkerWidth = 1;
input int    InpHookPhase04LabelFontSize = 7;

// ------------------------------ NDS Hook Phase 05 --------------------------
// Modular Hook Type A/B/C classifier. Uses Phase 03 Y-axis and Phase 04
// lifecycle records. Still visualization and diagnostics only.
input bool   InpHookPhase05Enabled = true;
input bool   InpHookPhase05ShowPositive = true;
input bool   InpHookPhase05ShowNegative = true;
input bool   InpHookPhase05DrawTypeLabel = true;
input bool   InpHookPhase05DrawTypeAnchor = true;
input bool   InpHookPhase05DrawTypeComparisonLines = true;
input bool   InpHookPhase05DrawLabels = true;
input bool   InpHookPhase05ExportCsv = false;
input bool   InpHookPhase05PrintSummary = false;
input bool   InpHookPhase05PrintSamples = false;
input bool   InpHookPhase05AllowY34AsThirdEvidence = false;
input int    InpHookPhase05MaxBarsToScan = 0;
input int    InpHookPhase05MaxSequences = 3000;
input int    InpHookPhase05MaxSequencesToDraw = 120;
input int    InpHookPhase05MinXNodesToKeep = 1;
input int    InpHookPhase05MaxXNodesPerSequence = 4;
input int    InpHookPhase05MinXNodesForType = 2;
input int    InpHookPhase05SampleLimit = 10;
input string InpHookPhase05Folder = "FlagCountingPhoenix";
input string InpHookPhase05ObjectPrefix = "DAL_HOOK_P05_";
input color  InpHookPhase05TypeAColor = clrLime;
input color  InpHookPhase05TypeBColor = clrDeepSkyBlue;
input color  InpHookPhase05TypeCColor = clrOrange;
input color  InpHookPhase05InsufficientColor = clrGray;
input color  InpHookPhase05ComparisonColor = clrSlateGray;
input color  InpHookPhase05LabelColor = clrWhite;
input int    InpHookPhase05LineWidth = 1;
input int    InpHookPhase05MarkerWidth = 1;
input int    InpHookPhase05LabelFontSize = 8;

// ------------------------------ NDS Hook Phase 06 --------------------------
// Modular X/Y closure strength and structural quality scoring. It uses Phase
// 05 Type A/B/C records plus Phase 04 lifecycle and Phase 03 Y-axis evidence.
// Still visualization and diagnostics only.
input bool   InpHookPhase06Enabled = true;
input bool   InpHookPhase06ShowPositive = true;
input bool   InpHookPhase06ShowNegative = true;
input bool   InpHookPhase06DrawQualityLabel = true;
input bool   InpHookPhase06DrawXYAnchor = true;
input bool   InpHookPhase06DrawProjectionLines = true;
input bool   InpHookPhase06DrawLabels = true;
input bool   InpHookPhase06ExportCsv = false;
input bool   InpHookPhase06PrintSummary = false;
input bool   InpHookPhase06PrintSamples = false;
input bool   InpHookPhase06IncludeDeadRecords = true;
input bool   InpHookPhase06RequireXClosedForXY = true;
input int    InpHookPhase06MaxBarsToScan = 0;
input int    InpHookPhase06MaxSequences = 3000;
input int    InpHookPhase06MaxSequencesToDraw = 120;
input int    InpHookPhase06MinXNodesToKeep = 1;
input int    InpHookPhase06MaxXNodesPerSequence = 4;
input int    InpHookPhase06MinXNodesForQuality = 3;
input int    InpHookPhase06MinYComparisonsForClosed = 2;
input int    InpHookPhase06SampleLimit = 10;
input double InpHookPhase06XWeight = 0.30;
input double InpHookPhase06YWeight = 0.30;
input double InpHookPhase06TypeWeight = 0.20;
input double InpHookPhase06LifecycleWeight = 0.20;
input double InpHookPhase06EliteThreshold = 0.80;
input double InpHookPhase06HighThreshold = 0.65;
input double InpHookPhase06MediumThreshold = 0.45;
input double InpHookPhase06LowThreshold = 0.25;
input string InpHookPhase06Folder = "FlagCountingPhoenix";
input string InpHookPhase06ObjectPrefix = "DAL_HOOK_P06_";
input color  InpHookPhase06XYClosedColor = clrLime;
input color  InpHookPhase06XOnlyColor = clrViolet;
input color  InpHookPhase06YOnlyColor = clrDeepSkyBlue;
input color  InpHookPhase06OpenColor = clrOrange;
input color  InpHookPhase06InsufficientColor = clrGray;
input color  InpHookPhase06ProjectionColor = clrSlateGray;
input color  InpHookPhase06LabelColor = clrWhite;
input int    InpHookPhase06LineWidth = 1;
input int    InpHookPhase06MarkerWidth = 1;
input int    InpHookPhase06LabelFontSize = 8;

// ------------------------------ NDS Hook Phase 07 --------------------------
// Central view-profile orchestrator for Hook phases. It controls which Hook
// layers draw together, optionally cleans stale Hook objects, and can write a
// profile audit row. It does not trade.
input bool   InpHookPhase07Enabled = true;
input FP_HookPhase07ViewProfile InpHookPhase07ViewProfile = FP_HOOK_P07_VIEW_MINIMAL_ALL_HOOKS;
input bool   InpHookPhase07RespectIndividualPhaseEnabled = true;
input bool   InpHookPhase07ForceEnableRequiredPhases = true;
input bool   InpHookPhase07ShowLabels = true;
input bool   InpHookPhase07GlobalExportCsv = false;
input bool   InpHookPhase07GlobalPrintSummary = false;
input bool   InpHookPhase07GlobalPrintSamples = false;
input bool   InpHookPhase07ExportProfileCsv = false;
input bool   InpHookPhase07PrintSummary = false;
input bool   InpHookPhase07CleanBeforeApply = true;
input bool   InpHookPhase07CleanCommonHookPrefix = true;
input string InpHookPhase07CommonHookObjectPrefix = "DAL_HOOK_";
input bool   InpHookPhase07CleanP01Objects = true;
input bool   InpHookPhase07CleanP02Objects = true;
input bool   InpHookPhase07CleanP03Objects = true;
input bool   InpHookPhase07CleanP04Objects = true;
input bool   InpHookPhase07CleanP05Objects = true;
input bool   InpHookPhase07CleanP06Objects = true;
input bool   InpHookPhase07CleanP07Objects = true;
input bool   InpHookPhase07CleanP08Objects = true;
input bool   InpHookPhase07CleanP09Objects = true;
input bool   InpHookPhase07CleanP10Objects = true;
input int    InpHookPhase07MaxNodesToDraw = 120;
input int    InpHookPhase07MaxSequencesToDraw = 6;
input int    InpHookPhase07SampleLimit = 10;
input string InpHookPhase07Folder = "FlagCountingPhoenix";
input string InpHookPhase07ObjectPrefix = "DAL_HOOK_P07_";

// NDS Hook Phase 08 - audit and CSV reconciliation
input bool   InpHookPhase08Enabled = true;
input bool   InpHookPhase08AllowRallyOnlyAudit = false;
input bool   InpHookPhase08ExportCsv = false;
input bool   InpHookPhase08ExportPhaseMatrixCsv = true;
input bool   InpHookPhase08ExportIntegrityCsv = true;
input bool   InpHookPhase08PrintSummary = false;
input bool   InpHookPhase08PrintSamples = false;
input bool   InpHookPhase08RequireRuntimeReportOk = true;
input bool   InpHookPhase08RequirePhaseChainAlignment = true;
input bool   InpHookPhase08RequireUniqueObjectPrefixes = true;
input bool   InpHookPhase08RequireNonnegativeCounts = true;
input bool   InpHookPhase08RequireAuditExportProfileAlignment = true;
input bool   InpHookPhase08RequireNoFileErrors = true;
input bool   InpHookPhase08RequireP06RecordsForQualityAudit = false;
input int    InpHookPhase08MaxWarningsAllowed = 0;
input int    InpHookPhase08SampleLimit = 20;
input string InpHookPhase08Folder = "FlagCountingPhoenix";
input string InpHookPhase08ObjectPrefix = "DAL_HOOK_P08_";

// NDS Hook Phase 09 - visual smoke-test harness
input bool   InpHookPhase09Enabled = true;
input bool   InpHookPhase09AllowRallyOnlySmoke = false;
input bool   InpHookPhase09RequirePhase08Ok = true;
input bool   InpHookPhase09RequireCurrentProfileCoverage = true;
input bool   InpHookPhase09RequireObjectCensus = true;
input bool   InpHookPhase09RequireDrawContractWhenRecordsExist = true;
input bool   InpHookPhase09RequireAuditOnlyNoHookDraw = true;
input bool   InpHookPhase09RequireNoPhaseFileErrors = true;
input bool   InpHookPhase09RequirePanelWhenEnabled = true;
input bool   InpHookPhase09DrawPanel = false;
input bool   InpHookPhase09CleanObjectsBeforeDraw = true;
input bool   InpHookPhase09ExportCsv = false;
input bool   InpHookPhase09ExportScenariosCsv = true;
input bool   InpHookPhase09ExportObjectCensusCsv = true;
input bool   InpHookPhase09ExportFindingsCsv = true;
input bool   InpHookPhase09PrintSummary = false;
input bool   InpHookPhase09PrintSamples = false;
input int    InpHookPhase09MaxWarningsAllowed = 0;
input int    InpHookPhase09SampleLimit = 20;
input string InpHookPhase09Folder = "FlagCountingPhoenix";
input string InpHookPhase09ObjectPrefix = "DAL_HOOK_P09_";
input ENUM_BASE_CORNER InpHookPhase09PanelCorner = CORNER_RIGHT_UPPER;
input int    InpHookPhase09PanelX = 16;
input int    InpHookPhase09PanelY = 86;
input int    InpHookPhase09PanelFontSize = 8;
input color  InpHookPhase09PanelOkColor = clrLime;
input color  InpHookPhase09PanelWarningColor = clrOrange;
input color  InpHookPhase09PanelBlockerColor = clrRed;
input color  InpHookPhase09PanelTextColor = clrWhite;

// NDS Hook Phase 10 - freeze Hook v1 and training contract
input bool   InpHookPhase10Enabled = true;
input FP_HookPhase10FreezeMode InpHookPhase10FreezeMode = FP_HOOK_P10_FREEZE_V1_CANDIDATE;
input bool   InpHookPhase10AllowRallyOnlyFreeze = false;
input bool   InpHookPhase10RequirePhase08Ok = true;
input bool   InpHookPhase10RequirePhase09Ok = true;
input bool   InpHookPhase10RequireHookRecords = true;
input bool   InpHookPhase10RequireXYQualityRecords = true;
input bool   InpHookPhase10RequireHighQualityRecords = false;
input bool   InpHookPhase10RequireViewProfileNotKeepInputs = false;
input bool   InpHookPhase10RequireExportContract = false;
input bool   InpHookPhase10RequireNoFileErrors = true;
input bool   InpHookPhase10ExportCsv = false;
input bool   InpHookPhase10ExportContractChecksCsv = true;
input bool   InpHookPhase10ExportTrainingSchemaCsv = true;
input bool   InpHookPhase10ExportFreezeManifestCsv = true;
input bool   InpHookPhase10PrintSummary = false;
input bool   InpHookPhase10PrintSamples = false;
input int    InpHookPhase10MinP06RecordsTotal = 1;
input int    InpHookPhase10MinXYClosedRecords = 0;
input int    InpHookPhase10MinHighOrEliteRecords = 0;
input int    InpHookPhase10MaxWarningsAllowed = 0;
input int    InpHookPhase10SampleLimit = 20;
input string InpHookPhase10Folder = "FlagCountingPhoenix";
input string InpHookPhase10ObjectPrefix = "DAL_HOOK_P10_";

// ------------------------------ Level 19 State Gate -------------------------
// Clean rebuild: read-only diagnostics. Disabled panel by default.
// It never mutates renderer objects, F/Hook/Node lines, curves, zones, or logic.
input bool            InpLevel19StateGateEnabled = true;
input bool            InpLevel19StateGateExportCsv = true;
input bool            InpLevel19StateGateExportClosedBarLedgerCsv = true;
input bool            InpLevel19StateGateExportStateDeltaCsv = true;
input bool            InpLevel19StateGateExportTransitionEventCsv = true;
input bool            InpLevel19StateGateExportTransitionSummaryCsv = true;
input bool            InpLevel19StateGateExportTransitionStabilityCsv = true;
input bool            InpLevel19StateGateExportRegimeLabelCsv = true;
input bool            InpLevel19StateGateExportCompletionCsv = true;
input bool            InpLevel19StateGatePanelEnabled = false;
input bool            InpLevel19StateGatePanelCleanOnInit = false;
input bool            InpLevel19StateGatePanelCleanOnDeinit = true;
input bool            InpLevel19StateGatePrintSummary = false;
input string          InpLevel19StateGateFolder = "FlagCountingPhoenix";
input string          InpLevel19StateGateObjectPrefix = "DAL_L19_STATE_GATE_PANEL_";
input ENUM_BASE_CORNER InpLevel19StateGatePanelCorner = CORNER_RIGHT_UPPER;
input int             InpLevel19StateGatePanelX = 16;
input int             InpLevel19StateGatePanelY = 32;
input int             InpLevel19StateGatePanelWidth = 420;
input int             InpLevel19StateGatePanelFontSize = 8;

// ------------------------------ Level 20 Entry Bridge -----------------------
// X/Y anchor join for entry research only. No order, no broker request, no execution.
input bool   InpLevel20EntryBridgeEnabled = true;
input bool   InpLevel20EntryBridgeExportCsv = true;
input bool   InpLevel20EntryBridgePrintSummary = false;
input bool   InpLevel20EntryBridgePreferLatestVisibleEvent = true;
input bool   InpLevel20EntryBridgeAllowHookFallback = true;
input double InpLevel20EntryBridgeMinRR = 1.0;
input string InpLevel20EntryBridgeFolder = "FlagCountingPhoenix";

// ------------------------------ Level 21 Paper Intent -----------------------
// Paper intent seed only. No order, no broker request, no real execution.
input bool   InpLevel21PaperIntentEnabled = true;
input bool   InpLevel21PaperIntentExportCsv = true;
input bool   InpLevel21PaperIntentPrintSummary = false;
input bool   InpLevel21PaperIntentRequireEntryBridgeReady = true;
input bool   InpLevel21PaperIntentRequireDirectionalGeometry = true;
input int    InpLevel21PaperIntentExpiryBars = 20;
input string InpLevel21PaperIntentFolder = "FlagCountingPhoenix";

// ------------------------------ Level 22 Paper Lifecycle --------------------
// Close-only paper lifecycle reconstruction. No order, no broker request, no real execution.
input bool   InpLevel22PaperLifecycleEnabled = true;
input bool   InpLevel22PaperLifecycleExportCsv = true;
input bool   InpLevel22PaperLifecyclePrintSummary = false;
input bool   InpLevel22PaperLifecycleRequireIntentAllowed = true;
input int    InpLevel22PaperLifecycleDefaultExpiryBars = 20;
input string InpLevel22PaperLifecycleFolder = "FlagCountingPhoenix";

// ------------------------------ Level 23 Paper Performance ------------------
// Performance summary from close-only paper lifecycle. No order, no broker request, no real execution.
input bool   InpLevel23PaperPerformanceEnabled = true;
input bool   InpLevel23PaperPerformanceExportCsv = true;
input bool   InpLevel23PaperPerformancePrintSummary = false;
input bool   InpLevel23PaperPerformanceCountBlockedSamples = true;
input bool   InpLevel23PaperPerformanceCountOpenSamples = true;
input bool   InpLevel23PaperPerformanceCountExpiredAsResolved = true;
input string InpLevel23PaperPerformanceFolder = "FlagCountingPhoenix";

// ------------------------------ Level 24 Safety Gate ------------------------
// Pre-broker safety gate. No order, no broker request, no real execution.
input bool   InpLevel24SafetyGateEnabled = true;
input bool   InpLevel24SafetyGateExportCsv = true;
input bool   InpLevel24SafetyGatePrintSummary = false;
input bool   InpLevel24SafetyGateManualArm = false;
input bool   InpLevel24SafetyGateRealExecutionEnabled = false;
input bool   InpLevel24SafetyGateRequireLicenseOk = true;
input bool   InpLevel24SafetyGateRequireSymbolAllowed = true;
input bool   InpLevel24SafetyGateRequireTimeframeAllowed = true;
input bool   InpLevel24SafetyGateRequireSpreadOk = true;
input bool   InpLevel24SafetyGateRequirePerformanceOk = false;
input bool   InpLevel24SafetyGateRequireManualArm = false;
input bool   InpLevel24SafetyGateRequireRealExecutionDisabled = true;
input string InpLevel24SafetyGateAllowedSymbols = "*";
input string InpLevel24SafetyGateAllowedTimeframes = "*";
input int    InpLevel24SafetyGateMaxSpreadPoints = 0;
input int    InpLevel24SafetyGateMinResolvedSamples = 30;
input double InpLevel24SafetyGateMinHitRateLike = 0.50;
input double InpLevel24SafetyGateMinAvgRLike = 0.00;
input string InpLevel24SafetyGateFolder = "FlagCountingPhoenix";

// ------------------------------ Level 25 Broker Dry Run ---------------------
// Broker-like request preview only. No OrderSend, no CTrade, no broker request, no real execution.
input bool   InpLevel25BrokerDryRunEnabled = true;
input bool   InpLevel25BrokerDryRunExportCsv = true;
input bool   InpLevel25BrokerDryRunPrintSummary = false;
input bool   InpLevel25BrokerDryRunRequireSafetyGatePassed = true;
input bool   InpLevel25BrokerDryRunRequireIntentAllowed = true;
input bool   InpLevel25BrokerDryRunOnly = true;
input long   InpLevel25BrokerDryRunMagic = 250025;
input string InpLevel25BrokerDryRunComment = "DAL_L25_DRY_RUN_ONLY";
input string InpLevel25BrokerDryRunFolder = "FlagCountingPhoenix";

// ------------------------------ Level 26 Broker Validator -------------------
// Validates broker-like dry-run preview only. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpLevel26BrokerValidatorEnabled = true;
input bool   InpLevel26BrokerValidatorExportCsv = true;
input bool   InpLevel26BrokerValidatorPrintSummary = false;
input bool   InpLevel26BrokerValidatorRequireDryRunBuilt = true;
input bool   InpLevel26BrokerValidatorRequireTickAlignment = true;
input bool   InpLevel26BrokerValidatorRequireStopDistance = true;
input bool   InpLevel26BrokerValidatorRequireNormalizedPrices = true;
input bool   InpLevel26BrokerValidatorRequireZeroVolume = true;
input bool   InpLevel26BrokerValidatorRequireDryRunOnly = true;
input string InpLevel26BrokerValidatorFolder = "FlagCountingPhoenix";

// ------------------------------ Level 27 Broker Request Ledger --------------
// Append-only broker request preview ledger. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpLevel27BrokerRequestLedgerEnabled = true;
input bool   InpLevel27BrokerRequestLedgerExportCsv = true;
input bool   InpLevel27BrokerRequestLedgerPrintSummary = false;
input bool   InpLevel27BrokerRequestLedgerAppendCsv = true;
input bool   InpLevel27BrokerRequestLedgerWriteLatestCsv = true;
input bool   InpLevel27BrokerRequestLedgerSkipDuplicateRequestKey = true;
input string InpLevel27BrokerRequestLedgerFolder = "FlagCountingPhoenix";

// ------------------------------ Level 28 Broker Request Audit ---------------
// Audits no-send broker request chain. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpLevel28BrokerRequestAuditEnabled = true;
input bool   InpLevel28BrokerRequestAuditExportCsv = true;
input bool   InpLevel28BrokerRequestAuditPrintSummary = false;
input bool   InpLevel28BrokerRequestAuditAppendCsv = true;
input bool   InpLevel28BrokerRequestAuditWriteLatestCsv = true;
input bool   InpLevel28BrokerRequestAuditSkipDuplicateAuditKey = true;
input bool   InpLevel28BrokerRequestAuditRequireDryRunOnly = true;
input bool   InpLevel28BrokerRequestAuditRequireZeroVolume = true;
input bool   InpLevel28BrokerRequestAuditRequireNoSendContract = true;
input bool   InpLevel28BrokerRequestAuditRequireRequestValidatorCoherence = true;
input bool   InpLevel28BrokerRequestAuditRequireSafetyIntentCoherence = true;
input string InpLevel28BrokerRequestAuditFolder = "FlagCountingPhoenix";

// ------------------------------ Level 29 Paper Broker Adapter ---------------
// Internal paper-broker adapter only. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpLevel29PaperBrokerAdapterEnabled = true;
input bool   InpLevel29PaperBrokerAdapterExportCsv = true;
input bool   InpLevel29PaperBrokerAdapterPrintSummary = false;
input bool   InpLevel29PaperBrokerAdapterAppendCsv = true;
input bool   InpLevel29PaperBrokerAdapterWriteLatestCsv = true;
input bool   InpLevel29PaperBrokerAdapterSkipDuplicateAdapterKey = true;
input bool   InpLevel29PaperBrokerAdapterRequireAuditPassed = true;
input bool   InpLevel29PaperBrokerAdapterRequireValidatorPassed = true;
input bool   InpLevel29PaperBrokerAdapterRequireRequestBuilt = true;
input bool   InpLevel29PaperBrokerAdapterRequireDryRunOnly = true;
input bool   InpLevel29PaperBrokerAdapterRequireZeroVolume = true;
input bool   InpLevel29PaperBrokerAdapterDryRunOnly = true;
input string InpLevel29PaperBrokerAdapterFolder = "FlagCountingPhoenix";

// ------------------------------ Level 30 Paper Broker Lifecycle -------------
// Internal paper-broker lifecycle only. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpLevel30PaperBrokerLifecycleEnabled = true;
input bool   InpLevel30PaperBrokerLifecycleExportCsv = true;
input bool   InpLevel30PaperBrokerLifecyclePrintSummary = false;
input bool   InpLevel30PaperBrokerLifecycleAppendCsv = true;
input bool   InpLevel30PaperBrokerLifecycleWriteLatestCsv = true;
input bool   InpLevel30PaperBrokerLifecycleSkipDuplicateLifecycleKey = true;
input bool   InpLevel30PaperBrokerLifecycleRequireAdapterRegistered = true;
input bool   InpLevel30PaperBrokerLifecycleRequireZeroVolume = true;
input bool   InpLevel30PaperBrokerLifecycleCloseOnly = true;
input int    InpLevel30PaperBrokerLifecycleExpiryBars = 20;
input string InpLevel30PaperBrokerLifecycleFolder = "FlagCountingPhoenix";

// ------------------------------ Consolidation 01 No-Send Context ------------
// Shared latest-row context snapshot. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpConsolidation01NoSendContextEnabled = true;
input bool   InpConsolidation01NoSendContextExportCsv = true;
input bool   InpConsolidation01NoSendContextPrintSummary = false;
input bool   InpConsolidation01NoSendContextWriteLatestCsv = true;
input string InpConsolidation01NoSendContextFolder = "FlagCountingPhoenix";

// ------------------------------ Consolidation 02 Final Decision -------------
// Human-readable final no-send decision state. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpConsolidation02FinalDecisionEnabled = true;
input bool   InpConsolidation02FinalDecisionExportCsv = true;
input bool   InpConsolidation02FinalDecisionPrintSummary = false;
input bool   InpConsolidation02FinalDecisionWriteLatestCsv = true;
input bool   InpConsolidation02FinalDecisionRequireContextReady = true;
input bool   InpConsolidation02FinalDecisionRequireLifecycleTracked = false;
input bool   InpConsolidation02FinalDecisionRequireNoSendIntegrity = true;
input string InpConsolidation02FinalDecisionFolder = "FlagCountingPhoenix";

// ------------------------------ Consolidation 04 CSV Normalization ----------
// Machine-friendly normalized final no-send decision CSV. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpConsolidation04FinalCsvNormalizationEnabled = true;
input bool   InpConsolidation04FinalCsvNormalizationExportCsv = true;
input bool   InpConsolidation04FinalCsvNormalizationPrintSummary = false;
input bool   InpConsolidation04FinalCsvNormalizationWriteLatestCsv = true;
input bool   InpConsolidation04FinalCsvNormalizationRequireNoSendIntegrity = true;
input string InpConsolidation04FinalCsvNormalizationFolder = "FlagCountingPhoenix";

// ------------------------------ Consolidation 05 Runtime Health -------------
// Runtime no-send health summary. No OrderSend, no OrderCheck, no CTrade, no real execution.
input bool   InpConsolidation05RuntimeHealthEnabled = true;
input bool   InpConsolidation05RuntimeHealthExportCsv = true;
input bool   InpConsolidation05RuntimeHealthPrintSummary = false;
input bool   InpConsolidation05RuntimeHealthWriteLatestCsv = true;
input bool   InpConsolidation05RuntimeHealthRequireContextReady = false;
input bool   InpConsolidation05RuntimeHealthRequireFinalDecisionExport = true;
input bool   InpConsolidation05RuntimeHealthRequireNormalizedExport = true;
input bool   InpConsolidation05RuntimeHealthRequireNoSendIntegrity = true;
input string InpConsolidation05RuntimeHealthFolder = "FlagCountingPhoenix";

static datetime g_fp_last_bar_time = 0;

FP_OfflineLicenseConfig g_fp_license_cfg;
FP_OfflineLicenseReport g_fp_license_report;
bool g_fp_license_ok = false;
datetime g_fp_license_next_check = 0;

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

   // Hook display family override. RALLY_ONLY preserves the previous render
   // behavior. HOOK_ONLY suppresses Rally/F rendering so Phase 01 Hook nodes can
   // be inspected without chart pollution. RALLY_AND_HOOK keeps both layers.
   if(InpNDSHookDisplayFamily == FP_NDS_HOOK_DISPLAY_HOOK_ONLY ||
      InpHookPhase07ViewProfile == FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG)
   {
      cfg.draw_f1 = false;
      cfg.draw_f2 = false;
      cfg.draw_f3 = false;
      cfg.draw_hooks = false;
      cfg.draw_candidates = false;
      cfg.draw_confirmed = false;
      cfg.draw_locked = false;
      cfg.draw_invalidated = false;
      cfg.show_hook_count_labels = false;
      cfg.detailed_labels = false;
      cfg.show_parent_ids = false;
      cfg.show_origin_labels = false;
      cfg.show_internal_labels = false;
      cfg.max_events_to_draw = 0;
      cfg.max_hooks_to_draw = 0;
      cfg.delete_existing_by_prefix = true;
   }

   cfg.print_sanity = InpPrintRenderSanity;
   cfg.print_samples = InpPrintRenderSamples;
   cfg.sample_limit = InpRenderSampleLimit;
}



void FP_LoadLevel19StateGateConfig(FP_Level19StateGateConfig &cfg)
{
   FP_ResetLevel19StateGateConfig(cfg);
   cfg.enabled = InpLevel19StateGateEnabled;
   cfg.export_csv = InpLevel19StateGateExportCsv;
   cfg.export_closed_bar_ledger_csv = InpLevel19StateGateExportClosedBarLedgerCsv;
   cfg.export_state_delta_csv = InpLevel19StateGateExportStateDeltaCsv;
   cfg.export_transition_event_csv = InpLevel19StateGateExportTransitionEventCsv;
   cfg.export_transition_summary_csv = InpLevel19StateGateExportTransitionSummaryCsv;
   cfg.export_transition_stability_csv = InpLevel19StateGateExportTransitionStabilityCsv;
   cfg.export_regime_label_csv = InpLevel19StateGateExportRegimeLabelCsv;
   cfg.export_completion_csv = InpLevel19StateGateExportCompletionCsv;
   cfg.panel_enabled = InpLevel19StateGatePanelEnabled;
   cfg.panel_clean_on_init = InpLevel19StateGatePanelCleanOnInit;
   cfg.panel_clean_on_deinit = InpLevel19StateGatePanelCleanOnDeinit;
   cfg.print_summary = InpLevel19StateGatePrintSummary;
   cfg.folder = InpLevel19StateGateFolder;
   cfg.object_prefix = InpLevel19StateGateObjectPrefix;
   cfg.panel_corner = InpLevel19StateGatePanelCorner;
   cfg.panel_x = InpLevel19StateGatePanelX;
   cfg.panel_y = InpLevel19StateGatePanelY;
   cfg.panel_width = InpLevel19StateGatePanelWidth;
   cfg.panel_font_size = InpLevel19StateGatePanelFontSize;
}



void FP_LoadLevel20EntryBridgeConfig(FP_Level20EntryBridgeConfig &cfg)
{
   FP_ResetLevel20EntryBridgeConfig(cfg);
   cfg.enabled = InpLevel20EntryBridgeEnabled;
   cfg.export_csv = InpLevel20EntryBridgeExportCsv;
   cfg.print_summary = InpLevel20EntryBridgePrintSummary;
   cfg.prefer_latest_visible_event = InpLevel20EntryBridgePreferLatestVisibleEvent;
   cfg.allow_hook_fallback = InpLevel20EntryBridgeAllowHookFallback;
   cfg.min_rr = InpLevel20EntryBridgeMinRR;
   cfg.folder = InpLevel20EntryBridgeFolder;
}



void FP_LoadLevel21PaperIntentConfig(FP_Level21PaperIntentConfig &cfg)
{
   FP_ResetLevel21PaperIntentConfig(cfg);
   cfg.enabled = InpLevel21PaperIntentEnabled;
   cfg.export_csv = InpLevel21PaperIntentExportCsv;
   cfg.print_summary = InpLevel21PaperIntentPrintSummary;
   cfg.require_entry_bridge_ready = InpLevel21PaperIntentRequireEntryBridgeReady;
   cfg.require_directional_geometry = InpLevel21PaperIntentRequireDirectionalGeometry;
   cfg.expiry_bars = InpLevel21PaperIntentExpiryBars;
   cfg.folder = InpLevel21PaperIntentFolder;
}



void FP_LoadLevel22PaperLifecycleConfig(FP_Level22PaperLifecycleConfig &cfg)
{
   FP_ResetLevel22PaperLifecycleConfig(cfg);
   cfg.enabled = InpLevel22PaperLifecycleEnabled;
   cfg.export_csv = InpLevel22PaperLifecycleExportCsv;
   cfg.print_summary = InpLevel22PaperLifecyclePrintSummary;
   cfg.require_intent_allowed = InpLevel22PaperLifecycleRequireIntentAllowed;
   cfg.default_expiry_bars = InpLevel22PaperLifecycleDefaultExpiryBars;
   cfg.folder = InpLevel22PaperLifecycleFolder;
}



void FP_LoadLevel23PaperPerformanceConfig(FP_Level23PaperPerformanceConfig &cfg)
{
   FP_ResetLevel23PaperPerformanceConfig(cfg);
   cfg.enabled = InpLevel23PaperPerformanceEnabled;
   cfg.export_csv = InpLevel23PaperPerformanceExportCsv;
   cfg.print_summary = InpLevel23PaperPerformancePrintSummary;
   cfg.count_blocked_samples = InpLevel23PaperPerformanceCountBlockedSamples;
   cfg.count_open_samples = InpLevel23PaperPerformanceCountOpenSamples;
   cfg.count_expired_as_resolved = InpLevel23PaperPerformanceCountExpiredAsResolved;
   cfg.folder = InpLevel23PaperPerformanceFolder;
}



void FP_LoadLevel24SafetyGateConfig(FP_Level24SafetyGateConfig &cfg)
{
   FP_ResetLevel24SafetyGateConfig(cfg);
   cfg.enabled = InpLevel24SafetyGateEnabled;
   cfg.export_csv = InpLevel24SafetyGateExportCsv;
   cfg.print_summary = InpLevel24SafetyGatePrintSummary;
   cfg.manual_arm = InpLevel24SafetyGateManualArm;
   cfg.real_execution_enabled = InpLevel24SafetyGateRealExecutionEnabled;
   cfg.require_license_ok = InpLevel24SafetyGateRequireLicenseOk;
   cfg.require_symbol_allowed = InpLevel24SafetyGateRequireSymbolAllowed;
   cfg.require_timeframe_allowed = InpLevel24SafetyGateRequireTimeframeAllowed;
   cfg.require_spread_ok = InpLevel24SafetyGateRequireSpreadOk;
   cfg.require_performance_ok = InpLevel24SafetyGateRequirePerformanceOk;
   cfg.require_manual_arm = InpLevel24SafetyGateRequireManualArm;
   cfg.require_real_execution_disabled = InpLevel24SafetyGateRequireRealExecutionDisabled;
   cfg.allowed_symbols = InpLevel24SafetyGateAllowedSymbols;
   cfg.allowed_timeframes = InpLevel24SafetyGateAllowedTimeframes;
   cfg.max_spread_points = InpLevel24SafetyGateMaxSpreadPoints;
   cfg.min_resolved_samples = InpLevel24SafetyGateMinResolvedSamples;
   cfg.min_hit_rate_like = InpLevel24SafetyGateMinHitRateLike;
   cfg.min_avg_r_like = InpLevel24SafetyGateMinAvgRLike;
   cfg.folder = InpLevel24SafetyGateFolder;
}



void FP_LoadLevel25BrokerDryRunConfig(FP_Level25BrokerDryRunConfig &cfg)
{
   FP_ResetLevel25BrokerDryRunConfig(cfg);
   cfg.enabled = InpLevel25BrokerDryRunEnabled;
   cfg.export_csv = InpLevel25BrokerDryRunExportCsv;
   cfg.print_summary = InpLevel25BrokerDryRunPrintSummary;
   cfg.require_safety_gate_passed = InpLevel25BrokerDryRunRequireSafetyGatePassed;
   cfg.require_intent_allowed = InpLevel25BrokerDryRunRequireIntentAllowed;
   cfg.dry_run_only = InpLevel25BrokerDryRunOnly;
   cfg.magic = InpLevel25BrokerDryRunMagic;
   cfg.request_comment = InpLevel25BrokerDryRunComment;
   cfg.folder = InpLevel25BrokerDryRunFolder;
}



void FP_LoadLevel26BrokerValidatorConfig(FP_Level26BrokerValidatorConfig &cfg)
{
   FP_ResetLevel26BrokerValidatorConfig(cfg);
   cfg.enabled = InpLevel26BrokerValidatorEnabled;
   cfg.export_csv = InpLevel26BrokerValidatorExportCsv;
   cfg.print_summary = InpLevel26BrokerValidatorPrintSummary;
   cfg.require_dry_run_built = InpLevel26BrokerValidatorRequireDryRunBuilt;
   cfg.require_tick_alignment = InpLevel26BrokerValidatorRequireTickAlignment;
   cfg.require_stop_distance = InpLevel26BrokerValidatorRequireStopDistance;
   cfg.require_normalized_prices = InpLevel26BrokerValidatorRequireNormalizedPrices;
   cfg.require_zero_volume = InpLevel26BrokerValidatorRequireZeroVolume;
   cfg.require_dry_run_only = InpLevel26BrokerValidatorRequireDryRunOnly;
   cfg.folder = InpLevel26BrokerValidatorFolder;
}



void FP_LoadLevel27BrokerRequestLedgerConfig(FP_Level27BrokerRequestLedgerConfig &cfg)
{
   FP_ResetLevel27BrokerRequestLedgerConfig(cfg);
   cfg.enabled = InpLevel27BrokerRequestLedgerEnabled;
   cfg.export_csv = InpLevel27BrokerRequestLedgerExportCsv;
   cfg.print_summary = InpLevel27BrokerRequestLedgerPrintSummary;
   cfg.append_ledger_csv = InpLevel27BrokerRequestLedgerAppendCsv;
   cfg.write_latest_csv = InpLevel27BrokerRequestLedgerWriteLatestCsv;
   cfg.skip_duplicate_request_key = InpLevel27BrokerRequestLedgerSkipDuplicateRequestKey;
   cfg.folder = InpLevel27BrokerRequestLedgerFolder;
}



void FP_LoadLevel28BrokerRequestAuditConfig(FP_Level28BrokerRequestAuditConfig &cfg)
{
   FP_ResetLevel28BrokerRequestAuditConfig(cfg);
   cfg.enabled = InpLevel28BrokerRequestAuditEnabled;
   cfg.export_csv = InpLevel28BrokerRequestAuditExportCsv;
   cfg.print_summary = InpLevel28BrokerRequestAuditPrintSummary;
   cfg.append_audit_csv = InpLevel28BrokerRequestAuditAppendCsv;
   cfg.write_latest_csv = InpLevel28BrokerRequestAuditWriteLatestCsv;
   cfg.skip_duplicate_audit_key = InpLevel28BrokerRequestAuditSkipDuplicateAuditKey;
   cfg.require_dry_run_only = InpLevel28BrokerRequestAuditRequireDryRunOnly;
   cfg.require_zero_volume = InpLevel28BrokerRequestAuditRequireZeroVolume;
   cfg.require_no_send_contract = InpLevel28BrokerRequestAuditRequireNoSendContract;
   cfg.require_request_validator_coherence = InpLevel28BrokerRequestAuditRequireRequestValidatorCoherence;
   cfg.require_safety_intent_coherence = InpLevel28BrokerRequestAuditRequireSafetyIntentCoherence;
   cfg.folder = InpLevel28BrokerRequestAuditFolder;
}



void FP_LoadLevel29PaperBrokerAdapterConfig(FP_Level29PaperBrokerAdapterConfig &cfg)
{
   FP_ResetLevel29PaperBrokerAdapterConfig(cfg);
   cfg.enabled = InpLevel29PaperBrokerAdapterEnabled;
   cfg.export_csv = InpLevel29PaperBrokerAdapterExportCsv;
   cfg.print_summary = InpLevel29PaperBrokerAdapterPrintSummary;
   cfg.append_adapter_csv = InpLevel29PaperBrokerAdapterAppendCsv;
   cfg.write_latest_csv = InpLevel29PaperBrokerAdapterWriteLatestCsv;
   cfg.skip_duplicate_adapter_key = InpLevel29PaperBrokerAdapterSkipDuplicateAdapterKey;
   cfg.require_audit_passed = InpLevel29PaperBrokerAdapterRequireAuditPassed;
   cfg.require_validator_passed = InpLevel29PaperBrokerAdapterRequireValidatorPassed;
   cfg.require_request_built = InpLevel29PaperBrokerAdapterRequireRequestBuilt;
   cfg.require_dry_run_only = InpLevel29PaperBrokerAdapterRequireDryRunOnly;
   cfg.require_zero_volume = InpLevel29PaperBrokerAdapterRequireZeroVolume;
   cfg.adapter_dry_run_only = InpLevel29PaperBrokerAdapterDryRunOnly;
   cfg.folder = InpLevel29PaperBrokerAdapterFolder;
}



void FP_LoadLevel30PaperBrokerLifecycleConfig(FP_Level30PaperBrokerLifecycleConfig &cfg)
{
   FP_ResetLevel30PaperBrokerLifecycleConfig(cfg);
   cfg.enabled = InpLevel30PaperBrokerLifecycleEnabled;
   cfg.export_csv = InpLevel30PaperBrokerLifecycleExportCsv;
   cfg.print_summary = InpLevel30PaperBrokerLifecyclePrintSummary;
   cfg.append_lifecycle_csv = InpLevel30PaperBrokerLifecycleAppendCsv;
   cfg.write_latest_csv = InpLevel30PaperBrokerLifecycleWriteLatestCsv;
   cfg.skip_duplicate_lifecycle_key = InpLevel30PaperBrokerLifecycleSkipDuplicateLifecycleKey;
   cfg.require_adapter_registered = InpLevel30PaperBrokerLifecycleRequireAdapterRegistered;
   cfg.require_zero_volume = InpLevel30PaperBrokerLifecycleRequireZeroVolume;
   cfg.close_only = InpLevel30PaperBrokerLifecycleCloseOnly;
   cfg.expiry_bars = InpLevel30PaperBrokerLifecycleExpiryBars;
   cfg.folder = InpLevel30PaperBrokerLifecycleFolder;
}



void FP_LoadConsolidation01NoSendContextConfig(FP_Consolidation01NoSendContextConfig &cfg)
{
   FP_ResetConsolidation01NoSendContextConfig(cfg);
   cfg.enabled = InpConsolidation01NoSendContextEnabled;
   cfg.export_csv = InpConsolidation01NoSendContextExportCsv;
   cfg.print_summary = InpConsolidation01NoSendContextPrintSummary;
   cfg.write_latest_csv = InpConsolidation01NoSendContextWriteLatestCsv;
   cfg.folder = InpConsolidation01NoSendContextFolder;
}



void FP_LoadConsolidation02FinalDecisionConfig(FP_Consolidation02FinalDecisionConfig &cfg)
{
   FP_ResetConsolidation02FinalDecisionConfig(cfg);
   cfg.enabled = InpConsolidation02FinalDecisionEnabled;
   cfg.export_csv = InpConsolidation02FinalDecisionExportCsv;
   cfg.print_summary = InpConsolidation02FinalDecisionPrintSummary;
   cfg.write_latest_csv = InpConsolidation02FinalDecisionWriteLatestCsv;
   cfg.require_context_ready_for_ready_state = InpConsolidation02FinalDecisionRequireContextReady;
   cfg.require_lifecycle_tracked_for_ready_state = InpConsolidation02FinalDecisionRequireLifecycleTracked;
   cfg.require_no_send_integrity = InpConsolidation02FinalDecisionRequireNoSendIntegrity;
   cfg.folder = InpConsolidation02FinalDecisionFolder;
}



void FP_LoadConsolidation04FinalCsvNormalizationConfig(FP_Consolidation04FinalCsvNormalizationConfig &cfg)
{
   FP_ResetConsolidation04FinalCsvNormalizationConfig(cfg);
   cfg.enabled = InpConsolidation04FinalCsvNormalizationEnabled;
   cfg.export_csv = InpConsolidation04FinalCsvNormalizationExportCsv;
   cfg.print_summary = InpConsolidation04FinalCsvNormalizationPrintSummary;
   cfg.write_latest_csv = InpConsolidation04FinalCsvNormalizationWriteLatestCsv;
   cfg.require_no_send_integrity = InpConsolidation04FinalCsvNormalizationRequireNoSendIntegrity;
   cfg.folder = InpConsolidation04FinalCsvNormalizationFolder;
}



void FP_LoadConsolidation05RuntimeHealthConfig(FP_Consolidation05RuntimeHealthConfig &cfg)
{
   FP_ResetConsolidation05RuntimeHealthConfig(cfg);
   cfg.enabled = InpConsolidation05RuntimeHealthEnabled;
   cfg.export_csv = InpConsolidation05RuntimeHealthExportCsv;
   cfg.print_summary = InpConsolidation05RuntimeHealthPrintSummary;
   cfg.write_latest_csv = InpConsolidation05RuntimeHealthWriteLatestCsv;
   cfg.require_context_ready = InpConsolidation05RuntimeHealthRequireContextReady;
   cfg.require_final_decision_export = InpConsolidation05RuntimeHealthRequireFinalDecisionExport;
   cfg.require_normalized_export = InpConsolidation05RuntimeHealthRequireNormalizedExport;
   cfg.require_no_send_integrity = InpConsolidation05RuntimeHealthRequireNoSendIntegrity;
   cfg.folder = InpConsolidation05RuntimeHealthFolder;
}


void FP_LoadHookPhase01Config(FP_HookPhase01Config &cfg)
{
   FP_ResetHookPhase01Config(cfg);
   cfg.enabled = InpHookPhase01Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;
   cfg.show_peaks = InpHookPhase01ShowPeaks;
   cfg.show_valleys = InpHookPhase01ShowValleys;
   cfg.draw_nodes = InpHookPhase01DrawNodes;
   cfg.draw_labels = InpHookPhase01DrawLabels;
   cfg.export_csv = InpHookPhase01ExportCsv;
   cfg.print_summary = InpHookPhase01PrintSummary;
   cfg.print_samples = InpHookPhase01PrintSamples;
   cfg.max_bars_to_scan = InpHookPhase01MaxBarsToScan;
   cfg.max_nodes = InpHookPhase01MaxNodes;
   cfg.max_nodes_to_draw = InpHookPhase01MaxNodesToDraw;
   cfg.sample_limit = InpHookPhase01SampleLimit;
   cfg.folder = InpHookPhase01Folder;
   cfg.object_prefix = InpHookPhase01ObjectPrefix;
   cfg.peak_color = InpHookPhase01PeakColor;
   cfg.valley_color = InpHookPhase01ValleyColor;
   cfg.label_color = InpHookPhase01LabelColor;
   cfg.marker_width = InpHookPhase01MarkerWidth;
   cfg.label_font_size = InpHookPhase01LabelFontSize;
}


void FP_LoadHookPhase02Config(FP_HookPhase02Config &cfg)
{
   FP_ResetHookPhase02Config(cfg);
   cfg.enabled = InpHookPhase02Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;
   cfg.origin_policy = InpHookPhase02OriginPolicy;

   cfg.show_positive = InpHookPhase02ShowPositive;
   cfg.show_negative = InpHookPhase02ShowNegative;

   cfg.draw_sequences = InpHookPhase02DrawSequences;
   cfg.draw_origin = InpHookPhase02DrawOrigin;
   cfg.draw_x_nodes = InpHookPhase02DrawXNodes;
   cfg.draw_x_lines = InpHookPhase02DrawXLines;
   cfg.draw_death_boundary = InpHookPhase02DrawDeathBoundary;
   cfg.draw_cycle_arc = InpHookPhase02DrawCycleArc;
   cfg.draw_sequence_count_label = InpHookPhase02DrawSequenceCountLabel;
   cfg.draw_labels = InpHookPhase02DrawLabels;

   cfg.export_csv = InpHookPhase02ExportCsv;
   cfg.print_summary = InpHookPhase02PrintSummary;
   cfg.print_samples = InpHookPhase02PrintSamples;

   cfg.max_bars_to_scan = InpHookPhase02MaxBarsToScan;
   cfg.max_sequences = InpHookPhase02MaxSequences;
   cfg.max_sequences_to_draw = InpHookPhase02MaxSequencesToDraw;
   cfg.min_x_count_to_draw = InpHookPhase02MinXCountToDraw;
   cfg.arc_min_x_count_to_draw = InpHookPhase02ArcMinXCountToDraw;
   cfg.sequence_draw_mode = InpHookPhase02SequenceDrawMode;
   cfg.sequence_draw_scale_l = InpHookPhase02SequenceDrawScaleL;
   cfg.sequence_draw_direction = InpHookPhase02SequenceDrawDirection;
   cfg.sequence_draw_sequence_id = InpHookPhase02SequenceDrawSequenceId;
   cfg.node_label_mode = InpHookPhase02NodeLabelMode;
   cfg.cycle_arc_end_mode = InpHookPhase02CycleArcEndMode;
   cfg.use_sequence_palette_colors = InpHookPhase02UseSequencePaletteColors;
   cfg.color_origin_with_sequence = InpHookPhase02ColorOriginWithSequence;
   cfg.color_node_labels_with_sequence = InpHookPhase02ColorNodeLabelsWithSequence;
   cfg.color_node_numbers_by_index = InpHookPhase02ColorNodeNumbersByIndex;
   cfg.minimal_numbers_only = InpHookPhase02MinimalNumbersOnly;
   cfg.use_minimal_node_markers = InpHookPhase02UseMinimalNodeMarkers;
   cfg.stack_node_labels_on_collisions = InpHookPhase02StackNodeLabelsOnCollisions;
   cfg.min_x_nodes_to_keep = InpHookPhase02MinXNodesToKeep;
   cfg.max_x_nodes_per_sequence = InpHookPhase02MaxXNodesPerSequence;
   cfg.sample_limit = InpHookPhase02SampleLimit;
   cfg.cycle_arc_segments = InpHookPhase02CycleArcSegments;
   cfg.cycle_arc_max_height_points = InpHookPhase02CycleArcMaxHeightPoints;
   cfg.node_number_offset_points = InpHookPhase02NodeNumberOffsetPoints;
   cfg.node_label_stack_step_points = InpHookPhase02NodeLabelStackStepPoints;
   cfg.minimal_node_marker_arrow_code = InpHookPhase02MinimalNodeMarkerArrowCode;
   cfg.cycle_arc_height_ratio = InpHookPhase02CycleArcHeightRatio;

   cfg.folder = InpHookPhase02Folder;
   cfg.object_prefix = InpHookPhase02ObjectPrefix;

   cfg.positive_color = InpHookPhase02PositiveColor;
   cfg.negative_color = InpHookPhase02NegativeColor;
   cfg.origin_color = InpHookPhase02OriginColor;
   cfg.death_color = InpHookPhase02DeathColor;
   cfg.cycle_arc_color = InpHookPhase02CycleArcColor;
   cfg.sequence_count_label_color = InpHookPhase02SequenceCountLabelColor;
   cfg.label_color = InpHookPhase02LabelColor;

   cfg.line_width = InpHookPhase02LineWidth;
   cfg.marker_width = InpHookPhase02MarkerWidth;
   cfg.label_font_size = InpHookPhase02LabelFontSize;
}


void FP_LoadHookPhase03Config(FP_HookPhase03Config &cfg)
{
   FP_ResetHookPhase03Config(cfg);
   cfg.enabled = InpHookPhase03Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;

   cfg.show_positive = InpHookPhase03ShowPositive;
   cfg.show_negative = InpHookPhase03ShowNegative;

   cfg.draw_y_extremes = InpHookPhase03DrawYExtremes;
   cfg.draw_y_lines = InpHookPhase03DrawYLines;
   cfg.draw_x_reference = InpHookPhase03DrawXReference;
   cfg.draw_labels = InpHookPhase03DrawLabels;

   cfg.export_csv = InpHookPhase03ExportCsv;
   cfg.print_summary = InpHookPhase03PrintSummary;
   cfg.print_samples = InpHookPhase03PrintSamples;

   cfg.max_bars_to_scan = InpHookPhase03MaxBarsToScan;
   cfg.max_sequences = InpHookPhase03MaxSequences;
   cfg.max_sequences_to_draw = InpHookPhase03MaxSequencesToDraw;
   cfg.min_x_nodes_to_keep = InpHookPhase03MinXNodesToKeep;
   cfg.max_x_nodes_per_sequence = InpHookPhase03MaxXNodesPerSequence;
   cfg.sample_limit = InpHookPhase03SampleLimit;

   cfg.folder = InpHookPhase03Folder;
   cfg.object_prefix = InpHookPhase03ObjectPrefix;

   cfg.positive_y_color = InpHookPhase03PositiveYColor;
   cfg.negative_y_color = InpHookPhase03NegativeYColor;
   cfg.x_reference_color = InpHookPhase03XReferenceColor;
   cfg.label_color = InpHookPhase03LabelColor;

   cfg.line_width = InpHookPhase03LineWidth;
   cfg.marker_width = InpHookPhase03MarkerWidth;
   cfg.label_font_size = InpHookPhase03LabelFontSize;
}


void FP_LoadHookPhase04Config(FP_HookPhase04Config &cfg)
{
   FP_ResetHookPhase04Config(cfg);
   cfg.enabled = InpHookPhase04Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;

   cfg.show_positive = InpHookPhase04ShowPositive;
   cfg.show_negative = InpHookPhase04ShowNegative;

   cfg.draw_nd = InpHookPhase04DrawND;
   cfg.draw_death = InpHookPhase04DrawDeath;
   cfg.draw_x_closure = InpHookPhase04DrawXClosure;
   cfg.draw_thresholds = InpHookPhase04DrawThresholds;
   cfg.draw_labels = InpHookPhase04DrawLabels;

   cfg.export_csv = InpHookPhase04ExportCsv;
   cfg.print_summary = InpHookPhase04PrintSummary;
   cfg.print_samples = InpHookPhase04PrintSamples;

   cfg.max_bars_to_scan = InpHookPhase04MaxBarsToScan;
   cfg.max_sequences = InpHookPhase04MaxSequences;
   cfg.max_sequences_to_draw = InpHookPhase04MaxSequencesToDraw;
   cfg.min_x_nodes_to_keep = InpHookPhase04MinXNodesToKeep;
   cfg.max_x_nodes_per_sequence = InpHookPhase04MaxXNodesPerSequence;
   cfg.min_x_nodes_for_closure = InpHookPhase04MinXNodesForClosure;
   cfg.sample_limit = InpHookPhase04SampleLimit;

   cfg.nd_return_ratio = InpHookPhase04NDReturnRatio;
   cfg.closure_retrace_ratio = InpHookPhase04ClosureRetraceRatio;

   cfg.folder = InpHookPhase04Folder;
   cfg.object_prefix = InpHookPhase04ObjectPrefix;

   cfg.nd_color = InpHookPhase04NDColor;
   cfg.death_color = InpHookPhase04DeathColor;
   cfg.closure_color = InpHookPhase04ClosureColor;
   cfg.threshold_color = InpHookPhase04ThresholdColor;
   cfg.label_color = InpHookPhase04LabelColor;

   cfg.line_width = InpHookPhase04LineWidth;
   cfg.marker_width = InpHookPhase04MarkerWidth;
   cfg.label_font_size = InpHookPhase04LabelFontSize;
}


void FP_LoadHookPhase05Config(FP_HookPhase05Config &cfg)
{
   FP_ResetHookPhase05Config(cfg);
   cfg.enabled = InpHookPhase05Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;

   cfg.show_positive = InpHookPhase05ShowPositive;
   cfg.show_negative = InpHookPhase05ShowNegative;

   cfg.draw_type_label = InpHookPhase05DrawTypeLabel;
   cfg.draw_type_anchor = InpHookPhase05DrawTypeAnchor;
   cfg.draw_type_comparison_lines = InpHookPhase05DrawTypeComparisonLines;
   cfg.draw_labels = InpHookPhase05DrawLabels;

   cfg.export_csv = InpHookPhase05ExportCsv;
   cfg.print_summary = InpHookPhase05PrintSummary;
   cfg.print_samples = InpHookPhase05PrintSamples;

   cfg.allow_y34_as_third_evidence = InpHookPhase05AllowY34AsThirdEvidence;

   cfg.max_bars_to_scan = InpHookPhase05MaxBarsToScan;
   cfg.max_sequences = InpHookPhase05MaxSequences;
   cfg.max_sequences_to_draw = InpHookPhase05MaxSequencesToDraw;
   cfg.min_x_nodes_to_keep = InpHookPhase05MinXNodesToKeep;
   cfg.max_x_nodes_per_sequence = InpHookPhase05MaxXNodesPerSequence;
   cfg.min_x_nodes_for_type = InpHookPhase05MinXNodesForType;
   cfg.sample_limit = InpHookPhase05SampleLimit;

   cfg.folder = InpHookPhase05Folder;
   cfg.object_prefix = InpHookPhase05ObjectPrefix;

   cfg.type_a_color = InpHookPhase05TypeAColor;
   cfg.type_b_color = InpHookPhase05TypeBColor;
   cfg.type_c_color = InpHookPhase05TypeCColor;
   cfg.insufficient_color = InpHookPhase05InsufficientColor;
   cfg.comparison_color = InpHookPhase05ComparisonColor;
   cfg.label_color = InpHookPhase05LabelColor;

   cfg.line_width = InpHookPhase05LineWidth;
   cfg.marker_width = InpHookPhase05MarkerWidth;
   cfg.label_font_size = InpHookPhase05LabelFontSize;
}



void FP_LoadHookPhase06Config(FP_HookPhase06Config &cfg)
{
   FP_ResetHookPhase06Config(cfg);
   cfg.enabled = InpHookPhase06Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;

   cfg.show_positive = InpHookPhase06ShowPositive;
   cfg.show_negative = InpHookPhase06ShowNegative;

   cfg.draw_quality_label = InpHookPhase06DrawQualityLabel;
   cfg.draw_xy_anchor = InpHookPhase06DrawXYAnchor;
   cfg.draw_projection_lines = InpHookPhase06DrawProjectionLines;
   cfg.draw_labels = InpHookPhase06DrawLabels;

   cfg.export_csv = InpHookPhase06ExportCsv;
   cfg.print_summary = InpHookPhase06PrintSummary;
   cfg.print_samples = InpHookPhase06PrintSamples;

   cfg.include_dead_records = InpHookPhase06IncludeDeadRecords;
   cfg.require_x_closed_for_xy = InpHookPhase06RequireXClosedForXY;

   cfg.max_bars_to_scan = InpHookPhase06MaxBarsToScan;
   cfg.max_sequences = InpHookPhase06MaxSequences;
   cfg.max_sequences_to_draw = InpHookPhase06MaxSequencesToDraw;
   cfg.min_x_nodes_to_keep = InpHookPhase06MinXNodesToKeep;
   cfg.max_x_nodes_per_sequence = InpHookPhase06MaxXNodesPerSequence;
   cfg.min_x_nodes_for_quality = InpHookPhase06MinXNodesForQuality;
   cfg.min_y_comparisons_for_closed = InpHookPhase06MinYComparisonsForClosed;
   cfg.sample_limit = InpHookPhase06SampleLimit;

   cfg.x_weight = InpHookPhase06XWeight;
   cfg.y_weight = InpHookPhase06YWeight;
   cfg.type_weight = InpHookPhase06TypeWeight;
   cfg.lifecycle_weight = InpHookPhase06LifecycleWeight;
   cfg.elite_threshold = InpHookPhase06EliteThreshold;
   cfg.high_threshold = InpHookPhase06HighThreshold;
   cfg.medium_threshold = InpHookPhase06MediumThreshold;
   cfg.low_threshold = InpHookPhase06LowThreshold;

   cfg.folder = InpHookPhase06Folder;
   cfg.object_prefix = InpHookPhase06ObjectPrefix;

   cfg.xy_closed_color = InpHookPhase06XYClosedColor;
   cfg.x_only_color = InpHookPhase06XOnlyColor;
   cfg.y_only_color = InpHookPhase06YOnlyColor;
   cfg.open_color = InpHookPhase06OpenColor;
   cfg.insufficient_color = InpHookPhase06InsufficientColor;
   cfg.projection_color = InpHookPhase06ProjectionColor;
   cfg.label_color = InpHookPhase06LabelColor;

   cfg.line_width = InpHookPhase06LineWidth;
   cfg.marker_width = InpHookPhase06MarkerWidth;
   cfg.label_font_size = InpHookPhase06LabelFontSize;
}


void FP_LoadHookPhase07Config(FP_HookPhase07Config &cfg)
{
   FP_ResetHookPhase07Config(cfg);
   cfg.enabled = InpHookPhase07Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;
   cfg.view_profile = InpHookPhase07ViewProfile;

   cfg.respect_individual_phase_enabled = InpHookPhase07RespectIndividualPhaseEnabled;
   cfg.force_enable_required_phases = InpHookPhase07ForceEnableRequiredPhases;
   cfg.show_labels = InpHookPhase07ShowLabels;
   cfg.global_export_csv = InpHookPhase07GlobalExportCsv;
   cfg.global_print_summary = InpHookPhase07GlobalPrintSummary;
   cfg.global_print_samples = InpHookPhase07GlobalPrintSamples;
   cfg.export_profile_csv = InpHookPhase07ExportProfileCsv;
   cfg.print_summary = InpHookPhase07PrintSummary;

   cfg.clean_before_apply = InpHookPhase07CleanBeforeApply;
   cfg.clean_common_hook_prefix = InpHookPhase07CleanCommonHookPrefix;
   cfg.common_hook_object_prefix = InpHookPhase07CommonHookObjectPrefix;
   cfg.clean_p01_objects = InpHookPhase07CleanP01Objects;
   cfg.clean_p02_objects = InpHookPhase07CleanP02Objects;
   cfg.clean_p03_objects = InpHookPhase07CleanP03Objects;
   cfg.clean_p04_objects = InpHookPhase07CleanP04Objects;
   cfg.clean_p05_objects = InpHookPhase07CleanP05Objects;
   cfg.clean_p06_objects = InpHookPhase07CleanP06Objects;
   cfg.clean_p07_objects = InpHookPhase07CleanP07Objects;
   cfg.clean_p08_objects = InpHookPhase07CleanP08Objects;
   cfg.clean_p09_objects = InpHookPhase07CleanP09Objects;
   cfg.clean_p10_objects = InpHookPhase07CleanP10Objects;

   cfg.clean_p08_object_prefix = InpHookPhase08ObjectPrefix;
   cfg.clean_p09_object_prefix = InpHookPhase09ObjectPrefix;
   cfg.clean_p10_object_prefix = InpHookPhase10ObjectPrefix;

   cfg.max_nodes_to_draw = InpHookPhase07MaxNodesToDraw;
   cfg.max_sequences_to_draw = InpHookPhase07MaxSequencesToDraw;
   cfg.sample_limit = InpHookPhase07SampleLimit;

   cfg.folder = InpHookPhase07Folder;
   cfg.object_prefix = InpHookPhase07ObjectPrefix;
}

void FP_LoadHookPhase08Config(FP_HookPhase08Config &cfg)
{
   FP_ResetHookPhase08Config(cfg);
   cfg.enabled = InpHookPhase08Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;
   cfg.allow_rally_only_audit = InpHookPhase08AllowRallyOnlyAudit;
   cfg.export_csv = InpHookPhase08ExportCsv;
   cfg.export_phase_matrix_csv = InpHookPhase08ExportPhaseMatrixCsv;
   cfg.export_integrity_csv = InpHookPhase08ExportIntegrityCsv;
   cfg.print_summary = InpHookPhase08PrintSummary;
   cfg.print_samples = InpHookPhase08PrintSamples;
   cfg.require_runtime_report_ok = InpHookPhase08RequireRuntimeReportOk;
   cfg.require_phase_chain_alignment = InpHookPhase08RequirePhaseChainAlignment;
   cfg.require_unique_object_prefixes = InpHookPhase08RequireUniqueObjectPrefixes;
   cfg.require_nonnegative_counts = InpHookPhase08RequireNonnegativeCounts;
   cfg.require_audit_export_profile_alignment = InpHookPhase08RequireAuditExportProfileAlignment;
   cfg.require_no_file_errors = InpHookPhase08RequireNoFileErrors;
   cfg.require_p06_records_for_quality_audit = InpHookPhase08RequireP06RecordsForQualityAudit;
   cfg.max_warnings_allowed = InpHookPhase08MaxWarningsAllowed;
   cfg.sample_limit = InpHookPhase08SampleLimit;
   cfg.folder = InpHookPhase08Folder;
   cfg.object_prefix = InpHookPhase08ObjectPrefix;
}



void FP_LoadHookPhase09Config(FP_HookPhase09Config &cfg)
{
   FP_ResetHookPhase09Config(cfg);
   cfg.enabled = InpHookPhase09Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;
   cfg.allow_rally_only_smoke = InpHookPhase09AllowRallyOnlySmoke;
   cfg.require_phase08_ok = InpHookPhase09RequirePhase08Ok;
   cfg.require_current_profile_coverage = InpHookPhase09RequireCurrentProfileCoverage;
   cfg.require_object_census = InpHookPhase09RequireObjectCensus;
   cfg.require_draw_contract_when_records_exist = InpHookPhase09RequireDrawContractWhenRecordsExist;
   cfg.require_audit_only_no_hook_draw = InpHookPhase09RequireAuditOnlyNoHookDraw;
   cfg.require_no_phase_file_errors = InpHookPhase09RequireNoPhaseFileErrors;
   cfg.require_p09_panel_when_enabled = InpHookPhase09RequirePanelWhenEnabled;
   cfg.draw_panel = InpHookPhase09DrawPanel;
   cfg.clean_p09_objects_before_draw = InpHookPhase09CleanObjectsBeforeDraw;
   cfg.export_csv = InpHookPhase09ExportCsv;
   cfg.export_scenarios_csv = InpHookPhase09ExportScenariosCsv;
   cfg.export_object_census_csv = InpHookPhase09ExportObjectCensusCsv;
   cfg.export_findings_csv = InpHookPhase09ExportFindingsCsv;
   cfg.print_summary = InpHookPhase09PrintSummary;
   cfg.print_samples = InpHookPhase09PrintSamples;
   cfg.max_warnings_allowed = InpHookPhase09MaxWarningsAllowed;
   cfg.sample_limit = InpHookPhase09SampleLimit;
   cfg.folder = InpHookPhase09Folder;
   cfg.object_prefix = InpHookPhase09ObjectPrefix;
   cfg.panel_corner = InpHookPhase09PanelCorner;
   cfg.panel_x = InpHookPhase09PanelX;
   cfg.panel_y = InpHookPhase09PanelY;
   cfg.panel_font_size = InpHookPhase09PanelFontSize;
   cfg.panel_ok_color = InpHookPhase09PanelOkColor;
   cfg.panel_warning_color = InpHookPhase09PanelWarningColor;
   cfg.panel_blocker_color = InpHookPhase09PanelBlockerColor;
   cfg.panel_text_color = InpHookPhase09PanelTextColor;
}


void FP_LoadHookPhase10Config(FP_HookPhase10Config &cfg)
{
   FP_ResetHookPhase10Config(cfg);
   cfg.enabled = InpHookPhase10Enabled;
   cfg.display_family = InpNDSHookDisplayFamily;
   cfg.freeze_mode = InpHookPhase10FreezeMode;
   cfg.allow_rally_only_freeze = InpHookPhase10AllowRallyOnlyFreeze;
   cfg.require_phase08_ok = InpHookPhase10RequirePhase08Ok;
   cfg.require_phase09_ok = InpHookPhase10RequirePhase09Ok;
   cfg.require_hook_records = InpHookPhase10RequireHookRecords;
   cfg.require_xy_quality_records = InpHookPhase10RequireXYQualityRecords;
   cfg.require_high_quality_records = InpHookPhase10RequireHighQualityRecords;
   cfg.require_view_profile_not_keep_inputs = InpHookPhase10RequireViewProfileNotKeepInputs;
   cfg.require_export_contract = InpHookPhase10RequireExportContract;
   cfg.require_no_file_errors = InpHookPhase10RequireNoFileErrors;
   cfg.export_csv = InpHookPhase10ExportCsv;
   cfg.export_contract_checks_csv = InpHookPhase10ExportContractChecksCsv;
   cfg.export_training_schema_csv = InpHookPhase10ExportTrainingSchemaCsv;
   cfg.export_freeze_manifest_csv = InpHookPhase10ExportFreezeManifestCsv;
   cfg.print_summary = InpHookPhase10PrintSummary;
   cfg.print_samples = InpHookPhase10PrintSamples;
   cfg.min_p06_records_total = InpHookPhase10MinP06RecordsTotal;
   cfg.min_xy_closed_records = InpHookPhase10MinXYClosedRecords;
   cfg.min_high_or_elite_records = InpHookPhase10MinHighOrEliteRecords;
   cfg.max_warnings_allowed = InpHookPhase10MaxWarningsAllowed;
   cfg.sample_limit = InpHookPhase10SampleLimit;
   cfg.folder = InpHookPhase10Folder;
   cfg.object_prefix = InpHookPhase10ObjectPrefix;
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
   cfg.print_sanity = InpPrintLicenseSanity;
   cfg.print_samples = InpPrintLicenseSamples;
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
   if(g_fp_license_cfg.print_sanity || (InpPrintLicenseFailures && !g_fp_license_ok))
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

   FP_Level19StateGateConfig state_gate_cfg;
   FP_LoadLevel19StateGateConfig(state_gate_cfg);

   FP_Level20EntryBridgeConfig entry_bridge_cfg;
   FP_LoadLevel20EntryBridgeConfig(entry_bridge_cfg);

   FP_Level21PaperIntentConfig paper_intent_cfg;
   FP_LoadLevel21PaperIntentConfig(paper_intent_cfg);

   FP_Level22PaperLifecycleConfig paper_lifecycle_cfg;
   FP_LoadLevel22PaperLifecycleConfig(paper_lifecycle_cfg);

   FP_Level23PaperPerformanceConfig paper_performance_cfg;
   FP_LoadLevel23PaperPerformanceConfig(paper_performance_cfg);

   FP_Level24SafetyGateConfig safety_gate_cfg;
   FP_LoadLevel24SafetyGateConfig(safety_gate_cfg);

   FP_Level25BrokerDryRunConfig broker_dry_run_cfg;
   FP_LoadLevel25BrokerDryRunConfig(broker_dry_run_cfg);

   FP_Level26BrokerValidatorConfig broker_validator_cfg;
   FP_LoadLevel26BrokerValidatorConfig(broker_validator_cfg);

   FP_Level27BrokerRequestLedgerConfig broker_request_ledger_cfg;
   FP_LoadLevel27BrokerRequestLedgerConfig(broker_request_ledger_cfg);

   FP_Level28BrokerRequestAuditConfig broker_request_audit_cfg;
   FP_LoadLevel28BrokerRequestAuditConfig(broker_request_audit_cfg);

   FP_Level29PaperBrokerAdapterConfig paper_broker_adapter_cfg;
   FP_LoadLevel29PaperBrokerAdapterConfig(paper_broker_adapter_cfg);

   FP_Level30PaperBrokerLifecycleConfig paper_broker_lifecycle_cfg;
   FP_LoadLevel30PaperBrokerLifecycleConfig(paper_broker_lifecycle_cfg);

   FP_Consolidation01NoSendContextConfig no_send_context_cfg;
   FP_LoadConsolidation01NoSendContextConfig(no_send_context_cfg);

   FP_Consolidation02FinalDecisionConfig final_decision_cfg;
   FP_LoadConsolidation02FinalDecisionConfig(final_decision_cfg);

   FP_Consolidation04FinalCsvNormalizationConfig final_csv_normalization_cfg;
   FP_LoadConsolidation04FinalCsvNormalizationConfig(final_csv_normalization_cfg);

   FP_Consolidation05RuntimeHealthConfig runtime_health_cfg;
   FP_LoadConsolidation05RuntimeHealthConfig(runtime_health_cfg);

   FP_HookPhase01Config hook_phase01_cfg;
   FP_LoadHookPhase01Config(hook_phase01_cfg);

   FP_HookPhase02Config hook_phase02_cfg;
   FP_LoadHookPhase02Config(hook_phase02_cfg);

   FP_HookPhase03Config hook_phase03_cfg;
   FP_LoadHookPhase03Config(hook_phase03_cfg);

   FP_HookPhase04Config hook_phase04_cfg;
   FP_LoadHookPhase04Config(hook_phase04_cfg);

   FP_HookPhase05Config hook_phase05_cfg;
   FP_LoadHookPhase05Config(hook_phase05_cfg);

   FP_HookPhase06Config hook_phase06_cfg;
   FP_LoadHookPhase06Config(hook_phase06_cfg);

   FP_HookPhase07Config hook_phase07_cfg;
   FP_LoadHookPhase07Config(hook_phase07_cfg);

   if(hook_phase07_cfg.view_profile == FP_HOOK_P07_VIEW_SEQUENCE_CYCLE_DEBUG)
   {
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
      FP_CleanupAllNDSHookObjectsByInputPrefixes();
   }

   FP_HookPhase08Config hook_phase08_cfg;
   FP_LoadHookPhase08Config(hook_phase08_cfg);

   FP_HookPhase09Config hook_phase09_cfg;
   FP_LoadHookPhase09Config(hook_phase09_cfg);

   FP_HookPhase10Config hook_phase10_cfg;
   FP_LoadHookPhase10Config(hook_phase10_cfg);

   FP_HookPhase07Report hook_phase07_report;
   FP_ApplyHookPhase07Profile(hook_phase07_cfg,
                              hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg,
                              hook_phase04_cfg, hook_phase05_cfg, hook_phase06_cfg,
                              hook_phase07_report);

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
      if(InpPrintFailureSummaries)
         Print("FP_SUMMARY status=timebase_failed reason=", timebase_report.reason,
               " bars=", copied,
               " status_detail=", timebase_report.status);
      return;
   }

   if(copied < InpMinClosedBars)
   {
      if(InpPrintFailureSummaries)
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
      if(InpPrintFailureSummaries)
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

   FP_HookPhase01Report hook_phase01_report;
   FP_RunHookPhase01(_Symbol, _Period, rates, copied, scales, scale_count,
                     hook_phase01_cfg, hook_phase01_report);

   FP_HookPhase02Report hook_phase02_report;
   FP_RunHookPhase02(_Symbol, _Period, rates, copied, scales, scale_count,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase02_report);

   FP_HookPhase03Report hook_phase03_report;
   FP_RunHookPhase03(_Symbol, _Period, rates, copied, scales, scale_count,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg, hook_phase03_report);

   FP_HookPhase04Report hook_phase04_report;
   FP_RunHookPhase04(_Symbol, _Period, rates, copied, scales, scale_count,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg, hook_phase04_cfg, hook_phase04_report);

   FP_HookPhase05Report hook_phase05_report;
   FP_RunHookPhase05(_Symbol, _Period, rates, copied, scales, scale_count,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg, hook_phase04_cfg, hook_phase05_cfg, hook_phase05_report);

   FP_HookPhase06Report hook_phase06_report;
   FP_RunHookPhase06(_Symbol, _Period, rates, copied, scales, scale_count,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg, hook_phase04_cfg, hook_phase05_cfg, hook_phase06_cfg, hook_phase06_report);

   FP_HookPhase08Report hook_phase08_report;
   FP_RunHookPhase08(_Symbol, _Period,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg,
                     hook_phase04_cfg, hook_phase05_cfg, hook_phase06_cfg,
                     hook_phase07_cfg, hook_phase08_cfg,
                     hook_phase01_report, hook_phase02_report, hook_phase03_report,
                     hook_phase04_report, hook_phase05_report, hook_phase06_report,
                     hook_phase07_report, hook_phase08_report);


   FP_HookPhase09Report hook_phase09_report;
   FP_RunHookPhase09(_Symbol, _Period,
                     hook_phase01_cfg, hook_phase02_cfg, hook_phase03_cfg,
                     hook_phase04_cfg, hook_phase05_cfg, hook_phase06_cfg,
                     hook_phase07_cfg, hook_phase08_cfg, hook_phase09_cfg,
                     hook_phase01_report, hook_phase02_report, hook_phase03_report,
                     hook_phase04_report, hook_phase05_report, hook_phase06_report,
                     hook_phase07_report, hook_phase08_report, hook_phase09_report);

   FP_HookPhase10Report hook_phase10_report;
   FP_RunHookPhase10(_Symbol, _Period,
                     hook_phase07_cfg, hook_phase10_cfg,
                     hook_phase06_report, hook_phase08_report, hook_phase09_report,
                     hook_phase10_report);

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

   FP_Level19StateGateReport state_gate_report;
   FP_RunLevel19StateGate(_Symbol, _Period, rates, copied, scales, scale_count,
                          events, hooks, result, timebase_report,
                          export_report, render_report, validation_report,
                          state_gate_cfg, state_gate_report);
   if(state_gate_cfg.print_summary)
      FP_PrintLevel19StateGateReport("FP_LEVEL19", state_gate_report);

   FP_Level20EntryBridgeReport entry_bridge_report;
   FP_RunLevel20EntryBridge(_Symbol, _Period, rates, copied,
                            events, hooks, timebase_report,
                            render_report, validation_report,
                            entry_bridge_cfg, entry_bridge_report);
   if(entry_bridge_cfg.print_summary)
      FP_PrintLevel20EntryBridgeReport("FP_LEVEL20", entry_bridge_report);

   FP_Level21PaperIntentReport paper_intent_report;
   FP_RunLevel21PaperIntent(_Symbol, _Period, rates, copied,
                            events, hooks, timebase_report,
                            render_report, validation_report,
                            entry_bridge_cfg, paper_intent_cfg,
                            paper_intent_report);
   if(paper_intent_cfg.print_summary)
      FP_PrintLevel21PaperIntentReport("FP_LEVEL21", paper_intent_report);

   FP_Level22PaperLifecycleReport paper_lifecycle_report;
   FP_RunLevel22PaperLifecycle(_Symbol, _Period, rates, copied,
                               events, hooks, timebase_report,
                               render_report, validation_report,
                               entry_bridge_cfg, paper_intent_cfg,
                               paper_lifecycle_cfg,
                               paper_lifecycle_report);
   if(paper_lifecycle_cfg.print_summary)
      FP_PrintLevel22PaperLifecycleReport("FP_LEVEL22", paper_lifecycle_report);

   FP_Level23PaperPerformanceReport paper_performance_report;
   FP_RunLevel23PaperPerformance(_Symbol, _Period, rates, copied,
                                 events, hooks, timebase_report,
                                 render_report, validation_report,
                                 entry_bridge_cfg, paper_intent_cfg,
                                 paper_lifecycle_cfg, paper_performance_cfg,
                                 paper_performance_report);
   if(paper_performance_cfg.print_summary)
      FP_PrintLevel23PaperPerformanceReport("FP_LEVEL23", paper_performance_report);

   FP_Level24SafetyGateReport safety_gate_report;
   FP_RunLevel24SafetyGate(_Symbol, _Period, g_fp_license_ok,
                           safety_gate_cfg, safety_gate_report);
   if(safety_gate_cfg.print_summary)
      FP_PrintLevel24SafetyGateReport("FP_LEVEL24", safety_gate_report);

   FP_Level25BrokerDryRunReport broker_dry_run_report;
   FP_RunLevel25BrokerDryRun(_Symbol, _Period, rates, copied,
                             events, hooks, timebase_report,
                             render_report, validation_report,
                             g_fp_license_ok,
                             entry_bridge_cfg, paper_intent_cfg,
                             safety_gate_cfg, broker_dry_run_cfg,
                             broker_dry_run_report);
   if(broker_dry_run_cfg.print_summary)
      FP_PrintLevel25BrokerDryRunReport("FP_LEVEL25", broker_dry_run_report);

   FP_Level26BrokerValidatorReport broker_validator_report;
   FP_RunLevel26BrokerValidator(_Symbol, _Period, rates, copied,
                                events, hooks, timebase_report,
                                render_report, validation_report,
                                g_fp_license_ok,
                                entry_bridge_cfg, paper_intent_cfg,
                                safety_gate_cfg, broker_dry_run_cfg,
                                broker_validator_cfg,
                                broker_validator_report);
   if(broker_validator_cfg.print_summary)
      FP_PrintLevel26BrokerValidatorReport("FP_LEVEL26", broker_validator_report);

   FP_Level27BrokerRequestLedgerReport broker_request_ledger_report;
   FP_RunLevel27BrokerRequestLedger(_Symbol, _Period, rates, copied,
                                    events, hooks, timebase_report,
                                    render_report, validation_report,
                                    g_fp_license_ok,
                                    entry_bridge_cfg, paper_intent_cfg,
                                    safety_gate_cfg, broker_dry_run_cfg,
                                    broker_validator_cfg,
                                    broker_request_ledger_cfg,
                                    broker_request_ledger_report);
   if(broker_request_ledger_cfg.print_summary)
      FP_PrintLevel27BrokerRequestLedgerReport("FP_LEVEL27", broker_request_ledger_report);

   FP_Level28BrokerRequestAuditReport broker_request_audit_report;
   FP_RunLevel28BrokerRequestAudit(_Symbol, _Period, rates, copied,
                                   events, hooks, timebase_report,
                                   render_report, validation_report,
                                   g_fp_license_ok,
                                   entry_bridge_cfg, paper_intent_cfg,
                                   safety_gate_cfg, broker_dry_run_cfg,
                                   broker_validator_cfg,
                                   broker_request_audit_cfg,
                                   broker_request_audit_report);
   if(broker_request_audit_cfg.print_summary)
      FP_PrintLevel28BrokerRequestAuditReport("FP_LEVEL28", broker_request_audit_report);

   FP_Level29PaperBrokerAdapterReport paper_broker_adapter_report;
   FP_RunLevel29PaperBrokerAdapter(_Symbol, _Period, rates, copied,
                                   events, hooks, timebase_report,
                                   render_report, validation_report,
                                   g_fp_license_ok,
                                   entry_bridge_cfg, paper_intent_cfg,
                                   safety_gate_cfg, broker_dry_run_cfg,
                                   broker_validator_cfg,
                                   broker_request_audit_cfg,
                                   paper_broker_adapter_cfg,
                                   paper_broker_adapter_report);
   if(paper_broker_adapter_cfg.print_summary)
      FP_PrintLevel29PaperBrokerAdapterReport("FP_LEVEL29", paper_broker_adapter_report);

   FP_Level30PaperBrokerLifecycleReport paper_broker_lifecycle_report;
   FP_RunLevel30PaperBrokerLifecycle(_Symbol, _Period, rates, copied,
                                     events, hooks, timebase_report,
                                     render_report, validation_report,
                                     g_fp_license_ok,
                                     entry_bridge_cfg, paper_intent_cfg,
                                     safety_gate_cfg, broker_dry_run_cfg,
                                     broker_validator_cfg,
                                     broker_request_audit_cfg,
                                     paper_broker_adapter_cfg,
                                     paper_broker_lifecycle_cfg,
                                     paper_broker_lifecycle_report);
   if(paper_broker_lifecycle_cfg.print_summary)
      FP_PrintLevel30PaperBrokerLifecycleReport("FP_LEVEL30", paper_broker_lifecycle_report);

   FP_Consolidation01NoSendContextReport no_send_context_report;
   FP_RunConsolidation01NoSendContext(_Symbol, _Period,
                                      no_send_context_cfg,
                                      no_send_context_report);
   if(no_send_context_cfg.print_summary)
      FP_PrintConsolidation01NoSendContextReport("FP_CONSOLIDATION01", no_send_context_report);

   FP_Consolidation02FinalDecisionReport final_decision_report;
   FP_RunConsolidation02FinalDecision(_Symbol, _Period,
                                      no_send_context_cfg,
                                      final_decision_cfg,
                                      final_decision_report);
   if(final_decision_cfg.print_summary)
      FP_PrintConsolidation02FinalDecisionReport("FP_CONSOLIDATION02", final_decision_report);

   FP_Consolidation04FinalCsvNormalizationReport final_csv_normalization_report;
   FP_RunConsolidation04FinalCsvNormalization(_Symbol, _Period,
                                              no_send_context_cfg,
                                              final_decision_cfg,
                                              final_csv_normalization_cfg,
                                              final_csv_normalization_report);
   if(final_csv_normalization_cfg.print_summary)
      FP_PrintConsolidation04FinalCsvNormalizationReport("FP_CONSOLIDATION04", final_csv_normalization_report);

   FP_Consolidation05RuntimeHealthReport runtime_health_report;
   FP_RunConsolidation05RuntimeHealth(_Symbol, _Period,
                                      no_send_context_cfg,
                                      final_decision_cfg,
                                      final_csv_normalization_cfg,
                                      runtime_health_cfg,
                                      runtime_health_report);
   if(runtime_health_cfg.print_summary)
      FP_PrintConsolidation05RuntimeHealthReport("FP_CONSOLIDATION05", runtime_health_report);

   if(InpPrintFinalSummary)
      FP_PrintSummary(_Symbol, _Period, copied, scale_count, result, drawn);
   if(InpVerboseAuditLogs)
   {
      for(int i=0; i<ArraySize(events); i++) FP_PrintEventAudit(events[i]);
      for(int h=0; h<ArraySize(hooks); h++) FP_PrintHookAudit(hooks[h]);
   }
}


int FP_CleanupAllNDSHookObjectsByInputPrefixes()
{
   int deleted = 0;
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase07CommonHookObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase01ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase02ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase03ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase04ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase05ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase06ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase07ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase08ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase09ObjectPrefix);
   deleted += FP_HookP07DeleteObjectsByPrefix(InpHookPhase10ObjectPrefix);
   return deleted;
}

bool FP_ShouldCleanObjectsOnDeinitReason(const int reason)
{
   if(InpCleanObjectsOnDeinit)
      return true;

   if(reason == REASON_CHARTCHANGE && InpCleanObjectsOnChartChange)
      return true;
   if(reason == REASON_REMOVE && InpCleanObjectsOnRemove)
      return true;
   if(reason == REASON_RECOMPILE && InpCleanObjectsOnRecompile)
      return true;
   if(reason == REASON_PARAMETERS && InpCleanObjectsOnParameterChange)
      return true;
   if(reason == REASON_TEMPLATE && InpCleanObjectsOnTemplateApply)
      return true;

   return false;
}

void FP_CleanupChartObjectsForLifecycle(const int reason)
{
   if(FP_ShouldCleanObjectsOnDeinitReason(reason))
   {
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
      FP_CleanupAllNDSHookObjectsByInputPrefixes();
   }

   if(InpLevel19StateGatePanelEnabled && InpLevel19StateGatePanelCleanOnDeinit)
      FP_L19PanelCleanup(InpLevel19StateGateObjectPrefix);
}


int OnInit()
{
   if(!FP_EnsureOfflineLicense(true))
      return INIT_FAILED;
   EventSetTimer(60);

   FP_ReleaseConfig init_release_cfg;
   FP_LoadReleaseConfig(init_release_cfg);
   if(InpCleanObjectsOnInit || FP_ReleaseProfileWantsCleanup(init_release_cfg))
   {
      FP_DeleteObjectsByPrefix(InpObjectPrefix);
      FP_CleanupAllNDSHookObjectsByInputPrefixes();
   }
   if(InpLevel19StateGatePanelEnabled && InpLevel19StateGatePanelCleanOnInit)
      FP_L19PanelCleanup(InpLevel19StateGateObjectPrefix);
   g_fp_last_bar_time = 0;
   FP_Run();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   FP_CleanupChartObjectsForLifecycle(reason);
}

void OnTick()
{
   if(!FP_EnsureOfflineLicense(false))
      return;
   if(FP_ShouldRedraw())
      FP_Run();
}

void OnTimer()
{
   if(!FP_EnsureOfflineLicense(true))
      return;
}
