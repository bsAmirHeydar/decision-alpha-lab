#ifndef __LCM10B_CAPABILITY_GUARD_MQH__
#define __LCM10B_CAPABILITY_GUARD_MQH__
class CLCM10BCapabilityGuard { public: bool SubmissionEnabled(void) const { return false; } bool BrokerMutationEnabled(void) const { return false; } bool DryReferenceEnabled(void) const { return true; } };
#endif
