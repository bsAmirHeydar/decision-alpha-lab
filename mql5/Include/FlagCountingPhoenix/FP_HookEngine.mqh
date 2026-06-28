#ifndef __FP_HOOK_ENGINE_MQH__
#define __FP_HOOK_ENGINE_MQH__
#property strict

#include "FP_NodeEngine.mqh"

// ============================================================================
// Phoenix Hook / ND Engine - contract-aligned branch implementation
// ----------------------------------------------------------------------------
// This file implements the Hook / ND documents under:
//   docs/flag_counting/phoenix_rebuild/hook_nd_branching/
//
// Core contract:
// - Hook / ND is a bounded same-side context, not a global monotonic run and
//   not a blind 3/4 alternating-node window.
// - Low-side Hook is built from LOW nodes. High-side Hook is built from HIGH
//   nodes. Opposite nodes are only used to find the cycle extreme for arc
//   curvature and retracement.
// - For every active same-side node, the engine walks backward to the nearest
//   older same-side boundary that is strictly farther in the adverse direction.
//   That boundary is the Hook floor/ceiling. The boundary itself is not counted
//   as 1/2/3/4.
// - Branches are extracted inside that bounded Hook span by right-to-left
//   discovery and old-to-new numbering.
// - A branch of 1 or 2 counted nodes is developing, not ND.
// - A branch of 3 or 4 counted nodes can become ND if retracement qualifies.
// - If any branch inside a bounded Hook context exceeds 4 counted nodes, the
//   whole context is skipped at this L; a higher-L view must compress it.
// - Equality is never a break and never validates a structural crossing.
// ============================================================================

int FP_AdverseKindForHookDirection(const int direction)
{
   return FP_OriginKindForDirection(direction);
}

int FP_FavorableKindForHookDirection(const int direction)
{
   return FP_OppositeKind(FP_AdverseKindForHookDirection(direction));
}

bool FP_HookBoundaryBreaksActive(const FP_Node &candidate, const FP_Node &active, const int direction, const double eps)
{
   // Low-side/Bullish: older LOW strictly below active LOW.
   // High-side/Bearish: older HIGH strictly above active HIGH.
   return FP_IsMoreAdverse(direction, candidate.price, active.price, eps);
}

bool FP_HookJoinableOlderNode(const FP_Node &candidate, const FP_Node &reference, const int direction, const double eps)
{
   // Low-side/Bullish: older LOW strictly above the current reference LOW.
   // High-side/Bearish: older HIGH strictly below the current reference HIGH.
   return FP_IsMoreFavorable(direction, candidate.price, reference.price, eps);
}

bool FP_HookSplitterNode(const FP_Node &candidate, const FP_Node &reference, const int direction, const double eps)
{
   // A splitter is an older same-side node that moves beyond the current
   // branch reference in the adverse direction. It closes the current branch
   // path without becoming part of that branch.
   return FP_IsMoreAdverse(direction, candidate.price, reference.price, eps);
}

int FP_HookFindNodePos(const FP_Node &nodes[], const int node_count, const FP_Node &needle)
{
   for(int i=0; i<node_count; i++)
   {
      if(nodes[i].id == needle.id && nodes[i].kind == needle.kind && nodes[i].index_anchor == needle.index_anchor) return i;
   }
   return -1;
}

int FP_CollectSameSidePositions(const FP_Node &nodes[], const int node_count, const int direction, int &positions[])
{
   ArrayResize(positions, 0);
   int kind = FP_AdverseKindForHookDirection(direction);
   for(int i=0; i<node_count; i++)
   {
      if(nodes[i].kind != kind) continue;
      int sz = ArraySize(positions);
      ArrayResize(positions, sz + 1);
      positions[sz] = i;
   }
   return ArraySize(positions);
}

void FP_AssignHookCountedNodes(FP_HookBranch &h, const FP_Node &a, const FP_Node &b, const FP_Node &c, const FP_Node &d, const int count)
{
   if(count >= 1) h.n1 = a;
   if(count >= 2) h.n2 = b;
   if(count >= 3) h.n3 = c;
   if(count >= 4) h.n4 = d;
}

