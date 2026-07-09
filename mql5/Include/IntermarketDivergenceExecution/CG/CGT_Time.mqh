#ifndef __CGT_TIME_MQH__
#define __CGT_TIME_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Types.mqh>

class CCGT_TimeAnatomy
{
private:
   SCGTTimeConfig m_config;

   datetime MakeDateTime(const int year,const int mon,const int day,const int hour,const int min,const int sec)
   {
      MqlDateTime dt;
      dt.year=year;
      dt.mon=mon;
      dt.day=day;
      dt.hour=hour;
      dt.min=min;
      dt.sec=sec;
      return StructToTime(dt);
   }

   int NthWeekdayOfMonth(const int year,const int month,const int weekday,const int nth)
   {
      datetime first=MakeDateTime(year,month,1,0,0,0);
      MqlDateTime f;
      TimeToStruct(first,f);
      int diff=(weekday-f.day_of_week+7)%7;
      return 1+diff+7*(nth-1);
   }

   int NewYorkOffsetFromUtc(const datetime utc_now)
   {
      if(!m_config.use_auto_new_york_dst)
         return m_config.manual_new_york_utc_offset_hours;

      MqlDateTime u;
      TimeToStruct(utc_now,u);
      int year=u.year;

      int march_second_sunday=NthWeekdayOfMonth(year,3,0,2);
      int november_first_sunday=NthWeekdayOfMonth(year,11,0,1);

      // US Eastern daylight time: from second Sunday in March at 07:00 UTC
      // until first Sunday in November at 06:00 UTC.
      datetime dst_start_utc=MakeDateTime(year,3,march_second_sunday,7,0,0);
      datetime dst_end_utc=MakeDateTime(year,11,november_first_sunday,6,0,0);

      if(utc_now>=dst_start_utc && utc_now<dst_end_utc)
         return -4;
      return -5;
   }

   string TradingDayLabelFromStart(const datetime trading_day_start_ny)
   {
      MqlDateTime d;
      TimeToStruct(trading_day_start_ny,d);
      return StringFormat("%04d-%02d-%02d",d.year,d.mon,d.day);
   }

public:
   void Configure(SCGTTimeConfig &config)
   {
      m_config=config;
      if(m_config.max_previous_cycles_shown<0)
         m_config.max_previous_cycles_shown=0;
   }

   datetime BrokerToUtc(const datetime broker_time)
   {
      return broker_time - (m_config.broker_utc_offset_hours*3600);
   }

   datetime UtcToNewYork(const datetime utc_time,const int ny_offset_hours)
   {
      return utc_time + (ny_offset_hours*3600);
   }

   bool BuildTimeSnapshot(const datetime broker_now,SCGTTimeSnapshot &snapshot)
   {
      snapshot.broker_now=broker_now;
      snapshot.utc_now=BrokerToUtc(broker_now);
      snapshot.new_york_utc_offset_hours=NewYorkOffsetFromUtc(snapshot.utc_now);
      snapshot.new_york_now=UtcToNewYork(snapshot.utc_now,snapshot.new_york_utc_offset_hours);

      MqlDateTime ny;
      TimeToStruct(snapshot.new_york_now,ny);

      MqlDateTime start=ny;
      start.hour=CGT_TRADING_DAY_START_HOUR_NY;
      start.min=0;
      start.sec=0;

      datetime start_candidate=StructToTime(start);
      if(ny.hour<CGT_TRADING_DAY_START_HOUR_NY)
         start_candidate-=86400;

      snapshot.trading_day_start_ny=start_candidate;
      snapshot.trading_day_end_ny=start_candidate+(CGT_TRADING_DAY_MINUTES*60);
      snapshot.inside_trading_day=(snapshot.new_york_now>=snapshot.trading_day_start_ny && snapshot.new_york_now<snapshot.trading_day_end_ny);
      snapshot.trading_day_label=TradingDayLabelFromStart(snapshot.trading_day_start_ny);

      if(snapshot.inside_trading_day)
      {
         snapshot.elapsed_minutes_from_day_start=(int)((snapshot.new_york_now-snapshot.trading_day_start_ny)/60);
         snapshot.remaining_minutes_to_day_end=CGT_TRADING_DAY_MINUTES-snapshot.elapsed_minutes_from_day_start;
      }
      else
      {
         snapshot.elapsed_minutes_from_day_start=-1;
         snapshot.remaining_minutes_to_day_end=0;
      }
      return true;
   }

