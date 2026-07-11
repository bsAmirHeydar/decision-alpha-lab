#ifndef __SF02_NULL_FEATURE_PROVIDER_MQH__
#define __SF02_NULL_FEATURE_PROVIDER_MQH__

#include "../../Ports/ISF02_FeatureProvider.mqh"
#include "../../Contracts/SF01_ContractRegistry.mqh"

class CSF02NullFeatureProvider : public ISF02FeatureProvider
{
private:
   bool m_ready;
public:
   CSF02NullFeatureProvider(void) { m_ready = false; }
   virtual string ServiceId(void) const { return "sf02.null_features"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_FEATURES; }
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
      h.detail = "null feature provider"; h.observed_at_utc_msc = now_utc_msc; return h;
   }
   virtual bool BuildSnapshot(const SF01_AnatomyEvent &event,
                              const long state_generation,
                              CSF01FeatureSnapshot &snapshot,
                              string &error)
   {
      snapshot.schema = SF01_FeatureSnapshotSchema();
      snapshot.event_id = event.event_id;
      snapshot.strategy_id = event.strategy_id;
      snapshot.snapshot_time = event.confirmation_time;
      snapshot.producer_id = ServiceId();
      snapshot.producer_version = "1.0.0";
      snapshot.source_hash = event.source_hash;
      snapshot.state_generation = state_generation;
      snapshot.snapshot_id = snapshot.DeriveId();
      return snapshot.Validate(error);
   }
};

#endif
