#ifndef __FP_F2_LIFECYCLE_RULES_MQH__
#define __FP_F2_LIFECYCLE_RULES_MQH__
#property strict

#include "FP_F1LifecycleEngine.mqh"

// ============================================================================
// Phoenix Level 08 - F2 Lifecycle Rules
// ----------------------------------------------------------------------------
// Pure rule helpers for F2 promotion.  F1 is the parent authority.  Level 08
// owns parent-readiness, F2 origin backfill, parent-size gate, and F3
// authorization; it does not draw objects or prune main-chart ownership.
// ============================================================================

string FP_F2LifecycleNodePart(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + IntegerToString(n.id) + "@" + IntegerToString(n.index_anchor);
}

string FP_BuildF2LifecycleId(const FP_FlagEvent &f2)
{
   return "F2LC|" + FP_DirectionName(f2.direction) +
          "|L" + IntegerToString(f2.scale_L) +
          "|seq" + IntegerToString(f2.sequence_id) +
          "|parent=" + IntegerToString(f2.parent_event_id) +
          "|body=" + f2.body_id +
          "|O=" + FP_F2LifecycleNodePart(f2.origin) +
          "|A=" + FP_F2LifecycleNodePart(f2.leg1) +
          "|W=" + FP_F2LifecycleNodePart(f2.waist) +
          "|B=" + FP_F2LifecycleNodePart(f2.leg2) +
          "|ratio=" + DoubleToString(f2.size_ratio, 4) +
          "|I=" + f2.internal_pack.internal_pack_id;
}

bool FP_F2ParentGatePasses(const FP_FlagEvent &f1)
{
   return FP_F1StatusCanSpawnF2(f1);
}

bool FP_F2SizeGatePasses(const FP_FlagEvent &f2, const FP_FlagEvent &f1, const FP_Config &cfg)
{
   if(f1.flag_size <= 0.0) return false;
   return (f2.flag_size >= cfg.f2_min_parent_size_ratio * f1.flag_size);
}

bool FP_F2StatusCanSpawnF3(const FP_FlagEvent &f2)
{
   if(f2.level != FP_LEVEL_F2) return false;
   if(f2.status != FP_STATUS_CONFIRMED) return false;
   if(!f2.has_confirm) return false;
   if(!f2.f2_can_spawn_f3) return false;
   return true;
}

bool FP_F2ShouldBeVisibleForLifecycle(const FP_FlagEvent &f2, const FP_Config &cfg)
{
   if(f2.status == FP_STATUS_INVALIDATED) return cfg.show_invalidated_in_audit;
   if(f2.status == FP_STATUS_CONFIRMED) return true;
   if(f2.status == FP_STATUS_POST_FLAG) return cfg.f2_show_post_flag_candidates;
   if(f2.status == FP_STATUS_LIVE_BODY || f2.status == FP_STATUS_LIVE_LEG) return cfg.f2_show_live_body_candidates;
   if(f2.f2_lifecycle_status == FP_F2_LC_SIZE_REJECTED) return cfg.f2_show_size_rejected_candidates;
   return f2.visible_main;
}

void FP_SetF2LifecycleState(FP_FlagEvent &f2,
                            const int lifecycle_status,
                            const string reason)
{
   f2.f2_lifecycle_status = lifecycle_status;
   f2.f2_body_complete = (f2.has_origin && f2.has_leg1 && f2.has_waist && f2.has_leg2 &&
                          (f2.body_status == FP_BODY_COMPLETE || f2.body_status == FP_BODY_EXTENDED));
   f2.f2_internal_ready = (f2.internal_pack.valid12 || f2.internal_pack.has_valid12);
   f2.f2_can_spawn_f3 = (f2.level == FP_LEVEL_F2 &&
                         f2.status == FP_STATUS_CONFIRMED &&
                         f2.has_confirm &&
                         f2.f2_parent_ready &&
                         f2.f2_size_gate_passed);
   f2.f2_lifecycle_id = FP_BuildF2LifecycleId(f2);
   if(f2.f2_origin_scan_start_pos < 0) f2.f2_origin_scan_start_pos = f2.pos_origin;
   int lc_end = f2.body_scan_end_pos;
   if(f2.pos_confirm > lc_end) lc_end = f2.pos_confirm;
   if(f2.pos_invalid > lc_end) lc_end = f2.pos_invalid;
   f2.f2_lifecycle_scan_end_pos = lc_end;
   f2.f2_lifecycle_reason = reason;
   f2.reason = f2.reason + ";f2_lifecycle_" + reason;
}

#endif // __FP_F2_LIFECYCLE_RULES_MQH__