FP_Node FP_FindHookCycleExtreme(const FP_Node &nodes[],
                                const int node_count,
                                const int from_pos,
                                const int to_pos,
                                const int direction,
                                const double eps)
{
   FP_Node best;
   FP_ResetNode(best);
   int fav_kind = FP_FavorableKindForHookDirection(direction);
   bool has = false;

   int a = MathMax(0, MathMin(from_pos, to_pos));
   int b = MathMin(node_count - 1, MathMax(from_pos, to_pos));
   for(int i=a; i<=b; i++)
   {
      if(nodes[i].kind != fav_kind) continue;
      if(!has)
      {
         best = nodes[i];
         has = true;
      }
      else if(FP_IsMoreFavorable(direction, nodes[i].price, best.price, eps))
      {
         best = nodes[i];
      }
   }
   return best;
}

void FP_FindCountedBranchExtremes(const FP_HookBranch &h, FP_Node &first_counted, FP_Node &last_counted)
{
   FP_ResetNode(first_counted);
   FP_ResetNode(last_counted);
   if(h.node_count >= 1) { first_counted = h.n1; last_counted = h.n1; }
   if(h.node_count >= 2) last_counted = h.n2;
   if(h.node_count >= 3) last_counted = h.n3;
   if(h.node_count >= 4) last_counted = h.n4;
}

double FP_HookRetraceRatio(const FP_HookBranch &h, const int direction)
{
   FP_Node first_counted;
   FP_Node last_counted;
   FP_FindCountedBranchExtremes(h, first_counted, last_counted);

   FP_Node cycle_start;
   if(h.has_cycle_start) cycle_start = h.cycle_start_node;
   else cycle_start = first_counted;
   if(cycle_start.id < 0 || last_counted.id < 0 || h.extreme_node.id < 0) return 0.0;

   double cycle = MathAbs(h.extreme_node.price - cycle_start.price);
   if(cycle <= 0.0) return 0.0;

   return MathAbs(last_counted.price - h.extreme_node.price) / cycle;
}

bool FP_HookBranchHasSameCountedIdentity(const FP_HookBranch &a, const FP_HookBranch &b)
{
   if(a.scale_L != b.scale_L) return false;
   if(a.direction != b.direction) return false;
   if(a.node_count != b.node_count) return false;
   if(a.has_cycle_start != b.has_cycle_start) return false;
   if(a.has_cycle_start && !FP_SameNodeIdentity(a.cycle_start_node, b.cycle_start_node)) return false;
   if(a.node_count >= 1 && !FP_SameNodeIdentity(a.n1, b.n1)) return false;
   if(a.node_count >= 2 && !FP_SameNodeIdentity(a.n2, b.n2)) return false;
   if(a.node_count >= 3 && !FP_SameNodeIdentity(a.n3, b.n3)) return false;
   if(a.node_count >= 4 && !FP_SameNodeIdentity(a.n4, b.n4)) return false;
   return true;
}

bool FP_HookIdentityExists(const FP_HookBranch &hooks[], const int hook_count, const FP_HookBranch &candidate)
{
   for(int i=0; i<hook_count; i++)
      if(FP_HookBranchHasSameCountedIdentity(hooks[i], candidate)) return true;
   return false;
}

bool FP_HookCandidateBetterForResolve(const FP_HookBranch &candidate, const FP_HookBranch &existing)
{
   // Keep the strongest branch at a resolve node. Prefer four-node branches,
   // then higher-L compression, then stronger retracement, then the older full
   // cycle boundary. This is visual compaction only; branch construction stays
   // deterministic and non-renderer-owned.
   if(candidate.node_count > existing.node_count) return true;
   if(candidate.node_count < existing.node_count) return false;
   if(candidate.scale_L > existing.scale_L) return true;
   if(candidate.scale_L < existing.scale_L) return false;
   if(candidate.retrace_ratio > existing.retrace_ratio) return true;
   if(candidate.retrace_ratio < existing.retrace_ratio) return false;

   int cidx = (candidate.has_cycle_start ? candidate.cycle_start_node.index_anchor : candidate.start_node.index_anchor);
   int eidx = (existing.has_cycle_start ? existing.cycle_start_node.index_anchor : existing.start_node.index_anchor);
   return (cidx < eidx);
}

