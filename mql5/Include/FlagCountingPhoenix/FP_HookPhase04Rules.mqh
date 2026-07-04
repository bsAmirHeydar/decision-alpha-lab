#ifndef __FP_HOOK_PHASE04_RULES_MQH__
#define __FP_HOOK_PHASE04_RULES_MQH__
#property strict

#include "FP_HookPhase04Types.mqh"

bool FP_HookP04ShouldRun(const FP_HookPhase04Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY)
      return false;
   return true;
}

bool FP_HookP04DirectionAllowed(const FP_HookPhase04Config &cfg,
                                const FP_HookPhase02Direction d)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return cfg.show_positive;
   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return cfg.show_negative;
   return false;
}

double FP_HookP04ClampRatio(const double x)
{
   if(x < 0.01) return 0.01;
   if(x > 0.99) return 0.99;
   return x;
}

datetime FP_HookP04LatestXTime(const FP_HookPhase02Sequence &seq)
{
   if(seq.x_count >= 4 && seq.x4_time > 0) return seq.x4_time;
   if(seq.x_count >= 3 && seq.x3_time > 0) return seq.x3_time;
   if(seq.x_count >= 2 && seq.x2_time > 0) return seq.x2_time;
   if(seq.x_count >= 1 && seq.x1_time > 0) return seq.x1_time;
   return seq.origin_time;
}

double FP_HookP04LatestXPrice(const FP_HookPhase02Sequence &seq)
{
   if(seq.x_count >= 4 && seq.x4_time > 0) return seq.x4_price;
   if(seq.x_count >= 3 && seq.x3_time > 0) return seq.x3_price;
   if(seq.x_count >= 2 && seq.x2_time > 0) return seq.x2_price;
   if(seq.x_count >= 1 && seq.x1_time > 0) return seq.x1_price;
   return seq.origin_price;
}

bool FP_HookP04GetLatestYReference(const FP_HookPhase03YAxis &y,
                                   const int x_count,
                                   datetime &t,
                                   double &price,
                                   string &slot)
{
   t = 0;
   price = 0.0;
   slot = "";

   if(x_count >= 4 && y.has_y34)
   {
      t = y.y34_time;
      price = y.y34_price;
      slot = "Y34";
      return true;
   }

   if(x_count >= 3 && y.has_y23)
   {
      t = y.y23_time;
      price = y.y23_price;
      slot = "Y23";
      return true;
   }

   if(x_count >= 2 && y.has_y12)
   {
      t = y.y12_time;
      price = y.y12_price;
      slot = "Y12";
      return true;
   }

   if(x_count >= 1 && y.has_y01)
   {
      t = y.y01_time;
      price = y.y01_price;
      slot = "Y01";
      return true;
   }

   return false;
}

bool FP_HookP04FindAfterTimeReturnEvent(const MqlRates &rates[],
                                        const int copied,
                                        const datetime after_time,
                                        const FP_HookPhase02Direction direction,
                                        const double threshold_price,
                                        int &bar_index,
                                        datetime &bar_time,
                                        double &event_price)
{
   bar_index = -1;
   bar_time = 0;
   event_price = 0.0;

   for(int i=0; i<copied; i++)
   {
      if(rates[i].time <= after_time)
         continue;

      if(direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         if(rates[i].high >= threshold_price)
         {
            bar_index = i;
            bar_time = rates[i].time;
            event_price = rates[i].high;
            return true;
         }
      }
      else
      {
         if(rates[i].low <= threshold_price)
         {
            bar_index = i;
            bar_time = rates[i].time;
            event_price = rates[i].low;
            return true;
         }
      }
   }

   return false;
}

bool FP_HookP04FindAfterTimeClosureEvent(const MqlRates &rates[],
                                         const int copied,
                                         const datetime after_time,
                                         const FP_HookPhase02Direction direction,
                                         const double threshold_price,
                                         int &bar_index,
                                         datetime &bar_time,
                                         double &event_price)
{
   bar_index = -1;
   bar_time = 0;
   event_price = 0.0;

   for(int i=0; i<copied; i++)
   {
      if(rates[i].time <= after_time)
         continue;

      if(direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         // Positive Hook: Y is a high; closure means retrace downward from Y
         // toward origin by the selected ratio.
         if(rates[i].low <= threshold_price)
         {
            bar_index = i;
            bar_time = rates[i].time;
            event_price = rates[i].low;
            return true;
         }
      }
      else
      {
         // Negative Hook: Y is a low; closure means retrace upward from Y
         // toward origin by the selected ratio.
         if(rates[i].high >= threshold_price)
         {
            bar_index = i;
            bar_time = rates[i].time;
            event_price = rates[i].high;
            return true;
         }
      }
   }

   return false;
}

