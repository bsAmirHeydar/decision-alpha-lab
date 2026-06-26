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


bool M0007_WaistBrokenByBar(const MqlRates &bar,
                            const M0007_F1Direction direction,
                            const double waist_level,
                            const double eps,
                            double &break_price)
{
   break_price = 0.0;
   if(direction == M0007_DIR_BULLISH)
   {
      if(bar.low <= waist_level - eps)
      {
         break_price = bar.low;
         return true;
      }
      return false;
   }

   if(direction == M0007_DIR_BEARISH)
   {
      if(bar.high >= waist_level + eps)
      {
         break_price = bar.high;
         return true;
      }
      return false;
   }

   return false;
}

bool M0007_FindWaistBreakInBars(const MqlRates &rates[],
                                const int total,
                                const int from_index,
                                const int to_index,
                                const M0007_F1Direction direction,
                                const double waist_level,
                                const double eps,
                                int &break_index,
                                datetime &break_time,
                                double &break_price)
{
   break_index = -1;
   break_time = 0;
   break_price = 0.0;

   int a = MathMax(0, from_index);
   int b = MathMin(total - 1, to_index);
   if(a > b) return false;

   for(int k=a; k<=b; k++)
   {
      double p;
      if(M0007_WaistBrokenByBar(rates[k], direction, waist_level, eps, p))
      {
         break_index = k;
         break_time = rates[k].time;
         break_price = p;
         return true;
      }
   }

   return false;
}

void M0007_AddEvent(M0007_F1Event &events[], const M0007_F1Event &event)
{
   int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n] = event;
}

