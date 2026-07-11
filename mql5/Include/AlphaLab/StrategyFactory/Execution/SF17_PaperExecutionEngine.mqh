#ifndef __SF17_PAPER_EXECUTION_ENGINE_MQH__
#define __SF17_PAPER_EXECUTION_ENGINE_MQH__
#include "SF17_ShadowComparator.mqh"
#include "../Decision/SF16_ExecutionIntent.mqh"
class CSF17PaperExecutionEngine
{
private:
   string m_run_id;SF17_ExecutionPolicy m_policy;SF17_PaperOrder m_orders[SF17_MAX_ORDERS];int m_order_count;
   SF17_FillRecord m_fills[SF17_MAX_FILLS];int m_fill_count;SF17_PositionRecord m_positions[SF17_MAX_POSITIONS];int m_position_count;
   CSF17TransactionLedger m_ledger;SF17_ExecutionTelemetry m_telemetry;
   int FindOrderByIntent(const string intent_id)const{for(int i=0;i<m_order_count;i++)if(m_orders[i].intent_id==intent_id)return i;return -1;}
   int FindPosition(const string position_id)const{for(int i=0;i<m_position_count;i++)if(m_positions[i].position_id==position_id)return i;return -1;}
   bool Triggered(const SF17_PaperOrder &o,const SF17_QuoteObservation &q)const
   {
      if(o.order_kind==SF08_ORDER_MARKET)return true;
      if(o.order_kind==SF08_ORDER_LIMIT)return o.direction==1?q.ask<=o.requested_price:q.bid>=o.requested_price;
      return o.direction==1?q.ask>=o.requested_price:q.bid<=o.requested_price;
   }
   double EntryPrice(const SF17_PaperOrder &o,const SF17_QuoteObservation &q)const
   {
      const double adverse=m_policy.adverse_slippage_points*m_policy.point;double base=0.0;
      if(o.order_kind==SF08_ORDER_MARKET)base=o.direction==1?q.ask:q.bid;
      else if(o.order_kind==SF08_ORDER_LIMIT)base=o.direction==1?MathMin(o.requested_price,q.ask):MathMax(o.requested_price,q.bid);
      else base=o.direction==1?MathMax(o.requested_price,q.ask):MathMin(o.requested_price,q.bid);
      return o.direction==1?base+adverse:base-adverse;
   }
   bool AddEntryFill(SF17_PaperOrder &o,const SF17_QuoteObservation &q)
   {
      if(m_fill_count>=SF17_MAX_FILLS)return false;double volume=o.remaining_volume;
      if(m_policy.max_fill_volume_per_quote>0.0)volume=MathMin(volume,m_policy.max_fill_volume_per_quote);
      if(!m_policy.allow_partial_fills&&volume+1e-12<o.remaining_volume)return false;
      const double price=EntryPrice(o,q),old=o.filled_volume;o.filled_volume+=volume;o.remaining_volume=MathMax(0.0,o.requested_volume-o.filled_volume);o.average_fill_price=(o.average_fill_price*old+price*volume)/o.filled_volume;o.state=o.remaining_volume<=1e-12?SF17_ORDER_FILLED:SF17_ORDER_PARTIALLY_FILLED;o.updated_at_utc_msc=q.time_utc_msc;SF17_RefreshOrderHash(o);
      SF17_FillRecord f;f.order_id=o.order_id;f.intent_id=o.intent_id;f.position_id=SF01_StableId("ppos",m_run_id+"|"+o.intent_id);f.symbol=o.symbol;f.direction=o.direction;f.reason=o.order_kind==SF08_ORDER_MARKET?SF17_FILL_ENTRY_MARKET:(o.order_kind==SF08_ORDER_LIMIT?SF17_FILL_ENTRY_LIMIT:SF17_FILL_ENTRY_STOP);f.volume=volume;f.price=price;f.commission_cash=volume*m_policy.commission_per_lot_per_side;f.slippage_cash_proxy=MathAbs(price-(o.direction==1?q.ask:q.bid))*volume;f.quote_sequence=q.sequence;f.fill_time_utc_msc=q.time_utc_msc;f.fill_id=SF17_DeriveFillId(f);f.fill_hash=f.fill_id;m_fills[m_fill_count++]=f;
      m_ledger.Append(o.state==SF17_ORDER_FILLED?SF17_TX_ORDER_FILLED:SF17_TX_ORDER_PARTIAL_FILL,o.order_id,q.time_utc_msc,f.fill_hash,"entry fill");
      int pi=FindPosition(f.position_id);if(pi<0){if(m_position_count>=SF17_MAX_POSITIONS)return false;pi=m_position_count++;SF17_PositionRecord p;p.position_id=f.position_id;p.intent_id=o.intent_id;p.symbol=o.symbol;p.direction=o.direction;p.state=SF17_POSITION_OPEN;p.volume=volume;p.average_entry_price=price;p.stop_price=o.stop_price;p.target_price=o.target_price;p.has_target=o.has_target;p.opened_at_utc_msc=q.time_utc_msc;p.closed_at_utc_msc=0;p.average_exit_price=0.0;p.realized_gross_price_units=0.0;p.commission_cash=f.commission_cash;p.close_reason=SF17_FILL_EXIT_MANUAL;SF17_RefreshPositionHash(p);m_positions[pi]=p;m_ledger.Append(SF17_TX_POSITION_OPENED,p.position_id,q.time_utc_msc,p.position_hash,"paper position opened");}
      else{SF17_PositionRecord p=m_positions[pi];const double total=p.volume+volume;p.average_entry_price=(p.average_entry_price*p.volume+price*volume)/total;p.volume=total;p.commission_cash+=f.commission_cash;SF17_RefreshPositionHash(p);m_positions[pi]=p;m_ledger.Append(SF17_TX_POSITION_INCREASED,p.position_id,q.time_utc_msc,p.position_hash,"paper position increased");}
      return true;
   }
   void EvaluatePositions(const SF17_QuoteObservation &q)
   {
      for(int i=0;i<m_position_count;i++){SF17_PositionRecord p=m_positions[i];if(p.symbol!=q.symbol||p.state!=SF17_POSITION_OPEN)continue;const bool stop=p.direction==1?q.bid<=p.stop_price:q.ask>=p.stop_price;const bool target=p.has_target&&(p.direction==1?q.bid>=p.target_price:q.ask<=p.target_price);if(!stop&&!target)continue;const ENUM_SF17_FILL_REASON reason=stop?SF17_FILL_EXIT_STOP:SF17_FILL_EXIT_TARGET;const double trigger=stop?p.stop_price:p.target_price;const double adverse=m_policy.adverse_slippage_points*m_policy.point;const double market=p.direction==1?q.bid:q.ask;double price=market;if(stop)price=p.direction==1?MathMin(trigger,market)-adverse:MathMax(trigger,market)+adverse;else price=p.direction==1?MathMax(trigger,market)-adverse:MathMin(trigger,market)+adverse;p.state=SF17_POSITION_CLOSED;p.closed_at_utc_msc=q.time_utc_msc;p.average_exit_price=price;p.realized_gross_price_units=(price-p.average_entry_price)*p.direction*p.volume;p.commission_cash+=p.volume*m_policy.commission_per_lot_per_side;p.close_reason=reason;SF17_RefreshPositionHash(p);m_positions[i]=p;m_ledger.Append(stop?SF17_TX_POSITION_CLOSED_STOP:SF17_TX_POSITION_CLOSED_TARGET,p.position_id,q.time_utc_msc,p.position_hash,"paper position closed");}
   }
public:
   CSF17PaperExecutionEngine(){m_run_id="";m_order_count=0;m_fill_count=0;m_position_count=0;SF17_ResetTelemetry(m_telemetry);}
   bool Configure(const string run_id,const SF17_ExecutionPolicy &policy,string &error){if(run_id==""||!SF17_ValidatePolicy(policy,error))return false;m_run_id=run_id;m_policy=policy;m_order_count=0;m_fill_count=0;m_position_count=0;m_ledger.Reset();SF17_ResetTelemetry(m_telemetry);error="";return true;}
   bool Submit(const SF16_ExecutionIntent &intent,const long now_utc_msc,SF17_PaperOrder &out,string &error)
   {
      m_telemetry.intents_received++;const int existing=FindOrderByIntent(intent.intent_id);if(existing>=0){m_telemetry.duplicate_intents++;if(m_orders[existing].intent_hash!=intent.intent_hash){error="duplicate hash conflict";return false;}out=m_orders[existing];error="";return true;}
      if(m_order_count>=SF17_MAX_ORDERS){error="order capacity";return false;}string intent_error;if(!SF16_ValidateIntent(intent,intent_error)){error="invalid intent:"+intent_error;return false;}if(intent.authority!=SF16_AUTHORITY_PAPER_ELIGIBLE&&!m_policy.allow_research_only_intents){error="research-only authority";return false;}if(now_utc_msc>intent.expires_at_utc_msc){error="expired intent";return false;}
      SF17_PaperOrder o;o.order_id=SF01_StableId("pord",m_run_id+"|"+intent.intent_id+"|"+intent.intent_hash+"|"+SF17_DerivePolicyHash(m_policy));o.intent_id=intent.intent_id;o.intent_hash=intent.intent_hash;o.symbol=intent.symbol;o.direction=intent.direction;o.order_kind=intent.order_kind;o.state=SF17_ORDER_WORKING;o.requested_volume=intent.volume;o.filled_volume=0.0;o.remaining_volume=intent.volume;o.requested_price=intent.entry_price;o.average_fill_price=0.0;o.stop_price=intent.stop_price;o.target_price=intent.target_price;o.has_target=intent.has_target;o.accepted_at_utc_msc=now_utc_msc;o.updated_at_utc_msc=now_utc_msc;o.expires_at_utc_msc=intent.expires_at_utc_msc;o.last_quote_sequence=-1;o.reject_reason=SF17_REJECT_NONE;SF17_RefreshOrderHash(o);m_orders[m_order_count++]=o;m_telemetry.intents_accepted++;m_ledger.Append(SF17_TX_INTENT_RECEIVED,intent.intent_id,now_utc_msc,intent.intent_hash,"intent received");m_ledger.Append(SF17_TX_ORDER_ACCEPTED,o.order_id,now_utc_msc,o.order_hash,"paper order accepted");m_ledger.Append(SF17_TX_ORDER_WORKING,o.order_id,now_utc_msc,o.order_hash,"paper order working");out=o;error="";return true;
   }
   bool OnQuote(const SF17_QuoteObservation &q,const long now_utc_msc,string &error){if(!SF17_ValidateQuote(q,error))return false;if(now_utc_msc-q.time_utc_msc>m_policy.maximum_quote_age_milliseconds){m_telemetry.stale_quotes++;error="stale quote";return false;}for(int i=0;i<m_order_count;i++){SF17_PaperOrder o=m_orders[i];if(o.symbol!=q.symbol||o.last_quote_sequence>=q.sequence)continue;o.last_quote_sequence=q.sequence;if(o.state==SF17_ORDER_WORKING||o.state==SF17_ORDER_PARTIALLY_FILLED){if(now_utc_msc>o.expires_at_utc_msc){o.state=SF17_ORDER_EXPIRED;o.updated_at_utc_msc=now_utc_msc;SF17_RefreshOrderHash(o);m_ledger.Append(SF17_TX_ORDER_EXPIRED,o.order_id,now_utc_msc,o.order_hash,"paper order expired");}else if(Triggered(o,q))AddEntryFill(o,q);}m_orders[i]=o;}EvaluatePositions(q);error="";return true;}
   int OrderCount()const{return m_order_count;}int FillCount()const{return m_fill_count;}int PositionCount()const{return m_position_count;}int TransactionCount()const{return m_ledger.Count();}
   bool GetOrder(const int index,SF17_PaperOrder &out)const{if(index<0||index>=m_order_count)return false;out=m_orders[index];return true;}
   bool GetPosition(const int index,SF17_PositionRecord &out)const{if(index<0||index>=m_position_count)return false;out=m_positions[index];return true;}
};
#endif
