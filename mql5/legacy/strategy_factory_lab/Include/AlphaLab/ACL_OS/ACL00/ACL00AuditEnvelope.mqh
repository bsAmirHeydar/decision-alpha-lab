#ifndef ALPHALAB_ACL00_AUDIT_ENVELOPE_MQH
#define ALPHALAB_ACL00_AUDIT_ENVELOPE_MQH
struct ACL00_AuditEnvelope { long sequence; string event_id; string payload_digest; string previous_hash; string event_hash; };
bool ACL00_AuditEnvelopeComplete(const ACL00_AuditEnvelope &x) { return x.sequence>0 && x.event_id!="" && x.payload_digest!="" && x.previous_hash!="" && x.event_hash!=""; }
#endif
