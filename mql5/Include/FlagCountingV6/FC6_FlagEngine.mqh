#ifndef __FC6_FLAG_ENGINE_MQH__
#define __FC6_FLAG_ENGINE_MQH__
#property strict
#include "FC6_Types.mqh"
#include "FC6_NodeEngine.mqh"
#include "FC6_HookEngine.mqh"

// ============================================================================
// V6 Flag Body + Post-Flag State Engine
// ----------------------------------------------------------------------------
// A flag is always two legs:
//   Origin -> Leg1 -> Waist -> Leg2
// The differences between F1/F2/F3 are post-body rules.
// ============================================================================

int FC6_AddEvent(FC6_FlagEvent &events[], FC6_FlagEvent &e)
{
   int sz = ArraySize(events);
   e.event_id = sz;
   ArrayResize(events, sz + 1);
   events[sz] = e;
   return sz;
}

bool FC6_EventExists(const FC6_FlagEvent &events[], const int count, const FC6_FlagEvent &e, const double eps)
{
   for(int i=0; i<count; i++)
      if(FC6_SameBodyIdentity(events[i], e, eps))
         return true;
   return false;
}

bool FC6_IsValidOriginForDirection(const FC6_Node &n, const int direction)
{
   if(direction == FC6_DIR_BULLISH) return n.kind == FC6_NODE_LOW;
   if(direction == FC6_DIR_BEARISH) return n.kind == FC6_NODE_HIGH;
   return false;
}

bool FC6_IsValidLeg1ForDirection(const FC6_Node &n, const int direction)
{
   return n.kind == FC6_FavorableNodeKind(direction);
}

bool FC6_IsValidWaistForDirection(const FC6_Node &n, const int direction)
{
   return n.kind == FC6_AdverseNodeKind(direction);
}

bool FC6_WaistKeepsFlagAlive(const FC6_Node &origin, const FC6_Node &waist, const int direction, const double eps)
{
   // The flag body itself is one object for all F levels: after Leg1, the
   // correction must not break the beginning of Leg1.
   if(direction == FC6_DIR_BULLISH) return waist.price > origin.price + eps;
   if(direction == FC6_DIR_BEARISH) return waist.price < origin.price - eps;
   return false;
}

bool FC6_Leg2BreaksLeg1(const FC6_Node &leg1, const FC6_Node &leg2, const int direction, const double eps)
{
   if(direction == FC6_DIR_BULLISH) return leg2.price > leg1.price + eps;
   if(direction == FC6_DIR_BEARISH) return leg2.price < leg1.price - eps;
   return false;
}

bool FC6_NodeBreaksOrigin(const FC6_Node &n, const FC6_Node &origin, const int direction, const double eps)
{
   if(direction == FC6_DIR_BULLISH) return n.kind == FC6_NODE_LOW && n.price < origin.price - eps;
   if(direction == FC6_DIR_BEARISH) return n.kind == FC6_NODE_HIGH && n.price > origin.price + eps;
   return false;
}

bool FC6_NodeBreaksWaist(const FC6_Node &n, const FC6_Node &waist, const int direction, const double eps)
{
   if(direction == FC6_DIR_BULLISH) return n.kind == FC6_NODE_LOW && n.price < waist.price - eps;
   if(direction == FC6_DIR_BEARISH) return n.kind == FC6_NODE_HIGH && n.price > waist.price + eps;
   return false;
}

bool FC6_NodeBreaksLeg2(const FC6_Node &n, const FC6_Node &leg2, const int direction, const double eps)
{
   if(direction == FC6_DIR_BULLISH) return n.kind == FC6_NODE_HIGH && n.price > leg2.price + eps;
   if(direction == FC6_DIR_BEARISH) return n.kind == FC6_NODE_LOW && n.price < leg2.price - eps;
   return false;
}

int FC6_FindPositionByIndexAnchor(const FC6_Node &nodes[], const int count, const int index_anchor)
{
   for(int i=0; i<count; i++)
      if(nodes[i].index_anchor == index_anchor)
         return i;
   return -1;
}

