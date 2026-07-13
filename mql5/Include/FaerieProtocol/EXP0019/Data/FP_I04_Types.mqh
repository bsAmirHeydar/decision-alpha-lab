#ifndef __EXP0019_FP_I04_TYPES_MQH__
#define __EXP0019_FP_I04_TYPES_MQH__
#include "FP_I04_Enums.mqh"
#define FP_I04_VERSION "1.0.0"
#define FP_I04_M1_SECONDS 60
struct FP_I04_SymbolSpec { string canonical_symbol; string aliases_csv; double tick_size; int digits; string spec_hash; };
struct FP_I04_SymbolPair { string context_id; string pair_id; FP_I04_SymbolSpec left; FP_I04_SymbolSpec right; string pair_hash; };
struct FP_I04_M1Bar { string canonical_symbol; datetime open_utc; double open; double high; double low; double close; long tick_volume; long real_volume; int spread_points; FP_I04_BarFinality finality; string source_id; long source_sequence; string source_revision; datetime received_utc; string bar_hash; };
struct FP_I04_DuplicateResolution { string canonical_symbol; datetime open_utc; FP_I04_DuplicateDisposition disposition; FP_I04_M1Bar selected_bar; bool has_selected_bar; string input_hashes_csv; string reason_code; string evidence_hash; };
struct FP_I04_CoverageInterval { string canonical_symbol; datetime start_utc; datetime end_utc; int present_minutes; int expected_minutes; int calendar_excluded_minutes; FP_I04_CoverageState state; string source_revision_hash; string reason_code; };
struct FP_I04_MinuteCell { string canonical_symbol; datetime open_utc; FP_I04_MinuteCellState state; FP_I04_M1Bar bar; bool has_bar; string reason_code; string source_revision_hash; };
struct FP_I04_AlignedMinute { string pair_id; datetime open_utc; FP_I04_MinuteCell left; FP_I04_MinuteCell right; string calendar_segment; string calendar_snapshot_hash; string row_id; };
struct FP_I04_DataRevision { string revision_id; string pair_id; string parent_revision_id; FP_I04_RevisionKind kind; string changed_symbols_csv; datetime affected_start_utc; datetime affected_end_utc; string previous_payload_hash; string current_payload_hash; datetime created_utc; string reason_code; };
struct FP_I04_IncrementalCursor { string pair_id; datetime last_emitted_open_utc; long left_last_source_sequence; long right_last_source_sequence; string data_revision_id; FP_I04_CursorState state; string cursor_id; };
struct FP_I04_BackfillRequest { string request_id; string canonical_symbol; datetime start_utc; datetime end_utc; int requested_minutes; FP_I04_BackfillAction action; string reason_code; int priority; };
struct FP_I04_SyncResult { string result_id; string pair_id; datetime start_utc; datetime end_utc; int row_count; int both_present_count; int gap_count; int conflict_count; FP_I04_SyncHealth health; string semantic_hash; string revision_id; };
struct FP_I04_SelfTestResult { int check_count; int pass_count; int fail_count; string latest_failed_check; string evidence_key; };
#endif