int M0007_EventEndIndex(const M0007_F1Event &e)
{
   int end_idx = e.H2.index;
   if(e.has_internal_2) end_idx = MathMax(end_idx, e.N2.index);
   else if(e.has_internal_1) end_idx = MathMax(end_idx, e.N1.index);

   if(e.confirm_index >= 0) end_idx = MathMax(end_idx, e.confirm_index);
   if(e.invalidation_index >= 0) end_idx = MathMax(end_idx, e.invalidation_index);
   return end_idx;
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

bool M0007_SameCoreF1(const M0007_F1Event &a, const M0007_F1Event &b)
{
   return (a.direction == b.direction &&
           a.Start.time == b.Start.time &&
           a.H1.time == b.H1.time &&
           a.W.time == b.W.time &&
           a.H2.time == b.H2.time);
}

int M0007_StatusRank(const M0007_F1Status s)
{
   if(s == M0007_STATUS_INVALIDATED) return 30; // invalidated must win so stale live objects can be deleted.
   if(s == M0007_STATUS_CONFIRMED)   return 20;
   return 10;
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

         bool same_core = M0007_SameCoreF1(cand, out[k]);
         if(!same_core && M0007_EventOverlapRatio(cand, out[k]) < overlap_threshold)
            continue;

         string merged_l = M0007_AddLToCsv(out[k].matched_L_values, cand.L_used);

         // Same mechanical F1 must keep a single object identity on chart.
         // Invalidated wins over stale OPEN/CONFIRMED variants so that the renderer can delete it.
         if(same_core)
         {
            int cr = M0007_StatusRank(cand.status);
            int orr = M0007_StatusRank(out[k].status);
            if(cr > orr || (cr == orr && cand.score > out[k].score))
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

void M0007_MarkCompletedAtLeg2(M0007_F1Event &e)
{
   // H2/L2 is structural completion, not final confirmation when leg-2-break confirmation is enabled.
   e.internal_trigger_index = e.H2.index;
   e.internal_trigger_time  = e.H2.time;
   e.internal_trigger_price = e.H2.price;

   e.invalidation_index = -1;
   e.invalidation_time  = 0;
   e.invalidation_price = 0.0;
}

void M0007_MarkConfirmedAtLeg2(M0007_F1Event &e)
{
   // Backward-compatible mode: consider F1 confirmed as soon as H2/L2 exists.
   M0007_MarkCompletedAtLeg2(e);
   e.status = M0007_STATUS_CONFIRMED;

   e.leg2_break_index = e.H2.index;
   e.leg2_break_time  = e.H2.time;
   e.leg2_break_price = e.H2.price;

   e.confirm_index = e.H2.index;
   e.confirm_time  = e.H2.time;
   e.confirm_price = e.H2.price;
}


void M0007_MarkInvalidatedAtWaistBreak(M0007_F1Event &e, const int idx, const datetime t, const double price)
{
   e.status = M0007_STATUS_INVALIDATED;

   e.waist_break_index = idx;
   e.waist_break_time  = t;
   e.waist_break_price = price;

   e.invalidation_index = idx;
   e.invalidation_time  = t;
   e.invalidation_price = price;
}

void M0007_MarkConfirmedAtLeg2Break(M0007_F1Event &e, const int idx, const datetime t, const double price)
{
   M0007_MarkCompletedAtLeg2(e);
   e.status = M0007_STATUS_CONFIRMED;

   e.leg2_break_index = idx;
   e.leg2_break_time  = t;
   e.leg2_break_price = price;

   e.confirm_index = idx;
   e.confirm_time  = t;
   e.confirm_price = price;
}

bool M0007_FindLeg2RebreakAfterInternal12(const MqlRates &rates[],
                                          const int total,
                                          const int from_index,
                                          const M0007_F1Direction direction,
                                          const double leg2_level,
                                          const double waist_level,
                                          const M0007_BreakMode mode,
                                          const double eps,
                                          const bool protect_waist,
                                          int &break_index,
                                          datetime &break_time,
                                          double &break_price,
                                          int &waist_break_index,
                                          datetime &waist_break_time,
                                          double &waist_break_price)
{
   break_index = -1;
   break_time = 0;
   break_price = 0.0;
   waist_break_index = -1;
   waist_break_time = 0;
   waist_break_price = 0.0;

   int start = MathMax(0, from_index);
   for(int k=start; k<total; k++)
   {
      if(protect_waist)
      {
         double wb;
         if(M0007_WaistBrokenByBar(rates[k], direction, waist_level, eps, wb))
         {
            waist_break_index = k;
            waist_break_time = rates[k].time;
            waist_break_price = wb;
            return false;
         }
      }

      if(direction == M0007_DIR_BULLISH && M0007_BreakAbove(rates[k], leg2_level, mode, eps))
      {
         break_index = k;
         break_time = rates[k].time;
         break_price = (mode == M0007_BREAK_CLOSE ? rates[k].close : rates[k].high);
         return true;
      }

      if(direction == M0007_DIR_BEARISH && M0007_BreakBelow(rates[k], leg2_level, mode, eps))
      {
         break_index = k;
         break_time = rates[k].time;
         break_price = (mode == M0007_BREAK_CLOSE ? rates[k].close : rates[k].low);
         return true;
      }
   }

   return false;
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

   double internal_bonus = 0.0;
   if(e.has_internal_1) internal_bonus += 10.0;
   if(e.has_internal_2) internal_bonus += 25.0;
   if(e.internal_12_valid) internal_bonus += 15.0;

   double confirmation_bonus = 0.0;
   if(e.status == M0007_STATUS_CONFIRMED) confirmation_bonus = 50.0;

   e.score = ((double)L * 1000000.0) +
             leg2_size * 1000.0 +
             break_size * 10000.0 +
             correction_quality * 100.0 +
             internal_bonus +
             confirmation_bonus;

   e.signature = M0007_DirectionToString(e.direction) + "|F1_4NODE_REAL_ORIGIN|" +
                 IntegerToString(e.Start.index) + "|" +
                 IntegerToString(e.H1.index) + "|" +
                 IntegerToString(e.W.index) + "|" +
                 IntegerToString(e.H2.index);

   if(e.has_internal_1)
      e.signature += "|I1=" + IntegerToString(e.N1.index);
   if(e.has_internal_2)
      e.signature += "|I2=" + IntegerToString(e.N2.index);
}

bool M0007_IsBullishF1FourNode(const MqlRates &rates[],
                               const M0007_F1Node &A,
                               const M0007_F1Node &B,
                               const M0007_F1Node &C,
                               const M0007_F1Node &D,
                               const M0007_BreakMode mode,
                               const double eps)
{
   if(A.type != M0007_NODE_LOW)  return false;
   if(B.type != M0007_NODE_HIGH) return false;
   if(C.type != M0007_NODE_LOW)  return false;
   if(D.type != M0007_NODE_HIGH) return false;

   // Real origin: A is the actual low before the first impulse. It is never a synthetic visual point.
   if(B.price <= A.price) return false;
   if(C.price >= B.price) return false;
   if(C.price <= A.price) return false;       // correction must not violate the origin low.
   if(D.price <= B.price + eps) return false; // leg 2 must sweep/break leg 1.

   if(!M0007_BreakAbove(rates[D.index], B.price, mode, eps))
      return false;

   return true;
}

bool M0007_IsBearishF1FourNode(const MqlRates &rates[],
                               const M0007_F1Node &A,
                               const M0007_F1Node &B,
                               const M0007_F1Node &C,
                               const M0007_F1Node &D,
                               const M0007_BreakMode mode,
                               const double eps)
{
   if(A.type != M0007_NODE_HIGH) return false;
   if(B.type != M0007_NODE_LOW)  return false;
   if(C.type != M0007_NODE_HIGH) return false;
   if(D.type != M0007_NODE_LOW)  return false;

   // Real origin: A is the actual high before the first bearish impulse.
   if(B.price >= A.price) return false;
   if(C.price <= B.price) return false;
   if(C.price >= A.price) return false;       // correction must not violate the origin high.
   if(D.price >= B.price - eps) return false; // leg 2 must sweep/break leg 1.

   if(!M0007_BreakBelow(rates[D.index], B.price, mode, eps))
      return false;

   return true;
}

void M0007_FindPostLeg2InternalCounts(const MqlRates &rates[],
                                      const int total,
                                      const M0007_F1Node &nodes[],
                                      const int n,
                                      const int start_node_pos,
                                      const M0007_F1Direction direction,
                                      const double waist_level,
                                      const bool protect_waist,
                                      const double eps,
                                      M0007_F1Event &e)
{
   M0007_ResetF1Node(e.N1);
   M0007_ResetF1Node(e.R12);
   M0007_ResetF1Node(e.N2);
   e.has_internal_1 = false;
   e.has_internal_2 = false;
   e.internal_12_valid = false;
   e.waist_break_index = -1;
   e.waist_break_time = 0;
   e.waist_break_price = 0.0;

   int scan_from_bar = e.H2.index + 1;

   if(direction == M0007_DIR_BULLISH)
   {
      // After a bullish F1 completes at H2, internal 1/2 is two descending lows.
      // Those internal lows must stay above the flag waist W. If they break W,
      // this is not a valid F1 continuation setup.
      for(int j=start_node_pos; j<n; j++)
      {
         if(nodes[j].index < scan_from_bar)
            continue;

         if(protect_waist)
         {
            int wb_idx;
            datetime wb_time;
            double wb_price;
            if(M0007_FindWaistBreakInBars(rates, total, scan_from_bar, nodes[j].index, direction, waist_level, eps, wb_idx, wb_time, wb_price))
            {
               e.waist_break_index = wb_idx;
               e.waist_break_time = wb_time;
               e.waist_break_price = wb_price;
               return;
            }
         }

         scan_from_bar = nodes[j].index + 1;

         if(nodes[j].type != M0007_NODE_LOW)
            continue;

         if(nodes[j].price <= waist_level - eps)
         {
            e.waist_break_index = nodes[j].index;
            e.waist_break_time = nodes[j].time;
            e.waist_break_price = nodes[j].price;
            return;
         }

         if(!e.has_internal_1)
         {
            e.N1 = nodes[j];
            e.has_internal_1 = true;
            continue;
         }

         if(nodes[j].price < e.N1.price - eps)
         {
            e.N2 = nodes[j];
            e.has_internal_2 = true;
            e.internal_12_valid = true;
            return;
         }
      }
      return;
   }

   if(direction == M0007_DIR_BEARISH)
   {
      // Mirror: after a bearish F1 completes at L2, internal 1/2 is two ascending highs.
      // Those internal highs must stay below the flag waist W.
      for(int j=start_node_pos; j<n; j++)
      {
         if(nodes[j].index < scan_from_bar)
            continue;

         if(protect_waist)
         {
            int wb_idx;
            datetime wb_time;
            double wb_price;
            if(M0007_FindWaistBreakInBars(rates, total, scan_from_bar, nodes[j].index, direction, waist_level, eps, wb_idx, wb_time, wb_price))
            {
               e.waist_break_index = wb_idx;
               e.waist_break_time = wb_time;
               e.waist_break_price = wb_price;
               return;
            }
         }

         scan_from_bar = nodes[j].index + 1;

         if(nodes[j].type != M0007_NODE_HIGH)
            continue;

         if(nodes[j].price >= waist_level + eps)
         {
            e.waist_break_index = nodes[j].index;
            e.waist_break_time = nodes[j].time;
            e.waist_break_price = nodes[j].price;
            return;
         }

         if(!e.has_internal_1)
         {
            e.N1 = nodes[j];
            e.has_internal_1 = true;
            continue;
         }

         if(nodes[j].price > e.N1.price + eps)
         {
            e.N2 = nodes[j];
            e.has_internal_2 = true;
            e.internal_12_valid = true;
            return;
         }
      }
   }
}

void M0007_ScanOneL(const MqlRates &rates[],
                    const int total,
                    const int L,
                    const M0007_BreakMode mode,
                    const double eps,
                    const bool require_leg2_break_for_confirm,
                    const bool require_internal_12_for_f1,
                    const bool protect_waist_during_internal_12,
                    M0007_F1Event &raw_events[])
{
   M0007_F1Node raw_nodes[];
   M0007_F1Node nodes[];
   M0007_DetectLNodes(rates, total, L, raw_nodes);
   M0007_CompressAlternatingNodes(raw_nodes, nodes);

   int n = ArraySize(nodes);
   if(n < 4) return;

   for(int i=0; i<=n-4; i++)
   {
      M0007_F1Node A = nodes[i];     // stored true origin / start
      M0007_F1Node B = nodes[i+1];   // end of leg 1
      M0007_F1Node C = nodes[i+2];   // correction
      M0007_F1Node D = nodes[i+3];   // end of leg 2

      if(M0007_IsBullishF1FourNode(rates, A, B, C, D, mode, eps))
      {
         M0007_F1Event ev;
         M0007_InitF1Event(ev);
         ev.direction = M0007_DIR_BULLISH;
         ev.Start = A;
         ev.H1 = B;
         ev.W  = C;
         ev.H2 = D;
         M0007_MarkCompletedAtLeg2(ev);
         M0007_FindPostLeg2InternalCounts(rates, total, nodes, n, i+4, ev.direction, ev.W.price, protect_waist_during_internal_12, eps, ev);

         // If the waist is broken after Leg2, this exact F1 object must be returned as INVALIDATED
         // so the renderer can delete any stale pending drawing with the same stable key.
         if(protect_waist_during_internal_12 && ev.waist_break_index >= 0)
         {
            M0007_MarkInvalidatedAtWaistBreak(ev, ev.waist_break_index, ev.waist_break_time, ev.waist_break_price);
            M0007_BuildCommonEventFields(ev, L);
            M0007_AddEvent(raw_events, ev);
            continue;
         }

         bool can_attempt_final_confirm = (!require_internal_12_for_f1 || ev.internal_12_valid);

         if(require_leg2_break_for_confirm && can_attempt_final_confirm)
         {
            int br_idx;
            datetime br_time;
            double br_price;
            int wb_idx;
            datetime wb_time;
            double wb_price;
            int from_idx = (ev.internal_12_valid ? ev.N2.index + 1 : D.index + 1);
            if(M0007_FindLeg2RebreakAfterInternal12(rates, total, from_idx, ev.direction, D.price, ev.W.price, mode, eps, protect_waist_during_internal_12, br_idx, br_time, br_price, wb_idx, wb_time, wb_price))
               M0007_MarkConfirmedAtLeg2Break(ev, br_idx, br_time, br_price);
            else if(wb_idx >= 0)
               M0007_MarkInvalidatedAtWaistBreak(ev, wb_idx, wb_time, wb_price);
         }
         else if(!require_leg2_break_for_confirm && can_attempt_final_confirm)
         {
            M0007_MarkConfirmedAtLeg2(ev);
         }

         M0007_BuildCommonEventFields(ev, L);
         M0007_AddEvent(raw_events, ev);
      }

      if(M0007_IsBearishF1FourNode(rates, A, B, C, D, mode, eps))
      {
         M0007_F1Event ev;
         M0007_InitF1Event(ev);
         ev.direction = M0007_DIR_BEARISH;
         ev.Start = A;
         ev.H1 = B;
         ev.W  = C;
         ev.H2 = D;
         M0007_MarkCompletedAtLeg2(ev);
         M0007_FindPostLeg2InternalCounts(rates, total, nodes, n, i+4, ev.direction, ev.W.price, protect_waist_during_internal_12, eps, ev);

         // If the waist is broken after Leg2, this exact F1 object must be returned as INVALIDATED
         // so the renderer can delete any stale pending drawing with the same stable key.
         if(protect_waist_during_internal_12 && ev.waist_break_index >= 0)
         {
            M0007_MarkInvalidatedAtWaistBreak(ev, ev.waist_break_index, ev.waist_break_time, ev.waist_break_price);
            M0007_BuildCommonEventFields(ev, L);
            M0007_AddEvent(raw_events, ev);
            continue;
         }

         bool can_attempt_final_confirm = (!require_internal_12_for_f1 || ev.internal_12_valid);

         if(require_leg2_break_for_confirm && can_attempt_final_confirm)
         {
            int br_idx;
            datetime br_time;
            double br_price;
            int wb_idx;
            datetime wb_time;
            double wb_price;
            int from_idx = (ev.internal_12_valid ? ev.N2.index + 1 : D.index + 1);
            if(M0007_FindLeg2RebreakAfterInternal12(rates, total, from_idx, ev.direction, D.price, ev.W.price, mode, eps, protect_waist_during_internal_12, br_idx, br_time, br_price, wb_idx, wb_time, wb_price))
               M0007_MarkConfirmedAtLeg2Break(ev, br_idx, br_time, br_price);
            else if(wb_idx >= 0)
               M0007_MarkInvalidatedAtWaistBreak(ev, wb_idx, wb_time, wb_price);
         }
         else if(!require_leg2_break_for_confirm && can_attempt_final_confirm)
         {
            M0007_MarkConfirmedAtLeg2(ev);
         }

         M0007_BuildCommonEventFields(ev, L);
         M0007_AddEvent(raw_events, ev);
      }
   }
}

void M0007_DetectAdaptiveF1(const MqlRates &rates[],
                            const int total,
                            const int L_min,
                            const int L_max,
                            const M0007_BreakMode mode,
                            const double eps,
                            const double overlap_threshold,
                            const bool require_leg2_break_for_confirm,
                            const bool require_internal_12_for_f1,
                            const bool protect_waist_during_internal_12,
                            M0007_F1Event &events[])
{
   M0007_F1Event raw_events[];
   ArrayResize(raw_events, 0);
   ArrayResize(events, 0);

   int fromL = MathMax(2, L_min);
   int toL = MathMax(fromL, L_max);
   for(int L=fromL; L<=toL; L++)
      M0007_ScanOneL(rates, total, L, mode, eps, require_leg2_break_for_confirm, require_internal_12_for_f1, protect_waist_during_internal_12, raw_events);

   M0007_MergeAdaptiveEvents(raw_events, overlap_threshold, events);
}

#endif
