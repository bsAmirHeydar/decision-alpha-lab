#property strict
#property version   "1.01"
#property description "M0007 | Adaptive F1 Flag Counting visual audit EA"

#include <M0007/DAL_M0007F1Types.mqh>
#include <M0007/DAL_M0007F1Detector.mqh>
#include <M0007/DAL_M0007F1Renderer.mqh>

input int               InpBarsToScan        = 3000;
input int               InpLMin              = 2;
input int               InpLMax              = 8;
input M0007_BreakMode   InpBreakMode         = M0007_BREAK_WICK;
input double            InpEpsilonPoints     = 0.0;
input double            InpOverlapThreshold  = 0.60;
input int               InpMaxEventsToDraw   = 20;
input bool              InpDrawOnlyConfirmed = true;
input bool              InpRedrawOnNewBar    = false;
input bool              InpDeleteOnDeinit    = false;
input string            InpObjectPrefix      = "DAL_M0007_F1_";

datetime g_last_bar_time = 0;

void M0007_ReverseRates(MqlRates &rates[])
{
   int n = ArraySize(rates);
   for(int i=0; i<n/2; i++)
   {
      MqlRates tmp = rates[i];
      rates[i] = rates[n-1-i];
      rates[n-1-i] = tmp;
   }
}

bool M0007_RunF1Detector()
{
   MqlRates rates[];
   int copied = CopyRates(_Symbol, _Period, 0, InpBarsToScan, rates);
   if(copied <= 0)
   {
      Print("DAL M0007 F1: CopyRates failed. error=", GetLastError());
      return false;
   }

   ArrayResize(rates, copied);

   // Detector expects chronological order: oldest -> newest.
   if(copied > 1 && rates[0].time > rates[copied-1].time)
      M0007_ReverseRates(rates);

   M0007_F1Event events[];
   double eps = InpEpsilonPoints * _Point;

   M0007_DetectAdaptiveF1(
      rates,
      copied,
      InpLMin,
      InpLMax,
      InpBreakMode,
      eps,
      InpOverlapThreshold,
      events
   );

   int total = ArraySize(events);
   int confirmed = 0;
   int invalidated = 0;
   int open = 0;

   for(int i=0; i<total; i++)
   {
      if(events[i].status == M0007_STATUS_CONFIRMED)
         confirmed++;
      else if(events[i].status == M0007_STATUS_INVALIDATED)
         invalidated++;
      else
         open++;
   }

   Print("DAL M0007 F1 Adaptive EA | symbol=", _Symbol,
         " tf=", EnumToString(_Period),
         " bars=", copied,
         " L=", InpLMin, "..", InpLMax,
         " total=", total,
         " confirmed=", confirmed,
         " invalidated=", invalidated,
         " open=", open);

   for(int i=MathMax(0,total-10); i<total; i++)
   {
      Print("DAL_M0007_EVENT ", i,
            " dir=", M0007_DirectionToString(events[i].direction),
            " status=", M0007_StatusToString(events[i].status),
            " L_used=", events[i].L_used,
            " matched_L=", events[i].matched_L_values,
            " H1/L1=", TimeToString(events[i].H1.time, TIME_DATE|TIME_MINUTES), "@", DoubleToString(events[i].H1.price, _Digits),
            " W=", DoubleToString(events[i].W.price, _Digits),
            " H2/L2=", DoubleToString(events[i].H2.price, _Digits),
            " R12=", DoubleToString(events[i].R12.price, _Digits),
            " N2=", DoubleToString(events[i].N2.price, _Digits));
   }

   M0007_DeleteObjectsByPrefix(InpObjectPrefix);
   M0007_DrawEvents(events, InpMaxEventsToDraw, InpDrawOnlyConfirmed, InpObjectPrefix);

   return true;
}

int OnInit()
{
   if(InpLMin < 2)
   {
      Print("DAL M0007 F1: InpLMin must be >= 2");
      return INIT_PARAMETERS_INCORRECT;
   }

   if(InpLMax < InpLMin)
   {
      Print("DAL M0007 F1: InpLMax must be >= InpLMin");
      return INIT_PARAMETERS_INCORRECT;
   }

   g_last_bar_time = iTime(_Symbol, _Period, 0);
   M0007_RunF1Detector();
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
      M0007_RunF1Detector();
   }
}

void OnDeinit(const int reason)
{
   if(InpDeleteOnDeinit)
      M0007_DeleteObjectsByPrefix(InpObjectPrefix);
}
