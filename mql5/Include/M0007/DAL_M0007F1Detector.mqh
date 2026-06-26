#ifndef __DAL_M0007_F1_DETECTOR_MQH__
#define __DAL_M0007_F1_DETECTOR_MQH__
#property strict
#include <M0007/DAL_M0007F1Types.mqh>
#include <M0007/DAL_M0007F1NodeDetector.mqh>

bool M0007_BreakAbove(const MqlRates &bar, const double level, const M0007_BreakMode mode, const double eps)
{
   if(mode == M0007_BREAK_CLOSE) return (bar.close >= level + eps);
   return (bar.high >= level + eps);
}

bool M0007_BreakBelow(const MqlRates &bar, const double level, const M0007_BreakMode mode, const double eps)
{
   if(mode == M0007_BREAK_CLOSE) return (bar.close <= level - eps);
   return (bar.low <= level - eps);
}

void M0007_AddEvent(M0007_F1Event &events[], const M0007_F1Event &event)
{
   int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n] = event;
}

int M0007_EventEndIndex(const M0007_F1Event &e)
{
   if(e.confirm_index >= 0) return e.confirm_index;
   if(e.invalidation_index >= 0) return e.invalidation_index;
   return e.H2.index;
}

double M0007_EventOverlapRatio(const M0007_F1Event &a, const M0007_F1Event &b)
{
   int a0 = a.Start.index;
   int a1 = M0007_EventEndIndex(a);
   int b0 = b.Start.index;
   int b1 = M0007_EventEndIndex(b);
   int inter = MathMax(0, MathMin(a1, b1) - MathMax(a0, b0));
   int uni   = MathMax(a1, b1) - MathMin(a0, b0);
   if(uni <= 0) return 0.0;
   return ((double)inter / (double)uni);
}

void M0007_MergeAdaptiveEvents(const M0007_F1Event &raw[], const double overlap_threshold, M0007_F1Event &out[])
{
   ArrayResize(out, 0);
   int n = ArraySize(raw);
   for(int i=0; i<n; i++)
   {
      M0007_F1Event cand = raw[i];
      bool merged = false;

      for(int k=0; k<ArraySize(out); k++)
      {
         if(cand.direction != out[k].direction) continue;
         if(M0007_EventOverlapRatio(cand, out[k]) < overlap_threshold) continue;

         string merged_l = M0007_AddLToCsv(out[k].matched_L_values, cand.L_used);
         if(cand.score > out[k].score)
         {
            out[k] = cand;
            out[k].matched_L_values = M0007_AddLToCsv(merged_l, cand.L_used);
         }
         else
         {
            out[k].matched_L_values = merged_l;
         }
         merged = true;
         break;
      }

      if(!merged)
         M0007_AddEvent(out, cand);
   }
}

void M0007_MarkConfirmedAtLeg2(M0007_F1Event &e)
{
   e.status = M0007_STATUS_CONFIRMED;

   e.internal_trigger_index = e.H2.index;
   e.internal_trigger_time  = e.H2.time;
   e.internal_trigger_price = e.H2.price;

   e.confirm_index = e.H2.index;
   e.confirm_time  = e.H2.time;
   e.confirm_price = e.H2.price;

   e.invalidation_index = -1;
   e.invalidation_time  = 0;
   e.invalidation_price = 0.0;
}

void M0007_BuildCommonEventFields(M0007_F1Event &e, const int L)
{
   e.L_used = L;
   e.matched_L_values = IntegerToString(L);
   e.bars_structure = e.H2.index - e.Start.index;
   e.bars_to_trigger = (e.internal_trigger_index >= 0 ? e.internal_trigger_index - e.W.index : -1);
   e.bars_to_confirm = (e.confirm_index >= 0 ? e.confirm_index - e.Start.index : -1);

   double leg1_size = MathAbs(e.H1.price - e.Start.price);
   double corr_size = MathAbs(e.H1.price - e.W.price);
   double leg2_size = MathAbs(e.H2.price - e.W.price);
   double break_size = MathAbs(e.H2.price - e.H1.price);
   double correction_quality = 0.0;
   if(leg1_size > 0.0)
      correction_quality = MathMax(0.0, 1.0 - (corr_size / leg1_size));

   e.score = ((double)L * 1000000.0) +
             leg2_size * 1000.0 +
             break_size * 10000.0 +
             correction_quality * 100.0;

   e.signature = M0007_DirectionToString(e.direction) + "|F1_4NODE|" +
                 IntegerToString(e.Start.index) + "|" +
                 IntegerToString(e.H1.index) + "|" +
                 IntegerToString(e.W.index) + "|" +
                 IntegerToString(e.H2.index);
}

