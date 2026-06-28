#ifndef __FP_HOOK_CONTEXT_MQH__
#define __FP_HOOK_CONTEXT_MQH__
#property strict

#include "FP_HookAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 04 / Hook Context Helpers
// ----------------------------------------------------------------------------
// Owns bounded same-side context checks.  These helpers are intentionally small
// so cycle-boundary failures can be debugged without reading the branch builder.
// ============================================================================

bool FP_HookCycleStartBrokenBetween(const FP_Node &nodes[],
                                    const int node_count,
                                    const int boundary_pos,
                                    const int resolve_pos,
                                    const int direction,
                                    const double eps,
                                    int &break_pos,
                                    FP_Node &break_node)
{
   break_pos = -1;
   FP_ResetNode(break_node);
   if(boundary_pos < 0 || boundary_pos >= node_count) return false;
   if(resolve_pos <= boundary_pos) return false;

   FP_Node boundary = nodes[boundary_pos];
   int side_kind = FP_OriginKindForDirection(direction);
   for(int i=boundary_pos + 1; i<resolve_pos && i<node_count; i++)
   {
      if(nodes[i].kind != side_kind) continue;
      if(FP_IsMoreAdverse(direction, nodes[i].price, boundary.price, eps))
      {
         break_pos = i;
         break_node = nodes[i];
         return true;
      }
   }
   return false;
}

bool FP_HookSpanHasOppositeExtreme(const FP_Node &nodes[],
                                   const int node_count,
                                   const int from_pos,
                                   const int to_pos,
                                   const int direction)
{
   int fav_kind = FP_OppositeKind(FP_OriginKindForDirection(direction));
   int a = MathMax(0, MathMin(from_pos, to_pos));
   int b = MathMin(node_count - 1, MathMax(from_pos, to_pos));
   for(int i=a; i<=b; i++)
      if(nodes[i].kind == fav_kind) return true;
   return false;
}

string FP_HookContextReason(const int direction,
                            const FP_Node &boundary,
                            const FP_Node &resolve,
                            const int span_len)
{
   return "bounded_context_dir_" + FP_DirectionName(direction) +
          "_cycle_" + IntegerToString(boundary.id) +
          "_resolve_" + IntegerToString(resolve.id) +
          "_span_" + IntegerToString(span_len);
}

#endif // __FP_HOOK_CONTEXT_MQH__
