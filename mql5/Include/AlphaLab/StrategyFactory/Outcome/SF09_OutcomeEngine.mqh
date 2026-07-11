#ifndef __SF09_OUTCOME_ENGINE_MQH__
#define __SF09_OUTCOME_ENGINE_MQH__
#include "SF09_CandidateRuntime.mqh"
#include "SF09_OutcomeQueue.mqh"
#include "SF09_CostRegistry.mqh"
#include "SF09_OutcomeTelemetry.mqh"

class CSF09OutcomeEngine
{
private:
   CSF09CandidateRuntime *m_active[SF09_MAX_ACTIVE_CANDIDATES];
   int m_capacity;
   SF09_SimulationPolicy m_policy;
   CSF09CostRegistry *m_cost_registry;
   string m_cost_model_id;
   string m_cost_model_version;
   CSF09OutcomeQueue m_outcomes;
   SF09_OutcomeTelemetry m_telemetry;

   double ConservativeCurrentPrice(const SF09_PriceObservation &o,const ENUM_SF01_DIRECTION direction,const bool entry) const
   {
      if(o.has_bid_ask)
      {
         if(entry)return (direction==SF01_DIRECTION_LONG)?o.ask_price:o.bid_price;
         return (direction==SF01_DIRECTION_LONG)?o.bid_price:o.ask_price;
      }
      return o.open_price;
   }
   bool EntryTouched(const SF08_TradeCandidate &c,const SF09_PriceObservation &o,double &fill_price) const
   {
      const double p=c.entry.requested_price;
      if(c.entry.order_kind==SF08_ORDER_MARKET)
      {
         fill_price=(m_policy.market_fill_policy==SF09_MARKET_FILL_AT_REQUESTED_PRICE)?p:ConservativeCurrentPrice(o,c.direction,true);
         return true;
      }
      if(c.entry.order_kind==SF08_ORDER_LIMIT)
      {
         const bool touched=(c.direction==SF01_DIRECTION_LONG)?(o.low_price<=p):(o.high_price>=p);
         if(!touched)return false;
         fill_price=p;
         if(m_policy.allow_limit_price_improvement)
         {
            if(c.direction==SF01_DIRECTION_LONG)fill_price=MathMin(p,o.open_price);
            else fill_price=MathMax(p,o.open_price);
         }
         return true;
      }
      if(c.entry.order_kind==SF08_ORDER_STOP)
      {
         const bool touched=(c.direction==SF01_DIRECTION_LONG)?(o.high_price>=p):(o.low_price<=p);
         if(!touched)return false;
         fill_price=p;
         if(m_policy.allow_stop_gap_slippage)
         {
            if(c.direction==SF01_DIRECTION_LONG)fill_price=MathMax(p,o.open_price);
            else fill_price=MathMin(p,o.open_price);
         }
         return true;
      }
      return false;
   }
   bool StopTouched(CSF09CandidateRuntime *r,const SF09_PriceObservation &o) const
   {
      if(!r.candidate.stop.has_price_stop)return false;
      return (r.candidate.direction==SF01_DIRECTION_LONG)?(o.low_price<=r.candidate.stop.stop_price):(o.high_price>=r.candidate.stop.stop_price);
   }
   bool TargetTouched(CSF09CandidateRuntime *r,const SF09_PriceObservation &o) const
   {
      if(r.target_consumed||!r.candidate.exit_plan.has_price_target)return false;
      return (r.candidate.direction==SF01_DIRECTION_LONG)?(o.high_price>=r.candidate.exit_plan.target_price):(o.low_price<=r.candidate.exit_plan.target_price);
   }
   double SignedPoints(CSF09CandidateRuntime *r,const double exit_price) const
   {return (r.candidate.direction==SF01_DIRECTION_LONG)?(exit_price-r.fill_price):(r.fill_price-exit_price);}
   bool Finalize(CSF09CandidateRuntime *r,const ENUM_SF09_RUNTIME_STATE terminal_state,const ENUM_SF09_EXIT_REASON reason,
                 const SF01_MarketTimestamp &exit_time,const double exit_price,const double exit_spread_points,string &error)
   {
      SF09_OutcomeRecord o;
      o.schema="alpha_lab.strategy_factory/outcome_record@1.0.0";o.outcome_id="";
      o.candidate_id=r.candidate.candidate_id;o.event_id=r.candidate.event_id;o.strategy_id=r.candidate.strategy_id;o.symbol=r.candidate.symbol;
      o.direction=r.candidate.direction;o.terminal_state=terminal_state;o.exit_reason=reason;o.fidelity=r.fidelity;
      o.filled=r.filled;o.ambiguous=r.ambiguity_seen;o.partial_exit_used=(r.remaining_fraction<1.0);
      o.registered_at=r.registered_at;o.fill_time=r.fill_time;o.fill_price=r.fill_price;o.exit_time=exit_time;o.exit_price=exit_price;
      o.remaining_fraction=0.0;
      double final_points=r.realized_weighted_points;
      if(r.filled && r.remaining_fraction>0.0)final_points+=r.remaining_fraction*SignedPoints(r,exit_price);
      o.gross_points=final_points;
      o.gross_r=r.filled?final_points/r.candidate.stop.initial_risk_points:0.0;
      o.mfe_points=r.path.MFEPoints();o.mae_points=r.path.MAEPoints();o.mfe_r=r.path.MFER();o.mae_r=r.path.MAER();
      o.holding_milliseconds=r.filled?(exit_time.utc_epoch_milliseconds-r.fill_time.utc_epoch_milliseconds):0;
      o.time_to_fill_milliseconds=r.filled?(r.fill_time.utc_epoch_milliseconds-r.registered_at.utc_epoch_milliseconds):0;
      o.simulation_policy_hash=m_policy.policy_hash;o.cost_registry_hash=(m_cost_registry==NULL)?"none":m_cost_registry.RegistryHash();
      o.path_hash=r.path.PathHash();o.source_hash=r.candidate.source_hash;
      SF09_CostBreakdown costs;
      if(r.filled)
      {
         ISF09CostModel *model=(m_cost_registry==NULL)?NULL:m_cost_registry.Resolve(m_cost_model_id,m_cost_model_version);
         if(model==NULL){error="cost model not found";m_telemetry.cost_failures++;return false;}
         SF09_CostRequest req;req.candidate_id=r.candidate.candidate_id;req.direction=r.candidate.direction;req.entry_price=r.fill_price;req.exit_price=exit_price;
         req.initial_risk_points=r.candidate.stop.initial_risk_points;req.observed_entry_spread_points=r.entry_spread_points;
         req.observed_exit_spread_points=exit_spread_points;req.point_size=1.0;
         if(!model.Compute(req,costs,error)){m_telemetry.cost_failures++;return false;}
      }
      else
      {
         costs.model_id=m_cost_model_id;costs.model_version=m_cost_model_version;costs.entry_spread_points=0.0;costs.exit_spread_points=0.0;
         costs.entry_slippage_points=0.0;costs.exit_slippage_points=0.0;costs.commission_r=0.0;costs.other_r=0.0;costs.total_cost_points=0.0;costs.total_cost_r=0.0;
         costs.cost_hash=SF09_DeriveCostHash(costs);
      }
      o.costs=costs;o.net_r=o.gross_r-costs.total_cost_r;o.outcome_id=SF09_DeriveOutcomeId(o);
      if(!SF09_ValidateOutcomeRecord(o,error))return false;
      if(!m_outcomes.Push(o,error))return false;
      r.state=terminal_state;m_telemetry.terminal_outcomes++;error="";return true;
   }
public:
   CSF09OutcomeEngine(void){m_capacity=SF09_MAX_ACTIVE_CANDIDATES;m_cost_registry=NULL;m_cost_model_id="";m_cost_model_version="";for(int i=0;i<SF09_MAX_ACTIVE_CANDIDATES;i++)m_active[i]=NULL;SF09_ResetTelemetry(m_telemetry);}
   ~CSF09OutcomeEngine(void){for(int i=0;i<SF09_MAX_ACTIVE_CANDIDATES;i++){if(CheckPointer(m_active[i])!=POINTER_INVALID){delete m_active[i];m_active[i]=NULL;}}}
   bool Configure(const int capacity,const SF09_SimulationPolicy &policy,CSF09CostRegistry *cost_registry,
                  const string cost_model_id,const string cost_model_version,string &error)
   {
      if(capacity<=0||capacity>SF09_MAX_ACTIVE_CANDIDATES){error="invalid outcome engine capacity";return false;}
      if(!SF09_ValidateSimulationPolicy(policy,error)||cost_registry==NULL||cost_registry.Resolve(cost_model_id,cost_model_version)==NULL)
      {if(error=="")error="invalid cost registry or model";return false;}
      m_capacity=capacity;m_policy=policy;m_cost_registry=cost_registry;m_cost_model_id=cost_model_id;m_cost_model_version=cost_model_version;
      if(!m_outcomes.Configure(capacity,SF09_QUEUE_FAIL_ENGINE,error))return false;
      error="";return true;
   }
   bool RegisterCandidate(const SF08_TradeCandidate &candidate,const SF01_MarketTimestamp &registered_at,string &error)
   {
      if(!SF08_ValidateTradeCandidate(candidate,error)||!SF01_ValidateTimestamp(registered_at,error))return false;
      int slot=-1;
      for(int i=0;i<m_capacity;i++)
      {
         if(CheckPointer(m_active[i])!=POINTER_INVALID)
         {
            if(m_active[i].candidate.candidate_id==candidate.candidate_id&&!SF09_IsTerminalState(m_active[i].state))
            {error="duplicate active candidate";return false;}
            if(SF09_IsTerminalState(m_active[i].state)&&slot<0)slot=i;
         }
         else if(slot<0)slot=i;
      }
      if(slot<0){error="active candidate capacity reached";return false;}
      if(CheckPointer(m_active[slot])!=POINTER_INVALID){delete m_active[slot];m_active[slot]=NULL;}
      CSF09CandidateRuntime *r=new CSF09CandidateRuntime();
      if(CheckPointer(r)==POINTER_INVALID){error="candidate runtime allocation failed";return false;}
      r.candidate=candidate;r.state=SF09_STATE_REGISTERED;r.registered_at=registered_at;
      if(!r.path.Initialize(candidate.direction,candidate.entry.requested_price,candidate.stop.initial_risk_points,m_policy.maximum_path_events,error)){delete r;return false;}
      if(!r.path.Append(SF09_PATH_REGISTERED,registered_at,candidate.entry.requested_price,0.0,0.0,error)){delete r;return false;}
      m_active[slot]=r;m_telemetry.registered++;error="";return true;
   }
   bool ProcessObservation(const SF09_PriceObservation &o,string &error)
   {
      if(!SF09_ValidatePriceObservation(o,error))return false;m_telemetry.observations++;
      for(int i=0;i<m_capacity;i++)
      {
         CSF09CandidateRuntime *r=m_active[i];
         if(CheckPointer(r)==POINTER_INVALID)continue;
         if(SF09_IsTerminalState(r.state)||r.candidate.symbol!=o.symbol)continue;
         if(r.last_observation_sequence==o.sequence){m_telemetry.duplicate_observations++;continue;}
         if(m_policy.strict_monotonic_observations&&r.last_observation_sequence>=0&&o.sequence<r.last_observation_sequence)
         {m_telemetry.out_of_order_rejections++;error="out-of-order observation";return false;}
         r.last_observation_sequence=o.sequence;r.last_observation_time=o.observed_at;r.fidelity=o.fidelity;
         const long now=o.observed_at.utc_epoch_milliseconds;
         if(!r.filled)
         {
            if(now<r.candidate.entry.activation_time.utc_epoch_milliseconds){r.state=SF09_STATE_WAITING_ACTIVATION;continue;}
            if(now>r.candidate.entry.expiration_time.utc_epoch_milliseconds)
            {
               if(!r.path.Append(SF09_PATH_EXPIRED,o.observed_at,o.close_price,0.0,0.0,error))return false;
               if(!Finalize(r,SF09_STATE_EXPIRED,SF09_EXIT_ENTRY_EXPIRED,o.observed_at,o.close_price,0.0,error))return false;
               m_telemetry.expirations++;m_telemetry.no_fills++;continue;
            }
            r.state=SF09_STATE_PENDING_FILL;double fill=0.0;
            if(!EntryTouched(r.candidate,o,fill))continue;
            r.filled=true;r.state=SF09_STATE_FILLED;r.fill_time=o.observed_at;r.fill_price=fill;r.entry_spread_points=o.spread_points;
            if(!r.path.Initialize(r.candidate.direction,fill,r.candidate.stop.initial_risk_points,m_policy.maximum_path_events,error))return false;
            if(!r.path.Append(SF09_PATH_FILLED,o.observed_at,fill,0.0,0.0,error))return false;m_telemetry.fills++;
         }
         if(!r.path.Update(o,error)){m_telemetry.path_overflows++;return false;}
         const bool stop=StopTouched(r,o);const bool target=TargetTouched(r,o);
         if(stop&&target)
         {
            r.ambiguity_seen=true;m_telemetry.ambiguities++;
            if(m_policy.ambiguity_policy==SF09_AMBIGUITY_EXCLUDE||m_policy.ambiguity_policy==SF09_AMBIGUITY_REQUIRE_LOWER_FIDELITY)
            {
               if(!r.path.Append(SF09_PATH_AMBIGUOUS,o.observed_at,o.close_price,r.path.MFEPoints(),r.path.MAEPoints(),error))return false;
               if(!Finalize(r,SF09_STATE_AMBIGUOUS,SF09_EXIT_AMBIGUOUS_BAR,o.observed_at,o.close_price,o.spread_points,error))return false;
               continue;
            }
         }
         const bool resolve_stop=stop&&(!target||m_policy.ambiguity_policy==SF09_AMBIGUITY_STOP_FIRST);
         const bool resolve_target=target&&(!stop||m_policy.ambiguity_policy==SF09_AMBIGUITY_TARGET_FIRST);
         if(resolve_stop)
         {
            if(!r.path.Append(SF09_PATH_STOP_TOUCH,o.observed_at,r.candidate.stop.stop_price,r.path.MFEPoints(),r.path.MAEPoints(),error))return false;
            ENUM_SF09_EXIT_REASON reason=(r.remaining_fraction<1.0)?SF09_EXIT_PARTIAL_TARGET_THEN_STOP:SF09_EXIT_STOP;
            if(!Finalize(r,SF09_STATE_CLOSED,reason,o.observed_at,r.candidate.stop.stop_price,o.spread_points,error))return false;
            m_telemetry.stops++;continue;
         }
         if(resolve_target)
         {
            if(!r.path.Append(SF09_PATH_TARGET_TOUCH,o.observed_at,r.candidate.exit_plan.target_price,r.path.MFEPoints(),r.path.MAEPoints(),error))return false;
            const double pf=r.candidate.exit_plan.partial_fraction;
            if(pf>0.0&&pf<1.0)
            {
               r.realized_weighted_points+=pf*SignedPoints(r,r.candidate.exit_plan.target_price);r.remaining_fraction-=pf;r.target_consumed=true;r.state=SF09_STATE_PARTIAL;
               if(!r.path.Append(SF09_PATH_PARTIAL_EXIT,o.observed_at,r.candidate.exit_plan.target_price,r.path.MFEPoints(),r.path.MAEPoints(),error))return false;
               m_telemetry.partial_exits++;continue;
            }
            if(!Finalize(r,SF09_STATE_CLOSED,SF09_EXIT_TARGET,o.observed_at,r.candidate.exit_plan.target_price,o.spread_points,error))return false;
            m_telemetry.targets++;continue;
         }
         const long held=now-r.fill_time.utc_epoch_milliseconds;
         const bool stop_time=r.candidate.stop.has_time_invalidation&&now>=r.candidate.stop.invalidation_time.utc_epoch_milliseconds;
         const bool exit_time=r.candidate.exit_plan.maximum_holding_milliseconds>0&&held>=r.candidate.exit_plan.maximum_holding_milliseconds;
         if(stop_time||exit_time)
         {
            const double px=ConservativeCurrentPrice(o,r.candidate.direction,false);
            if(!r.path.Append(SF09_PATH_TIME_EXIT,o.observed_at,px,r.path.MFEPoints(),r.path.MAEPoints(),error))return false;
            ENUM_SF09_EXIT_REASON reason=(r.remaining_fraction<1.0)?SF09_EXIT_PARTIAL_TARGET_THEN_TIME:SF09_EXIT_TIME;
            if(!Finalize(r,SF09_STATE_CLOSED,reason,o.observed_at,px,o.spread_points,error))return false;
            m_telemetry.time_exits++;continue;
         }
      }
      error="";return true;
   }
   bool PopOutcome(SF09_OutcomeRecord &outcome){return m_outcomes.Pop(outcome);}
   int ActiveCount(void) const{int count=0;for(int i=0;i<m_capacity;i++)if(CheckPointer(m_active[i])!=POINTER_INVALID&&!SF09_IsTerminalState(m_active[i].state))count++;return count;}
   int PendingOutcomeCount(void) const{return m_outcomes.Count();}
   SF09_OutcomeTelemetry Telemetry(void) const{return m_telemetry;}
};

#endif
