#property strict
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Types.mqh>
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Gate.mqh>
int OnInit(){UCEI15_GateState g;g.tournament_not_reference_only=false;g.bounded_challenger_exists=true;g.paper_mode_prospective=false;g.paper_completed=false;g.paper_untouched=true;g.paper_no_critical_findings=false;g.paper_zero_reconciliation_mismatch=true;if(UCEI15_Decide(g,true)!=UCEI15_REJECT)return(INIT_FAILED);return(INIT_SUCCEEDED);}
void OnTick(){}
