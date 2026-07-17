#ifndef ALPHALAB_ACL01_REGISTRY_ENVELOPE_MQH
#define ALPHALAB_ACL01_REGISTRY_ENVELOPE_MQH
struct ACL01RegistryEnvelope { string schema_version; long revision; string registry_digest; int artifact_count; bool mutation_authorized; };
bool ACL01RegistryEnvelopeValid(const ACL01RegistryEnvelope &x) { return x.revision>=0 && StringLen(x.registry_digest)>0; }
#endif
