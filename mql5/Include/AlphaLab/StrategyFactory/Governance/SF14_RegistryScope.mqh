#ifndef __SF14_REGISTRY_SCOPE_MQH__
#define __SF14_REGISTRY_SCOPE_MQH__
#include "../Contracts/SF01_Hash.mqh"
struct SF14_RegistryScope{string strategy_id;string anatomy_plugin_id;string anatomy_plugin_version;string symbol_universe_id;string timeframe_profile_id;string deployment_profile_id;string feature_schema_hash;string label_contract_hash;string scope_id;};
string SF14_RegistryScopeCanonical(const SF14_RegistryScope &v){return "alpha_lab.strategy_factory/registry_scope@1.0.0|"+v.strategy_id+"|"+v.anatomy_plugin_id+"|"+v.anatomy_plugin_version+"|"+v.symbol_universe_id+"|"+v.timeframe_profile_id+"|"+v.deployment_profile_id+"|"+v.feature_schema_hash+"|"+v.label_contract_hash;}
string SF14_DeriveScopeId(const SF14_RegistryScope &v){return SF01_StableId("scope",SF14_RegistryScopeCanonical(v));}
bool SF14_ValidateRegistryScope(const SF14_RegistryScope &v,string &error){if(v.strategy_id==""||v.anatomy_plugin_id==""||v.anatomy_plugin_version==""||v.symbol_universe_id==""||v.timeframe_profile_id==""||v.deployment_profile_id==""||v.feature_schema_hash==""||v.label_contract_hash==""){error="missing registry scope identity";return false;}if(v.scope_id!=""&&v.scope_id!=SF14_DeriveScopeId(v)){error="registry scope identity mismatch";return false;}error="";return true;}
#endif
