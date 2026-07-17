#ifndef ALPHALAB_ACL00_LIFECYCLE_GATE_MQH
#define ALPHALAB_ACL00_LIFECYCLE_GATE_MQH
bool ACL00_IsAdjacentResearchTransition(const int from_state,const int to_state) { if(from_state<ACL00_DRAFT_CONTEXT || from_state>ACL00_CHAMPION) return false; return to_state==from_state+1; }
bool ACL00_IsTerminal(const int state) { return state==ACL00_RETIRED; }
bool ACL00_CanSubmitLiveOrders() { return false; }
#endif
