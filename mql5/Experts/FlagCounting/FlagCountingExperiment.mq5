#property strict
#property version   "1.00"
#property description "Unified modular flag-counting experiment: F1 and F2 in one reusable module."

#include "../../Include/FlagCounting/DAL_FlagCountingDetector.mqh"
#include "../../Include/FlagCounting/DAL_FlagCountingRenderer.mqh"

input int  InpBarsToScan = 6000;
input int  InpSwingL = 3;
input int  InpBreakEpsilonPoints = 5;

input bool InpScanF1 = true;
input bool InpScanF2 = true;
input bool InpScanBullish = true;
input bool InpScanBearish = true;

input bool InpRequireF1Internal12 = true;
input bool InpRequireF1Leg2RebreakForConfirm = true;
input bool InpRequireParentF1ConfirmedForF2 = true;
input bool InpAllowF2WaistBreakBranch = true;
input bool InpRequireF2Branch12 = true;
input bool InpRequireF2Leg2RebreakForConfirm = true;

input bool InpDrawF1 = true;
input bool InpDrawF2 = true;
input bool InpDrawOnlyConfirmed = false;
input int  InpMaxEventsToDraw = 160;
input string InpObjectPrefix = "DAL_FC_";
input bool InpCleanObjectsOnInit = true;
input bool InpRedrawOnNewBar = true;

input color InpF1PendingColor = clrDeepSkyBlue;
input color InpF1ConfirmedColor = clrLime;
input color InpF2PendingColor = clrGold;
input color InpF2ConfirmedColor = clrTomato;
input int InpLineWidth = 2;
input int InpCurveSegments = 10;
input bool InpShowFlagLabel = true;
input bool InpShowInternal12Labels = true;
input int InpFlagFontSize = 16;
input int InpInternalFontSize = 12;

input bool InpPrintSummary = true;
input bool InpPrintLastEvents = true;
input int  InpPrintLastN = 8;

datetime g_last_bar_time = 0;

void FC_PrintEvent(const FC_FlagEvent &e, const int ordinal)
{
   Print("FC_EVENT#", ordinal,
         " level=", FC_LevelToString(e.level),
         " dir=", FC_DirectionToString(e.direction),
         " status=", FC_StatusToString(e.status),
         " branch=", FC_BranchToString(e.branch_type),
         " origin=", TimeToString(e.origin.time), "@", DoubleToString(e.origin.price, _Digits),
         " leg1=", TimeToString(e.leg1.time), "@", DoubleToString(e.leg1.price, _Digits),
         " waist=", TimeToString(e.waist.time), "@", DoubleToString(e.waist.price, _Digits),
         " leg2=", TimeToString(e.leg2.time), "@", DoubleToString(e.leg2.price, _Digits),
         " n1=", (e.has_n1 ? TimeToString(e.n1.time) : "NA"), "@", (e.has_n1 ? DoubleToString(e.n1.price, _Digits) : "NA"),
         " n2=", (e.has_n2 ? TimeToString(e.n2.time) : "NA"), "@", (e.has_n2 ? DoubleToString(e.n2.price, _Digits) : "NA"),
         " confirm=", (e.confirm_index >= 0 ? TimeToString(e.confirm_time) : "NA"), "@", (e.confirm_index >= 0 ? DoubleToString(e.confirm_price, _Digits) : "NA"));
}

void FC_PrintSummary(const FC_FlagEvent &events[], const int nodes_count, const int drawn)
{
   int total = ArraySize(events);
   int f1=0, f2=0, conf=0, open=0, branch_i12=0, branch_wb=0;
   for(int i=0; i<total; i++)
   {
      if(events[i].level == FC_LEVEL_F1) f1++;
      if(events[i].level == FC_LEVEL_F2) f2++;
      if(events[i].status == FC_STATUS_CONFIRMED) conf++;
      if(events[i].status == FC_STATUS_OPEN) open++;
      if(events[i].branch_type == FC_BRANCH_INTERNAL12) branch_i12++;
      if(events[i].branch_type == FC_BRANCH_WAIST_BREAK) branch_wb++;
   }

   Print("FC_SUMMARY symbol=", _Symbol,
         " tf=", EnumToString(_Period),
         " bars=", InpBarsToScan,
         " nodes=", nodes_count,
         " events=", total,
         " f1=", f1,
         " f2=", f2,
         " confirmed=", conf,
         " open=", open,
         " internal12=", branch_i12,
         " waistBreak=", branch_wb,
         " drawn=", drawn);

   if(InpPrintLastEvents)
   {
      int start = (int)MathMax(0, total - InpPrintLastN);
      for(int j=start; j<total; j++)
         FC_PrintEvent(events[j], j);
   }
}

bool FC_RunExperiment()
{
   int bars = (int)MathMax(300, InpBarsToScan);
   MqlRates rates[];
   ArraySetAsSeries(rates, false);
   int copied = CopyRates(_Symbol, _Period, 0, bars, rates);
   if(copied <= 100)
   {
      Print("FC experiment: not enough copied rates. copied=", copied);
      return false;
   }
   ArrayResize(rates, copied);

   FC_Node nodes[];
   FC_FlagEvent events[];
   double eps = (double)InpBreakEpsilonPoints * _Point;

   int total_events = FC_DetectFlags(rates,
                                     copied,
                                     InpSwingL,
                                     InpScanF1,
                                     InpScanF2,
                                     InpScanBullish,
                                     InpScanBearish,
                                     InpRequireF1Internal12,
                                     InpRequireF1Leg2RebreakForConfirm,
                                     InpRequireParentF1ConfirmedForF2,
                                     InpAllowF2WaistBreakBranch,
                                     InpRequireF2Branch12,
                                     InpRequireF2Leg2RebreakForConfirm,
                                     eps,
                                     nodes,
                                     events);

   int drawn = FC_DrawFlags(events,
                            InpMaxEventsToDraw,
                            InpDrawF1,
                            InpDrawF2,
                            InpDrawOnlyConfirmed,
                            InpObjectPrefix,
                            InpF1PendingColor,
                            InpF1ConfirmedColor,
                            InpF2PendingColor,
                            InpF2ConfirmedColor,
                            InpLineWidth,
                            InpCurveSegments,
                            InpShowFlagLabel,
                            InpShowInternal12Labels,
                            InpFlagFontSize,
                            InpInternalFontSize);

   if(InpPrintSummary)
      FC_PrintSummary(events, ArraySize(nodes), drawn);

   return total_events >= 0;
}

int OnInit()
{
   if(InpCleanObjectsOnInit)
      FC_DeleteObjectsByPrefix(InpObjectPrefix);

   FC_RunExperiment();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(InpCleanObjectsOnInit)
      FC_DeleteObjectsByPrefix(InpObjectPrefix);
}

void OnTick()
{
   if(!InpRedrawOnNewBar)
      return;

   datetime t = iTime(_Symbol, _Period, 0);
   if(t == 0) return;
   if(t == g_last_bar_time) return;
   g_last_bar_time = t;

   FC_RunExperiment();
}
