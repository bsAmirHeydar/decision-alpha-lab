#ifndef __DAL_M0002_ENGINE_MQH__
#define __DAL_M0002_ENGINE_MQH__

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Types.mqh>

int DAL_M0002AppendSample(DALM0002BranchSample &samples[], const DALM0002BranchSample &sample)
{
   int size = ArraySize(samples);
   ArrayResize(samples, size + 1);
   samples[size] = sample;
   return size;
}

bool DAL_M0002IntSeen(const int &values[], const int value)
{
   for(int i = 0; i < ArraySize(values); i++)
   {
      if(values[i] == value)
         return true;
   }
   return false;
}

void DAL_M0002AppendUniqueInt(int &values[], const int value)
{
   if(DAL_M0002IntSeen(values, value))
      return;
   int size = ArraySize(values);
   ArrayResize(values, size + 1);
   values[size] = value;
}

bool DAL_M0002ClassifyReversalContinuation(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count,
   const int exit_index,
   const int outcome_candle_offset_after_exit,
   ENUM_DALM0002Outcome &outcome,
   int &outcome_index
)
{
   outcome = DAL_M0002_OUTCOME_UNKNOWN;
   outcome_index = -1;

   int offset = outcome_candle_offset_after_exit;
   if(offset < 0)
      offset = 0;

   outcome_index = exit_index + offset;
   if(outcome_index < 0 || outcome_index >= bars_count)
      return false;

   double close_price = bars[outcome_index].close;
   if(close_price == event.node_price)
      return false;

   // Correct H0002 semantics:
   // - LOW/valley node: after the completed exit window, close above node => REVERSAL; close below node => CONTINUATION.
   // - HIGH/peak node: after the completed exit window, close below node => REVERSAL; close above node => CONTINUATION.
   // This has no dependency on future hunt/not-hunt state.
   if(event.node_type == DAL_NODE_LOW)
      outcome = close_price > event.node_price ? DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT : DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT;
   else
      outcome = close_price < event.node_price ? DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT : DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT;

   return true;
}

bool DAL_M0002MakePseudoRandomEvent(
   const int sample_id,
   const int sample_length,
   DALM0001Event &pseudo_event
)
{
   if(sample_length <= 0)
      return false;

   pseudo_event.id = sample_id;
   pseudo_event.rtv_sample_length = sample_length;
   return true;
}


// H0002 intentionally does not define a separate neutral event builder.
// Production M0002 receives events from DAL_M0001ComputeEvents() so node
// consumption, touch confirmation, hunt priority, revisit reset, warmup, and
// RTV-window semantics remain identical to H0001.