int FP_FindHookWithSameResolve(const FP_HookBranch &hooks[], const int hook_count, const FP_HookBranch &candidate)
{
   for(int i=0; i<hook_count; i++)
   {
      if(hooks[i].direction != candidate.direction) continue;
      if(hooks[i].resolve_node.id != candidate.resolve_node.id) continue;
      if(hooks[i].resolve_node.index_anchor != candidate.resolve_node.index_anchor) continue;
      return i;
   }
   return -1;
}

bool FP_BuildHookFromCountedNodesAndBoundary(const FP_Node &nodes[],
                                             const int node_count,
                                             const int scale_L,
                                             const int direction,
                                             const int boundary_pos,
                                             const FP_Node &c1,
                                             const FP_Node &c2,
                                             const FP_Node &c3,
                                             const FP_Node &c4,
                                             const int counted,
                                             const FP_Config &cfg,
                                             const int branch_id,
                                             FP_HookBranch &h)
{
   FP_ResetHook(h);
   if(counted != 3 && counted != 4) return false;
   if(boundary_pos < 0 || boundary_pos >= node_count) return false;

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   int side_kind = FP_AdverseKindForHookDirection(direction);
   if(c1.kind != side_kind || c2.kind != side_kind || c3.kind != side_kind) return false;
   if(counted == 4 && c4.kind != side_kind) return false;

   // Counted branch order is old-to-new. It must move strictly in the adverse
   // direction from one counted node to the next. The bounding cycle start is
   // intentionally NOT numbered.
   if(!FP_IsMoreAdverse(direction, c2.price, c1.price, eps)) return false;
   if(!FP_IsMoreAdverse(direction, c3.price, c2.price, eps)) return false;
   if(counted == 4 && !FP_IsMoreAdverse(direction, c4.price, c3.price, eps)) return false;

   FP_Node last = (counted == 4 ? c4 : c3);
   int first_pos = FP_HookFindNodePos(nodes, node_count, c1);
   int last_pos = FP_HookFindNodePos(nodes, node_count, last);
   if(first_pos < 0 || last_pos < 0 || last_pos <= first_pos) return false;
   if(boundary_pos >= first_pos) return false;

   FP_Node boundary = nodes[boundary_pos];
   if(boundary.kind != side_kind) return false;

   FP_Node extreme = FP_FindHookCycleExtreme(nodes, node_count, boundary_pos, last_pos, direction, eps);
   if(extreme.id < 0) return false;

   h.branch_id = branch_id;
   h.scale_L = scale_L;
   h.direction = direction;
   h.status = FP_STATUS_CONFIRMED;
   h.node_count = counted;
   h.start_node = c1;                  // semantic counted-branch start
   h.cycle_start_node = boundary;      // full cycle start / Hook floor or ceiling
   h.has_cycle_start = true;
   h.extreme_node = extreme;
   h.resolve_node = last;              // this is the ND close / F1 phase boundary
   FP_AssignHookCountedNodes(h, c1, c2, c3, c4, counted);
   h.retrace_ratio = FP_HookRetraceRatio(h, direction);
   h.is_nd = (cfg.nd_allow_below_half_cycle || h.retrace_ratio > cfg.nd_min_retrace_ratio);
   h.reason = "bounded_hook_branch_" + IntegerToString(counted) +
              "_nodes_boundary_" + IntegerToString(boundary.id) +
              "_resolve_" + IntegerToString(last.id) +
              "_retrace_" + DoubleToString(h.retrace_ratio, 3);
   return h.is_nd;
}

int FP_AddHookIfAccepted(FP_HookBranch &hooks[], FP_HookBranch &h, const FP_Config &cfg, int &next_branch_id)
{
   if(FP_HookIdentityExists(hooks, ArraySize(hooks), h)) return ArraySize(hooks);

   int same_resolve = (cfg.compact_hook_rendering ? FP_FindHookWithSameResolve(hooks, ArraySize(hooks), h) : -1);
   if(same_resolve >= 0)
   {
      if(FP_HookCandidateBetterForResolve(h, hooks[same_resolve]))
      {
         h.branch_id = hooks[same_resolve].branch_id;
         h.reason = h.reason + ";replaced_weaker_same_resolve_hook";
         hooks[same_resolve] = h;
      }
      return ArraySize(hooks);
   }

   h.branch_id = next_branch_id;
   FP_AddHook(hooks, h);
   next_branch_id++;
   return ArraySize(hooks);
}

