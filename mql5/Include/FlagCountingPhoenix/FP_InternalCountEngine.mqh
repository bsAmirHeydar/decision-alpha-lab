#ifndef __FP_INTERNAL_COUNT_ENGINE_MQH__
#define __FP_INTERNAL_COUNT_ENGINE_MQH__
#property strict

#include "FP_FlagBodyEngine.mqh"

// ============================================================================
// Phoenix Internal Count / Post-Flag Correction Engine
// ----------------------------------------------------------------------------
// Counts internal adverse-side nodes after a completed flag body.
// Bullish: adverse nodes are LOWs. Bearish: adverse nodes are HIGHs.
// 1/2 must exist before F1 confirmation. In F1, the middle opposite node between
// 1 and 2 must not break the flag end. For 3/4 the restriction no longer applies
// once a valid 1/2 branch exists.
// ============================================================================

int FP_AdverseKindForDirection(const int direction)
{
   return FP_OriginKindForDirection(direction);
}

int FP_FavorableKindForDirection(const int direction)
{
   return FP_OppositeKind(FP_OriginKindForDirection(direction));
}

void FP_SetInternalNode(FP_InternalPack &p, const int num, const FP_Node &n)
{
   if(num == 1) p.n1 = n;
   else if(num == 2) p.n2 = n;
   else if(num == 3) p.n3 = n;
   else if(num == 4) p.n4 = n;
}

void FP_SetInternalMid(FP_InternalPack &p, const int before_num, const FP_Node &n)
{
   if(before_num == 1) { p.mid12 = n; p.has_mid12 = true; }
   else if(before_num == 2) { p.mid23 = n; p.has_mid23 = true; }
   else if(before_num == 3) { p.mid34 = n; p.has_mid34 = true; }
}

bool FP_InternalNodeIsMoreAdverseThanPrevious(const FP_InternalPack &p, const int next_num, const FP_Node &candidate, const int direction, const double eps)
{
   if(next_num <= 1) return true;
   FP_Node prev;
   FP_ResetNode(prev);
   if(next_num == 2) prev = p.n1;
   else if(next_num == 3) prev = p.n2;
   else if(next_num == 4) prev = p.n3;
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

bool FP_F1MiddleNodeAllowed(const FP_Node &mid, const FP_FlagEvent &flag, const double eps)
{
   if(mid.id < 0) return false;
   // Bullish F1: middle HIGH between 1/2 must not break Leg2.
   // Bearish F1: middle LOW between 1/2 must not break Leg2.
   return !FP_NodeBreaksFlagEnd(mid, flag.direction, flag.leg2.price, eps);
}

// This function does not mutate the flag body. It returns the post-flag count,
// confirmation/invalid position and the internal pack. If a pre-1/2 extension
// occurs, the caller can rebuild the body from a later Leg2 in a stricter pass.
bool FP_BuildPostFlagInternalPack(const FP_Node &nodes[],
                                  const int node_count,
                                  const FP_FlagEvent &flag,
                                  const FP_Config &cfg,
                                  FP_InternalPack &pack,
                                  int &confirm_pos,
                                  int &invalid_pos,
                                  int &last_scanned_pos)
{
   FP_ResetInternalPack(pack);
   confirm_pos = -1;
   invalid_pos = -1;
   last_scanned_pos = flag.pos_leg2;
   if(flag.pos_leg2 < 0) return false;

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   int adverse_kind = FP_AdverseKindForDirection(flag.direction);
   int max_internal = FP_MAX_INTERNAL_NODES;
   int last_adverse_pos = -1;
   bool have_valid12 = false;

   for(int i=flag.pos_leg2 + 1; i<node_count; i++)
   {
      last_scanned_pos = i;
      FP_Node n = nodes[i];

      // Invalidation boundary differs by level.
      // F1 invalidates at waist before confirmation.
      // F2 invalidates at origin; waist-break can become branch.
      // F3 ignores post-flag correction for completion.
      if(flag.level == FP_LEVEL_F1)
      {
         if(FP_NodeBreaksBoundary(n, flag.direction, flag.waist.price, eps))
         {
            invalid_pos = i;
            return (pack.count > 0);
         }
      }
      else if(flag.level == FP_LEVEL_F2)
      {
         if(FP_NodeBreaksBoundary(n, flag.direction, flag.origin.price, eps))
         {
            invalid_pos = i;
            return (pack.count > 0);
         }
      }
      else if(flag.level == FP_LEVEL_F3)
      {
         // F3 is complete by the body itself. No post-flag invalidation here.
         return true;
      }

      if(FP_NodeBreaksFlagEnd(n, flag.direction, flag.leg2.price, eps))
      {
         if(have_valid12)
         {
            confirm_pos = i;
            return true;
         }
         // Before valid 1/2 this is body extension in the contract. Keep scanning
         // but do not confirm. The engine can later rebuild with extended Leg2.
         continue;
      }

      if(n.kind != adverse_kind) continue;
      if(pack.count >= max_internal) continue;

      int next_num = pack.count + 1;
      if(next_num > 1 && !FP_InternalNodeIsMoreAdverseThanPrevious(pack, next_num, n, flag.direction, eps))
      {
         // Branch-local counting: if this adverse node is not deeper than previous,
         // it may belong to another hook branch. This pack keeps the strict branch.
         continue;
      }

      if(next_num > 1 && last_adverse_pos >= 0)
      {
         FP_Node mid;
         bool has_mid = FP_FindBestMiddleBetween(nodes, last_adverse_pos, i, flag.direction, eps, mid);
         if(!has_mid) continue;
         if(flag.level == FP_LEVEL_F1 && next_num == 2)
         {
            if(!FP_F1MiddleNodeAllowed(mid, flag, eps)) continue;
         }
         FP_SetInternalMid(pack, next_num - 1, mid);
      }

      FP_SetInternalNode(pack, next_num, n);
      pack.count = next_num;
      last_adverse_pos = i;

      if(pack.count >= 2)
      {
         pack.valid12 = true;
         have_valid12 = true;
      }
      if(pack.count == 3 || pack.count == 4)
      {
         pack.is_nd = true;
      }
   }

   return (pack.count > 0);
}

void FP_CopyInternalPackToEvent(FP_FlagEvent &e, const FP_InternalPack &pack)
{
   e.internal_pack = pack;
}

#endif // __FP_INTERNAL_COUNT_ENGINE_MQH__
