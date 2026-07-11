#property strict
#include <AlphaLab/StrategyFactory/Live/SF18_AllLive.mqh>
int OnInit()
{
   long now=(long)TimeTradeServer()*1000;
   if(now<=0)now=(long)TimeCurrent()*1000;
   if(now<=0)now=2000000;
   MqlTick tick;
   if(!SymbolInfoTick(_Symbol,tick))
   {
      Print("SF18 SymbolInfoTick failed: ",GetLastError());
      return INIT_FAILED;
   }
   const double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
   if(point<=0.0||tick.bid<=0.0||tick.ask<tick.bid)
   {
      Print("SF18 invalid terminal quote");
      return INIT_FAILED;
   }
   SF18_MicroLiveRelease release;
   SF18_BuildReferenceRelease(now,release);
   release.allowed_symbol=_Symbol;
   release.release_hash=SF18_DeriveReleaseHash(release);
   SF18_LiveAuthorization auth;
   SF18_BuildReferenceAuthorization(now,release,SF18_LIVE_DRY_RUN,auth);
   SF18_SafetyPolicy policy;
   SF18_BuildReferencePolicy(policy);
   SF18_QuoteSnapshot quote;
   quote.symbol=_Symbol;quote.bid=tick.bid;quote.ask=tick.ask;quote.point=point;quote.time_utc_msc=now;quote.sequence=1;
   policy.maximum_spread_points=SF18_SpreadPoints(quote)+10.0;
   policy.policy_hash=SF18_DeriveSafetyPolicyHash(policy);
   CSF18DryRunBrokerAdapter broker;
   CSF18LiveExecutionCoordinator engine;
   string error;
   if(!engine.Configure("sf18-self-test",SF18_LIVE_DRY_RUN,release,auth,policy,&broker,180018,error))
   {
      Print("SF18 configure failed: ",error);
      return INIT_FAILED;
   }
   SF16_ExecutionIntent intent;
   SF18_BuildReferenceIntent(now,intent);
   const double distance=MathMax(100.0*point,tick.ask*0.01);
   intent.symbol=_Symbol;
   intent.entry_price=tick.ask;
   intent.stop_price=MathMax(point,tick.ask-distance);
   intent.target_price=tick.ask+2.0*distance;
   intent.intent_hash=SF16_DeriveIntentHash(intent);
   SF18_AccountGuardSnapshot account;
   account.account_login=123456;account.account_server="Broker-Demo";account.equity_cash=10000;account.balance_cash=10000;account.free_margin_cash=9000;account.margin_level_percent=1000;account.daily_realized_pnl_cash=0;account.floating_pnl_cash=0;account.total_exposure_volume=0;account.active_order_count=0;account.open_position_count=0;account.terminal_trade_allowed=true;account.account_trade_allowed=true;account.expert_trade_allowed=true;account.snapshot_time_utc_msc=now;account.snapshot_hash=SF18_DeriveAccountSnapshotHash(account);
   SF18_LiveDecisionRecord decision;
   if(!engine.Submit(intent,account,quote,now,decision,error)||decision.decision!=SF18_LIVE_CHECK_ONLY||engine.SessionOrders()!=0)
   {
      Print("SF18 self-test failed: ",error," reason=",IntegerToString((int)decision.reject_reason));
      return INIT_FAILED;
   }
   Print("SF18 self-test PASS ledger=",engine.LedgerCount()," tail=",engine.LedgerTailHash());
   return INIT_SUCCEEDED;
}
void OnTick(){}
