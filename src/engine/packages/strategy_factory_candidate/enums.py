from enum import IntEnum
class PolicyKind(IntEnum): ENTRY=1; STOP=2; EXIT=3; GATE=4
class OrderKind(IntEnum): MARKET=1; LIMIT=2; STOP=3
class ExitKind(IntEnum): PRICE_TARGET=1; TIME_ONLY=2; PRICE_OR_TIME=3; STRUCTURAL=4
class PolicyDecision(IntEnum): ADMIT=1; SKIP=2; ERROR=3
class CandidateStatus(IntEnum): EMPTY=0; VALID=1; SKIPPED=2; REJECTED=3
