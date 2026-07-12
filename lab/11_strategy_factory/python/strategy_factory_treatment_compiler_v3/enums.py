from enum import Enum
class RuleType(str,Enum):
    REQUIRE_ATOM='require_atom'; PROHIBIT_ATOM='prohibit_atom'; REQUIRE_TAG='require_tag'; PROHIBIT_TAG='prohibit_tag';
    REQUIRE_CONTEXT_FIELD='require_context_field'; REQUIRE_CAPABILITY='require_capability'; PARAMETER_RELATION='parameter_relation';
    MARKET_MODE='market_mode'; ACCOUNT_MODE='account_mode'; MAX_COUNT='max_count'; QUANTITY_SUM='quantity_sum'
class RuleSeverity(str,Enum): ERROR='error'; WARNING='warning'
class PathState(str,Enum):
    DRAFT='draft'; PENDING='pending'; TRIGGERED='triggered'; PARTIALLY_FILLED='partially_filled'; OPEN='open'; SCALED='scaled';
    PARTIALLY_EXITED='partially_exited'; TRAILED='trailed'; STOPPED='stopped'; TARGETED='targeted'; TIMED_OUT='timed_out';
    CANCELED='canceled'; REJECTED='rejected'; CLOSED='closed'
class PathEventType(str,Enum):
    SUBMIT='submit'; TRIGGER='trigger'; FILL='fill'; SCALE='scale'; PARTIAL_EXIT='partial_exit'; TRAIL_UPDATE='trail_update';
    STOP_HIT='stop_hit'; TARGET_HIT='target_hit'; TIMEOUT='timeout'; CANCEL='cancel'; REJECT='reject'; CLOSE='close'
class FidelityMode(str,Enum): TICK='tick'; BAR='bar'; HYBRID='hybrid'
class AmbiguityPolicy(str,Enum): STOP_FIRST='stop_first'; TARGET_FIRST='target_first'; NEAREST_FIRST='nearest_first'; WORST_CASE='worst_case'; BEST_CASE='best_case'; REJECT='reject_ambiguous'
class GapPolicy(str,Enum): FILL_AT_OPEN='fill_at_open'; FILL_AT_LEVEL='fill_at_level'; WORST_EXECUTABLE='worst_executable'; REJECT='reject_gap'
class PartialFillPriority(str,Enum): FIFO='fifo'; STOP_FIRST='stop_first'; TARGET_FIRST='target_first'; ENTRY_FIRST='entry_first'
class StaleQuotePolicy(str,Enum): REJECT='reject'; HOLD='hold'; USE_LAST='use_last'
class MatrixOverflowPolicy(str,Enum): REJECT='reject'; TRUNCATE_DETERMINISTIC='truncate_deterministic'; SAMPLE_SEEDED='sample_seeded'
class CompilerMode(str,Enum): RESEARCH='research'; MANUAL='manual'; AI_SEARCH='ai_search'; RUNTIME='runtime'
class AccountMode(str,Enum): NETTING='netting'; HEDGING='hedging'; ANY='any'
class MarketMode(str,Enum): EXCHANGE='exchange'; OTC='otc'; ANY='any'
