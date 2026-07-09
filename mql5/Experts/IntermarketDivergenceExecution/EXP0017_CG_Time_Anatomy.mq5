#property strict
#property version   "1.00"
#property description "EXP0017 Phase 01 - Cycle Group Time Anatomy"
#property description "No trading, no hunt, no divergence. This expert only builds NY trading-day and CG cycle awareness."

#include <IntermarketDivergenceExecution/CG/CGT_Engine.mqh>

input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

input int  InpBrokerUtcOffsetHours = 3;
input bool InpUseAutoNewYorkDst = true;
input int  InpManualNewYorkUtcOffsetHours = -5;

input bool InpShowChartPanel = true;
input bool InpPrintSummaryOnNewMinute = false;
input int  InpTimerSeconds = 5;
input int  InpMaxPreviousCyclesShown = 5;

input bool InpShow_cg_3m   = true;
input bool InpShow_cg_5m   = true;
input bool InpShow_cg_9m   = true;
input bool InpShow_cg_10m  = true;
input bool InpShow_cg_15m  = true;
input bool InpShow_cg_18m  = true;
input bool InpShow_cg_20m  = true;
input bool InpShow_cg_24m  = true;
input bool InpShow_cg_30m  = true;
input bool InpShow_cg_40m  = true;
input bool InpShow_cg_45m  = true;
input bool InpShow_cg_60m  = true;
input bool InpShow_cg_72m  = true;
input bool InpShow_cg_90m  = true;
input bool InpShow_cg_120m = true;
input bool InpShow_cg_150m = true;
input bool InpShow_cg_180m = true;
input bool InpShow_cg_240m = true;
input bool InpShow_cg_300m = true;
input bool InpShow_cg_360m = true;
input bool InpShow_cg_720m = true;

CCGT_Engine g_engine;

int OnInit()
{
   SymbolSelect(InpSymbolA,true);
   SymbolSelect(InpSymbolB,true);

   SCGTTimeConfig config;
   config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   config.use_auto_new_york_dst=InpUseAutoNewYorkDst;
   config.manual_new_york_utc_offset_hours=InpManualNewYorkUtcOffsetHours;
   config.max_previous_cycles_shown=InpMaxPreviousCyclesShown;

   bool enabled[CGT_GROUP_COUNT];
   enabled[CGT_CG3M]   = InpShow_cg_3m;
   enabled[CGT_CG5M]   = InpShow_cg_5m;
   enabled[CGT_CG9M]   = InpShow_cg_9m;
   enabled[CGT_CG10M]  = InpShow_cg_10m;
   enabled[CGT_CG15M]  = InpShow_cg_15m;
   enabled[CGT_CG18M]  = InpShow_cg_18m;
   enabled[CGT_CG20M]  = InpShow_cg_20m;
   enabled[CGT_CG24M]  = InpShow_cg_24m;
   enabled[CGT_CG30M]  = InpShow_cg_30m;
   enabled[CGT_CG40M]  = InpShow_cg_40m;
   enabled[CGT_CG45M]  = InpShow_cg_45m;
   enabled[CGT_CG60M]  = InpShow_cg_60m;
   enabled[CGT_CG72M]  = InpShow_cg_72m;
   enabled[CGT_CG90M]  = InpShow_cg_90m;
   enabled[CGT_CG120M] = InpShow_cg_120m;
   enabled[CGT_CG150M] = InpShow_cg_150m;
   enabled[CGT_CG180M] = InpShow_cg_180m;
   enabled[CGT_CG240M] = InpShow_cg_240m;
   enabled[CGT_CG300M] = InpShow_cg_300m;
   enabled[CGT_CG360M] = InpShow_cg_360m;
   enabled[CGT_CG720M] = InpShow_cg_720m;

   g_engine.Init(config,enabled,InpShowChartPanel,InpPrintSummaryOnNewMinute);

   int timer_seconds=InpTimerSeconds;
   if(timer_seconds<1)
      timer_seconds=1;
   EventSetTimer(timer_seconds);
   g_engine.Pulse();

   Print("EXP0017 Phase 01 Time Anatomy initialized. No trading is enabled. Symbols: ",InpSymbolA," / ",InpSymbolB);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_engine.Clear();
}

void OnTick()
{
   // Kept intentionally light. Time anatomy is refreshed by OnTimer.
}

void OnTimer()
{
   g_engine.Pulse();
}
