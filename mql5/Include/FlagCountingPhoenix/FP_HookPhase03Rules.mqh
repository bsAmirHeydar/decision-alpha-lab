#ifndef __FP_HOOK_PHASE03_RULES_MQH__
#define __FP_HOOK_PHASE03_RULES_MQH__
#property strict

#include "FP_HookPhase03Types.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

bool FP_HookP03ShouldRun(const FP_HookPhase03Config &cfg)
{
   return AL_UC04ShouldRun(
      cfg.enabled,
      (int)cfg.display_family,
      (int)FP_NDS_HOOK_DISPLAY_RALLY_ONLY
   );
}

bool FP_HookP03DirectionAllowed(const FP_HookPhase03Config &cfg,
                                const FP_HookPhase02Direction d)
{
   return AL_UC04DirectionAllowed(
      cfg.show_positive,
      cfg.show_negative,
      (int)d,
      (int)FP_HOOK_P02_DIRECTION_POSITIVE,
      (int)FP_HOOK_P02_DIRECTION_NEGATIVE
   );
}

void FP_HookP03FinalizeYAxisState(FP_HookPhase03YAxis &y, const int x_count)
{
   y.y_count = 0;
   if(y.has_y01) y.y_count++;
   if(y.has_y12) y.y_count++;
   if(y.has_y23) y.y_count++;
   if(y.has_y34) y.y_count++;

   if(y.y_count <= 0)
   {
      y.y_state = FP_HOOK_P03_Y_MISSING;
      y.y_state_reason = "NO_Y_EXTREMES_FOUND";
      return;
   }

   int expected = x_count;
   if(expected > 4)
      expected = 4;

   if(expected <= 0)
   {
      y.y_state = FP_HOOK_P03_Y_MISSING;
      y.y_state_reason = "NO_X_SEGMENTS";
      return;
   }

   if(y.y_count >= expected)
   {
      y.y_state = FP_HOOK_P03_Y_COMPLETE;
      y.y_state_reason = "ALL_AVAILABLE_X_SEGMENTS_HAVE_Y";
      return;
   }

   y.y_state = FP_HOOK_P03_Y_PARTIAL;
   y.y_state_reason = "SOME_X_SEGMENTS_HAVE_Y";
}

bool FP_HookP03FindOppositeExtremeBetween(const MqlRates &rates[],
                                          const int copied,
                                          const datetime t1,
                                          const datetime t2,
                                          const FP_HookPhase02Direction direction,
                                          int &bar_index,
                                          datetime &bar_time,
                                          double &price)
{
   bar_index = -1;
   bar_time = 0;
   price = 0.0;

   if(copied <= 0 || t1 <= 0 || t2 <= 0 || t1 == t2)
      return false;

   datetime a = t1;
   datetime b = t2;
   if(a > b)
   {
      datetime tmp = a;
      a = b;
      b = tmp;
   }

   bool found = false;
   double best = 0.0;
   int best_i = -1;

   for(int i=0; i<copied; i++)
   {
      datetime bt = rates[i].time;

      // Include the segment endpoints. This is intentional for Phase 03 audit.
      // Later closure logic may decide whether endpoint inclusion should be
      // stricter for a specific calculation.
      if(bt < a || bt > b)
         continue;

      double candidate = 0.0;
      if(direction == FP_HOOK_P02_DIRECTION_POSITIVE)
         candidate = rates[i].high;
      else
         candidate = rates[i].low;

      if(!found)
      {
         found = true;
         best = candidate;
         best_i = i;
      }
      else
      {
         if(direction == FP_HOOK_P02_DIRECTION_POSITIVE && candidate > best)
         {
            best = candidate;
            best_i = i;
         }
         else if(direction == FP_HOOK_P02_DIRECTION_NEGATIVE && candidate < best)
         {
            best = candidate;
            best_i = i;
         }
      }
   }

   if(!found || best_i < 0)
      return false;

   bar_index = best_i;
   bar_time = rates[best_i].time;
   price = best;
   return true;
}

void FP_HookP03SetYSlot(FP_HookPhase03YAxis &y,
                        const int slot,
                        const bool has_value,
                        const int bar_index,
                        const datetime bar_time,
                        const double price)
{
   if(slot == 1)
   {
      y.has_y01 = has_value;
      y.y01_bar_index = bar_index;
      y.y01_time = bar_time;
      y.y01_price = price;
   }
   else if(slot == 2)
   {
      y.has_y12 = has_value;
      y.y12_bar_index = bar_index;
      y.y12_time = bar_time;
      y.y12_price = price;
   }
   else if(slot == 3)
   {
      y.has_y23 = has_value;
      y.y23_bar_index = bar_index;
      y.y23_time = bar_time;
      y.y23_price = price;
   }
   else if(slot == 4)
   {
      y.has_y34 = has_value;
      y.y34_bar_index = bar_index;
      y.y34_time = bar_time;
      y.y34_price = price;
   }
}

bool FP_HookP03GetXBoundaryTimes(const FP_HookPhase02Sequence &seq,
                                 const int segment,
                                 datetime &t1,
                                 datetime &t2)
{
   t1 = 0;
   t2 = 0;

   if(segment == 1 && seq.x_count >= 1)
   {
      t1 = seq.origin_time;
      t2 = seq.x1_time;
      return true;
   }

   if(segment == 2 && seq.x_count >= 2)
   {
      t1 = seq.x1_time;
      t2 = seq.x2_time;
      return true;
   }

   if(segment == 3 && seq.x_count >= 3)
   {
      t1 = seq.x2_time;
      t2 = seq.x3_time;
      return true;
   }

   if(segment == 4 && seq.x_count >= 4)
   {
      t1 = seq.x3_time;
      t2 = seq.x4_time;
      return true;
   }

   return false;
}

