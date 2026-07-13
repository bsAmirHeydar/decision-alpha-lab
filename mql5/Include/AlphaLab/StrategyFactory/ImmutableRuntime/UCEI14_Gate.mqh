#ifndef ALPHALAB_UCEI14_GATE
#define ALPHALAB_UCEI14_GATE
#include "UCEI14_Parity.mqh"
#include "UCEI14_Generation.mqh"
#include "UCEI14_Journal.mqh"
bool UCEI14BundleActivatable(const UCEI14BundleManifest &m){return(UCEI14HashLooksValid(m.bundle_hash)&&UCEI14HashLooksValid(m.preprocessing_hash)&&UCEI14HashLooksValid(m.model_hash)&&UCEI14HashLooksValid(m.export_hash)&&UCEI14HashLooksValid(m.policy_graph_hash)&&m.signature_valid&&m.parity_pass&&m.generation>0);}
UCEI14Decision UCEI14Decide(const UCEI14BundleManifest &m,const UCEI14Input &input,CUCEI14DecisionJournal &journal){UCEI14Decision d;d.request_id=input.request_id;d.occurrence_id=input.occurrence_id;d.bundle_hash=m.bundle_hash;d.generation=m.generation;d.order_authority=false;string key=UCEI14StableDecisionKey(input.request_id,m.bundle_hash);if(journal.Contains(key)){d.result=UCEI14_GATE_ABSTAIN;d.label="no_action";d.reason="duplicate_request";return(d);}if(!UCEI14BundleActivatable(m)){d.result=UCEI14_GATE_REJECT;d.label="no_action";d.reason="bundle_not_activatable";return(d);}if(input.kill_switch){d.result=UCEI14_GATE_REJECT;d.label="reject";d.reason="kill_switch";journal.Append(key);return(d);}UCEI14Vector x;UCEI14Output y;string reason;if(!UCEI14Preprocess(input,x,reason)||!UCEI14Infer(x,y)){d.result=UCEI14_GATE_ABSTAIN;d.label="no_action";d.reason=reason;return(d);}d.result=UCEI14_GATE_ACCEPT;d.label=y.label;d.reason="";journal.Append(key);return(d);}
#endif
