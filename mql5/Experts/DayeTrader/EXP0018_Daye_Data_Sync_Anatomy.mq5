
#property strict
#property version   "2.00"
#property description "EXP0018 P02 exact-timestamp multi-symbol data synchronization. No hunt, signal, drawing, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_DataEngine.mqh>
#include <AlphaLab/UC04/AL_UC04DayeTimeConfig.mqh>

input group "EXP0018 P02 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P02 — Base Bars"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpRequestedBarsPerSymbol = 2000;
input int InpMinimumCommonBars = 100;
input int InpMaximumPairsToPublish = 2000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteAlignment = false;

input group "EXP0018 P02 — Freshness and Refresh"
input bool InpEnforceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 2;

input group "EXP0018 P02 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P02 — Runtime Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintSymbolHealthOnRefresh = false;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P02 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input bool InpWriteLatestPairRows = true;
input string InpAuditCsvFilename = "EXP0018_Phase02_Data_Sync_Audit_v2.csv";

CDayeMultiSymbolDataEngine g_daye_data_engine;

void DAYE_BuildP02TimeConfig(DAYE_TimeConfig &config)
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

void DAYE_BuildP02DataConfig(DAYE_DataSyncConfig &config)
{
   ZeroMemory(config);
   config.schema_version = DAYE_DATA_SCHEMA_VERSION;
   config.broker_symbol_a = InpSymbolA;
   config.broker_symbol_b = InpSymbolB;
   config.canonical_symbol_a = InpCanonicalSymbolA;
   config.canonical_symbol_b = InpCanonicalSymbolB;
   config.base_timeframe = InpBaseTimeframe;
   config.requested_bars_per_symbol = InpRequestedBarsPerSymbol;
   config.minimum_common_bars = InpMinimumCommonBars;
   config.maximum_pairs_to_publish = InpMaximumPairsToPublish;
   config.use_closed_bars_only = InpUseClosedBarsOnly;
   config.require_series_synchronized = InpRequireSeriesSynchronized;
   config.fail_on_any_invalid_bar = InpFailOnAnyInvalidBar;
   config.require_complete_alignment = InpRequireCompleteAlignment;
   config.enforce_freshness = InpEnforceFreshness;
   config.maximum_latest_bar_age_seconds = InpMaximumLatestBarAgeSeconds;
   config.force_full_refresh_seconds = InpForceFullRefreshSeconds;
}

datetime DAYE_P02CurrentBrokerTime(void)
{
   datetime value = TimeTradeServer();
   if(value <= 0)
      value = TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config;
   DAYE_DataSyncConfig data_config;
   DAYE_BuildP02TimeConfig(time_config);
   DAYE_BuildP02DataConfig(data_config);

   if(!g_daye_data_engine.Initialize(data_config,
                                     time_config,
                                     InpRunEmbeddedSelfTestsOnInit,
                                     InpWriteAuditCsv,
                                     InpAuditCsvFilename))
      return INIT_FAILED;

   int timer_seconds = InpTimerSeconds;
   if(timer_seconds < 1)
      timer_seconds = 1;
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P02 EventSetTimer failed error=",GetLastError());
      g_daye_data_engine.Shutdown();
      return INIT_FAILED;
   }

   datetime now = DAYE_P02CurrentBrokerTime();
   if(now > 0)
      g_daye_data_engine.Process(now,
                                 InpPrintSummaryOnRefresh,
                                 InpPrintSymbolHealthOnRefresh,
                                 InpPrintTransitionEvents,
                                 InpShowChartComment,
                                 InpWriteSummaryRows,
                                 InpWriteLatestPairRows);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now = DAYE_P02CurrentBrokerTime();
   if(now > 0)
      g_daye_data_engine.Process(now,
                                 InpPrintSummaryOnRefresh,
                                 InpPrintSymbolHealthOnRefresh,
                                 InpPrintTransitionEvents,
                                 InpShowChartComment,
                                 InpWriteSummaryRows,
                                 InpWriteLatestPairRows);
}

void OnTick()
{
   // P02 is timer-driven and closed-bar oriented. It intentionally performs no market detection or trading work.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_data_engine.Shutdown();
}
