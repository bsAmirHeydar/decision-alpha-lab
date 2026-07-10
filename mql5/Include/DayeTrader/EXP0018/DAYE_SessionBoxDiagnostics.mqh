#ifndef __EXP0018_DAYE_SESSION_BOX_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_SESSION_BOX_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxEvents.mqh>

string DAYE_FormatSessionBoxProjection(const DAYE_SessionBoxProjection &p)
{
   return "P09 box="+p.object_name+" symbol="+p.canonical_symbol+" session="+p.session_code+
          " chart="+IntegerToString(p.target_chart_id)+" status="+DAYE_SessionBoxProjectionStatusToString(p.status)+
          " high="+DoubleToString(p.geometry.high_price,8)+" low="+DoubleToString(p.geometry.low_price,8)+
          " reason="+p.reason_code;
}

string DAYE_FormatSessionBoxSummary(const DAYE_SessionBoxStoreSummary &s)
{
   return "EXP0018 P09 status="+DAYE_SessionBoxEngineStatusToString(s.status)+
          " source_sessions="+IntegerToString(s.source_session_count)+
          " eligible_symbol_sessions="+IntegerToString(s.eligible_symbol_session_count)+
          " projections="+IntegerToString(s.projection_count)+
          " created="+IntegerToString(s.created_count)+
          " open_updated="+IntegerToString(s.updated_open_count)+
          " closed_verified="+IntegerToString(s.verified_closed_count)+
          " repaired="+IntegerToString(s.repaired_count)+
          " waiting="+IntegerToString(s.waiting_chart_count)+
          " failures="+IntegerToString(s.failed_object_count)+
          " orphans_deleted="+IntegerToString(s.deleted_orphan_count)+
          " reason="+s.reason_code;
}

string DAYE_FormatSessionBoxEvent(const DAYE_SessionBoxEvent &e)
{
   return "EXP0018 P09 event="+DAYE_SessionBoxEventTypeToString(e.event_type)+
          " projection="+e.projection_id+" object="+e.object_name+
          " symbol="+e.broker_symbol+" session="+e.session_code+
          " reason="+e.reason_code;
}

#endif
