#ifndef __FP_HOOK_ENGINE_MQH__
#define __FP_HOOK_ENGINE_MQH__
#property strict

#include "FP_NodeEngine.mqh"

// ============================================================================
// Phoenix Hook / ND Engine
// ----------------------------------------------------------------------------
// The hook engine is intentionally branch-aware.  It does not merely dump every
// sliding window.  It builds readable 3/4-node hook branches from alternating
// structural nodes and marks them as ND when the branch has returned more than
// the configured cycle retracement threshold from its extreme toward the start.
// ============================================================================

bool FP_WindowAlternates(const FP_Node &nodes[], const int start, const int count)
{
   if(count < 2) return false;
   for(int i=start+1; i<start+count; i++)
      if(nodes[i].kind == nodes[i-1].kind) return false;
   return true;
}

int FP_AdverseKindForHookDirection(const int direction)
{
   return FP_OriginKindForDirection(direction);
}

void FP_AssignHookWindowNodes(FP_HookBranch &h, const FP_Node &nodes[], const int start, const int count)
{
   if(count >= 1) h.n1 = nodes[start];
   if(count >= 2) h.n2 = nodes[start + 1];
   if(count >= 3) h.n3 = nodes[start + 2];
   if(count >= 4) h.n4 = nodes[start + 3];
}

FP_Node FP_ExtremeAdverseNodeInWindow(const FP_Node &nodes[], const int start, const int count, const int direction, const double eps)
{
   FP_Node best;
   FP_ResetNode(best);
   int adverse_kind = FP_AdverseKindForHookDirection(direction);
   bool has = false;
   for(int i=start; i<start+count; i++)
   {
      if(nodes[i].kind != adverse_kind) continue;
      if(!has)
      {
         best = nodes[i];
         has = true;
      }
      else if(FP_IsMoreAdverse(direction, nodes[i].price, best.price, eps))
      {
         best = nodes[i];
      }
   }
   return best;
}

