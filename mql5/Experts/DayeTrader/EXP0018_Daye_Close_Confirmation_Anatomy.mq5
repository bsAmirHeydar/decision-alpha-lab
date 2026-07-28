#property strict
#property version   "2.00"
#property description "EXP0018 P06 host-timeframe close confirmation over live P05 transitions. No lifecycle, drawing, direction, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_ConfirmationEngine.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

input group "EXP0018 P06 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P06 — Source Bars"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpRequestedBarsPerSymbol = 10000;
input int InpMinimumCommonBars = 500;
input int InpMaximumPairsToPublish = 10000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteSourceAlignment = false;

input group "EXP0018 P06 — Period Families"
input bool InpIncludeDailyPeriods = true;
input bool InpIncludeSessionPeriods = true;
input bool InpIncludeSubcyclePeriods = true;
input bool InpIncludeWeeklyPeriods = false;
input bool InpIncludeOpenPeriods = true;
input bool InpPublishPartialPeriods = true;
input int InpMinimumCompletePairedPeriods = 10;
input int InpMaximumPeriodsToPublish = 2000;

input group "EXP0018 P06 — Relationship Registry"
input bool InpEnableMajorRelationships = true;
input bool InpEnableMinorRelationships = true;
input bool InpAllowOpenCurrentPeriods = true;
input bool InpAllowPartialCurrentPeriods = false;
input bool InpRequireCompleteReferencePeriods = true;
input bool InpPublishUnavailableResolutions = true;
input bool InpPublishBlockedRegistryRecords = true;
input int InpMinimumReadyResolutions = 1;
input int InpMaximumResolutionsToPublish = 5000;

input group "EXP0018 P06 — Hunt Observation"
input bool InpEnableHighSide = true;
input bool InpEnableLowSide = true;
input bool InpEqualityCountsAsHunt = true;
input bool InpPublishUnavailableObservations = false;
input bool InpRequirePositivePrices = true;
input int InpMinimumReadyObservations = 1;
input int InpMaximumObservationsToPublish = 10000;

input group "EXP0018 P06 — Host Close Confirmation"
input ENUM_TIMEFRAMES InpHostTimeframe = PERIOD_CURRENT;
input bool InpRequireExactHostSymbolAlignment = true;
input bool InpRequireClosedHostBars = true;
input bool InpPublishNonconfirmedResults = true;
input bool InpFailClosedOnMissedHostClose = true;
input int InpMaximumPendingCandidates = 5000;
input int InpMaximumResultsToPublish = 10000;
input int InpMaximumFinalizedIdsToRemember = 20000;

input group "EXP0018 P06 — Restart Checkpoint"
input bool InpPersistCheckpoint = true;
input string InpCheckpointPrefix = "EXP0018_P06_Confirmation_State_v2";

input group "EXP0018 P06 — Refresh"
input bool InpEnforceSourceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 1;

input group "EXP0018 P06 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P06 — Runtime Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintLatestResult = true;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P06 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input int InpAuditLatestCandidateCount = 25;
input int InpAuditLatestResultCount = 25;
input string InpAuditCsvFilename = "EXP0018_Phase06_Confirmation_Audit_v2.csv";

CDayeConfirmationEngine g_daye_confirmation_engine;

void DAYE_BuildP06TimeConfig(DAYE_TimeConfig &config)
{
   AL_UC04BuildDayeTimeConfig(
      config,
      InpBrokerOffsetMode,
      InpBrokerUtcOffsetHours,
      InpNewYorkOffsetMode,
      InpManualNewYorkUtcOffsetHours,
      InpAmbiguousStartPolicy,
      InpAmbiguousEndPolicy
   );
}

