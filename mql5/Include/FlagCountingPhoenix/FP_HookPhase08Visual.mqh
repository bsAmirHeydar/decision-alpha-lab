#ifndef __FP_HOOK_PHASE08_VISUAL_MQH__
#define __FP_HOOK_PHASE08_VISUAL_MQH__
#property strict

#include "FP_HookPhase08Rules.mqh"

// Phase 08 intentionally does not draw chart objects.
// It is an audit/export reconciliation layer. Visual behavior is controlled by
// Phase 07 profiles and the individual Phase 01..06 visual modules.

int FP_HookP08VisualObjectsCreated()
{
   return 0;
}

#endif // __FP_HOOK_PHASE08_VISUAL_MQH__
