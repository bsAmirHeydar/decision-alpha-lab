#ifndef ALPHALAB_ACL05_CANDIDATE_FREEZE_MQH
#define ALPHALAB_ACL05_CANDIDATE_FREEZE_MQH
#include "ACL05Types.mqh"
struct ACL05CandidateFreeze { string freeze_id; string freeze_digest; int research_count; int diagnostic_count; bool payloads_mutable; bool diagnostic_selectable; };
bool ACL05CandidateFreezeValid(const ACL05CandidateFreeze &x){ return StringLen(x.freeze_id)>0 && StringLen(x.freeze_digest)==71 && x.research_count>0 && x.diagnostic_count>=0 && !x.payloads_mutable && !x.diagnostic_selectable; }
#endif
