#ifndef __FP_HOOK_ENGINE_MQH__
#define __FP_HOOK_ENGINE_MQH__
#property strict

#include "FP_NodeEngine.mqh"

// ============================================================================
// Phoenix Hook / ND Engine - branch sequence implementation
// ----------------------------------------------------------------------------
// Contract implemented here:
// - Hook / ND is NOT a blind 3/4 alternating-node sliding window.
// - A hook is a same-side branch container.
// - Bullish hook uses LOW nodes as counted nodes.
// - Bearish hook uses HIGH nodes as counted nodes.
// - Opposite nodes are not counted; they are used to identify cycle extremes
//   and to draw the gray hook arc.
// - A counted branch is a chronological same-side sequence whose newer counted
//   nodes move strictly farther in the adverse direction:
//      bullish/low-side:  LOW1 > LOW2 > LOW3 > LOW4
//      bearish/high-side: HIGH1 < HIGH2 < HIGH3 < HIGH4
// - A branch with one or two counted nodes is developing, not ND.
// - A branch with three or four counted nodes can qualify as ND/Hook.
// - If the same-side run exceeds four counted nodes, the run is skipped at this
//   L.  A higher L compressed node view must represent it.
// - Equality is ignored: equal prices never extend, break, or validate a branch.
// ============================================================================

int FP_AdverseKindForHookDirection(const int direction)
{
   return FP_OriginKindForDirection(direction);
}

int FP_FavorableKindForHookDirection(const int direction)
{
   return FP_OppositeKind(FP_AdverseKindForHookDirection(direction));
}

bool FP_HookNodeMovesAdverse(const FP_Node &newer, const FP_Node &older, const int direction, const double eps)
{
   // True when chronological movement from older -> newer is deeper/adverse
   // for the hook side.
   return FP_IsMoreAdverse(direction, newer.price, older.price, eps);
}

bool FP_HookNodeSamePrice(const FP_Node &a, const FP_Node &b, const double eps)
{
   return FP_AlmostEqual(a.price, b.price, eps);
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

   if(first_counted.id < 0 || last_counted.id < 0 || h.extreme_node.id < 0) return 0.0;

   double cycle = MathAbs(h.extreme_node.price - first_counted.price);
   if(cycle <= 0.0) return 0.0;

   // The final same-side node must have travelled back from the favorable
   // extreme toward / beyond the branch start.  This matches the user's
   // definition of "the last node has returned more than 50% of the cycle".
   return MathAbs(last_counted.price - h.extreme_node.price) / cycle;
}

bool FP_HookBranchHasSameCountedIdentity(const FP_HookBranch &a, const FP_HookBranch &b)
{
   if(a.scale_L != b.scale_L) return false;
   if(a.direction != b.direction) return false;
   if(a.node_count != b.node_count) return false;
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
   // Prefer richer semantic branch first, then stronger cycle retracement,
   // then older start so older sequences stay closer to price in rendering.
   if(candidate.node_count > existing.node_count) return true;
   if(candidate.node_count < existing.node_count) return false;
   if(candidate.retrace_ratio > existing.retrace_ratio) return true;
   if(candidate.retrace_ratio < existing.retrace_ratio) return false;
   return (candidate.start_node.index_anchor < existing.start_node.index_anchor);
}

int FP_FindHookWithSameResolve(const FP_HookBranch &hooks[], const int hook_count, const FP_HookBranch &candidate)
{
   for(int i=0; i<hook_count; i++)
   {
      if(hooks[i].scale_L != candidate.scale_L) continue;
      if(hooks[i].direction != candidate.direction) continue;
      if(hooks[i].resolve_node.id != candidate.resolve_node.id) continue;
      if(hooks[i].resolve_node.index_anchor != candidate.resolve_node.index_anchor) continue;
      return i;
   }
   return -1;
}

