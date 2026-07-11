#ifndef __SF03_TIME_KERNEL_MQH__
#define __SF03_TIME_KERNEL_MQH__
#include "SF03_MarketTypes.mqh"
#include "SF03_TimeMath.mqh"
#include "../Ports/ISF02_ClockPort.mqh"

class CSF03TimeKernel : public ISF02ClockPort
{
private:
   SF03_ClockConfig m_config;
   bool m_initialized;
   bool m_started;
   long m_fixture_utc_msc;

   int InferBrokerOffsetMinutes(void) const
   {
      const datetime server_now=TimeTradeServer();
      const datetime gmt_now=TimeGMT();
      if(server_now<=0 || gmt_now<=0) return m_config.broker_utc_offset_minutes;
      return (int)MathRound(((double)((long)server_now-(long)gmt_now))/60.0);
   }

public:
   CSF03TimeKernel(void)
   {
      m_config.mode=SF03_CLOCK_GMT_NATIVE;
      m_config.broker_utc_offset_minutes=0;
      m_config.broker_timezone_id="broker";
      m_config.source_clock_id="sf03_time_kernel";
      m_config.strict_offset_validation=true;
      m_initialized=false;
      m_started=false;
      m_fixture_utc_msc=0;
   }

   void Configure(const SF03_ClockConfig &value){ m_config=value; }
   void SetFixtureUtcMilliseconds(const long value){ m_fixture_utc_msc=value; }

   string ServiceId(void) const { return "sf03.time_kernel"; }
   ENUM_SF02_SERVICE_KIND ServiceKind(void) const { return SF02_SERVICE_CLOCK; }

   bool Initialize(const SF02_RuntimeConfig &config,string &error)
   {
      if(m_config.broker_utc_offset_minutes<-840 || m_config.broker_utc_offset_minutes>840)
      { error="broker UTC offset out of range"; return false; }
      if(!SF01_IsSafeIdentifier(m_config.broker_timezone_id,96) ||
         !SF01_IsSafeIdentifier(m_config.source_clock_id,96))
      { error="invalid clock identifier"; return false; }
      if(m_config.mode==SF03_CLOCK_SERVER_INFERRED_OFFSET)
         m_config.broker_utc_offset_minutes=InferBrokerOffsetMinutes();
      m_initialized=true;
      error="";
      return true;
   }

   bool Start(string &error)
   {
      if(!m_initialized){ error="time kernel not initialized"; return false; }
      m_started=true; error=""; return true;
   }
   void Stop(void){ m_started=false; }
   void Shutdown(void){ m_started=false; m_initialized=false; }

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

   long UtcNowMilliseconds(void) const
   {
      if(m_config.mode==SF03_CLOCK_FIXTURE) return m_fixture_utc_msc;
      if(m_config.mode==SF03_CLOCK_GMT_NATIVE) return SF03_SecondsToMilliseconds(TimeGMT());
      return SF03_SecondsToMilliseconds(TimeTradeServer())-
             ((long)m_config.broker_utc_offset_minutes*60L*1000L);
   }

   ulong MonotonicMicroseconds(void) const { return GetMicrosecondCount(); }

   SF01_MarketTimestamp Now(const string source_clock_id="runtime") const
   {
      const string id=(source_clock_id=="runtime")?m_config.source_clock_id:source_clock_id;
      return SF01_MakeUtcMilliseconds(UtcNowMilliseconds(),"UTC",0,id,SF01_TIME_MILLISECONDS);
   }

   int BrokerUtcOffsetMinutes(void) const { return m_config.broker_utc_offset_minutes; }

   long ServerSecondsToUtcMilliseconds(const datetime server_time) const
   {
      return SF03_SecondsToMilliseconds(server_time)-
             ((long)m_config.broker_utc_offset_minutes*60L*1000L);
   }

   long NewYorkDstStartUtcMilliseconds(const int year) const
   {
      const int day=SF03_NthWeekdayOfMonth(year,3,0,2);
      return SF03_MakeUtcMilliseconds(year,3,day,7,0,0);
   }
   long NewYorkDstEndUtcMilliseconds(const int year) const
   {
      const int day=SF03_NthWeekdayOfMonth(year,11,0,1);
      return SF03_MakeUtcMilliseconds(year,11,day,6,0,0);
   }
   bool IsNewYorkDst(const long utc_msc) const
   {
      MqlDateTime parts;
      SF03_UtcParts(utc_msc,parts);
      return utc_msc>=NewYorkDstStartUtcMilliseconds(parts.year) &&
             utc_msc<NewYorkDstEndUtcMilliseconds(parts.year);
   }
   int NewYorkUtcOffsetMinutes(const long utc_msc) const
   {
      return IsNewYorkDst(utc_msc)?-240:-300;
   }
   int ResolveOffsetMinutes(const ENUM_SF03_TIMEZONE_KIND kind,
                            const long utc_msc,
                            const int fixed_offset_minutes=0) const
   {
      if(kind==SF03_TZ_UTC) return 0;
      if(kind==SF03_TZ_BROKER) return BrokerUtcOffsetMinutes();
      if(kind==SF03_TZ_NEW_YORK) return NewYorkUtcOffsetMinutes(utc_msc);
      return fixed_offset_minutes;
   }
   int TradingDayId(const long utc_msc,
                    const ENUM_SF03_TIMEZONE_KIND kind,
                    const int rollover_minute,
                    const int fixed_offset_minutes=0) const
   {
      const int offset=ResolveOffsetMinutes(kind,utc_msc,fixed_offset_minutes);
      const long shifted=SF03_ShiftMilliseconds(utc_msc,offset)-
                         ((long)SF03_NormalizeMinuteOfDay(rollover_minute)*60L*1000L);
      MqlDateTime parts;
      SF03_UtcParts(shifted,parts);
      return SF03_DateId(parts);
   }
};
#endif
