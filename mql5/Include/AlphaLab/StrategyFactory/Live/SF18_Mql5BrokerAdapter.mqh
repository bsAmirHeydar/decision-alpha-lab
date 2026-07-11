#ifndef __SF18_MQL5_BROKER_ADAPTER_MQH__
#define __SF18_MQL5_BROKER_ADAPTER_MQH__
#include "SF18_BrokerContracts.mqh"
// This is the only Strategy Factory Phase 18 source file allowed to invoke broker mutation APIs.
// The coordinator must complete all release, authorization, kill-switch, circuit, account, quote,
// exposure and risk gates before calling this adapter.
class CSF18Mql5BrokerAdapter:public ISF18BrokerPort
{
public:
 virtual bool HasLiveAuthority(void)const{return true;}
 virtual bool Check(const MqlTradeRequest &request,const string request_id,const long now_utc_msc,SF18_BrokerCheckResult &out)
 {
  MqlTradeCheckResult raw;ZeroMemory(raw);ResetLastError();const bool ok=OrderCheck(request,raw);
  out.request_id=request_id;out.api_ok=ok;out.retcode=raw.retcode;out.retcode_class=SF18_ClassifyRetcode(raw.retcode);out.balance_cash=raw.balance;out.equity_cash=raw.equity;out.margin_cash=raw.margin;out.free_margin_cash=raw.margin_free;out.comment=raw.comment;out.checked_at_utc_msc=now_utc_msc;
  out.result_hash=SF01_StableId("lchk",request_id+"|"+SF01_CanonicalBool(ok)+"|"+IntegerToString((long)raw.retcode)+"|"+SF01_CanonicalDouble(raw.margin)+"|"+IntegerToString(now_utc_msc));return ok;
 }
 virtual bool Send(const MqlTradeRequest &request,const string request_id,const long now_utc_msc,SF18_BrokerSendResult &out)
 {
  MqlTradeResult raw;ZeroMemory(raw);ResetLastError();const bool ok=OrderSend(request,raw);
  out.request_id=request_id;out.api_ok=ok;out.retcode=raw.retcode;out.retcode_class=SF18_ClassifyRetcode(raw.retcode);out.order_ticket=raw.order;out.deal_ticket=raw.deal;out.volume=raw.volume;out.price=raw.price;out.bid=raw.bid;out.ask=raw.ask;out.comment=raw.comment;out.sent_at_utc_msc=now_utc_msc;
  out.result_hash=SF01_StableId("lsnd",request_id+"|"+SF01_CanonicalBool(ok)+"|"+IntegerToString((long)raw.retcode)+"|"+IntegerToString((long)raw.order)+"|"+IntegerToString((long)raw.deal)+"|"+IntegerToString(now_utc_msc));return ok;
 }
};
#endif
