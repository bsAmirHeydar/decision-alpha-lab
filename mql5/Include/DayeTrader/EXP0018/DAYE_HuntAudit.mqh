#ifndef __EXP0018_DAYE_HUNT_AUDIT_MQH__
#define __EXP0018_DAYE_HUNT_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntDiagnostics.mqh>

class CDayeHuntAuditWriter
{
private:
   int m_handle;
   bool m_enabled;

   bool WriteHeader(void)
   {
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                "schema_version","record_type","record_id","status","reason_code",
                "observation_id","opportunity_id","relationship_id","source_alias","side","pair_state","major","chart_label",
                "current_period_code","current_period_instance_id","current_trading_day_key","current_open",
                "reference_period_code","reference_period_instance_id","reference_trading_day_key",
                "hunter_symbol","protected_symbol","one_sided","double_hunt","no_hunt",
                "symbol_a","a_state","a_reference","a_current","a_penetration","a_equality","a_beyond",
                "symbol_b","b_state","b_reference","b_current","b_penetration","b_equality","b_beyond",
                "event_time_utc","availability_time_utc","processing_time_utc",
                "source_resolution_count","observation_count","ready_count","unavailable_count","one_sided_count","double_count","none_count","equality_count",
                "event_type","from_status","to_status","from_pair_state","to_pair_state");
      FileFlush(m_handle);
      return true;
   }

public:
   CDayeHuntAuditWriter(void) { m_handle=INVALID_HANDLE; m_enabled=false; }

   bool Open(const string filename,const bool enabled)
   {
      m_enabled = enabled;
      if(!enabled) return true;
      m_handle = FileOpen(filename,FILE_READ|FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_SHARE_READ|FILE_SHARE_WRITE,',');
      if(m_handle == INVALID_HANDLE)
      {
         Print("EXP0018 P05 audit open failed file=",filename," error=",GetLastError());
         return false;
      }
      if(FileSize(m_handle) == 0) return WriteHeader();
      FileSeek(m_handle,0,SEEK_END);
      return true;
   }

   bool WriteSummary(const DAYE_HuntStoreSummary &summary)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                summary.schema_version,"SUMMARY",summary.run_key,DAYE_HuntObservationStatusToString(summary.status),summary.reason_code,
                summary.latest_observation_id,"",summary.latest_relationship_id,"","","",0,"",
                "",summary.latest_current_period_instance_id,"",0,
                "","","",
                "","",0,0,0,
                "","",0,0,0,0,0,
                "","",0,0,0,0,0,
                summary.event_time_utc,summary.availability_time_utc,summary.processing_time_utc,
                summary.source_resolution_count,summary.observation_count,summary.ready_observation_count,summary.unavailable_observation_count,summary.one_sided_count,summary.double_hunt_count,summary.no_hunt_count,summary.equality_hunt_count,
                "","","","","");
      return true;
   }

   bool WriteObservation(const DAYE_HuntObservation &item)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                item.schema_version,"OBSERVATION",item.observation_id,DAYE_HuntObservationStatusToString(item.status),item.reason_code,
                item.observation_id,item.opportunity_id,item.relationship_id,item.source_alias,DAYE_HuntSideToString(item.side),DAYE_HuntPairStateToString(item.pair_state),item.is_major ? 1 : 0,item.chart_label,
                item.current_period_code,item.current_period_instance_id,item.current_trading_day_key,item.current_period_is_open ? 1 : 0,
                item.reference_period_code,item.reference_period_instance_id,item.reference_trading_day_key,
                item.hunter_canonical_symbol,item.protected_canonical_symbol,item.is_one_sided ? 1 : 0,item.is_double_hunt ? 1 : 0,item.is_no_hunt ? 1 : 0,
                item.symbol_a.canonical_symbol,DAYE_SymbolHuntStateToString(item.symbol_a.state),item.symbol_a.reference_price,item.symbol_a.current_extreme,item.symbol_a.signed_penetration,item.symbol_a.touched_by_equality ? 1 : 0,item.symbol_a.touched_beyond ? 1 : 0,
                item.symbol_b.canonical_symbol,DAYE_SymbolHuntStateToString(item.symbol_b.state),item.symbol_b.reference_price,item.symbol_b.current_extreme,item.symbol_b.signed_penetration,item.symbol_b.touched_by_equality ? 1 : 0,item.symbol_b.touched_beyond ? 1 : 0,
                item.event_time_utc,item.availability_time_utc,item.processing_time_utc,
                0,0,0,0,0,0,0,0,
                "","","","","");
      return true;
   }

   bool WriteEvent(const DAYE_HuntEvent &event)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                event.schema_version,"EVENT",event.event_id,DAYE_HuntObservationStatusToString(event.to_status),event.reason_code,
                event.observation_id,event.opportunity_id,event.relationship_id,"",DAYE_HuntSideToString(event.side),DAYE_HuntPairStateToString(event.to_pair_state),0,"",
                "","","",0,
                "","","",
                "","",0,0,0,
                "","",0,0,0,0,0,
                "","",0,0,0,0,0,
                event.event_time_utc,event.availability_time_utc,event.processing_time_utc,
                0,0,0,0,0,0,0,0,
                DAYE_HuntEventTypeToString(event.event_type),DAYE_HuntObservationStatusToString(event.from_status),DAYE_HuntObservationStatusToString(event.to_status),DAYE_HuntPairStateToString(event.from_pair_state),DAYE_HuntPairStateToString(event.to_pair_state));
      return true;
   }

   void Flush(void) { if(m_enabled && m_handle != INVALID_HANDLE) FileFlush(m_handle); }
   void Close(void)
   {
      if(m_handle != INVALID_HANDLE) FileClose(m_handle);
      m_handle=INVALID_HANDLE;
      m_enabled=false;
   }
};

#endif
