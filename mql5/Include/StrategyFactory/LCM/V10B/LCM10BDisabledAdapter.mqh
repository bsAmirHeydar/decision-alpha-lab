#ifndef __LCM10B_DISABLED_ADAPTER_MQH__
#define __LCM10B_DISABLED_ADAPTER_MQH__
#include "LCM10BTypes.mqh"
#include "LCM10BCapabilityGuard.mqh"
#include "LCM10BIntentValidator.mqh"
class CLCM10BDisabledAdapter { private: CLCM10BCapabilityGuard m_guard; CLCM10BIntentValidator m_validator; public: ENUM_LCM10B_RESULT DryReference(const LCM10BExecutionIntent &intent,string &reason){ if(!m_guard.DryReferenceEnabled()){reason="DRY_REFERENCE_DISABLED";return LCM10B_RESULT_BLOCKED;} if(!m_validator.Validate(intent,reason))return LCM10B_RESULT_BLOCKED; reason="DRY_REFERENCE_ONLY";return LCM10B_RESULT_DRY_REFERENCE;} bool SubmissionEnabled(void) const { return false; } };
#endif
