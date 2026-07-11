#ifndef __SF20_EXP0017_DIFFERENTIAL_LEDGER_MQH__
#define __SF20_EXP0017_DIFFERENTIAL_LEDGER_MQH__
#include "SF20_EXP0017Mapper.mqh"
class CSF20EXP0017DifferentialLedger
{
private:SF20_EXP0017MappingRecord m_mappings[];SF20_EXP0017DifferentialRecord m_records[];int m_capacity;
public:CSF20EXP0017DifferentialLedger(){m_capacity=8192;}bool Configure(const int capacity,string &error){if(capacity<1||capacity>100000){error="invalid differential capacity";return false;}m_capacity=capacity;ArrayResize(m_mappings,0);ArrayResize(m_records,0);error="";return true;}
 bool AppendMapping(const SF20_EXP0017MappingRecord &mapping,string &error){if(ArraySize(m_mappings)>=m_capacity){error="mapping ledger capacity";return false;}int n=ArraySize(m_mappings);ArrayResize(m_mappings,n+1);m_mappings[n]=mapping;error="";return true;}
 bool AppendMatch(const SCGDDivergenceCandidate &legacy,const SF01_AnatomyEvent &event,const long known,string &error){if(ArraySize(m_records)>=m_capacity){error="differential ledger capacity";return false;}SF20_EXP0017DifferentialRecord r;r.legacy_divergence_id=legacy.divergence_id;r.canonical_event_id=event.event_id;r.legacy_payload_hash=SF01_StableId("sf20lp",SF20_LegacyCandidatePayload(legacy));r.canonical_payload_hash=SF01_StableId("sf20cp",SF01_AnatomyEventCanonicalIdentity(event));r.status=SF20_DIFF_MATCH;r.mismatched_fields="";r.known_time_utc_msc=known;r.record_id=SF01_StableId("sf20diff",legacy.divergence_id+"|"+event.event_id+"|match|"+IntegerToString(known));int n=ArraySize(m_records);ArrayResize(m_records,n+1);m_records[n]=r;error="";return true;}
 int MappingCount()const{return ArraySize(m_mappings);}int RecordCount()const{return ArraySize(m_records);}
};
#endif
