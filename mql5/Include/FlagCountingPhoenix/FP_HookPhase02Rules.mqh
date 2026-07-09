#ifndef __FP_HOOK_PHASE02_RULES_MQH__
#define __FP_HOOK_PHASE02_RULES_MQH__
#property strict

#include "FP_HookPhase02Types.mqh"

// ============================================================================
// Phase 02 — Contract-aligned Hook / ND branch sequence builder
// ----------------------------------------------------------------------------
// Implements the corrected Hook sequence model:
// - positive / low-side Hook uses valley nodes only
// - negative / high-side Hook uses peak nodes only
// - raw same-side nodes are scanned old-to-new inside an origin boundary context
// - the first unused raw node becomes node 1 of the next sequence
// - each sequence is extended greedily to the end of the raw list
// - nodes that participated earlier may not restart as node 1
// - participated nodes may still appear later as continuation nodes when strict ordering requires
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
         s.x4_node_id == seq.x4_node_id &&
         s.resolve_node_id == seq.resolve_node_id)
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

   FP_HookPhase01Node boundary = direction_nodes[boundary_index];
   FP_HookP02InitSequenceFromBoundary(ArraySize(direction_nodes), d, boundary, seq);

   seq.x_count = branch_count;
   if(branch_count > cfg.max_x_nodes_per_sequence && cfg.max_x_nodes_per_sequence > 0)
      seq.capped = true;

   for(int p=0; p<branch_count; p++)
   {
      int idx = branch_indexes_old_to_new[p];
      if(idx < 0 || idx >= ArraySize(direction_nodes))
         return false;
      if(idx <= boundary_index)
         return false;

      // The sequence is always extended to its true terminal node.
      // The compact MQL struct only has X1..X4 display slots, so nodes beyond
      // slot 4 are represented by x_count + resolve_* and marked capped.
      if(p < 4)
         FP_HookP02SetXNode(seq, p + 1, direction_nodes[idx]);
   }

   // Resolve node is the newest/rightmost counted same-side node in this branch,
   // even when the readable display slots are capped at 4.
   int resolve_index = branch_indexes_old_to_new[branch_count - 1];
   FP_HookPhase01Node resolve_node = direction_nodes[resolve_index];
   seq.last_x_price = resolve_node.price;
   seq.last_x_time = resolve_node.bar_time;
   seq.last_x_bar_index = resolve_node.bar_index;
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

   bool semantic_ready = true;
   string semantic_reason = "RENDER_ELIGIBLE_CONFIRMED_NEAR_DEATH";
   if(cfg.require_near_death_for_semantic_arc && !seq.near_death_confirmed)
   {
      // Do not discard the structural sequence here. A Hook terminal is a price
      // extreme, not only the last confirmed Phase01 node. A later raw candle
      // extreme can still make the same Hook near-death before drawing/export.
      semantic_ready = false;
      semantic_reason = "WAITING_FOR_RAW_PRICE_TERMINAL_NEAR_DEATH";
   }

   seq.valid = true;
   seq.render_eligible = semantic_ready;
   seq.visibility_reason = semantic_reason;
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


bool FP_HookP02IndexParticipated(const int idx,
                                  const int &participated_indexes[])
{
   for(int i=0; i<ArraySize(participated_indexes); i++)
   {
      if(participated_indexes[i] == idx)
         return true;
   }
   return false;
}

void FP_HookP02MarkBranchParticipated(const int &branch_indexes_old_to_new[],
                                      int &participated_indexes[])
{
   for(int i=0; i<ArraySize(branch_indexes_old_to_new); i++)
   {
      int idx = branch_indexes_old_to_new[i];
      if(idx < 0)
         continue;
      if(FP_HookP02IndexParticipated(idx, participated_indexes))
         continue;

      int n = ArraySize(participated_indexes);
      ArrayResize(participated_indexes, n + 1);
      participated_indexes[n] = idx;
   }
}

