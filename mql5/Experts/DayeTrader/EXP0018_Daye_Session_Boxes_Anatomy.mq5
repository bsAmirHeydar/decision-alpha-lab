#property strict
#property version   "2.00"
#property description "EXP0018 P09 A/L/N/P session boxes from symbol-local P03 ranges. No signal, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_SessionBoxEngine.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

input group "EXP0018 P09 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P09 — Source History"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpLookbackWeeks = 2;
input int InpRequestedBarsPerSymbol = 30000;
input int InpMinimumCommonBars = 500;
input int InpMaximumPairsToPublish = 30000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteSourceAlignment = false;
input bool InpPublishPartialSourcePeriods = true;
input int InpMaximumSourcePeriods = 4000;

input group "EXP0018 P09 — Session Admission"
input bool InpRenderSessionA = true;
input bool InpRenderSessionL = true;
input bool InpRenderSessionN = true;
input bool InpRenderSessionP = true;
input bool InpRenderCompleteSessions = true;
input bool InpRenderOpenSessions = true;
input bool InpRenderPartialSessions = false;
input bool InpRequireSymbolPeriodPublishable = false;

input group "EXP0018 P09 — Chart Targets"
input DAYE_SessionBoxTargetPolicy InpTargetPolicy = DAYE_SESSION_BOX_TARGET_ALL_OPEN_SYMBOL_CHARTS;
input bool InpOpenMissingSymbolChart = false;
input ENUM_TIMEFRAMES InpOpenedChartTimeframe = PERIOD_M15;
input int InpMaximumTargetChartsPerSymbol = 8;

input group "EXP0018 P09 — Session Colors"
input color InpAColor = clrSkyBlue;
input color InpLColor = clrLime;
input color InpNColor = clrOrange;
input color InpPColor = C'255,128,128';
input int InpFillAlpha = 45;
input ENUM_LINE_STYLE InpBorderStyle = STYLE_SOLID;
input int InpBorderWidth = 1;
input bool InpDrawInBackground = true;
input bool InpSelectable = false;
input bool InpHiddenInObjectList = false;

input group "EXP0018 P09 — Ownership and Repair"
input bool InpVerifyExistingOwnedObjects = true;
input bool InpRepairExistingOwnedObjects = true;
input bool InpRecreateManuallyDeletedOwnedObjects = true;
input bool InpDeleteOwnedObjectsOutsideLookback = true;
input bool InpDeleteOwnedObjectsOnDeinit = false;
input int InpObjectVerificationIntervalSeconds = 10;
input int InpMaximumProjectionRecords = 20000;

input group "EXP0018 P09 — Refresh"
input bool InpEnforceSourceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 2;

input group "EXP0018 P09 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P09 — Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintTransitionEvents = false;
input bool InpShowChartComment = false;

input group "EXP0018 P09 — Optional Audit"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input string InpAuditCsvFilename = "EXP0018_Phase09_Session_Boxes_Audit_v2.csv";

CDayeSessionBoxEngine g_daye_session_box_engine;

void DAYE_BuildP09TimeConfig(DAYE_TimeConfig &config)
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

