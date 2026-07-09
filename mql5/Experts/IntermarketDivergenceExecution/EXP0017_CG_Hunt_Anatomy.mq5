#property strict
#property version   "1.00"
#property description "EXP0017 Phase 03 - Cycle Group Hunt Anatomy"
#property description "No trading and no divergence. This expert only detects current-cycle high/low hunts against same-day CG references."

#include <IntermarketDivergenceExecution/CG/CGH_Engine.mqh>

input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";

input int  InpBrokerUtcOffsetHours = 3;
input bool InpUseAutoNewYorkDst = true;
input int  InpManualNewYorkUtcOffsetHours = -5;

input bool InpShowChartPanel = true;
input bool InpPrintSummaryOnNewMinute = false;
input int  InpTimerSeconds = 5;
input int  InpMaxGroupsShown = 8;
input int  InpMaxHuntsPerGroupShown = 3;
input bool InpShowOnlyGroupsWithHunts = false;
input bool InpRequireM1History = true;
input bool InpShowReferencePrices = true;
input bool InpShowCurrentCycleRanges = true;

input bool InpBuild_cg_3m   = true;
input bool InpBuild_cg_5m   = true;
input bool InpBuild_cg_9m   = true;
input bool InpBuild_cg_10m  = true;
input bool InpBuild_cg_15m  = true;
input bool InpBuild_cg_18m  = true;
input bool InpBuild_cg_20m  = true;
input bool InpBuild_cg_24m  = true;
input bool InpBuild_cg_30m  = true;
input bool InpBuild_cg_40m  = true;
input bool InpBuild_cg_45m  = true;
input bool InpBuild_cg_60m  = true;
input bool InpBuild_cg_72m  = true;
input bool InpBuild_cg_90m  = true;
input bool InpBuild_cg_120m = true;
input bool InpBuild_cg_150m = true;
input bool InpBuild_cg_180m = true;
input bool InpBuild_cg_240m = true;
input bool InpBuild_cg_300m = true;
input bool InpBuild_cg_360m = true;
input bool InpBuild_cg_720m = true;

CCGH_Engine g_engine;

int OnInit()
{
   SymbolSelect(InpSymbolA,true);
   SymbolSelect(InpSymbolB,true);

   SCGTTimeConfig time_config;
   time_config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   time_config.use_auto_new_york_dst=InpUseAutoNewYorkDst;
   time_config.manual_new_york_utc_offset_hours=InpManualNewYorkUtcOffsetHours;
   time_config.max_previous_cycles_shown=InpMaxHuntsPerGroupShown;

   SCGHHuntConfig hunt_config;
   hunt_config.symbol_a=InpSymbolA;
   hunt_config.symbol_b=InpSymbolB;
   hunt_config.broker_utc_offset_hours=InpBrokerUtcOffsetHours;
   hunt_config.max_groups_shown=InpMaxGroupsShown;
   hunt_config.max_hunts_per_group_shown=InpMaxHuntsPerGroupShown;
   hunt_config.require_m1_history=InpRequireM1History;
   hunt_config.show_only_groups_with_hunts=InpShowOnlyGroupsWithHunts;
   hunt_config.show_reference_prices=InpShowReferencePrices;
   hunt_config.show_current_cycle_ranges=InpShowCurrentCycleRanges;

   bool enabled[CGT_GROUP_COUNT];
   enabled[CGT_CG3M]   = InpBuild_cg_3m;
   enabled[CGT_CG5M]   = InpBuild_cg_5m;
   enabled[CGT_CG9M]   = InpBuild_cg_9m;
   enabled[CGT_CG10M]  = InpBuild_cg_10m;
   enabled[CGT_CG15M]  = InpBuild_cg_15m;
   enabled[CGT_CG18M]  = InpBuild_cg_18m;
   enabled[CGT_CG20M]  = InpBuild_cg_20m;
   enabled[CGT_CG24M]  = InpBuild_cg_24m;
   enabled[CGT_CG30M]  = InpBuild_cg_30m;
   enabled[CGT_CG40M]  = InpBuild_cg_40m;
   enabled[CGT_CG45M]  = InpBuild_cg_45m;
   enabled[CGT_CG60M]  = InpBuild_cg_60m;
   enabled[CGT_CG72M]  = InpBuild_cg_72m;
   enabled[CGT_CG90M]  = InpBuild_cg_90m;
   enabled[CGT_CG120M] = InpBuild_cg_120m;
   enabled[CGT_CG150M] = InpBuild_cg_150m;
   enabled[CGT_CG180M] = InpBuild_cg_180m;
   enabled[CGT_CG240M] = InpBuild_cg_240m;
   enabled[CGT_CG300M] = InpBuild_cg_300m;
   enabled[CGT_CG360M] = InpBuild_cg_360m;
   enabled[CGT_CG720M] = InpBuild_cg_720m;

   g_engine.Init(time_config,hunt_config,enabled,InpShowChartPanel,InpPrintSummaryOnNewMinute);

   int timer_seconds=InpTimerSeconds;
   if(timer_seconds<1)
      timer_seconds=1;
   EventSetTimer(timer_seconds);
   g_engine.Pulse();

   Print("EXP0017 Phase 03 Hunt Anatomy initialized. No trading, no divergence. Symbols: ",InpSymbolA," / ",InpSymbolB);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_engine.Clear();
}

void OnTick()
{
   // Hunt anatomy is refreshed by OnTimer to keep the observation layer deterministic.
}

void OnTimer()
{
   g_engine.Pulse();
}
