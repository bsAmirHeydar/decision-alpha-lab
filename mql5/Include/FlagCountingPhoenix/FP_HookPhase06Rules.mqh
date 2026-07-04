#ifndef __FP_HOOK_PHASE06_RULES_MQH__
#define __FP_HOOK_PHASE06_RULES_MQH__
#property strict

#include "FP_HookPhase06Types.mqh"

bool FP_HookP06ShouldRun(const FP_HookPhase06Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY)
      return false;
   return true;
}

bool FP_HookP06DirectionAllowed(const FP_HookPhase06Config &cfg,
                                const FP_HookPhase02Direction d)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return cfg.show_positive;
   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return cfg.show_negative;
   return false;
}

double FP_HookP06Clamp01(const double x)
{
   if(x < 0.0) return 0.0;
   if(x > 1.0) return 1.0;
   return x;
}

bool FP_HookP06YStepPass(const FP_HookPhase02Direction direction,
                         const double previous_y,
                         const double next_y)
{
   // NDS-R02 internal Y-sequence reading:
   // - Positive CycleHook: opposite highs should step lower.
   // - Negative CycleHook: opposite lows should step higher.
   // This is intentionally separate from Hook Type A/B/C, which is a broader
   // global structure classifier.
   if(direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (next_y < previous_y);
   return (next_y > previous_y);
}

void FP_HookP06EvaluateYClosure(const FP_HookPhase02Sequence &seq,
                                const FP_HookPhase03YAxis &y,
                                const FP_HookPhase06Config &cfg,
                                FP_HookPhase06Score &s)
{
   s.sufficient_y = false;
   s.y_closed = false;
   s.y_partial = false;
   s.y_state = FP_HOOK_P06_Y_INSUFFICIENT;

   if(y.has_y01 && y.has_y12)
   {
      s.y_comparisons_total++;
      s.y01_y12_passed = FP_HookP06YStepPass(seq.direction, y.y01_price, y.y12_price);
      if(s.y01_y12_passed)
         s.y_comparisons_passed++;
   }

   if(y.has_y12 && y.has_y23)
   {
      s.y_comparisons_total++;
      s.y12_y23_passed = FP_HookP06YStepPass(seq.direction, y.y12_price, y.y23_price);
      if(s.y12_y23_passed)
         s.y_comparisons_passed++;
   }

   if(y.has_y23 && y.has_y34)
   {
      s.y_comparisons_total++;
      s.y23_y34_passed = FP_HookP06YStepPass(seq.direction, y.y23_price, y.y34_price);
      if(s.y23_y34_passed)
         s.y_comparisons_passed++;
   }

   s.sufficient_y = (s.y_comparisons_total > 0);

   if(!s.sufficient_y)
   {
      s.y_state = FP_HOOK_P06_Y_INSUFFICIENT;
      s.y_strength = 0.0;
      return;
   }

   s.y_strength = FP_HookP06Clamp01((double)s.y_comparisons_passed / (double)s.y_comparisons_total);
   s.y_partial = (s.y_comparisons_passed > 0 && s.y_comparisons_passed < s.y_comparisons_total);

   int min_closed = cfg.min_y_comparisons_for_closed;
   if(min_closed < 1)
      min_closed = 1;
   if(min_closed > 3)
      min_closed = 3;

   s.y_closed = (s.y_comparisons_passed == s.y_comparisons_total &&
                 s.y_comparisons_passed >= min_closed);

   if(s.y_closed)
      s.y_state = FP_HOOK_P06_Y_CLOSED;
   else if(s.y_partial)
      s.y_state = FP_HOOK_P06_Y_PARTIAL;
   else
      s.y_state = FP_HOOK_P06_Y_NOT_CLOSED;
}

double FP_HookP06TypeStrength(const FP_HookPhase05HookType t)
{
   if(t == FP_HOOK_P05_TYPE_A) return 1.00;
   if(t == FP_HOOK_P05_TYPE_B) return 0.67;
   if(t == FP_HOOK_P05_TYPE_C) return 0.33;
   return 0.0;
}

double FP_HookP06LifecycleStrength(const FP_HookPhase04LifecycleState state)
{
   if(state == FP_HOOK_P04_LIFE_X_CLOSED) return 1.00;
   if(state == FP_HOOK_P04_LIFE_X_CLOSURE_CANDIDATE) return 0.70;
   if(state == FP_HOOK_P04_LIFE_ND_CANDIDATE) return 0.55;
   if(state == FP_HOOK_P04_LIFE_ALIVE) return 0.35;
   return 0.0;
}

FP_HookPhase06QualityBucket FP_HookP06BucketFromScore(const FP_HookPhase06Config &cfg,
                                                      const FP_HookPhase06Score &s)
{
   if(s.dead || s.xy_state == FP_HOOK_P06_XY_INSUFFICIENT)
      return FP_HOOK_P06_QUALITY_INVALID;
   if(s.quality_score >= cfg.elite_threshold)
      return FP_HOOK_P06_QUALITY_ELITE;
   if(s.quality_score >= cfg.high_threshold)
      return FP_HOOK_P06_QUALITY_HIGH;
   if(s.quality_score >= cfg.medium_threshold)
      return FP_HOOK_P06_QUALITY_MEDIUM;
   if(s.quality_score >= cfg.low_threshold)
      return FP_HOOK_P06_QUALITY_LOW;
   return FP_HOOK_P06_QUALITY_INVALID;
}

void FP_HookP06ChooseAnchor(const FP_HookPhase05Record &p05,
                            FP_HookPhase06Score &s)
{
   FP_HookPhase02Sequence seq = p05.p04.p03.sequence;
   FP_HookPhase04Lifecycle life = p05.p04.lifecycle;
   FP_HookPhase03YAxis y = p05.p04.p03.y_axis;

   s.anchor_time = seq.origin_time;
   s.anchor_price = seq.origin_price;
   s.anchor_slot = "ORIGIN";

   if(life.x_closure_time > 0)
   {
      s.anchor_time = life.x_closure_time;
      s.anchor_price = life.x_closure_price;
      s.anchor_slot = "X_CLOSURE";
      return;
   }

   if(life.nd_time > 0)
   {
      s.anchor_time = life.nd_time;
      s.anchor_price = life.nd_price;
      s.anchor_slot = "ND";
      return;
   }

   if(y.has_y34)
   {
      s.anchor_time = y.y34_time;
      s.anchor_price = y.y34_price;
      s.anchor_slot = "Y34";
      return;
   }

   if(y.has_y23)
   {
      s.anchor_time = y.y23_time;
      s.anchor_price = y.y23_price;
      s.anchor_slot = "Y23";
      return;
   }

   if(y.has_y12)
   {
      s.anchor_time = y.y12_time;
      s.anchor_price = y.y12_price;
      s.anchor_slot = "Y12";
      return;
   }

   if(y.has_y01)
   {
      s.anchor_time = y.y01_time;
      s.anchor_price = y.y01_price;
      s.anchor_slot = "Y01";
   }
}

void FP_HookP06EvaluateScore(const FP_HookPhase05Record &p05,
                             const FP_HookPhase06Config &cfg,
                             FP_HookPhase06Score &s)
{
   FP_ResetHookPhase06Score(s);

   FP_HookPhase02Sequence seq = p05.p04.p03.sequence;
   FP_HookPhase03YAxis y = p05.p04.p03.y_axis;
   FP_HookPhase04Lifecycle life = p05.p04.lifecycle;
   FP_HookPhase05Classification c = p05.classification;

   s.dead = (life.state == FP_HOOK_P04_LIFE_DEAD_BY_ORIGIN_RETURN || life.origin_return_penetrated);
   s.sufficient_x = (seq.x_count >= cfg.min_x_nodes_for_quality);

   s.x_strength = FP_HookP06Clamp01((double)seq.x_count / 4.0);
   if(life.x_closure_candidate && s.x_strength < 0.75)
      s.x_strength = 0.75;
   if(life.x_closed)
      s.x_strength = 1.0;

   s.x_closed = life.x_closed;
   if(!cfg.require_x_closed_for_xy && life.x_closure_candidate)
      s.x_closed = true;

   FP_HookP06EvaluateYClosure(seq, y, cfg, s);

   s.type_strength = FP_HookP06TypeStrength(c.hook_type);
   s.lifecycle_strength = FP_HookP06LifecycleStrength(life.state);

   if(s.dead)
   {
      s.xy_state = FP_HOOK_P06_XY_DEAD_BY_ORIGIN_RETURN;
      s.reason = "DEAD_BY_ORIGIN_RETURN";
   }
   else if(!s.sufficient_x || !s.sufficient_y)
   {
      s.xy_state = FP_HOOK_P06_XY_INSUFFICIENT;
      s.reason = "INSUFFICIENT_X_OR_Y_FOR_XY_QUALITY";
   }
   else if(s.x_closed && s.y_closed)
   {
      s.xy_state = FP_HOOK_P06_XY_CLOSED;
      s.reason = "X_CLOSED_AND_Y_SEQUENCE_CLOSED";
   }
   else if(s.x_closed)
   {
      s.xy_state = FP_HOOK_P06_XY_X_ONLY;
      s.reason = "X_CLOSED_WITHOUT_Y_SEQUENCE_CLOSURE";
   }
   else if(s.y_closed)
   {
      s.xy_state = FP_HOOK_P06_XY_Y_ONLY;
      s.reason = "Y_SEQUENCE_CLOSED_WITHOUT_X_CLOSURE";
   }
   else
   {
      s.xy_state = FP_HOOK_P06_XY_OPEN;
      s.reason = "XY_OPEN_OR_PARTIAL";
   }

   double weight_sum = cfg.x_weight + cfg.y_weight + cfg.type_weight + cfg.lifecycle_weight;
   if(weight_sum <= 0.0)
      weight_sum = 1.0;

   s.quality_score = FP_HookP06Clamp01(
      (s.x_strength * cfg.x_weight +
       s.y_strength * cfg.y_weight +
       s.type_strength * cfg.type_weight +
       s.lifecycle_strength * cfg.lifecycle_weight) / weight_sum
   );

   if(s.dead || s.xy_state == FP_HOOK_P06_XY_INSUFFICIENT)
      s.quality_score = 0.0;

   s.quality_bucket = FP_HookP06BucketFromScore(cfg, s);
   FP_HookP06ChooseAnchor(p05, s);
}

bool FP_HookP06AppendRecord(FP_HookPhase06Record &records[],
                            const FP_HookPhase06Record &record)
{
   int n = ArraySize(records);
   ArrayResize(records, n + 1);
   records[n] = record;
   return true;
}

void FP_HookP06BuildRecords(const FP_HookPhase05Record &p05_records[],
                            const FP_HookPhase06Config &cfg,
                            FP_HookPhase06Record &records[],
                            FP_HookPhase06Report &report)
{
   ArrayResize(records, 0);
   report.phase05_records_seen = ArraySize(p05_records);

   for(int i=0; i<ArraySize(p05_records); i++)
   {
      FP_HookPhase05Record p05 = p05_records[i];

      if(!p05.valid)
         continue;

      if(!FP_HookP06DirectionAllowed(cfg, p05.p04.p03.sequence.direction))
         continue;

      if(!cfg.include_dead_records &&
         p05.p04.lifecycle.state == FP_HOOK_P04_LIFE_DEAD_BY_ORIGIN_RETURN)
         continue;

      FP_HookPhase06Record rec;
      FP_ResetHookPhase06Record(rec);
      rec.p05 = p05;
      FP_HookP06EvaluateScore(p05, cfg, rec.score);
      rec.valid = true;

      FP_HookP06AppendRecord(records, rec);

      report.records_total++;

      if(p05.p04.p03.sequence.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
         report.records_positive++;
      else
         report.records_negative++;

      if(rec.score.xy_state == FP_HOOK_P06_XY_CLOSED)
         report.xy_closed_count++;
      else if(rec.score.xy_state == FP_HOOK_P06_XY_X_ONLY)
         report.x_only_count++;
      else if(rec.score.xy_state == FP_HOOK_P06_XY_Y_ONLY)
         report.y_only_count++;
      else if(rec.score.xy_state == FP_HOOK_P06_XY_OPEN)
         report.open_count++;
      else if(rec.score.xy_state == FP_HOOK_P06_XY_DEAD_BY_ORIGIN_RETURN)
         report.dead_count++;
      else
         report.insufficient_count++;

      if(rec.score.y_state == FP_HOOK_P06_Y_CLOSED)
         report.y_closed_count++;
      else if(rec.score.y_state == FP_HOOK_P06_Y_PARTIAL)
         report.y_partial_count++;
      else if(rec.score.y_state == FP_HOOK_P06_Y_NOT_CLOSED)
         report.y_not_closed_count++;

      if(rec.score.quality_bucket == FP_HOOK_P06_QUALITY_ELITE)
         report.elite_count++;
      else if(rec.score.quality_bucket == FP_HOOK_P06_QUALITY_HIGH)
         report.high_count++;
      else if(rec.score.quality_bucket == FP_HOOK_P06_QUALITY_MEDIUM)
         report.medium_count++;
      else if(rec.score.quality_bucket == FP_HOOK_P06_QUALITY_LOW)
         report.low_count++;
      else
         report.invalid_count++;
   }
}

void FP_HookP06FinalizeReport(FP_HookPhase06Report &report)
{
   report.ok = true;
   report.status = "HOOK_P06_OK";
   report.reason = "XY_CLOSURE_QUALITY_SCORE_BUILT";

   if(report.phase05_records_seen <= 0)
   {
      report.status = "HOOK_P06_NO_PHASE05_RECORDS";
      report.reason = "NO_TYPE_RECORDS_FOR_XY_QUALITY";
   }
   else if(report.records_total <= 0)
   {
      report.status = "HOOK_P06_NO_RECORDS";
      report.reason = "NO_VALID_XY_QUALITY_RECORDS";
   }
}

void FP_PrintHookPhase06Report(const string tag, const FP_HookPhase06Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP06BoolName(r.attempted),
         " ok=", FP_HookP06BoolName(r.ok),
         " bars_seen=", r.bars_seen,
         " bars_scanned=", r.bars_scanned,
         " scales_seen=", r.scales_seen,
         " nodes_seen=", r.nodes_seen,
         " p02_sequences=", r.phase02_sequences_seen,
         " p03_records=", r.phase03_records_seen,
         " p04_records=", r.phase04_records_seen,
         " p05_records=", r.phase05_records_seen,
         " records=", r.records_total,
         " positive=", r.records_positive,
         " negative=", r.records_negative,
         " xy_closed=", r.xy_closed_count,
         " x_only=", r.x_only_count,
         " y_only=", r.y_only_count,
         " open=", r.open_count,
         " dead=", r.dead_count,
         " insufficient=", r.insufficient_count,
         " y_closed=", r.y_closed_count,
         " y_partial=", r.y_partial_count,
         " elite=", r.elite_count,
         " high=", r.high_count,
         " medium=", r.medium_count,
         " low=", r.low_count,
         " invalid=", r.invalid_count,
         " drawn=", r.records_drawn,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase06Samples(const string tag,
                                const FP_HookPhase06Record &records[],
                                const int sample_limit)
{
   int n = ArraySize(records);
   int limit = sample_limit;
   if(limit <= 0 || limit > n)
      limit = n;

   for(int i=0; i<limit; i++)
   {
      FP_HookPhase06Record r = records[i];
      FP_HookPhase02Sequence seq = r.p05.p04.p03.sequence;

      Print(tag,
            " sample=", i,
            " sequence_id=", seq.sequence_id,
            " direction=", FP_HookP02DirectionName(seq.direction),
            " L=", seq.scale_l,
            " X=", seq.x_count,
            " type=", FP_HookP05TypeName(r.p05.classification.hook_type),
            " y_state=", FP_HookP06YStateName(r.score.y_state),
            " xy_state=", FP_HookP06XYStateName(r.score.xy_state),
            " bucket=", FP_HookP06QualityBucketName(r.score.quality_bucket),
            " score=", DoubleToString(r.score.quality_score, 2),
            " x_str=", DoubleToString(r.score.x_strength, 2),
            " y_str=", DoubleToString(r.score.y_strength, 2),
            " type_str=", DoubleToString(r.score.type_strength, 2),
            " life_str=", DoubleToString(r.score.lifecycle_strength, 2),
            " reason=", r.score.reason);
   }
}

#endif // __FP_HOOK_PHASE06_RULES_MQH__
