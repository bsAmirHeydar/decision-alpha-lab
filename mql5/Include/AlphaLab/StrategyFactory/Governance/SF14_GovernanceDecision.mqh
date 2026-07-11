#ifndef __SF14_GOVERNANCE_DECISION_MQH__
#define __SF14_GOVERNANCE_DECISION_MQH__
#include "SF14_RegistryEntry.mqh"
struct SF14_GovernanceDecision{int sequence;ENUM_SF14_DECISION_TYPE decision_type;string entry_id;string scope_id;ENUM_SF14_REGISTRY_STATE from_state;ENUM_SF14_REGISTRY_STATE to_state;string actor_id;string reason_code;string evidence_hash;string previous_decision_hash;long decided_at_utc_msc;string decision_id;string decision_hash;};
string SF14_GovernanceDecisionIdentity(const SF14_GovernanceDecision &v){return IntegerToString(v.sequence)+"|"+IntegerToString((int)v.decision_type)+"|"+v.entry_id+"|"+v.scope_id+"|"+IntegerToString((int)v.from_state)+"|"+IntegerToString((int)v.to_state)+"|"+IntegerToString(v.decided_at_utc_msc);}
string SF14_DeriveDecisionId(const SF14_GovernanceDecision &v){return SF01_StableId("gdec",SF14_GovernanceDecisionIdentity(v));}
string SF14_DeriveDecisionHash(const SF14_GovernanceDecision &v){return SF01_StableId("gdech","alpha_lab.strategy_factory/governance_decision@1.0.0|"+v.decision_id+"|"+SF14_GovernanceDecisionIdentity(v)+"|"+v.actor_id+"|"+v.reason_code+"|"+v.evidence_hash+"|"+v.previous_decision_hash);}
#endif
