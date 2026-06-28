#ifndef __FP_F3_LIFECYCLE_RULES_MQH__
#define __FP_F3_LIFECYCLE_RULES_MQH__
#property strict

#include "FP_F2LifecycleEngine.mqh"

// ============================================================================
// Phoenix Level 09 - F3 Lifecycle Rules
// ----------------------------------------------------------------------------
// F3 is the terminal child of a confirmed/authorized F2.  It is body-complete
// and OR-qualified by either parent-size or parent-L evidence.  It does not
// require a post-body internal count in this layer.
// ============================================================================

string FP_F3LifecycleNodePart(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + IntegerToString(n.id) + "@" + IntegerToString(n.index_anchor);
}

string FP_BuildF3LifecycleId(const FP_FlagEvent &f3)
{
   return "F3LC|" + FP_DirectionName(f3.direction) +
          "|L" + IntegerToString(f3.scale_L) +
          "|seq" + IntegerToString(f3.sequence_id) +
          "|parent=" + IntegerToString(f3.parent_event_id) +
          "|body=" + f3.body_id +
          "|O=" + FP_F3LifecycleNodePart(f3.origin) +
          "|A=" + FP_F3LifecycleNodePart(f3.leg1) +
          "|W=" + FP_F3LifecycleNodePart(f3.waist) +
          "|B=" + FP_F3LifecycleNodePart(f3.leg2) +
          "|size_ratio=" + DoubleToString(f3.f3_parent_size_ratio, 4) +
          "|L_ratio=" + DoubleToString(f3.f3_parent_leg1_L_ratio, 4) +
          "|or=" + FP_BoolName(f3.f3_or_gate_passed) +
          "|locked=" + FP_BoolName(f3.f3_locked);
}

bool FP_F3ParentGatePasses(const FP_FlagEvent &f2)
{
   return FP_F2StatusCanSpawnF3(f2);
}

bool FP_F3SizeGatePasses(const FP_FlagEvent &f3, const FP_FlagEvent &f2, const FP_Config &cfg)
{
   if(f2.flag_size <= 0.0) return false;
   return (f3.flag_size >= cfg.f3_min_parent_size_ratio * f2.flag_size);
}

bool FP_F3Leg1LGatePasses(const FP_FlagEvent &f3, const FP_FlagEvent &f2, const FP_Config &cfg)
{
   int parent_L = MathMax(1, f2.leg1_L);
   int min_leg1_L = (int)MathCeil(cfg.f3_leg1_L_min_ratio * (double)parent_L);
   return (f3.leg1_L >= min_leg1_L);
}

bool FP_F3OrGatePasses(const FP_FlagEvent &f3, const FP_FlagEvent &f2, const FP_Config &cfg)
{
   return (FP_F3SizeGatePasses(f3, f2, cfg) || FP_F3Leg1LGatePasses(f3, f2, cfg));
}

bool FP_F3StatusCanLock(const FP_FlagEvent &f3)
{
   if(f3.level != FP_LEVEL_F3) return false;
   if(f3.status != FP_STATUS_COMPLETED && f3.status != FP_STATUS_LOCKED) return false;
   if(!f3.f3_terminal_complete) return false;
   if(!f3.f3_or_gate_passed) return false;
   return true;
}

bool FP_F3ShouldBeVisibleForLifecycle(const FP_FlagEvent &f3, const FP_Config &cfg)
{
   if(f3.status == FP_STATUS_LOCKED || f3.status == FP_STATUS_COMPLETED) return true;
   if(f3.status == FP_STATUS_LIVE_BODY || f3.status == FP_STATUS_LIVE_LEG) return cfg.f3_show_live_body_candidates;
   if(!f3.f3_or_gate_passed) return cfg.f3_show_or_rejected_candidates;
   return f3.visible_main;
}

void FP_SetF3LifecycleState(FP_FlagEvent &f3,
                            const int lifecycle_status,
                            const string reason)
{
   f3.f3_lifecycle_status = lifecycle_status;
   f3.f3_body_complete = (f3.has_origin && f3.has_leg1 && f3.has_waist && f3.has_leg2 &&
                          (f3.body_status == FP_BODY_COMPLETE || f3.body_status == FP_BODY_EXTENDED));
   f3.f3_terminal_complete = (f3.status == FP_STATUS_COMPLETED || f3.status == FP_STATUS_LOCKED);
   f3.f3_lock_ready = FP_F3StatusCanLock(f3);
   f3.f3_lifecycle_id = FP_BuildF3LifecycleId(f3);
   if(f3.f3_origin_scan_start_pos < 0) f3.f3_origin_scan_start_pos = f3.pos_origin;
   int lc_end = f3.body_scan_end_pos;
   if(f3.has_extension && f3.pos_extension_end > lc_end) lc_end = f3.pos_extension_end;
   f3.f3_lifecycle_scan_end_pos = lc_end;
   f3.f3_lifecycle_reason = reason;
   f3.reason = f3.reason + ";f3_lifecycle_" + reason;
}

#endif // __FP_F3_LIFECYCLE_RULES_MQH__
