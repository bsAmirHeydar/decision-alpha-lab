#ifndef __FP_I05_CONTRACTS_MQH__
#define __FP_I05_CONTRACTS_MQH__
#include "FP_I05_Enums.mqh"
struct FP_I05_WindowDescriptor {
 string descriptor_id,pair_id,trading_date,trading_day_id,week_id,calendar_config_hash,source_calendar_window_id;
 FP_I05_WINDOW_KIND kind; long start_utc_ms,end_utc_ms; int expected_minutes;
 bool Valid() const { return descriptor_id!="" && pair_id!="" && end_utc_ms>start_utc_ms && expected_minutes>0 && calendar_config_hash!=""; }
};
struct FP_I05_SymbolWindowAggregate {
 string aggregate_id,descriptor_id,canonical_symbol,source_revision_id,semantic_hash,reason_code;
 FP_I05_WINDOW_STATE state; double open,high,low,close; long high_utc_ms,low_utc_ms;
 int present_minutes,expected_elapsed_minutes,expected_total_minutes,missing_minutes,out_of_coverage_minutes,conflict_minutes;
 bool Valid() const { return aggregate_id!="" && descriptor_id!="" && canonical_symbol!="" && expected_total_minutes>0 && present_minutes>=0 && conflict_minutes>=0 && semantic_hash!=""; }
};
struct FP_I05_PairWindowAggregate {
 string pair_window_id,source_revision_id,semantic_hash,reason_code;
 FP_I05_WindowDescriptor descriptor; FP_I05_SymbolWindowAggregate left,right; FP_I05_HEALTH health;
 bool Complete() const { return left.state==FP_I05_WINDOW_COMPLETE && right.state==FP_I05_WINDOW_COMPLETE; }
 bool Valid() const { return pair_window_id!="" && descriptor.Valid() && left.Valid() && right.Valid() && left.descriptor_id==descriptor.descriptor_id && right.descriptor_id==descriptor.descriptor_id; }
};
struct FP_I05_ReferenceLevel {
 string reference_id,pair_id,canonical_symbol,source_pair_window_id,source_descriptor_id,source_trading_date,source_week_id,source_revision_id,semantic_hash,reason_code;
 FP_I05_REFERENCE_SIDE side; FP_I05_WINDOW_KIND source_window_kind; FP_I05_REFERENCE_STATE state;
 double price; long extreme_utc_ms,created_utc_ms,last_transition_utc_ms; int state_sequence;
 bool ActiveForHunt() const { return state==FP_I05_REF_FRESH || state==FP_I05_REF_HUNTER_SEEN; }
 bool Valid() const { return reference_id!="" && pair_id!="" && canonical_symbol!="" && MathIsValidNumber(price) && extreme_utc_ms>=0 && semantic_hash!=""; }
};
struct FP_I05_CalendarDaySelectionItem {
 int offset; string target_date,pair_window_id,descriptor_id,reason_code,evidence_hash; FP_I05_SELECTOR_DISPOSITION disposition;
 bool Valid() const { return offset>0 && target_date!="" && evidence_hash!=""; }
};
#endif
