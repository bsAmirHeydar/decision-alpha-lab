#ifndef __EXP0019_FP_I04_COVERAGE_MQH__
#define __EXP0019_FP_I04_COVERAGE_MQH__
#include "FP_I04_DuplicateResolver.mqh"
void FP_I04_BuildCoverage(const string symbol,const datetime start_utc,const datetime end_utc,const int present,const int expected,const int excluded,const int conflicts,FP_I04_CoverageInterval &out)
  { out.canonical_symbol=symbol;out.start_utc=start_utc;out.end_utc=end_utc;out.present_minutes=present;out.expected_minutes=expected;out.calendar_excluded_minutes=excluded;if(conflicts>0){out.state=FP_I04_COVERAGE_CONFLICTED;out.reason_code="FP_DRC_COVERAGE_CONFLICTED";}else if(present==0){out.state=FP_I04_COVERAGE_EMPTY;out.reason_code="FP_DRC_COVERAGE_EMPTY";}else if(present==expected){out.state=FP_I04_COVERAGE_COMPLETE;out.reason_code="FP_DRC_COVERAGE_COMPLETE";}else{out.state=FP_I04_COVERAGE_PARTIAL;out.reason_code="FP_DRC_COVERAGE_PARTIAL";}out.source_revision_hash=FP_I02_CompactId("FPCOVSRC",symbol+"|"+IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc)+"|"+IntegerToString(present)); }
#endif
