#ifndef __SF18_LIVE_EXECUTION_COORDINATOR_MQH__
#define __SF18_LIVE_EXECUTION_COORDINATOR_MQH__
#include "SF18_RequestBuilder.mqh"
class CSF18LiveExecutionCoordinator
{
private:
 string m_run_id;ENUM_SF18_LIVE_MODE m_mode;SF18_MicroLiveRelease m_release;SF18_LiveAuthorization m_auth;SF18_SafetyPolicy m_policy;ISF18BrokerPort *m_broker;
 CSF18KillSwitch m_kill;CSF18CircuitBreaker m_circuit;CSF18LiveLedger m_ledger;ENUM_SF18_AUTH_STATE m_auth_state;int m_session_orders,m_identity_count;
 string m_intent_ids[SF18_MAX_INTENT_IDENTITIES],m_intent_hashes[SF18_MAX_INTENT_IDENTITIES];ulong m_magic;
 int FindIntent(const string id)const{for(int i=0;i<m_identity_count;i++)if(m_intent_ids[i]==id)return i;return -1;}
 SF18_LiveDecisionRecord MakeDecision(const SF16_ExecutionIntent &intent,const ENUM_SF18_LIVE_DECISION decision,const ENUM_SF18_REJECT_REASON reason,const string request_id,const long now,const string message)
 {
  SF18_LiveDecisionRecord d;d.intent_id=intent.intent_id;d.decision=decision;d.reject_reason=reason;d.request_id=request_id;d.authorization_id=m_auth.authorization_id;d.release_hash=m_release.release_hash;d.event_time_utc_msc=now;d.message=message;
  const string canonical=d.intent_id+"|"+IntegerToString((int)decision)+"|"+IntegerToString((int)reason)+"|"+request_id+"|"+d.authorization_id+"|"+d.release_hash+"|"+IntegerToString(now)+"|"+message;d.decision_id=SF01_StableId("ldec",canonical);d.decision_hash=d.decision_id;return d;
 }
 ENUM_SF18_REJECT_REASON Preflight(const SF16_ExecutionIntent &intent,const SF18_AccountGuardSnapshot &account,const SF18_QuoteSnapshot &quote,const long now,string &error)
 {
  if(m_mode==SF18_LIVE_DISABLED)return SF18_REJECT_MODE_DISABLED;if(m_mode==SF18_LIVE_MICRO&&m_kill.Engaged())return SF18_REJECT_KILL_SWITCH;if(!m_circuit.CanAttempt(now))return SF18_REJECT_CIRCUIT_OPEN;
  if(!SF16_ValidateIntent(intent,error))return SF18_REJECT_INVALID_INTENT;if(intent.authority!=SF16_AUTHORITY_PAPER_ELIGIBLE)return SF18_REJECT_INTENT_AUTHORITY;if(now>intent.expires_at_utc_msc)return SF18_REJECT_INTENT_EXPIRED;
  if(m_auth_state!=SF18_AUTH_ARMED)return m_auth_state==SF18_AUTH_CONSUMED?SF18_REJECT_AUTH_CONSUMED:SF18_REJECT_AUTH_MISSING;if(now>m_auth.expires_at_utc_msc)return SF18_REJECT_AUTH_EXPIRED;
  if(m_auth.release_hash!=m_release.release_hash||m_auth.mode!=m_mode)return SF18_REJECT_AUTH_INVALID;if(now<m_release.valid_from_utc_msc||now>m_release.valid_until_utc_msc)return SF18_REJECT_RELEASE_MISMATCH;
  if(account.account_login!=m_release.account_login||account.account_login!=m_auth.account_login)return SF18_REJECT_ACCOUNT_MISMATCH;if(account.account_server!=m_release.account_server||account.account_server!=m_auth.account_server)return SF18_REJECT_SERVER_MISMATCH;
  if(intent.symbol!=m_release.allowed_symbol||intent.symbol!=m_auth.allowed_symbol||quote.symbol!=intent.symbol)return SF18_REJECT_SYMBOL_NOT_ALLOWED;
  if(intent.strategy_id!=m_release.strategy_id||intent.strategy_version!=m_release.strategy_version||intent.runtime_generation_id!=m_release.runtime_generation_id||intent.model_release_hash!=m_release.model_release_hash||intent.decision_policy_hash!=m_release.decision_policy_hash||intent.risk_policy_hash!=m_release.risk_policy_hash||intent.allocation_policy_hash!=m_release.allocation_policy_hash)return SF18_REJECT_RELEASE_MISMATCH;
  if(m_policy.require_terminal_permission&&(!account.terminal_trade_allowed||!account.expert_trade_allowed))return SF18_REJECT_TERMINAL_DISABLED;if(m_policy.require_account_permission&&!account.account_trade_allowed)return SF18_REJECT_ACCOUNT_DISABLED;
  if(now-account.snapshot_time_utc_msc>m_policy.maximum_account_snapshot_age_milliseconds)return SF18_REJECT_STALE_ACCOUNT;if(now-quote.time_utc_msc>m_policy.maximum_quote_age_milliseconds)return SF18_REJECT_STALE_QUOTE;if(SF18_SpreadPoints(quote)>m_policy.maximum_spread_points)return SF18_REJECT_SPREAD;
  const double max_volume=MathMin(m_policy.maximum_volume_per_order,MathMin(m_release.maximum_volume,m_auth.maximum_volume));if(intent.volume>max_volume+0.000000000001)return SF18_REJECT_VOLUME;if(intent.expected_max_loss_cash>m_policy.maximum_cash_risk_per_order+0.00000001)return SF18_REJECT_RISK;
  if(-account.daily_realized_pnl_cash>=m_policy.maximum_daily_realized_loss_cash||-(account.daily_realized_pnl_cash+account.floating_pnl_cash)>=m_policy.maximum_daily_total_loss_cash)return SF18_REJECT_DAILY_LOSS;
  if(account.equity_cash<m_policy.minimum_equity_cash)return SF18_REJECT_EQUITY_FLOOR;if(account.free_margin_cash<m_policy.minimum_free_margin_cash)return SF18_REJECT_FREE_MARGIN;if(account.margin_level_percent<m_policy.minimum_margin_level_percent)return SF18_REJECT_MARGIN_LEVEL;
  if(account.total_exposure_volume+intent.volume>m_policy.maximum_total_exposure_volume+0.000000000001)return SF18_REJECT_EXPOSURE;if(m_session_orders>=MathMin(m_policy.maximum_orders_per_session,MathMin(m_release.maximum_orders,m_auth.maximum_orders)))return SF18_REJECT_SESSION_LIMIT;
  if(account.active_order_count>=m_policy.maximum_concurrent_orders)return SF18_REJECT_CONCURRENT_ORDERS;if(account.open_position_count>=m_policy.maximum_positions)return SF18_REJECT_POSITION_LIMIT;return SF18_REJECT_NONE;
 }
public:
 CSF18LiveExecutionCoordinator(){m_run_id="";m_mode=SF18_LIVE_DISABLED;m_broker=NULL;m_auth_state=SF18_AUTH_LOCKED;m_session_orders=0;m_identity_count=0;m_magic=180018;}
 bool Configure(const string run_id,const ENUM_SF18_LIVE_MODE mode,const SF18_MicroLiveRelease &release,const SF18_LiveAuthorization &auth,const SF18_SafetyPolicy &policy,ISF18BrokerPort *broker,const ulong magic,string &error)
 {
  if(run_id==""||broker==NULL||!SF18_ValidateRelease(release,error)||!SF18_ValidateAuthorization(auth,error)||!SF18_ValidateSafetyPolicy(policy,error)){return false;}if(auth.release_hash!=release.release_hash){error="authorization release mismatch";return false;}
  if(mode==SF18_LIVE_MICRO&&!broker.HasLiveAuthority()){error="micro-live requires live broker port";return false;}if(mode==SF18_LIVE_DRY_RUN&&broker.HasLiveAuthority()){error="dry-run cannot bind live broker port";return false;}
  m_run_id=run_id;m_mode=mode;m_release=release;m_auth=auth;m_policy=policy;m_broker=broker;m_magic=magic;m_session_orders=0;m_identity_count=0;m_ledger.Reset();m_circuit.Configure(policy.maximum_consecutive_failures,policy.cooldown_after_failure_milliseconds);m_auth_state=mode==SF18_LIVE_DRY_RUN?SF18_AUTH_ARMED:SF18_AUTH_LOCKED;error="";return true;
 }
 bool ArmMicroLive(const long now,string &error){if(m_mode!=SF18_LIVE_MICRO){error="not micro-live";return false;}if(!m_kill.Disarm(m_auth,now)){error="authorization cannot disarm kill switch";return false;}m_auth_state=SF18_AUTH_ARMED;m_ledger.Append(SF18_TX_KILL_DISARMED,m_auth.authorization_id,now,m_auth.authorization_hash,"micro-live armed");error="";return true;}
 void EngageKillSwitch(const string reason,const long now){m_kill.Engage(reason,now);m_auth_state=SF18_AUTH_REVOKED;m_ledger.Append(SF18_TX_KILL_ENGAGED,m_run_id,now,SF01_StableId("ksw",reason),reason);}
 bool Submit(const SF16_ExecutionIntent &intent,const SF18_AccountGuardSnapshot &account,const SF18_QuoteSnapshot &quote,const long now,SF18_LiveDecisionRecord &out,string &error)
 {
  m_ledger.Append(SF18_TX_INTENT_RECEIVED,intent.intent_id,now,intent.intent_hash,"live intent received");const int existing=FindIntent(intent.intent_id);if(existing>=0){if(m_intent_hashes[existing]!=intent.intent_hash){out=MakeDecision(intent,SF18_LIVE_REJECT,SF18_REJECT_DUPLICATE_CONFLICT,"",now,"duplicate hash conflict");error=out.message;return false;}out=MakeDecision(intent,SF18_LIVE_CHECK_ONLY,SF18_REJECT_IDEMPOTENT_REPLAY,"",now,"idempotent replay");error="";return true;}
  if(m_identity_count>=SF18_MAX_INTENT_IDENTITIES){out=MakeDecision(intent,SF18_LIVE_REJECT,SF18_REJECT_CAPACITY,"",now,"identity capacity");error=out.message;return false;}m_intent_ids[m_identity_count]=intent.intent_id;m_intent_hashes[m_identity_count]=intent.intent_hash;m_identity_count++;
  const ENUM_SF18_REJECT_REASON reason=Preflight(intent,account,quote,now,error);if(reason!=SF18_REJECT_NONE){out=MakeDecision(intent,SF18_LIVE_REJECT,reason,"",now,"preflight rejected");m_ledger.Append(SF18_TX_PREFLIGHT_REJECTED,intent.intent_id,now,out.decision_hash,out.message);error=out.message;return false;}
  MqlTradeRequest request;string request_id;if(!SF18_BuildOpenRequest(intent,quote,m_policy,m_magic,request,request_id,error)){out=MakeDecision(intent,SF18_LIVE_REJECT,SF18_REJECT_SYMBOL_SPEC,"",now,error);return false;}m_ledger.Append(SF18_TX_PREFLIGHT_PASSED,intent.intent_id,now,request_id,"preflight passed");m_ledger.Append(SF18_TX_CHECK_REQUESTED,request_id,now,request_id,"broker check requested");
  SF18_BrokerCheckResult check;if(!m_broker.Check(request,request_id,now,check)||!check.api_ok||!SF18_RetcodeSuccess(check.retcode)){const bool opened=m_circuit.RecordFailure("check",now);m_ledger.Append(SF18_TX_CHECK_REJECTED,request_id,now,check.result_hash,"broker check rejected");if(opened)m_ledger.Append(SF18_TX_CIRCUIT_OPENED,m_run_id,now,check.result_hash,"circuit opened");out=MakeDecision(intent,SF18_LIVE_REJECT,SF18_REJECT_CHECK_RETCODE,request_id,now,"order check rejected");error=out.message;return false;}
  m_ledger.Append(SF18_TX_CHECK_ACCEPTED,request_id,now,check.result_hash,"broker check accepted");if(m_mode==SF18_LIVE_DRY_RUN){m_circuit.RecordSuccess();out=MakeDecision(intent,SF18_LIVE_CHECK_ONLY,SF18_REJECT_NONE,request_id,now,"dry-run check accepted");error="";return true;}
  m_ledger.Append(SF18_TX_SEND_REQUESTED,request_id,now,request_id,"broker send requested");SF18_BrokerSendResult sent;if(!m_broker.Send(request,request_id,now,sent)||!sent.api_ok||!SF18_RetcodeSuccess(sent.retcode)){const bool opened=m_circuit.RecordFailure("send",now);m_ledger.Append(SF18_TX_SEND_REJECTED,request_id,now,sent.result_hash,"broker send rejected");if(opened)m_ledger.Append(SF18_TX_CIRCUIT_OPENED,m_run_id,now,sent.result_hash,"circuit opened");out=MakeDecision(intent,SF18_LIVE_REJECT,SF18_REJECT_SEND_RETCODE,request_id,now,"order send rejected");error=out.message;return false;}
  m_session_orders++;m_circuit.RecordSuccess();m_ledger.Append(SF18_TX_SEND_ACCEPTED,request_id,now,sent.result_hash,"broker send accepted");if(m_policy.one_shot_authorization){m_auth_state=SF18_AUTH_CONSUMED;m_ledger.Append(SF18_TX_AUTH_CONSUMED,m_auth.authorization_id,now,m_auth.authorization_hash,"one-shot consumed");}out=MakeDecision(intent,SF18_LIVE_ACCEPTED,SF18_REJECT_NONE,request_id,now,"broker accepted request");error="";return true;
 }
 int SessionOrders(void)const{return m_session_orders;}ENUM_SF18_AUTH_STATE AuthorizationState(void)const{return m_auth_state;}ENUM_SF18_CIRCUIT_STATE CircuitState(void)const{return m_circuit.State();}ENUM_SF18_KILL_SWITCH_STATE KillSwitchState(void)const{return m_kill.State();}int LedgerCount(void)const{return m_ledger.Count();}string LedgerTailHash(void)const{return m_ledger.TailHash();}
};
#endif
