#ifndef DECISION_ALPHA_LAB_SAED_V4_14_REGISTRY_CONTRACT_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_REGISTRY_CONTRACT_MQH
bool SAEDV414RegistryAdmissible(const bool immutable_registry,const bool runtime_authority,const int entry_count){return immutable_registry && !runtime_authority && entry_count>0;}
#endif
