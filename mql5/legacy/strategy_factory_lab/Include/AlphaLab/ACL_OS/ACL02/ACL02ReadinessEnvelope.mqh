#ifndef ALPHALAB_ACL02_READINESS_MQH
#define ALPHALAB_ACL02_READINESS_MQH
#include "ACL02Enums.mqh"
struct ACL02ReadinessEnvelope{string context_id;ACL02ReadinessState state;ACL02IntakeDecision decision;double completeness;int blockers;string report_digest;bool live_order_submission_allowed;bool capital_activation_allowed;};
#endif
