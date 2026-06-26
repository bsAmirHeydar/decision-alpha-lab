#property strict
#property description "Astro-only moon timing window executor."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile           = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours   = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe          = PERIOD_M1;
input bool            InpRequireExactBarTime    = true;
input double          InpMoonReleaseMinimum     = 60.0;
input double          InpMinuteWindowMinimum    = 64.0;
input bool            InpUseChartComment        = true;
input string          InpJournalFile            = "astro\\paper\\a0005_moon_timing_window.csv";
input bool            InpJournalUseCommon       = true;
input bool            InpBatchBacktestOnInit    = true;
input bool            InpStopAfterBatch         = true;
input int             InpTimerSeconds           = 5;
input string          InpSignalWindowFile       = "astro\\paper\\a0005_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds  = true;
input double          InpArmThreshold           = 58.0;
input double          InpEnterThreshold         = 66.0;
input double          InpReduceThreshold        = 52.0;
input double          InpExitThreshold          = 58.0;

DAL_AstroMapStore g_store_moon;
datetime g_last_bar_time_moon = 0;
DAL_AstroExecState g_state_moon;
DAL_AstroThresholdProfile g_thresholds_moon;
int g_batch_journal_handle_moon = INVALID_HANDLE;

bool A0005_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   double moon_release_min = InpUseDoctrineThresholds ? g_thresholds_moon.moon_release_minimum : InpMoonReleaseMinimum;
   double minute_window_min = InpUseDoctrineThresholds ? g_thresholds_moon.minute_window_minimum : InpMinuteWindowMinimum;

   bool waxing_permission = (StringFind(row.moon_phase_bucket, "waxing") >= 0 || row.moon_phase_bucket == "first_quarter");
   bool waning_permission = (StringFind(row.moon_phase_bucket, "waning") >= 0 || row.moon_phase_bucket == "last_quarter" || row.moon_phase_bucket == "full");
   bool release_ready = (s.micro_timing_score >= moon_release_min && s.minute_window_score >= minute_window_min && s.trigger_state == "trigger_ready");

   string moon_state = "blocked";
   DAL_AstroPureSignal gated = s;
   if(release_ready)
   {
      if(s.direction_name == "long" && waxing_permission)
         moon_state = "waxing_release";
      else if(s.direction_name == "short" && waning_permission)
         moon_state = "waning_pressure";
      else
         gated.entry_signal = "wait";
   }
   else
      gated.entry_signal = "wait";

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds_moon.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds_moon.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_moon.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds_moon.exit_threshold   : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_moon, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle_moon != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle_moon, row, gated, g_state_moon);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_moon);

   if(verbose)
   {
      string txt = "A0005 ASTRO MOON TIMING WINDOW\n";
      txt += "moon_phase=" + row.moon_phase_bucket + " state=" + moon_state + "\n";
      txt += "micro=" + DoubleToString(s.micro_timing_score, 1) + " minute=" + DoubleToString(s.minute_window_score, 1) + "\n";
      txt += "entry=" + gated.entry_signal + " exit=" + gated.exit_signal + "\n";
      txt += DAL_AstroExecState_ToText(g_state_moon);

      if(InpUseChartComment)
         Comment(txt);

      Print("A0005|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|phase=", row.moon_phase_bucket,
            "|state=", moon_state,
            "|micro=", DoubleToString(s.micro_timing_score, 1),
            "|minute=", DoubleToString(s.minute_window_score, 1),
            "|action=", g_state_moon.action);
   }

   return true;
}

void A0005_RunBatch()
{
   if(!g_store_moon.loaded)
      return;

   DAL_AstroExecState_Reset(g_state_moon, "A0005_moon_timing_window");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle_moon);

   int processed = 0;
   for(int i = 0; i < g_store_moon.row_count; i++)
   {
      if(A0005_ProcessRow(g_store_moon.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle_moon != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle_moon);
      g_batch_journal_handle_moon = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store_moon);
   Print("A0005 BATCH COMPLETE | rows=", g_store_moon.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0005_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_moon)
      return;
   g_last_bar_time_moon = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_moon, bar_time, row, InpRequireExactBarTime))
      return;

   A0005_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_moon, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_moon, "A0005_moon_timing_window");
   DAL_AstroThresholdProfile_Load("A0005_moon_timing_window", g_thresholds_moon);

   if(InpBatchBacktestOnInit)
   {
      A0005_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0005_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
