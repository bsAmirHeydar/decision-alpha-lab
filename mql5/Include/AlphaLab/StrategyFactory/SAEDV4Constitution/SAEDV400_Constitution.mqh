#ifndef __ALPHALAB_SAEDV400_CONSTITUTION_MQH__
#define __ALPHALAB_SAEDV400_CONSTITUTION_MQH__
#include "SAEDV400_Authority.mqh"
#include "SAEDV400_EvidenceFirewall.mqh"

class CSAEDV400Constitution
  {
private:
   string m_constitution_hash;
   string m_policy_hash;
public:
   bool Configure(const string constitution_hash,const string policy_hash)
     {
      if(StringLen(constitution_hash)!=64 || StringLen(policy_hash)!=64)
         return(false);
      m_constitution_hash=constitution_hash;
      m_policy_hash=policy_hash;
      return(true);
     }

   string ConstitutionHash(void) const { return(m_constitution_hash); }
   string PolicyHash(void) const { return(m_policy_hash); }

   SAEDV400_Decision EvaluateAuthority(const SAEDV400_AuthorityRequest &request) const
     {
      return(CSAEDV400Authority::Evaluate(request));
     }

   SAEDV400_Decision EvaluateEvidence(const SAEDV400_EvidenceRequest &request) const
     {
      return(CSAEDV400EvidenceFirewall::Evaluate(request));
     }
  };

#endif
