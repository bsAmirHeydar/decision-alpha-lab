#property strict
#include <DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Types.mqh>
#include <DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_NodeDetector.mqh>

bool H0007_BreakAbove(const MqlRates &bar, const double level, const H0007_BreakMode mode, const double eps)
{
   if(mode == H0007_BREAK_CLOSE) return (bar.close >= level + eps);
   return (bar.high >= level + eps);
}

bool H0007_BreakBelow(const MqlRates &bar, const double level, const H0007_BreakMode mode, const double eps)
{
   if(mode == H0007_BREAK_CLOSE) return (bar.close <= level - eps);
   return (bar.low <= level - eps);
}

void H0007_AddEvent(H0007_F1Event &events[], const H0007_F1Event &event)
{
   int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n] = event;
}

int H0007_EventEndIndex(const H0007_F1Event &e)
{
   if(e.confirm_index >= 0) return e.confirm_index;
   if(e.invalidation_index >= 0) return e.invalidation_index;
   return e.N2.index;
}

double H0007_EventOverlapRatio(const H0007_F1Event &a, const H0007_F1Event &b)
{
   int a0 = a.H1.index;
   int a1 = H0007_EventEndIndex(a);
   int b0 = b.H1.index;
   int b1 = H0007_EventEndIndex(b);
   int inter = MathMax(0, MathMin(a1, b1) - MathMax(a0, b0));
   int uni   = MathMax(a1, b1) - MathMin(a0, b0);
   if(uni <= 0) return 0.0;
   return ((double)inter / (double)uni);
}

void H0007_MergeAdaptiveEvents(const H0007_F1Event &raw[], const double overlap_threshold, H0007_F1Event &out[])
{
   ArrayResize(out, 0);
   int n = ArraySize(raw);
   for(int i=0; i<n; i++)
   {
      H0007_F1Event cand = raw[i];
      bool merged = false;

      for(int k=0; k<ArraySize(out); k++)
      {
         if(cand.direction != out[k].direction) continue;
         if(H0007_EventOverlapRatio(cand, out[k]) < overlap_threshold) continue;

         out[k].matched_L_values = H0007_AddLToCsv(out[k].matched_L_values, cand.L_used);
         if(cand.score > out[k].score)
         {
            string merged_l = out[k].matched_L_values;
            out[k] = cand;
            out[k].matched_L_values = H0007_AddLToCsv(merged_l, cand.L_used);
         }
         merged = true;
         break;
      }

      if(!merged)
         H0007_AddEvent(out, cand);
   }
}

void H0007_ResolveBullish(const MqlRates &rates[], const int total, H0007_F1Event &e, const H0007_BreakMode mode, const double eps)
{
   e.status = H0007_STATUS_OPEN;
   e.internal_trigger_index = -1;
   e.confirm_index = -1;
   e.invalidation_index = -1;

   for(int i=e.N2.index + 1; i<total; i++)
   {
      // Conservative same-bar ambiguity: waist violation wins before confirmation.
      if(H0007_BreakBelow(rates[i], e.W.price, mode, eps))
      {
         e.status = H0007_STATUS_INVALIDATED;
         e.invalidation_index = i;
         e.invalidation_time = rates[i].time;
         e.invalidation_price = rates[i].low;
         return;
      }

      if(e.internal_trigger_index < 0 && H0007_BreakAbove(rates[i], e.R12.price, mode, eps))
      {
         e.internal_trigger_index = i;
         e.internal_trigger_time = rates[i].time;
         e.internal_trigger_price = rates[i].high;
      }

      if(e.internal_trigger_index >= 0 && H0007_BreakAbove(rates[i], e.H2.price, mode, eps))
      {
         e.status = H0007_STATUS_CONFIRMED;
         e.confirm_index = i;
         e.confirm_time = rates[i].time;
         e.confirm_price = rates[i].high;
         return;
      }
   }
}

void H0007_ResolveBearish(const MqlRates &rates[], const int total, H0007_F1Event &e, const H0007_BreakMode mode, const double eps)
{
   e.status = H0007_STATUS_OPEN;
   e.internal_trigger_index = -1;
   e.confirm_index = -1;
   e.invalidation_index = -1;

   for(int i=e.N2.index + 1; i<total; i++)
   {
      if(H0007_BreakAbove(rates[i], e.W.price, mode, eps))
      {
         e.status = H0007_STATUS_INVALIDATED;
         e.invalidation_index = i;
         e.invalidation_time = rates[i].time;
         e.invalidation_price = rates[i].high;
         return;
      }

      if(e.internal_trigger_index < 0 && H0007_BreakBelow(rates[i], e.R12.price, mode, eps))
      {
         e.internal_trigger_index = i;
         e.internal_trigger_time = rates[i].time;
         e.internal_trigger_price = rates[i].low;
      }

      if(e.internal_trigger_index >= 0 && H0007_BreakBelow(rates[i], e.H2.price, mode, eps))
      {
         e.status = H0007_STATUS_CONFIRMED;
         e.confirm_index = i;
         e.confirm_time = rates[i].time;
         e.confirm_price = rates[i].low;
         return;
      }
   }
}