int FP_HookP02FindContextEndBeforeBoundaryBreach(const FP_HookPhase01Node &direction_nodes[],
                                                 const FP_HookPhase02Direction d,
                                                 const int boundary_index,
                                                 const bool touch_kills)
{
   int n = ArraySize(direction_nodes);
   if(boundary_index < 0 || boundary_index >= n - 1)
      return -1;

   double boundary_price = direction_nodes[boundary_index].price;
   int end_index = n - 1;
   for(int i=boundary_index + 1; i<n; i++)
   {
      if(FP_HookP02BoundaryBreachedPrice(d, boundary_price, direction_nodes[i].price, touch_kills))
      {
         end_index = i - 1;
         break;
      }
   }

   if(end_index <= boundary_index)
      return -1;
   return end_index;
}

int FP_HookP02BuildBranchFromSeedToEnd(const FP_HookPhase01Node &direction_nodes[],
                                       const FP_HookPhase02Direction d,
                                       const int seed_index,
                                       const int span_end,
                                       int &branch_indexes_old_to_new[])
{
   ArrayResize(branch_indexes_old_to_new, 0);
   if(seed_index < 0 || span_end < seed_index || span_end >= ArraySize(direction_nodes))
      return 0;

   ArrayResize(branch_indexes_old_to_new, 1);
   branch_indexes_old_to_new[0] = seed_index;
   double reference_price = direction_nodes[seed_index].price;

   for(int i=seed_index + 1; i<=span_end; i++)
   {
      if(FP_HookP02StrictAcceptsNext(d, reference_price, direction_nodes[i].price))
      {
         int n = ArraySize(branch_indexes_old_to_new);
         ArrayResize(branch_indexes_old_to_new, n + 1);
         branch_indexes_old_to_new[n] = i;
         reference_price = direction_nodes[i].price;
      }
   }

   return ArraySize(branch_indexes_old_to_new);
}


bool FP_HookP02SameTerminalHookGroup(const FP_HookPhase02Sequence &a,
                                     const FP_HookPhase02Sequence &b)
{
   return (a.direction == b.direction &&
           a.scale_l == b.scale_l &&
           a.origin_node_id == b.origin_node_id &&
           a.origin_time == b.origin_time &&
           a.origin_price == b.origin_price);
}

bool FP_HookP02ResolveIsMoreTerminal(const FP_HookPhase02Direction d,
                                     const double candidate_price,
                                     const datetime candidate_time,
                                     const double current_price,
                                     const datetime current_time)
{
   // Positive Hook terminal doctrine: the Hook ends at the lowest valley it has seen.
   // Negative Hook mirror doctrine: the Hook ends at the highest peak it has seen.
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (candidate_price < current_price ||
              (candidate_price == current_price && candidate_time > current_time));

   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return (candidate_price > current_price ||
              (candidate_price == current_price && candidate_time > current_time));

   return false;
}

void FP_HookP02ApplyTerminalToSequence(FP_HookPhase02Sequence &seq,
                                       const int terminal_node_id,
                                       const datetime terminal_time,
                                       const double terminal_price,
                                       const bool terminal_confirmed,
                                       const FP_HookPhase02Config &cfg)
{
   seq.resolve_node_id = terminal_node_id;
   seq.resolve_time = terminal_time;
   seq.resolve_price = terminal_price;
   seq.resolve_confirmed = terminal_confirmed;

   // last_x is the structural Hook terminal used by Hook-after-Hook continuity and export.
   // X1..X4 display slots remain the compact readable sequence labels.
   seq.last_x_time = terminal_time;
   seq.last_x_price = terminal_price;
   seq.last_x_bar_index = -1;

   if(seq.cycle_crown_valid)
   {
      seq.retracement_ratio = FP_HookP02ComputeRetracementRatio(seq.direction,
                                                                seq.origin_price,
                                                                seq.cycle_crown_price,
                                                                seq.resolve_price);
      seq.near_death_confirmed = (seq.resolve_confirmed &&
                                  seq.retracement_ratio >= cfg.near_death_retrace_threshold);

      if(cfg.require_near_death_for_semantic_arc && !seq.near_death_confirmed)
      {
         seq.visibility_reason = "GROUP_TERMINAL_NOT_CONFIRMED_NEAR_DEATH";
         seq.render_eligible = false;
      }
   }
}

