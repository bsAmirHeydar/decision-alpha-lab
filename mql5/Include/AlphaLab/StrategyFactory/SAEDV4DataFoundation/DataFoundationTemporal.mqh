#ifndef __AL_SAED_V4_DATA_FOUNDATION_TEMPORAL_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_TEMPORAL_MQH__
#include "DataFoundationContracts.mqh"
class ALDataTemporalGate {
public:
 static bool Validate(const ALBitemporalStamp &stamp,string &reason){
   if(stamp.event_time<=0 || stamp.known_time<=0){reason="time_missing";return false;}
   if(stamp.known_time<stamp.event_time){reason="known_before_event";return false;}
   if(stamp.has_valid_to && stamp.valid_to<=stamp.event_time){reason="invalid_valid_to";return false;}
   reason="pass";return true;
 }
 static bool VisibleAsOf(const ALBitemporalStamp &stamp,const datetime known_as_of,const datetime event_as_of,const bool use_event_as_of){
   if(stamp.known_time>known_as_of)return false;
   if(!use_event_as_of)return true;
   if(stamp.event_time>event_as_of)return false;
   if(stamp.has_valid_to && event_as_of>=stamp.valid_to)return false;
   return true;
 }
};
#endif
