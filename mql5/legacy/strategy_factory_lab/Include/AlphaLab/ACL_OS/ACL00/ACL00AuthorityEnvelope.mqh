#ifndef ALPHALAB_ACL00_AUTHORITY_ENVELOPE_MQH
#define ALPHALAB_ACL00_AUTHORITY_ENVELOPE_MQH
struct ACL00_AuthorityEnvelope { string transition_id; string subject_id; string policy_digest; int decision; string reason_code; bool capital_activation_allowed; bool live_order_submission_allowed; };
bool ACL00_EnvelopeFailClosed(const ACL00_AuthorityEnvelope &x) { return (x.transition_id=="" || x.subject_id=="" || x.policy_digest=="" || x.decision!=ACL00_ALLOW || x.capital_activation_allowed || x.live_order_submission_allowed); }
#endif
