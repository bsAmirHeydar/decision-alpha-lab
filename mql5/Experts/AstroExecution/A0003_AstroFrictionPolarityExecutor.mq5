#property strict
#property description "Astro-only friction polarity executor. Reads pure astro friction/exit logic."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile          = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours  = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe         = PERIOD_M1;
input bool            InpRequireExactBarTime   = true;
input double          InpFrictionMinimum       = 60.0;
input bool            InpUseChartComment       = true;
input string          InpJournalFile           = "astro\\paper\\a0003_friction_polarity.csv";
input bool            InpJournalUseCommon      = true;
input bool            InpBatchBacktestOnInit   = true;
input bool            InpStopAfterBatch        = true;
input int             InpTimerSeconds          = 5;
input string          InpSignalWindowFile      = "astro\\paper\\a0003_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds = true;
input double          InpArmThreshold          = 58.0;
input double          InpEnterThreshold        = 68.0;
input double          InpReduceThreshold       = 52.0;
input double          InpExitThreshold         = 60.0;

DAL_AstroMapStore g_store_friction;
datetime g_last_bar_time_friction = 0;
DAL_AstroExecState g_state_friction;
DAL_AstroThresholdProfile g_thresholds_friction;
int g_batch_journal_handle_friction = INVALID_HANDLE;

bool A0003_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   double friction_minimum = InpUseDoctrineThresholds ? g_thresholds_friction.friction_minimum : InpFrictionMinimum;
   string polarity = "neutral";
   if(s.friction_score >= friction_minimum)
   {
      if(s.short_bias_score >= s.long_bias_score)
         polarity = "short_friction";
      else
         polarity = "long_friction";
   }

   DAL_AstroPureSignal gated = s;
   if(polarity == "neutral")
      gated.entry_signal = "wait";

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds_friction.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds_friction.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_friction.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds_friction.exit_threshold   : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_friction, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle_friction != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle_friction, row, gated, g_state_friction);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_friction);

   if(verbose)
   {
      string txt = "A0003 ASTRO FRICTION POLARITY\n";
      txt += "polarity=" + polarity + "\n";
      txt += "friction=" + DoubleToString(s.friction_score, 1) + " exit=" + s.exit_signal + "\n";
      txt += "long=" + DoubleToString(s.long_bias_score, 1) + " short=" + DoubleToString(s.short_bias_score, 1) + "\n";
      txt += DAL_AstroExecState_ToText(g_state_friction);

      if(InpUseChartComment)
         Comment(txt);

      Print("A0003|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|polarity=", polarity,
            "|friction=", DoubleToString(s.friction_score, 1),
            "|exit=", s.exit_signal,
            "|phase=", g_state_friction.phase,
            "|action=", g_state_friction.action);
   }
   return true;
}

void A0003_RunBatch()
{
   if(!g_store_friction.loaded)
      return;

   DAL_AstroExecState_Reset(g_state_friction, "A0003_friction_polarity");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle_friction);

   int processed = 0;
   for(int i = 0; i < g_store_friction.row_count; i++)
   {
      if(A0003_ProcessRow(g_store_friction.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle_friction != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle_friction);
      g_batch_journal_handle_friction = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store_friction);
   Print("A0003 BATCH COMPLETE | rows=", g_store_friction.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0003_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_friction)
      return;
   g_last_bar_time_friction = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_friction, bar_time, row, InpRequireExactBarTime))
      return;

   A0003_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_friction, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_friction, "A0003_friction_polarity");
   DAL_AstroThresholdProfile_Load("A0003_friction_polarity", g_thresholds_friction);

   if(InpBatchBacktestOnInit)
   {
      A0003_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0003_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
