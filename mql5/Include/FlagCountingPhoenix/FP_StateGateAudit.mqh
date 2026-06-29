#ifndef __FP_STATE_GATE_AUDIT_MQH__
#define __FP_STATE_GATE_AUDIT_MQH__
#property strict

#include "FP_StateGateRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Audit
// ============================================================================

void FP_PrintStateGateReport(const string tag, const FP_StateGateReport &r)
{
   string msg = tag;
   msg += " version=" + r.version;
   msg += " attempted=" + FP_StateGateBoolName(r.attempted);
   msg += " ok=" + FP_StateGateBoolName(r.ok);
   msg += " status=" + r.status;
   msg += " reason=" + r.reason;
   msg += " symbol=" + r.symbol;
   msg += " tfs=" + IntegerToString(r.timeframe_count);
   msg += " checked=" + IntegerToString(r.slots_checked);
   msg += " available=" + IntegerToString(r.available_timeframes);
   msg += " dirty_tfs=" + IntegerToString(r.dirty_timeframes);
   msg += " unchanged_tfs=" + IntegerToString(r.unchanged_timeframes);
   msg += " unavailable_tfs=" + IntegerToString(r.unavailable_timeframes);
   msg += " rally_rows=" + IntegerToString(r.rally_rows);
   msg += " hook_rows=" + IntegerToString(r.hook_rows);
   msg += " panel_redrawn=" + FP_StateGateBoolName(r.panel_redrawn);
   msg += " export_attempted=" + FP_StateGateBoolName(r.export_attempted);
   msg += " skipped_no_dirty=" + FP_StateGateBoolName(r.skipped_no_dirty);
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
      msg += " status=" + snapshot.tf_states[i].tracker_status;
      msg += " dirty=" + FP_StateGateBoolName(snapshot.tf_states[i].dirty);
      msg += " closed=" + FP_StateGateClosedBarTimeLabel(snapshot.tf_states[i].last_closed_bar_time);
      msg += " prev=" + FP_StateGateClosedBarTimeLabel(snapshot.tf_states[i].previous_closed_bar_time);
      msg += " close=" + FP_StateGateCloseLabel(snapshot.tf_states[i].last_closed_bar_close);
      msg += " updates=" + IntegerToString(snapshot.tf_states[i].update_count);
      msg += " rally=" + snapshot.tf_states[i].latest_established_f_summary;
      msg += " probable=" + snapshot.tf_states[i].probable_next_f_summary;
      msg += " hook=" + snapshot.tf_states[i].hook_summary;
      Print(msg);
   }
}

#endif // __FP_STATE_GATE_AUDIT_MQH__
