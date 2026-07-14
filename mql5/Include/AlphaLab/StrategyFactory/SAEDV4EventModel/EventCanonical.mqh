#ifndef ALPHA_LAB_SAED_V4_EVENT_CANONICAL
#define ALPHA_LAB_SAED_V4_EVENT_CANONICAL
string SAED_EventCanonicalKey(const string stream_id,const long seq,const datetime event_time,const datetime known_time){return stream_id+"|"+IntegerToString(seq)+"|"+TimeToString(event_time,TIME_DATE|TIME_SECONDS)+"|"+TimeToString(known_time,TIME_DATE|TIME_SECONDS);}
#endif
