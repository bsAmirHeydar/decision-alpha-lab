#ifndef FP_SAEDV430INDEPENDENCE_MQH
#define FP_SAEDV430INDEPENDENCE_MQH
#include "FP_SAEDV430Lab.mqh"
bool FP_SAEDV430LabsIndependent(const FP_SAEDV430Lab &left,const FP_SAEDV430Lab &right) { return(left.organization_id!=right.organization_id && left.operator_id!=right.operator_id && left.signing_key_id!=right.signing_key_id && left.environment_id!=right.environment_id && left.infrastructure_id!=right.infrastructure_id && left.mutable_state_group!=right.mutable_state_group); }
#endif
