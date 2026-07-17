#ifndef ALPHALAB_ACL05_EVENT_CONTRACT_MQH
#define ALPHALAB_ACL05_EVENT_CONTRACT_MQH
struct ACL05BatchEvent { string event_id; int sequence; string event_type; string previous_digest; string event_digest; bool order_submission_allowed; bool capital_activation_allowed; };
bool ACL05EventAuthorityValid(const ACL05BatchEvent &x){ return x.sequence>0 && !x.order_submission_allowed && !x.capital_activation_allowed && StringLen(x.event_digest)==71; }
#endif
