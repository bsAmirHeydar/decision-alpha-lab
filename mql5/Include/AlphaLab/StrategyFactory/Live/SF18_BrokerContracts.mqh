#ifndef __SF18_BROKER_CONTRACTS_MQH__
#define __SF18_BROKER_CONTRACTS_MQH__
#include "SF18_QuoteSnapshot.mqh"
#include "SF18_RetcodeMap.mqh"
#include "../Decision/SF16_ExecutionIntent.mqh"
struct SF18_BrokerCheckResult{string request_id;bool api_ok;uint retcode;ENUM_SF18_RETCODE_CLASS retcode_class;double balance_cash,equity_cash,margin_cash,free_margin_cash;string comment;long checked_at_utc_msc;string result_hash;};
struct SF18_BrokerSendResult{string request_id;bool api_ok;uint retcode;ENUM_SF18_RETCODE_CLASS retcode_class;ulong order_ticket,deal_ticket;double volume,price,bid,ask;string comment;long sent_at_utc_msc;string result_hash;};
struct SF18_LiveDecisionRecord{string decision_id,intent_id;ENUM_SF18_LIVE_DECISION decision;ENUM_SF18_REJECT_REASON reject_reason;string request_id,authorization_id,release_hash;long event_time_utc_msc;string message,decision_hash;};
class ISF18BrokerPort
{
public:
 virtual bool Check(const MqlTradeRequest &request,const string request_id,const long now_utc_msc,SF18_BrokerCheckResult &out)=0;
 virtual bool Send(const MqlTradeRequest &request,const string request_id,const long now_utc_msc,SF18_BrokerSendResult &out)=0;
 virtual bool HasLiveAuthority(void)const=0;
};
#endif