bool FC6_BuildBodyFromOriginPosition(const FC6_Node &nodes[],
                                     const int count,
                                     const int origin_pos,
                                     const int level,
                                     const int direction,
                                     const int sequence_id,
                                     const int parent_id,
                                     const int chain_index,
                                     const double eps,
                                     FC6_FlagEvent &e,
                                     const bool allow_seed)
{
   FC6_ResetFlagEvent(e);
   if(origin_pos < 0 || origin_pos >= count) return false;
   FC6_Node origin = nodes[origin_pos];
   if(!FC6_IsValidOriginForDirection(origin, direction)) return false;

   e.sequence_id = sequence_id;
   e.parent_event_id = parent_id;
   e.chain_index = chain_index;
   e.scale_L = origin.L;
   e.direction = direction;
   e.level = level;
   e.status = FC6_STATUS_RAW_SEED;
   e.origin = origin;
   e.has_origin = true;
   e.leg1_L = origin.L;

   int p = origin_pos + 1;
   while(p < count && !FC6_IsValidLeg1ForDirection(nodes[p], direction)) p++;
   if(p >= count) return allow_seed;
   e.leg1 = nodes[p];
   e.has_leg1 = true;
   e.leg1_L = nodes[p].L;
   e.status = FC6_STATUS_RAW_SEED;
   e.draw_kind = FC6_DRAW_PROBABLE_LEG;

   int w = p + 1;
   while(w < count && !FC6_IsValidWaistForDirection(nodes[w], direction)) w++;
   if(w >= count) return allow_seed;
   if(!FC6_WaistKeepsFlagAlive(origin, nodes[w], direction, eps))
   {
      e.invalid = nodes[w];
      e.has_invalid = true;
      e.status = FC6_STATUS_INVALIDATED;
      e.reason = "flag_body_waist_broke_origin";
      return false;
   }
   e.waist = nodes[w];
   e.has_waist = true;

   int l2 = w + 1;
   while(l2 < count)
   {
      if(FC6_NodeBreaksOrigin(nodes[l2], origin, direction, eps))
      {
         e.invalid = nodes[l2];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "body_invalidated_before_leg2";
         return false;
      }
      if(FC6_IsValidLeg1ForDirection(nodes[l2], direction) && FC6_Leg2BreaksLeg1(e.leg1, nodes[l2], direction, eps))
      {
         e.leg2 = nodes[l2];
         e.has_leg2 = true;
         e.status = FC6_STATUS_LIVE_BODY;
         e.draw_kind = FC6_DRAW_FLAG_BODY;
         e.flag_size = FC6_FlagSize(e.origin, e.leg2);
         e.size_ratio = 0.0;
         e.reason = "two_leg_body_complete";
         return true;
      }
      l2++;
   }
   return allow_seed;
}

bool FC6_MiddleBetweenValidForF1(const FC6_Node &mid, const FC6_Node &leg2, const int direction, const double eps)
{
   if(!FC6_NodeValid(mid)) return false;
   // F1 requires the opposite middle node between internal 1 and 2 to stay
   // inside the F1 flag endpoint.  This restriction is only for the minimum 1/2.
   if(direction == FC6_DIR_BULLISH) return mid.price < leg2.price - eps;
   if(direction == FC6_DIR_BEARISH) return mid.price > leg2.price + eps;
   return false;
}

void FC6_WriteInternalNode(FC6_InternalPack &p, const int ordinal, const FC6_Node &n)
{
   if(ordinal == 1) p.n1 = n;
   else if(ordinal == 2) p.n2 = n;
   else if(ordinal == 3) p.n3 = n;
   else if(ordinal == 4) p.n4 = n;
   if(ordinal > p.count) p.count = ordinal;
}

FC6_Node FC6_ReadInternalNode(const FC6_InternalPack &p, const int ordinal)
{
   if(ordinal == 1) return p.n1;
   if(ordinal == 2) return p.n2;
   if(ordinal == 3) return p.n3;
   if(ordinal == 4) return p.n4;
   FC6_Node z; FC6_ResetNode(z); return z;
}

