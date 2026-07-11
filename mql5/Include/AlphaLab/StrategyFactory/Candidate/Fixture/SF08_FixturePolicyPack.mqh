#ifndef __SF08_FIXTURE_POLICY_PACK_MQH__
#define __SF08_FIXTURE_POLICY_PACK_MQH__
#include "SF08_ConfirmationMarketEntry.mqh"
#include "SF08_ReferenceLimitEntry.mqh"
#include "SF08_AnatomyInvalidationStop.mqh"
#include "SF08_BufferedInvalidationStop.mqh"
#include "SF08_FixedRExit.mqh"
#include "SF08_TimeOnlyExit.mqh"
class CSF08FixturePolicyPack
{
private:
   CSF08ConfirmationMarketEntry m_market;
   CSF08ReferenceLimitEntry m_limit;
   CSF08AnatomyInvalidationStop m_invalidation;
   CSF08BufferedInvalidationStop m_buffered;
   CSF08FixedRExit m_fixed_r;
   CSF08TimeOnlyExit m_time;
public:
   bool RegisterAll(CSF08PolicyRegistry &registry,string &error)
   {return registry.RegisterEntry(&m_market,error)&&registry.RegisterEntry(&m_limit,error)&&registry.RegisterStop(&m_invalidation,error)&&registry.RegisterStop(&m_buffered,error)&&registry.RegisterExit(&m_fixed_r,error)&&registry.RegisterExit(&m_time,error);}
   bool BuildReferenceMatrix(CSF08CandidateMatrixPlan &plan,string &error)
   {
      plan.plan_id="sf08.reference_matrix";plan.plan_version="1.0.0";
      SF08_CandidateTemplate t;SF08_ResetPolicyParameters(t.entry_parameters);SF08_ResetPolicyParameters(t.stop_parameters);SF08_ResetPolicyParameters(t.exit_parameters);
      t.template_id="market_invalidation_1r5";t.template_version="1.0.0";t.enabled=true;t.priority=10;t.entry_policy_id="sf08.entry.confirmation_market";t.entry_policy_version="1.0.0";t.entry_parameters.integer_values[0]=5000;t.entry_parameters.numeric[0]=2.0;t.stop_policy_id="sf08.stop.anatomy_invalidation";t.stop_policy_version="1.0.0";t.exit_policy_id="sf08.exit.fixed_r";t.exit_policy_version="1.0.0";t.exit_parameters.numeric[0]=1.5;t.exit_parameters.integer_values[0]=3600000;t.admissibility_tag="reference";if(!plan.Add(t,error))return false;
      SF08_ResetPolicyParameters(t.entry_parameters);SF08_ResetPolicyParameters(t.stop_parameters);SF08_ResetPolicyParameters(t.exit_parameters);t.template_id="reference_buffered_2r";t.template_version="1.0.0";t.enabled=true;t.priority=20;t.entry_policy_id="sf08.entry.reference_limit";t.entry_policy_version="1.0.0";t.entry_parameters.integer_values[0]=900000;t.stop_policy_id="sf08.stop.buffered_invalidation";t.stop_policy_version="1.0.0";t.stop_parameters.numeric[0]=0.0002;t.exit_policy_id="sf08.exit.fixed_r";t.exit_policy_version="1.0.0";t.exit_parameters.numeric[0]=2.0;t.exit_parameters.integer_values[0]=7200000;t.admissibility_tag="reference";if(!plan.Add(t,error))return false;
      return true;
   }
};
#endif
