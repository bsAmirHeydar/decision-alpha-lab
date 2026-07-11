#ifndef __SF18_DRY_RUN_BROKER_ADAPTER_MQH__
#define __SF18_DRY_RUN_BROKER_ADAPTER_MQH__
#include "SF18_BrokerContracts.mqh"
class CSF18DryRunBrokerAdapter:public ISF18BrokerPort
{
private:uint m_check_retcode,m_send_retcode;ulong m_counter;
public:
 CSF18DryRunBrokerAdapter(){m_check_retcode=0;m_send_retcode=TRADE_RETCODE_DONE;m_counter=180000;}
 void Configure(const uint check_retcode,const uint send_retcode){m_check_retcode=check_retcode;m_send_retcode=send_retcode;}
 virtual bool HasLiveAuthority(void)const{return false;}
 virtual bool Check(const MqlTradeRequest &request,const string request_id,const long now_utc_msc,SF18_BrokerCheckResult &out)
 {
  out.request_id=request_id;out.api_ok=true;out.retcode=m_check_retcode;out.retcode_class=SF18_ClassifyRetcode(m_check_retcode);out.balance_cash=100000.0;out.equity_cash=100000.0;out.margin_cash=100.0;out.free_margin_cash=99900.0;out.comment="deterministic dry run";out.checked_at_utc_msc=now_utc_msc;out.result_hash=SF01_StableId("lchk",request_id+"|"+IntegerToString((long)m_check_retcode)+"|"+IntegerToString(now_utc_msc));return true;
 }
 virtual bool Send(const MqlTradeRequest &request,const string request_id,const long now_utc_msc,SF18_BrokerSendResult &out)
 {
  m_counter++;out.request_id=request_id;out.api_ok=true;out.retcode=m_send_retcode;out.retcode_class=SF18_ClassifyRetcode(m_send_retcode);out.order_ticket=m_counter;out.deal_ticket=m_counter+100000;out.volume=request.volume;out.price=request.price;out.bid=request.price;out.ask=request.price;out.comment="deterministic dry run";out.sent_at_utc_msc=now_utc_msc;out.result_hash=SF01_StableId("lsnd",request_id+"|"+IntegerToString((long)m_send_retcode)+"|"+IntegerToString(now_utc_msc));return true;
 }
};
#endif
