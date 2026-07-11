#ifndef __SF05_APPEND_ONLY_MEMORY_SINK_MQH__
#define __SF05_APPEND_ONLY_MEMORY_SINK_MQH__
#include "ISF05_VersionedResultSink.mqh"
#include "SF05_EnvelopeFactory.mqh"

class CSF05AppendOnlyMemorySink:public ISF05VersionedResultSink
{
private:
   SF05_RunManifest m_manifest;
   SF05_RuntimeGenerationRecord m_generation;
   SF05_ResultSinkConfig m_config;
   SF05_ResultEnvelope m_records[];
   CSF05EnvelopeFactory m_factory;
   SF05_ResultSinkTelemetry m_telemetry;
   bool m_configured;
   bool m_ready;
   bool m_sealed;
   bool Seen(const string id)const{for(int i=0;i<ArraySize(m_records);i++)if(m_records[i].record_id==id)return true;return false;}
   bool Append(SF05_ResultEnvelope &v,string &e){if(m_sealed){e="sink sealed";return false;}if(!SF05_ValidateResultEnvelope(v,e))return false;if(v.sequence!=m_telemetry.last_sequence+1){e="non-monotonic sequence";return false;}if(Seen(v.record_id)){m_telemetry.duplicate_rejections++;e="duplicate record";return false;}int n=ArraySize(m_records);ArrayResize(m_records,n+1);m_records[n]=v;m_telemetry.records_written++;m_telemetry.last_sequence=v.sequence;m_telemetry.bytes_written+=StringLen(v.payload_json);e="";return true;}
public:
   CSF05AppendOnlyMemorySink(void){m_configured=false;m_ready=false;m_sealed=false;ZeroMemory(m_telemetry);}
   virtual string ServiceId(void)const{return "sf05.memory_sink";}
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void)const{return SF02_SERVICE_RESULT_SINK;}
   virtual bool Configure(const SF05_RunManifest &m,const SF05_RuntimeGenerationRecord &g,const SF05_ResultSinkConfig &c,string &e){if(!SF05_ValidateRunManifest(m,e)||!SF05_ValidateRuntimeGeneration(g,e)||!SF05_ValidateResultSinkConfig(c,e))return false;m_manifest=m;m_generation=g;m_config=c;m_factory.Configure(m.run_id,g.generation_uid);m_configured=true;e="";return true;}
   virtual bool Initialize(const SF02_RuntimeConfig &c,string &e){if(!m_configured){e="sink not configured";return false;}m_ready=true;SF05_ResultEnvelope manifest_record=m_factory.Create(SF05_RECORD_RUN_MANIFEST,m_manifest.manifest_id,"sf05.manifest","1.0.0",m_manifest.created_at,m_manifest.created_at,"alpha_lab.strategy_factory/run_manifest@1.0.0",SF05_RunManifestToJson(m_manifest));if(!Append(manifest_record,e))return false;SF01_MarketTimestamp known=m_generation.compiled_at;if(m_generation.activated_at.utc_epoch_milliseconds>=m_generation.compiled_at.utc_epoch_milliseconds)known=m_generation.activated_at;SF05_ResultEnvelope generation_record=m_factory.Create(SF05_RECORD_GENERATION,m_generation.generation_uid,"sf05.generation_compiler","1.0.0",m_generation.compiled_at,known,"alpha_lab.strategy_factory/runtime_generation@1.0.0",SF05_RuntimeGenerationToJson(m_generation));if(!Append(generation_record,e))return false;e="";return true;}
   virtual bool Start(string &e){if(!m_ready){e="sink not initialized";return false;}e="";return true;}
   virtual void Stop(void){}
   virtual void Shutdown(void){m_ready=false;}
   virtual SF02_ServiceHealth Health(const long now)const{SF02_ServiceHealth h;h.service_id=ServiceId();h.service_kind=ServiceKind();h.status=(m_ready&&!m_sealed)?SF02_HEALTH_HEALTHY:(m_sealed?SF02_HEALTH_DEGRADED:SF02_HEALTH_UNHEALTHY);h.detail="records="+IntegerToString(m_telemetry.records_written)+",sealed="+(m_sealed?"true":"false");h.observed_at_utc_msc=now;return h;}
   virtual bool WriteEnvelope(SF05_ResultEnvelope &v,string &e){return Append(v,e);}
   virtual bool WriteEvent(const SF01_AnatomyEvent &event,string &e){string payload=SF01_AnatomyEventToJson(event);SF05_ResultEnvelope v=m_factory.Create(SF05_RECORD_ANATOMY_EVENT,event.event_id,event.producer_id,event.producer_version,event.event_time,event.known_time,"alpha_lab.strategy_factory/anatomy_event@1.0.0",payload);bool ok=Append(v,e);if(ok)m_telemetry.events_written++;return ok;}
   virtual bool WriteSnapshot(const CSF01FeatureSnapshot &snapshot,string &e){string features="[";for(int i=0;i<snapshot.Size();i++){SF01_FeatureValue x;snapshot.At(i,x);if(i>0)features+=",";features+=SF01_FeatureValueToJson(x);}features+="]";string payload="{\"snapshot_id\":\""+snapshot.snapshot_id+"\",\"event_id\":\""+snapshot.event_id+"\",\"strategy_id\":\""+snapshot.strategy_id+"\",\"snapshot_time\":"+SF01_TimestampToJson(snapshot.snapshot_time)+",\"producer_id\":\""+snapshot.producer_id+"\",\"producer_version\":\""+snapshot.producer_version+"\",\"source_hash\":\""+snapshot.source_hash+"\",\"state_generation\":"+IntegerToString(snapshot.state_generation)+",\"features\":"+features+"}";SF05_ResultEnvelope v=m_factory.Create(SF05_RECORD_FEATURE_SNAPSHOT,snapshot.snapshot_id,snapshot.producer_id,snapshot.producer_version,snapshot.snapshot_time,snapshot.snapshot_time,"alpha_lab.strategy_factory/feature_snapshot@1.0.0",payload);bool ok=Append(v,e);if(ok)m_telemetry.snapshots_written++;return ok;}
   virtual bool Flush(string &e){m_telemetry.flush_count++;e="";return true;}
   virtual bool Seal(const SF01_MarketTimestamp &t,string &e){if(m_sealed){e="";return true;}m_sealed=true;e="";return true;}
   virtual bool IsSealed(void)const{return m_sealed;}
   virtual SF05_ResultSinkTelemetry Telemetry(void)const{return m_telemetry;}
   int Count(void)const{return ArraySize(m_records);}
   bool At(const int i,SF05_ResultEnvelope &v)const{if(i<0||i>=ArraySize(m_records))return false;v=m_records[i];return true;}
};
#endif
