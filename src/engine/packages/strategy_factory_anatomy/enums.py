from enum import IntEnum
class ObservationKind(IntEnum):
    UNKNOWN=0; REFERENCE_SWEEP_HIGH=1; REFERENCE_SWEEP_LOW=2; CONFIRMATION=3; INVALIDATION=4
class LifecycleState(IntEnum):
    UNKNOWN=0; OBSERVED=1; CONFIRMED=2; EMITTED=3; REJECTED=4; RETIRED=5
ALLOWED={(LifecycleState.UNKNOWN,LifecycleState.OBSERVED),(LifecycleState.OBSERVED,LifecycleState.CONFIRMED),(LifecycleState.OBSERVED,LifecycleState.REJECTED),(LifecycleState.CONFIRMED,LifecycleState.EMITTED),(LifecycleState.CONFIRMED,LifecycleState.REJECTED),(LifecycleState.EMITTED,LifecycleState.RETIRED),(LifecycleState.REJECTED,LifecycleState.RETIRED)}
