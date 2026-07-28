#property strict
#property version   "2.00"
#property description "EXP0018 P05 touch-only HIGH/LOW hunt observation over P04 relationship contexts. No direction, confirmation, drawing, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_HuntEngine.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

input group "EXP0018 P05 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P05 — Source Bars"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpRequestedBarsPerSymbol = 10000;
input int InpMinimumCommonBars = 500;
input int InpMaximumPairsToPublish = 10000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteSourceAlignment = false;

input group "EXP0018 P05 — Period Families"
input bool InpIncludeDailyPeriods = true;
input bool InpIncludeSessionPeriods = true;
input bool InpIncludeSubcyclePeriods = true;
input bool InpIncludeWeeklyPeriods = false;
input bool InpIncludeOpenPeriods = true;
input bool InpPublishPartialPeriods = true;
input int InpMinimumCompletePairedPeriods = 10;
input int InpMaximumPeriodsToPublish = 2000;

input group "EXP0018 P05 — Relationship Registry"
input bool InpEnableMajorRelationships = true;
input bool InpEnableMinorRelationships = true;
input bool InpAllowOpenCurrentPeriods = true;
input bool InpAllowPartialCurrentPeriods = false;
input bool InpRequireCompleteReferencePeriods = true;
input bool InpPublishUnavailableResolutions = true;
input bool InpPublishBlockedRegistryRecords = true;
input int InpMinimumReadyResolutions = 1;
input int InpMaximumResolutionsToPublish = 5000;

input group "EXP0018 P05 — Hunt Observation"
input bool InpEnableHighSide = true;
input bool InpEnableLowSide = true;
input bool InpEqualityCountsAsHunt = true;
input bool InpPublishUnavailableObservations = false;
input bool InpRequirePositivePrices = true;
input int InpMinimumReadyObservations = 1;
input int InpMaximumObservationsToPublish = 10000;

input group "EXP0018 P05 — Refresh"
input bool InpEnforceSourceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 2;

input group "EXP0018 P05 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P05 — Runtime Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintLatestOneSidedObservation = true;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P05 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input int InpAuditLatestObservationCount = 25;
input string InpAuditCsvFilename = "EXP0018_Phase05_Hunt_Audit_v2.csv";

CDayeHuntEngine g_daye_hunt_engine;

void DAYE_BuildP05TimeConfig(DAYE_TimeConfig &config)
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

