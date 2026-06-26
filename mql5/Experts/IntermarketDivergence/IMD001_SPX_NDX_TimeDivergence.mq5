#property strict
#property version   "1.00"
#property description "EXP0015 Intermarket Time Divergence | SPX/NQ high-low/session/node divergence batch lab"

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <IntermarketDivergence/DAL_IMDTypes.mqh>
#include <IntermarketDivergence/DAL_IMDSeries.mqh>
#include <IntermarketDivergence/DAL_IMDReferenceLevels.mqh>
#include <IntermarketDivergence/DAL_IMDEngine.mqh>
#include <IntermarketDivergence/DAL_IMDJournal.mqh>

input string              InpSymbolA                         = "US500";
input string              InpSymbolB                         = "NAS100";
input string              InpPairLabel                       = "SPX_NDX";
input ENUM_TIMEFRAMES     InpSignalTimeframe                 = PERIOD_M5;
input int                 InpBarsToScan                      = 0;       // 0 = all tester/terminal bars
input DAL_IMDOriginBarMode InpOriginBarMode                  = IMD_ORIGIN_CLOSED_BARS_ONLY;

input int                 InpStepEveryBars                   = 1;       // evaluate every N bars
input int                 InpStepOffsetBars                  = 0;       // phase offset for step schedule
input int                 InpDestinationLagBars              = 0;       // destination may confirm within this many bars; if it does, no divergence
input int                 InpSignalValidBars                 = 12;      // validity window after divergence is confirmed
input int                 InpStartAfterBars                  = 50;      // warmup before first evaluation

input bool                InpScanAAsOrigin                   = true;
input bool                InpScanBAsOrigin                   = true;
input bool                InpCheckHighDivergence             = true;
input bool                InpCheckLowDivergence              = true;

input DAL_IMDLevelSource  InpOriginLevelSource               = IMD_LEVEL_L_NODE;
input DAL_IMDLevelSource  InpDestinationLevelSource          = IMD_LEVEL_L_NODE;
input int                 InpL                               = 3;
input int                 InpOriginRollingLookbackBars       = 20;
input int                 InpDestinationRollingLookbackBars  = 20;
input bool                InpExcludeCurrentBarFromReference  = true;

input DAL_IMDTriggerMode  InpTriggerMode                     = IMD_TRIGGER_WICK_TOUCH;
input double              InpEpsilonPoints                   = 0.0;

input int                 InpSessionStartHour                = 16;      // broker time; NY cash open is often 16:30 when broker is GMT+3 in US DST
input int                 InpSessionStartMinute              = 30;
input int                 InpSessionEndHour                  = 23;
input int                 InpSessionEndMinute                = 0;

input bool                InpUseCommonFiles                  = true;
input string              InpOutputFolder                    = "imd\\EXP0015";
input string              InpEventsCsvName                   = "imd001_divergence_events.csv";
input string              InpSummaryCsvName                  = "imd001_summary.csv";
input string              InpStepsCsvName                    = "imd001_evaluated_steps.csv";
input bool                InpWriteAllEvaluatedSteps          = false;
input bool                InpRunOnceOnInit                   = true;

string IMD001_PathJoin(const string folder, const string name)
{
   if(folder == "") return name;
   string f = folder;
   StringReplace(f, "/", "\\");
   if(StringLen(f) > 0 && StringSubstr(f, StringLen(f)-1, 1) == "\\")
      return f + name;
   return f + "\\" + name;
}