bool FC6_Internal2DeeperThan1(const FC6_InternalPack &p, const int direction, const double eps)
{
   if(p.count < 2) return false;
   if(direction == FC6_DIR_BULLISH) return p.n2.price < p.n1.price - eps;
   if(direction == FC6_DIR_BEARISH) return p.n2.price > p.n1.price + eps;
   return false;
}

bool FC6_CollectInternalPackAfterLeg2(const FC6_Node &nodes[],
                                      const int count,
                                      FC6_FlagEvent &e,
                                      const int start_pos,
                                      const int end_pos_exclusive,
                                      const double eps,
                                      FC6_InternalPack &pack)
{
   FC6_ResetInternalPack(pack);
   FC6_Node ctx[];
   ArrayResize(ctx, 0);
   for(int i=start_pos; i<end_pos_exclusive && i<count; i++)
   {
      int sz = ArraySize(ctx);
      ArrayResize(ctx, sz + 1);
      ctx[sz] = nodes[i];
   }
   int ctx_count = ArraySize(ctx);
   if(ctx_count <= 0) return false;

   FC6_Node adverse[];
   int adverse_count = FC6_CollectAdverseNodes(ctx, ctx_count, e.direction, adverse);
   if(adverse_count <= 0) return false;

   int limit = MathMin(adverse_count, FC6_MAX_INTERNAL_NODES);
   for(int k=0; k<limit; k++)
      FC6_WriteInternalNode(pack, k + 1, adverse[k]);

   if(pack.count >= 2)
   {
      pack.mid12 = FC6_FindFavorableBetween(ctx, ctx_count, pack.n1, pack.n2, e.direction);
      pack.has_mid12 = FC6_NodeValid(pack.mid12);
   }
   if(pack.count >= 3)
   {
      pack.mid23 = FC6_FindFavorableBetween(ctx, ctx_count, pack.n2, pack.n3, e.direction);
      pack.has_mid23 = FC6_NodeValid(pack.mid23);
   }
   if(pack.count >= 4)
   {
      pack.mid34 = FC6_FindFavorableBetween(ctx, ctx_count, pack.n3, pack.n4, e.direction);
      pack.has_mid34 = FC6_NodeValid(pack.mid34);
   }

   // ND exists when readable correction branch has 3 or 4 adverse numbers.
   pack.is_nd = (pack.count == 3 || pack.count == 4);
   return pack.count > 0;
}

int FC6_FindConfirmationAfterInternal(const FC6_Node &nodes[],
                                      const int count,
                                      const FC6_FlagEvent &e,
                                      const int start_pos,
                                      const double eps)
{
   for(int i=start_pos; i<count; i++)
   {
      if(FC6_NodeBreaksLeg2(nodes[i], e.leg2, e.direction, eps))
         return i;
   }
   return -1;
}

void FC6_ExtendLeg2UntilInternalOrInvalid(const FC6_Node &nodes[],
                                          const int count,
                                          FC6_FlagEvent &e,
                                          const int level,
                                          const double eps)
{
   // Before internal 1/2 appears, any favorable break is still the same flag
   // Leg2 extension.  This is critical for F1 and also for F2/F3 candidates.
   int leg2_pos = FC6_FindPositionByIndexAnchor(nodes, count, e.leg2.index_anchor);
   if(leg2_pos < 0) return;

   int p = leg2_pos + 1;
   while(p < count)
   {
      if(level == FC6_LEVEL_F1 && FC6_NodeBreaksWaist(nodes[p], e.waist, e.direction, eps))
      {
         e.invalid = nodes[p];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "f1_waist_hit_before_internal12";
         return;
      }
      if((level == FC6_LEVEL_F2 || level == FC6_LEVEL_F3) && FC6_NodeBreaksOrigin(nodes[p], e.origin, e.direction, eps))
      {
         e.invalid = nodes[p];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "child_origin_hit_before_internal12";
         return;
      }
      if(nodes[p].kind == FC6_AdverseNodeKind(e.direction))
      {
         // First adverse correction means internal counting can begin.
         return;
      }
      if(FC6_NodeBreaksLeg2(nodes[p], e.leg2, e.direction, eps))
      {
         e.leg2 = nodes[p];
         e.flag_size = FC6_FlagSize(e.origin, e.leg2);
         e.branch_mode = FC6_BRANCH_EXTENSION;
         e.reason = "leg2_extended_before_internal12";
      }
      p++;
   }
}

