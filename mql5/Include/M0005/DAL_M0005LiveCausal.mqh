#ifndef __DAL_M0005_LIVE_CAUSAL_MQH__
#define __DAL_M0005_LIVE_CAUSAL_MQH__

#include <M0004/DAL_M0004Reports.mqh>

#define DAL_H5_REGIME_UNKNOWN -1
#define DAL_H5_REGIME_REVERSAL 0
#define DAL_H5_REGIME_CONTINUATION 1
#define DAL_H5_REGIME_AMBIGUOUS 2

struct DALM0005CausalRegimeState
{
   bool valid;
   bool ambiguous_energy;
   bool ambiguous_direction;
   int energy;
   int direction;
   int known_index;
   datetime known_time;
   int batch_count;
   int reversal_count;
   int continuation_count;
   int buy_direction_count;
   int sell_direction_count;
   int mixed_batch_count;
   int same_bar_batch_count;
   string reason;
};

void DAL_M0005ResetCausalRegimeState(DALM0005CausalRegimeState &s)
{
   s.valid = false;
   s.ambiguous_energy = false;
   s.ambiguous_direction = false;
   s.energy = DAL_H5_REGIME_UNKNOWN;
   s.direction = 0;
   s.known_index = -1;
   s.known_time = 0;
   s.batch_count = 0;
   s.reversal_count = 0;
   s.continuation_count = 0;
   s.buy_direction_count = 0;
   s.sell_direction_count = 0;
   s.mixed_batch_count = 0;
   s.same_bar_batch_count = 0;
   s.reason = "not_built";
}

string DAL_M0005CausalEnergyToString(const int energy)
{
   if(energy == DAL_H5_REGIME_REVERSAL) return "REVERSAL";
   if(energy == DAL_H5_REGIME_CONTINUATION) return "CONTINUATION";
   if(energy == DAL_H5_REGIME_AMBIGUOUS) return "AMBIGUOUS";
   return "UNKNOWN";
}

string DAL_M0005CausalDirectionToString(const int direction)
{
   if(direction > 0) return "BUY";
   if(direction < 0) return "SELL";
   return "AMBIGUOUS_OR_NONE";
}

int DAL_M0005CausalEnergyFromOutcome(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return DAL_H5_REGIME_REVERSAL;
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return DAL_H5_REGIME_CONTINUATION;
   return DAL_H5_REGIME_UNKNOWN;
}

int DAL_M0005CausalDirectionFromSample(const DALM0002BranchSample &sample, const int energy)
{
   bool low = (sample.node_type == DAL_NODE_LOW);
   if(energy == DAL_H5_REGIME_REVERSAL)
      return low ? +1 : -1;
   if(energy == DAL_H5_REGIME_CONTINUATION)
      return low ? -1 : +1;
   return 0;
}

int DAL_M0005CausalKnownIndex(const DALM0002BranchSample &sample)
{
   if(sample.outcome_index >= 0)
      return sample.outcome_index;
   if(sample.exit_index >= 0)
      return sample.exit_index;
   return sample.entry_index;
}

// Build the latest regime that was knowable by decision_index.  All samples
// whose outcome/known index is the same candle are treated as one simultaneous
// batch.  This prevents a fake sequence when several highs/lows are confirmed
// on the same candle.
bool DAL_M0005BuildLatestCausalRegimeState(
   const DALM0002BranchSample &samples[],
   const int sample_count,
   const DALBar &bars[],
   const int bars_count,
   const int decision_index,
   DALM0005CausalRegimeState &state
)
{
   DAL_M0005ResetCausalRegimeState(state);
   state.reason = "no_known_sample";

   if(sample_count <= 0 || bars_count <= 0 || decision_index < 0)
      return false;

   int latest_known = -1;
   for(int i = 0; i < sample_count; i++)
   {
      int known = DAL_M0005CausalKnownIndex(samples[i]);
      if(known < 0 || known > decision_index)
         continue;
      if(known > latest_known)
         latest_known = known;
   }

   if(latest_known < 0)
      return false;

   int rev = 0;
   int cont = 0;
   int buy = 0;
   int sell = 0;
   int batch = 0;

   for(int j = 0; j < sample_count; j++)
   {
      int known_j = DAL_M0005CausalKnownIndex(samples[j]);
      if(known_j != latest_known)
         continue;

      int e = DAL_M0005CausalEnergyFromOutcome(samples[j].outcome);
      if(e == DAL_H5_REGIME_UNKNOWN)
         continue;

      batch++;
      if(e == DAL_H5_REGIME_REVERSAL)
         rev++;
      else if(e == DAL_H5_REGIME_CONTINUATION)
         cont++;

      int dir = DAL_M0005CausalDirectionFromSample(samples[j], e);
      if(dir > 0)
         buy++;
      else if(dir < 0)
         sell++;
   }

   if(batch <= 0)
      return false;

   state.known_index = latest_known;
   state.known_time = (latest_known >= 0 && latest_known < bars_count ? bars[latest_known].time : 0);
   state.batch_count = batch;
   state.reversal_count = rev;
   state.continuation_count = cont;
   state.buy_direction_count = buy;
   state.sell_direction_count = sell;
   state.same_bar_batch_count = (batch > 1 ? 1 : 0);

   if(rev > 0 && cont > 0)
   {
      state.valid = false;
      state.ambiguous_energy = true;
      state.energy = DAL_H5_REGIME_AMBIGUOUS;
      state.mixed_batch_count = 1;
      state.reason = "same_candle_mixed_reversal_continuation_batch";
      return false;
   }

   if(rev > 0)
      state.energy = DAL_H5_REGIME_REVERSAL;
   else if(cont > 0)
      state.energy = DAL_H5_REGIME_CONTINUATION;
   else
      state.energy = DAL_H5_REGIME_UNKNOWN;

   if(buy > 0 && sell > 0)
   {
      state.ambiguous_direction = true;
      state.direction = 0;
   }
   else if(buy > 0)
      state.direction = +1;
   else if(sell > 0)
      state.direction = -1;
   else
      state.direction = 0;

   state.valid = (state.energy == DAL_H5_REGIME_REVERSAL || state.energy == DAL_H5_REGIME_CONTINUATION);
   state.reason = (state.valid ? "ok_causal_same_bar_batch_respected" : "unknown_energy");
   return state.valid;
}

#endif
