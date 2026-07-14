#property strict
#property description "SAED V4-00 constitutional diagnostic. No trading authority."
#include <AlphaLab/StrategyFactory/SAEDV4Constitution/SAEDV400_All.mqh>

int OnInit()
  {
   CSAEDV400Constitution constitution;
   if(!constitution.Configure("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                              "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"))
      return(INIT_FAILED);

   SAEDV400_AuthorityRequest request;
   request.program_id="diagnostic";
   request.actor.actor_id="diagnostic-agent";
   request.actor.actor_type=SAEDV400_ACTOR_AGENT;
   request.actor.organization_unit="research-ai";
   request.authority=SAEDV400_AUTH_ORDER;
   request.known_time=TimeCurrent();
   request.purpose="diagnostic";

   SAEDV400_Decision decision=constitution.EvaluateAuthority(request);
   if(decision.status!=SAEDV400_DECISION_REJECT)
      return(INIT_FAILED);

   Print("SAED V4-00 diagnostic PASS: research agent order authority rejected.");
   return(INIT_SUCCEEDED);
  }

void OnTick() {}
