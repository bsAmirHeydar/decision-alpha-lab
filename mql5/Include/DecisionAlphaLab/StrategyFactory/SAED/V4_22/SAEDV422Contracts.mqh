#ifndef SAEDV422_CONTRACTS_MQH
#define SAEDV422_CONTRACTS_MQH
bool SAEDV422ClosedContract(const bool deterministic,const bool research_only,const bool runtime_executable){return deterministic && research_only && !runtime_executable;}
#endif
