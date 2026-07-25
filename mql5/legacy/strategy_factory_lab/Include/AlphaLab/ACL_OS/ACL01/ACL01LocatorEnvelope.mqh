#ifndef ALPHALAB_ACL01_LOCATOR_ENVELOPE_MQH
#define ALPHALAB_ACL01_LOCATOR_ENVELOPE_MQH
#include "ACL01Enums.mqh"
#include "ACL01ArtifactIdentity.mqh"
struct ACL01LocatorEnvelope { ENUM_ACL01_RESOLUTION_STATUS status; ACL01ArtifactIdentity identity; string canonical_path; string registry_digest; bool verified_digest; bool live_order_submission_allowed; bool capital_activation_allowed; };
bool ACL01LocatorEnvelopeSafe(const ACL01LocatorEnvelope &x) { return !x.live_order_submission_allowed && !x.capital_activation_allowed && (x.status!=ACL01_RESOLVED || x.verified_digest); }
#endif