void FP_HookP02NormalizeHookGroupTerminals(FP_HookPhase02Sequence &sequences[],
                                           const FP_HookPhase02Config &cfg)
{
   // A Hook is an origin group, not merely one compact sequence row.
   // Therefore its terminal is the extreme same-side point seen by that origin group:
   // positive Hook -> lowest valley, negative Hook -> highest peak.
   // This normalized terminal is used by Hook-after-Hook validity:
   // previous Hook terminal == current Hook origin.
   int n = ArraySize(sequences);
   for(int i=0; i<n; i++)
   {
      if(!sequences[i].valid || sequences[i].resolve_node_id < 0)
         continue;

      int best_id = sequences[i].resolve_node_id;
      datetime best_time = sequences[i].resolve_time;
      double best_price = sequences[i].resolve_price;
      bool best_confirmed = sequences[i].resolve_confirmed;

      for(int j=0; j<n; j++)
      {
         if(i == j)
            continue;
         if(!sequences[j].valid || sequences[j].resolve_node_id < 0)
            continue;
         if(!FP_HookP02SameTerminalHookGroup(sequences[i], sequences[j]))
            continue;

         if(FP_HookP02ResolveIsMoreTerminal(sequences[i].direction,
                                            sequences[j].resolve_price,
                                            sequences[j].resolve_time,
                                            best_price,
                                            best_time))
         {
            best_id = sequences[j].resolve_node_id;
            best_time = sequences[j].resolve_time;
            best_price = sequences[j].resolve_price;
            best_confirmed = sequences[j].resolve_confirmed;
         }
      }

      FP_HookP02ApplyTerminalToSequence(sequences[i], best_id, best_time,
                                        best_price, best_confirmed, cfg);
   }
}

bool FP_HookP02SequenceCycleClosed(const FP_HookPhase02Sequence &seq)
{
   // Canon: Hook-1 may validate Hook-2 only after its own sequence/cycle has
   // reached a structural terminal. Near-death rendering readiness is not part
   // of this structural test.
   if(!seq.valid)
      return false;
   if(seq.hook_failed)
      return false;
   if(seq.origin_node_id < 0 || seq.resolve_node_id < 0)
      return false;
   if(seq.resolve_time <= 0 || seq.origin_time <= 0)
      return false;
   if(seq.resolve_time < seq.origin_time)
      return false;
   return true;
}

bool FP_HookP02SameHookGenus(const FP_HookPhase02Sequence &a,
                             const FP_HookPhase02Sequence &b)
{
   // User canon: Hook-after-Hook requires both hooks to be هم‌جنس. In this
   // engine that means the same Hook direction. Scale is metadata, not genus.
   return (a.direction == b.direction);
}

bool FP_HookP02IsHookAfterHookChild(const FP_HookPhase02Sequence &child,
                                    const FP_HookPhase02Sequence &parent)
{
   if(!FP_HookP02SequenceCycleClosed(parent))
      return false;
   if(!child.valid || child.hook_failed)
      return false;
   if(!FP_HookP02SameHookGenus(child, parent))
      return false;
   if(child.origin_node_id < 0 || parent.resolve_node_id < 0)
      return false;

   // Canonical continuity rule: the second Hook starts from the terminal node
   // of the previous Hook. Raw terminal price/time is for drawing the cycle;
   // structural node id is for chain ownership.
   if(child.origin_node_id != parent.resolve_node_id)
      return false;

   if(parent.resolve_time > 0 && child.origin_time > 0 &&
      parent.resolve_time > child.origin_time)
      return false;

   return true;
}