FP_Node FP_FavorableExtremeNodeInWindow(const FP_Node &nodes[], const int start, const int count, const int direction, const double eps)
{
   FP_Node best;
   FP_ResetNode(best);
   int fav_kind = FP_OppositeKind(FP_AdverseKindForHookDirection(direction));
   bool has = false;
   for(int i=start; i<start+count; i++)
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

double FP_HookRetraceRatio(const FP_HookBranch &h, const int direction)
{
   double cycle = MathAbs(h.extreme_node.price - h.start_node.price);
   if(cycle <= 0.0)
   {
      // If start and extreme are the same node/price, use the full high-low span
      // in the branch. This keeps plateau-origin hooks auditable instead of
      // silently discarding them.
      double hi = h.start_node.price;
      double lo = h.start_node.price;
      if(h.node_count >= 1) { hi = MathMax(hi, h.n1.price); lo = MathMin(lo, h.n1.price); }
      if(h.node_count >= 2) { hi = MathMax(hi, h.n2.price); lo = MathMin(lo, h.n2.price); }
      if(h.node_count >= 3) { hi = MathMax(hi, h.n3.price); lo = MathMin(lo, h.n3.price); }
      if(h.node_count >= 4) { hi = MathMax(hi, h.n4.price); lo = MathMin(lo, h.n4.price); }
      cycle = MathAbs(hi - lo);
   }
   if(cycle <= 0.0) return 0.0;
   return MathAbs(h.resolve_node.price - h.extreme_node.price) / cycle;
}

bool FP_HookIdentityExists(const FP_HookBranch &hooks[], const int hook_count, const FP_HookBranch &candidate)
{
   for(int i=0; i<hook_count; i++)
   {
      if(hooks[i].scale_L != candidate.scale_L) continue;
      if(hooks[i].direction != candidate.direction) continue;
      if(hooks[i].node_count != candidate.node_count) continue;
      if(hooks[i].start_node.id != candidate.start_node.id) continue;
      if(hooks[i].extreme_node.id != candidate.extreme_node.id) continue;
      if(hooks[i].resolve_node.id != candidate.resolve_node.id) continue;
      return true;
   }
   return false;
}

bool FP_BuildHookFromWindow(const FP_Node &nodes[],
                            const int start,
                            const int count,
                            const int scale_L,
                            const int direction,
                            const FP_Config &cfg,
                            const int branch_id,
                            FP_HookBranch &h)
{
   FP_ResetHook(h);
   if(count != 3 && count != 4) return false;
   if(!FP_WindowAlternates(nodes, start, count)) return false;

   int adverse_kind = FP_AdverseKindForHookDirection(direction);
   if(nodes[start].kind != adverse_kind) return false;

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   h.branch_id = branch_id;
   h.scale_L = scale_L;
   h.direction = direction;
   h.status = FP_STATUS_CONFIRMED;
   h.node_count = count;
   h.start_node = nodes[start];
   h.resolve_node = nodes[start + count - 1];
   h.extreme_node = FP_ExtremeAdverseNodeInWindow(nodes, start, count, direction, eps);
   if(h.extreme_node.id < 0) return false;
   FP_AssignHookWindowNodes(h, nodes, start, count);
   h.retrace_ratio = FP_HookRetraceRatio(h, direction);
   h.is_nd = (h.node_count == 3 || h.node_count == 4) && (cfg.nd_allow_below_half_cycle || h.retrace_ratio > cfg.nd_min_retrace_ratio);
   h.reason = "branch_hook_" + IntegerToString(count) + "_nodes_retrace_" + DoubleToString(h.retrace_ratio, 3);
   return h.is_nd;
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

bool FP_HookCandidateBetterForResolve(const FP_HookBranch &candidate, const FP_HookBranch &existing)
{
   // Prefer the richer 4-node branch; if node_count ties, prefer stronger retracement.
   if(candidate.node_count > existing.node_count) return true;
   if(candidate.node_count < existing.node_count) return false;
   return (candidate.retrace_ratio > existing.retrace_ratio);
}

// Builds hook/ND branches at the current L view.
// If a denser branch would exceed 4 nodes, the caller should let higher L views
// also run; the multi-scale engine naturally gives the higher-L compressed view.
int FP_BuildHookBranches(const FP_Node &nodes[], const int node_count, const int scale_L, const FP_Config &cfg, FP_HookBranch &hooks[])
{
   ArrayResize(hooks, 0);
   if(!cfg.scan_hooks || node_count < 3) return 0;

   int next_branch_id = 0;
   for(int direction_index=0; direction_index<2; direction_index++)
   {
      int direction = (direction_index == 0 ? FP_DIR_BULLISH : FP_DIR_BEARISH);
      for(int i=0; i<node_count; i++)
      {
         for(int count=3; count<=4; count++)
         {
            if(i + count > node_count) continue;
            FP_HookBranch h;
            if(FP_BuildHookFromWindow(nodes, i, count, scale_L, direction, cfg, next_branch_id, h))
            {
               if(!FP_HookIdentityExists(hooks, ArraySize(hooks), h))
               {
                  int same_resolve = (cfg.compact_hook_rendering ? FP_FindHookWithSameResolve(hooks, ArraySize(hooks), h) : -1);
                  if(same_resolve >= 0)
                  {
                     if(FP_HookCandidateBetterForResolve(h, hooks[same_resolve]))
                     {
                        h.branch_id = hooks[same_resolve].branch_id;
                        h.reason = h.reason + ";replaced_weaker_same_resolve_hook";
                        hooks[same_resolve] = h;
                     }
                  }
                  else
                  {
                     FP_AddHook(hooks, h);
                     next_branch_id++;
                     if(cfg.max_hooks > 0 && ArraySize(hooks) >= cfg.max_hooks) return ArraySize(hooks);
                  }
               }
            }
         }
      }
   }
   return ArraySize(hooks);
}

// Returns the canonical F1 origin implied by a hook branch.
// Bullish: lowest LOW inside positive hook.
// Bearish: highest HIGH inside negative hook.
FP_Node FP_HookOriginNode(const FP_HookBranch &h, const double eps)
{
   FP_Node best;
   FP_ResetNode(best);
   best = h.extreme_node;

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