void FP_HookP04EvaluateLifecycle(const MqlRates &rates[],
                                 const int copied,
                                 const FP_HookPhase03Record &p03,
                                 const FP_HookPhase04Config &cfg,
                                 FP_HookPhase04Lifecycle &life)
{
   FP_ResetHookPhase04Lifecycle(life);

   FP_HookPhase02Sequence seq = p03.sequence;
   FP_HookPhase03YAxis y = p03.y_axis;

   life.death_boundary_price = seq.origin_price;
   life.nd_return_ratio = FP_HookP04ClampRatio(cfg.nd_return_ratio);
   life.closure_retrace_ratio = FP_HookP04ClampRatio(cfg.closure_retrace_ratio);

   life.has_required_x = (seq.x_count >= cfg.min_x_nodes_for_closure);
   life.has_required_y = (y.y_count > 0);

   datetime last_x_time = FP_HookP04LatestXTime(seq);
   double last_x_price = FP_HookP04LatestXPrice(seq);

   // -------------------------------------------------------------------------
   // ND candidate / return-toward-origin skeleton
   // -------------------------------------------------------------------------
   // With Phase 02 definitions:
   // - Positive sequence descends through valleys, so return toward origin is up.
   // - Negative sequence ascends through peaks, so return toward origin is down.
   // This is an audit skeleton, not a final trading signal.
   if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      life.nd_threshold_price = last_x_price + life.nd_return_ratio * (seq.origin_price - last_x_price);
   else
      life.nd_threshold_price = last_x_price - life.nd_return_ratio * (last_x_price - seq.origin_price);

   int ev_bar;
   datetime ev_time;
   double ev_price;

   life.nd_detected = FP_HookP04FindAfterTimeReturnEvent(rates, copied, last_x_time,
                                                         seq.direction,
                                                         life.nd_threshold_price,
                                                         ev_bar, ev_time, ev_price);
   if(life.nd_detected)
   {
      life.nd_bar_index = ev_bar;
      life.nd_time = ev_time;
      life.nd_price = ev_price;
   }

   life.origin_return_penetrated = FP_HookP04FindAfterTimeReturnEvent(rates, copied, last_x_time,
                                                                      seq.direction,
                                                                      seq.origin_price,
                                                                      ev_bar, ev_time, ev_price);
   if(life.origin_return_penetrated)
   {
      life.death_bar_index = ev_bar;
      life.death_time = ev_time;
      life.death_price = ev_price;
   }

   // -------------------------------------------------------------------------
   // X closure skeleton by 50% retracement from latest Y reference toward origin
   // -------------------------------------------------------------------------
   datetime y_ref_time;
   double y_ref_price;
   string y_ref_slot;

   if(FP_HookP04GetLatestYReference(y, seq.x_count, y_ref_time, y_ref_price, y_ref_slot))
   {
      life.x_closure_reference_y_time = y_ref_time;
      life.x_closure_reference_y_price = y_ref_price;
      life.x_closure_reference_y_slot = y_ref_slot;
      life.x_closure_candidate = life.has_required_x;

      if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         // From high Y down toward origin valley.
         life.x_closure_threshold_price =
            y_ref_price - life.closure_retrace_ratio * (y_ref_price - seq.origin_price);
      }
      else
      {
         // From low Y up toward origin peak.
         life.x_closure_threshold_price =
            y_ref_price + life.closure_retrace_ratio * (seq.origin_price - y_ref_price);
      }

      if(life.x_closure_candidate)
      {
         life.x_closed = FP_HookP04FindAfterTimeClosureEvent(rates, copied, y_ref_time,
                                                             seq.direction,
                                                             life.x_closure_threshold_price,
                                                             ev_bar, ev_time, ev_price);
         if(life.x_closed)
         {
            life.x_closure_bar_index = ev_bar;
            life.x_closure_time = ev_time;
            life.x_closure_price = ev_price;
         }
      }
   }

   // -------------------------------------------------------------------------
   // Lifecycle state priority
   // -------------------------------------------------------------------------
   if(!life.has_required_y || seq.x_count <= 0)
   {
      life.state = FP_HOOK_P04_LIFE_INSUFFICIENT_DATA;
      life.state_reason = "MISSING_X_OR_Y_FOR_LIFECYCLE";
      return;
   }

   if(life.origin_return_penetrated)
   {
      life.state = FP_HOOK_P04_LIFE_DEAD_BY_ORIGIN_RETURN;
      life.state_reason = "RETURN_PASSED_ORIGIN_BOUNDARY";
      return;
   }

   if(life.x_closed)
   {
      life.state = FP_HOOK_P04_LIFE_X_CLOSED;
      life.state_reason = "X_CLOSURE_RETRACE_THRESHOLD_REACHED";
      return;
   }

   if(life.x_closure_candidate)
   {
      life.state = FP_HOOK_P04_LIFE_X_CLOSURE_CANDIDATE;
      life.state_reason = "HAS_REQUIRED_X_AND_Y_REFERENCE";
      return;
   }

   if(life.nd_detected)
   {
      life.state = FP_HOOK_P04_LIFE_ND_CANDIDATE;
      life.state_reason = "RETURN_TOWARD_ORIGIN_THRESHOLD_REACHED";
      return;
   }

   life.state = FP_HOOK_P04_LIFE_ALIVE;
   life.state_reason = "NO_DEATH_OR_CLOSURE_EVENT_YET";
}

