#ifndef AL_ACL04_SETUP_POLICY_IR_MQH
#define AL_ACL04_SETUP_POLICY_IR_MQH

struct AL_ACL04_RiskContract
  {
   string sizing_mode;
   double max_risk_units;
   bool   protective_reference_required;
  };

struct AL_ACL04_SetupClause
  {
   string clause_id;
   string clause_kind;
   string expression_digest;
   string action_id;
   string action_parameters_digest;
   int    priority;
  };

struct AL_ACL04_SetupPolicyIR
  {
   string schema_version;
   string ir_type;
   string policy_ir_digest;
   string context_id;
   string context_version;
   string lane;
   string treatment_family;
   string parameter_digest;
   string clause_set_digest;
   AL_ACL04_RiskContract risk_contract;
   bool   known_time_contract;
   bool   execution_authority;
   bool   diagnostic_only;
  };

bool AL_ACL04_PolicyIRIsNonExecuting(const AL_ACL04_SetupPolicyIR &policy)
  {
   return(policy.ir_type=="ACL04_SETUP_POLICY_IR" &&
          policy.known_time_contract &&
          !policy.execution_authority &&
          StringFind(policy.policy_ir_digest,"sha256:")==0);
  }

#endif
