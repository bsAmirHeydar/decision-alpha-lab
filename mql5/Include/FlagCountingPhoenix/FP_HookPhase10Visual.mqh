#ifndef __FP_HOOK_PHASE10_VISUAL_MQH__
#define __FP_HOOK_PHASE10_VISUAL_MQH__
#property strict

#include "FP_HookPhase10Rules.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

// Phase 10 is intentionally no-draw. The freeze/training contract must not add
// chart evidence that could be confused with Hook structure. All artifacts are
// CSV/log contracts only.
int FP_HookP10DeleteObjectsByPrefix(const string prefix)
{
   return AL_UC04DeleteObjectsByPrefix(0, prefix);
}

#endif // __FP_HOOK_PHASE10_VISUAL_MQH__
