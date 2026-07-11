from enum import IntEnum

class ExecutionMode(IntEnum):
    PAPER = 1
    SHADOW = 2

class OrderKind(IntEnum):
    MARKET = 1
    LIMIT = 2
    STOP = 3

class OrderState(IntEnum):
    RECEIVED = 1
    WORKING = 2
    PARTIALLY_FILLED = 3
    FILLED = 4
    CANCELED = 5
    EXPIRED = 6
    REJECTED = 7

class PositionState(IntEnum):
    OPEN = 1
    CLOSED = 2

class TransactionType(IntEnum):
    INTENT_RECEIVED = 1
    ORDER_ACCEPTED = 2
    ORDER_REJECTED = 3
    ORDER_WORKING = 4
    ORDER_PARTIAL_FILL = 5
    ORDER_FILLED = 6
    ORDER_CANCELED = 7
    ORDER_EXPIRED = 8
    POSITION_OPENED = 9
    POSITION_INCREASED = 10
    POSITION_CLOSED_STOP = 11
    POSITION_CLOSED_TARGET = 12
    POSITION_CLOSED_MANUAL = 13
    RECONCILIATION = 14

class FillReason(IntEnum):
    ENTRY_MARKET = 1
    ENTRY_LIMIT = 2
    ENTRY_STOP = 3
    EXIT_STOP = 4
    EXIT_TARGET = 5
    EXIT_MANUAL = 6

class RejectReason(IntEnum):
    NONE = 0
    INVALID_INTENT = 1
    RESEARCH_ONLY_AUTHORITY = 2
    EXPIRED_INTENT = 3
    DUPLICATE_HASH_CONFLICT = 4
    INVALID_SYMBOL_SPEC = 5
    INVALID_POLICY = 6
    CAPACITY_EXCEEDED = 7
    STALE_QUOTE = 8

class ReconciliationStatus(IntEnum):
    MATCHED = 1
    MISSING_EXPECTED = 2
    UNEXPECTED_OBSERVED = 3
    VOLUME_MISMATCH = 4
    DIRECTION_MISMATCH = 5
    PRICE_DRIFT = 6
