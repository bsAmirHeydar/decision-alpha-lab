#ifndef ALPHALAB_OPERATIONS_RETIREMENT_GUARD_MQH
#define ALPHALAB_OPERATIONS_RETIREMENT_GUARD_MQH
struct ALOperationsRetirementState { bool positions_flat; bool reservations_zero; bool leases_revoked; int open_high_or_critical_incidents; };
bool ALOpsRetirementAllowed(const ALOperationsRetirementState &state){ return state.positions_flat&&state.reservations_zero&&state.leases_revoked&&state.open_high_or_critical_incidents==0; }
#endif
