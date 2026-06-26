#property strict
#property description "Astro-only station transition executor."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>
#include <Research/DAL_AstroSignalWindows.mqh>

input string          InpAstroCsvFile            = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours    = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe           = PERIOD_M1;
input bool            InpRequireExactBarTime     = true;
input double          InpTransitionMinimum       = 66.0;
input double          InpMinuteWindowMinimum     = 60.0;
input bool            InpUseChartComment         = true;
input string          InpJournalFile             = "astro\\paper\\a0007_station_transition.csv";
input bool            InpJournalUseCommon        = true;
input bool            InpBatchBacktestOnInit     = true;
input bool            InpStopAfterBatch          = true;
input int             InpTimerSeconds            = 5;
input string          InpSignalWindowFile        = "astro\\paper\\a0007_pure_signal_windows.csv";
input bool            InpUseDoctrineThresholds   = true;
input double          InpArmThreshold            = 59.0;
input double          InpEnterThreshold          = 67.0;
input double          InpReduceThreshold         = 53.0;
input double          InpExitThreshold           = 59.0;

DAL_AstroMapStore g_store_transition;
datetime g_last_bar_time_transition = 0;
DAL_AstroExecState g_state_transition;
DAL_AstroThresholdProfile g_thresholds_transition;
int g_batch_journal_handle_transition = INVALID_HANDLE;

bool A0007_ProcessRow(const DAL_AstroMapRow &row, const bool verbose)
{
   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return false;

   int moon = DAL_AstroBodyIndexByName("moon");
   int jupiter = DAL_AstroBodyIndexByName("jupiter");
   int saturn = DAL_AstroBodyIndexByName("saturn");
   int uranus = DAL_AstroBodyIndexByName("uranus");
   int neptune = DAL_AstroBodyIndexByName("neptune");
   int pluto = DAL_AstroBodyIndexByName("pluto");
   if(moon < 0 || jupiter < 0 || saturn < 0 || uranus < 0 || neptune < 0 || pluto < 0)
      return false;

   double transition_min = InpUseDoctrineThresholds ? g_thresholds_transition.transition_minimum : InpTransitionMinimum;
   double minute_min = InpUseDoctrineThresholds ? g_thresholds_transition.minute_window_minimum : InpMinuteWindowMinimum;

   double outer_station = DAL_AstroFM_Avg3(
      DAL_AstroFM_StationRisk(row.body[uranus]),
      DAL_AstroFM_StationRisk(row.body[neptune]),
      DAL_AstroFM_StationRisk(row.body[pluto])
   );
   double ingress_cluster = DAL_AstroFM_Avg4(
      DAL_AstroFM_IngressIntensity(row.body[jupiter]),
      DAL_AstroFM_IngressIntensity(row.body[saturn]),
      DAL_AstroFM_IngressIntensity(row.body[uranus]),
      DAL_AstroFM_IngressIntensity(row.body[moon])
   );
   double transition_field = DAL_AstroFM_Avg4(
      outer_station,
      ingress_cluster,
      s.volatility_score,
      100.0 - s.macro_timing_score
   );

   bool transition_ready = (transition_field >= transition_min && s.minute_window_score >= minute_min && s.minute_exhaustion_score <= 58.0);
   bool long_ready = (s.direction_name == "long" && s.benefic_support_score >= s.malefic_pressure_score + 4.0 && s.house_lift_score >= s.house_drag_score);
   bool short_ready = (s.direction_name == "short" && s.malefic_pressure_score >= s.benefic_support_score + 4.0 && s.house_drag_score >= s.house_lift_score);

   string transition_state = "blocked";
   DAL_AstroPureSignal gated = s;
   if(transition_ready)
   {
      if(long_ready)
         transition_state = "transition_release";
      else if(short_ready)
         transition_state = "transition_pressure";
      else
         gated.entry_signal = "wait";
   }
   else
      gated.entry_signal = "wait";

   double arm_threshold    = InpUseDoctrineThresholds ? g_thresholds_transition.arm_threshold    : InpArmThreshold;
   double enter_threshold  = InpUseDoctrineThresholds ? g_thresholds_transition.enter_threshold  : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_transition.reduce_threshold : InpReduceThreshold;
   double exit_threshold   = InpUseDoctrineThresholds ? g_thresholds_transition.exit_threshold   : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_transition, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   if(g_batch_journal_handle_transition != INVALID_HANDLE)
      DAL_AstroJournal_WriteHandle(g_batch_journal_handle_transition, row, gated, g_state_transition);
   else
      DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_transition);

   if(verbose)
   {
      string txt = "A0007 ASTRO STATION TRANSITION\n";
      txt += "state=" + transition_state + "\n";
      txt += "transition=" + DoubleToString(transition_field, 1) + " minute=" + DoubleToString(s.minute_window_score, 1) + "\n";
      txt += "exhaust=" + DoubleToString(s.minute_exhaustion_score, 1) + " outer_station=" + DoubleToString(outer_station, 1) + "\n";
      txt += "entry=" + gated.entry_signal + " exit=" + gated.exit_signal + "\n";
      txt += DAL_AstroExecState_ToText(g_state_transition);

      if(InpUseChartComment)
         Comment(txt);

      Print("A0007|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
            "|state=", transition_state,
            "|transition=", DoubleToString(transition_field, 1),
            "|minute=", DoubleToString(s.minute_window_score, 1),
            "|action=", g_state_transition.action);
   }

   return true;
}

void A0007_RunBatch()
{
   if(!g_store_transition.loaded)
      return;

   DAL_AstroExecState_Reset(g_state_transition, "A0007_station_transition");
   DAL_AstroJournal_OpenReset(InpJournalFile, InpJournalUseCommon, g_batch_journal_handle_transition);

   int processed = 0;
   for(int i = 0; i < g_store_transition.row_count; i++)
   {
      if(A0007_ProcessRow(g_store_transition.rows[i], false))
         processed++;
   }

   if(g_batch_journal_handle_transition != INVALID_HANDLE)
   {
      FileClose(g_batch_journal_handle_transition);
      g_batch_journal_handle_transition = INVALID_HANDLE;
   }

   bool windows_ok = DAL_AstroSW_ExportPureWindows(InpSignalWindowFile, InpJournalUseCommon, g_store_transition);
   Print("A0007 BATCH COMPLETE | rows=", g_store_transition.row_count,
         " processed=", processed,
         " windows_export=", windows_ok ? "ok" : "failed",
         " journal=", InpJournalFile,
         " windows=", InpSignalWindowFile);
}

void A0007_ProcessCurrentBar()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_transition)
      return;
   g_last_bar_time_transition = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_transition, bar_time, row, InpRequireExactBarTime))
      return;

   A0007_ProcessRow(row, true);
}

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_transition, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_transition, "A0007_station_transition");
   DAL_AstroThresholdProfile_Load("A0007_station_transition", g_thresholds_transition);

   if(InpBatchBacktestOnInit)
   {
      A0007_RunBatch();
      if(InpStopAfterBatch)
         ExpertRemove();
      return INIT_SUCCEEDED;
   }

   EventSetTimer(MathMax(1, InpTimerSeconds));
   return INIT_SUCCEEDED;
}

void OnTick() {}
void OnTimer() { A0007_ProcessCurrentBar(); }

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}
