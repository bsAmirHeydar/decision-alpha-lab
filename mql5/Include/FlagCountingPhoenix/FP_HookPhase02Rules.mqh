#ifndef __FP_HOOK_PHASE02_RULES_MQH__
#define __FP_HOOK_PHASE02_RULES_MQH__
#property strict

#include "FP_HookPhase02Types.mqh"

bool FP_HookP02ShouldRun(const FP_HookPhase02Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY)
      return false;
   return true;
}

bool FP_HookP02DirectionAllowed(const FP_HookPhase02Config &cfg,
                                const FP_HookPhase02Direction d)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return cfg.show_positive;
   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return cfg.show_negative;
   return false;
}

FP_HookPhase01NodeType FP_HookP02RequiredNodeType(const FP_HookPhase02Direction d)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return FP_HOOK_P01_NODE_VALLEY;
   return FP_HOOK_P01_NODE_PEAK;
}

bool FP_HookP02NodeMatchesDirection(const FP_HookPhase01Node &node,
                                    const FP_HookPhase02Direction d)
{
   return (node.node_type == FP_HookP02RequiredNodeType(d));
}

bool FP_HookP02StrictAcceptsNext(const FP_HookPhase02Direction d,
                                 const double previous_price,
                                 const double candidate_price)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (candidate_price < previous_price);

   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return (candidate_price > previous_price);

   return false;
}

bool FP_HookP02StarterUsed(const int node_id, const int &used_starters[])
{
   for(int i=0; i<ArraySize(used_starters); i++)
   {
      if(used_starters[i] == node_id)
         return true;
   }
   return false;
}

void FP_HookP02MarkStarterUsed(const int node_id, int &used_starters[])
{
   if(FP_HookP02StarterUsed(node_id, used_starters))
      return;

   int n = ArraySize(used_starters);
   ArrayResize(used_starters, n + 1);
   used_starters[n] = node_id;
}

void FP_HookP02SetXNode(FP_HookPhase02Sequence &seq,
                        const int slot,
                        const FP_HookPhase01Node &node)
{
   if(slot == 1)
   {
      seq.x1_node_id = node.node_id;
      seq.x1_bar_index = node.bar_index;
      seq.x1_time = node.bar_time;
      seq.x1_price = node.price;
   }
   else if(slot == 2)
   {
      seq.x2_node_id = node.node_id;
      seq.x2_bar_index = node.bar_index;
      seq.x2_time = node.bar_time;
      seq.x2_price = node.price;
   }
   else if(slot == 3)
   {
      seq.x3_node_id = node.node_id;
      seq.x3_bar_index = node.bar_index;
      seq.x3_time = node.bar_time;
      seq.x3_price = node.price;
   }
   else if(slot == 4)
   {
      seq.x4_node_id = node.node_id;
      seq.x4_bar_index = node.bar_index;
      seq.x4_time = node.bar_time;
      seq.x4_price = node.price;
   }

   seq.last_x_price = node.price;
   seq.last_x_time = node.bar_time;
   seq.last_x_bar_index = node.bar_index;
}

bool FP_HookP02AppendSequence(FP_HookPhase02Sequence &sequences[],
                              const FP_HookPhase02Sequence &seq,
                              const int max_sequences)
{
   int n = ArraySize(sequences);
   if(max_sequences > 0 && n >= max_sequences)
      return false;

   ArrayResize(sequences, n + 1);
   sequences[n] = seq;
   return true;
}

void FP_HookP02FinalizeSequenceState(FP_HookPhase02Sequence &seq,
                                     const FP_HookPhase02Config &cfg)
{
   seq.valid = (seq.x_count >= cfg.min_x_nodes_to_keep);

   if(!seq.valid)
   {
      seq.state = FP_HOOK_P02_STATE_REJECTED;
      if(StringLen(seq.reject_reason) <= 0)
         seq.reject_reason = "MIN_X_NODES_NOT_REACHED";
      return;
   }

   if(seq.capped)
   {
      seq.state = FP_HOOK_P02_STATE_CAPPED;
      return;
   }

   if(seq.x_count >= 3)
   {
      seq.state = FP_HOOK_P02_STATE_MATURE;
      return;
   }

   seq.state = FP_HOOK_P02_STATE_READY;
}

