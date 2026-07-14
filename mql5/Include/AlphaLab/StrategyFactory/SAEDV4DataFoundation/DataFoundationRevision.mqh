#ifndef __AL_SAED_V4_DATA_FOUNDATION_REVISION_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_REVISION_MQH__
#include "DataFoundationContracts.mqh"
#include "DataFoundationTemporal.mqh"
class ALRevisionGate {
public:
 static bool ValidateFirst(const ALRevisionIdentity &value,string &reason){
   if(value.revision_number!=1 || value.supersedes_revision_id!=""){reason="invalid_first_revision";return false;}
   return ALDataTemporalGate::Validate(value.temporal,reason);
 }
 static bool ValidateNext(const ALRevisionIdentity &head,const ALRevisionIdentity &next,string &reason){
   if(head.entity_id!=next.entity_id){reason="entity_mismatch";return false;}
   if(next.revision_number!=head.revision_number+1){reason="revision_gap";return false;}
   if(next.supersedes_revision_id!=head.revision_id){reason="supersedes_mismatch";return false;}
   if(next.temporal.known_time<head.temporal.known_time){reason="known_time_regression";return false;}
   return ALDataTemporalGate::Validate(next.temporal,reason);
 }
};
#endif
