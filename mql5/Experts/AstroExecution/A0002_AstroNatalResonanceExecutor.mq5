#property strict
#property description "Astro-only natal resonance executor. Requires natal-enabled CSV."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>

input string          InpAstroCsvFile            = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours    = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe           = PERIOD_M1;
input bool            InpRequireExactBarTime     = true;
input double          InpNatalActivationMinimum  = 40.0;
input bool            InpUseChartComment         = true;
input string          InpJournalFile             = "astro\\paper\\a0002_natal_resonance.csv";
input bool            InpJournalUseCommon        = true;
input bool            InpUseDoctrineThresholds   = true;
input double          InpArmThreshold            = 58.0;
input double          InpEnterThreshold          = 68.0;
input double          InpReduceThreshold         = 52.0;
input double          InpExitThreshold           = 60.0;

DAL_AstroMapStore g_store_natal;
datetime g_last_bar_time_natal = 0;
DAL_AstroExecState g_state_natal;
DAL_AstroThresholdProfile g_thresholds_natal;

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_natal, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_natal, "A0002_natal_resonance");
   DAL_AstroThresholdProfile_Load("A0002_natal_resonance", g_thresholds_natal);
   return INIT_SUCCEEDED;
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_natal)
      return;
   g_last_bar_time_natal = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_natal, bar_time, row, InpRequireExactBarTime))
      return;

   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return;

   double natal_activation_minimum = InpUseDoctrineThresholds ? g_thresholds_natal.natal_activation_minimum : InpNatalActivationMinimum;
   string entry = "wait";
   if(row.natal_enabled && s.natal_activation_score >= natal_activation_minimum)
      entry = s.entry_signal;

   DAL_AstroPureSignal gated = s;
   gated.entry_signal = entry;
   double arm_threshold = InpUseDoctrineThresholds ? g_thresholds_natal.arm_threshold : InpArmThreshold;
   double enter_threshold = InpUseDoctrineThresholds ? g_thresholds_natal.enter_threshold : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_natal.reduce_threshold : InpReduceThreshold;
   double exit_threshold = InpUseDoctrineThresholds ? g_thresholds_natal.exit_threshold : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_natal, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_natal);

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

void OnDeinit(const int reason)
{
   Comment("");
}
