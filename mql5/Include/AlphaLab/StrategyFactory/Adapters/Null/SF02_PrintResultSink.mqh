#ifndef __SF02_PRINT_RESULT_SINK_MQH__
#define __SF02_PRINT_RESULT_SINK_MQH__

#include "../../Ports/ISF02_ResultSink.mqh"

class CSF02PrintResultSink : public ISF02ResultSink
{
private:
   bool m_ready;
   long m_events;
   long m_snapshots;
public:
   CSF02PrintResultSink(void) { m_ready = false; m_events = 0; m_snapshots = 0; }
   virtual string ServiceId(void) const { return "sf02.print_sink"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_RESULT_SINK; }
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error)
   { m_ready = true; error = ""; return true; }
   virtual bool Start(string &error) { error = ""; return m_ready; }
   virtual void Stop(void) {}
   virtual void Shutdown(void) { m_ready = false; }
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const
   {
      SF02_ServiceHealth h;
      h.service_id = ServiceId(); h.service_kind = ServiceKind();
      h.status = m_ready ? SF02_HEALTH_HEALTHY : SF02_HEALTH_UNHEALTHY;
      h.detail = "events=" + IntegerToString(m_events) + ",snapshots=" + IntegerToString(m_snapshots);
      h.observed_at_utc_msc = now_utc_msc; return h;
   }
   virtual bool WriteEvent(const SF01_AnatomyEvent &event, string &error)
   { m_events++; Print("SF02 EVENT ", event.event_id, " ", event.strategy_id); error = ""; return true; }
   virtual bool WriteSnapshot(const CSF01FeatureSnapshot &snapshot, string &error)
   { m_snapshots++; Print("SF02 SNAPSHOT ", snapshot.snapshot_id, " features=", snapshot.Size()); error = ""; return true; }
   virtual bool Flush(string &error) { error = ""; return true; }
   long EventCount(void) const { return m_events; }
   long SnapshotCount(void) const { return m_snapshots; }
};

#endif
