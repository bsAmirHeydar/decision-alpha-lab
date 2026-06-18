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


int DAL_M0002ComputeNeutralExitEvents(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Config &config,
   DALM0001Event &events[]
)
{
   ArrayResize(events, 0);

   if(bars_count <= 0 || nodes_count <= 0)
      return 0;

   double log_moves[];
   DAL_M0001BuildLogMoves(bars, bars_count, log_moves);

   int event_id = 0;

   for(int n = 0; n < nodes_count; n++)
   {
      DALLRuleNode node = nodes[n];
      int start = node.active_from_index;

      if(start < 0 || start >= bars_count)
         continue;

      int revisit_id = 0;
      double tracking_extreme = DAL_M0001InitialExtreme(node.type, bars[start]);
      int i = start;

      while(i < bars_count)
      {
         bool in_event = false;
         int entry_index = -1;
         int outside_count = 0;

         double event_extreme = tracking_extreme;
         double event_lower = node.price;
         double event_upper = node.price;

         // H0002 neutral event builder:
         // Wait for a territory touch exactly like M0001, but do NOT consume or
         // discard a node/event when node_price is crossed. Continuation is one
         // of the outcomes under test, so hunt/consume semantics must not filter
         // the sample before reversal/continuation classification.
         for(; i < bars_count; i++)
         {
            tracking_extreme = DAL_M0001UpdateExtreme(node.type, tracking_extreme, bars[i]);

            double live_lower = node.price;
            double live_upper = node.price;
            DAL_M0001Territory(node.type, node.price, tracking_extreme, config.zone_ratio, live_lower, live_upper);

            bool touched_zone = DAL_CandleIntersectsZone(bars[i].low, bars[i].high, live_lower, live_upper);
            if(!touched_zone)
               continue;

            in_event = true;
            entry_index = i;
            outside_count = 0;
            event_extreme = tracking_extreme;
            event_lower = live_lower;
            event_upper = live_upper;
            i++;
            break;
         }

         if(!in_event)
            break;

         // After entry, keep the event alive until exit_gap consecutive candles
         // are fully outside the frozen event zone. Do not stop on hunt/cross.
         // At the completed exit candle, M0002 later classifies close vs node_price.
         for(; i < bars_count; i++)
         {
            tracking_extreme = DAL_M0001UpdateExtreme(node.type, tracking_extreme, bars[i]);

            bool fully_outside_frozen_zone = !DAL_CandleIntersectsZone(
               bars[i].low,
               bars[i].high,
               event_lower,
               event_upper
            );

            if(fully_outside_frozen_zone)
               outside_count++;
            else
               outside_count = 0;

            if(outside_count >= config.exit_gap)
            {
               DALM0001Event event;
               if(DAL_M0001FinalizeEvent(
                     bars,
                     log_moves,
                     node,
                     event_id,
                     revisit_id,
                     entry_index,
                     i,
                     event_lower,
                     event_upper,
                     event_extreme,
                     true,
                     i,
                     false,
                     false,
                     DAL_M0001_CONSUMED_NONE,
                     -1,
                     config.exit_gap,
                     event
                  ))
               {
                  if(event.rtv >= config.min_rtv)
                  {
                     DAL_M0001AppendEvent(events, event);
                     event_id++;
                  }
               }

               revisit_id++;

               // Keep node alive and restart the next territory cycle after the
               // completed event, matching the post-revisit reset architecture but
               // without any hunt/touch consumption branch.
               int next_tracking_index = i + 1;
               if(next_tracking_index < bars_count)
                  tracking_extreme = DAL_M0001InitialExtreme(node.type, bars[next_tracking_index]);

               i++;
               break;
            }
         }

         if(config.max_events > 0 && ArraySize(events) >= config.max_events)
            return ArraySize(events);

         if(i >= bars_count)
            break;
      }
   }

   return ArraySize(events);
}

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

   int sample_len = config.post_outcome_sample_bars;
   if(config.use_event_length_for_sample || sample_len <= 0)
      sample_len = event.rtv_sample_length;
   if(sample_len <= 0)
      return false;

   int sample_start = outcome_index + 1;
   int baseline_start = entry_index - sample_len;
   if(baseline_start < 0)
      return false;

   if(sample_start < 0 || sample_start + sample_len > bars_count)
      return false;

   double before_mean = DAL_M0001MeanLogMoveWindow(bars, bars_count, baseline_start, sample_len);
   double after_mean = DAL_M0001MeanLogMoveWindow(bars, bars_count, sample_start, sample_len);
   if(before_mean <= 0.0 || after_mean <= 0.0)
      return false;

   double rtv = after_mean / before_mean;
   if(rtv <= 0.0 || !DAL_M0001NullValidNumber(rtv))
      return false;

   DALM0001Event pseudo;
   if(!DAL_M0002MakePseudoRandomEvent(sample_id, sample_len, pseudo))
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
            int sample_len = config.post_outcome_sample_bars;
            if(config.use_event_length_for_sample || sample_len <= 0)
               sample_len = events[i].rtv_sample_length;
            if(events[i].entry_index - sample_len < 0)
               audit.skipped_no_baseline++;
            else
               audit.skipped_no_future++;
         }
         continue;
      }

      DAL_M0002AppendSample(all_samples, sample);
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