bool DAL_M0002BuildBranchSample(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const datetime min_entry_time,
   const DALM0002Config &config,
   const int sample_id,
   DALM0002BranchSample &sample,
   ENUM_DALM0002Outcome &outcome
)
{
   outcome = DAL_M0002_OUTCOME_UNKNOWN;

   if(!event.closed)
      return false;
   if(!event.touch_confirmed)
      return false;
   if(!event.rtv_ready)
      return false;
   if(!DAL_M0001EventPassesAnalysisStart(event, min_entry_time))
      return false;

   int entry_index = event.entry_index;
   int exit_index = event.exit_index;
   if(entry_index < 0)
      entry_index = DAL_M0001BarIndexByTime(bars, bars_count, event.entry_time);
   if(exit_index < 0)
      exit_index = event.touch_confirmed_index;
   if(entry_index < 0 || exit_index < 0 || exit_index >= bars_count)
      return false;

   int outcome_index = -1;
   if(!DAL_M0002ClassifyReversalContinuation(event, bars, bars_count, exit_index, config.outcome_candle_offset_after_exit, outcome, outcome_index))
      return false;

   int sample_len = event.rtv_sample_length;
   int sample_start = entry_index;
   int baseline_start = event.rtv_before_start_index;
   double before_mean = event.mean_before;
   double after_mean = event.mean_inside;
   double rtv = event.rtv;
   int inside_end_index = event.rtv_inside_end_index;
   double post_outcome_rtv = 0.0;
   double post_outcome_log = 0.0;

   // Primary H0002 metric:
   // Split the exact M0001 completed-exit event RTV by the node-side outcome
   // observed at the completed exit candle.  The outcome is a label only; it
   // must not change the measured window. This preserves H0001 semantics:
   // entry-window logRTV = mean(entry..inside_end) / mean(before entry), with
   // final exit_gap candles excluded from the inside sample.
   if(config.measure_mode == DAL_M0002_MEASURE_POST_OUTCOME_FIXED)
   {
      sample_len = config.post_outcome_sample_bars;
      if(config.use_event_length_for_sample || sample_len <= 0)
         sample_len = event.rtv_sample_length;
      if(sample_len <= 0)
         return false;

      sample_start = outcome_index + 1;
      baseline_start = entry_index - sample_len;
      inside_end_index = sample_start + sample_len - 1;
      if(baseline_start < 0)
         return false;
      if(sample_start < 0 || sample_start + sample_len > bars_count)
         return false;

      before_mean = DAL_M0001MeanLogMoveWindow(bars, bars_count, baseline_start, sample_len);
      after_mean = DAL_M0001MeanLogMoveWindow(bars, bars_count, sample_start, sample_len);
      if(before_mean <= 0.0 || after_mean <= 0.0)
         return false;

      rtv = after_mean / before_mean;
      if(rtv <= 0.0 || !DAL_M0001NullValidNumber(rtv))
         return false;

      post_outcome_rtv = rtv;
      post_outcome_log = MathLog(rtv);
   }
   else
   {
      if(sample_len <= 0 || baseline_start < 0 || inside_end_index < entry_index)
         return false;
      if(before_mean <= 0.0 || after_mean <= 0.0 || rtv <= 0.0)
         return false;
      if(!DAL_M0001NullValidNumber(rtv))
         return false;
   }

   DALM0001Event pseudo;
   if(!DAL_M0002MakePseudoRandomEvent(event.id, sample_len, pseudo))
      return false;

   double random_log = 0.0;
   if(!DAL_M0001RandomLogForEvent(pseudo, bars, bars_count, analysis_start_index, config.random_samples_per_event, random_log))
      return false;

   sample.id = sample_id;
   sample.parent_event_id = event.id;
   sample.node_id = event.node_id;
   sample.revisit_id = event.revisit_id;
   sample.outcome = outcome;
   sample.node_type = event.node_type;
   sample.entry_index = entry_index;
   sample.exit_index = exit_index;
   sample.outcome_index = outcome_index;
   sample.sample_start_index = sample_start;
   sample.sample_length = sample_len;
   sample.baseline_start_index = baseline_start;
   sample.event_rtv_inside_end_index = inside_end_index;
   sample.entry_time = event.entry_time;
   sample.exit_time = bars[exit_index].time;
   sample.outcome_time = bars[outcome_index].time;
   sample.sample_start_time = bars[sample_start].time;
   sample.node_price = event.node_price;
   sample.outcome_close = bars[outcome_index].close;
   sample.territory_lower = event.territory_lower;
   sample.territory_upper = event.territory_upper;
   sample.pre_entry_mean = before_mean;
   sample.post_mean = after_mean;
   sample.event_mean_inside = event.mean_inside;
   sample.event_mean_before = event.mean_before;
   sample.event_rtv = event.rtv;
   sample.event_log = MathLog(event.rtv);
   sample.post_outcome_rtv = post_outcome_rtv;
   sample.post_outcome_log = post_outcome_log;
   sample.branch_rtv = rtv;
   sample.branch_log = MathLog(rtv);
   sample.random_log = random_log;
   sample.delta_log = sample.branch_log - sample.random_log;
   sample.pre_entry_vol = DAL_M0001PreEntryVol(bars, bars_count, entry_index, config.regime_lookback_bars);
   sample.utc_hour = DAL_M0001UtcHourFromBrokerTime(event.entry_time, config.broker_utc_offset_hours);
   sample.utc_session = DAL_M0001UtcSessionFromHour(sample.utc_hour);
   sample.trend_regime = DAL_M0001PreEntryTrendRegime(bars, bars_count, entry_index, config.regime_lookback_bars);

   return true;
}

