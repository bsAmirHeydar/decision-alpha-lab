#property strict
#include <AlphaLab/StrategyFactory/OutcomeDataset/UCEI06_All.mqh>
int OnInit(){
 UCEI06_OpportunityAnchor a;a.context_package_key="context.synthetic@1.0.0";a.context_occurrence_id="ctx.001";a.dependence_cluster_id="cluster.001";a.symbol="EURUSD";a.timeframe=PERIOD_M5;a.side=1;a.event_time_ms=1000;a.decision_time_ms=1000;a.known_time_ms=1000;a.feature_frame_hash="frame.001";a.eligible=true;
 CUCEI06OpportunityAnchorBuilder b;string reason="";if(!b.Validate(a,reason))return INIT_FAILED;a.opportunity_id=b.BuildIdentity(a);if(a.opportunity_id=="")return INIT_FAILED;
 CUCEI06MaturityEngine m;UCEI06_MaturityEvidence e=m.Evaluate(UCEI06_RESOLVED,UCEI06_TERM_TARGET,2000,2000);if(!e.mature||!e.event_observed)return INIT_FAILED;
 Print("UCE-I06 self-test PASS: ",a.opportunity_id);return INIT_SUCCEEDED;}
void OnTick(){}