void FP_HookP02AnnotateValidityFamilies(FP_HookPhase02Sequence &sequences[],
                                        FP_HookPhase02Report &report)
{
   report.valid_after_hook = 0;
   report.valid_after_opposing_f3 = 0;
   report.valid_hook_family_total = 0;

   int n = ArraySize(sequences);
   for(int i=0; i<n; i++)
   {
      sequences[i].valid_after_hook = false;
      sequences[i].valid_after_opposing_f3 = false;
      sequences[i].valid_hook_family = false;
      sequences[i].hook_validity_family = "UNQUALIFIED";
      sequences[i].previous_hook_sequence_id = -1;
      sequences[i].previous_hook_terminal_node_id = -1;
      sequences[i].opposing_f3_event_id = -1;
   }

   for(int i=0; i<n; i++)
   {
      if(!sequences[i].valid || sequences[i].origin_node_id < 0)
         continue;

      int best_parent = -1;
      datetime best_parent_time = 0;

      for(int j=0; j<n; j++)
      {
         if(i == j)
            continue;
         if(!FP_HookP02IsHookAfterHookChild(sequences[i], sequences[j]))
            continue;

         if(best_parent < 0 ||
            sequences[j].resolve_time > best_parent_time ||
            (sequences[j].resolve_time == best_parent_time &&
             sequences[j].sequence_id > sequences[best_parent].sequence_id))
         {
            best_parent = j;
            best_parent_time = sequences[j].resolve_time;
         }
      }

      if(best_parent >= 0)
      {
         sequences[i].valid_after_hook = true;
         sequences[i].valid_hook_family = true;
         sequences[i].hook_validity_family = "HOOK_AFTER_HOOK";
         sequences[i].previous_hook_sequence_id = sequences[best_parent].sequence_id;
         sequences[i].previous_hook_terminal_node_id = sequences[best_parent].resolve_node_id;
      }

      if(sequences[i].valid_after_hook)
         report.valid_after_hook++;
      if(sequences[i].valid_after_opposing_f3)
         report.valid_after_opposing_f3++;
      if(sequences[i].valid_hook_family)
         report.valid_hook_family_total++;
   }
}

bool FP_HookP02EventIsCompletedOrLockedF3(const FP_FlagEvent &ev)
{
   if(ev.level != FP_LEVEL_F3)
      return false;
   if(ev.f3_terminal_complete || ev.f3_locked)
      return true;
   if(ev.status == FP_STATUS_COMPLETED || ev.status == FP_STATUS_LOCKED)
      return true;
   return false;
}

datetime FP_HookP02NodeTime(const FP_Node &node)
{
   if(node.time_anchor > 0)
      return node.time_anchor;
   if(node.time_end > 0)
      return node.time_end;
   if(node.time_start > 0)
      return node.time_start;
   return 0;
}

double FP_HookP02NodePrice(const FP_Node &node)
{
   return node.price;
}

bool FP_HookP02PriceAlmostEqual(const double a,
                                const double b)
{
   double tol = _Point * 2.0;
   if(tol <= 0.0)
      tol = MathMax(MathAbs(a), MathAbs(b)) * 0.0000001;
   if(tol <= 0.0)
      tol = 0.0000001;
   return (MathAbs(a - b) <= tol);
}

bool FP_HookP02SequenceDirectionOpposesF3(const FP_FlagEvent &ev,
                                          const FP_HookPhase02Sequence &seq)
{
   // Canon is not optional: a valid post-F3 Hook must oppose the F3 direction.
   return (ev.direction == -((int)seq.direction));
}

bool FP_HookP02EventScaleMatchesSequence(const FP_FlagEvent &ev,
                                         const FP_HookPhase02Sequence &seq,
                                         const FP_HookPhase02Config &cfg)
{
   // Scale strictness is still a research toggle. Genus/direction is canonical;
   // same-scale matching is only an optional metadata filter.
   if(!cfg.valid_f3_require_same_scale)
      return true;
   if(ev.scale_L <= 0)
      return true;
   return (seq.scale_l == ev.scale_L);
}

