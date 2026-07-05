#ifndef __FP_HOOK_PHASE02_RULES_MQH__
#define __FP_HOOK_PHASE02_RULES_MQH__
#property strict

#include "FP_HookPhase02Types.mqh"

// ============================================================================
// Phase 02 — Contract-aligned Hook / ND branch sequence builder
// ----------------------------------------------------------------------------
// Implements the documented Hook/ND branch model:
// - positive / low-side Hook uses valley nodes only
// - negative / high-side Hook uses peak nodes only
// - branches are built end-backward and labelled old-to-new as 1..4
// - branches with more than four counted nodes are not emitted in readable view
// - valid 1/2 requires an opposite-side node between node 1 and node 2
// - opposite extreme is captured for Hook envelope rendering
// - no trade / execution / broker behavior
// ============================================================================

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

FP_HookPhase01NodeType FP_HookP02OppositeNodeType(const FP_HookPhase02Direction d)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return FP_HOOK_P01_NODE_PEAK;
   return FP_HOOK_P01_NODE_VALLEY;
}

bool FP_HookP02NodeMatchesDirection(const FP_HookPhase01Node &node,
                                    const FP_HookPhase02Direction d)
{
   return (node.node_type == FP_HookP02RequiredNodeType(d));
}

bool FP_HookP02NodeMatchesOpposite(const FP_HookPhase01Node &node,
                                   const FP_HookPhase02Direction d)
{
   return (node.node_type == FP_HookP02OppositeNodeType(d));
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

bool FP_HookP02StrictEarlierBelongsToBackwardBranch(const FP_HookPhase02Direction d,
                                                    const double earlier_price,
                                                    const double later_branch_price)
{
   // End-backward form of the same strict rule.
   // Positive / lows: earlier lows must be higher than later lows.
   // Negative / highs: earlier highs must be lower than later highs.
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (earlier_price > later_branch_price);
   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return (earlier_price < later_branch_price);
   return false;
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

void FP_HookP02InitSequenceFromBoundary(const int sequence_id,
                                         const FP_HookPhase02Direction d,
                                         const FP_HookPhase01Node &boundary_node,
                                         FP_HookPhase02Sequence &seq)
{
   FP_ResetHookPhase02Sequence(seq);
   seq.sequence_id = sequence_id;
   seq.scale_l = boundary_node.scale_l;
   seq.direction = d;
   seq.state = FP_HOOK_P02_STATE_CANDIDATE;

   // Contract-aligned: origin is the Hook floor/ceiling boundary.
   // It is NOT counted as node 1/2/3/4.
   seq.origin_node_id = boundary_node.node_id;
   seq.origin_bar_index = boundary_node.bar_index;
   seq.origin_time = boundary_node.bar_time;
   seq.origin_price = boundary_node.price;
   seq.death_boundary_price = boundary_node.price;

   seq.source = "HOOK_P02_BOUNDARY_BRANCH_CONTEXT";
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

void FP_HookP02UpdateReportForCommittedSequence(const FP_HookPhase02Direction d,
                                                const FP_HookPhase02Sequence &seq,
                                                FP_HookPhase02Report &report)
{
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

void FP_HookP02FinalizeSequenceState(FP_HookPhase02Sequence &seq,
                                     const FP_HookPhase02Config &cfg)
{
   seq.valid = (seq.x_count >= cfg.min_x_nodes_to_keep);

   if(!seq.valid)
   {
      seq.state = FP_HOOK_P02_STATE_REJECTED;
      if(StringLen(seq.reject_reason) <= 0)
         seq.reject_reason = "MIN_COUNTED_NODES_NOT_REACHED";
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

bool FP_HookP02CommitSequence(FP_HookPhase02Sequence &seq,
                              const FP_HookPhase02Direction d,
                              const FP_HookPhase02Config &cfg,
                              FP_HookPhase02Sequence &sequences[],
                              FP_HookPhase02Report &report)
{
   FP_HookP02FinalizeSequenceState(seq, cfg);

   if(!seq.valid)
   {
      report.rejected_candidates++;
      return false;
   }

   seq.sequence_id = ArraySize(sequences);
   if(!FP_HookP02AppendSequence(sequences, seq, cfg.max_sequences))
      return false;

   FP_HookP02UpdateReportForCommittedSequence(d, seq, report);
   return true;
}

bool FP_HookP02ScaleAlreadySeen(const int scale_l,
                                const int &scales_seen[])
{
   for(int i=0; i<ArraySize(scales_seen); i++)
   {
      if(scales_seen[i] == scale_l)
         return true;
   }
   return false;
}

void FP_HookP02AppendScaleSeen(const int scale_l,
                               int &scales_seen[])
{
   if(FP_HookP02ScaleAlreadySeen(scale_l, scales_seen))
      return;

   int n = ArraySize(scales_seen);
   ArrayResize(scales_seen, n + 1);
   scales_seen[n] = scale_l;
}

bool FP_HookP02SameScaleTimeBetween(const FP_HookPhase01Node &node,
                                    const int scale_l,
                                    const datetime a,
                                    const datetime b)
{
   if(node.scale_l != scale_l)
      return false;

   datetime t1 = a;
   datetime t2 = b;
   if(t2 < t1)
   {
      datetime tmp = t1;
      t1 = t2;
      t2 = tmp;
   }

   return (node.bar_time > t1 && node.bar_time < t2);
}

bool FP_HookP02HasOppositeNodeBetween(const FP_HookPhase01Node &all_nodes[],
                                      const int scale_l,
                                      const FP_HookPhase02Direction d,
                                      const datetime a,
                                      const datetime b)
{
   for(int i=0; i<ArraySize(all_nodes); i++)
   {
      FP_HookPhase01Node node = all_nodes[i];
      if(!FP_HookP02NodeMatchesOpposite(node, d))
         continue;
      if(FP_HookP02SameScaleTimeBetween(node, scale_l, a, b))
         return true;
   }
   return false;
}

bool FP_HookP02FindOppositeExtreme(const FP_HookPhase01Node &all_nodes[],
                                   const int scale_l,
                                   const FP_HookPhase02Direction d,
                                   const datetime start_time,
                                   const datetime end_time,
                                   int &node_id,
                                   datetime &node_time,
                                   double &node_price)
{
   bool found = false;
   node_id = -1;
   node_time = 0;
   node_price = 0.0;

   datetime t1 = start_time;
   datetime t2 = end_time;
   if(t2 < t1)
   {
      datetime tmp = t1;
      t1 = t2;
      t2 = tmp;
   }

   for(int i=0; i<ArraySize(all_nodes); i++)
   {
      FP_HookPhase01Node node = all_nodes[i];
      if(node.scale_l != scale_l)
         continue;
      if(!FP_HookP02NodeMatchesOpposite(node, d))
         continue;
      if(node.bar_time < t1 || node.bar_time > t2)
         continue;

      if(!found)
      {
         found = true;
         node_id = node.node_id;
         node_time = node.bar_time;
         node_price = node.price;
         continue;
      }

      if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         if(node.price > node_price || (node.price == node_price && node.bar_time < node_time))
         {
            node_id = node.node_id;
            node_time = node.bar_time;
            node_price = node.price;
         }
      }
      else
      {
         if(node.price < node_price || (node.price == node_price && node.bar_time < node_time))
         {
            node_id = node.node_id;
            node_time = node.bar_time;
            node_price = node.price;
         }
      }
   }

   return found;
}

bool FP_HookP02BranchDuplicate(const FP_HookPhase02Sequence &seq,
                               const FP_HookPhase02Sequence &sequences[])
{
   for(int i=0; i<ArraySize(sequences); i++)
   {
      FP_HookPhase02Sequence s = sequences[i];
      if(s.direction != seq.direction || s.scale_l != seq.scale_l || s.x_count != seq.x_count)
         continue;
      if(s.x1_node_id == seq.x1_node_id &&
         s.x2_node_id == seq.x2_node_id &&
         s.x3_node_id == seq.x3_node_id &&
         s.x4_node_id == seq.x4_node_id)
         return true;
   }
   return false;
}


bool FP_HookP02BoundaryCondition(const FP_HookPhase02Direction d,
                                const double older_price,
                                const double active_price)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (older_price < active_price);
   return (older_price > active_price);
}

bool FP_HookP02BoundaryBreachedPrice(const FP_HookPhase02Direction d,
                                     const double boundary_price,
                                     const double candidate_price,
                                     const bool touch_kills)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (touch_kills ? candidate_price <= boundary_price : candidate_price < boundary_price);
   return (touch_kills ? candidate_price >= boundary_price : candidate_price > boundary_price);
}

int FP_HookP02FindOriginBoundaryIndex(const FP_HookPhase01Node &direction_nodes[],
                                      const FP_HookPhase02Direction d,
                                      const int active_index)
{
   if(active_index <= 0 || active_index >= ArraySize(direction_nodes))
      return -1;

   double active_price = direction_nodes[active_index].price;
   for(int i=active_index-1; i>=0; i--)
   {
      if(FP_HookP02BoundaryCondition(d, direction_nodes[i].price, active_price))
         return i;
   }
   return -1;
}

bool FP_HookP02HookBoundaryFailedInsideSpan(const FP_HookPhase01Node &direction_nodes[],
                                           const FP_HookPhase02Direction d,
                                           const int boundary_index,
                                           const int active_index,
                                           const bool touch_kills,
                                           int &failure_node_id,
                                           datetime &failure_time,
                                           double &failure_price)
{
   failure_node_id = -1;
   failure_time = 0;
   failure_price = 0.0;

   if(boundary_index < 0 || active_index <= boundary_index || active_index >= ArraySize(direction_nodes))
      return true;

   double boundary_price = direction_nodes[boundary_index].price;

   for(int i=boundary_index+1; i<=active_index; i++)
   {
      FP_HookPhase01Node n = direction_nodes[i];
      if(FP_HookP02BoundaryBreachedPrice(d, boundary_price, n.price, touch_kills))
      {
         failure_node_id = n.node_id;
         failure_time = n.bar_time;
         failure_price = n.price;
         return true;
      }
   }
   return false;
}

double FP_HookP02ComputeRetracementRatio(const FP_HookPhase02Direction d,
                                         const double boundary_price,
                                         const double crown_price,
                                         const double resolve_price)
{
   double denom = MathAbs(crown_price - boundary_price);
   if(denom <= _Point * 0.1)
      return 0.0;

   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (crown_price - resolve_price) / denom;

   return (resolve_price - crown_price) / denom;
}

bool FP_HookP02ResolveNodeConfirmed(const FP_HookPhase01Node &direction_nodes[],
                                    const int &branch_indexes_old_to_new[])
{
   int n = ArraySize(branch_indexes_old_to_new);
   if(n <= 0)
      return false;

   int idx = branch_indexes_old_to_new[n - 1];
   if(idx < 0 || idx >= ArraySize(direction_nodes))
      return false;

   return direction_nodes[idx].confirmed;
}

bool FP_HookP02BuildSequenceFromBranchIndexes(const FP_HookPhase01Node &direction_nodes[],
                                              const int boundary_index,
                                              const int &branch_indexes_old_to_new[],
                                              const FP_HookPhase01Node &all_nodes[],
                                              const FP_HookPhase02Direction d,
                                              const FP_HookPhase02Config &cfg,
                                              FP_HookPhase02Sequence &seq,
                                              FP_HookPhase02Report &report)
{
   int branch_count = ArraySize(branch_indexes_old_to_new);
   if(branch_count <= 0)
      return false;

   if(boundary_index < 0 || boundary_index >= ArraySize(direction_nodes))
      return false;

   if(branch_count > 4)
   {
      report.rejected_candidates++;
      seq.reject_reason = "BRANCH_EXCEEDS_FOUR_REQUIRES_HIGHER_L";
      return false;
   }

   FP_HookPhase01Node boundary = direction_nodes[boundary_index];
   FP_HookP02InitSequenceFromBoundary(ArraySize(direction_nodes), d, boundary, seq);

   seq.x_count = branch_count;
   for(int p=0; p<branch_count; p++)
   {
      int idx = branch_indexes_old_to_new[p];
      if(idx < 0 || idx >= ArraySize(direction_nodes))
         return false;
      if(idx <= boundary_index)
         return false;
      FP_HookP02SetXNode(seq, p + 1, direction_nodes[idx]);
   }

   // Resolve node is the newest/rightmost counted same-side node in this branch.
   int resolve_index = branch_indexes_old_to_new[branch_count - 1];
   FP_HookPhase01Node resolve_node = direction_nodes[resolve_index];
   seq.resolve_node_id = resolve_node.node_id;
   seq.resolve_time = resolve_node.bar_time;
   seq.resolve_price = resolve_node.price;
   seq.resolve_confirmed = resolve_node.confirmed;

   if(cfg.require_confirmed_resolve_node && !seq.resolve_confirmed)
   {
      seq.visibility_reason = "RESOLVE_NODE_NOT_CONFIRMED";
      seq.render_eligible = false;
      report.rejected_candidates++;
      return false;
   }

   int failure_id;
   datetime failure_time;
   double failure_price;
   if(FP_HookP02HookBoundaryFailedInsideSpan(direction_nodes, d, boundary_index, resolve_index,
                                            cfg.death_on_boundary_touch,
                                            failure_id, failure_time, failure_price))
   {
      seq.hook_failed = true;
      seq.failure_node_id = failure_id;
      seq.failure_time = failure_time;
      seq.failure_price = failure_price;
      seq.visibility_reason = "HOOK_BOUNDARY_TOUCHED_OR_BREACHED_BEFORE_RESOLVE";
      seq.render_eligible = false;
      report.rejected_candidates++;
      return false;
   }

   // Documented minimum 1/2: node 2 must strictly pass node 1 and an opposite node must exist between them.
   if(branch_count >= 2)
   {
      if(!FP_HookP02StrictAcceptsNext(d, seq.x1_price, seq.x2_price))
      {
         seq.reject_reason = "NON_STRICT_1_2";
         report.rejected_candidates++;
         return false;
      }

      if(!FP_HookP02HasOppositeNodeBetween(all_nodes, seq.scale_l, d, seq.x1_time, seq.x2_time))
      {
         seq.reject_reason = "NO_OPPOSITE_NODE_BETWEEN_1_2";
         report.rejected_candidates++;
         return false;
      }
   }

   int crown_id;
   datetime crown_time;
   double crown_price;
   if(!FP_HookP02FindOppositeExtreme(all_nodes, seq.scale_l, d, seq.origin_time, seq.resolve_time,
                                     crown_id, crown_time, crown_price))
   {
      seq.visibility_reason = "NO_OPPOSITE_CYCLE_EXTREME";
      seq.render_eligible = false;
      report.rejected_candidates++;
      return false;
   }

   seq.cycle_crown_node_id = crown_id;
   seq.cycle_crown_time = crown_time;
   seq.cycle_crown_price = crown_price;
   seq.cycle_crown_valid = true;

   seq.retracement_ratio = FP_HookP02ComputeRetracementRatio(d, seq.origin_price, seq.cycle_crown_price, seq.resolve_price);
   seq.near_death_confirmed = (seq.resolve_confirmed && seq.retracement_ratio >= cfg.near_death_retrace_threshold);

   if(cfg.require_near_death_for_semantic_arc && !seq.near_death_confirmed)
   {
      seq.visibility_reason = "RESOLVE_NODE_NOT_CONFIRMED_NEAR_DEATH";
      seq.render_eligible = false;
      report.rejected_candidates++;
      return false;
   }

   seq.valid = true;
   seq.render_eligible = true;
   seq.visibility_reason = "RENDER_ELIGIBLE_CONFIRMED_NEAR_DEATH";
   seq.source = "HOOK_P02_DOC_BOUNDARY_CONFIRMED_NEAR_DEATH";
   return true;
}

int FP_HookP02CollectDirectionScaleNodes(const FP_HookPhase01Node &nodes[],
                                         const FP_HookPhase02Direction d,
                                         const int scale_l,
                                         FP_HookPhase01Node &direction_nodes[])
{
   ArrayResize(direction_nodes, 0);
   for(int i=0; i<ArraySize(nodes); i++)
   {
      FP_HookPhase01Node node = nodes[i];
      if(node.scale_l != scale_l)
         continue;
      if(!FP_HookP02NodeMatchesDirection(node, d))
         continue;

      int n = ArraySize(direction_nodes);
      ArrayResize(direction_nodes, n + 1);
      direction_nodes[n] = node;
   }
   return ArraySize(direction_nodes);
}

void FP_HookP02ReverseIntArray(int &arr[])
{
   int n = ArraySize(arr);
   for(int i=0; i<n/2; i++)
   {
      int j = n - 1 - i;
      int tmp = arr[i];
      arr[i] = arr[j];
      arr[j] = tmp;
   }
}

int FP_HookP02BuildDirectionScaleEndBackward(const FP_HookPhase01Node &all_nodes[],
                                             const FP_HookPhase02Direction d,
                                             const FP_HookPhase02Config &cfg,
                                             const int scale_l,
                                             FP_HookPhase02Sequence &sequences[],
                                             FP_HookPhase02Report &report)
{
   FP_HookPhase01Node direction_nodes[];
   int n = FP_HookP02CollectDirectionScaleNodes(all_nodes, d, scale_l, direction_nodes);
   if(n <= 1)
      return 0;

   int built = 0;
   int max_readable = cfg.max_x_nodes_per_sequence;
   if(max_readable <= 0 || max_readable > 4)
      max_readable = 4;

   for(int active_i=1; active_i<n; active_i++)
   {
      int boundary_index = FP_HookP02FindOriginBoundaryIndex(direction_nodes, d, active_i);
      if(boundary_index < 0)
         continue;

      int failure_id;
      datetime failure_time;
      double failure_price;
      if(FP_HookP02HookBoundaryFailedInsideSpan(direction_nodes, d, boundary_index, active_i,
                                               cfg.death_on_boundary_touch,
                                               failure_id, failure_time, failure_price))
      {
         report.rejected_candidates++;
         continue;
      }

      // Extract all right-to-left branch paths inside this Hook context.
      for(int resolver_i=boundary_index+1; resolver_i<=active_i; resolver_i++)
      {
         int backward_indexes[];
         ArrayResize(backward_indexes, 1);
         backward_indexes[0] = resolver_i;
         double reference = direction_nodes[resolver_i].price;

         for(int k=resolver_i-1; k>boundary_index; k--)
         {
            // If the candidate would break the running branch reference, this branch path closes.
            if(FP_HookP02BoundaryCondition(d, direction_nodes[k].price, reference))
               break;

            if(FP_HookP02StrictEarlierBelongsToBackwardBranch(d, direction_nodes[k].price, reference))
            {
               int m = ArraySize(backward_indexes);
               ArrayResize(backward_indexes, m + 1);
               backward_indexes[m] = k;
               reference = direction_nodes[k].price;
            }
         }

         if(ArraySize(backward_indexes) > max_readable)
         {
            report.rejected_candidates++;
            continue;
         }

         FP_HookP02ReverseIntArray(backward_indexes);

         FP_HookPhase02Sequence seq;
         FP_ResetHookPhase02Sequence(seq);
         if(!FP_HookP02BuildSequenceFromBranchIndexes(direction_nodes, boundary_index, backward_indexes,
                                                       all_nodes, d, cfg, seq, report))
            continue;

         if(FP_HookP02BranchDuplicate(seq, sequences))
            continue;

         if(FP_HookP02CommitSequence(seq, d, cfg, sequences, report))
            built++;

         if(cfg.max_sequences > 0 && ArraySize(sequences) >= cfg.max_sequences)
            break;
      }

      if(cfg.max_sequences > 0 && ArraySize(sequences) >= cfg.max_sequences)
         break;
   }

   return built;
}

int FP_HookP02BuildDirectionEndBackward(const FP_HookPhase01Node &nodes[],
                                        const FP_HookPhase02Direction d,
                                        const FP_HookPhase02Config &cfg,
                                        FP_HookPhase02Sequence &sequences[],
                                        FP_HookPhase02Report &report)
{
   if(!FP_HookP02DirectionAllowed(cfg, d))
      return 0;

   int scales_seen[];
   for(int i=0; i<ArraySize(nodes); i++)
   {
      FP_HookPhase01Node node = nodes[i];
      if(FP_HookP02NodeMatchesDirection(node, d))
         FP_HookP02AppendScaleSeen(node.scale_l, scales_seen);
   }

   int built = 0;
   for(int s=0; s<ArraySize(scales_seen); s++)
   {
      built += FP_HookP02BuildDirectionScaleEndBackward(nodes, d, cfg, scales_seen[s], sequences, report);
      if(cfg.max_sequences > 0 && ArraySize(sequences) >= cfg.max_sequences)
         break;
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
   report.origin_promotions = 0;
   report.promoted_chains = 0;

   int built = 0;
   built += FP_HookP02BuildDirectionEndBackward(nodes, FP_HOOK_P02_DIRECTION_POSITIVE, cfg, sequences, report);
   built += FP_HookP02BuildDirectionEndBackward(nodes, FP_HOOK_P02_DIRECTION_NEGATIVE, cfg, sequences, report);
   return built;
}

void FP_HookP02FinalizeReport(FP_HookPhase02Report &report)
{
   report.ok = true;
   report.status = "HOOK_P02_OK";
   report.reason = "DOC_ALIGNED_END_BACKWARD_BRANCHES_BUILT";

   if(report.nodes_seen <= 0)
   {
      report.status = "HOOK_P02_NO_NODES";
      report.reason = "PHASE01_NODE_SOURCE_EMPTY";
   }
   else if(report.sequences_total <= 0)
   {
      report.status = "HOOK_P02_NO_SEQUENCES";
      report.reason = "NO_DOC_ALIGNED_HOOK_BRANCHES_FOUND";
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
         " origin_promotions=", r.origin_promotions,
         " promoted_chains=", r.promoted_chains,
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
            " x4=", DoubleToString(s.x4_price, _Digits),
            " crown_valid=", FP_HookP02BoolName(s.cycle_crown_valid),
            " crown_price=", DoubleToString(s.cycle_crown_price, _Digits));
   }
}

#endif // __FP_HOOK_PHASE02_RULES_MQH__
