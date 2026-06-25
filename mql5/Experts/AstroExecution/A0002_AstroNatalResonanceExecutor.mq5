#property strict
#property description "Astro-only natal resonance executor. Requires natal-enabled CSV."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile            = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours    = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe           = PERIOD_M1;
input bool            InpRequireExactBarTime     = true;
input double          InpNatalActivationMinimum  = 40.0;
input bool            InpUseChartComment         = true;
input string          InpJournalFile             = "astro\\paper\\a0002_natal_resonance.csv";
input bool            InpJournalUseCommon        = true;
input bool            InpBatchBacktestOnInit     = true;
input bool            InpStopAfterBatch          = true;
input int             InpTimerSeconds            = 5;
input string          InpSignalWindowFile        = "astro\\paper\\a0002_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds   = true;
input double          InpArmThreshold            = 58.0;
input double          InpEnterThreshold          = 68.0;
input double          InpReduceThreshold         = 52.0;
input double          InpExitThreshold           = 60.0;

DAL_AstroMapStore g_store_natal;
datetime g_last_bar_time_natal = 0;
DAL_AstroExecState g_state_natal;
DAL_AstroThresholdProfile g_thresholds_natal;
int g_batch_journal_handle_natal = INVALID_HANDLE;

bool A0002_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   double natal_activation_minimum = InpUseDoctrineThresholds ? g_thresholds_natal.natal_activation_minimum : InpNatalActivationMinimum;
   string entry = "wait";
   if(row.natal_enabled && s.natal_activation_score >= natal_activation_minimum)
      entry = s.entry_signal;

   DAL_AstroPureSignal gated = s;
   gated.entry_signal = entry;

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds_natal.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds_natal.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_natal.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds_natal.exit_threshold   : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_natal, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle_natal != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle_natal, row, gated, g_state_natal);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_natal);

   if(verbose)
   {
      string txt = "A0002 ASTRO NATAL RESONANCE\n";
      txt += "natal=" + (row.natal_enabled ? row.natal_label : "missing") + "\n";
      txt += "entry=" + entry + " exit=" + s.exit_signal + "\n";
      txt += "natal_activation=" + DoubleToString(s.natal_activation_score, 1) + "\n";
      txt += "dir=" + s.direction_name + " regime=" + s.regime_name + "\n";
      txt += DAL_AstroExecState_ToText(g_state_natal);

      if(InpUseChartComment)
         Comment(txt);

      Print("A0002|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|natal=", row.natal_enabled ? row.natal_label : "missing",
            "|entry=", entry,
            "|natal_act=", DoubleToString(s.natal_activation_score, 1),
            "|phase=", g_state_natal.phase,
            "|action=", g_state_natal.action);
   }
   return true;
}

void A0002_RunBatch()
{
   if(!g_store_natal.loaded)
      return;

   DAL_AstroExecState_Reset(g_state_natal, "A0002_natal_resonance");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle_natal);

   int processed = 0;
   for(int i = 0; i < g_store_natal.row_count; i++)
   {
      if(A0002_ProcessRow(g_store_natal.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle_natal != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle_natal);
      g_batch_journal_handle_natal = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store_natal);
   Print("A0002 BATCH COMPLETE | rows=", g_store_natal.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0002_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_natal)
      return;
   g_last_bar_time_natal = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_natal, bar_time, row, InpRequireExactBarTime))
      return;

   A0002_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_natal, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_natal, "A0002_natal_resonance");
   DAL_AstroThresholdProfile_Load("A0002_natal_resonance", g_thresholds_natal);

   if(InpBatchBacktestOnInit)
   {
      A0002_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0002_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