bool FP_HookP02SequenceStartsAtNodeEndpoint(const FP_HookPhase02Sequence &seq,
                                            const FP_Node &node,
                                            datetime &endpoint_time,
                                            double &endpoint_price)
{
   endpoint_time = FP_HookP02NodeTime(node);
   endpoint_price = FP_HookP02NodePrice(node);
   if(endpoint_time <= 0 || endpoint_price == 0.0)
      return false;
   if(seq.origin_time <= 0 || seq.origin_price == 0.0)
      return false;
   if(seq.origin_time < endpoint_time)
      return false;

   // The canonical phrase is: the Hook begins from the end of the opposing F3.
   // In code, the safest available invariant is terminal price equality with a
   // small platform-point tolerance; time may differ because confirmation is
   // delayed, but price identity should remain anchored to the terminal side.
   if(!FP_HookP02PriceAlmostEqual(seq.origin_price, endpoint_price))
      return false;

   return true;
}

bool FP_HookP02SequenceStartsAtF3Terminal(const FP_FlagEvent &ev,
                                          const FP_HookPhase02Sequence &seq,
                                          datetime &matched_time,
                                          double &matched_price)
{
   matched_time = 0;
   matched_price = 0.0;

   // Prefer the latest/most terminal endpoint first. F3 can extend after its
   // base body is built; a Hook after F3 should attach to the current terminal
   // side, not to an early body anchor.
   datetime t;
   double p;
   if(ev.has_extension && FP_HookP02SequenceStartsAtNodeEndpoint(seq, ev.extension_end, t, p))
   {
      matched_time = t;
      matched_price = p;
      return true;
   }
   if(ev.has_confirm && FP_HookP02SequenceStartsAtNodeEndpoint(seq, ev.confirm, t, p))
   {
      matched_time = t;
      matched_price = p;
      return true;
   }
   if(ev.has_leg2 && FP_HookP02SequenceStartsAtNodeEndpoint(seq, ev.leg2, t, p))
   {
      matched_time = t;
      matched_price = p;
      return true;
   }

   return false;
}

int FP_HookP02FindImmediateHookAfterF3(const FP_FlagEvent &ev,
                                       const FP_HookPhase02Config &cfg,
                                       const FP_HookPhase02Sequence &sequences[],
                                       datetime &matched_f3_terminal_time,
                                       double &matched_f3_terminal_price)
{
   int best_index = -1;
   datetime best_hook_time = 0;
   datetime best_terminal_time = 0;
   double best_terminal_price = 0.0;

   for(int i=0; i<ArraySize(sequences); i++)
   {
      if(!sequences[i].valid || sequences[i].hook_failed)
         continue;
      if(!FP_HookP02SequenceDirectionOpposesF3(ev, sequences[i]))
         continue;
      if(!FP_HookP02EventScaleMatchesSequence(ev, sequences[i], cfg))
         continue;

      datetime terminal_time;
      double terminal_price;
      if(!FP_HookP02SequenceStartsAtF3Terminal(ev, sequences[i], terminal_time, terminal_price))
         continue;

      datetime hook_start = sequences[i].origin_time;
      if(hook_start <= 0)
         continue;

      if(best_index < 0 ||
         hook_start < best_hook_time ||
         (hook_start == best_hook_time && sequences[i].sequence_id < sequences[best_index].sequence_id))
      {
         best_index = i;
         best_hook_time = hook_start;
         best_terminal_time = terminal_time;
         best_terminal_price = terminal_price;
      }
   }

   matched_f3_terminal_time = best_terminal_time;
   matched_f3_terminal_price = best_terminal_price;
   return best_index;
}

void FP_HookP02MarkSequenceAsOpposingF3Valid(FP_HookPhase02Sequence &seq,
                                             const FP_FlagEvent &ev)
{
   seq.valid_after_opposing_f3 = true;
   seq.valid_hook_family = true;
   if(seq.valid_after_hook)
      seq.hook_validity_family = "HOOK_AFTER_HOOK_AND_OPPOSING_F3_TERMINAL";
   else
      seq.hook_validity_family = "HOOK_AFTER_OPPOSING_F3_TERMINAL";
   seq.opposing_f3_event_id = ev.event_id;
}