void FC6_EvaluateF1PostFlag(const FC6_Node &nodes[],
                            const int count,
                            FC6_FlagEvent &e,
                            const double eps)
{
   if(!e.has_leg2) return;
   e.level = FC6_LEVEL_F1;
   e.status = FC6_STATUS_LIVE_BODY;
   FC6_ExtendLeg2UntilInternalOrInvalid(nodes, count, e, FC6_LEVEL_F1, eps);
   if(e.status == FC6_STATUS_INVALIDATED) return;

   int leg2_pos = FC6_FindPositionByIndexAnchor(nodes, count, e.leg2.index_anchor);
   if(leg2_pos < 0) return;

   for(int p = leg2_pos + 1; p < count; p++)
   {
      if(FC6_NodeBreaksWaist(nodes[p], e.waist, e.direction, eps))
      {
         e.invalid = nodes[p];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "f1_waist_hit_before_confirmation";
         return;
      }

      if(nodes[p].kind != FC6_AdverseNodeKind(e.direction))
         continue;

      // Try to collect the minimum 1/2 from this point forward.
      for(int q = p + 1; q < count; q++)
      {
         if(FC6_NodeBreaksWaist(nodes[q], e.waist, e.direction, eps))
         {
            e.invalid = nodes[q];
            e.has_invalid = true;
            e.status = FC6_STATUS_INVALIDATED;
            e.reason = "f1_waist_hit_while_counting";
            return;
         }

         if(nodes[q].kind == FC6_AdverseNodeKind(e.direction))
         {
            FC6_InternalPack pack; FC6_ResetInternalPack(pack);
            FC6_WriteInternalNode(pack, 1, nodes[p]);
            FC6_WriteInternalNode(pack, 2, nodes[q]);
            FC6_Node mid = FC6_FindFavorableBetween(nodes, count, nodes[p], nodes[q], e.direction);
            pack.mid12 = mid;
            pack.has_mid12 = FC6_NodeValid(mid);
            if(FC6_Internal2DeeperThan1(pack, e.direction, eps) && pack.has_mid12 && FC6_MiddleBetweenValidForF1(mid, e.leg2, e.direction, eps))
            {
               int conf_pos = FC6_FindConfirmationAfterInternal(nodes, count, e, q + 1, eps);
               if(conf_pos >= 0)
               {
                  // Fill extended 3/4 if they exist before confirmation.
                  FC6_InternalPack full; FC6_CollectInternalPackAfterLeg2(nodes, count, e, p, conf_pos, eps, full);
                  e.internal_pack = full;
                  e.confirm = nodes[conf_pos];
                  e.has_confirm = true;
                  e.status = FC6_STATUS_CONFIRMED;
                  e.branch_mode = FC6_BRANCH_NORMAL_INTERNAL;
                  e.reason = "f1_confirmed_after_internal12_and_leg2_rebreak";
                  return;
               }
               e.internal_pack = pack;
               e.status = FC6_STATUS_POST_FLAG;
               e.branch_mode = FC6_BRANCH_NORMAL_INTERNAL;
               e.reason = "f1_has_internal12_waiting_confirmation";
               return;
            }
         }

         if(FC6_NodeBreaksLeg2(nodes[q], e.leg2, e.direction, eps))
         {
            // If Leg2 breaks before valid 1/2, it is extension, not confirmation.
            e.leg2 = nodes[q];
            e.flag_size = FC6_FlagSize(e.origin, e.leg2);
            e.reason = "f1_leg2_extended_before_valid_internal12";
            FC6_EvaluateF1PostFlag(nodes, count, e, eps);
            return;
         }
      }
      return;
   }
}

