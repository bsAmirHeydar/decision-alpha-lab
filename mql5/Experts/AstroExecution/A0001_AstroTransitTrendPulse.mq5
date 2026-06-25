#property strict
#property description "Astro-only transit trend pulse executor. No market-structure filters."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile          = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours  = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe         = PERIOD_M1;
input bool            InpRequireExactBarTime   = true;
input bool            InpUseChartComment       = true;
input string          InpJournalFile           = "astro\\paper\\a0001_transit_trend_pulse.csv";
input bool            InpJournalUseCommon      = true;
input bool            InpBatchBacktestOnInit   = true;
input bool            InpStopAfterBatch        = true;
input int             InpTimerSeconds          = 5;
input string          InpSignalWindowFile      = "astro\\paper\\a0001_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds = true;
input double          InpArmThreshold          = 58.0;
input double          InpEnterThreshold        = 68.0;
input double          InpReduceThreshold       = 52.0;
input double          InpExitThreshold         = 60.0;

DAL_AstroMapStore g_store;
datetime g_last_bar_time = 0;
DAL_AstroExecState g_state;
DAL_AstroThresholdProfile g_thresholds;
int g_batch_journal_handle = INVALID_HANDLE;

string DAL_AstroTransitPulse_Text(const DAL_AstroMapRow &row, const DAL_AstroPureSignal &s)
{
   string txt = "A0001 ASTRO TRANSIT TREND PULSE\n";
   txt += "bar=" + TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES) + "\n";
   txt += "direction=" + s.direction_name + " regime=" + s.regime_name + "\n";
   txt += "entry=" + s.entry_signal + " exit=" + s.exit_signal + "\n";
   txt += "entry_score=" + DoubleToString(s.entry_score, 1) + " path=" + DoubleToString(s.path_score, 1) + "\n";
   txt += s.astro_trade_key;
   return txt;
}

bool A0001_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds.exit_threshold   : InpExitThreshold;

   DAL_AstroExecState_Step(g_state, row, s, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle, row, s, g_state);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, s, g_state);

   if(verbose && InpUseChartComment)
      Comment(DAL_AstroTransitPulse_Text(row, s) + "\n" + DAL_AstroExecState_ToText(g_state));

   if(verbose)
      Print("A0001|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|dir=", s.direction_name,
            "|entry=", s.entry_signal,
            "|exit=", s.exit_signal,
            "|phase=", g_state.phase,
            "|action=", g_state.action);
   return true;
}

void A0001_RunBatch()
{
   if(!g_store.loaded)
      return;

   DAL_AstroExecState_Reset(g_state, "A0001_transit_trend_pulse");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle);

   int processed = 0;
   for(int i = 0; i < g_store.row_count; i++)
   {
      if(A0001_ProcessRow(g_store.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle);
      g_batch_journal_handle = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store);
   Print("A0001 BATCH COMPLETE | rows=", g_store.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0001_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time)
      return;
   g_last_bar_time = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store, bar_time, row, InpRequireExactBarTime))
      return;

   A0001_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state, "A0001_transit_trend_pulse");
   DAL_AstroThresholdProfile_Load("A0001_transit_trend_pulse", g_thresholds);

   if(InpBatchBacktestOnInit)
   {
      A0001_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0001_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
