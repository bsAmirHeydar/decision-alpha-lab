#ifndef __FP_I06_REVISION_INVALIDATION_MQH__
#define __FP_I06_REVISION_INVALIDATION_MQH__
class FP_I06_RevisionInvalidation { public: static bool MinuteOverlaps(long minute,long start_ms,long end_ms){return minute>=start_ms && minute<end_ms;} static bool WindowAffects(string changed_window,string reference_window,string check_window){return changed_window==reference_window || changed_window==check_window;} };
#endif
