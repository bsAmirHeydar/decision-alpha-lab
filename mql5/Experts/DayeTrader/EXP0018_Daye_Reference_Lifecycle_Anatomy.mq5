#property strict
#property version   "2.00"
#property description "EXP0018 P07 reference lifecycle and first-sweep state machine. No drawing, direction, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_LifecycleEngine.mqh>

input group "EXP0018 P07 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P07 — Source Bars"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpRequestedBarsPerSymbol = 10000;
input int InpMinimumCommonBars = 500;
input int InpMaximumPairsToPublish = 10000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteSourceAlignment = false;

input group "EXP0018 P07 — Period Families"
input bool InpIncludeDailyPeriods = true;
input bool InpIncludeSessionPeriods = true;
input bool InpIncludeSubcyclePeriods = true;
input bool InpIncludeWeeklyPeriods = false;
input bool InpIncludeOpenPeriods = true;
input bool InpPublishPartialPeriods = true;
input int InpMinimumCompletePairedPeriods = 10;
input int InpMaximumPeriodsToPublish = 2000;

input group "EXP0018 P07 — Relationship Registry"
input bool InpEnableMajorRelationships = true;
input bool InpEnableMinorRelationships = true;
input bool InpAllowOpenCurrentPeriods = true;
input bool InpAllowPartialCurrentPeriods = false;
input bool InpRequireCompleteReferencePeriods = true;
input bool InpPublishUnavailableResolutions = true;
input bool InpPublishBlockedRegistryRecords = true;
input int InpMinimumReadyResolutions = 1;
input int InpMaximumResolutionsToPublish = 5000;

input group "EXP0018 P07 — Hunt Observation"
input bool InpEnableHighSide = true;
input bool InpEnableLowSide = true;
input bool InpEqualityCountsAsHunt = true;
input bool InpPublishUnavailableObservations = false;
input bool InpRequirePositivePrices = true;
input int InpMinimumReadyObservations = 1;
input int InpMaximumObservationsToPublish = 10000;

input group "EXP0018 P07 — Host Close Confirmation"
input ENUM_TIMEFRAMES InpHostTimeframe = PERIOD_CURRENT;
input bool InpRequireExactHostSymbolAlignment = true;
input bool InpRequireClosedHostBars = true;
input bool InpPublishNonconfirmedResults = true;
input bool InpFailClosedOnMissedHostClose = true;
input int InpMaximumPendingCandidates = 5000;
input int InpMaximumResultsToPublish = 10000;
input int InpMaximumFinalizedIdsToRemember = 20000;
input bool InpPersistConfirmationCheckpoint = true;
input string InpConfirmationCheckpointPrefix = "EXP0018_P06_Confirmation_State_v2";

input group "EXP0018 P07 — Reference Lifecycle"
input bool InpAllowRepeatAcrossNewOpportunitiesWhileProtectedSurvives = true;
input bool InpSuppressDuplicateExactOpportunity = true;
input bool InpRetireOnProtectedTouch = true;
input bool InpRetireOnDoubleHunt = true;
input bool InpRetireOnRoleSwitch = true;
input bool InpPreserveAcceptedUsesAfterRetirement = true;
input bool InpPublishRejectedUses = true;
input int InpMaximumReferenceRecords = 10000;
input int InpMaximumUseRecords = 20000;
input int InpMaximumProcessedResultIds = 30000;

input group "EXP0018 P07 — Restart Checkpoint"
input bool InpPersistLifecycleCheckpoint = true;
input string InpLifecycleCheckpointPrefix = "EXP0018_P07_Lifecycle_State_v2";

input group "EXP0018 P07 — Refresh"
input bool InpEnforceSourceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 1;

input group "EXP0018 P07 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P07 — Runtime Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintLatestReference = true;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P07 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input int InpAuditLatestReferenceCount = 25;
input int InpAuditLatestUseCount = 25;
input string InpAuditCsvFilename = "EXP0018_Phase07_Lifecycle_Audit_v2.csv";

CDayeLifecycleEngine g_daye_lifecycle_engine;

