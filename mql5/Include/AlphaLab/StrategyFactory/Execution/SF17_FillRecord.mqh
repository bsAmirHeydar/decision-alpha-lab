#ifndef __SF17_FILL_RECORD_MQH__
#define __SF17_FILL_RECORD_MQH__
#include "SF17_PaperOrder.mqh"
struct SF17_FillRecord{string fill_id;string order_id;string intent_id;string position_id;string symbol;int direction;ENUM_SF17_FILL_REASON reason;double volume;double price;double commission_cash;double slippage_cash_proxy;long quote_sequence;long fill_time_utc_msc;string fill_hash;};
string SF17_DeriveFillId(const SF17_FillRecord &f){return SF01_StableId("pfil",f.order_id+"|"+f.position_id+"|"+IntegerToString((int)f.reason)+"|"+SF01_CanonicalDouble(f.volume)+"|"+SF01_CanonicalDouble(f.price)+"|"+IntegerToString(f.quote_sequence)+"|"+IntegerToString(f.fill_time_utc_msc));}
#endif