void DAYE_BuildP09Config(DAYE_SessionBoxConfig &config)
{
   ZeroMemory(config);
   config.schema_version=DAYE_SESSION_BOX_SCHEMA_VERSION;
   config.period_config.schema_version=DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.period_config.data_config.schema_version=DAYE_DATA_SCHEMA_VERSION;
   config.period_config.data_config.broker_symbol_a=InpSymbolA;
   config.period_config.data_config.broker_symbol_b=InpSymbolB;
   config.period_config.data_config.canonical_symbol_a=InpCanonicalSymbolA;
   config.period_config.data_config.canonical_symbol_b=InpCanonicalSymbolB;
   config.period_config.data_config.base_timeframe=InpBaseTimeframe;
   config.period_config.data_config.requested_bars_per_symbol=InpRequestedBarsPerSymbol;
   config.period_config.data_config.minimum_common_bars=InpMinimumCommonBars;
   config.period_config.data_config.maximum_pairs_to_publish=InpMaximumPairsToPublish;
   config.period_config.data_config.use_closed_bars_only=InpUseClosedBarsOnly;
   config.period_config.data_config.require_series_synchronized=InpRequireSeriesSynchronized;
   config.period_config.data_config.fail_on_any_invalid_bar=InpFailOnAnyInvalidBar;
   config.period_config.data_config.require_complete_alignment=InpRequireCompleteSourceAlignment;
   config.period_config.data_config.enforce_freshness=InpEnforceSourceFreshness;
   config.period_config.data_config.maximum_latest_bar_age_seconds=InpMaximumLatestBarAgeSeconds;
   config.period_config.data_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;
   config.period_config.include_daily_periods=false;
   config.period_config.include_session_periods=true;
   config.period_config.include_subcycle_periods=false;
   config.period_config.include_weekly_periods=false;
   config.period_config.include_open_periods=InpRenderOpenSessions;
   config.period_config.publish_partial_periods=InpPublishPartialSourcePeriods;
   config.period_config.require_both_symbols_complete=false;
   config.period_config.minimum_publishable_coverage_percent=0.0;
   config.period_config.minimum_complete_paired_periods=1;
   config.period_config.maximum_periods_to_publish=InpMaximumSourcePeriods;
   config.period_config.force_full_refresh_seconds=InpForceFullRefreshSeconds;

   config.target_policy=InpTargetPolicy;
   config.lookback_weeks=InpLookbackWeeks;
   config.render_session_a=InpRenderSessionA;
   config.render_session_l=InpRenderSessionL;
   config.render_session_n=InpRenderSessionN;
   config.render_session_p=InpRenderSessionP;
   config.render_complete_sessions=InpRenderCompleteSessions;
   config.render_open_sessions=InpRenderOpenSessions;
   config.render_partial_sessions=InpRenderPartialSessions;
   config.require_symbol_period_publishable=InpRequireSymbolPeriodPublishable;
   config.open_missing_symbol_chart=InpOpenMissingSymbolChart;
   config.opened_chart_timeframe=InpOpenedChartTimeframe;
   config.maximum_target_charts_per_symbol=InpMaximumTargetChartsPerSymbol;
   config.color_a=InpAColor;
   config.color_l=InpLColor;
   config.color_n=InpNColor;
   config.color_p=InpPColor;
   config.fill_alpha=InpFillAlpha;
   config.border_style=InpBorderStyle;
   config.border_width=InpBorderWidth;
   config.draw_in_background=InpDrawInBackground;
   config.selectable=InpSelectable;
   config.hidden=InpHiddenInObjectList;
   config.verify_existing_owned_objects=InpVerifyExistingOwnedObjects;
   config.repair_existing_owned_objects=InpRepairExistingOwnedObjects;
   config.recreate_manually_deleted_owned_objects=InpRecreateManuallyDeletedOwnedObjects;
   config.delete_owned_objects_outside_lookback=InpDeleteOwnedObjectsOutsideLookback;
   config.delete_owned_objects_on_deinit=InpDeleteOwnedObjectsOnDeinit;
   config.object_verification_interval_seconds=InpObjectVerificationIntervalSeconds;
   config.maximum_projection_records=InpMaximumProjectionRecords;
}

datetime DAYE_P09CurrentBrokerTime(void)
{
   datetime value=TimeTradeServer();
   if(value<=0) value=TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config;
   DAYE_SessionBoxConfig config;
   DAYE_BuildP09TimeConfig(time_config);
   DAYE_BuildP09Config(config);
   if(!g_daye_session_box_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename))
      return INIT_FAILED;
   int seconds=InpTimerSeconds; if(seconds<1) seconds=1;
   if(!EventSetTimer(seconds))
   {
      Print("EXP0018 P09 EventSetTimer failed error=",GetLastError());
      g_daye_session_box_engine.Shutdown();
      return INIT_FAILED;
   }
   datetime now=DAYE_P09CurrentBrokerTime();
   if(now>0) g_daye_session_box_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now=DAYE_P09CurrentBrokerTime();
   if(now>0) g_daye_session_box_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows);
}

void OnTick()
{
   // Timer-driven session-range projection only.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_session_box_engine.Shutdown();
}