void FP_HookP02InitSequenceFromOrigin(const int sequence_id,
                                      const FP_HookPhase02Direction d,
                                      const FP_HookPhase01Node &origin,
                                      FP_HookPhase02Sequence &seq)
{
   FP_ResetHookPhase02Sequence(seq);
   seq.sequence_id = sequence_id;
   seq.scale_l = origin.scale_l;
   seq.direction = d;
   seq.state = FP_HOOK_P02_STATE_CANDIDATE;

   seq.origin_node_id = origin.node_id;
   seq.origin_bar_index = origin.bar_index;
   seq.origin_time = origin.bar_time;
   seq.origin_price = origin.price;

   seq.last_x_price = origin.price;
   seq.last_x_time = origin.bar_time;
   seq.last_x_bar_index = origin.bar_index;

   seq.death_boundary_price = origin.price;
   seq.source = "HOOK_P02_STRICT_X_SEQUENCE_BUILDER";
}

bool FP_HookP02CandidateIsAfterOrigin(const FP_HookPhase01Node &origin,
                                      const FP_HookPhase01Node &candidate)
{
   // Prefer time ordering over array ordering. If timestamps are equal, fall back
   // to bar-index ordering. This keeps the adapter tolerant of series/non-series
   // MqlRates arrays.
   if(candidate.bar_time > origin.bar_time)
      return true;
   if(candidate.bar_time == origin.bar_time && candidate.bar_index > origin.bar_index)
      return true;
   return false;
}

int FP_HookP02BuildOneDirection(const FP_HookPhase01Node &nodes[],
                                const FP_HookPhase02Direction d,
                                const FP_HookPhase02Config &cfg,
                                FP_HookPhase02Sequence &sequences[],
                                FP_HookPhase02Report &report)
{
   if(!FP_HookP02DirectionAllowed(cfg, d))
      return 0;

   int used_starters[];
   int built = 0;
   int node_count = ArraySize(nodes);

   for(int i=0; i<node_count; i++)
   {
      FP_HookPhase01Node origin = nodes[i];

      if(!FP_HookP02NodeMatchesDirection(origin, d))
         continue;

      if(FP_HookP02StarterUsed(origin.node_id, used_starters))
         continue;

      if(cfg.max_sequences > 0 && ArraySize(sequences) >= cfg.max_sequences)
         break;

      FP_HookPhase02Sequence seq;
      FP_HookP02InitSequenceFromOrigin(ArraySize(sequences), d, origin, seq);

      int max_x = cfg.max_x_nodes_per_sequence;
      if(max_x <= 0 || max_x > 4)
         max_x = 4;

      for(int j=0; j<node_count; j++)
      {
         FP_HookPhase01Node candidate = nodes[j];

         if(candidate.scale_l != origin.scale_l)
            continue;
         if(candidate.node_id == origin.node_id)
            continue;
         if(!FP_HookP02NodeMatchesDirection(candidate, d))
            continue;
         if(!FP_HookP02CandidateIsAfterOrigin(origin, candidate))
            continue;

         if(FP_HookP02StrictAcceptsNext(d, seq.last_x_price, candidate.price))
         {
            seq.x_count++;
            FP_HookP02SetXNode(seq, seq.x_count, candidate);

            if(seq.x_count >= max_x)
            {
               seq.capped = true;
               break;
            }
         }
      }

      FP_HookP02FinalizeSequenceState(seq, cfg);

      if(seq.valid)
      {
         if(FP_HookP02AppendSequence(sequences, seq, cfg.max_sequences))
         {
            FP_HookP02MarkStarterUsed(origin.node_id, used_starters);
            built++;

            report.sequences_total++;
            if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
               report.sequences_positive++;
            else
               report.sequences_negative++;

            if(seq.state == FP_HOOK_P02_STATE_READY)
               report.sequences_ready++;
            else if(seq.state == FP_HOOK_P02_STATE_MATURE)
               report.sequences_mature++;
            else if(seq.state == FP_HOOK_P02_STATE_CAPPED)
               report.sequences_capped++;
         }
      }
      else
      {
         report.rejected_candidates++;
         FP_HookP02MarkStarterUsed(origin.node_id, used_starters);
      }
   }

   return built;
}