bool FP_BuildHookFromCountedNodes(const FP_Node &nodes[],
                                  const int node_count,
                                  const int scale_L,
                                  const int direction,
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

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   int side_kind = FP_AdverseKindForHookDirection(direction);
   if(c1.kind != side_kind || c2.kind != side_kind || c3.kind != side_kind) return false;
   if(counted == 4 && c4.kind != side_kind) return false;

   // Strict same-side adverse staircase.
   if(!FP_HookNodeMovesAdverse(c2, c1, direction, eps)) return false;
   if(!FP_HookNodeMovesAdverse(c3, c2, direction, eps)) return false;
   if(counted == 4 && !FP_HookNodeMovesAdverse(c4, c3, direction, eps)) return false;

   FP_Node last = (counted == 4 ? c4 : c3);
   FP_Node extreme = FP_FindHookCycleExtreme(nodes, node_count, FP_HookFindNodePos(nodes, node_count, c1), FP_HookFindNodePos(nodes, node_count, last), direction, eps);
   if(extreme.id < 0) return false;

   h.branch_id = branch_id;
   h.scale_L = scale_L;
   h.direction = direction;
   h.status = FP_STATUS_CONFIRMED;
   h.node_count = counted;
   h.start_node = c1;
   h.extreme_node = extreme;
   h.resolve_node = last;
   FP_AssignHookCountedNodes(h, c1, c2, c3, c4, counted);
   h.retrace_ratio = FP_HookRetraceRatio(h, direction);
   h.is_nd = (cfg.nd_allow_below_half_cycle || h.retrace_ratio > cfg.nd_min_retrace_ratio);
   h.reason = "same_side_branch_" + IntegerToString(counted) + "_nodes_retrace_" + DoubleToString(h.retrace_ratio, 3);
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

// Builds hook/ND branches at the current L view using the same-side branch
// sequence contract.  This is deliberately NOT sliding-window alternating logic.
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
      if(side_count < 3) continue;

      int run_start = 0;
      int run_len = 1;

      for(int s=1; s<=side_count; s++)
      {
         bool continues = false;
         if(s < side_count)
         {
            FP_Node older = nodes[side_positions[s - 1]];
            FP_Node newer = nodes[side_positions[s]];
            continues = FP_HookNodeMovesAdverse(newer, older, direction, eps);
            if(FP_HookNodeSamePrice(newer, older, eps)) continues = false;
         }

         if(s < side_count && continues)
         {
            run_len++;
            continue;
         }

         // Close current strict adverse run [run_start, run_start + run_len - 1].
         if(run_len >= 3 && run_len <= 4)
         {
            // Emit the 3-node branch and, when present, the 4-node branch.
            // This preserves multiple internal sequences inside one hook.
            int max_end = run_start + run_len - 1;
            for(int end=run_start + 2; end<=max_end; end++)
            {
               int counted = end - run_start + 1;
               if(counted != 3 && counted != 4) continue;

               FP_Node c1 = nodes[side_positions[run_start]];
               FP_Node c2 = nodes[side_positions[run_start + 1]];
               FP_Node c3 = nodes[side_positions[run_start + 2]];
               FP_Node c4; FP_ResetNode(c4);
               if(counted == 4) c4 = nodes[side_positions[run_start + 3]];

               FP_HookBranch h;
               if(FP_BuildHookFromCountedNodes(nodes, node_count, scale_L, direction, c1, c2, c3, c4, counted, cfg, next_branch_id, h))
               {
                  FP_AddHookIfAccepted(hooks, h, cfg, next_branch_id);
                  if(cfg.max_hooks > 0 && ArraySize(hooks) >= cfg.max_hooks) return ArraySize(hooks);
               }
            }
         }
         else if(run_len > 4)
         {
            // Contract: branch > 4 is not accepted at this L.  Higher L views
            // are expected to compress it.  Do not emit sub-branches from the
            // invalid long run, otherwise the chart lies about the hook scale.
         }

         run_start = s;
         run_len = 1;
      }
   }
   return ArraySize(hooks);
}

// Returns the canonical F1 origin implied by a hook branch.
// Bullish: lowest LOW inside the hook branch.
// Bearish: highest HIGH inside the hook branch.
FP_Node FP_HookOriginNode(const FP_HookBranch &h, const double eps)
{
   FP_Node best;
   FP_ResetNode(best);

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
      if(best.id < 0 || FP_IsMoreAdverse(h.direction, candidates[i].price, best.price, eps)) best = candidates[i];
   }
   return best;
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