void DAYE_BuildP07TimeConfig(DAYE_TimeConfig &config)
{
   config.schema_version=DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode=InpBrokerOffsetMode;
   config.broker_utc_offset_minutes=(int)MathRound(InpBrokerUtcOffsetHours*60.0);
   config.ny_offset_mode=InpNewYorkOffsetMode;
   config.manual_new_york_utc_offset_minutes=(int)MathRound(InpManualNewYorkUtcOffsetHours*60.0);
   config.ambiguous_start_policy=InpAmbiguousStartPolicy;
   config.ambiguous_end_policy=InpAmbiguousEndPolicy;
}

void DAYE_BuildP07Config(DAYE_LifecycleConfig &config)
{
   ZeroMemory(config); config.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   config.confirmation_config.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   config.confirmation_config.hunt_config.schema_version=DAYE_HUNT_SCHEMA_VERSION;
   config.confirmation_config.hunt_config.relationship_config.schema_version=DAYE_RELATIONSHIP_SCHEMA_VERSION;
   config.confirmation_config.hunt_config.relationship_config.period_config.schema_version=DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.schema_version=DAYE_DATA_SCHEMA_VERSION;

   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a=InpSymbolA;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b=InpSymbolB;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a=InpCanonicalSymbolA;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b=InpCanonicalSymbolB;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.base_timeframe=InpBaseTimeframe;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.requested_bars_per_symbol=InpRequestedBarsPerSymbol;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.minimum_common_bars=InpMinimumCommonBars;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.maximum_pairs_to_publish=InpMaximumPairsToPublish;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.use_closed_bars_only=InpUseClosedBarsOnly;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.require_series_synchronized=InpRequireSeriesSynchronized;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.fail_on_any_invalid_bar=InpFailOnAnyInvalidBar;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.require_complete_alignment=InpRequireCompleteSourceAlignment;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.enforce_freshness=InpEnforceSourceFreshness;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.maximum_latest_bar_age_seconds=InpMaximumLatestBarAgeSeconds;
   config.confirmation_config.hunt_config.relationship_config.period_config.data_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.confirmation_config.hunt_config.relationship_config.period_config.include_daily_periods=InpIncludeDailyPeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.include_session_periods=InpIncludeSessionPeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.include_subcycle_periods=InpIncludeSubcyclePeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.include_weekly_periods=InpIncludeWeeklyPeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.include_open_periods=InpIncludeOpenPeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.publish_partial_periods=InpPublishPartialPeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.require_both_symbols_complete=false;
   config.confirmation_config.hunt_config.relationship_config.period_config.minimum_publishable_coverage_percent=0.0;
   config.confirmation_config.hunt_config.relationship_config.period_config.minimum_complete_paired_periods=InpMinimumCompletePairedPeriods;
   config.confirmation_config.hunt_config.relationship_config.period_config.maximum_periods_to_publish=InpMaximumPeriodsToPublish;
   config.confirmation_config.hunt_config.relationship_config.period_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.confirmation_config.hunt_config.relationship_config.enable_major_relationships=InpEnableMajorRelationships;
   config.confirmation_config.hunt_config.relationship_config.enable_minor_relationships=InpEnableMinorRelationships;
   config.confirmation_config.hunt_config.relationship_config.allow_open_current_periods=InpAllowOpenCurrentPeriods;
   config.confirmation_config.hunt_config.relationship_config.allow_partial_current_periods=InpAllowPartialCurrentPeriods;
   config.confirmation_config.hunt_config.relationship_config.require_complete_reference_periods=InpRequireCompleteReferencePeriods;
   config.confirmation_config.hunt_config.relationship_config.publish_unavailable_resolutions=InpPublishUnavailableResolutions;
   config.confirmation_config.hunt_config.relationship_config.publish_blocked_registry_records=InpPublishBlockedRegistryRecords;
   config.confirmation_config.hunt_config.relationship_config.minimum_ready_resolutions=InpMinimumReadyResolutions;
   config.confirmation_config.hunt_config.relationship_config.maximum_resolutions_to_publish=InpMaximumResolutionsToPublish;

   config.confirmation_config.hunt_config.enable_high_side=InpEnableHighSide; config.confirmation_config.hunt_config.enable_low_side=InpEnableLowSide;
   config.confirmation_config.hunt_config.equality_counts_as_hunt=InpEqualityCountsAsHunt;
   config.confirmation_config.hunt_config.publish_unavailable_observations=InpPublishUnavailableObservations;
   config.confirmation_config.hunt_config.require_positive_prices=InpRequirePositivePrices;
   config.confirmation_config.hunt_config.minimum_ready_observations=InpMinimumReadyObservations;
   config.confirmation_config.hunt_config.maximum_observations_to_publish=InpMaximumObservationsToPublish;

   config.confirmation_config.host_timeframe=InpHostTimeframe; config.confirmation_config.require_exact_host_symbol_alignment=InpRequireExactHostSymbolAlignment;
   config.confirmation_config.require_closed_host_bars=InpRequireClosedHostBars; config.confirmation_config.persist_checkpoint=InpPersistConfirmationCheckpoint;
   config.confirmation_config.checkpoint_prefix=InpConfirmationCheckpointPrefix; config.confirmation_config.publish_nonconfirmed_results=InpPublishNonconfirmedResults;
   config.confirmation_config.fail_closed_on_missed_host_close=InpFailClosedOnMissedHostClose;
   config.confirmation_config.maximum_pending_candidates=InpMaximumPendingCandidates; config.confirmation_config.maximum_results_to_publish=InpMaximumResultsToPublish;
   config.confirmation_config.maximum_finalized_ids_to_remember=InpMaximumFinalizedIdsToRemember;

   config.allow_repeat_across_new_opportunities_while_protected_survives=InpAllowRepeatAcrossNewOpportunitiesWhileProtectedSurvives;
   config.suppress_duplicate_exact_opportunity=InpSuppressDuplicateExactOpportunity;
   config.retire_on_protected_touch=InpRetireOnProtectedTouch; config.retire_on_double_hunt=InpRetireOnDoubleHunt;
   config.retire_on_role_switch=InpRetireOnRoleSwitch; config.preserve_accepted_uses_after_retirement=InpPreserveAcceptedUsesAfterRetirement;
   config.publish_rejected_uses=InpPublishRejectedUses; config.persist_checkpoint=InpPersistLifecycleCheckpoint;
   config.checkpoint_prefix=InpLifecycleCheckpointPrefix; config.maximum_reference_records=InpMaximumReferenceRecords;
   config.maximum_use_records=InpMaximumUseRecords; config.maximum_processed_result_ids=InpMaximumProcessedResultIds;
}