bool FP_HookP04AppendRecord(FP_HookPhase04Record &records[],
                            const FP_HookPhase04Record &record)
{
   int n = ArraySize(records);
   ArrayResize(records, n + 1);
   records[n] = record;
   return true;
}

void FP_HookP04BuildRecords(const MqlRates &rates[],
                            const int copied,
                            const FP_HookPhase03Record &p03_records[],
                            const FP_HookPhase04Config &cfg,
                            FP_HookPhase04Record &records[],
                            FP_HookPhase04Report &report)
{
   ArrayResize(records, 0);
   report.phase03_records_seen = ArraySize(p03_records);

   for(int i=0; i<ArraySize(p03_records); i++)
   {
      FP_HookPhase03Record p03 = p03_records[i];

      if(!p03.valid)
         continue;

      if(!FP_HookP04DirectionAllowed(cfg, p03.sequence.direction))
         continue;

      FP_HookPhase04Record rec;
      FP_ResetHookPhase04Record(rec);
      rec.p03 = p03;
      FP_HookP04EvaluateLifecycle(rates, copied, p03, cfg, rec.lifecycle);
      rec.valid = true;

      FP_HookP04AppendRecord(records, rec);

      report.records_total++;

      if(p03.sequence.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
         report.records_positive++;
      else
         report.records_negative++;

      if(rec.lifecycle.nd_detected)
         report.nd_count++;

      if(rec.lifecycle.origin_return_penetrated)
         report.death_count++;

      if(rec.lifecycle.x_closure_candidate)
         report.x_closure_candidate_count++;

      if(rec.lifecycle.x_closed)
         report.x_closed_count++;

      if(rec.lifecycle.state == FP_HOOK_P04_LIFE_ALIVE)
         report.alive_count++;

      if(rec.lifecycle.state == FP_HOOK_P04_LIFE_INSUFFICIENT_DATA)
         report.insufficient_count++;
   }
}

void FP_HookP04FinalizeReport(FP_HookPhase04Report &report)
{
   report.ok = true;
   report.status = "HOOK_P04_OK";
   report.reason = "LIFECYCLE_AND_X_CLOSURE_SKELETON_BUILT";

   if(report.phase03_records_seen <= 0)
   {
      report.status = "HOOK_P04_NO_PHASE03_RECORDS";
      report.reason = "NO_Y_AXIS_RECORDS_FOR_LIFECYCLE";
   }
   else if(report.records_total <= 0)
   {
      report.status = "HOOK_P04_NO_RECORDS";
      report.reason = "NO_VALID_LIFECYCLE_RECORDS";
   }
}

void FP_PrintHookPhase04Report(const string tag, const FP_HookPhase04Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP04BoolName(r.attempted),
         " ok=", FP_HookP04BoolName(r.ok),
         " bars_seen=", r.bars_seen,
         " bars_scanned=", r.bars_scanned,
         " scales_seen=", r.scales_seen,
         " nodes_seen=", r.nodes_seen,
         " p02_sequences=", r.phase02_sequences_seen,
         " p03_records=", r.phase03_records_seen,
         " records=", r.records_total,
         " positive=", r.records_positive,
         " negative=", r.records_negative,
         " nd=", r.nd_count,
         " death=", r.death_count,
         " closure_candidates=", r.x_closure_candidate_count,
         " x_closed=", r.x_closed_count,
         " alive=", r.alive_count,
         " insufficient=", r.insufficient_count,
         " drawn=", r.records_drawn,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase04Samples(const string tag,
                                const FP_HookPhase04Record &records[],
                                const int sample_limit)
{
   int n = ArraySize(records);
   int limit = sample_limit;
   if(limit <= 0 || limit > n)
      limit = n;

   for(int i=0; i<limit; i++)
   {
      FP_HookPhase04Record r = records[i];

      Print(tag,
            " sample=", i,
            " sequence_id=", r.p03.sequence.sequence_id,
            " direction=", FP_HookP02DirectionName(r.p03.sequence.direction),
            " L=", r.p03.sequence.scale_l,
            " X=", r.p03.sequence.x_count,
            " Y=", r.p03.y_axis.y_count,
            " state=", FP_HookP04LifecycleStateName(r.lifecycle.state),
            " nd=", FP_HookP04BoolName(r.lifecycle.nd_detected),
            " death=", FP_HookP04BoolName(r.lifecycle.origin_return_penetrated),
            " x_closed=", FP_HookP04BoolName(r.lifecycle.x_closed),
            " nd_threshold=", DoubleToString(r.lifecycle.nd_threshold_price, _Digits),
            " closure_threshold=", DoubleToString(r.lifecycle.x_closure_threshold_price, _Digits),
            " y_ref=", r.lifecycle.x_closure_reference_y_slot);
   }
}

#endif // __FP_HOOK_PHASE04_RULES_MQH__