   int TotalCycleCount(const int group_minutes)
   {
      if(group_minutes<=0)
         return 0;
      int full=CGT_TRADING_DAY_MINUTES/group_minutes;
      if((CGT_TRADING_DAY_MINUTES%group_minutes)!=0)
         full++;
      return full;
   }

   bool BuildCycleSnapshot(SCGTTimeSnapshot &time_snapshot,SCGTGroupDef &group,SCGTCycleSnapshot &cycle)
   {
      cycle.group_name=group.name;
      cycle.group_minutes=group.minutes;
      cycle.enabled=group.enabled;
      cycle.inside_trading_day=time_snapshot.inside_trading_day;
      cycle.total_cycle_count=TotalCycleCount(group.minutes);

      cycle.current_cycle_index=-1;
      cycle.current_cycle_number=0;
      cycle.previous_cycle_count=0;
      cycle.cycle_start_minute=-1;
      cycle.cycle_end_minute=-1;
      cycle.cycle_start_ny=0;
      cycle.cycle_end_ny=0;
      cycle.minutes_elapsed_in_cycle=0;
      cycle.minutes_remaining_in_cycle=0;
      cycle.is_last_cycle_of_day=false;
      cycle.is_partial_last_cycle=false;

      if(!group.enabled || !time_snapshot.inside_trading_day || group.minutes<=0)
         return false;

      int elapsed=time_snapshot.elapsed_minutes_from_day_start;
      int idx=elapsed/group.minutes;
      int start_minute=idx*group.minutes;
      int end_minute=start_minute+group.minutes;
      if(end_minute>CGT_TRADING_DAY_MINUTES)
         end_minute=CGT_TRADING_DAY_MINUTES;

      cycle.current_cycle_index=idx;
      cycle.current_cycle_number=idx+1;
      cycle.previous_cycle_count=idx;
      cycle.cycle_start_minute=start_minute;
      cycle.cycle_end_minute=end_minute;
      cycle.cycle_start_ny=time_snapshot.trading_day_start_ny+(start_minute*60);
      cycle.cycle_end_ny=time_snapshot.trading_day_start_ny+(end_minute*60);
      cycle.minutes_elapsed_in_cycle=elapsed-start_minute;
      cycle.minutes_remaining_in_cycle=end_minute-elapsed;
      cycle.is_last_cycle_of_day=(idx==(cycle.total_cycle_count-1));
      cycle.is_partial_last_cycle=((CGT_TRADING_DAY_MINUTES%group.minutes)!=0 && cycle.is_last_cycle_of_day);
      return true;
   }

   string FormatNY(const datetime t)
   {
      if(t<=0)
         return "-";
      return TimeToString(t,TIME_DATE|TIME_MINUTES);
   }

   string FormatNYTimeOnly(const datetime t)
   {
      if(t<=0)
         return "-";
      return TimeToString(t,TIME_MINUTES);
   }

   string FormatMinuteRange(const int start_minute,const int end_minute_exclusive)
   {
      if(start_minute<0 || end_minute_exclusive<0)
         return "-";
      int s_h=(CGT_TRADING_DAY_START_HOUR_NY+(start_minute/60))%24;
      int s_m=start_minute%60;
      int end_inclusive=end_minute_exclusive-1;
      if(end_inclusive<start_minute)
         end_inclusive=start_minute;
      int e_h=(CGT_TRADING_DAY_START_HOUR_NY+(end_inclusive/60))%24;
      int e_m=end_inclusive%60;
      return StringFormat("%02d:%02d-%02d:%02d NY",s_h,s_m,e_h,e_m);
   }

   int MaxPreviousCyclesShown()
   {
      return m_config.max_previous_cycles_shown;
   }
};

#endif
