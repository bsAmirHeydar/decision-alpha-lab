#ifndef __SF02_TERMINAL_CLOCK_MQH__
#define __SF02_TERMINAL_CLOCK_MQH__

#include "../../Ports/ISF02_ClockPort.mqh"

class CSF02TerminalClock : public ISF02ClockPort
{
private:
   bool m_initialized;
public:
   CSF02TerminalClock(void) { m_initialized = false; }
   virtual string ServiceId(void) const { return "sf02.terminal_clock"; }
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_CLOCK; }
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error)
   { m_initialized = true; error = ""; return true; }
   virtual bool Start(string &error) { error = ""; return m_initialized; }
   virtual void Stop(void) {}
   virtual void Shutdown(void) { m_initialized = false; }
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const
   {
      SF02_ServiceHealth h;
      h.service_id = ServiceId(); h.service_kind = ServiceKind();
      h.status = m_initialized ? SF02_HEALTH_HEALTHY : SF02_HEALTH_UNHEALTHY;
      h.detail = m_initialized ? "terminal clock ready" : "terminal clock not initialized";
      h.observed_at_utc_msc = now_utc_msc;
      return h;
   }
   virtual long UtcNowMilliseconds(void) const { return ((long)TimeGMT()) * 1000; }
   virtual ulong MonotonicMicroseconds(void) const { return GetMicrosecondCount(); }
   virtual SF01_MarketTimestamp Now(const string source_clock_id = "runtime") const
   { return SF01_MakeUtcMilliseconds(UtcNowMilliseconds(), "UTC", 0, source_clock_id, SF01_TIME_MILLISECONDS); }
};

#endif
