#ifndef __SF03_MARKET_SERVICE_BUNDLE_MQH__
#define __SF03_MARKET_SERVICE_BUNDLE_MQH__
#include "SF03_TimeKernel.mqh"
#include "SF03_TerminalMarketSource.mqh"
#include "SF03_MarketDataService.mqh"
#include "SF03_SymbolSpecCache.mqh"
#include "SF03_SessionSchedule.mqh"

class CSF03MarketServiceBundle
{
private:
   CSF03TimeKernel m_clock;
   CSF03TerminalMarketSource m_source;
   CSF03MarketDataService m_market;
   CSF03SymbolSpecCache m_specs;
   CSF03SessionSchedule m_sessions;
public:
   CSF03MarketServiceBundle(void)
   {
      m_source.BindClock(&m_clock);
      m_market.BindSource(&m_source);
      m_market.BindClock(&m_clock);
      m_specs.BindSource(&m_source);
   }

   CSF03TimeKernel *Clock(void){ return &m_clock; }
   CSF03MarketDataService *Market(void){ return &m_market; }
   CSF03SymbolSpecCache *Specs(void){ return &m_specs; }
   CSF03SessionSchedule *Sessions(void){ return &m_sessions; }

   bool Initialize(const SF02_RuntimeConfig &runtime_config,
                   const SF03_ClockConfig &clock_config,string &error)
   {
      m_clock.Configure(clock_config);
      if(!m_clock.Initialize(runtime_config,error)) return false;
      if(!m_market.Initialize(runtime_config,error)) return false;
      if(!m_specs.Initialize(runtime_config,error)) return false;
      return true;
   }
   bool Start(string &error)
   {
      if(!m_clock.Start(error)) return false;
      if(!m_market.Start(error)) return false;
      if(!m_specs.Start(error)) return false;
      return true;
   }
   void Stop(void){ m_specs.Stop(); m_market.Stop(); m_clock.Stop(); }
   void Shutdown(void){ m_specs.Shutdown(); m_market.Shutdown(); m_clock.Shutdown(); }
};
#endif
