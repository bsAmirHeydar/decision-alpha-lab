# Structural Node Module Lock

The structural node detector has been validated and is now treated as a stable
module.

Public include:

```text
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
```

Stable public function:

```text
DAL_DetectConfirmedStructuralNodes(...)
```

Implementation files:

```text
StructuralNodes/LRule/DAL_LRuleTypes.mqh
StructuralNodes/LRule/DAL_LRuleDetector.mqh
```

Rule:

```text
Do not change L-rule detection while working on M0001 expansion, territory, event,
RTV or hunt validation.
```

M0001 should consume confirmed structural nodes as input and build additional
logic on top of them.
