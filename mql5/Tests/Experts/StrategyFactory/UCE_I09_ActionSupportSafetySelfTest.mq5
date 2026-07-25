#property strict
#include <AlphaLab/StrategyFactory/AdvancedTasks/UCEI09_All.mqh>
int OnInit(){string declared[]={"wide_stop@1.0.0","tight_stop@1.0.0"};UCEI09_ConservativePolicyDecision d;d.decision_id="d";d.row_id="r";d.selected_action_key="unseen@1.0.0";d.baseline_action_key=declared[0];d.decision=UCEI09_ACTION;d.evidence_hash="h";if(d.UsesDeclaredAction(declared))return INIT_FAILED;d.selected_action_key=declared[1];return d.UsesDeclaredAction(declared)?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
