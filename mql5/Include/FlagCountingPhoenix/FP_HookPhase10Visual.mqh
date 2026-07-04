#ifndef __FP_HOOK_PHASE10_VISUAL_MQH__
#define __FP_HOOK_PHASE10_VISUAL_MQH__
#property strict

#include "FP_HookPhase10Rules.mqh"

// Phase 10 is intentionally no-draw. The freeze/training contract must not add
// chart evidence that could be confused with Hook structure. All artifacts are
// CSV/log contracts only.
int FP_HookP10DeleteObjectsByPrefix(const string prefix)
{
   if(StringLen(prefix) <= 0)
      return 0;

   int deleted = 0;
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
      {
         if(ObjectDelete(0, name))
            deleted++;
      }
   }
   return deleted;
}

#endif // __FP_HOOK_PHASE10_VISUAL_MQH__
