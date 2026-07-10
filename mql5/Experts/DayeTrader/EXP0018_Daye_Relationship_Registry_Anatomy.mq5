#property strict
#property version   "2.00"
#property description "EXP0018 P04 declarative 22-relationship registry and period-context resolver. No hunt, signal, drawing, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_RelationshipEngine.mqh>

input group "EXP0018 P04 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P04 — Source Bars"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpRequestedBarsPerSymbol = 10000;
input int InpMinimumCommonBars = 500;
input int InpMaximumPairsToPublish = 10000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteSourceAlignment = false;

input group "EXP0018 P04 — Period Families"
input bool InpIncludeDailyPeriods = true;
input bool InpIncludeSessionPeriods = true;
input bool InpIncludeSubcyclePeriods = true;
input bool InpIncludeWeeklyPeriods = false;
input bool InpIncludeOpenPeriods = true;
input bool InpPublishPartialPeriods = true;
input int InpMinimumCompletePairedPeriods = 10;
input int InpMaximumPeriodsToPublish = 2000;

input group "EXP0018 P04 — Relationship Registry"
input bool InpEnableMajorRelationships = true;
input bool InpEnableMinorRelationships = true;
input bool InpAllowOpenCurrentPeriods = true;
input bool InpAllowPartialCurrentPeriods = false;
input bool InpRequireCompleteReferencePeriods = true;
input bool InpPublishUnavailableResolutions = true;
input bool InpPublishBlockedRegistryRecords = true;
input int InpMinimumReadyResolutions = 1;
input int InpMaximumResolutionsToPublish = 5000;

input group "EXP0018 P04 — Refresh"
input bool InpEnforceSourceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 2;

input group "EXP0018 P04 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P04 — Runtime Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintLatestReadyResolution = true;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P04 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input int InpAuditLatestResolutionCount = 25;
input string InpAuditCsvFilename = "EXP0018_Phase04_Relationship_Audit_v2.csv";

CDayeRelationshipEngine g_daye_relationship_engine;

void DAYE_BuildP04TimeConfig(DAYE_TimeConfig &config)
{
   config.schema_version = DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode = InpBrokerOffsetMode;
   config.broker_utc_offset_minutes = (int)MathRound(InpBrokerUtcOffsetHours * 60.0);
   config.ny_offset_mode = InpNewYorkOffsetMode;
   config.manual_new_york_utc_offset_minutes = (int)MathRound(InpManualNewYorkUtcOffsetHours * 60.0);
   config.ambiguous_start_policy = InpAmbiguousStartPolicy;
   config.ambiguous_end_policy = InpAmbiguousEndPolicy;
}

void DAYE_BuildP04Config(DAYE_RelationshipConfig &config)
{
   ZeroMemory(config);
   config.schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;

   config.period_config.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.period_config.data_config.schema_version = DAYE_DATA_SCHEMA_VERSION;
   config.period_config.data_config.broker_symbol_a = InpSymbolA;
   config.period_config.data_config.broker_symbol_b = InpSymbolB;
   config.period_config.data_config.canonical_symbol_a = InpCanonicalSymbolA;
   config.period_config.data_config.canonical_symbol_b = InpCanonicalSymbolB;
   config.period_config.data_config.base_timeframe = InpBaseTimeframe;
   config.period_config.data_config.requested_bars_per_symbol = InpRequestedBarsPerSymbol;
   config.period_config.data_config.minimum_common_bars = InpMinimumCommonBars;
   config.period_config.data_config.maximum_pairs_to_publish = InpMaximumPairsToPublish;
   config.period_config.data_config.use_closed_bars_only = InpUseClosedBarsOnly;
   config.period_config.data_config.require_series_synchronized = InpRequireSeriesSynchronized;
   config.period_config.data_config.fail_on_any_invalid_bar = InpFailOnAnyInvalidBar;
   config.period_config.data_config.require_complete_alignment = InpRequireCompleteSourceAlignment;
   config.period_config.data_config.enforce_freshness = InpEnforceSourceFreshness;
   config.period_config.data_config.maximum_latest_bar_age_seconds = InpMaximumLatestBarAgeSeconds;
   config.period_config.data_config.force_full_refresh_seconds = InpForceFullRefreshSeconds;

   config.period_config.include_daily_periods = InpIncludeDailyPeriods;
   config.period_config.include_session_periods = InpIncludeSessionPeriods;
   config.period_config.include_subcycle_periods = InpIncludeSubcyclePeriods;
   config.period_config.include_weekly_periods = InpIncludeWeeklyPeriods;
   config.period_config.include_open_periods = InpIncludeOpenPeriods;
   config.period_config.publish_partial_periods = InpPublishPartialPeriods;
   config.period_config.require_both_symbols_complete = false;
   config.period_config.minimum_publishable_coverage_percent = 0.0;
   config.period_config.minimum_complete_paired_periods = InpMinimumCompletePairedPeriods;
   config.period_config.maximum_periods_to_publish = InpMaximumPeriodsToPublish;
   config.period_config.force_full_refresh_seconds = InpForceFullRefreshSeconds;

   config.enable_major_relationships = InpEnableMajorRelationships;
   config.enable_minor_relationships = InpEnableMinorRelationships;
   config.allow_open_current_periods = InpAllowOpenCurrentPeriods;
   config.allow_partial_current_periods = InpAllowPartialCurrentPeriods;
   config.require_complete_reference_periods = InpRequireCompleteReferencePeriods;
   config.publish_unavailable_resolutions = InpPublishUnavailableResolutions;
   config.publish_blocked_registry_records = InpPublishBlockedRegistryRecords;
   config.minimum_ready_resolutions = InpMinimumReadyResolutions;
   config.maximum_resolutions_to_publish = InpMaximumResolutionsToPublish;
}

datetime DAYE_P04CurrentBrokerTime(void)
{
   datetime value = TimeTradeServer();
   if(value <= 0) value = TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config;
   DAYE_RelationshipConfig config;
   DAYE_BuildP04TimeConfig(time_config);
   DAYE_BuildP04Config(config);

   if(!g_daye_relationship_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename))
      return INIT_FAILED;

   int timer_seconds = InpTimerSeconds;
   if(timer_seconds < 1) timer_seconds = 1;
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P04 EventSetTimer failed error=",GetLastError());
      g_daye_relationship_engine.Shutdown();
      return INIT_FAILED;
   }

   datetime now = DAYE_P04CurrentBrokerTime();
   if(now > 0)
      g_daye_relationship_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestReadyResolution,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestResolutionCount);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now = DAYE_P04CurrentBrokerTime();
   if(now > 0)
      g_daye_relationship_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestReadyResolution,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestResolutionCount);
}

void OnTick()
{
   // P04 is timer-driven and topology-only. It performs no hunt, SMT, drawing, or trading work.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_relationship_engine.Shutdown();
}
