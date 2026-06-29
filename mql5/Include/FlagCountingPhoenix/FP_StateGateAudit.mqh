#ifndef __FP_STATE_GATE_AUDIT_MQH__
#define __FP_STATE_GATE_AUDIT_MQH__
#property strict

#include "FP_StateGatePanel.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Audit
// ============================================================================

void FP_PrintStateGateReport(const string tag, const FP_StateGateReport &r)
{
   string msg = tag;
   msg += " version=" + r.version;
   msg += " attempted=" + FP_BoolName(r.attempted);
   msg += " ok=" + FP_BoolName(r.ok);
   msg += " status=" + r.status;
   msg += " reason=" + r.reason;
   msg += " symbol=" + r.symbol;
   msg += " tfs=" + IntegerToString(r.timeframe_count);
   msg += " dirty_tfs=" + IntegerToString(r.dirty_timeframes);
   msg += " rally_rows=" + IntegerToString(r.rally_rows);
   msg += " hook_rows=" + IntegerToString(r.hook_rows);
   msg += " objects=" + IntegerToString(r.objects_created);
   msg += " object_errors=" + IntegerToString(r.object_errors);
   msg += " files=" + IntegerToString(r.files_written);
   msg += " file_errors=" + IntegerToString(r.file_errors);
   Print(msg);
}

void FP_PrintStateGateSnapshotSamples(const string tag,
                                      const FP_StateGateSnapshot &snapshot,
                                      const int limit)
{
   int max_rows = MathMax(0, limit);
   for(int i=0; i<snapshot.timeframe_count && i<max_rows; i++)
   {
      string msg = tag;
      msg += " tf=" + snapshot.tf_states[i].timeframe_label;
      msg += " closed=" + FP_StateGateClosedBarTimeLabel(snapshot.tf_states[i].last_closed_bar_time);
      msg += " close=" + DoubleToString(snapshot.tf_states[i].last_closed_bar_close, _Digits);
      msg += " rally=" + snapshot.tf_states[i].latest_established_f_summary;
      msg += " probable=" + snapshot.tf_states[i].probable_next_f_summary;
      msg += " hook=" + snapshot.tf_states[i].hook_summary;
      Print(msg);
   }
}

#endif // __FP_STATE_GATE_AUDIT_MQH__
