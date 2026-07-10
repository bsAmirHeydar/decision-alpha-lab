#ifndef __EXP0018_DAYE_SESSION_BOX_IDENTITY_MQH__
#define __EXP0018_DAYE_SESSION_BOX_IDENTITY_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxTypes.mqh>

uint DAYE_SessionBoxHash32(const string value)
{
   uint hash=2166136261;
   for(int i=0;i<StringLen(value);i++)
   {
      hash^=(uint)StringGetCharacter(value,i);
      hash*=16777619;
   }
   return hash;
}

string DAYE_SessionBoxHashText(const string value)
{
   return StringFormat("%08X",DAYE_SessionBoxHash32(value));
}

string DAYE_BuildSessionBoxProjectionId(const string symbol_snapshot_id,const long chart_id)
{
   return "EXP0018|P09|BOX|"+symbol_snapshot_id+"|CHART|"+IntegerToString(chart_id);
}

string DAYE_BuildSessionBoxObjectName(const string symbol_snapshot_id)
{
   return DAYE_SESSION_BOX_OBJECT_PREFIX+DAYE_SessionBoxHashText(symbol_snapshot_id);
}

string DAYE_BuildSessionBoxEventId(const DAYE_SessionBoxEventType type,const string projection_id,
                                   const datetime event_time_utc,const string reason_code)
{
   return "EXP0018|P09|EVENT|"+IntegerToString((int)type)+"|"+projection_id+"|"+
          IntegerToString((long)event_time_utc)+"|"+DAYE_SessionBoxHashText(reason_code);
}

bool DAYE_IsOwnedSessionBoxObjectName(const string object_name)
{
   return StringFind(object_name,DAYE_SESSION_BOX_OBJECT_PREFIX)==0;
}

bool DAYE_UtcToBrokerSessionBoxTime(const datetime utc_time,const DAYE_TimeConfig &time_config,
                                    datetime &broker_time,bool &replay_safe,string &reason_code)
{
   reason_code="";
   replay_safe=true;
   int offset_minutes=0;
   if(!DAYE_ResolveBrokerOffsetMinutes(time_config,offset_minutes,replay_safe,reason_code)) return false;
   broker_time=DAYE_ShiftMinutes(utc_time,offset_minutes);
   return broker_time>0;
}

#endif