int DAL_M0002CollectBranchSamples(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const datetime min_entry_time,
   const DALM0002Config &config,
   DALM0002BranchSample &all_samples[],
   DALM0002BranchSample &reversal_samples[],
   DALM0002BranchSample &continuation_samples[],
   DALM0002Audit &audit
)
{
   ArrayResize(all_samples, 0);
   ArrayResize(reversal_samples, 0);
   ArrayResize(continuation_samples, 0);
   DAL_M0002ResetAudit(audit);

   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);
   int sample_id = 0;
   int unique_node_ids[];
   ArrayResize(unique_node_ids, 0);

   for(int i = 0; i < events_count; i++)
   {
      audit.source_events++;
      if(DAL_M0001EventPassesAnalysisStart(events[i], min_entry_time))
         audit.after_start++;
      if(events[i].touch_confirmed)
         audit.touch_confirmed++;

      ENUM_DALM0002Outcome outcome = DAL_M0002_OUTCOME_UNKNOWN;
      DALM0002BranchSample sample;
      bool ok = DAL_M0002BuildBranchSample(events[i], bars, bars_count, analysis_start_index, min_entry_time, config, sample_id, sample, outcome);

      if(!ok)
      {
         if(events[i].closed && events[i].touch_confirmed && DAL_M0001EventPassesAnalysisStart(events[i], min_entry_time))
         {
            if(!events[i].rtv_ready || events[i].rtv_sample_length <= 0 || events[i].rtv_before_start_index < 0)
               audit.skipped_no_baseline++;
            else
               audit.unknown_outcome++;
         }
         continue;
      }

      DAL_M0002AppendSample(all_samples, sample);
      DAL_M0002AppendUniqueInt(unique_node_ids, sample.node_id);
      if(sample.revisit_id > audit.max_revisit_id)
         audit.max_revisit_id = sample.revisit_id;

      if(config.measure_mode == DAL_M0002_MEASURE_POST_OUTCOME_FIXED)
         audit.post_outcome_mode_count++;
      else
         audit.event_rtv_mode_count++;

      if(sample.outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      {
         DAL_M0002AppendSample(reversal_samples, sample);
         audit.reversal_count++;
      }
      else if(sample.outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      {
         DAL_M0002AppendSample(continuation_samples, sample);
         audit.continuation_count++;
      }
      else
      {
         audit.unknown_outcome++;
      }

      sample_id++;
   }

   audit.paired_count = ArraySize(all_samples);
   audit.unique_node_count = ArraySize(unique_node_ids);
   return audit.paired_count;
}

void DAL_M0002SamplesToM0001Pairs(
   const DALM0002BranchSample &samples[],
   DALM0001PairedLogRtv &pairs[],
   double &branch_logs[],
   double &random_logs[]
)
{
   int count = ArraySize(samples);
   ArrayResize(pairs, count);
   ArrayResize(branch_logs, count);
   ArrayResize(random_logs, count);

   for(int i = 0; i < count; i++)
   {
      pairs[i].event_id = samples[i].id;
      pairs[i].sample_length = samples[i].sample_length;
      pairs[i].entry_time = samples[i].sample_start_time;
      pairs[i].entry_index = samples[i].sample_start_index;
      pairs[i].pre_entry_vol = samples[i].pre_entry_vol;
      pairs[i].utc_hour = samples[i].utc_hour;
      pairs[i].utc_session = samples[i].utc_session;
      pairs[i].trend_regime = samples[i].trend_regime;
      pairs[i].node_log = samples[i].branch_log;
      pairs[i].random_log = samples[i].random_log;
      pairs[i].delta_log = samples[i].delta_log;

      branch_logs[i] = samples[i].branch_log;
      random_logs[i] = samples[i].random_log;
   }
}

void DAL_M0002SamplesToLogs(
   const DALM0002BranchSample &samples[],
   double &logs[]
)
{
   int count = ArraySize(samples);
   ArrayResize(logs, count);
   for(int i = 0; i < count; i++)
      logs[i] = samples[i].branch_log;
}

#endif
