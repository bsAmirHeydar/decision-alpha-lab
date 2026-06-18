#ifndef __DAL_STRUCTURAL_NODE_ENGINE_MQH__
#define __DAL_STRUCTURAL_NODE_ENGINE_MQH__

// Decision Alpha Lab structural node public API.
//
// This module is intentionally the stable boundary for structural node detection.
// The L-rule implementation is validated and should be treated as frozen for
// M0001 development. Downstream modules should include this facade, not the
// detector internals directly.

#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleDetector.mqh>

int DAL_DetectConfirmedStructuralNodes(
   const DALBar &bars[],
   const int bars_count,
   const int L,
   DALLRuleNode &nodes[]
)
{
   return DAL_DetectLRuleNodes(bars, bars_count, L, nodes);
}

#endif
