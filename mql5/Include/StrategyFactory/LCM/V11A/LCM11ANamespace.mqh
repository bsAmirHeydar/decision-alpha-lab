#ifndef ALPHA_LAB_LCM11A_NAMESPACE_MQH
#define ALPHA_LAB_LCM11A_NAMESPACE_MQH
#include "LCM11AVisualTypes.mqh"
string LCM11A_SanitizeToken(string value){StringReplace(value,"::","_");StringReplace(value," ","_");StringReplace(value,"/","_");StringReplace(value,"\\","_");return value;}
string LCM11A_ObjectId(const SLCM11A_VisualIdentity &id,const string visual_token){return "ALV1::"+LCM11A_SanitizeToken(id.owner)+"::"+LCM11A_SanitizeToken(id.subsystem)+"::"+LCM11A_SanitizeToken(id.instance_id)+"::"+(string)id.chart_id+"::"+LCM11A_SanitizeToken(id.symbol)+"::"+(string)id.timeframe+"::"+LCM11A_SanitizeToken(id.event_id)+"::"+LCM11A_SanitizeToken(id.role)+"::"+LCM11A_SanitizeToken(visual_token);}
string LCM11A_CleanupPrefix(const SLCM11A_VisualIdentity &id){return "ALV1::"+LCM11A_SanitizeToken(id.owner)+"::"+LCM11A_SanitizeToken(id.subsystem)+"::"+LCM11A_SanitizeToken(id.instance_id)+"::"+(string)id.chart_id+"::";}
#endif
