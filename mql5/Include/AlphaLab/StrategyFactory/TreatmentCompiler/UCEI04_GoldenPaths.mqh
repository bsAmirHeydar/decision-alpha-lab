#ifndef __UCEI04_GOLDEN_PATHS_MQH__
#define __UCEI04_GOLDEN_PATHS_MQH__
#include "UCEI04_Manual.mqh"
void UCEI04_MakeEvent(const int seq,const ENUM_UCEI04_EVENT_TYPE type,const long tm,const double price,const double qty,UCEI04_PathEvent &e){e.sequence=seq;e.event_type=type;e.event_time_ms=tm;e.known_time_ms=tm;e.has_price=price>0.0;e.price=price;e.quantity_fraction=qty;e.source="golden";e.reason=UCEI04_EventTypeName(type);e.metadata_json="{}";UCEI04_SealPathEvent(e);}
bool UCEI04_ReplayTargetPath(const UCEI04_CompiledTreatment &t,UCEI04_PathSnapshot &final,string &error){CUCEI04PathStateMachine sm;UCEI04_PathSnapshot s,n;sm.Initial(t,s);double p=t.entry.legs[0].trigger_price;UCEI04_PathEvent e;UCEI04_MakeEvent(1,UCEI04_SUBMIT,t.decision_time_ms,0.0,0.0,e);if(!sm.Apply(s,e,n,error))return false;s=n;UCEI04_MakeEvent(2,UCEI04_FILL,t.decision_time_ms+1,p,1.0,e);if(!sm.Apply(s,e,n,error))return false;s=n;UCEI04_MakeEvent(3,UCEI04_TARGET_HIT,t.decision_time_ms+2,p+1.0,1.0,e);if(!sm.Apply(s,e,n,error))return false;s=n;UCEI04_MakeEvent(4,UCEI04_CLOSE,t.decision_time_ms+3,p+1.0,0.0,e);if(!sm.Apply(s,e,n,error))return false;final=n;error="";return true;}
#endif
