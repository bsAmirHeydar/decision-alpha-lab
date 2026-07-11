from enum import IntEnum
class UpdateScope(IntEnum):
    STATIC=0; EVENT=1; TICK=2; NEW_BAR=3; TIMER=4
class MissingPolicy(IntEnum):
    FAIL=0; DEFAULT=1; ZERO=2
class ContextStatus(IntEnum):
    EMPTY=0; COMPILING=1; READY=2; BUILDING=3; DEGRADED=4; FAILED=5
