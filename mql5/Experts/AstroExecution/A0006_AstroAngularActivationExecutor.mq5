#property strict
#property description "Astro-only angular activation executor."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile              = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours      = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe             = PERIOD_M1;
input bool            InpRequireExactBarTime       = true;
input double          InpAngularActivationMinimum  = 68.0;
input double          InpMinuteWindowMinimum       = 62.0;
input bool            InpUseChartComment           = true;
input string          InpJournalFile               = "astro\\paper\\a0006_angular_activation.csv";
input bool            InpJournalUseCommon          = true;
input bool            InpBatchBacktestOnInit       = true;
input bool            InpStopAfterBatch            = true;
input int             InpTimerSeconds              = 5;
input string          InpSignalWindowFile          = "astro\\paper\\a0006_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds     = true;
input double          InpArmThreshold              = 59.0;
input double          InpEnterThreshold            = 67.0;
input double          InpReduceThreshold           = 53.0;
input double          InpExitThreshold             = 59.0;

DAL_AstroMapStore g_store_ang;
datetime g_last_bar_time_ang = 0;
DAL_AstroExecState g_state_ang;
DAL_AstroThresholdProfile g_thresholds_ang;
int g_batch_journal_handle_ang = INVALID_HANDLE;

bool A0006_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   double angular_min = InpUseDoctrineThresholds ? g_thresholds_ang.angular_activation_minimum : InpAngularActivationMinimum;
   double minute_min = InpUseDoctrineThresholds ? g_thresholds_ang.minute_window_minimum : InpMinuteWindowMinimum;

   bool angular_ready = (s.angular_power_score >= angular_min && s.minute_window_score >= minute_min);
   bool lift_ready = (s.house_lift_score >= s.house_drag_score + 6.0);
   bool drag_ready = (s.house_drag_score >= s.house_lift_score + 6.0);

   string activation_state = "neutral";
   DAL_AstroPureSignal gated = s;
   if(angular_ready)
   {
      if(s.direction_name == "long" && lift_ready)
         activation_state = "angular_release";
      else if(s.direction_name == "short" && drag_ready)
         activation_state = "angular_pressure";
      else
         gated.entry_signal = "wait";
   }
   else
      gated.entry_signal = "wait";

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds_ang.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds_ang.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_ang.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds_ang.exit_threshold   : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_ang, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle_ang != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle_ang, row, gated, g_state_ang);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_ang);

   if(verbose)
   {
      string txt = "A0006 ASTRO ANGULAR ACTIVATION\n";
      txt += "state=" + activation_state + "\n";
      txt += "angular=" + DoubleToString(s.angular_power_score, 1) + " minute=" + DoubleToString(s.minute_window_score, 1) + "\n";
      txt += "lift=" + DoubleToString(s.house_lift_score, 1) + " drag=" + DoubleToString(s.house_drag_score, 1) + "\n";
      txt += "entry=" + gated.entry_signal + " exit=" + gated.exit_signal + "\n";
      txt += DAL_AstroExecState_ToText(g_state_ang);

      if(InpUseChartComment)
         Comment(txt);

      Print("A0006|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|state=", activation_state,
            "|angular=", DoubleToString(s.angular_power_score, 1),
            "|minute=", DoubleToString(s.minute_window_score, 1),
            "|action=", g_state_ang.action);
   }

   return true;
}

void A0006_RunBatch()
{
   if(!g_store_ang.loaded)
      return;

   DAL_AstroExecState_Reset(g_state_ang, "A0006_angular_activation");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle_ang);

   int processed = 0;
   for(int i = 0; i < g_store_ang.row_count; i++)
   {
      if(A0006_ProcessRow(g_store_ang.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle_ang != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle_ang);
      g_batch_journal_handle_ang = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store_ang);
   Print("A0006 BATCH COMPLETE | rows=", g_store_ang.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0006_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_ang)
      return;
   g_last_bar_time_ang = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_ang, bar_time, row, InpRequireExactBarTime))
      return;

   A0006_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_ang, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_ang, "A0006_angular_activation");
   DAL_AstroThresholdProfile_Load("A0006_angular_activation", g_thresholds_ang);

   if(InpBatchBacktestOnInit)
   {
      A0006_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0006_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
