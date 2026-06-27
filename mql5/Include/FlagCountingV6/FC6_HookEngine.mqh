#ifndef __FC6_HOOK_ENGINE_MQH__
#define __FC6_HOOK_ENGINE_MQH__
#property strict
#include "FC6_Types.mqh"
#include "FC6_NodeEngine.mqh"

// ============================================================================
// V6 Hook / ND Engine
// ----------------------------------------------------------------------------
// The hook model is branch-based, not blind sliding-window based.  It extracts
// adverse-side branch counts from a phase context.  A branch can share a resolve
// node with other branches.  ND is emitted when a branch resolves into 3 or 4
// readable adverse nodes and the last node has retraced more than the configured
// part of the cycle from the extreme back toward the start.  Two nodes are not ND.
// ============================================================================

int FC6_AddHook(FC6_HookBranch &hooks[], FC6_HookBranch &h)
{
   int sz = ArraySize(hooks);
   h.branch_id = sz;
   ArrayResize(hooks, sz + 1);
   hooks[sz] = h;
   return sz;
}

void FC6_SetHookBranchNode(FC6_HookBranch &h, const int ordinal, const FC6_Node &n)
{
   if(ordinal == 1) h.n1 = n;
   else if(ordinal == 2) h.n2 = n;
   else if(ordinal == 3) h.n3 = n;
   else if(ordinal == 4) h.n4 = n;
}

FC6_Node FC6_GetHookBranchNode(const FC6_HookBranch &h, const int ordinal)
{
   if(ordinal == 1) return h.n1;
   if(ordinal == 2) return h.n2;
   if(ordinal == 3) return h.n3;
   if(ordinal == 4) return h.n4;
   FC6_Node z; FC6_ResetNode(z); return z;
}

bool FC6_NodeAdverseDeeper(const FC6_Node &candidate, const FC6_Node &reference, const int direction, const double eps)
{
   if(direction == FC6_DIR_BULLISH)
      return candidate.price < reference.price - eps;
   if(direction == FC6_DIR_BEARISH)
      return candidate.price > reference.price + eps;
   return false;
}

bool FC6_NodeAdverseHigherForBackwardChain(const FC6_Node &candidate, const FC6_Node &reference, const int direction, const double eps)
{
   // This is the user's backward counting rule.
   // For bullish corrections we count LOWs from latest to older.  When we move
   // backward, an older LOW belongs to the same branch if it is higher than the
   // newer LOW.  For bearish corrections we count HIGHs; older HIGH belongs to
   // the same branch if it is lower than the newer HIGH.
   if(direction == FC6_DIR_BULLISH)
      return candidate.price > reference.price + eps;
   if(direction == FC6_DIR_BEARISH)
      return candidate.price < reference.price - eps;
   return false;
}

FC6_Node FC6_ExtremeAdverseNode(const FC6_Node &a, const FC6_Node &b, const int direction)
{
   if(!FC6_NodeValid(a)) return b;
   if(!FC6_NodeValid(b)) return a;
   if(direction == FC6_DIR_BULLISH)
      return (a.price <= b.price ? a : b);
   if(direction == FC6_DIR_BEARISH)
      return (a.price >= b.price ? a : b);
   return a;
}

FC6_Node FC6_ExtremeFavorableNode(const FC6_Node &a, const FC6_Node &b, const int direction)
{
   if(!FC6_NodeValid(a)) return b;
   if(!FC6_NodeValid(b)) return a;
   if(direction == FC6_DIR_BULLISH)
      return (a.price >= b.price ? a : b);
   if(direction == FC6_DIR_BEARISH)
      return (a.price <= b.price ? a : b);
   return a;
}

double FC6_HookRetraceRatio(const FC6_HookBranch &h)
{
   if(!FC6_NodeValid(h.start_node) || !FC6_NodeValid(h.extreme_node) || !FC6_NodeValid(h.resolve_node)) return 0.0;
   double cycle = MathAbs(h.extreme_node.price - h.start_node.price);
   if(cycle <= 0.0) return 0.0;
   double retrace = MathAbs(h.resolve_node.price - h.extreme_node.price);
   return retrace / cycle;
}

bool FC6_HookPassesND(const FC6_HookBranch &h, const double min_ratio, const bool allow_below)
{
   if(h.node_count < 3 || h.node_count > 4) return false;
   if(allow_below) return true;
   return h.retrace_ratio > min_ratio;
}

int FC6_CollectContextNodes(const FC6_Node &nodes[],
                            const int count,
                            const int start_index_anchor,
                            const int end_index_anchor,
                            FC6_Node &ctx[])
{
   ArrayResize(ctx, 0);
   for(int i=0; i<count; i++)
   {
      int idx = nodes[i].index_anchor;
      if(idx <= start_index_anchor) continue;
      if(end_index_anchor >= 0 && idx >= end_index_anchor) continue;
      int sz = ArraySize(ctx);
      ArrayResize(ctx, sz + 1);
      ctx[sz] = nodes[i];
   }
   return ArraySize(ctx);
}

int FC6_CollectAdverseNodes(const FC6_Node &ctx[],
                            const int count,
                            const int direction,
                            FC6_Node &adverse[])
{
   ArrayResize(adverse, 0);
   int kind = FC6_AdverseNodeKind(direction);
   for(int i=0; i<count; i++)
   {
      if(ctx[i].kind != kind) continue;
      int sz = ArraySize(adverse);
      ArrayResize(adverse, sz + 1);
      adverse[sz] = ctx[i];
   }
   return ArraySize(adverse);
}

