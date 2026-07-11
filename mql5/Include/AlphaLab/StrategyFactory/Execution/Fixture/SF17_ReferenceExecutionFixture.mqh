#ifndef __SF17_REFERENCE_EXECUTION_FIXTURE_MQH__
#define __SF17_REFERENCE_EXECUTION_FIXTURE_MQH__
#include "../SF17_PaperExecutionEngine.mqh"
SF17_ExecutionPolicy SF17_ReferencePolicy(){SF17_ExecutionPolicy p;p.policy_id="paper-reference";p.policy_version="1.0.0";p.mode=SF17_MODE_PAPER;p.point=0.01;p.adverse_slippage_points=1.0;p.commission_per_lot_per_side=2.5;p.max_fill_volume_per_quote=0.5;p.maximum_quote_age_milliseconds=1000;p.allow_research_only_intents=false;p.allow_partial_fills=true;p.fill_market_on_next_quote=true;p.deterministic_seed=1701;p.policy_hash=SF17_DerivePolicyHash(p);return p;}
SF17_QuoteObservation SF17_ReferenceQuote(const double bid,const double ask,const long time,const long sequence){SF17_QuoteObservation q;q.symbol="TEST";q.bid=bid;q.ask=ask;q.time_utc_msc=time;q.sequence=sequence;q.source="fixture";return q;}
#endif
