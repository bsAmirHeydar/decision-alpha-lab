#ifndef __FP_I05_REFERENCE_ENGINE_MQH__
#define __FP_I05_REFERENCE_ENGINE_MQH__
#include "FP_I05_Contracts.mqh"
class FP_I05_ReferenceEngine {
 public:
  static bool ApplyHunterTouch(FP_I05_ReferenceLevel &value,const long event_utc_ms){ if(!value.ActiveForHunt()) return false; value.state=FP_I05_REF_HUNTER_SEEN; value.state_sequence++; value.last_transition_utc_ms=event_utc_ms; value.reason_code="FP_RRC_HUNTER_TOUCH_NONCONSUMING"; return true; }
  static bool ApplyProtectedTouch(FP_I05_ReferenceLevel &value,const long event_utc_ms){ if(!value.ActiveForHunt()) return false; value.state=FP_I05_REF_CONSUMED_BY_PROTECTED; value.state_sequence++; value.last_transition_utc_ms=event_utc_ms; value.reason_code="FP_RRC_REFERENCE_CONSUMED_BY_PROTECTED"; return true; }
  static bool Expire(FP_I05_ReferenceLevel &value,const long event_utc_ms){ if(!value.ActiveForHunt()) return false; value.state=FP_I05_REF_EXPIRED; value.state_sequence++; value.last_transition_utc_ms=event_utc_ms; value.reason_code="FP_RRC_REFERENCE_EXPIRED"; return true; }
};
#endif
