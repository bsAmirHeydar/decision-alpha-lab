#ifndef __SF05_COMPOSITE_RESULT_SINK_MQH__
#define __SF05_COMPOSITE_RESULT_SINK_MQH__
#include "ISF05_VersionedResultSink.mqh"
class CSF05CompositeResultSink:public ISF05VersionedResultSink
{
private:ISF05VersionedResultSink *m_primary;ISF05VersionedResultSink *m_mirror;bool m_configured;
public:CSF05CompositeResultSink(void){m_primary=NULL;m_mirror=NULL;m_configured=false;}void Bind(ISF05VersionedResultSink *p,ISF05VersionedResultSink *m){m_primary=p;m_mirror=m;}
virtual string ServiceId(void)const{return "sf05.composite_sink";}virtual ENUM_SF02_SERVICE_KIND ServiceKind(void)const{return SF02_SERVICE_RESULT_SINK;}
virtual bool Configure(const SF05_RunManifest &a,const SF05_RuntimeGenerationRecord &g,const SF05_ResultSinkConfig &c,string &e){if(CheckPointer(m_primary)==POINTER_INVALID||CheckPointer(m_mirror)==POINTER_INVALID){e="composite sink not bound";return false;}if(!m_primary.Configure(a,g,c,e)||!m_mirror.Configure(a,g,c,e))return false;m_configured=true;e="";return true;}
virtual bool Initialize(const SF02_RuntimeConfig &c,string &e){if(!m_configured){e="not configured";return false;}return m_primary.Initialize(c,e)&&m_mirror.Initialize(c,e);}virtual bool Start(string &e){return m_primary.Start(e)&&m_mirror.Start(e);}virtual void Stop(void){m_primary.Stop();m_mirror.Stop();}virtual void Shutdown(void){m_primary.Shutdown();m_mirror.Shutdown();}virtual SF02_ServiceHealth Health(const long now)const{SF02_ServiceHealth a=m_primary.Health(now),b=m_mirror.Health(now);if(a.status==SF02_HEALTH_UNHEALTHY)return a;if(b.status==SF02_HEALTH_UNHEALTHY)return b;return a;}
virtual bool WriteEnvelope(SF05_ResultEnvelope &v,string &e){SF05_ResultEnvelope copy=v;if(!m_primary.WriteEnvelope(v,e))return false;if(!m_mirror.WriteEnvelope(copy,e))return false;return true;}virtual bool WriteEvent(const SF01_AnatomyEvent &v,string &e){return m_primary.WriteEvent(v,e)&&m_mirror.WriteEvent(v,e);}virtual bool WriteSnapshot(const CSF01FeatureSnapshot &v,string &e){return m_primary.WriteSnapshot(v,e)&&m_mirror.WriteSnapshot(v,e);}virtual bool Flush(string &e){return m_primary.Flush(e)&&m_mirror.Flush(e);}virtual bool Seal(const SF01_MarketTimestamp &t,string &e){return m_primary.Seal(t,e)&&m_mirror.Seal(t,e);}virtual bool IsSealed(void)const{return m_primary.IsSealed()&&m_mirror.IsSealed();}virtual SF05_ResultSinkTelemetry Telemetry(void)const{return m_primary.Telemetry();}
};
#endif