void DAYE_BuildP06Config(DAYE_ConfirmationConfig &config)
{
   ZeroMemory(config);
   config.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   config.hunt_config.schema_version=DAYE_HUNT_SCHEMA_VERSION;
   config.hunt_config.relationship_config.schema_version=DAYE_RELATIONSHIP_SCHEMA_VERSION;

   config.hunt_config.relationship_config.period_config.schema_version=DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.hunt_config.relationship_config.period_config.data_config.schema_version=DAYE_DATA_SCHEMA_VERSION;
   config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a=InpSymbolA;
   config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b=InpSymbolB;
   config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a=InpCanonicalSymbolA;
   config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b=InpCanonicalSymbolB;
   config.hunt_config.relationship_config.period_config.data_config.base_timeframe=InpBaseTimeframe;
   config.hunt_config.relationship_config.period_config.data_config.requested_bars_per_symbol=InpRequestedBarsPerSymbol;
   config.hunt_config.relationship_config.period_config.data_config.minimum_common_bars=InpMinimumCommonBars;
   config.hunt_config.relationship_config.period_config.data_config.maximum_pairs_to_publish=InpMaximumPairsToPublish;
   config.hunt_config.relationship_config.period_config.data_config.use_closed_bars_only=InpUseClosedBarsOnly;
   config.hunt_config.relationship_config.period_config.data_config.require_series_synchronized=InpRequireSeriesSynchronized;
   config.hunt_config.relationship_config.period_config.data_config.fail_on_any_invalid_bar=InpFailOnAnyInvalidBar;
   config.hunt_config.relationship_config.period_config.data_config.require_complete_alignment=InpRequireCompleteSourceAlignment;
   config.hunt_config.relationship_config.period_config.data_config.enforce_freshness=InpEnforceSourceFreshness;
   config.hunt_config.relationship_config.period_config.data_config.maximum_latest_bar_age_seconds=InpMaximumLatestBarAgeSeconds;
   config.hunt_config.relationship_config.period_config.data_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.hunt_config.relationship_config.period_config.include_daily_periods=InpIncludeDailyPeriods;
   config.hunt_config.relationship_config.period_config.include_session_periods=InpIncludeSessionPeriods;
   config.hunt_config.relationship_config.period_config.include_subcycle_periods=InpIncludeSubcyclePeriods;
   config.hunt_config.relationship_config.period_config.include_weekly_periods=InpIncludeWeeklyPeriods;
   config.hunt_config.relationship_config.period_config.include_open_periods=InpIncludeOpenPeriods;
   config.hunt_config.relationship_config.period_config.publish_partial_periods=InpPublishPartialPeriods;
   config.hunt_config.relationship_config.period_config.require_both_symbols_complete=false;
   config.hunt_config.relationship_config.period_config.minimum_publishable_coverage_percent=0.0;
   config.hunt_config.relationship_config.period_config.minimum_complete_paired_periods=InpMinimumCompletePairedPeriods;
   config.hunt_config.relationship_config.period_config.maximum_periods_to_publish=InpMaximumPeriodsToPublish;
   config.hunt_config.relationship_config.period_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.hunt_config.relationship_config.enable_major_relationships=InpEnableMajorRelationships;
   config.hunt_config.relationship_config.enable_minor_relationships=InpEnableMinorRelationships;
   config.hunt_config.relationship_config.allow_open_current_periods=InpAllowOpenCurrentPeriods;
   config.hunt_config.relationship_config.allow_partial_current_periods=InpAllowPartialCurrentPeriods;
   config.hunt_config.relationship_config.require_complete_reference_periods=InpRequireCompleteReferencePeriods;
   config.hunt_config.relationship_config.publish_unavailable_resolutions=InpPublishUnavailableResolutions;
   config.hunt_config.relationship_config.publish_blocked_registry_records=InpPublishBlockedRegistryRecords;
   config.hunt_config.relationship_config.minimum_ready_resolutions=InpMinimumReadyResolutions;
   config.hunt_config.relationship_config.maximum_resolutions_to_publish=InpMaximumResolutionsToPublish;

   config.hunt_config.enable_high_side=InpEnableHighSide;
   config.hunt_config.enable_low_side=InpEnableLowSide;
   config.hunt_config.equality_counts_as_hunt=InpEqualityCountsAsHunt;
   config.hunt_config.publish_unavailable_observations=InpPublishUnavailableObservations;
   config.hunt_config.require_positive_prices=InpRequirePositivePrices;
   config.hunt_config.minimum_ready_observations=InpMinimumReadyObservations;
   config.hunt_config.maximum_observations_to_publish=InpMaximumObservationsToPublish;

   config.host_timeframe=InpHostTimeframe;
   config.require_exact_host_symbol_alignment=InpRequireExactHostSymbolAlignment;
   config.require_closed_host_bars=InpRequireClosedHostBars;
   config.persist_checkpoint=InpPersistCheckpoint;
   config.checkpoint_prefix=InpCheckpointPrefix;
   config.publish_nonconfirmed_results=InpPublishNonconfirmedResults;
   config.fail_closed_on_missed_host_close=InpFailClosedOnMissedHostClose;
   config.maximum_pending_candidates=InpMaximumPendingCandidates;
   config.maximum_results_to_publish=InpMaximumResultsToPublish;
   config.maximum_finalized_ids_to_remember=InpMaximumFinalizedIdsToRemember;
}

datetime DAYE_P06CurrentBrokerTime(void)
{
   datetime value=TimeTradeServer();
   if(value<=0) value=TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config;
   DAYE_ConfirmationConfig config;
   DAYE_BuildP06TimeConfig(time_config);
   DAYE_BuildP06Config(config);

   if(!g_daye_confirmation_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename))
      return INIT_FAILED;

   int timer_seconds=InpTimerSeconds;
   if(timer_seconds<1) timer_seconds=1;
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P06 EventSetTimer failed error=",GetLastError());
      g_daye_confirmation_engine.Shutdown();
      return INIT_FAILED;
   }

   datetime now=DAYE_P06CurrentBrokerTime();
   if(now>0)
      g_daye_confirmation_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestResult,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestCandidateCount,InpAuditLatestResultCount);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now=DAYE_P06CurrentBrokerTime();
   if(now>0)
      g_daye_confirmation_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestResult,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestCandidateCount,InpAuditLatestResultCount);
}

void OnTick()
{
   // P06 is timer-driven. It does not draw, map direction, retire references, size risk, or trade.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_confirmation_engine.Shutdown();
}