int FP_HookP02BuildSequences(const FP_HookPhase01Node &nodes[],
                             const FP_HookPhase02Config &cfg,
                             FP_HookPhase02Sequence &sequences[],
                             FP_HookPhase02Report &report)
{
   ArrayResize(sequences, 0);
   report.nodes_seen = ArraySize(nodes);

   int built = 0;
   built += FP_HookP02BuildOneDirection(nodes, FP_HOOK_P02_DIRECTION_POSITIVE, cfg, sequences, report);
   built += FP_HookP02BuildOneDirection(nodes, FP_HOOK_P02_DIRECTION_NEGATIVE, cfg, sequences, report);

   return built;
}

void FP_HookP02FinalizeReport(FP_HookPhase02Report &report)
{
   report.ok = true;
   report.status = "HOOK_P02_OK";
   report.reason = "CYCLEHOOK_SEQUENCES_BUILT";

   if(report.nodes_seen <= 0)
   {
      report.status = "HOOK_P02_NO_NODES";
      report.reason = "PHASE01_NODE_SOURCE_EMPTY";
   }
   else if(report.sequences_total <= 0)
   {
      report.status = "HOOK_P02_NO_SEQUENCES";
      report.reason = "NO_STRICT_CYCLEHOOK_SEQUENCES_FOUND";
   }
}

void FP_PrintHookPhase02Report(const string tag, const FP_HookPhase02Report &r)
{
   Print(tag,
         " status=", r.status,
         " reason=", r.reason,
         " attempted=", FP_HookP02BoolName(r.attempted),
         " ok=", FP_HookP02BoolName(r.ok),
         " bars_seen=", r.bars_seen,
         " bars_scanned=", r.bars_scanned,
         " scales_seen=", r.scales_seen,
         " nodes_seen=", r.nodes_seen,
         " sequences=", r.sequences_total,
         " positive=", r.sequences_positive,
         " negative=", r.sequences_negative,
         " ready=", r.sequences_ready,
         " mature=", r.sequences_mature,
         " capped=", r.sequences_capped,
         " rejected=", r.rejected_candidates,
         " drawn=", r.sequences_drawn,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase02Samples(const string tag,
                                const FP_HookPhase02Sequence &sequences[],
                                const int sample_limit)
{
   int n = ArraySize(sequences);
   int limit = sample_limit;
   if(limit <= 0 || limit > n)
      limit = n;

   for(int i=0; i<limit; i++)
   {
      FP_HookPhase02Sequence s = sequences[i];
      Print(tag,
            " sample=", i,
            " sequence_id=", s.sequence_id,
            " direction=", FP_HookP02DirectionName(s.direction),
            " state=", FP_HookP02StateName(s.state),
            " L=", s.scale_l,
            " origin_node=", s.origin_node_id,
            " origin_time=", TimeToString(s.origin_time, TIME_DATE|TIME_SECONDS),
            " origin_price=", DoubleToString(s.origin_price, _Digits),
            " x_count=", s.x_count,
            " x1=", DoubleToString(s.x1_price, _Digits),
            " x2=", DoubleToString(s.x2_price, _Digits),
            " x3=", DoubleToString(s.x3_price, _Digits),
            " x4=", DoubleToString(s.x4_price, _Digits));
   }
}

#endif // __FP_HOOK_PHASE02_RULES_MQH__
