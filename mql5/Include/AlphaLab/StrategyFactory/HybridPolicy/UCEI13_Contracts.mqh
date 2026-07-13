#ifndef ALPHALAB_UCEI13_CONTRACTS
#define ALPHALAB_UCEI13_CONTRACTS
#include "UCEI13_Enums.mqh"
struct UCEI13ManualDecision{bool eligible;bool vetoed;string action;string treatment;string risk_tier;string policy_hash;};
struct UCEI13ModelOutput{bool valid;bool stale;bool ood;bool low_confidence;bool missing_view;string action;string treatment;string risk_tier;double score;string output_hash;};
struct UCEI13Decision{UCEI13DecisionStatus status;UCEI13Authority authority;UCEI13Fallback fallback;string action;string treatment;string risk_tier;string reason;};
#endif
