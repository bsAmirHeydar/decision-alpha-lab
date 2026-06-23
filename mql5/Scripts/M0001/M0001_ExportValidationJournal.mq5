//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Validation Journal Export             |
//+------------------------------------------------------------------+
#property strict
#property script_show_inputs

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/LRule/DAL_LRuleDetector.mqh>
#include <M0001/DAL_M0001Config.mqh>
#include <M0001/DAL_M0001Engine.mqh>
#include <Research/DAL_ValidationJournal.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 2000;
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input string InpOutputPrefix = "DecisionAlphaLab\\M0001\\";

void OnStart()
{
   string symbol = InpSymbol == "" ? _Symbol : InpSymbol;
   ENUM_TIMEFRAMES timeframe = InpTimeframe == PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpTimeframe;

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(symbol, timeframe, InpBars, true, bars);

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectLRuleNodes(bars, bars_count, InpL, nodes);

   DALM0001Config config;
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, config, events);

   DAL_WriteM0001NodeJournal(InpOutputPrefix + symbol + "_M0001_nodes.csv", nodes, nodes_count);
   DAL_WriteM0001EventJournal(InpOutputPrefix + symbol + "_M0001_events.csv", events, events_count);

   Print("M0001 journal exported | nodes=", nodes_count, " events=", events_count);
}