void H0007_BuildCommonEventFields(H0007_F1Event &e, const int L)
{
   e.L_used = L;
   e.matched_L_values = IntegerToString(L);
   e.bars_structure = e.N2.index - e.H1.index;
   e.bars_to_trigger = (e.internal_trigger_index >= 0 ? e.internal_trigger_index - e.N2.index : -1);
   e.bars_to_confirm = (e.confirm_index >= 0 ? e.confirm_index - e.N2.index : -1);
   double structural_height = MathAbs(e.H2.price - e.W.price);
   double count_depth = MathAbs(e.N1.price - e.N2.price);
   e.score = ((double)L * 1000000.0) + structural_height * 1000.0 + count_depth;
   e.signature = H0007_DirectionToString(e.direction) + "|" +
                 IntegerToString(e.H1.index) + "|" + IntegerToString(e.W.index) + "|" +
                 IntegerToString(e.H2.index) + "|" + IntegerToString(e.N1.index) + "|" +
                 IntegerToString(e.R12.index) + "|" + IntegerToString(e.N2.index);
}

void H0007_ScanOneL(const MqlRates &rates[], const int total, const int L, const H0007_BreakMode mode, const double eps, H0007_F1Event &raw_events[])
{
   H0007_F1Node raw_nodes[];
   H0007_F1Node nodes[];
   H0007_DetectLNodes(rates, total, L, raw_nodes);
   H0007_CompressAlternatingNodes(raw_nodes, nodes);

   int n = ArraySize(nodes);
   if(n < 6) return;

   for(int i=0; i<=n-6; i++)
   {
      H0007_F1Node A = nodes[i];
      H0007_F1Node B = nodes[i+1];
      H0007_F1Node C = nodes[i+2];
      H0007_F1Node D = nodes[i+3];
      H0007_F1Node E = nodes[i+4];
      H0007_F1Node F = nodes[i+5];

      // Bullish: H1 -> W -> H2 -> N1 -> R12 -> N2
      if(A.type == H0007_NODE_HIGH && B.type == H0007_NODE_LOW && C.type == H0007_NODE_HIGH &&
         D.type == H0007_NODE_LOW  && E.type == H0007_NODE_HIGH && F.type == H0007_NODE_LOW)
      {
         if(C.price > A.price && F.price < D.price && F.price > B.price && E.price < C.price)
         {
            H0007_F1Event ev;
            ev.direction = H0007_DIR_BULLISH;
            ev.H1 = A; ev.W = B; ev.H2 = C; ev.N1 = D; ev.R12 = E; ev.N2 = F;
            H0007_ResolveBullish(rates, total, ev, mode, eps);
            H0007_BuildCommonEventFields(ev, L);
            H0007_AddEvent(raw_events, ev);
         }
      }

      // Bearish: L1 -> W -> L2 -> N1 -> R12 -> N2
      if(A.type == H0007_NODE_LOW && B.type == H0007_NODE_HIGH && C.type == H0007_NODE_LOW &&
         D.type == H0007_NODE_HIGH && E.type == H0007_NODE_LOW  && F.type == H0007_NODE_HIGH)
      {
         if(C.price < A.price && F.price > D.price && F.price < B.price && E.price > C.price)
         {
            H0007_F1Event ev;
            ev.direction = H0007_DIR_BEARISH;
            ev.H1 = A; ev.W = B; ev.H2 = C; ev.N1 = D; ev.R12 = E; ev.N2 = F;
            H0007_ResolveBearish(rates, total, ev, mode, eps);
            H0007_BuildCommonEventFields(ev, L);
            H0007_AddEvent(raw_events, ev);
         }
      }
   }
}

void H0007_DetectAdaptiveF1(const MqlRates &rates[], const int total, const int L_min, const int L_max, const H0007_BreakMode mode, const double eps, const double overlap_threshold, H0007_F1Event &events[])
{
   H0007_F1Event raw_events[];
   ArrayResize(raw_events, 0);
   ArrayResize(events, 0);

   int fromL = MathMax(2, L_min);
   int toL = MathMax(fromL, L_max);
   for(int L=fromL; L<=toL; L++)
      H0007_ScanOneL(rates, total, L, mode, eps, raw_events);

   H0007_MergeAdaptiveEvents(raw_events, overlap_threshold, events);
}
