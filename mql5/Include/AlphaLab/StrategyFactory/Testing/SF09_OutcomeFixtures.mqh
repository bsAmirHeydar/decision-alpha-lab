#ifndef __SF09_OUTCOME_FIXTURES_MQH__
#define __SF09_OUTCOME_FIXTURES_MQH__
#include "../Outcome/SF09_AllOutcome.mqh"

SF01_MarketTimestamp SF09_FixtureTime(const long ms)
{
   SF01_MarketTimestamp t;t.utc_epoch_milliseconds=ms;t.source_timezone_id="UTC";t.source_utc_offset_minutes=0;t.source_clock_id="fixture";t.precision=SF01_TIME_PRECISION_MILLISECONDS;return t;
}

SF08_TradeCandidate SF09_FixtureCandidate(const string id,const ENUM_SF08_ORDER_KIND kind,const double entry,const double stop,const double target,const double partial=0.0)
{
   SF08_TradeCandidate c;c.schema="alpha_lab.strategy_factory/trade_candidate@1.0.0";c.candidate_id="";c.template_id="sf09_fixture";c.template_hash="ctpl_fixture";
   c.event_id="evt_sf09";c.snapshot_id="snap_sf09";c.context_frame_id="ctx_sf09";c.strategy_id="sf09_fixture";c.strategy_version="1.0.0";
   c.symbol="EURUSD";c.direction=SF01_DIRECTION_LONG;c.runtime_generation_id=9;c.created_at=SF09_FixtureTime(1000);
   c.entry.order_kind=kind;c.entry.requested_price=entry;c.entry.activation_time=SF09_FixtureTime(1000);c.entry.expiration_time=SF09_FixtureTime(5000);
   c.entry.maximum_fill_delay_milliseconds=0;c.entry.maximum_slippage_points=0.0;c.entry.geometry_hash=SF08_DeriveEntryPlanHash(c.entry);
   c.stop.has_price_stop=true;c.stop.stop_price=stop;c.stop.has_time_invalidation=false;c.stop.invalidation_time=SF09_FixtureTime(0);
   c.stop.initial_risk_points=entry-stop;c.stop.geometry_hash=SF08_DeriveStopPlanHash(c.stop);
   c.exit_plan.exit_kind=SF08_EXIT_PRICE_OR_TIME;c.exit_plan.has_price_target=true;c.exit_plan.target_price=target;c.exit_plan.maximum_holding_milliseconds=10000;
   c.exit_plan.planned_reward_points=target-entry;c.exit_plan.partial_fraction=partial;c.exit_plan.geometry_hash=SF08_DeriveExitPlanHash(c.exit_plan);
   c.planned_r_multiple=c.exit_plan.planned_reward_points/c.stop.initial_risk_points;c.source_hash="src_sf09";c.status=SF08_CANDIDATE_VALID;c.candidate_id=SF08_DeriveTradeCandidateId(c);
   return c;
}

SF09_PriceObservation SF09_FixtureBar(const long seq,const long time,const double open,const double high,const double low,const double close)
{
   SF09_PriceObservation o;o.observation_id="";o.symbol="EURUSD";o.kind=SF09_OBSERVATION_CLOSED_BAR;o.fidelity=SF09_FIDELITY_BAR_APPROXIMATION;
   o.sequence=seq;o.interval_open=SF09_FixtureTime(time-1000);o.interval_close=SF09_FixtureTime(time);o.observed_at=SF09_FixtureTime(time);
   o.open_price=open;o.high_price=high;o.low_price=low;o.close_price=close;o.has_bid_ask=false;o.bid_price=0.0;o.ask_price=0.0;o.spread_points=0.0001;o.source_hash="src_bar";
   o.observation_id=SF09_DerivePriceObservationId(o);return o;
}

#endif
