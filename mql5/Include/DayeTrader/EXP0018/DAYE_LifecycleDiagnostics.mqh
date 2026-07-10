#ifndef __EXP0018_DAYE_LIFECYCLE_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_LIFECYCLE_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleCheckpoint.mqh>

string DAYE_FormatLifecycleReference(const DAYE_ReferenceLifecycleRecord &r)
{
   return "reference="+r.reference_id+" state="+DAYE_ReferenceLifecycleStateToString(r.state)+
          " side="+DAYE_HuntSideToString(r.side)+" protected="+r.protected_canonical_symbol+
          " uses="+IntegerToString(r.accepted_use_count)+" reason="+r.reason_code;
}

string DAYE_FormatLifecycleUse(const DAYE_ReferenceUseRecord &u)
{
   return "use="+u.use_id+" status="+DAYE_ReferenceUseStatusToString(u.status)+
          " relationship="+u.relationship_id+" hunter="+u.hunter_canonical_symbol+
          " protected="+u.protected_canonical_symbol+" reason="+u.reason_code;
}

string DAYE_FormatLifecycleSummary(const DAYE_LifecycleStoreSummary &s)
{
   return "EXP0018 P07 status="+DAYE_LifecycleStatusToString(s.status)+
          " ready="+(s.is_ready?"true":"false")+
          " references="+IntegerToString(s.reference_count)+
          " surviving="+IntegerToString(s.surviving_reference_count)+
          " retired="+IntegerToString(s.retired_reference_count)+
          " accepted_uses="+IntegerToString(s.accepted_use_count)+
          " duplicate_uses="+IntegerToString(s.duplicate_use_count)+
          " rejected_uses="+IntegerToString(s.rejected_use_count)+
          " reason="+s.reason_code;
}

string DAYE_FormatLifecycleEvent(const DAYE_LifecycleEvent &e)
{
   return "EXP0018 P07 event="+DAYE_LifecycleEventTypeToString(e.event_type)+
          " reference="+e.reference_id+" use="+e.use_id+" reason="+e.reason_code;
}

#endif
