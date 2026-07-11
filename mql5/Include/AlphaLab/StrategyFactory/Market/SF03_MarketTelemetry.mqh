#ifndef __SF03_MARKET_TELEMETRY_MQH__
#define __SF03_MARKET_TELEMETRY_MQH__
#include "SF03_MarketTypes.mqh"
class CSF03MarketTelemetry
{
private:
   SF03_MarketTelemetrySnapshot m_value;
public:
   CSF03MarketTelemetry(void){ ZeroMemory(m_value); }
   void TickUpdate(void){ m_value.tick_updates++; }
   void TickHit(void){ m_value.tick_hits++; }
   void TickMiss(void){ m_value.tick_misses++; }
   void BarRefresh(void){ m_value.bar_refreshes++; }
   void BarInserted(void){ m_value.bar_insertions++; }
   void BarReplaced(void){ m_value.bar_replacements++; }
   void BarDuplicate(void){ m_value.bar_duplicates++; }
   void GapDetected(void){ m_value.detected_gaps++; }
   void SyncCheck(void){ m_value.sync_checks++; }
   void SyncFailure(void){ m_value.sync_failures++; }
   void SpecRefresh(void){ m_value.specification_refreshes++; }
   void SourceError(void){ m_value.source_errors++; }
   void RefreshLatency(const ulong value)
   {
      m_value.last_refresh_latency_us=value;
      if(value>m_value.maximum_refresh_latency_us) m_value.maximum_refresh_latency_us=value;
   }
   SF03_MarketTelemetrySnapshot Snapshot(void) const { return m_value; }
};
#endif
