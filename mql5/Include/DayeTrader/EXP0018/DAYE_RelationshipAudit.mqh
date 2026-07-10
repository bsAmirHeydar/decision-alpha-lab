#ifndef __EXP0018_DAYE_RELATIONSHIP_AUDIT_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_AUDIT_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipDiagnostics.mqh>

class CDayeRelationshipAuditWriter
{
private:
   int m_handle;
   bool m_enabled;

   bool WriteHeader(void)
   {
      if(m_handle == INVALID_HANDLE)
         return false;
      FileWrite(m_handle,
                "schema_version","record_type","record_id","status","reason_code",
                "relationship_id","source_alias","family","selector","major","chart_label","doctrine_status","blocker_decision_id",
                "opportunity_id","current_period_code","current_period_instance_id","current_paired_period_id","current_completeness","current_trading_day_key",
                "reference_period_code","reference_period_instance_id","reference_paired_period_id","reference_completeness","reference_trading_day_key",
                "event_time_utc","availability_time_utc","processing_time_utc",
                "registry_count","ready_registry_count","blocked_registry_count","enabled_registry_count","source_period_count","resolved_count","ready_resolution_count","unavailable_resolution_count",
                "event_type","from_status","to_status");
      FileFlush(m_handle);
      return true;
   }

public:
   CDayeRelationshipAuditWriter(void)
   {
      m_handle = INVALID_HANDLE;
      m_enabled = false;
   }

   bool Open(const string filename,const bool enabled)
   {
      m_enabled = enabled;
      if(!enabled)
         return true;
      m_handle = FileOpen(filename,FILE_READ|FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_SHARE_READ|FILE_SHARE_WRITE,',');
      if(m_handle == INVALID_HANDLE)
      {
         Print("EXP0018 P04 audit open failed file=",filename," error=",GetLastError());
         return false;
      }
      if(FileSize(m_handle) == 0)
         return WriteHeader();
      FileSeek(m_handle,0,SEEK_END);
      return true;
   }

   bool WriteRegistry(const DAYE_RelationshipDefinition &item)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                item.schema_version,"REGISTRY",item.relationship_id,DAYE_RelationshipDoctrineStatusToString(item.doctrine_status),item.notes,
                item.relationship_id,item.source_alias,DAYE_RelationshipFamilyToString(item.family),DAYE_RelationshipSelectorToString(item.selector),item.is_major ? 1 : 0,item.chart_label,DAYE_RelationshipDoctrineStatusToString(item.doctrine_status),item.blocker_decision_id,
                "",item.current_period_code,"","","","",
                item.reference_period_code,"","","","",
                0,0,TimeGMT(),
                0,0,0,0,0,0,0,0,
                "","","");
      return true;
   }

   bool WriteSummary(const DAYE_RelationshipStoreSummary &summary)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                summary.schema_version,"SUMMARY",summary.run_key,DAYE_RelationshipResolutionStatusToString(summary.status),summary.reason_code,
                summary.latest_relationship_id,"","","",0,"","","",
                summary.latest_ready_opportunity_id,"",summary.latest_current_period_instance_id,"","","",
                "","","","","",
                summary.event_time_utc,summary.availability_time_utc,summary.processing_time_utc,
                summary.registry_count,summary.ready_registry_count,summary.blocked_registry_count,summary.enabled_registry_count,summary.source_period_count,summary.resolved_count,summary.ready_resolution_count,summary.unavailable_resolution_count,
                "","","");
      return true;
   }

   bool WriteResolution(const DAYE_RelationshipResolution &item)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                item.schema_version,"RESOLUTION",item.opportunity_id,DAYE_RelationshipResolutionStatusToString(item.status),item.reason_code,
                item.relationship_id,item.source_alias,DAYE_RelationshipFamilyToString(item.family),DAYE_RelationshipSelectorToString(item.selector),item.is_major ? 1 : 0,item.chart_label,"","",
                item.opportunity_id,item.current_period_code,item.current_period_instance_id,item.current_paired_period_id,DAYE_PeriodCompletenessToString(item.current_period.completeness),item.current_trading_day_key,
                item.reference_period_code,item.reference_period_instance_id,item.reference_paired_period_id,DAYE_PeriodCompletenessToString(item.reference_period.completeness),item.reference_trading_day_key,
                item.event_time_utc,item.availability_time_utc,item.processing_time_utc,
                0,0,0,0,0,0,0,0,
                "","","");
      return true;
   }

   bool WriteEvent(const DAYE_RelationshipEvent &event)
   {
      if(!m_enabled) return true;
      if(m_handle == INVALID_HANDLE) return false;
      FileWrite(m_handle,
                event.schema_version,"EVENT",event.event_id,DAYE_RelationshipResolutionStatusToString(event.to_status),event.reason_code,
                event.relationship_id,"","","",0,"","","",
                event.opportunity_id,"","","","","",
                "","","","","",
                event.event_time_utc,event.availability_time_utc,event.processing_time_utc,
                0,0,0,0,0,0,0,0,
                DAYE_RelationshipEventTypeToString(event.event_type),DAYE_RelationshipResolutionStatusToString(event.from_status),DAYE_RelationshipResolutionStatusToString(event.to_status));
      return true;
   }

   void Flush(void)
   {
      if(m_enabled && m_handle != INVALID_HANDLE)
         FileFlush(m_handle);
   }

   void Close(void)
   {
      if(m_handle != INVALID_HANDLE)
         FileClose(m_handle);
      m_handle = INVALID_HANDLE;
      m_enabled = false;
   }
};

#endif
