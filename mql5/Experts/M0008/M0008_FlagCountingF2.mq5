#property strict
#property version   "1.00"
#property description "M0008 | F2 flag counting after F1 internal-2 start"

#include <M0008/DAL_M0008F2Detector.mqh>
#include <M0008/DAL_M0008F2Renderer.mqh>

input int               InpBarsToScan        = 3000;
input int               InpLMin              = 2;
input int               InpLMax              = 8;
input M0007_BreakMode   InpBreakMode         = M0007_BREAK_WICK;
input double            InpEpsilonPoints     = 0.0;

input bool              InpRequireParentF1Confirmed = true;
input bool              InpAllowWaistBreakBranch    = true;
input bool              InpRequireBranch12ForF2     = true;
input bool              InpRequireLeg2RebreakForConfirm = true;
input bool              InpScanBullishF2 = true;
input bool              InpScanBearishF2 = true;

input int               InpMaxEventsToDraw   = 120;
input bool              InpDrawOnlyConfirmed = false;
input bool              InpShowInternal12    = true;
input bool              InpShowF2Label       = true;
input bool              InpShowWaistBreakTag = false;

input color             InpBullishPendingColor   = clrDodgerBlue;
input color             InpBearishPendingColor   = clrOrange;
input color             InpBullishConfirmedColor = clrLime;
input color             InpBearishConfirmedColor = clrTomato;

input bool              InpRedrawOnNewBar    = true;
input bool              InpCleanObjectsOnInit = true;
input bool              InpDeleteOnDeinit    = false;
input string            InpObjectPrefix      = "DAL_M0008_F2_";

datetime g_last_bar_time = 0;

void M0008_ReverseRates(MqlRates &rates[])
{
   int n = ArraySize(rates);
   for(int i=0; i<n/2; i++)
   {
      MqlRates tmp = rates[i];
      rates[i] = rates[n-1-i];
      rates[n-1-i] = tmp;
   }
}

bool M0008_RunF2Detector()
{
   MqlRates rates[];
   int copied = CopyRates(_Symbol, _Period, 0, InpBarsToScan, rates);
   if(copied <= 0)
   {
      Print("DAL M0008 F2: CopyRates failed. error=", GetLastError());
      return false;
   }

   ArrayResize(rates, copied);
   if(copied > 1 && rates[0].time > rates[copied-1].time)
      M0008_ReverseRates(rates);

   M0008_F2Event events[];
   double eps = InpEpsilonPoints * _Point;

   M0008_DetectAdaptiveF2(rates,
                          copied,
                          InpLMin,
                          InpLMax,
                          InpBreakMode,
                          eps,
                          InpRequireParentF1Confirmed,
                          InpAllowWaistBreakBranch,
                          InpRequireBranch12ForF2,
                          InpRequireLeg2RebreakForConfirm,
                          InpScanBullishF2,
                          InpScanBearishF2,
                          events);

   int total = ArraySize(events);
   int confirmed = 0;
   int open_count = 0;
   int internal_branch = 0;
   int waist_branch = 0;
   for(int i=0; i<total; i++)
   {
      if(events[i].status == M0007_STATUS_CONFIRMED) confirmed++;
      else open_count++;
      if(events[i].branch == M0008_F2_BRANCH_INTERNAL12) internal_branch++;
      if(events[i].branch == M0008_F2_BRANCH_WAIST_BREAK) waist_branch++;
   }

   Print("DAL M0008 F2 EA | symbol=", _Symbol,
         " tf=", EnumToString(_Period),
         " bars=", copied,
         " L=", InpLMin, "..", InpLMax,
         " total=", total,
         " confirmed=", confirmed,
         " open=", open_count,
         " internalBranch=", internal_branch,
         " waistBreakBranch=", waist_branch,
         " parentConfirmedRequired=", (InpRequireParentF1Confirmed ? "true" : "false"),
         " allowWaistBreak=", (InpAllowWaistBreakBranch ? "true" : "false"));

   for(int i=MathMax(0,total-10); i<total; i++)
   {
      Print("DAL_M0008_F2_EVENT ", i,
            " dir=", M0007_DirectionToString(events[i].direction),
            " status=", M0007_StatusToString(events[i].status),
            " branch=", M0008_F2BranchToString(events[i].branch),
            " L=", events[i].matched_L_values,
            " Start=", TimeToString(events[i].Start.time, TIME_DATE|TIME_MINUTES), "@", DoubleToString(events[i].Start.price, _Digits),
            " H1=", TimeToString(events[i].H1.time, TIME_DATE|TIME_MINUTES), "@", DoubleToString(events[i].H1.price, _Digits),
            " W=", TimeToString(events[i].W.time, TIME_DATE|TIME_MINUTES), "@", DoubleToString(events[i].W.price, _Digits),
            " H2=", TimeToString(events[i].H2.time, TIME_DATE|TIME_MINUTES), "@", DoubleToString(events[i].H2.price, _Digits),
            " N1=", (events[i].has_internal_1 ? TimeToString(events[i].N1.time, TIME_DATE|TIME_MINUTES)+"@"+DoubleToString(events[i].N1.price, _Digits) : "NA"),
            " N2=", (events[i].has_internal_2 ? TimeToString(events[i].N2.time, TIME_DATE|TIME_MINUTES)+"@"+DoubleToString(events[i].N2.price, _Digits) : "NA"),
            " Confirm=", (events[i].confirm_index >= 0 ? TimeToString(events[i].confirm_time, TIME_DATE|TIME_MINUTES)+"@"+DoubleToString(events[i].confirm_price, _Digits) : "NA"));
   }

   int drawn = M0008_DrawEvents(events,
                                InpMaxEventsToDraw,
                                InpDrawOnlyConfirmed,
                                InpObjectPrefix,
                                InpShowInternal12,
                                InpShowF2Label,
                                InpShowWaistBreakTag,
                                InpBullishPendingColor,
                                InpBearishPendingColor,
                                InpBullishConfirmedColor,
                                InpBearishConfirmedColor);

   Print("DAL M0008 F2: drawn schematics=", drawn);
   return true;
}

int OnInit()
{
   if(InpLMin < 2)
   {
      Print("DAL M0008 F2: InpLMin must be >= 2");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(InpLMax < InpLMin)
   {
      Print("DAL M0008 F2: InpLMax must be >= InpLMin");
      return INIT_PARAMETERS_INCORRECT;
   }

   g_last_bar_time = iTime(_Symbol, _Period, 0);
   if(InpCleanObjectsOnInit)
      M0008_DeleteObjectsByPrefix(InpObjectPrefix);

   M0008_RunF2Detector();
   return INIT_SUCCEEDED;
}

void OnTick()
{
   if(!InpRedrawOnNewBar)
      return;

   datetime current_bar_time = iTime(_Symbol, _Period, 0);
   if(current_bar_time != g_last_bar_time)
   {
      g_last_bar_time = current_bar_time;
      M0008_RunF2Detector();
   }
}

void OnDeinit(const int reason)
{
   if(InpDeleteOnDeinit)
      M0008_DeleteObjectsByPrefix(InpObjectPrefix);
}