bool IMD001_RunBatch()
{
   if(InpSymbolA == "" || InpSymbolB == "")
   {
      Print("IMD001: symbols must not be empty");
      return false;
   }
   if(InpL < 1)
   {
      Print("IMD001: InpL must be >= 1");
      return false;
   }

   bool closed_bars_only = (InpOriginBarMode == IMD_ORIGIN_CLOSED_BARS_ONLY);

   DAL_IMDBarPair pairs[];
   int pairs_count = DAL_IMD_LoadAlignedPair(InpSymbolA, InpSymbolB, InpSignalTimeframe, InpBarsToScan, closed_bars_only, pairs);
   if(pairs_count <= 0)
   {
      Print("IMD001: no aligned bars. A=", InpSymbolA, " B=", InpSymbolB, " tf=", EnumToString(InpSignalTimeframe), " err=", GetLastError());
      return false;
   }

   DALBar bars_a[];
   DALBar bars_b[];
   DAL_IMD_ExtractSymbolBars(pairs, pairs_count, true, bars_a);
   DAL_IMD_ExtractSymbolBars(pairs, pairs_count, false, bars_b);

   DALLRuleNode nodes_a[];
   DALLRuleNode nodes_b[];
   int nodes_a_count = DAL_DetectConfirmedStructuralNodes(bars_a, pairs_count, InpL, nodes_a);
   int nodes_b_count = DAL_DetectConfirmedStructuralNodes(bars_b, pairs_count, InpL, nodes_b);

   DAL_IMDDivergenceEvent events[];
   DAL_IMDEvaluatedStep steps[];
   ArrayResize(events, 0);
   ArrayResize(steps, 0);

   if(InpScanAAsOrigin)
   {
      DAL_IMD_BuildDivergenceEventsOneDirection(
         InpPairLabel,
         InpSymbolA,
         InpSymbolB,
         InpSignalTimeframe,
         bars_a,
         bars_b,
         pairs_count,
         nodes_a,
         nodes_a_count,
         nodes_b,
         nodes_b_count,
         InpStartAfterBars,
         InpStepEveryBars,
         InpStepOffsetBars,
         InpOriginLevelSource,
         InpDestinationLevelSource,
         InpOriginRollingLookbackBars,
         InpDestinationRollingLookbackBars,
         InpExcludeCurrentBarFromReference,
         InpSessionStartHour,
         InpSessionStartMinute,
         InpSessionEndHour,
         InpSessionEndMinute,
         InpTriggerMode,
         InpDestinationLagBars,
         InpSignalValidBars,
         InpEpsilonPoints,
         _Point,
         InpCheckHighDivergence,
         InpCheckLowDivergence,
         InpWriteAllEvaluatedSteps,
         events,
         steps
      );
   }

   if(InpScanBAsOrigin)
   {
      DAL_IMD_BuildDivergenceEventsOneDirection(
         InpPairLabel,
         InpSymbolB,
         InpSymbolA,
         InpSignalTimeframe,
         bars_b,
         bars_a,
         pairs_count,
         nodes_b,
         nodes_b_count,
         nodes_a,
         nodes_a_count,
         InpStartAfterBars,
         InpStepEveryBars,
         InpStepOffsetBars,
         InpOriginLevelSource,
         InpDestinationLevelSource,
         InpOriginRollingLookbackBars,
         InpDestinationRollingLookbackBars,
         InpExcludeCurrentBarFromReference,
         InpSessionStartHour,
         InpSessionStartMinute,
         InpSessionEndHour,
         InpSessionEndMinute,
         InpTriggerMode,
         InpDestinationLagBars,
         InpSignalValidBars,
         InpEpsilonPoints,
         _Point,
         InpCheckHighDivergence,
         InpCheckLowDivergence,
         InpWriteAllEvaluatedSteps,
         events,
         steps
      );
   }

   int period_seconds = DAL_PeriodSecondsSafe(InpSignalTimeframe);
   DAL_IMD_ApplyNextDivergenceWindowEnd(events, ArraySize(events), period_seconds);

   DAL_IMD_EnsureFolder(InpOutputFolder, InpUseCommonFiles);

   string run_id = StringFormat("IMD001_%s_%s_%s_L%d_%s_%s_STEP%d_LAG%d",
      InpPairLabel,
      InpSymbolA,
      InpSymbolB,
      InpL,
      DAL_IMD_LevelSourceToString(InpOriginLevelSource),
      DAL_IMD_TriggerModeToString(InpTriggerMode),
      MathMax(1, InpStepEveryBars),
      MathMax(0, InpDestinationLagBars)
   );

   string events_path = IMD001_PathJoin(InpOutputFolder, InpEventsCsvName);
   string summary_path = IMD001_PathJoin(InpOutputFolder, InpSummaryCsvName);
   string steps_path = IMD001_PathJoin(InpOutputFolder, InpStepsCsvName);

   bool ok_events = DAL_IMD_WriteEventsCsv(events_path, InpUseCommonFiles, run_id, events, ArraySize(events));
   bool ok_summary = DAL_IMD_WriteSummaryCsv(summary_path, InpUseCommonFiles, run_id, InpSymbolA, InpSymbolB, InpSignalTimeframe, pairs_count, nodes_a_count, nodes_b_count, ArraySize(events), ArraySize(steps), events);
   bool ok_steps = true;
   if(InpWriteAllEvaluatedSteps)
      ok_steps = DAL_IMD_WriteStepsCsv(steps_path, InpUseCommonFiles, run_id, steps, ArraySize(steps));

   Print("IMD001_RESULT pair=", InpPairLabel,
      " A=", InpSymbolA,
      " B=", InpSymbolB,
      " tf=", EnumToString(InpSignalTimeframe),
      " aligned_bars=", pairs_count,
      " nodes_a=", nodes_a_count,
      " nodes_b=", nodes_b_count,
      " events=", ArraySize(events),
      " steps=", ArraySize(steps),
      " events_csv=", events_path,
      " summary_csv=", summary_path,
      " common=", (InpUseCommonFiles ? "true" : "false")
   );

   return (ok_events && ok_summary && ok_steps);
}

int OnInit()
{
   if(InpRunOnceOnInit)
   {
      IMD001_RunBatch();
      ExpertRemove();
   }
   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Deliberately empty. EXP0015 is a time-step/bar-close divergence lab, not a tick-driven executor.
}
