from .canonical import canonical_sha256
from .constants import *
CONTRACTS=(
 'SymbolSpec','SymbolPairSpec','M1Bar','DuplicateResolution','CoverageInterval','GapInterval','MinuteCell','AlignedMinute','DataRevision','IncrementalCursor','BackfillRequest','SynchronizationResult','RevisionImpact','SynchronizerConfig','PairDatasetSnapshot'
)
REASONS=(
 'FP_DRC_BAR_UNIQUE','FP_DRC_DUPLICATE_IDENTICAL_DEDUPLICATED','FP_DRC_DUPLICATE_CONFLICT','FP_DRC_M1_PRESENT','FP_DRC_M1_MISSING','FP_DRC_M1_REVISED','FP_DRC_COVERAGE_COMPLETE','FP_DRC_COVERAGE_PARTIAL','FP_DRC_COVERAGE_EMPTY','FP_DRC_COVERAGE_CONFLICTED','FP_DRC_SYNC_READY','FP_DRC_SYNC_DEGRADED','FP_DRC_SYNC_BLOCKED','FP_DRC_REVISION_INITIAL','FP_DRC_REVISION_APPEND','FP_DRC_REVISION_LATE_INSERT','FP_DRC_REVISION_VALUE_CORRECTION','FP_DRC_REVISION_DELETE','FP_DRC_REVISION_NO_CHANGE','FP_DRC_REVISION_CONFLICT','FP_DRC_REVISION_IMPACT_COMPUTED','FP_DRC_BACKFILL_RANGE_PLANNED','FP_DRC_BACKFILL_LIMIT_EXCEEDED','FP_DRC_BACKFILL_BLOCKED_CONFLICT','FP_DRC_CURSOR_REVISION_MISMATCH','FP_DRC_PROVISIONAL_BAR_FORBIDDEN','FP_DRC_PRICE_OFF_TICK_GRID','FP_DRC_CALENDAR_HASH_MISMATCH','FP_DRC_SYMBOL_UNRESOLVED','FP_DRC_BAR_OUTSIDE_PAIR'
)
def contract_registry():
    payload={'phase':'FP-I04','version':KERNEL_VERSION,'contracts':CONTRACTS}
    return {**payload,'contract_count':len(CONTRACTS),'registry_hash':canonical_sha256(payload)}
def reason_registry():
    payload={'phase':'FP-I04','version':KERNEL_VERSION,'reasons':REASONS}
    return {**payload,'reason_count':len(REASONS),'registry_hash':canonical_sha256(payload)}
