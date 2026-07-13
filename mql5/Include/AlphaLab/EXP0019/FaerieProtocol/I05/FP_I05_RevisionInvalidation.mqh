#ifndef __FP_I05_REVISION_INVALIDATION_MQH__
#define __FP_I05_REVISION_INVALIDATION_MQH__
#include "FP_I05_Contracts.mqh"
class FP_I05_RevisionInvalidation {
 public:
  static bool Overlaps(const FP_I05_WindowDescriptor &window,const long start_utc_ms,const long end_utc_ms){ return window.start_utc_ms<end_utc_ms && start_utc_ms<window.end_utc_ms; }
};
#endif
