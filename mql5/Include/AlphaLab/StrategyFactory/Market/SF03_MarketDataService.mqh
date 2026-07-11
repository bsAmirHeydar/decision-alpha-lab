#ifndef __SF03_MARKET_DATA_SERVICE_MQH__
#define __SF03_MARKET_DATA_SERVICE_MQH__
#include "ISF03_MarketSource.mqh"
#include "SF03_TickCache.mqh"
#include "SF03_BarCache.mqh"
#include "SF03_MultiSymbolSync.mqh"
#include "SF03_MarketTelemetry.mqh"
#include "../Ports/ISF02_MarketDataPort.mqh"

class CSF03MarketDataService : public ISF02MarketDataPort
{
private:
   ISF03MarketSource *m_source;
   ISF02ClockPort *m_clock;
   CSF03TickCache m_ticks;
   CSF03BarCache m_bars;
   CSF03MarketTelemetry m_telemetry;
   bool m_initialized;
   bool m_started;
   long m_source_generation;
   long m_tick_max_age_msc;
   int m_series_capacity;
   ENUM_SF03_MISSING_BAR_POLICY m_missing_policy;

public:
   CSF03MarketDataService(void)
   {
      m_source=NULL;
      m_clock=NULL;
      m_initialized=false;
      m_started=false;
      m_source_generation=1;
      m_tick_max_age_msc=5000;
      m_series_capacity=4096;
      m_missing_policy=SF03_MISSING_FAIL_CLOSED;
   }
   void BindSource(ISF03MarketSource *value){ m_source=value; }
   void BindClock(ISF02ClockPort *value){ m_clock=value; }
   void Configure(const long tick_max_age_msc,const int series_capacity,
                  const ENUM_SF03_MISSING_BAR_POLICY policy)
   {
      m_tick_max_age_msc=tick_max_age_msc;
      m_series_capacity=series_capacity;
      m_missing_policy=policy;
   }

