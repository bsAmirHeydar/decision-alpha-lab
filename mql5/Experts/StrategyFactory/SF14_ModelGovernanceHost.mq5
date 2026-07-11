#property strict
#include <AlphaLab/StrategyFactory/Governance/SF14_AllGovernance.mqh>
input string InpRegistryVersion="1.0.0";
CSF14ModelRegistry g_registry;
int OnInit(){Print("SF14 Model Governance Host ready registry_version=",InpRegistryVersion," capital_authority=false");return INIT_SUCCEEDED;}
void OnTick(){}
void OnDeinit(const int reason){Print("SF14 Model Governance Host stopped entries=",g_registry.EntryCount()," decisions=",g_registry.DecisionCount()," reason=",reason);}
