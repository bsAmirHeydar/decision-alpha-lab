#ifndef __LCM11B_OBJECT_REGISTRY_MQH__
#define __LCM11B_OBJECT_REGISTRY_MQH__
string LCM11BSanitize(const string value)
  {
   string out=value;
   StringReplace(out," ","_");StringReplace(out,"/","_");StringReplace(out,"\\","_");StringReplace(out,":","_");
   return out;
  }
string LCM11BObjectId(const string owner,const string subsystem,const string instance_id,const long chart_id,const string symbol,const ENUM_TIMEFRAMES timeframe,const string event_id,const string role,const string visual_token)
  {
   return "ALV1::"+LCM11BSanitize(owner)+"::"+LCM11BSanitize(subsystem)+"::"+LCM11BSanitize(instance_id)+"::"+IntegerToString(chart_id)+"::"+LCM11BSanitize(symbol)+"::"+IntegerToString((int)timeframe)+"::"+LCM11BSanitize(event_id)+"::"+LCM11BSanitize(role)+"::"+LCM11BSanitize(visual_token);
  }
string LCM11BCleanupPrefix(const string owner,const string subsystem,const string instance_id,const long chart_id)
  {
   return "ALV1::"+LCM11BSanitize(owner)+"::"+LCM11BSanitize(subsystem)+"::"+LCM11BSanitize(instance_id)+"::"+IntegerToString(chart_id)+"::";
  }
int LCM11BDeleteOwned(const long chart_id,const string prefix)
  {
   int deleted=0;
   for(int i=ObjectsTotal(chart_id)-1;i>=0;i--)
     {
      string name=ObjectName(chart_id,i);
      if(StringFind(name,prefix)==0 && ObjectDelete(chart_id,name))deleted++;
     }
   return deleted;
  }
#endif
