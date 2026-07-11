#ifndef __SF03_TIME_MATH_MQH__
#define __SF03_TIME_MATH_MQH__
long SF03_SecondsToMilliseconds(const datetime value){ return ((long)value)*1000L; }
datetime SF03_MillisecondsToSeconds(const long value){ return (datetime)(value/1000L); }
int SF03_NormalizeMinuteOfDay(const int value)
{
   int out=value%1440;
   if(out<0) out+=1440;
   return out;
}
int SF03_NthWeekdayOfMonth(const int year,const int month,const int weekday,const int occurrence)
{
   MqlDateTime dt;
   ZeroMemory(dt);
   dt.year=year; dt.mon=month; dt.day=1;
   MqlDateTime first_parts;
   TimeToStruct(StructToTime(dt),first_parts);
   int delta=weekday-first_parts.day_of_week;
   if(delta<0) delta+=7;
   return 1+delta+((occurrence-1)*7);
}
long SF03_MakeUtcMilliseconds(const int year,const int month,const int day,
                              const int hour,const int minute,const int second=0)
{
   MqlDateTime dt;
   ZeroMemory(dt);
   dt.year=year; dt.mon=month; dt.day=day;
   dt.hour=hour; dt.min=minute; dt.sec=second;
   return SF03_SecondsToMilliseconds(StructToTime(dt));
}
void SF03_UtcParts(const long utc_msc,MqlDateTime &parts)
{
   TimeToStruct(SF03_MillisecondsToSeconds(utc_msc),parts);
}
long SF03_ShiftMilliseconds(const long utc_msc,const int offset_minutes)
{
   return utc_msc+((long)offset_minutes*60L*1000L);
}
int SF03_DateId(const MqlDateTime &parts)
{
   return parts.year*10000+parts.mon*100+parts.day;
}
#endif
