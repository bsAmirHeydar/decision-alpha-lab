#property strict
#property description "Astro-only friction polarity executor. Reads pure astro friction/exit logic."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroFamilyThresholds.mqh>
#include <Research/DAL_AstroExecutionJournal.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>

input string          InpAstroCsvFile         = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe        = PERIOD_M1;
input bool            InpRequireExactBarTime  = true;
input double          InpFrictionMinimum      = 60.0;
input bool            InpUseChartComment      = true;
input string          InpJournalFile          = "astro\\paper\\a0003_friction_polarity.csv";
input bool            InpJournalUseCommon     = true;
input bool            InpUseDoctrineThresholds = true;
input double          InpArmThreshold         = 58.0;
input double          InpEnterThreshold       = 68.0;
input double          InpReduceThreshold      = 52.0;
input double          InpExitThreshold        = 60.0;

DAL_AstroMapStore g_store_friction;
datetime g_last_bar_time_friction = 0;
DAL_AstroExecState g_state_friction;
DAL_AstroThresholdProfile g_thresholds_friction;

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store_friction, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   DAL_AstroExecState_Reset(g_state_friction, "A0003_friction_polarity");
   DAL_AstroThresholdProfile_Load("A0003_friction_polarity", g_thresholds_friction);
   return INIT_SUCCEEDED;
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time_friction)
      return;
   g_last_bar_time_friction = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store_friction, bar_time, row, InpRequireExactBarTime))
      return;

   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return;

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
   double arm_threshold = InpUseDoctrineThresholds ? g_thresholds_friction.arm_threshold : InpArmThreshold;
   double enter_threshold = InpUseDoctrineThresholds ? g_thresholds_friction.enter_threshold : InpEnterThreshold;
   double reduce_threshold = InpUseDoctrineThresholds ? g_thresholds_friction.reduce_threshold : InpReduceThreshold;
   double exit_threshold = InpUseDoctrineThresholds ? g_thresholds_friction.exit_threshold : InpExitThreshold;
   DAL_AstroExecState_Step(g_state_friction, row, gated, arm_threshold, enter_threshold, reduce_threshold, exit_threshold);
   DAL_AstroJournal_Append(InpJournalFile, InpJournalUseCommon, row, gated, g_state_friction);

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

void OnDeinit(const int reason)
{
   Comment("");
}