int FP_FindHookBoundarySideIndex(const FP_Node &nodes[],
                                 const int side_positions[],
                                 const int active_side_index,
                                 const int direction,
                                 const double eps)
{
   if(active_side_index <= 0) return -1;
   FP_Node active = nodes[side_positions[active_side_index]];
   for(int j=active_side_index - 1; j>=0; j--)
   {
      FP_Node candidate = nodes[side_positions[j]];
      if(FP_HookBoundaryBreaksActive(candidate, active, direction, eps)) return j;
   }
   return -1;
}

int FP_ExtractHookBranchLength(const FP_Node &nodes[],
                               const int side_positions[],
                               const int span_start,
                               const int right,
                               const int direction,
                               const double eps,
                               int &branch_side_indexes[])
{
   ArrayResize(branch_side_indexes, 0);
   if(right < span_start) return 0;

   int sz = 0;
   ArrayResize(branch_side_indexes, 1);
   branch_side_indexes[0] = right;
   sz = 1;

   int reference = right;
   for(int left=right - 1; left>=span_start; left--)
   {
      FP_Node candidate = nodes[side_positions[left]];
      FP_Node ref_node = nodes[side_positions[reference]];

      if(FP_HookJoinableOlderNode(candidate, ref_node, direction, eps))
      {
         ArrayResize(branch_side_indexes, sz + 1);
         branch_side_indexes[sz] = left;
         sz++;
         reference = left;
         continue;
      }

      if(FP_HookSplitterNode(candidate, ref_node, direction, eps))
      {
         break;
      }

      // Equality or neutral same-side compression: ignore; do not join and do
      // not split. This preserves the global equality contract.
   }
   return sz;
}

bool FP_HookBranchSideIdentityExists(const int &seen0[],
                                      const int &seen1[],
                                      const int &seen2[],
                                      const int &seen3[],
                                      const int existing_count,
                                      const int key0,
                                      const int key1,
                                      const int key2,
                                      const int key3)
{
   for(int i=0; i<existing_count; i++)
   {
      if(seen0[i] == key0 && seen1[i] == key1 && seen2[i] == key2 && seen3[i] == key3)
         return true;
   }
   return false;
}

