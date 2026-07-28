#ifndef __FP_HOOK_PHASE05_RULES_MQH__
#define __FP_HOOK_PHASE05_RULES_MQH__
#property strict

#include "FP_HookPhase05Types.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

bool FP_HookP05ShouldRun(const FP_HookPhase05Config &cfg)
{
   return AL_UC04ShouldRun(
      cfg.enabled,
      (int)cfg.display_family,
      (int)FP_NDS_HOOK_DISPLAY_RALLY_ONLY
   );
}

bool FP_HookP05DirectionAllowed(const FP_HookPhase05Config &cfg,
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

void FP_HookP05LoadEvidence(const FP_HookPhase03YAxis &y,
                            const FP_HookPhase05Config &cfg,
                            FP_HookPhase05Classification &c)
{
   c.has_y01 = y.has_y01;
   c.has_y12 = y.has_y12;
   c.has_y23 = y.has_y23;
   c.has_y34 = y.has_y34;

   c.y01_price = y.y01_price;
   c.y12_price = y.y12_price;
   c.y23_price = y.y23_price;
   c.y34_price = y.y34_price;

   c.y01_time = y.y01_time;
   c.y12_time = y.y12_time;
   c.y23_time = y.y23_time;
   c.y34_time = y.y34_time;

   c.evidence_count = 0;
   if(c.has_y01) c.evidence_count++;
   if(c.has_y12) c.evidence_count++;
   if(c.has_y23) c.evidence_count++;
   if(c.has_y34) c.evidence_count++;

   if(c.has_y23)
   {
      c.third_y_price = c.y23_price;
      c.third_y_time = c.y23_time;
      c.third_y_slot = "Y23";
      c.used_y34_as_third = false;
   }
   else if(cfg.allow_y34_as_third_evidence && c.has_y34)
   {
      c.third_y_price = c.y34_price;
      c.third_y_time = c.y34_time;
      c.third_y_slot = "Y34";
      c.used_y34_as_third = true;
   }
   else
   {
      c.third_y_price = 0.0;
      c.third_y_time = 0;
      c.third_y_slot = "";
      c.used_y34_as_third = false;
   }
}

void FP_HookP05ClassifyPositive(FP_HookPhase05Classification &c)
{
   c.condition_first = (c.has_y01 && c.has_y12 && c.y12_price > c.y01_price);
   c.condition_second = (c.condition_first && c.third_y_time > 0 && c.third_y_price > c.y12_price);

   if(c.condition_second)
   {
      c.hook_type = FP_HOOK_P05_TYPE_A;
      c.reason = "POSITIVE_TYPE_A_Y12_GT_Y01_AND_THIRD_Y_GT_Y12";
   }
   else if(c.condition_first)
   {
      c.hook_type = FP_HOOK_P05_TYPE_B;
      c.reason = "POSITIVE_TYPE_B_Y12_GT_Y01_ONLY";
   }
   else
   {
      c.hook_type = FP_HOOK_P05_TYPE_C;
      c.reason = "POSITIVE_TYPE_C_NO_B_OR_A_STRUCTURE";
   }
}

void FP_HookP05ClassifyNegative(FP_HookPhase05Classification &c)
{
   c.condition_first = (c.has_y01 && c.has_y12 && c.y12_price < c.y01_price);
   c.condition_second = (c.condition_first && c.third_y_time > 0 && c.third_y_price < c.y12_price);

   if(c.condition_second)
   {
      c.hook_type = FP_HOOK_P05_TYPE_A;
      c.reason = "NEGATIVE_TYPE_A_Y12_LT_Y01_AND_THIRD_Y_LT_Y12";
   }
   else if(c.condition_first)
   {
      c.hook_type = FP_HOOK_P05_TYPE_B;
      c.reason = "NEGATIVE_TYPE_B_Y12_LT_Y01_ONLY";
   }
   else
   {
      c.hook_type = FP_HOOK_P05_TYPE_C;
      c.reason = "NEGATIVE_TYPE_C_NO_B_OR_A_STRUCTURE";
   }
}

void FP_HookP05FinalizeScores(FP_HookPhase05Classification &c)
{
   if(c.hook_type == FP_HOOK_P05_TYPE_A)
      c.type_rank_score = 3.0;
   else if(c.hook_type == FP_HOOK_P05_TYPE_B)
      c.type_rank_score = 2.0;
   else if(c.hook_type == FP_HOOK_P05_TYPE_C)
      c.type_rank_score = 1.0;
   else
      c.type_rank_score = 0.0;

   double conf = 0.0;
   if(c.has_y01) conf += 0.25;
   if(c.has_y12) conf += 0.25;
   if(c.third_y_time > 0) conf += 0.35;
   if(c.used_y34_as_third) conf -= 0.10;
   if(c.hook_type == FP_HOOK_P05_TYPE_A) conf += 0.15;
   if(c.hook_type == FP_HOOK_P05_TYPE_B) conf += 0.05;

   if(conf < 0.0) conf = 0.0;
   if(conf > 1.0) conf = 1.0;

   c.confidence_score = conf;
}

void FP_HookP05ClassifyRecord(const FP_HookPhase04Record &p04,
                              const FP_HookPhase05Config &cfg,
                              FP_HookPhase05Classification &c)
{
   FP_ResetHookPhase05Classification(c);
   FP_HookP05LoadEvidence(p04.p03.y_axis, cfg, c);

   FP_HookPhase02Sequence seq = p04.p03.sequence;

   if(seq.x_count < cfg.min_x_nodes_for_type)
   {
      c.hook_type = FP_HOOK_P05_TYPE_INSUFFICIENT;
      c.state = FP_HOOK_P05_STATE_INSUFFICIENT;
      c.reason = "INSUFFICIENT_X_NODES_FOR_TYPE";
      FP_HookP05FinalizeScores(c);
      return;
   }

   if(!c.has_y01 || !c.has_y12)
   {
      c.hook_type = FP_HOOK_P05_TYPE_INSUFFICIENT;
      c.state = FP_HOOK_P05_STATE_INSUFFICIENT;
      c.reason = "INSUFFICIENT_Y01_OR_Y12_FOR_TYPE";
      FP_HookP05FinalizeScores(c);
      return;
   }

   if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      FP_HookP05ClassifyPositive(c);
   else
      FP_HookP05ClassifyNegative(c);

   c.state = FP_HOOK_P05_STATE_CLASSIFIED;
   FP_HookP05FinalizeScores(c);
}

bool FP_HookP05AppendRecord(FP_HookPhase05Record &records[],
                            const FP_HookPhase05Record &record)
{
   int n = ArraySize(records);
   ArrayResize(records, n + 1);
   records[n] = record;
   return true;
}

void FP_HookP05BuildRecords(const FP_HookPhase04Record &p04_records[],
                            const FP_HookPhase05Config &cfg,
                            FP_HookPhase05Record &records[],
                            FP_HookPhase05Report &report)
{
   ArrayResize(records, 0);
   report.phase04_records_seen = ArraySize(p04_records);

   for(int i=0; i<ArraySize(p04_records); i++)
   {
      FP_HookPhase04Record p04 = p04_records[i];

      if(!p04.valid)
         continue;

      if(!FP_HookP05DirectionAllowed(cfg, p04.p03.sequence.direction))
         continue;

      FP_HookPhase05Record rec;
      FP_ResetHookPhase05Record(rec);
      rec.p04 = p04;

      FP_HookP05ClassifyRecord(p04, cfg, rec.classification);
      rec.valid = true;

      FP_HookP05AppendRecord(records, rec);

      report.records_total++;

      if(p04.p03.sequence.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
         report.records_positive++;
      else
         report.records_negative++;

      if(rec.classification.hook_type == FP_HOOK_P05_TYPE_A)
         report.type_a_count++;
      else if(rec.classification.hook_type == FP_HOOK_P05_TYPE_B)
         report.type_b_count++;
      else if(rec.classification.hook_type == FP_HOOK_P05_TYPE_C)
         report.type_c_count++;
      else
         report.insufficient_count++;

      if(rec.classification.used_y34_as_third)
         report.y34_fallback_count++;
   }
}

void FP_HookP05FinalizeReport(FP_HookPhase05Report &report)
{
   report.ok = true;
   report.status = "HOOK_P05_OK";
   report.reason = "HOOK_TYPE_ABC_CLASSIFIED";

   if(report.phase04_records_seen <= 0)
   {
      report.status = "HOOK_P05_NO_PHASE04_RECORDS";
      report.reason = "NO_LIFECYCLE_RECORDS_FOR_TYPE_CLASSIFICATION";
   }
   else if(report.records_total <= 0)
   {
      report.status = "HOOK_P05_NO_RECORDS";
      report.reason = "NO_VALID_TYPE_RECORDS";
   }
}

void FP_PrintHookPhase05Report(const string tag, const FP_HookPhase05Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP05BoolName(r.attempted),
         " ok=", FP_HookP05BoolName(r.ok),
         " bars_seen=", r.bars_seen,
         " bars_scanned=", r.bars_scanned,
         " scales_seen=", r.scales_seen,
         " nodes_seen=", r.nodes_seen,
         " p02_sequences=", r.phase02_sequences_seen,
         " p03_records=", r.phase03_records_seen,
         " p04_records=", r.phase04_records_seen,
         " records=", r.records_total,
         " positive=", r.records_positive,
         " negative=", r.records_negative,
         " type_a=", r.type_a_count,
         " type_b=", r.type_b_count,
         " type_c=", r.type_c_count,
         " insufficient=", r.insufficient_count,
         " y34_fallback=", r.y34_fallback_count,
         " drawn=", r.records_drawn,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase05Samples(const string tag,
                                const FP_HookPhase05Record &records[],
                                const int sample_limit)
{
   int n = ArraySize(records);
   int limit = sample_limit;
   if(limit <= 0 || limit > n)
      limit = n;

   for(int i=0; i<limit; i++)
   {
      FP_HookPhase05Record r = records[i];

      Print(tag,
            " sample=", i,
            " sequence_id=", r.p04.p03.sequence.sequence_id,
            " direction=", FP_HookP02DirectionName(r.p04.p03.sequence.direction),
            " L=", r.p04.p03.sequence.scale_l,
            " X=", r.p04.p03.sequence.x_count,
            " Y=", r.p04.p03.y_axis.y_count,
            " type=", FP_HookP05TypeName(r.classification.hook_type),
            " state=", FP_HookP05StateName(r.classification.state),
            " conf=", DoubleToString(r.classification.confidence_score, 2),
            " rank=", DoubleToString(r.classification.type_rank_score, 2),
            " first=", FP_HookP05BoolName(r.classification.condition_first),
            " second=", FP_HookP05BoolName(r.classification.condition_second),
            " reason=", r.classification.reason);
   }
}

#endif // __FP_HOOK_PHASE05_RULES_MQH__
