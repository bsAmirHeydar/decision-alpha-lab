#ifndef __SF17_POSITION_RECORD_MQH__
#define __SF17_POSITION_RECORD_MQH__
#include "SF17_FillRecord.mqh"
struct SF17_PositionRecord{string position_id;string intent_id;string symbol;int direction;ENUM_SF17_POSITION_STATE state;double volume;double average_entry_price;double stop_price;double target_price;bool has_target;long opened_at_utc_msc;long closed_at_utc_msc;double average_exit_price;double realized_gross_price_units;double commission_cash;ENUM_SF17_FILL_REASON close_reason;string position_hash;};
string SF17_PositionCanonical(const SF17_PositionRecord &p){return p.position_id+"|"+p.intent_id+"|"+p.symbol+"|"+IntegerToString(p.direction)+"|"+IntegerToString((int)p.state)+"|"+SF01_CanonicalDouble(p.volume)+"|"+SF01_CanonicalDouble(p.average_entry_price)+"|"+SF01_CanonicalDouble(p.stop_price)+"|"+SF01_CanonicalDouble(p.target_price)+"|"+SF01_CanonicalBool(p.has_target)+"|"+IntegerToString(p.opened_at_utc_msc)+"|"+IntegerToString(p.closed_at_utc_msc)+"|"+SF01_CanonicalDouble(p.average_exit_price)+"|"+SF01_CanonicalDouble(p.realized_gross_price_units)+"|"+SF01_CanonicalDouble(p.commission_cash)+"|"+IntegerToString((int)p.close_reason);}
void SF17_RefreshPositionHash(SF17_PositionRecord &p){p.position_hash=SF01_StableId("ppos",SF17_PositionCanonical(p));}
#endif
