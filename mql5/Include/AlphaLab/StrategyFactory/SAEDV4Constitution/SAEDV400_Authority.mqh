#ifndef __ALPHALAB_SAEDV400_AUTHORITY_MQH__
#define __ALPHALAB_SAEDV400_AUTHORITY_MQH__
#include "SAEDV400_Contracts.mqh"

class CSAEDV400Authority
  {
public:
   static bool IsResearchActor(const ENUM_SAEDV400_ACTOR_TYPE actor_type)
     {
      return(actor_type==SAEDV400_ACTOR_AGENT ||
             actor_type==SAEDV400_ACTOR_HUMAN_RESEARCHER ||
             actor_type==SAEDV400_ACTOR_HUMAN_REVIEWER);
     }

   static bool IsHardDeniedForResearch(const ENUM_SAEDV400_AUTHORITY authority)
     {
      return(authority==SAEDV400_AUTH_CONTEXT_TRUTH_MUTATION ||
             authority==SAEDV400_AUTH_EVIDENCE_ROLE_REASSIGNMENT ||
             authority==SAEDV400_AUTH_HIDDEN_EVALUATION_ROW_ACCESS ||
             authority==SAEDV400_AUTH_CONSTITUTION_SELF_AMENDMENT ||
             authority==SAEDV400_AUTH_PROMOTION_SIGNATURE ||
             authority==SAEDV400_AUTH_RISK_LIMIT_CHANGE ||
             authority==SAEDV400_AUTH_PORTFOLIO_ALLOCATION ||
             authority==SAEDV400_AUTH_RUNTIME_ACTIVATION ||
             authority==SAEDV400_AUTH_ORDER ||
             authority==SAEDV400_AUTH_BROKER ||
             authority==SAEDV400_AUTH_NETWORK);
     }

   static bool HasExplicitGrant(const ENUM_SAEDV400_ACTOR_TYPE actor_type,
                                const ENUM_SAEDV400_AUTHORITY authority)
     {
      if(actor_type==SAEDV400_ACTOR_AGENT)
         return(authority==SAEDV400_AUTH_RESEARCH_PROPOSAL ||
                authority==SAEDV400_AUTH_SANDBOX_COMPUTE ||
                authority==SAEDV400_AUTH_EVIDENCE_PACKET_DRAFT ||
                authority==SAEDV400_AUTH_RED_TEAM_CHALLENGE);
      if(actor_type==SAEDV400_ACTOR_HUMAN_RESEARCHER)
         return(authority==SAEDV400_AUTH_RESEARCH_PROPOSAL ||
                authority==SAEDV400_AUTH_SANDBOX_COMPUTE ||
                authority==SAEDV400_AUTH_EVIDENCE_PACKET_DRAFT);
      if(actor_type==SAEDV400_ACTOR_HUMAN_REVIEWER)
         return(authority==SAEDV400_AUTH_INDEPENDENT_REVIEW ||
                authority==SAEDV400_AUTH_RED_TEAM_CHALLENGE);
      if(actor_type==SAEDV400_ACTOR_HIDDEN_EVALUATION_SERVICE)
         return(authority==SAEDV400_AUTH_HIDDEN_EVALUATION_ROW_ACCESS ||
                authority==SAEDV400_AUTH_EVIDENCE_PACKET_DRAFT);
      if(actor_type==SAEDV400_ACTOR_RISK_COMMITTEE)
         return(authority==SAEDV400_AUTH_INDEPENDENT_REVIEW ||
                authority==SAEDV400_AUTH_PROMOTION_SIGNATURE ||
                authority==SAEDV400_AUTH_RISK_LIMIT_CHANGE);
      if(actor_type==SAEDV400_ACTOR_RUNTIME_COMPILER)
         return(authority==SAEDV400_AUTH_RUNTIME_ACTIVATION);
      if(actor_type==SAEDV400_ACTOR_PORTFOLIO_ENGINE)
         return(authority==SAEDV400_AUTH_PORTFOLIO_ALLOCATION);
      if(actor_type==SAEDV400_ACTOR_EXECUTION_ADAPTER)
         return(authority==SAEDV400_AUTH_ORDER ||
                authority==SAEDV400_AUTH_BROKER ||
                authority==SAEDV400_AUTH_NETWORK);
      return(false);
     }

   static SAEDV400_Decision Evaluate(const SAEDV400_AuthorityRequest &request)
     {
      SAEDV400_Decision decision;
      decision.status=SAEDV400_DECISION_REJECT;
      decision.reason_code="authority_denied";
      decision.detail="No explicit constitutional grant.";

      if(IsResearchActor(request.actor.actor_type) && IsHardDeniedForResearch(request.authority))
        {
         decision.detail="Hard authority is constitutionally denied to research actors.";
         return(decision);
        }
      if(!HasExplicitGrant(request.actor.actor_type,request.authority))
         return(decision);

      if(request.actor.actor_type==SAEDV400_ACTOR_HIDDEN_EVALUATION_SERVICE &&
         request.authority==SAEDV400_AUTH_HIDDEN_EVALUATION_ROW_ACCESS &&
         StringFind(request.purpose,"hidden_evaluation")<0)
        {
         decision.detail="Hidden row access is purpose limited.";
         return(decision);
        }

      decision.status=SAEDV400_DECISION_ALLOW;
      decision.reason_code="ok";
      decision.detail="";
      return(decision);
     }
  };

#endif
