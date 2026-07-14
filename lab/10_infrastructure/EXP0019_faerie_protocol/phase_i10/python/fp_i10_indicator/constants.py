PHASE_ID = "FP-I10"
PHASE_VERSION = "1.0.0"
CONTEXT_ID = "FP-CONTEXT-001"
INDICATOR_PRODUCT_ID = "EXP0019_FaerieProtocol_Context"
INDICATOR_SCHEMA_VERSION = "1.0.0"
CHECKPOINT_VERSION = "1.0.0"
COMPOSITION_VERSION = "1.0.0"
OUTPUT_VERSION = "1.0.0"
EXPECTED_UPSTREAM = (
    ("FP-I03", "1.0.0"),
    ("FP-I04", "1.0.0"),
    ("FP-I05", "1.0.0"),
    ("FP-I06", "1.0.0"),
    ("FP-I07", "1.0.0"),
    ("FP-I08", "1.0.0"),
    ("FP-I09", "1.0.0"),
)
EXPECTED_UPSTREAM_PHASES = tuple(x[0] for x in EXPECTED_UPSTREAM)
BUFFER_NAMES = (
    "health_code",
    "lifecycle_code",
    "data_readiness_code",
    "active_ww_direction",
    "confirmed_signal_count",
    "allowed_signal_count",
    "suppressed_by_ww_count",
    "suppressed_by_quota_count",
    "quota_winner_present",
    "ledger_event_count",
    "source_revision_sequence",
    "heartbeat_utc_minute",
)
BUFFER_COUNT = len(BUFFER_NAMES)
DEFAULT_TIMER_SECONDS = 1
DEFAULT_HISTORY_DAYS = 90
DEFAULT_MAX_INCREMENTAL_MINUTES = 1440
MIN_HISTORY_DAYS = 5
MAX_HISTORY_DAYS = 3660
MIN_TIMER_SECONDS = 1
MAX_TIMER_SECONDS = 60
MAX_INCREMENTAL_LIMIT = 10080
NO_RUNTIME_AUTHORITY = "NONE"
FORBIDDEN_MQL5_TOKENS = (
    "OrderSend(", "OrderSendAsync(", "CTrade", "PositionOpen(", "PositionClose(",
    "Buy(", "Sell(", "WebRequest(", "ObjectCreate(", "ObjectDelete(", "ChartSetSymbolPeriod("
)