FC6_Node FC6_FindFavorableBetween(const FC6_Node &ctx[],
                                  const int count,
                                  const FC6_Node &a,
                                  const FC6_Node &b,
                                  const int direction)
{
   FC6_Node best; FC6_ResetNode(best);
   int fav = FC6_FavorableNodeKind(direction);
   int lo = MathMin(a.index_anchor, b.index_anchor);
   int hi = MathMax(a.index_anchor, b.index_anchor);
   for(int i=0; i<count; i++)
   {
      if(ctx[i].kind != fav) continue;
      if(ctx[i].index_anchor <= lo || ctx[i].index_anchor >= hi) continue;
      best = FC6_ExtremeFavorableNode(best, ctx[i], direction);
   }
   return best;
}

int FC6_BuildBackwardHookBranches(const FC6_Node &ctx[],
                                  const int ctx_count,
                                  const int direction,
                                  const int scale_L,
                                  const int sequence_id,
                                  const double eps,
                                  const double nd_min_ratio,
                                  const bool nd_allow_below,
                                  FC6_HookBranch &hooks[])
{
   ArrayResize(hooks, 0);
   FC6_Node adverse[];
   int adverse_count = FC6_CollectAdverseNodes(ctx, ctx_count, direction, adverse);
   if(adverse_count < 2) return 0;

   // For every latest adverse node, walk backward and collect older adverse nodes
   // that are progressively higher (bullish lows) or lower (bearish highs).  This
   // creates branch-local hook sequences.  Branches are then numbered oldest to
   // newest by their start times after construction.
   for(int last = adverse_count - 1; last >= 0; last--)
   {
      FC6_HookBranch h; FC6_ResetHookBranch(h);
      h.scale_L = scale_L;
      h.sequence_id = sequence_id;
      h.direction = direction;
      h.status = FC6_STATUS_LIVE_BODY;
      h.resolve_node = adverse[last];
      h.extreme_node = adverse[last];
      h.node_count = 1;
      FC6_SetHookBranchNode(h, 1, adverse[last]);

      FC6_Node ref = adverse[last];
      for(int prev = last - 1; prev >= 0; prev--)
      {
         if(FC6_NodeAdverseHigherForBackwardChain(adverse[prev], ref, direction, eps))
         {
            h.node_count++;
            if(h.node_count <= 4)
               FC6_SetHookBranchNode(h, h.node_count, adverse[prev]);
            h.start_node = adverse[prev];
            ref = adverse[prev];
            if(h.node_count > 4)
               break;
         }
      }

      if(!FC6_NodeValid(h.start_node)) h.start_node = adverse[last];
      // Extreme is the farthest adverse node in the branch.
      for(int k=1; k<=MathMin(h.node_count, 4); k++)
      {
         FC6_Node x = FC6_GetHookBranchNode(h, k);
         if(FC6_NodeValid(x)) h.extreme_node = FC6_ExtremeAdverseNode(h.extreme_node, x, direction);
      }
      h.retrace_ratio = FC6_HookRetraceRatio(h);
      h.is_nd = FC6_HookPassesND(h, nd_min_ratio, nd_allow_below);
      h.reason = h.is_nd ? "nd_hook_branch" : "hook_branch_not_nd";
      FC6_AddHook(hooks, h);
   }

   // Oldest branch closer to price labels. Stable insertion sort by start time.
   for(int i=1; i<ArraySize(hooks); i++)
   {
      FC6_HookBranch key = hooks[i];
      int j = i - 1;
      while(j >= 0 && hooks[j].start_node.time_anchor > key.start_node.time_anchor)
      {
         hooks[j + 1] = hooks[j];
         j--;
      }
      hooks[j + 1] = key;
   }
   for(int i=0; i<ArraySize(hooks); i++) hooks[i].branch_id = i;
   return ArraySize(hooks);
}

FC6_Node FC6_DeepestAdverseInContext(const FC6_Node &ctx[], const int count, const int direction)
{
   FC6_Node best; FC6_ResetNode(best);
   int kind = FC6_AdverseNodeKind(direction);
   for(int i=0; i<count; i++)
   {
      if(ctx[i].kind != kind) continue;
      best = FC6_ExtremeAdverseNode(best, ctx[i], direction);
   }
   return best;
}

FC6_Node FC6_FirstFavorableBreakAfter(const FC6_Node &nodes[],
                                      const int count,
                                      const int start_index_anchor,
                                      const int direction,
                                      const double level,
                                      const double eps)
{
   FC6_Node none; FC6_ResetNode(none);
   int fav = FC6_FavorableNodeKind(direction);
   for(int i=0; i<count; i++)
   {
      if(nodes[i].index_anchor <= start_index_anchor) continue;
      if(nodes[i].kind != fav) continue;
      if(direction == FC6_DIR_BULLISH && FC6_StrictBreaksAbove(nodes[i].price, level, eps)) return nodes[i];
      if(direction == FC6_DIR_BEARISH && FC6_StrictBreaksBelow(nodes[i].price, level, eps)) return nodes[i];
   }
   return none;
}

#endif // __FC6_HOOK_ENGINE_MQH__
