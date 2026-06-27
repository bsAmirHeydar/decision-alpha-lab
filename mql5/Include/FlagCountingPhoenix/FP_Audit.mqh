#ifndef __FP_AUDIT_MQH__
#define __FP_AUDIT_MQH__
#property strict

#include "FP_Renderer.mqh"

void FP_PrintSummary(const string symbol,
                     const ENUM_TIMEFRAMES period,
                     const int bars,
                     const int scale_count,
                     const FP_DetectResult &result,
                     const int drawn)
{
   Print("FP_SUMMARY symbol=", symbol,
         " tf=", EnumToString(period),
         " bars=", bars,
         " scales=", scale_count,
         " nodes=", result.nodes_total,
         " hooks=", result.hooks_total,
         " nd=", result.nd_total,
         " events=", result.events_total,
         " visible=", result.visible_events_total,
         " f1=", result.f1_total,
         " f2=", result.f2_total,
         " f3=", result.f3_total,
         " invalid=", result.invalid_total,
         " drawn=", drawn);
}

string FP_NodeAudit(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + "#" + IntegerToString(n.id) +
          " L" + IntegerToString(n.L) +
          " i" + IntegerToString(n.index_anchor) +
          " p" + DoubleToString(n.price, _Digits);
}

void FP_PrintEventAudit(const FP_FlagEvent &e)
{
   Print("FP_EVENT",
         " id=", e.event_id,
         " seq=", e.sequence_id,
         " parent=", e.parent_event_id,
         " level=", FP_LevelName(e.level),
         " dir=", FP_DirectionName(e.direction),
         " L=", e.scale_L,
         " status=", FP_StatusName(e.status),
         " visible=", FP_BoolName(e.visible_main),
         " size=", DoubleToString(e.flag_size, _Digits),
         " ratio=", DoubleToString(e.size_ratio, 4),
         " O=", FP_NodeAudit(e.origin),
         " A=", FP_NodeAudit(e.leg1),
         " W=", FP_NodeAudit(e.waist),
         " B=", FP_NodeAudit(e.leg2),
         " C=", FP_NodeAudit(e.confirm),
         " internal_count=", e.internal_pack.count,
         " reason=", e.reason);
}

void FP_PrintHookAudit(const FP_HookBranch &h)
{
   Print("FP_HOOK",
         " id=", h.branch_id,
         " dir=", FP_DirectionName(h.direction),
         " L=", h.scale_L,
         " nodes=", h.node_count,
         " nd=", FP_BoolName(h.is_nd),
         " retrace=", DoubleToString(h.retrace_ratio, 4),
         " start=", FP_NodeAudit(h.start_node),
         " extreme=", FP_NodeAudit(h.extreme_node),
         " resolve=", FP_NodeAudit(h.resolve_node),
         " reason=", h.reason);
}

#endif // __FP_AUDIT_MQH__
