#property strict
#property version   "1.00"
#property description "Decision Alpha Lab - EXP0015 candle/session intermarket divergence engine"

#include <IntermarketDivergence/DAL_IMDTypes.mqh>
#include <IntermarketDivergence/DAL_IMDSeries.mqh>
#include <IntermarketDivergence/DAL_IMDEngine.mqh>
#include <IntermarketDivergence/DAL_IMDJournal.mqh>

input IMD_RunMode InpRunMode = IMD_RUN_BACKTEST_BATCH;
input IMD_DataSource InpDataSource = IMD_DS_BROKER_SERIES;
input string InpRunId = "EXP0015_IMD001";
input string InpPairLabel = "ES_NQ";
input string InpSymbolA = "ES";
input string InpSymbolB = "NQ";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M1;
input int InpMaxBars = 50000;
input string InpCsvACommon = "dal/cme/ES_M1.csv";
input string InpCsvBCommon = "dal/cme/NQ_M1.csv";

input bool InpScanAAsOrigin = true;
input bool InpScanBAsOrigin = true;
input IMD_LevelFamily InpLevelFamily = IMD_LEVEL_CURRENT_SESSION;
input IMD_TriggerMode InpTriggerMode = IMD_TRIGGER_WICK_TOUCH;
input int InpRollingLookback = 20;
input int InpStepEveryBars = 1;
input int InpStepOffsetBars = 0;
input int InpDestinationLagBars = 2;
input int InpSignalValidBars = 12;
input int InpStartAfterBars = 100;
input int InpOutcomeHorizonBars = 12;

// Session is expressed in the timestamp timezone of the loaded bars.
// For CME RTH in New York timestamps: 09:30 -> 16:00 = 570 -> 960.
input int InpSessionStartMinute = 570;
input int InpSessionEndMinute = 960;

input string InpOutputEventsCommon = "imd/EXP0015/imd001_divergence_events.csv";
input string InpOutputSummaryCommon = "imd/EXP0015/imd001_summary.csv";
input int InpLiveTimerSeconds = 10;
input bool InpRemoveAfterBatch = true;

IMD_Bar g_a_raw[];
IMD_Bar g_b_raw[];
IMD_Bar g_a[];
IMD_Bar g_b[];
IMD_Event g_events[];
datetime g_last_run_time = 0;

bool IMD_LoadInputs()
{
   ArrayResize(g_a_raw, 0);
   ArrayResize(g_b_raw, 0);
   ArrayResize(g_a, 0);
   ArrayResize(g_b, 0);

   bool ok_a=false, ok_b=false;
   if(InpDataSource == IMD_DS_BROKER_SERIES)
   {
      ok_a = IMD_LoadBrokerBars(InpSymbolA, InpTimeframe, InpMaxBars, g_a_raw);
      ok_b = IMD_LoadBrokerBars(InpSymbolB, InpTimeframe, InpMaxBars, g_b_raw);
   }
   else
   {
      ok_a = IMD_LoadCsvBarsCommon(InpCsvACommon, InpMaxBars, g_a_raw);
      ok_b = IMD_LoadCsvBarsCommon(InpCsvBCommon, InpMaxBars, g_b_raw);
   }

   if(!ok_a || !ok_b)
   {
      Print("IMD001: input load failed ok_a=", ok_a, " ok_b=", ok_b);
      return false;
   }

   int aligned = IMD_AlignByTime(g_a_raw, g_b_raw, g_a, g_b);
   if(aligned <= 10)
   {
      Print("IMD001: too few aligned bars: ", aligned);
      return false;
   }
   Print("IMD001: loaded aligned bars=", aligned, " A=", InpSymbolA, " B=", InpSymbolB);
   return true;
}

void IMD_RunEngine()
{
   if(!IMD_LoadInputs()) return;

   ArrayResize(g_events, 0);
   if(InpScanAAsOrigin)
   {
      int added = IMD_DetectOriginDestination(InpPairLabel, InpSymbolA, InpSymbolB, g_a, g_b,
                                              InpLevelFamily, InpTriggerMode, InpRollingLookback,
                                              InpSessionStartMinute, InpSessionEndMinute,
                                              InpStepEveryBars, InpStepOffsetBars, InpDestinationLagBars,
                                              InpSignalValidBars, InpStartAfterBars, InpOutcomeHorizonBars,
                                              g_events);
      Print("IMD001: A as origin events=", added);
   }
   if(InpScanBAsOrigin)
   {
      int added = IMD_DetectOriginDestination(InpPairLabel, InpSymbolB, InpSymbolA, g_b, g_a,
                                              InpLevelFamily, InpTriggerMode, InpRollingLookback,
                                              InpSessionStartMinute, InpSessionEndMinute,
                                              InpStepEveryBars, InpStepOffsetBars, InpDestinationLagBars,
                                              InpSignalValidBars, InpStartAfterBars, InpOutcomeHorizonBars,
                                              g_events);
      Print("IMD001: B as origin events=", added);
   }

   IMD_WriteEventsCsv(InpOutputEventsCommon, g_events);
   IMD_WriteSummaryCsv(InpOutputSummaryCommon, InpRunId, InpSymbolA, InpSymbolB, ArraySize(g_a), g_events);
   g_last_run_time = TimeCurrent();
   Print("IMD001: total divergence events=", ArraySize(g_events), " events_file=", InpOutputEventsCommon);
}

int OnInit()
{
   if(InpRunMode == IMD_RUN_LIVE_MONITOR)
   {
      EventSetTimer(MathMax(1, InpLiveTimerSeconds));
      IMD_RunEngine();
      return INIT_SUCCEEDED;
   }

   IMD_RunEngine();
   if(InpRemoveAfterBatch)
      ExpertRemove();
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   if(InpRunMode == IMD_RUN_LIVE_MONITOR)
      IMD_RunEngine();
}

void OnDeinit(const int reason)
{
   EventKillTimer();
}

void OnTick()
{
   // Research-only; live mode is timer based so it can read broker bars or bridge-updated CSV files.
}
