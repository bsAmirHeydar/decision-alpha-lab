#ifndef __SF02_NO_SEND_EXECUTION_BOUNDARY_MQH__
#define __SF02_NO_SEND_EXECUTION_BOUNDARY_MQH__

#include "../../Ports/ISF02_ExecutionBoundary.mqh"

class CSF02NoSendExecutionBoundary : public ISF02ExecutionBoundary
{
private:
   bool m_ready;
public:
   CSF02NoSendExecutionBoundary(void) { m_ready = false; }
   virtual string ServiceId(void) const { return "sf02.no_send_execution"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_EXECUTION_BOUNDARY; }
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
      h.detail = "no-send boundary"; h.observed_at_utc_msc = now_utc_msc; return h;
   }
   virtual bool HasLiveOrderAuthority(void) const { return false; }
   virtual string AuthorityDescription(void) const { return "NO_ORDER_SEND_NO_CTRADE_NO_BROKER_AUTHORITY"; }
};

#endif
