#ifndef __SF17_PAPER_ORDER_MQH__
#define __SF17_PAPER_ORDER_MQH__
#include "SF17_ExecutionPolicy.mqh"
#include "../Candidate/SF08_CandidateEnums.mqh"
struct SF17_PaperOrder{string order_id;string intent_id;string intent_hash;string symbol;int direction;ENUM_SF08_ORDER_KIND order_kind;ENUM_SF17_ORDER_STATE state;double requested_volume;double filled_volume;double remaining_volume;double requested_price;double average_fill_price;double stop_price;double target_price;bool has_target;long accepted_at_utc_msc;long updated_at_utc_msc;long expires_at_utc_msc;long last_quote_sequence;ENUM_SF17_REJECT_REASON reject_reason;string order_hash;};
string SF17_OrderCanonical(const SF17_PaperOrder &o){return o.order_id+"|"+o.intent_id+"|"+o.intent_hash+"|"+o.symbol+"|"+IntegerToString(o.direction)+"|"+IntegerToString((int)o.order_kind)+"|"+IntegerToString((int)o.state)+"|"+SF01_CanonicalDouble(o.requested_volume)+"|"+SF01_CanonicalDouble(o.filled_volume)+"|"+SF01_CanonicalDouble(o.remaining_volume)+"|"+SF01_CanonicalDouble(o.requested_price)+"|"+SF01_CanonicalDouble(o.average_fill_price)+"|"+SF01_CanonicalDouble(o.stop_price)+"|"+SF01_CanonicalDouble(o.target_price)+"|"+SF01_CanonicalBool(o.has_target)+"|"+IntegerToString(o.accepted_at_utc_msc)+"|"+IntegerToString(o.updated_at_utc_msc)+"|"+IntegerToString(o.expires_at_utc_msc)+"|"+IntegerToString(o.last_quote_sequence)+"|"+IntegerToString((int)o.reject_reason);}
void SF17_RefreshOrderHash(SF17_PaperOrder &o){o.order_hash=SF01_StableId("pord",SF17_OrderCanonical(o));}
#endif
