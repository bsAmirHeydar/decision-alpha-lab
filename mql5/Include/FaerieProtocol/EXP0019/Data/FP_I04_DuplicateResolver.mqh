#ifndef __EXP0019_FP_I04_DUPLICATE_RESOLVER_MQH__
#define __EXP0019_FP_I04_DUPLICATE_RESOLVER_MQH__
#include "FP_I04_BarValidation.mqh"
bool FP_I04_ResolveTwoBars(const FP_I04_M1Bar &a,const FP_I04_M1Bar &b,FP_I04_DuplicateResolution &out)
  { out.canonical_symbol=a.canonical_symbol;out.open_utc=a.open_utc;string ha=FP_I04_BarHash(a),hb=FP_I04_BarHash(b);out.input_hashes_csv=(ha<hb?ha+","+hb:hb+","+ha);if(a.canonical_symbol!=b.canonical_symbol||a.open_utc!=b.open_utc){out.disposition=FP_I04_DUP_CONFLICT;out.has_selected_bar=false;out.reason_code="FP_DRC_DUPLICATE_KEY_MISMATCH";return false;}if(ha!=hb){out.disposition=FP_I04_DUP_CONFLICT;out.has_selected_bar=false;out.reason_code="FP_DRC_DUPLICATE_CONFLICT";out.evidence_hash=FP_I02_CompactId("FPDUP",out.input_hashes_csv);return false;}out.disposition=FP_I04_DUP_IDENTICAL_DEDUPLICATED;if(a.source_sequence>=b.source_sequence)out.selected_bar=a;else out.selected_bar=b;out.has_selected_bar=true;out.reason_code="FP_DRC_DUPLICATE_IDENTICAL_DEDUPLICATED";out.evidence_hash=FP_I02_CompactId("FPDUP",out.input_hashes_csv+"|"+IntegerToString(out.selected_bar.source_sequence));return true; }
#endif
