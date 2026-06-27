#ifndef __FC6_AUDIT_MQH__
#define __FC6_AUDIT_MQH__
#property strict
#include "FC6_Types.mqh"

string FC6_NodeAudit(const FC6_Node &n)
{
   if(!FC6_NodeValid(n)) return "NA";
   return FC6_NodeKindToString(n.kind) + "@" + TimeToString(n.time_anchor, TIME_DATE|TIME_MINUTES) + ":" + DoubleToString(n.price, _Digits) + ":L" + IntegerToString(n.L);
}

string FC6_InternalAudit(const FC6_InternalPack &p)
{
   string s = "count=" + IntegerToString(p.count);
   if(p.count >= 1) s += ";1=" + FC6_NodeAudit(p.n1);
   if(p.count >= 2) s += ";2=" + FC6_NodeAudit(p.n2);
   if(p.count >= 3) s += ";3=" + FC6_NodeAudit(p.n3);
   if(p.count >= 4) s += ";4=" + FC6_NodeAudit(p.n4);
   s += ";nd=" + (p.is_nd ? "true" : "false");
   return s;
}

void FC6_PrintEventAudit(const FC6_FlagEvent &e)
{
   Print("FC6_EVENT id=", e.event_id,
         " seq=", e.sequence_id,
         " parent=", e.parent_event_id,
         " level=", FC6_LevelToString(e.level),
         " dir=", FC6_DirectionToString(e.direction),
         " status=", FC6_StatusToString(e.status),
         " branch=", FC6_BranchModeToString(e.branch_mode),
         " L=", e.scale_L,
         " O=", FC6_NodeAudit(e.origin),
         " L1=", FC6_NodeAudit(e.leg1),
         " W=", FC6_NodeAudit(e.waist),
         " L2=", FC6_NodeAudit(e.leg2),
         " C=", FC6_NodeAudit(e.confirm),
         " INV=", FC6_NodeAudit(e.invalid),
         " size=", DoubleToString(e.flag_size, _Digits),
         " parentSize=", DoubleToString(e.parent_flag_size, _Digits),
         " ratio=", DoubleToString(e.size_ratio, 4),
         " internal={", FC6_InternalAudit(e.internal_pack), "}",
         " reason=", e.reason);
}

void FC6_PrintHookAudit(const FC6_HookBranch &h)
{
   Print("FC6_HOOK id=", h.branch_id,
         " seq=", h.sequence_id,
         " dir=", FC6_DirectionToString(h.direction),
         " L=", h.scale_L,
         " count=", h.node_count,
         " nd=", (h.is_nd ? "true" : "false"),
         " ratio=", DoubleToString(h.retrace_ratio, 4),
         " start=", FC6_NodeAudit(h.start_node),
         " extreme=", FC6_NodeAudit(h.extreme_node),
         " resolve=", FC6_NodeAudit(h.resolve_node),
         " reason=", h.reason);
}

void FC6_PrintSummary(const string symbol,
                      const ENUM_TIMEFRAMES tf,
                      const int bar_count,
                      const int scale_count,
                      const FC6_DetectResult &r,
                      const int drawn)
{
   Print("FC6_SUMMARY symbol=", symbol,
         " tf=", EnumToString(tf),
         " bars=", bar_count,
         " scales=", scale_count,
         " events=", r.events_total,
         " hooks=", r.hooks_total,
         " nd=", r.nd_total,
         " f1=", r.f1_total,
         " f2=", r.f2_total,
         " f3=", r.f3_total,
         " drawn=", drawn);
}

#endif // __FC6_AUDIT_MQH__