void FP_HookP03BuildYAxisForSequence(const MqlRates &rates[],
                                     const int copied,
                                     const FP_HookPhase02Sequence &seq,
                                     FP_HookPhase03YAxis &y)
{
   FP_ResetHookPhase03YAxis(y);

   for(int segment=1; segment<=4; segment++)
   {
      datetime t1, t2;
      if(!FP_HookP03GetXBoundaryTimes(seq, segment, t1, t2))
         continue;

      int bar_index;
      datetime bar_time;
      double price;

      bool ok = FP_HookP03FindOppositeExtremeBetween(rates, copied, t1, t2,
                                                     seq.direction,
                                                     bar_index, bar_time, price);

      FP_HookP03SetYSlot(y, segment, ok, bar_index, bar_time, price);
   }

   FP_HookP03FinalizeYAxisState(y, seq.x_count);
}

bool FP_HookP03AppendRecord(FP_HookPhase03Record &records[],
                            const FP_HookPhase03Record &record)
{
   int n = ArraySize(records);
   ArrayResize(records, n + 1);
   records[n] = record;
   return true;
}

void FP_HookP03BuildRecords(const MqlRates &rates[],
                            const int copied,
                            const FP_HookPhase02Sequence &sequences[],
                            const FP_HookPhase03Config &cfg,
                            FP_HookPhase03Record &records[],
                            FP_HookPhase03Report &report)
{
   ArrayResize(records, 0);
   report.phase02_sequences_seen = ArraySize(sequences);

   for(int i=0; i<ArraySize(sequences); i++)
   {
      FP_HookPhase02Sequence seq = sequences[i];

      if(!seq.valid)
         continue;

      if(!FP_HookP03DirectionAllowed(cfg, seq.direction))
         continue;

      FP_HookPhase03Record rec;
      FP_ResetHookPhase03Record(rec);
      rec.sequence = seq;
      FP_HookP03BuildYAxisForSequence(rates, copied, seq, rec.y_axis);
      rec.valid = true;

      FP_HookP03AppendRecord(records, rec);

      report.records_total++;
      if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
         report.records_positive++;
      else
         report.records_negative++;

      if(rec.y_axis.has_y01) report.y01_count++;
      if(rec.y_axis.has_y12) report.y12_count++;
      if(rec.y_axis.has_y23) report.y23_count++;
      if(rec.y_axis.has_y34) report.y34_count++;

      if(rec.y_axis.y_state == FP_HOOK_P03_Y_COMPLETE)
         report.y_complete_count++;
      else if(rec.y_axis.y_state == FP_HOOK_P03_Y_PARTIAL)
         report.y_partial_count++;
      else if(rec.y_axis.y_state == FP_HOOK_P03_Y_MISSING)
         report.y_missing_count++;
   }
}

void FP_HookP03FinalizeReport(FP_HookPhase03Report &report)
{
   report.ok = true;
   report.status = "HOOK_P03_OK";
   report.reason = "Y_AXIS_OPPOSITE_EXTREMES_BUILT";

   if(report.phase02_sequences_seen <= 0)
   {
      report.status = "HOOK_P03_NO_PHASE02_SEQUENCES";
      report.reason = "NO_X_SEQUENCES_FOR_Y_AXIS";
   }
   else if(report.records_total <= 0)
   {
      report.status = "HOOK_P03_NO_RECORDS";
      report.reason = "NO_VALID_Y_AXIS_RECORDS";
   }
}

void FP_PrintHookPhase03Report(const string tag, const FP_HookPhase03Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP03BoolName(r.attempted),
         " ok=", FP_HookP03BoolName(r.ok),
         " bars_seen=", r.bars_seen,
         " bars_scanned=", r.bars_scanned,
         " scales_seen=", r.scales_seen,
         " nodes_seen=", r.nodes_seen,
         " p02_sequences=", r.phase02_sequences_seen,
         " records=", r.records_total,
         " positive=", r.records_positive,
         " negative=", r.records_negative,
         " y01=", r.y01_count,
         " y12=", r.y12_count,
         " y23=", r.y23_count,
         " y34=", r.y34_count,
         " complete=", r.y_complete_count,
         " partial=", r.y_partial_count,
         " missing=", r.y_missing_count,
         " drawn=", r.records_drawn,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase03Samples(const string tag,
                                const FP_HookPhase03Record &records[],
                                const int sample_limit)
{
   int n = ArraySize(records);
   int limit = sample_limit;
   if(limit <= 0 || limit > n)
      limit = n;

   for(int i=0; i<limit; i++)
   {
      FP_HookPhase03Record r = records[i];

      Print(tag,
            " sample=", i,
            " sequence_id=", r.sequence.sequence_id,
            " direction=", FP_HookP02DirectionName(r.sequence.direction),
            " L=", r.sequence.scale_l,
            " X=", r.sequence.x_count,
            " Y_state=", FP_HookP03YStateName(r.y_axis.y_state),
            " Y_count=", r.y_axis.y_count,
            " y01=", DoubleToString(r.y_axis.y01_price, _Digits),
            " y12=", DoubleToString(r.y_axis.y12_price, _Digits),
            " y23=", DoubleToString(r.y_axis.y23_price, _Digits),
            " y34=", DoubleToString(r.y_axis.y34_price, _Digits));
   }
}

#endif // __FP_HOOK_PHASE03_RULES_MQH__
