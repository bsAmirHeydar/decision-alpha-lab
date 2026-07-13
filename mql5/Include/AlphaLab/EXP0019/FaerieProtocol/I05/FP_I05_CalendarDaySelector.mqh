#ifndef __FP_I05_CALENDAR_DAY_SELECTOR_MQH__
#define __FP_I05_CALENDAR_DAY_SELECTOR_MQH__
#include "FP_I05_WindowStore.mqh"
class FP_I05_CalendarDaySelector {
 public:
  static bool IsCanonicalOffsetSequence(const FP_I05_CalendarDaySelectionItem &items[],const int depth){ if(ArraySize(items)!=depth) return false; for(int i=0;i<depth;i++) if(items[i].offset!=i+1) return false; return true; }
};
#endif
