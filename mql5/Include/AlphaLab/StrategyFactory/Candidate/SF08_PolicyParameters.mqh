#ifndef __SF08_POLICY_PARAMETERS_MQH__
#define __SF08_POLICY_PARAMETERS_MQH__
#include "../Contracts/SF01_AllContracts.mqh"
#include "SF08_CandidateEnums.mqh"

struct SF08_PolicyParameters
{
   double numeric[SF08_MAX_POLICY_PARAMS];
   long integer_values[SF08_MAX_POLICY_PARAMS];
   string string_value;
   string parameter_hash;
};

void SF08_ResetPolicyParameters(SF08_PolicyParameters &p)
{
   for(int i=0;i<SF08_MAX_POLICY_PARAMS;i++)
   {
      p.numeric[i]=0.0;
      p.integer_values[i]=0;
   }
   p.string_value="";
   p.parameter_hash="";
}

string SF08_PolicyParametersCanonical(const SF08_PolicyParameters &p)
{
   string payload="";
   for(int i=0;i<SF08_MAX_POLICY_PARAMS;i++)
      payload += "|d"+IntegerToString(i)+"="+SF01_CanonicalDouble(p.numeric[i]);
   for(int i=0;i<SF08_MAX_POLICY_PARAMS;i++)
      payload += "|i"+IntegerToString(i)+"="+IntegerToString(p.integer_values[i]);
   payload += "|s="+SF01_EscapeJsonString(p.string_value);
   return payload;
}

string SF08_DerivePolicyParameterHash(const SF08_PolicyParameters &p)
{
   return SF01_StableId("ppar",SF08_PolicyParametersCanonical(p));
}

bool SF08_ValidatePolicyParameters(const SF08_PolicyParameters &p,string &error)
{
   for(int i=0;i<SF08_MAX_POLICY_PARAMS;i++)
      if(!MathIsValidNumber(p.numeric[i]))
      { error="non-finite policy numeric parameter"; return false; }
   if(StringLen(p.string_value)>256)
   { error="policy string parameter too long"; return false; }
   const string expected=SF08_DerivePolicyParameterHash(p);
   if(p.parameter_hash!="" && p.parameter_hash!=expected)
   { error="policy parameter hash mismatch"; return false; }
   error="";
   return true;
}

#endif