   string ServiceId(void) const { return "sf03.market_data"; }
   ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_MARKET_DATA; }

   bool Initialize(const SF02_RuntimeConfig &config,string &error)
   {
      if(CheckPointer(m_source)==POINTER_INVALID || CheckPointer(m_clock)==POINTER_INVALID)
      { error="source or clock not bound"; return false; }
      if(m_tick_max_age_msc<0 || m_series_capacity<2)
      { error="invalid market configuration"; return false; }
      m_initialized=true; error=""; return true;
   }
   bool Start(string &error)
   {
      if(!m_initialized){ error="not initialized"; return false; }
      m_started=true; error=""; return true;
   }
   void Stop(void){ m_started=false; }
   void Shutdown(void){ m_started=false; m_initialized=false; m_bars.Clear(); }

   SF02_ServiceHealth Health(const long now_utc_msc) const
   {
      SF02_ServiceHealth out;
      out.service_id=ServiceId();
      out.service_kind=ServiceKind();
      out.observed_at_utc_msc=now_utc_msc;
      out.status=(m_initialized && m_started)?SF02_HEALTH_HEALTHY:SF02_HEALTH_DEGRADED;
      out.detail=(m_initialized && m_started)?"running":"not running";
      return out;
   }

   bool EnsureSymbol(const string symbol,string &error)
   {
      return m_source.EnsureSymbol(symbol,error);
   }

   bool RegisterSeries(const string symbol,const int timeframe_seconds,string &error)
   {
      if(!EnsureSymbol(symbol,error)) return false;
      return m_bars.Ensure(symbol,timeframe_seconds,m_series_capacity,error);
   }

   bool RefreshTick(const string symbol,string &error)
   {
      const ulong started=m_clock.MonotonicMicroseconds();
      MqlTick tick;
      if(!m_source.ReadLatestTick(symbol,tick,error))
      { m_telemetry.SourceError(); return false; }
      if(!m_ticks.Put(symbol,tick,m_clock.UtcNowMilliseconds(),m_source_generation,error))
      { m_telemetry.SourceError(); return false; }
      m_telemetry.TickUpdate();
      m_telemetry.RefreshLatency(m_clock.MonotonicMicroseconds()-started);
      return true;
   }

   bool LatestTick(const string symbol,MqlTick &tick,string &error)
   {
      SF03_TickSnapshot snapshot;
      if(!m_ticks.Get(symbol,m_clock.UtcNowMilliseconds(),m_tick_max_age_msc,snapshot,error))
      {
         m_telemetry.TickMiss();
         if(!RefreshTick(symbol,error)) return false;
         if(!m_ticks.Get(symbol,m_clock.UtcNowMilliseconds(),m_tick_max_age_msc,snapshot,error)) return false;
      }
      else m_telemetry.TickHit();
      tick=snapshot.tick;
      error="";
      return true;
   }

   int RefreshSeries(const string symbol,const int timeframe_seconds,const int requested,string &error)
   {
      const ulong started=m_clock.MonotonicMicroseconds();
      if(!RegisterSeries(symbol,timeframe_seconds,error)) return 0;
      SF01_BarRecord incoming[];
      const int copied=m_source.ReadClosedBars(symbol,timeframe_seconds,requested,incoming,error);
      if(copied<=0){ m_telemetry.SourceError(); return 0; }
      m_telemetry.BarRefresh();

      for(int i=0;i<copied;i++)
      {
         const ENUM_SF03_BAR_UPDATE_RESULT result=m_bars.Upsert(incoming[i],error);
         if(result==SF03_BAR_REJECTED){ m_telemetry.SourceError(); return i; }
         if(result==SF03_BAR_INSERTED) m_telemetry.BarInserted();
         if(result==SF03_BAR_REPLACED) m_telemetry.BarReplaced();
         if(result==SF03_BAR_DUPLICATE) m_telemetry.BarDuplicate();
         if(result==SF03_BAR_GAP_INSERTED)
         { m_telemetry.BarInserted(); m_telemetry.GapDetected(); }
      }
      m_telemetry.RefreshLatency(m_clock.MonotonicMicroseconds()-started);
      error="";
      return copied;
   }

   bool LatestClosedBar(const string symbol,const int timeframe_seconds,
                        SF01_BarRecord &bar,string &error)
   {
      if(!m_bars.Latest(symbol,timeframe_seconds,bar,error))
      {
         if(RefreshSeries(symbol,timeframe_seconds,3,error)<=0) return false;
         if(!m_bars.Latest(symbol,timeframe_seconds,bar,error)) return false;
      }
      if(m_clock.UtcNowMilliseconds()-bar.close_time.utc_epoch_milliseconds<0)
      { error="bar close in future"; return false; }
      if(m_bars.HasGap(symbol,timeframe_seconds) && m_missing_policy==SF03_MISSING_FAIL_CLOSED)
      { error="series contains gap"; return false; }
      error="";
      return true;
   }

   bool IsSynchronized(const string symbol,const int timeframe_seconds) const
   {
      SF01_BarRecord bar;
      string error="";
      return m_bars.Latest(symbol,timeframe_seconds,bar,error) &&
             !m_bars.HasGap(symbol,timeframe_seconds);
   }

   int CopyRecentClosedBars(const string symbol,const int timeframe_seconds,
                            const int requested,SF01_BarRecord &out[]) const
   {
      return m_bars.CopyRecent(symbol,timeframe_seconds,requested,out);
   }

   bool EvaluateSynchronization(const SF03_SyncRequirement &requirements[],
                                SF03_SyncResult &result,string &error)
   {
      CSF03MultiSymbolSynchronizer sync;
      for(int i=0;i<ArraySize(requirements);i++)
         if(!sync.AddRequirement(requirements[i],error)) return false;
      m_telemetry.SyncCheck();
      const bool ready=sync.Evaluate(m_bars,m_clock.UtcNowMilliseconds(),result);
      if(!ready) m_telemetry.SyncFailure();
      error=ready?"":result.detail;
      return ready;
   }

   long SeriesGeneration(const string symbol,const int timeframe_seconds) const
   { return m_bars.Generation(symbol,timeframe_seconds); }

   SF03_MarketTelemetrySnapshot Telemetry(void) const { return m_telemetry.Snapshot(); }
};
#endif
