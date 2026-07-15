#ifndef ALPHALAB_OPERATIONS_RELEASE_BINDING_MQH
#define ALPHALAB_OPERATIONS_RELEASE_BINDING_MQH
#include "OperationsEnums.mqh"
#include "OperationsHashGuard.mqh"
struct ALOperationsReleaseBinding { string release_manifest_hash; string qualification_report_hash; string environment_hash; string generation_hash; string rollback_generation_hash; ALOperationsStage maximum_stage; bool authority_order; bool authority_broker; double maximum_risk_units; long expires_at_ms; };
bool ALOpsReleaseBindingValid(const ALOperationsReleaseBinding &value,const long now_ms){ if(!ALOpsIsSha256(value.release_manifest_hash)||!ALOpsIsSha256(value.qualification_report_hash)||!ALOpsIsSha256(value.environment_hash)||!ALOpsIsSha256(value.generation_hash)||!ALOpsIsSha256(value.rollback_generation_hash)) return false; if(now_ms>=value.expires_at_ms||value.maximum_risk_units<0.0) return false; if((value.authority_order||value.authority_broker) && value.maximum_stage<AL_OPS_MICRO_LIVE) return false; return true; }
#endif