void FP_HookP02AnnotateValidityFamiliesWithF3(FP_HookPhase02Sequence &sequences[],
                                             const FP_FlagEvent &events[],
                                             const int event_count,
                                             const FP_HookPhase02Config &cfg,
                                             FP_HookPhase02Report &report)
{
   // First apply the chained Hook-after-Hook family. This family is local and
   // exact: previous terminal node == current origin node.
   FP_HookP02AnnotateValidityFamilies(sequences, report);

   // Canonical opposing-F3 doctrine:
   // A completed/locked F3 validates the first structural Hook that starts from
   // one of that F3 terminal endpoints and opposes the F3 direction. A historical
   // F3 does not validate arbitrary later Hooks.
   for(int e=0; e<event_count; e++)
   {
      FP_FlagEvent ev = events[e];
      if(!FP_HookP02EventIsCompletedOrLockedF3(ev))
         continue;

      datetime matched_terminal_time;
      double matched_terminal_price;
      int immediate_index = FP_HookP02FindImmediateHookAfterF3(ev, cfg, sequences,
                                                               matched_terminal_time,
                                                               matched_terminal_price);
      if(immediate_index < 0 || immediate_index >= ArraySize(sequences))
         continue;

      FP_HookP02MarkSequenceAsOpposingF3Valid(sequences[immediate_index], ev);
   }

   report.valid_after_hook = 0;
   report.valid_after_opposing_f3 = 0;
   report.valid_hook_family_total = 0;
   for(int i=0; i<ArraySize(sequences); i++)
   {
      if(sequences[i].valid_after_hook) report.valid_after_hook++;
      if(sequences[i].valid_after_opposing_f3) report.valid_after_opposing_f3++;
      if(sequences[i].valid_hook_family) report.valid_hook_family_total++;
   }
}


int FP_HookP02BuildDirectionScaleSeedOwned(const FP_HookPhase01Node &all_nodes[],
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
   int participated_indexes[];
   ArrayResize(participated_indexes, 0);

   // Boundary contexts are walked old-to-new. Inside each bounded context, raw
   // same-side nodes are converted into canonical seed-owned sequences. A node
   // that already participated may still be counted as 2/3/4 in a later branch,
   // but it is not allowed to restart that later branch as node 1.
   for(int boundary_i=0; boundary_i<n-1; boundary_i++)
   {
      int span_end = FP_HookP02FindContextEndBeforeBoundaryBreach(direction_nodes, d, boundary_i,
                                                                  cfg.death_on_boundary_touch);
      if(span_end <= boundary_i)
         continue;

      for(int seed_i=boundary_i+1; seed_i<=span_end; seed_i++)
      {
         if(cfg.seed_used_nodes_cannot_restart && FP_HookP02IndexParticipated(seed_i, participated_indexes))
         {
            report.seed_reuse_rejects++;
            continue;
         }

         int branch_indexes[];
         int branch_count = FP_HookP02BuildBranchFromSeedToEnd(direction_nodes, d, seed_i, span_end,
                                                               branch_indexes);
         if(branch_count <= 0)
            continue;

         FP_HookPhase02Sequence seq;
         FP_ResetHookPhase02Sequence(seq);
         if(!FP_HookP02BuildSequenceFromBranchIndexes(direction_nodes, boundary_i, branch_indexes,
                                                       all_nodes, d, cfg, seq, report))
            continue;

         if(FP_HookP02BranchDuplicate(seq, sequences))
            continue;

         if(FP_HookP02CommitSequence(seq, d, cfg, sequences, report))
         {
            FP_HookP02MarkBranchParticipated(branch_indexes, participated_indexes);
            built++;
         }

         if(cfg.max_sequences > 0 && ArraySize(sequences) >= cfg.max_sequences)
            break;
      }

      if(cfg.max_sequences > 0 && ArraySize(sequences) >= cfg.max_sequences)
         break;
   }

   return built;
}

int FP_HookP02BuildDirectionSeedOwned(const FP_HookPhase01Node &nodes[],
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
      built += FP_HookP02BuildDirectionScaleSeedOwned(nodes, d, cfg, scales_seen[s], sequences, report);
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
   built += FP_HookP02BuildDirectionSeedOwned(nodes, FP_HOOK_P02_DIRECTION_POSITIVE, cfg, sequences, report);
   built += FP_HookP02BuildDirectionSeedOwned(nodes, FP_HOOK_P02_DIRECTION_NEGATIVE, cfg, sequences, report);

   FP_HookP02NormalizeHookGroupTerminals(sequences, cfg);
   FP_HookP02AnnotateValidityFamilies(sequences, report);
   return built;
}

