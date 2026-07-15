#ifndef ALPHALAB_OPERATIONS_TARGET_BINDING_MQH
#define ALPHALAB_OPERATIONS_TARGET_BINDING_MQH
#include "OperationsHashGuard.mqh"
struct ALOperationsTargetBinding { string target_hash; string environment_hash; string broker_server_hash; string account_hash; string symbol_name; string terminal_instance_id; };
bool ALOpsTargetBindingValid(const ALOperationsTargetBinding &value){ return ALOpsIsSha256(value.target_hash) && ALOpsIsSha256(value.environment_hash) && ALOpsIsSha256(value.broker_server_hash) && ALOpsIsSha256(value.account_hash) && StringLen(value.symbol_name)>0 && StringLen(value.terminal_instance_id)>0; }
#endif
