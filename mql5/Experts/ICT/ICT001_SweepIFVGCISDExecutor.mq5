#property strict
#property version   "1.00"
#property description "EXP0014 ICT | L-node sweep -> path FVG -> IFVG -> CISD -> RR>=threshold batch executor"

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <ICT/DAL_ICTTypes.mqh>
#include <ICT/DAL_ICTSweepDetector.mqh>
#include <ICT/DAL_ICTFVGDetector.mqh>
#include <ICT/DAL_ICTCISDDetector.mqh>
#include <ICT/DAL_ICTExecutionModel.mqh>
#include <ICT/DAL_ICTJournal.mqh>

input ENUM_TIMEFRAMES     InpSignalTimeframe          = PERIOD_M10;
input int                 InpBarsToScan               = 0;       // 0 = all tester/terminal bars
input int                 InpL                         = 3;       // structural node L
input DAL_ICTSweepMode    InpSweepMode                 = ICT_SWEEP_HUNT;
input DAL_ICTTargetMode   InpTargetMode                = ICT_TARGET_TOUCH;
input double              InpNodeZoneHalfWidthPoints   = 20.0;
input double              InpSweepZoneTouchPct         = 50.0;
input double              InpTargetZoneTouchPct        = 50.0;
input double              InpFvgMinGapPoints           = 1.0;
input double              InpFvgTouchPctForIFVG        = 50.0;
input int                 InpPreSweepFvgLookbackBars   = 18;
input int                 InpMaxSetupBarsAfterSweep    = 24;
input int                 InpMaxLegLookbackBars        = 12;
input double              InpMinRR                     = 2.0;
input double              InpSLBufferPoints            = 5.0;
input double              InpEpsilonPoints             = 0.0;
input bool                InpExitOnNextSweep           = true;
input bool                InpUseCommonFiles            = true;
input string              InpOutputFolder              = "ict\\EXP0014";
input string              InpSignalsCsvName            = "ict001_entry_signals.csv";
input string              InpSummaryCsvName            = "ict001_summary.csv";
input bool                InpRunOnceOnInit             = true;

string ICT001_PathJoin(const string folder, const string name)
{
   if(folder == "") return name;
   string f = folder;
   StringReplace(f, "/", "\\");
   if(StringSubstr(f, StringLen(f)-1, 1) == "\\")
      return f + name;
   return f + "\\" + name;
}

bool ICT001_RunBatch()
{
   if(InpL < 1)
   {
      Print("ICT001: InpL must be >= 1");
      return false;
   }

   DALBar bars[];
   int bars_count = DAL_LoadBarsChronological(_Symbol, InpSignalTimeframe, InpBarsToScan, true, bars);
   if(bars_count <= 0)
   {
      Print("ICT001: no bars loaded. symbol=", _Symbol, " tf=", EnumToString(InpSignalTimeframe), " err=", GetLastError());
      return false;
   }

   DALLRuleNode nodes[];
   int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, InpL, nodes);

   DAL_ICTSweepEvent sweeps[];
   int sweeps_count = DAL_ICT_DetectSweepEvents(
      bars,
      bars_count,
      nodes,
      nodes_count,
      InpSweepMode,
      InpSweepZoneTouchPct,
      InpNodeZoneHalfWidthPoints,
      _Point,
      InpEpsilonPoints,
      sweeps
   );

   DAL_ICTFVG fvgs[];
   int fvgs_count = DAL_ICT_DetectFVGs(bars, bars_count, _Point, InpFvgMinGapPoints, fvgs);

   DAL_ICTEntrySignal signals[];
   int signals_count = DAL_ICT_BuildSweepIFVGCISDSignals(
      _Symbol,
      InpSignalTimeframe,
      bars,
      bars_count,
      InpL,
      nodes,
      nodes_count,
      sweeps,
      sweeps_count,
      fvgs,
      fvgs_count,
      _Point,
      InpPreSweepFvgLookbackBars,
      InpMaxSetupBarsAfterSweep,
      InpMaxLegLookbackBars,
      InpFvgTouchPctForIFVG,
      InpNodeZoneHalfWidthPoints,
      InpTargetZoneTouchPct,
      InpTargetMode,
      InpMinRR,
      InpSLBufferPoints,
      InpEpsilonPoints,
      InpExitOnNextSweep,
      signals
   );

   DAL_ICT_EnsureFolder(InpOutputFolder, InpUseCommonFiles);

   string run_id = StringFormat("ICT001_%s_%s_L%d_%s_%s",
      _Symbol,
      EnumToString(InpSignalTimeframe),
      InpL,
      DAL_ICT_SweepModeToString(InpSweepMode),
      DAL_ICT_TargetModeToString(InpTargetMode)
   );

   string signals_path = ICT001_PathJoin(InpOutputFolder, InpSignalsCsvName);
   string summary_path = ICT001_PathJoin(InpOutputFolder, InpSummaryCsvName);

   bool ok_signals = DAL_ICT_WriteEntrySignalsCsv(
      signals_path,
      InpUseCommonFiles,
      signals,
      signals_count,
      run_id,
      DAL_ICT_SweepModeToString(InpSweepMode),
      DAL_ICT_TargetModeToString(InpTargetMode)
   );

   bool ok_summary = DAL_ICT_WriteSummaryCsv(
      summary_path,
      InpUseCommonFiles,
      run_id,
      _Symbol,
      InpSignalTimeframe,
      bars_count,
      nodes_count,
      sweeps_count,
      fvgs_count,
      signals_count,
      signals
   );

   Print("ICT001_RESULT symbol=", _Symbol,
      " tf=", EnumToString(InpSignalTimeframe),
      " bars=", bars_count,
      " nodes=", nodes_count,
      " sweeps=", sweeps_count,
      " fvgs=", fvgs_count,
      " entry_signals=", signals_count,
      " signals_csv=", signals_path,
      " summary_csv=", summary_path,
      " common=", (InpUseCommonFiles ? "true" : "false")
   );

   return (ok_signals && ok_summary);
}

int OnInit()
{
   if(InpRunOnceOnInit)
   {
      ICT001_RunBatch();
      ExpertRemove();
   }
   return INIT_SUCCEEDED;
}

void OnTick()
{
   // Deliberately empty. This experiment is batch/bar based, not tick based.
}
