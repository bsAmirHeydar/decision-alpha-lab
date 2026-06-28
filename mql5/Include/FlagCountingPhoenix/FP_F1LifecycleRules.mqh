#ifndef __FP_F1_LIFECYCLE_RULES_MQH__
#define __FP_F1_LIFECYCLE_RULES_MQH__
#property strict

#include "FP_InternalCountEngine.mqh"

// ============================================================================
// Phoenix Level 07 - F1 Lifecycle Rules
// ----------------------------------------------------------------------------
// Pure rule helpers for F1 lifecycle promotion.  This layer consumes Level 05
// body facts and Level 06 internal-count evidence.  It does not build F2/F3,
// draw objects, or perform sequence ownership pruning.
// ============================================================================

string FP_F1LifecycleNodePart(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + IntegerToString(n.id) + "@" + IntegerToString(n.index_anchor);
}

string FP_BuildF1LifecycleId(const FP_FlagEvent &f1)
{
   return "F1LC|" + FP_DirectionName(f1.direction) +
          "|L" + IntegerToString(f1.scale_L) +
          "|seq" + IntegerToString(f1.sequence_id) +
          "|body=" + f1.body_id +
          "|O=" + FP_F1LifecycleNodePart(f1.origin) +
          "|A=" + FP_F1LifecycleNodePart(f1.leg1) +
          "|W=" + FP_F1LifecycleNodePart(f1.waist) +
          "|B=" + FP_F1LifecycleNodePart(f1.leg2) +
          "|I=" + f1.internal_pack.internal_pack_id;
}

bool FP_F1PhaseGatePasses(const bool from_phase_boundary,
                          const bool from_fail_open,
                          const FP_Config &cfg)
{
   if(from_phase_boundary) return true;
   if(from_fail_open && cfg.allow_f1_fail_open_when_no_hook) return true;
   if(!cfg.require_f1_phase_boundary) return true;
   return false;
}

bool FP_F1StatusCanSpawnF2(const FP_FlagEvent &f1)
{
   if(f1.level != FP_LEVEL_F1) return false;
   if(f1.status != FP_STATUS_CONFIRMED) return false;
   if(!f1.has_confirm) return false;
   if(!f1.lifecycle_can_spawn_f2) return false;
   return true;
}

bool FP_F1ShouldBeVisibleForLifecycle(const FP_FlagEvent &f1, const FP_Config &cfg)
{
   if(f1.status == FP_STATUS_INVALIDATED) return cfg.show_invalidated_in_audit;
   if(f1.status == FP_STATUS_CONFIRMED) return true;
   if(f1.status == FP_STATUS_POST_FLAG) return cfg.f1_show_post_flag_candidates;
   if(f1.status == FP_STATUS_LIVE_BODY || f1.status == FP_STATUS_LIVE_LEG) return cfg.f1_show_live_body_candidates;
   return f1.visible_main;
}

void FP_SetF1LifecycleState(FP_FlagEvent &f1,
                            const int lifecycle_status,
                            const string reason)
{
   f1.lifecycle_id = FP_BuildF1LifecycleId(f1);
   f1.lifecycle_status = lifecycle_status;
   f1.lifecycle_stage_level = FP_LEVEL_F1;
   f1.lifecycle_body_complete = (f1.has_origin && f1.has_leg1 && f1.has_waist && f1.has_leg2 &&
                                 (f1.body_status == FP_BODY_COMPLETE || f1.body_status == FP_BODY_EXTENDED));
   f1.lifecycle_internal_ready = (f1.internal_pack.valid12 || f1.internal_pack.has_valid12);
   f1.lifecycle_can_spawn_f2 = FP_F1StatusCanSpawnF2(f1);
   f1.lifecycle_scan_start_pos = f1.pos_origin;
   int lc_end = f1.body_scan_end_pos;
   if(f1.pos_confirm > lc_end) lc_end = f1.pos_confirm;
   if(f1.pos_invalid > lc_end) lc_end = f1.pos_invalid;
   f1.lifecycle_scan_end_pos = lc_end;
   f1.lifecycle_reason = reason;
   f1.reason = f1.reason + ";f1_lifecycle_" + reason;
}

#endif // __FP_F1_LIFECYCLE_RULES_MQH__
