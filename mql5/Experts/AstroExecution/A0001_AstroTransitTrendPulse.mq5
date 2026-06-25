#property strict
#property description "Astro-only transit trend pulse executor. No market-structure filters."

#include <Research/DAL_AstroExcelCandleReader.mqh>
#include <Research/DAL_AstroPureAstrologySignals.mqh>

input string          InpAstroCsvFile         = "astro_live_mql.csv";
input double          InpBrokerGmtOffsetHours = 0.0;
input ENUM_TIMEFRAMES InpReadTimeframe        = PERIOD_M1;
input bool            InpRequireExactBarTime  = true;
input bool            InpUseChartComment      = true;

DAL_AstroMapStore g_store;
datetime g_last_bar_time = 0;

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

int OnInit()
{
   DAL_AstroMapStore_LoadExcelCsv(g_store, InpAstroCsvFile, InpBrokerGmtOffsetHours, PeriodSeconds(InpReadTimeframe) / 60);
   return INIT_SUCCEEDED;
}

void OnTick()
{
   datetime bar_time = iTime(_Symbol, InpReadTimeframe, 0);
   if(bar_time <= 0 || bar_time == g_last_bar_time)
      return;
   g_last_bar_time = bar_time;

   DAL_AstroMapRow row;
   if(!DAL_AstroMapStore_FindForCandleOpen(g_store, bar_time, row, InpRequireExactBarTime))
      return;

   DAL_AstroPureSignal s;
   if(!DAL_AstroPureSignal_Calc(row, s) || !s.valid)
      return;

   if(InpUseChartComment)
      Comment(DAL_AstroTransitPulse_Text(row, s));

   Print("A0001|", TimeToString(row.broker_time, TIME_DATE | TIME_MINUTES),
         "|dir=", s.direction_name,
         "|entry=", s.entry_signal,
         "|exit=", s.exit_signal,
         "|score=", DoubleToString(s.entry_score, 1));
}

void OnDeinit(const int reason)
{
   Comment("");
}