void M0007_SetLegacySlots(M0007_F1Event &e)
{
   // Legacy slots are populated with semantic equivalents so older logging code remains safe.
   e.N1  = e.W;
   e.R12 = e.H2;
   e.N2  = e.H2;
}

bool M0007_IsBullishF1FourNode(const MqlRates &rates[], const M0007_F1Node &A, const M0007_F1Node &B, const M0007_F1Node &C, const M0007_F1Node &D, const M0007_BreakMode mode, const double eps)
{
   if(A.type != M0007_NODE_LOW)  return false;
   if(B.type != M0007_NODE_HIGH) return false;
   if(C.type != M0007_NODE_LOW)  return false;
   if(D.type != M0007_NODE_HIGH) return false;

   // Real F1 origin logic: the start is the low before Leg 1, not a synthetic point.
   if(B.price <= A.price) return false;
   if(C.price >= B.price) return false;
   if(C.price <= A.price) return false;      // correction must stay above the origin low.
   if(D.price <= B.price + eps) return false; // Leg 2 must break/sweep the Leg 1 high.

   if(!M0007_BreakAbove(rates[D.index], B.price, mode, eps))
      return false;

   return true;
}

bool M0007_IsBearishF1FourNode(const MqlRates &rates[], const M0007_F1Node &A, const M0007_F1Node &B, const M0007_F1Node &C, const M0007_F1Node &D, const M0007_BreakMode mode, const double eps)
{
   if(A.type != M0007_NODE_HIGH) return false;
   if(B.type != M0007_NODE_LOW)  return false;
   if(C.type != M0007_NODE_HIGH) return false;
   if(D.type != M0007_NODE_LOW)  return false;

   // Real F1 origin logic: the start is the high before Leg 1, not a synthetic point.
   if(B.price >= A.price) return false;
   if(C.price <= B.price) return false;
   if(C.price >= A.price) return false;      // correction must stay below the origin high.
   if(D.price >= B.price - eps) return false; // Leg 2 must break/sweep the Leg 1 low.

   if(!M0007_BreakBelow(rates[D.index], B.price, mode, eps))
      return false;

   return true;
}

void M0007_ScanOneL(const MqlRates &rates[], const int total, const int L, const M0007_BreakMode mode, const double eps, M0007_F1Event &raw_events[])
{
   M0007_F1Node raw_nodes[];
   M0007_F1Node nodes[];
   M0007_DetectLNodes(rates, total, L, raw_nodes);
   M0007_CompressAlternatingNodes(raw_nodes, nodes);

   int n = ArraySize(nodes);
   if(n < 4) return;

   for(int i=0; i<=n-4; i++)
   {
      M0007_F1Node A = nodes[i];     // true origin / start
      M0007_F1Node B = nodes[i+1];   // end of Leg 1
      M0007_F1Node C = nodes[i+2];   // correction
      M0007_F1Node D = nodes[i+3];   // end of Leg 2

      if(M0007_IsBullishF1FourNode(rates, A, B, C, D, mode, eps))
      {
         M0007_F1Event ev;
         ev.direction = M0007_DIR_BULLISH;
         ev.Start = A;
         ev.H1 = B;
         ev.W  = C;
         ev.H2 = D;
         M0007_SetLegacySlots(ev);
         M0007_MarkConfirmedAtLeg2(ev);
         M0007_BuildCommonEventFields(ev, L);
         M0007_AddEvent(raw_events, ev);
      }

      if(M0007_IsBearishF1FourNode(rates, A, B, C, D, mode, eps))
      {
         M0007_F1Event ev;
         ev.direction = M0007_DIR_BEARISH;
         ev.Start = A;
         ev.H1 = B;
         ev.W  = C;
         ev.H2 = D;
         M0007_SetLegacySlots(ev);
         M0007_MarkConfirmedAtLeg2(ev);
         M0007_BuildCommonEventFields(ev, L);
         M0007_AddEvent(raw_events, ev);
      }
   }
}

void M0007_DetectAdaptiveF1(const MqlRates &rates[], const int total, const int L_min, const int L_max, const M0007_BreakMode mode, const double eps, const double overlap_threshold, M0007_F1Event &events[])
{
   M0007_F1Event raw_events[];
   ArrayResize(raw_events, 0);
   ArrayResize(events, 0);

   int fromL = MathMax(2, L_min);
   int toL = MathMax(fromL, L_max);
   for(int L=fromL; L<=toL; L++)
      M0007_ScanOneL(rates, total, L, mode, eps, raw_events);

   M0007_MergeAdaptiveEvents(raw_events, overlap_threshold, events);
}

#endif
