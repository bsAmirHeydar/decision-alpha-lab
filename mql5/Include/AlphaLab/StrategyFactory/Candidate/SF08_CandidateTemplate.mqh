#ifndef __SF08_CANDIDATE_TEMPLATE_MQH__
#define __SF08_CANDIDATE_TEMPLATE_MQH__
#include "SF08_PolicyParameters.mqh"

struct SF08_CandidateTemplate
{
   string template_id;
   string template_version;
   bool enabled;
   int priority;
   string entry_policy_id;
   string entry_policy_version;
   SF08_PolicyParameters entry_parameters;
   string stop_policy_id;
   string stop_policy_version;
   SF08_PolicyParameters stop_parameters;
   string exit_policy_id;
   string exit_policy_version;
   SF08_PolicyParameters exit_parameters;
   string admissibility_tag;
   string template_hash;
};

string SF08_CandidateTemplateCanonical(const SF08_CandidateTemplate &t)
{
   return t.template_id+"|"+t.template_version+"|"+SF01_CanonicalBool(t.enabled)+"|"+
          IntegerToString(t.priority)+"|"+t.entry_policy_id+"|"+t.entry_policy_version+"|"+
          SF08_DerivePolicyParameterHash(t.entry_parameters)+"|"+t.stop_policy_id+"|"+
          t.stop_policy_version+"|"+SF08_DerivePolicyParameterHash(t.stop_parameters)+"|"+
          t.exit_policy_id+"|"+t.exit_policy_version+"|"+
          SF08_DerivePolicyParameterHash(t.exit_parameters)+"|"+t.admissibility_tag;
}
string SF08_DeriveCandidateTemplateHash(const SF08_CandidateTemplate &t)
{return SF01_StableId("ctpl",SF08_CandidateTemplateCanonical(t));}

bool SF08_ValidateCandidateTemplate(const SF08_CandidateTemplate &t,string &error)
{
   if(!SF01_IsSafeIdentifier(t.template_id,128) || !SF01_IsSafeIdentifier(t.template_version,64))
   { error="invalid template identity"; return false; }
   if(t.priority<0 || t.priority>1000000)
   { error="invalid template priority"; return false; }
   if(!SF01_IsSafeIdentifier(t.entry_policy_id,128) || !SF01_IsSafeIdentifier(t.entry_policy_version,64) ||
      !SF01_IsSafeIdentifier(t.stop_policy_id,128) || !SF01_IsSafeIdentifier(t.stop_policy_version,64) ||
      !SF01_IsSafeIdentifier(t.exit_policy_id,128) || !SF01_IsSafeIdentifier(t.exit_policy_version,64))
   { error="invalid template policy identity"; return false; }
   if(t.admissibility_tag!="" && !SF01_IsSafeIdentifier(t.admissibility_tag,128))
   { error="invalid admissibility tag"; return false; }
   if(!SF08_ValidatePolicyParameters(t.entry_parameters,error) ||
      !SF08_ValidatePolicyParameters(t.stop_parameters,error) ||
      !SF08_ValidatePolicyParameters(t.exit_parameters,error)) return false;
   const string expected=SF08_DeriveCandidateTemplateHash(t);
   if(t.template_hash!="" && t.template_hash!=expected)
   { error="template hash mismatch"; return false; }
   error=""; return true;
}

#endif