// Compatibility wrapper for Hook Phase 03-06 rebuild callers.
// Previous lifecycle patches rebuilt Phase 02 through a rate-aware entrypoint:
//    FP_HookP02BuildSequencesWithRates(rates, copied, nodes, cfg, sequences, report)
// The seed-owned root rebuild moved the production sequence ownership model into
// FP_HookP02BuildSequences(...). Keeping this wrapper preserves the public Phase
// 02 API expected by later Hook phases and prevents compile-time signature drift.
//
// Important: rates/copy are intentionally accepted here so Phase 03-06 do not
// need to be rewritten just to compile against the seed-owned builder. The
// sequence numbering doctrine is still owned by FP_HookP02BuildSequences.

bool FP_HookP02RawTerminalCandidateInsideOriginBoundary(const FP_HookPhase02Direction d,
                                                            const double origin_price,
                                                            const double candidate_price,
                                                            const bool touch_kills)
{
   // Canon terminal doctrine:
   // - Positive Hook terminal is the lowest price/valley still ABOVE origin.
   // - Negative Hook terminal is the highest price/peak still BELOW origin.
   // If the raw price touches or crosses origin before terminal confirmation,
   // the candidate is no longer a living Hook terminal; it is boundary death.
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (touch_kills ? candidate_price > origin_price : candidate_price >= origin_price);

   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE)
      return (touch_kills ? candidate_price < origin_price : candidate_price <= origin_price);

   return false;
}

bool FP_HookP02FindRawTerminalPriceExtreme(const MqlRates &rates[],
                                           const int copied,
                                           const FP_HookPhase02Direction d,
                                           const datetime from_time,
                                           const double origin_price,
                                           const bool touch_kills,
                                           datetime &terminal_time,
                                           double &terminal_price,
                                           int &terminal_bar_index)
{
   terminal_time = 0;
   terminal_price = 0.0;
   terminal_bar_index = -1;

   int n = MathMin(copied, ArraySize(rates));
   if(n <= 0 || from_time <= 0 || origin_price == 0.0)
      return false;

   bool found = false;
   for(int i=0; i<n; i++)
   {
      if(rates[i].time < from_time)
         continue;

      double candidate = (d == FP_HOOK_P02_DIRECTION_POSITIVE ? rates[i].low : rates[i].high);
      datetime candidate_time = rates[i].time;

      if(!FP_HookP02RawTerminalCandidateInsideOriginBoundary(d, origin_price, candidate, touch_kills))
      {
         // Stop at the first origin-boundary touch/cross. A terminal after this
         // point would belong to a failed/non-living Hook and must not extend
         // the visible production cycle.
         break;
      }

      if(!found)
      {
         found = true;
         terminal_price = candidate;
         terminal_time = candidate_time;
         terminal_bar_index = i;
         continue;
      }

      if(FP_HookP02ResolveIsMoreTerminal(d, candidate, candidate_time,
                                         terminal_price, terminal_time))
      {
         terminal_price = candidate;
         terminal_time = candidate_time;
         terminal_bar_index = i;
      }
   }

   return found;
}

