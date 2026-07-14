#property strict
#include <AlphaLab/StrategyFactory/SAEDV4Constitution/SAEDV400_All.mqh>

bool Expect(const bool condition,const string message)
  {
   if(!condition)
      Print("FAIL: ",message);
   return(condition);
  }

int OnInit()
  {
   SAEDV400_AuthorityRequest request;
   request.program_id="self-test";
   request.actor.actor_id="agent";
   request.actor.actor_type=SAEDV400_ACTOR_AGENT;
   request.actor.organization_unit="research-ai";
   request.known_time=TimeCurrent();
   request.purpose="research";

   request.authority=SAEDV400_AUTH_RESEARCH_PROPOSAL;
   SAEDV400_Decision allowed=CSAEDV400Authority::Evaluate(request);
   if(!Expect(allowed.status==SAEDV400_DECISION_ALLOW,"research proposal must be allowed")) return(INIT_FAILED);

   request.authority=SAEDV400_AUTH_ORDER;
   SAEDV400_Decision denied=CSAEDV400Authority::Evaluate(request);
   if(!Expect(denied.status==SAEDV400_DECISION_REJECT,"order must be denied")) return(INIT_FAILED);

   request.authority=SAEDV400_AUTH_CONSTITUTION_SELF_AMENDMENT;
   denied=CSAEDV400Authority::Evaluate(request);
   if(!Expect(denied.status==SAEDV400_DECISION_REJECT,"self amendment must be denied")) return(INIT_FAILED);
   return(INIT_SUCCEEDED);
  }

void OnTick() {}
