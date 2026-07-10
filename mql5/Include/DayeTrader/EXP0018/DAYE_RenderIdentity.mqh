#ifndef __EXP0018_DAYE_RENDER_IDENTITY_MQH__
#define __EXP0018_DAYE_RENDER_IDENTITY_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderTypes.mqh>

uint DAYE_RenderHash32(const string value)
{
   uint hash=2166136261;
   int length=StringLen(value);
   for(int i=0;i<length;i++)
   {
      hash ^= (uint)StringGetCharacter(value,i);
      hash *= 16777619;
   }
   return hash;
}

string DAYE_RenderHashText(const string value)
{
   return StringFormat("%08X",DAYE_RenderHash32(value));
}

string DAYE_BuildRenderProjectionId(const string use_id,const long chart_id)
{
   return "EXP0018|P08|"+use_id+"|CHART|"+IntegerToString(chart_id);
}

string DAYE_BuildRenderLineName(const string use_id)
{
   return DAYE_RENDER_OBJECT_PREFIX+"L_"+DAYE_RenderHashText(use_id);
}

string DAYE_BuildRenderTextName(const string use_id)
{
   return DAYE_RENDER_OBJECT_PREFIX+"T_"+DAYE_RenderHashText(use_id);
}

string DAYE_BuildRenderEventId(const DAYE_RenderEventType type,const string projection_id,const datetime processing_time_utc)
{
   return "EXP0018|P08|EVENT|"+IntegerToString((int)type)+"|"+projection_id+"|"+IntegerToString((long)processing_time_utc);
}

bool DAYE_IsOwnedRenderObjectName(const string object_name)
{
   return StringFind(object_name,DAYE_RENDER_OBJECT_PREFIX)==0;
}

bool DAYE_UtcToBrokerRenderTime(const datetime utc_time,const DAYE_TimeConfig &time_config,
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