void FC6_EvaluateF2PostFlag(const FC6_Node &nodes[],
                            const int count,
                            FC6_FlagEvent &e,
                            const double eps,
                            const double f2_min_ratio)
{
   if(!e.has_leg2) return;
   e.level = FC6_LEVEL_F2;
   e.status = FC6_STATUS_LIVE_BODY;

   // F2 can wait for size qualification via Leg2 extension. It is not rejected.
   if(e.parent_flag_size > 0.0)
      e.size_ratio = e.flag_size / e.parent_flag_size;

   FC6_ExtendLeg2UntilInternalOrInvalid(nodes, count, e, FC6_LEVEL_F2, eps);
   if(e.status == FC6_STATUS_INVALIDATED) return;
   if(e.parent_flag_size > 0.0)
      e.size_ratio = e.flag_size / e.parent_flag_size;

   int leg2_pos = FC6_FindPositionByIndexAnchor(nodes, count, e.leg2.index_anchor);
   if(leg2_pos < 0) return;

   int first_adverse_pos = -1;
   for(int i=leg2_pos+1; i<count; i++)
   {
      if(FC6_NodeBreaksOrigin(nodes[i], e.origin, e.direction, eps))
      {
         e.invalid = nodes[i];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "f2_origin_hit";
         return;
      }
      if(nodes[i].kind == FC6_AdverseNodeKind(e.direction)) { first_adverse_pos = i; break; }
   }
   if(first_adverse_pos < 0) return;

   bool waist_break_seen = false;
   int waist_break_pos = -1;
   for(int i=first_adverse_pos; i<count; i++)
   {
      if(FC6_NodeBreaksOrigin(nodes[i], e.origin, e.direction, eps))
      {
         e.invalid = nodes[i];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "f2_origin_hit_while_counting";
         return;
      }
      if(FC6_NodeBreaksWaist(nodes[i], e.waist, e.direction, eps))
      {
         waist_break_seen = true;
         waist_break_pos = i;
         break;
      }
      if(nodes[i].kind == FC6_AdverseNodeKind(e.direction) && i > first_adverse_pos)
      {
         FC6_InternalPack pack; FC6_ResetInternalPack(pack);
         FC6_WriteInternalNode(pack, 1, nodes[first_adverse_pos]);
         FC6_WriteInternalNode(pack, 2, nodes[i]);
         FC6_Node mid = FC6_FindFavorableBetween(nodes, count, nodes[first_adverse_pos], nodes[i], e.direction);
         pack.mid12 = mid; pack.has_mid12 = FC6_NodeValid(mid);
         if(FC6_Internal2DeeperThan1(pack, e.direction, eps) && pack.has_mid12)
         {
            int conf_pos = FC6_FindConfirmationAfterInternal(nodes, count, e, i + 1, eps);
            if(conf_pos >= 0 && e.size_ratio >= f2_min_ratio)
            {
               FC6_InternalPack full; FC6_CollectInternalPackAfterLeg2(nodes, count, e, first_adverse_pos, conf_pos, eps, full);
               e.internal_pack = full;
               e.confirm = nodes[conf_pos];
               e.has_confirm = true;
               e.status = FC6_STATUS_CONFIRMED;
               e.branch_mode = FC6_BRANCH_NORMAL_INTERNAL;
               e.reason = "f2_confirmed_after_internal12_and_leg2_rebreak";
               return;
            }
            e.internal_pack = pack;
            e.status = (e.size_ratio >= f2_min_ratio ? FC6_STATUS_QUALIFIED : FC6_STATUS_POST_FLAG);
            e.branch_mode = FC6_BRANCH_NORMAL_INTERNAL;
            e.reason = "f2_internal12_waiting_size_or_confirmation";
            return;
         }
      }
   }

   if(waist_break_seen && waist_break_pos >= 0)
   {
      FC6_InternalPack pack; FC6_ResetInternalPack(pack);
      FC6_WriteInternalNode(pack, 1, e.waist);
      FC6_WriteInternalNode(pack, 2, nodes[waist_break_pos]);
      e.internal_pack = pack;
      e.branch_mode = FC6_BRANCH_WAIST_BREAK;
      int conf_pos = FC6_FindConfirmationAfterInternal(nodes, count, e, waist_break_pos + 1, eps);
      if(conf_pos >= 0 && e.size_ratio >= f2_min_ratio)
      {
         e.confirm = nodes[conf_pos];
         e.has_confirm = true;
         e.status = FC6_STATUS_CONFIRMED;
         e.reason = "f2_confirmed_by_waist_break_branch_then_leg2_rebreak";
      }
      else
      {
         e.status = (e.size_ratio >= f2_min_ratio ? FC6_STATUS_QUALIFIED : FC6_STATUS_POST_FLAG);
         e.reason = "f2_waist_break_branch_waiting_confirmation_or_size";
      }
   }
}