void DAYE_BuildP05Config(DAYE_HuntConfig &config)
{
   ZeroMemory(config);
   config.schema_version = DAYE_HUNT_SCHEMA_VERSION;
   config.relationship_config.schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;

   config.relationship_config.period_config.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.relationship_config.period_config.data_config.schema_version = DAYE_DATA_SCHEMA_VERSION;
   config.relationship_config.period_config.data_config.broker_symbol_a = InpSymbolA;
   config.relationship_config.period_config.data_config.broker_symbol_b = InpSymbolB;
   config.relationship_config.period_config.data_config.canonical_symbol_a = InpCanonicalSymbolA;
   config.relationship_config.period_config.data_config.canonical_symbol_b = InpCanonicalSymbolB;
   config.relationship_config.period_config.data_config.base_timeframe = InpBaseTimeframe;
   config.relationship_config.period_config.data_config.requested_bars_per_symbol = InpRequestedBarsPerSymbol;
   config.relationship_config.period_config.data_config.minimum_common_bars = InpMinimumCommonBars;
   config.relationship_config.period_config.data_config.maximum_pairs_to_publish = InpMaximumPairsToPublish;
   config.relationship_config.period_config.data_config.use_closed_bars_only = InpUseClosedBarsOnly;
   config.relationship_config.period_config.data_config.require_series_synchronized = InpRequireSeriesSynchronized;
   config.relationship_config.period_config.data_config.fail_on_any_invalid_bar = InpFailOnAnyInvalidBar;
   config.relationship_config.period_config.data_config.require_complete_alignment = InpRequireCompleteSourceAlignment;
   config.relationship_config.period_config.data_config.enforce_freshness = InpEnforceSourceFreshness;
   config.relationship_config.period_config.data_config.maximum_latest_bar_age_seconds = InpMaximumLatestBarAgeSeconds;
   config.relationship_config.period_config.data_config.force_full_refresh_seconds = InpForceFullRefreshSeconds;

   config.relationship_config.period_config.include_daily_periods = InpIncludeDailyPeriods;
   config.relationship_config.period_config.include_session_periods = InpIncludeSessionPeriods;
   config.relationship_config.period_config.include_subcycle_periods = InpIncludeSubcyclePeriods;
   config.relationship_config.period_config.include_weekly_periods = InpIncludeWeeklyPeriods;
   config.relationship_config.period_config.include_open_periods = InpIncludeOpenPeriods;
   config.relationship_config.period_config.publish_partial_periods = InpPublishPartialPeriods;
   config.relationship_config.period_config.require_both_symbols_complete = false;
   config.relationship_config.period_config.minimum_publishable_coverage_percent = 0.0;
   config.relationship_config.period_config.minimum_complete_paired_periods = InpMinimumCompletePairedPeriods;
   config.relationship_config.period_config.maximum_periods_to_publish = InpMaximumPeriodsToPublish;
   config.relationship_config.period_config.force_full_refresh_seconds = InpForceFullRefreshSeconds;

   config.relationship_config.enable_major_relationships = InpEnableMajorRelationships;
   config.relationship_config.enable_minor_relationships = InpEnableMinorRelationships;
   config.relationship_config.allow_open_current_periods = InpAllowOpenCurrentPeriods;
   config.relationship_config.allow_partial_current_periods = InpAllowPartialCurrentPeriods;
   config.relationship_config.require_complete_reference_periods = InpRequireCompleteReferencePeriods;
   config.relationship_config.publish_unavailable_resolutions = InpPublishUnavailableResolutions;
   config.relationship_config.publish_blocked_registry_records = InpPublishBlockedRegistryRecords;
   config.relationship_config.minimum_ready_resolutions = InpMinimumReadyResolutions;
   config.relationship_config.maximum_resolutions_to_publish = InpMaximumResolutionsToPublish;

   config.enable_high_side = InpEnableHighSide;
   config.enable_low_side = InpEnableLowSide;
   config.equality_counts_as_hunt = InpEqualityCountsAsHunt;
   config.publish_unavailable_observations = InpPublishUnavailableObservations;
   config.require_positive_prices = InpRequirePositivePrices;
   config.minimum_ready_observations = InpMinimumReadyObservations;
   config.maximum_observations_to_publish = InpMaximumObservationsToPublish;
}

datetime DAYE_P05CurrentBrokerTime(void)
{
   datetime value = TimeTradeServer();
   if(value <= 0) value = TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config;
   DAYE_HuntConfig config;
   DAYE_BuildP05TimeConfig(time_config);
   DAYE_BuildP05Config(config);

   if(!g_daye_hunt_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename))
      return INIT_FAILED;

   int timer_seconds=InpTimerSeconds;
   if(timer_seconds < 1) timer_seconds=1;
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P05 EventSetTimer failed error=",GetLastError());
      g_daye_hunt_engine.Shutdown();
      return INIT_FAILED;
   }

   datetime now=DAYE_P05CurrentBrokerTime();
   if(now > 0)
      g_daye_hunt_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestOneSidedObservation,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestObservationCount);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now=DAYE_P05CurrentBrokerTime();
   if(now > 0)
      g_daye_hunt_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestOneSidedObservation,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestObservationCount);
}

void OnTick()
{
   // P05 is timer-driven and fact-only. It performs no direction mapping, close confirmation, drawing, or trading work.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_hunt_engine.Shutdown();
}
