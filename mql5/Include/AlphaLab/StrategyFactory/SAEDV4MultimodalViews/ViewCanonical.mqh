#ifndef ALPHA_LAB_SAED_V4_VIEW_CANONICAL_MQH
#define ALPHA_LAB_SAED_V4_VIEW_CANONICAL_MQH
string SAEDViewCanonicalKey(const string twin_id,const int kind,const datetime known_as_of,const datetime event_as_of){ return twin_id+"|"+IntegerToString(kind)+"|"+TimeToString(known_as_of,TIME_DATE|TIME_SECONDS)+"|"+TimeToString(event_as_of,TIME_DATE|TIME_SECONDS); }
#endif
