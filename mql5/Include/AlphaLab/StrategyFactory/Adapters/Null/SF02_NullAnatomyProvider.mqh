#ifndef __SF02_NULL_ANATOMY_PROVIDER_MQH__
#define __SF02_NULL_ANATOMY_PROVIDER_MQH__

#include "../../Ports/ISF02_AnatomyProvider.mqh"

class CSF02NullAnatomyProvider : public ISF02AnatomyProvider
{
private:
   bool m_ready;
public:
   CSF02NullAnatomyProvider(void) { m_ready = false; }
   virtual string ServiceId(void) const { return "sf02.null_anatomy"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_ANATOMY; }
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
      h.detail = "null anatomy provider"; h.observed_at_utc_msc = now_utc_msc; return h;
   }
   virtual void ProcessTick(const MqlTick &tick) {}
   virtual void ProcessTimer(const long now_utc_msc) {}
   virtual bool PopEvent(SF01_AnatomyEvent &event) { return false; }
   virtual int PendingEventCount(void) const { return 0; }
};

#endif
