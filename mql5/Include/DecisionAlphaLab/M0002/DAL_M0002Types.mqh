#ifndef __DAL_M0002_TYPES_MQH__
#define __DAL_M0002_TYPES_MQH__

#include <DecisionAlphaLab/Common/DAL_Common.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>

enum ENUM_DALM0002Outcome
{
   DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT = 0,
   DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT = 1,
   DAL_M0002_OUTCOME_UNKNOWN = 2
};

enum ENUM_DALM0002MeasureMode
{
   // H0002 default: classify the completed neutral exit event by node side,
   // then measure the exact same event-window RTV semantics as M0001.
   DAL_M0002_MEASURE_EVENT_RTV = 0,

   // Optional diagnostic: classify at the completed exit candle, but measure
   // a fixed window after the outcome candle. This is not the primary H0002 metric.
   DAL_M0002_MEASURE_POST_OUTCOME_FIXED = 1
};

string DAL_M0002MeasureModeToString(const ENUM_DALM0002MeasureMode mode)
{
   if(mode == DAL_M0002_MEASURE_POST_OUTCOME_FIXED)
      return "POST_OUTCOME_FIXED";
   return "EVENT_RTV";
}

string DAL_M0002OutcomeToString(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return "REVERSAL_AFTER_EXIT";
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return "CONTINUATION_AFTER_EXIT";
   return "UNKNOWN";
}

struct DALM0002Config
{
   ENUM_DALM0002MeasureMode measure_mode;
   int outcome_candle_offset_after_exit;
   int post_outcome_sample_bars;
   bool use_event_length_for_sample;
   int random_samples_per_event;
   int bootstrap_iterations;
   int permutation_iterations;
   int validation_splits;
   int broker_utc_offset_hours;
   int regime_lookback_bars;
   bool print_group_session_regime;
};

struct DALM0002BranchSample
{
   int id;
   int parent_event_id;
   int node_id;
   int revisit_id;
   ENUM_DALM0002Outcome outcome;
   ENUM_DALNodeType node_type;

   int entry_index;
   int exit_index;
   int outcome_index;
   int sample_start_index;
   int sample_length;
   int baseline_start_index;
   int event_rtv_inside_end_index;

   datetime entry_time;
   datetime exit_time;
   datetime outcome_time;
   datetime sample_start_time;

   double node_price;
   double outcome_close;
   double territory_lower;
   double territory_upper;
   double pre_entry_mean;
   double post_mean;
   double event_mean_inside;
   double event_mean_before;
   double event_rtv;
   double event_log;
   double post_outcome_rtv;
   double post_outcome_log;
   double branch_rtv;
   double branch_log;
   double random_log;
   double delta_log;

   double pre_entry_vol;
   int utc_hour;
   int utc_session;
   int trend_regime;
};

struct DALM0002Audit
{
   int source_events;
   int after_start;
   int touch_confirmed;
   int skipped_no_baseline;
   int skipped_no_future;
   int unknown_outcome;
   int continuation_count;
   int reversal_count;
   int paired_count;
   int event_rtv_mode_count;
   int post_outcome_mode_count;
};

void DAL_M0002DefaultConfig(DALM0002Config &config)
{
   config.measure_mode = DAL_M0002_MEASURE_EVENT_RTV;
   config.outcome_candle_offset_after_exit = 0;
   config.post_outcome_sample_bars = 20;
   config.use_event_length_for_sample = false;
   config.random_samples_per_event = 20;
   config.bootstrap_iterations = 300;
   config.permutation_iterations = 500;
   config.validation_splits = 5;
   config.broker_utc_offset_hours = 0;
   config.regime_lookback_bars = 100;
   config.print_group_session_regime = true;
}

void DAL_M0002ResetAudit(DALM0002Audit &audit)
{
   audit.source_events = 0;
   audit.after_start = 0;
   audit.touch_confirmed = 0;
   audit.skipped_no_baseline = 0;
   audit.skipped_no_future = 0;
   audit.unknown_outcome = 0;
   audit.continuation_count = 0;
   audit.reversal_count = 0;
   audit.paired_count = 0;
   audit.event_rtv_mode_count = 0;
   audit.post_outcome_mode_count = 0;
}

#endif
