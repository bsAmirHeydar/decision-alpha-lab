#ifndef ALPHALAB_ACL05_LABEL_CONTRACT_MQH
#define ALPHALAB_ACL05_LABEL_CONTRACT_MQH
struct ACL05LabelContract { string label_id; string role; string contract_digest; long horizon_seconds; long available_after_seconds; bool future_path_diagnostic; bool segregated; };
bool ACL05LabelContractValid(const ACL05LabelContract &x){ if(x.horizon_seconds<=0 || x.available_after_seconds<x.horizon_seconds) return false; if(x.role=="PRIMARY" && x.future_path_diagnostic) return false; if(x.role=="DIAGNOSTIC" && !x.segregated) return false; return StringLen(x.contract_digest)==71; }
#endif