bool FC6_F3SameScaleOrSizePasses(const FC6_FlagEvent &f3, const FC6_Config &cfg)
{
   bool cond_L = false;
   if(f3.parent_leg1_L > 0)
   {
      int min_L = (int)MathCeil(cfg.f3_leg1_L_min_ratio * (double)f3.parent_leg1_L);
      cond_L = (f3.leg1_L >= min_L);
   }
   bool cond_size = false;
   if(f3.parent_flag_size > 0.0)
      cond_size = (f3.flag_size > cfg.f3_min_parent_size_ratio * f3.parent_flag_size);
   return (cond_L || cond_size);
}

void FC6_EvaluateF3BodyAndExtension(const FC6_Node &nodes[],
                                    const int count,
                                    FC6_FlagEvent &e,
                                    const FC6_Config &cfg)
{
   if(!e.has_leg2) return;
   e.level = FC6_LEVEL_F3;
   e.status = FC6_STATUS_LIVE_BODY;
   if(e.parent_flag_size > 0.0)
      e.size_ratio = e.flag_size / e.parent_flag_size;

   int leg2_pos = FC6_FindPositionByIndexAnchor(nodes, count, e.leg2.index_anchor);
   if(leg2_pos < 0) return;
   double eps = cfg.boundary_epsilon_points * _Point;

   // F3 is never rejected just because the first body is small. It continues
   // until one OR qualification passes, unless origin is truly broken before it
   // becomes a completed F3 candidate.
   for(int i=leg2_pos+1; i<count; i++)
   {
      if(FC6_NodeBreaksOrigin(nodes[i], e.origin, e.direction, eps) && !FC6_F3SameScaleOrSizePasses(e, cfg))
      {
         e.invalid = nodes[i];
         e.has_invalid = true;
         e.status = FC6_STATUS_INVALIDATED;
         e.reason = "f3_origin_hit_before_qualification";
         return;
      }
      if(FC6_NodeBreaksLeg2(nodes[i], e.leg2, e.direction, eps))
      {
         e.leg2 = nodes[i];
         e.flag_size = FC6_FlagSize(e.origin, e.leg2);
         if(e.parent_flag_size > 0.0) e.size_ratio = e.flag_size / e.parent_flag_size;
         e.branch_mode = FC6_BRANCH_EXTENSION;
      }
      if(FC6_F3SameScaleOrSizePasses(e, cfg))
      {
         e.status = FC6_STATUS_COMPLETED;
         e.confirm = e.leg2;
         e.has_confirm = true;
         e.extension_end = e.leg2;
         e.has_extension = true;
         e.reason = "f3_completed_by_two_leg_body_and_or_same_scale_rule";
         return;
      }
   }

   if(FC6_F3SameScaleOrSizePasses(e, cfg))
   {
      e.status = FC6_STATUS_COMPLETED;
      e.confirm = e.leg2;
      e.has_confirm = true;
      e.extension_end = e.leg2;
      e.has_extension = true;
      e.reason = "f3_completed_at_end_of_scan";
   }
   else
   {
      e.reason = "f3_waiting_or_condition";
   }
}

#endif // __FC6_FLAG_ENGINE_MQH__
