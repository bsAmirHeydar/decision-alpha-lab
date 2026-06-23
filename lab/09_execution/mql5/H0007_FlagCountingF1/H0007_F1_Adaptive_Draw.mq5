#property strict
#property script_show_inputs

#include "Include/H0007_F1_Types.mqh"
#include "Include/H0007_F1_Detector.mqh"
#include "Include/H0007_F1_Renderer.mqh"

input int               InpBarsToScan       = 3000;
input int               InpLMin             = 2;
input int               InpLMax             = 8;
input H0007_BreakMode   InpBreakMode        = H0007_BREAK_WICK;
input double            InpEpsilonPoints    = 0.0;
input double            InpOverlapThreshold = 0.60;
input int               InpMaxEventsToDraw  = 20;
input bool              InpDrawOnlyConfirmed= true;
input string            InpObjectPrefix     = "H0007_F1_";

void H0007_ReverseRates(MqlRates &rates[])
{
   int n = ArraySize(rates);
   for(int i=0; i<n/2; i++)
   {
      MqlRates tmp = rates[i];
      rates[i] = rates[n-1-i];
      rates[n-1-i] = tmp;
   }
}

void OnStart()
{
   MqlRates rates[];
   int copied = CopyRates(_Symbol, _Period, 0, InpBarsToScan, rates);
   if(copied <= 0)
   {
      Print("H0007 F1: CopyRates failed. error=", GetLastError());
      return;
   }

   ArrayResize(rates, copied);
   if(copied > 1 && rates[0].time > rates[copied-1].time)
      H0007_ReverseRates(rates);

   H0007_F1Event events[];
   double eps = InpEpsilonPoints * _Point;

   H0007_DetectAdaptiveF1(
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
      if(events[i].status == H0007_STATUS_CONFIRMED) confirmed++;
      else if(events[i].status == H0007_STATUS_INVALIDATED) invalidated++;
      else open++;
   }

   Print("H0007 F1 Adaptive Draw | symbol=", _Symbol,
         " tf=", EnumToString(_Period),
         " bars=", copied,
         " L=", InpLMin, "..", InpLMax,
         " total=", total,
         " confirmed=", confirmed,
         " invalidated=", invalidated,
         " open=", open);

   for(int i=MathMax(0,total-10); i<total; i++)
   {
      Print("H0007_EVENT ", i,
            " dir=", H0007_DirectionToString(events[i].direction),
            " status=", H0007_StatusToString(events[i].status),
            " L_used=", events[i].L_used,
            " matched_L=", events[i].matched_L_values,
            " H1/L1=", TimeToString(events[i].H1.time, TIME_DATE|TIME_MINUTES), "@", DoubleToString(events[i].H1.price, _Digits),
            " W=", DoubleToString(events[i].W.price, _Digits),
            " H2/L2=", DoubleToString(events[i].H2.price, _Digits),
            " R12=", DoubleToString(events[i].R12.price, _Digits),
            " N2=", DoubleToString(events[i].N2.price, _Digits));
   }

   H0007_DeleteObjectsByPrefix(InpObjectPrefix);
   H0007_DrawEvents(events, InpMaxEventsToDraw, InpDrawOnlyConfirmed, InpObjectPrefix);
}