// Builds Hook/ND branches according to the bounded context algorithm. This is
// deliberately not the older global strict-run implementation.
int FP_BuildHookBranches(const FP_Node &nodes[], const int node_count, const int scale_L, const FP_Config &cfg, FP_HookBranch &hooks[])
{
   ArrayResize(hooks, 0);
   if(!cfg.scan_hooks || node_count < 5) return 0;

   int next_branch_id = 0;
   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);

   for(int direction_index=0; direction_index<2; direction_index++)
   {
      int direction = (direction_index == 0 ? FP_DIR_BULLISH : FP_DIR_BEARISH);
      int side_positions[];
      int side_count = FP_CollectSameSidePositions(nodes, node_count, direction, side_positions);
      if(side_count < 4) continue; // boundary + at least three counted nodes

      for(int active=0; active<side_count; active++)
      {
         int boundary_side = FP_FindHookBoundarySideIndex(nodes, side_positions, active, direction, eps);
         if(boundary_side < 0) continue;

         int span_start = boundary_side + 1;
         int span_end = active;
         int span_len = span_end - span_start + 1;
         if(span_len < 3) continue;

         // First pass: if any branch in this bounded Hook context exceeds four
         // counted nodes, skip the entire context at this L. Higher L views must
         // compress it; do not render misleading 3/4 sub-branches from it.
         bool overextended = false;
         for(int right=span_end; right>=span_start; right--)
         {
            int branch_side_indexes[];
            int cnt = FP_ExtractHookBranchLength(nodes, side_positions, span_start, right, direction, eps, branch_side_indexes);
            if(cnt > 4)
            {
               overextended = true;
               break;
            }
         }
         if(overextended) continue;

         // Second pass: emit only ND-qualified branch lengths 3 and 4. A single
         // Hook may still yield multiple distinct branches.
         int seen0[];
         int seen1[];
         int seen2[];
         int seen3[];
         ArrayResize(seen0, 0);
         ArrayResize(seen1, 0);
         ArrayResize(seen2, 0);
         ArrayResize(seen3, 0);
         int seen_count = 0;
         for(int right=span_end; right>=span_start; right--)
         {
            int branch_side_indexes[];
            int cnt = FP_ExtractHookBranchLength(nodes, side_positions, span_start, right, direction, eps, branch_side_indexes);
            if(cnt != 3 && cnt != 4) continue;

            // branch_side_indexes are newest-to-oldest; convert to old-to-new.
            int k0 = branch_side_indexes[cnt - 1];
            int k1 = branch_side_indexes[cnt - 2];
            int k2 = branch_side_indexes[cnt - 3];
            int k3 = (cnt == 4 ? branch_side_indexes[0] : -1);
            if(FP_HookBranchSideIdentityExists(seen0, seen1, seen2, seen3, seen_count, k0, k1, k2, k3)) continue;
            ArrayResize(seen0, seen_count + 1);
            ArrayResize(seen1, seen_count + 1);
            ArrayResize(seen2, seen_count + 1);
            ArrayResize(seen3, seen_count + 1);
            seen0[seen_count] = k0;
            seen1[seen_count] = k1;
            seen2[seen_count] = k2;
            seen3[seen_count] = k3;
            seen_count++;

            FP_Node c1 = nodes[side_positions[k0]];
            FP_Node c2 = nodes[side_positions[k1]];
            FP_Node c3 = nodes[side_positions[k2]];
            FP_Node c4; FP_ResetNode(c4);
            if(cnt == 4) c4 = nodes[side_positions[k3]];

            FP_HookBranch h;
            if(FP_BuildHookFromCountedNodesAndBoundary(nodes, node_count, scale_L, direction, side_positions[boundary_side], c1, c2, c3, c4, cnt, cfg, next_branch_id, h))
            {
               FP_AddHookIfAccepted(hooks, h, cfg, next_branch_id);
               if(cfg.max_hooks > 0 && ArraySize(hooks) >= cfg.max_hooks) return ArraySize(hooks);
            }
         }
      }
   }
   return ArraySize(hooks);
}

// Returns the F1 phase boundary implied by a Hook branch. The F1 root is the
// node where the Hook/ND closes, not the older full-cycle boundary and not an
// arbitrary interior numbered node.
FP_Node FP_HookOriginNode(const FP_HookBranch &h, const double eps)
{
   FP_Node out;
   FP_ResetNode(out);
   if(h.resolve_node.id >= 0) return h.resolve_node;

   // Defensive fallback for legacy branches.
   int adverse_kind = FP_AdverseKindForHookDirection(h.direction);
   FP_Node candidates[4];
   candidates[0] = h.n1;
   candidates[1] = h.n2;
   candidates[2] = h.n3;
   candidates[3] = h.n4;
   for(int i=0; i<4; i++)
   {
      if(candidates[i].id < 0) continue;
      if(candidates[i].kind != adverse_kind) continue;
      if(out.id < 0 || FP_IsMoreAdverse(h.direction, candidates[i].price, out.price, eps)) out = candidates[i];
   }
   return out;
}

int FP_CollectHookOrigins(const FP_HookBranch &hooks[], const int hook_count, const int direction, const double eps, FP_Node &origins[])
{
   ArrayResize(origins, 0);
   for(int i=0; i<hook_count; i++)
   {
      if(hooks[i].direction != direction) continue;
      if(!hooks[i].is_nd) continue;
      FP_Node o = FP_HookOriginNode(hooks[i], eps);
      if(o.id < 0) continue;

      bool exists = false;
      for(int j=0; j<ArraySize(origins); j++)
      {
         if(origins[j].id == o.id && origins[j].kind == o.kind && origins[j].index_anchor == o.index_anchor)
         {
            exists = true;
            break;
         }
      }
      if(!exists) FP_AddNode(origins, o);
   }
   return ArraySize(origins);
}

#endif // __FP_HOOK_ENGINE_MQH__
