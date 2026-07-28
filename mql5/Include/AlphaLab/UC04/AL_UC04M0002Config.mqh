#ifndef __AL_UC04_M0002_CONFIG_MQH__
#define __AL_UC04_M0002_CONFIG_MQH__

#include <M0002/DAL_M0002Types.mqh>

void AL_UC04BuildM0002Config(
   DALM0002Config &config,
   const int outcome_candle_offset_after_exit,
   const int broker_utc_offset_hours,
   const int regime_lookback_bars,
   const ENUM_DALM0001ConsumeMode consume_mode
)
{
   DAL_M0002DefaultConfig(config);
   config.measure_mode = DAL_M0002_MEASURE_EVENT_RTV;
   config.outcome_candle_offset_after_exit = MathMax(0, outcome_candle_offset_after_exit);
   config.post_outcome_sample_bars = 0;
   config.use_event_length_for_sample = false;
   config.random_samples_per_event = 1;
   config.bootstrap_iterations = 0;
   config.permutation_iterations = 0;
   config.validation_splits = 1;
   config.broker_utc_offset_hours = broker_utc_offset_hours;
   config.regime_lookback_bars = MathMax(1, regime_lookback_bars);
   config.print_group_session_regime = false;
   config.run_stress_suite = false;
   config.hard_random_candidates = 1;
   config.placebo_shift_bars = 1;
   config.nonoverlap_gap_bars = 0;
   config.block_bootstrap_iterations = 0;
   config.block_bootstrap_block_pairs = 1;
   config.consume_mode = consume_mode;
   config.consume_on_touch = (consume_mode == DAL_M0001_CONSUME_BY_TOUCH);
}

#endif