datetime DAYE_P07CurrentBrokerTime(void)
{
   datetime value=TimeTradeServer(); if(value<=0) value=TimeCurrent(); return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config; DAYE_LifecycleConfig config;
   DAYE_BuildP07TimeConfig(time_config); DAYE_BuildP07Config(config);
   if(!g_daye_lifecycle_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename)) return INIT_FAILED;
   int timer_seconds=InpTimerSeconds; if(timer_seconds<1) timer_seconds=1;
   if(!EventSetTimer(timer_seconds)) { Print("EXP0018 P07 EventSetTimer failed error=",GetLastError()); g_daye_lifecycle_engine.Shutdown(); return INIT_FAILED; }
   datetime now=DAYE_P07CurrentBrokerTime();
   if(now>0) g_daye_lifecycle_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestReference,InpPrintTransitionEvents,
                                             InpShowChartComment,InpWriteSummaryRows,InpAuditLatestReferenceCount,InpAuditLatestUseCount);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now=DAYE_P07CurrentBrokerTime();
   if(now>0) g_daye_lifecycle_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestReference,InpPrintTransitionEvents,
                                             InpShowChartComment,InpWriteSummaryRows,InpAuditLatestReferenceCount,InpAuditLatestUseCount);
}

void OnTick()
{
   // P07 is timer-driven. It owns lifecycle only and does not draw, map direction, size risk, or trade.
}

void OnDeinit(const int reason)
{
   EventKillTimer(); g_daye_lifecycle_engine.Shutdown();
}