void FP_HookP02PromoteRawPriceTerminalIfMoreExtreme(FP_HookPhase02Sequence &seq,
                                                    const MqlRates &rates[],
                                                    const int copied,
                                                    const FP_HookPhase02Config &cfg)
{
   if(!seq.valid || seq.hook_failed)
      return;
   if(!seq.cycle_crown_valid || seq.cycle_crown_time <= 0)
      return;

   datetime raw_time;
   double raw_price;
   int raw_bar;
   if(!FP_HookP02FindRawTerminalPriceExtreme(rates, copied, seq.direction,
                                             seq.cycle_crown_time,
                                             seq.origin_price,
                                             cfg.death_on_boundary_touch,
                                             raw_time, raw_price, raw_bar))
      return;

   if(!FP_HookP02ResolveIsMoreTerminal(seq.direction, raw_price, raw_time,
                                       seq.resolve_price, seq.resolve_time))
      return;

   // Keep resolve_node_id as the structural node terminal for Hook-after-Hook
   // continuity. Promote only the terminal time/price used by the cycle envelope
   // and near-death geometry. This matches the doctrine: the visual end of a
   // positive Hook is the lowest price it has actually seen; the mirrored
   // negative Hook ends at the highest price it has actually seen.
   seq.resolve_time = raw_time;
   seq.resolve_price = raw_price;
   seq.last_x_time = raw_time;
   seq.last_x_price = raw_price;
   seq.last_x_bar_index = raw_bar;

   if(seq.cycle_crown_valid)
   {
      seq.retracement_ratio = FP_HookP02ComputeRetracementRatio(seq.direction,
                                                                seq.origin_price,
                                                                seq.cycle_crown_price,
                                                                seq.resolve_price);
      seq.near_death_confirmed = (seq.resolve_confirmed &&
                                  seq.retracement_ratio >= cfg.near_death_retrace_threshold);

      if(cfg.require_near_death_for_semantic_arc && seq.near_death_confirmed)
      {
         seq.render_eligible = true;
         seq.visibility_reason = "RENDER_ELIGIBLE_RAW_PRICE_TERMINAL_NEAR_DEATH";
      }
   }

   if(StringFind(seq.source, "RAW_PRICE_TERMINAL") < 0)
      seq.source = seq.source + "+RAW_PRICE_TERMINAL";
}

void FP_HookP02PromoteRawPriceTerminals(FP_HookPhase02Sequence &sequences[],
                                        const MqlRates &rates[],
                                        const int copied,
                                        const FP_HookPhase02Config &cfg)
{
   for(int i=0; i<ArraySize(sequences); i++)
      FP_HookP02PromoteRawPriceTerminalIfMoreExtreme(sequences[i], rates, copied, cfg);
}

int FP_HookP02BuildSequencesWithRates(const MqlRates &rates[],
                                      const int copied,
                                      const FP_HookPhase01Node &nodes[],
                                      const FP_HookPhase02Config &cfg,
                                      FP_HookPhase02Sequence &sequences[],
                                      FP_HookPhase02Report &report)
{
   int built = FP_HookP02BuildSequences(nodes, cfg, sequences, report);
   FP_HookP02PromoteRawPriceTerminals(sequences, rates, copied, cfg);
   // Hook-after-Hook depends on structural node ids, while raw terminal promotion
   // changes price/time only. Re-annotate to keep CSV/report counters consistent
   // after terminal geometry promotion.
   FP_HookP02AnnotateValidityFamilies(sequences, report);
   return built;
}

void FP_HookP02FinalizeReport(FP_HookPhase02Report &report)
{
   report.ok = true;
   report.status = "HOOK_P02_OK";
   report.reason = "SEED_OWNED_FORWARD_HOOK_SEQUENCES_BUILT";

   if(report.nodes_seen <= 0)
   {
      report.status = "HOOK_P02_NO_NODES";
      report.reason = "PHASE01_NODE_SOURCE_EMPTY";
   }
   else if(report.sequences_total <= 0)
   {
      report.status = "HOOK_P02_NO_SEQUENCES";
      report.reason = "NO_SEED_OWNED_HOOK_SEQUENCES_FOUND";
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
         " seed_reuse_rejects=", r.seed_reuse_rejects,
         " valid_after_hook=", r.valid_after_hook,
         " valid_after_opposing_f3=", r.valid_after_opposing_f3,
         " valid_hook_family=", r.valid_hook_family_total,
         " invalid_family_filtered=", r.invalid_family_filtered,
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
            " crown_price=", DoubleToString(s.cycle_crown_price, _Digits),
            " validity_family=", s.hook_validity_family,
            " valid_family=", FP_HookP02BoolName(s.valid_hook_family));
   }
}

#endif // __FP_HOOK_PHASE02_RULES_MQH__
