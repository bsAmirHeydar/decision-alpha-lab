#ifndef __SF14_ROLLBACK_PLAN_MQH__
#define __SF14_ROLLBACK_PLAN_MQH__
#include "SF14_RegistrySnapshot.mqh"
#define SF14_MAX_ROLLBACK_TRIGGERS 16
struct SF14_RollbackPlan{string plan_id;string scope_id;string from_entry_id;string to_entry_id;int trigger_count;string trigger_codes[SF14_MAX_ROLLBACK_TRIGGERS];string registry_snapshot_hash;string approved_by;long approved_at_utc_msc;bool no_execution_authority;string plan_hash;};
string SF14_RollbackPlanCanonical(const SF14_RollbackPlan &v){string t="";for(int i=0;i<v.trigger_count;i++)t+="|"+v.trigger_codes[i];return "alpha_lab.strategy_factory/rollback_plan@1.0.0|"+v.plan_id+"|"+v.scope_id+"|"+v.from_entry_id+"|"+v.to_entry_id+t+"|"+v.registry_snapshot_hash+"|"+v.approved_by+"|"+IntegerToString(v.approved_at_utc_msc)+"|"+SF01_CanonicalBool(v.no_execution_authority);}
string SF14_DeriveRollbackPlanHash(const SF14_RollbackPlan &v){return SF01_StableId("rplan",SF14_RollbackPlanCanonical(v));}
bool SF14_ValidateRollbackPlan(const SF14_RollbackPlan &v,string &error){if(v.plan_id==""||v.scope_id==""||v.from_entry_id==""||v.to_entry_id==""||v.from_entry_id==v.to_entry_id||v.trigger_count<1||v.trigger_count>SF14_MAX_ROLLBACK_TRIGGERS||v.registry_snapshot_hash==""||v.approved_by==""||!v.no_execution_authority){error="invalid rollback plan";return false;}if(v.plan_hash!=""&&v.plan_hash!=SF14_DeriveRollbackPlanHash(v)){error="rollback plan hash mismatch";return false;}error="";return true;}
#endif
