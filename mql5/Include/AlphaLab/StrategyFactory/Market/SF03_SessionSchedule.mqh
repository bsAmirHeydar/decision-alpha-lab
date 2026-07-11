#ifndef __SF03_SESSION_SCHEDULE_MQH__
#define __SF03_SESSION_SCHEDULE_MQH__
#include "SF03_TimeKernel.mqh"

class CSF03SessionSchedule
{
private:
   SF03_SessionDefinition m_items[];
   bool MinuteMatches(const int minute,const int start_minute,const int end_minute) const
   {
      if(start_minute==end_minute) return true;
      if(start_minute<end_minute) return minute>=start_minute && minute<end_minute;
      return minute>=start_minute || minute<end_minute;
   }
public:
   int Count(void) const { return ArraySize(m_items); }

   bool Add(const SF03_SessionDefinition &value,string &error)
   {
      if(!SF01_IsSafeIdentifier(value.session_id,64)){ error="invalid session id"; return false; }
      if(value.start_minute_of_day<0 || value.start_minute_of_day>=1440 ||
         value.end_minute_of_day<0 || value.end_minute_of_day>=1440)
      { error="session minute out of range"; return false; }
      if(value.weekday_mask<0 || value.weekday_mask>127)
      { error="weekday mask out of range"; return false; }
      for(int i=0;i<ArraySize(m_items);i++)
         if(m_items[i].session_id==value.session_id)
         { error="duplicate session id"; return false; }
      const int n=ArraySize(m_items);
      ArrayResize(m_items,n+1);
      m_items[n]=value;
      error="";
      return true;
   }

   bool Resolve(const long utc_msc,const CSF03TimeKernel &clock,SF03_SessionMatch &match) const
   {
      match.matched=false;
      match.session_id="";
      match.local_minute_of_day=-1;
      match.local_weekday=-1;
      match.utc_offset_minutes=0;
      for(int i=0;i<ArraySize(m_items);i++)
      {
         const SF03_SessionDefinition item=m_items[i];
         if(!item.enabled) continue;
         const int offset=clock.ResolveOffsetMinutes(item.timezone_kind,utc_msc,item.fixed_offset_minutes);
         MqlDateTime parts;
         SF03_UtcParts(SF03_ShiftMilliseconds(utc_msc,offset),parts);
         const int bit=1<<parts.day_of_week;
         if((item.weekday_mask & bit)==0) continue;
         const int minute=parts.hour*60+parts.min;
         if(!MinuteMatches(minute,item.start_minute_of_day,item.end_minute_of_day)) continue;
         match.matched=true;
         match.session_id=item.session_id;
         match.local_minute_of_day=minute;
         match.local_weekday=parts.day_of_week;
         match.utc_offset_minutes=offset;
         return true;
      }
      return false;
   }
};

SF03_SessionDefinition SF03_MakeSession(const string id,
                                        const ENUM_SF03_TIMEZONE_KIND kind,
                                        const int start_minute,
                                        const int end_minute,
                                        const int weekday_mask=62,
                                        const int fixed_offset_minutes=0)
{
   SF03_SessionDefinition out;
   out.session_id=id;
   out.enabled=true;
   out.timezone_kind=kind;
   out.fixed_offset_minutes=fixed_offset_minutes;
   out.start_minute_of_day=start_minute;
   out.end_minute_of_day=end_minute;
   out.weekday_mask=weekday_mask;
   return out;
}
#endif
