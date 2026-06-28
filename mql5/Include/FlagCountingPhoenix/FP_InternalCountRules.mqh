#ifndef __FP_INTERNAL_COUNT_RULES_MQH__
#define __FP_INTERNAL_COUNT_RULES_MQH__
#property strict

#include "FP_FlagBodyEngine.mqh"

// ============================================================================
// Phoenix Level 06 - Internal Count Rules
// ----------------------------------------------------------------------------
// Pure helpers for post-flag correction counting.  This file must not create
// events, draw objects, or decide F1/F2/F3 lifecycle ownership.
// ============================================================================

int FP_AdverseKindForDirection(const int direction)
{
   return FP_OriginKindForDirection(direction);
}

int FP_FavorableKindForDirection(const int direction)
{
   return FP_OppositeKind(FP_OriginKindForDirection(direction));
}

void FP_GetInternalPackNodeAt(const FP_InternalPack &p, const int num, FP_Node &out)
{
   FP_ResetNode(out);
   if(num == 1) out = p.n1;
   else if(num == 2) out = p.n2;
   else if(num == 3) out = p.n3;
   else if(num == 4) out = p.n4;
}

void FP_SetInternalNode(FP_InternalPack &p, const int num, const FP_Node &n)
{
   if(num == 1) p.n1 = n;
   else if(num == 2) p.n2 = n;
   else if(num == 3) p.n3 = n;
   else if(num == 4) p.n4 = n;
   p.last_counted_pos = n.index_anchor;
}

void FP_SetInternalMid(FP_InternalPack &p, const int before_num, const FP_Node &n)
{
   if(before_num == 1) { p.mid12 = n; p.has_mid12 = true; }
   else if(before_num == 2) { p.mid23 = n; p.has_mid23 = true; }
   else if(before_num == 3) { p.mid34 = n; p.has_mid34 = true; }
}

string FP_InternalNodeIdPart(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + IntegerToString(n.id) + "@" + IntegerToString(n.index_anchor);
}

string FP_BuildInternalBranchIdText(const FP_FlagEvent &flag, const FP_InternalPack &p)
{
   return "I|" + FP_LevelName(flag.level) +
          "|" + FP_DirectionName(flag.direction) +
          "|L" + IntegerToString(flag.scale_L) +
          "|body=" + flag.body_id +
          "|n1=" + FP_InternalNodeIdPart(p.n1) +
          "|n2=" + FP_InternalNodeIdPart(p.n2) +
          "|n3=" + FP_InternalNodeIdPart(p.n3) +
          "|n4=" + FP_InternalNodeIdPart(p.n4);
}

string FP_BuildInternalPackId(const FP_FlagEvent &flag, const FP_InternalPack &p)
{
   return FP_BuildInternalBranchIdText(flag, p) +
          "|count=" + IntegerToString(p.count) +
          "|valid12=" + FP_BoolName(p.valid12) +
          "|confirm=" + IntegerToString(p.confirm_pos) +
          "|invalid=" + IntegerToString(p.invalid_pos);
}

bool FP_InternalNodeIsMoreAdverseThanPrevious(const FP_InternalPack &p,
                                              const int next_num,
                                              const FP_Node &candidate,
                                              const int direction,
                                              const double eps)
{
   if(next_num <= 1) return true;
   FP_Node prev;
   FP_GetInternalPackNodeAt(p, next_num - 1, prev);
   if(prev.id < 0) return true;
   return FP_IsMoreAdverse(direction, candidate.price, prev.price, eps);
}

bool FP_FindBestMiddleBetween(const FP_Node &nodes[],
                              const int from_pos,
                              const int to_pos,
                              const int direction,
                              const double eps,
                              FP_Node &mid)
{
   FP_ResetNode(mid);
   int fav_kind = FP_FavorableKindForDirection(direction);
   bool has = false;
   for(int i=from_pos+1; i<to_pos; i++)
   {
      if(nodes[i].kind != fav_kind) continue;
      if(!has)
      {
         mid = nodes[i];
         has = true;
      }
      else if(FP_IsMoreFavorable(direction, nodes[i].price, mid.price, eps))
      {
         mid = nodes[i];
      }
   }
   return has;
}

bool FP_F1MiddleNodeAllowed(const FP_Node &mid, const FP_FlagEvent &flag, const double eps)
{
   if(mid.id < 0) return false;
   // Bullish F1: middle HIGH between 1/2 must not break Leg2.
   // Bearish F1: middle LOW between 1/2 must not break Leg2.
   return !FP_NodeBreaksFlagEnd(mid, flag.direction, flag.leg2.price, eps);
}

bool FP_InternalInvalidationBreaks(const FP_FlagEvent &flag, const FP_Node &n, const double eps)
{
   if(flag.level == FP_LEVEL_F1)
      return FP_NodeBreaksBoundary(n, flag.direction, flag.waist.price, eps);
   if(flag.level == FP_LEVEL_F2)
      return FP_NodeBreaksBoundary(n, flag.direction, flag.origin.price, eps);
   return false;
}

string FP_InternalInvalidationBoundaryName(const int level)
{
   if(level == FP_LEVEL_F1) return "waist";
   if(level == FP_LEVEL_F2) return "origin";
   if(level == FP_LEVEL_F3) return "none";
   return "unknown";
}

// Finds the deepest adverse correction after a flag body before confirmation.
// Used for F2/F3 origin backfill.
bool FP_FindDeepestAdverseNode(const FP_Node &nodes[],
                               const int node_count,
                               const int from_pos,
                               const int to_pos_inclusive,
                               const int direction,
                               const double epsilon_points,
                               int &best_pos,
                               FP_Node &best_node)
{
   best_pos = -1;
   FP_ResetNode(best_node);
   double eps = FP_EpsilonPrice(epsilon_points);
   int adverse_kind = FP_AdverseKindForDirection(direction);
   int to_pos = MathMin(node_count - 1, to_pos_inclusive);
   for(int i=MathMax(0, from_pos); i<=to_pos; i++)
   {
      if(nodes[i].kind != adverse_kind) continue;
      if(best_pos < 0 || FP_IsMoreAdverse(direction, nodes[i].price, best_node.price, eps))
      {
         best_pos = i;
         best_node = nodes[i];
      }
   }
   return (best_pos >= 0);
}

#endif // __FP_INTERNAL_COUNT_RULES_MQH__
