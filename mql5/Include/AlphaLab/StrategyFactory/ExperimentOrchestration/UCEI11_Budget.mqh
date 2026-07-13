#ifndef __UCEI11_BUDGET_MQH__
#define __UCEI11_BUDGET_MQH__

#include "UCEI11_Contracts.mqh"

struct UCEI11_BudgetUsage
  {
   int    trials_started;
   int    trials_completed;
   double total_wall_seconds;
   long   artifact_bytes;
   int    memory_high_water_mb;

   void Reset()
     {
      trials_started=0;
      trials_completed=0;
      total_wall_seconds=0.0;
      artifact_bytes=0;
      memory_high_water_mb=0;
     }
  };

class CUCEI11BudgetGuard
  {
private:
   UCEI11_BudgetPolicy m_policy;
   UCEI11_BudgetUsage  m_usage;

public:
   bool Configure(const UCEI11_BudgetPolicy &policy)
     {
      if(!policy.Valid())
         return false;
      m_policy=policy;
      m_usage.Reset();
      return true;
     }

   UCEI11_BUDGET_DECISION Assess(const UCEI11_ResourceClaim &claim,string &reason) const
     {
      reason="";
      if(!claim.Valid())
        {
         reason="invalid_resource_claim";
         return UCEI11_BUDGET_DENY;
        }
      if(m_usage.trials_started>=m_policy.max_trials)
        {
         reason="trial_count_exhausted";
         return UCEI11_BUDGET_DENY;
        }
      if(claim.wall_seconds>m_policy.max_trial_wall_seconds)
        {
         reason="trial_wall_budget_exceeded";
         return UCEI11_BUDGET_DENY;
        }
      if(m_usage.total_wall_seconds+claim.wall_seconds>m_policy.max_total_wall_seconds)
        {
         reason="total_wall_budget_exhausted";
         return UCEI11_BUDGET_DENY;
        }
      if(claim.memory_mb>m_policy.max_memory_mb)
        {
         reason="memory_budget_exceeded";
         return UCEI11_BUDGET_DENY;
        }
      if(claim.cpu_slots>m_policy.cpu_slots || claim.gpu_slots>m_policy.gpu_slots)
        {
         reason="compute_slot_budget_exceeded";
         return UCEI11_BUDGET_DENY;
        }
      if(m_usage.artifact_bytes+claim.artifact_bytes>m_policy.max_artifact_bytes)
        {
         reason="artifact_budget_exhausted";
         return UCEI11_BUDGET_DENY;
        }
      return UCEI11_BUDGET_ALLOW;
     }

   bool Reserve(const UCEI11_ResourceClaim &claim,string &reason)
     {
      if(Assess(claim,reason)!=UCEI11_BUDGET_ALLOW)
         return false;
      m_usage.trials_started++;
      if(claim.memory_mb>m_usage.memory_high_water_mb)
         m_usage.memory_high_water_mb=claim.memory_mb;
      return true;
     }

   void Complete(const double elapsed_seconds,const long artifact_bytes)
     {
      m_usage.trials_completed++;
      if(elapsed_seconds>0.0)
         m_usage.total_wall_seconds+=elapsed_seconds;
      if(artifact_bytes>0)
         m_usage.artifact_bytes+=artifact_bytes;
     }

   UCEI11_BudgetUsage Usage() const
     {
      return m_usage;
     }
  };

#endif
