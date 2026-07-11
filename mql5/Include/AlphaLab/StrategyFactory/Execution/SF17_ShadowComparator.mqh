#ifndef __SF17_SHADOW_COMPARATOR_MQH__
#define __SF17_SHADOW_COMPARATOR_MQH__
#include "SF17_Reconciliation.mqh"
#include "../Contracts/SF01_AllContracts.mqh"
struct SF17_ShadowComparison{string comparison_id;string intent_id;string paper_order_id;string observed_external_order_id;double paper_fill_price;double observed_fill_price;long paper_fill_time_utc_msc;long observed_fill_time_utc_msc;double price_delta;long latency_delta_milliseconds;double volume_delta;bool matched;string comparison_hash;};
SF17_ShadowComparison SF17_CompareShadow(const string intent_id,const string paper_order_id,const string external_id,const double paper_price,const double observed_price,const long paper_time,const long observed_time,const double paper_volume,const double observed_volume,const double price_tolerance,const long latency_tolerance,const double volume_tolerance)
{
   SF17_ShadowComparison x;x.intent_id=intent_id;x.paper_order_id=paper_order_id;x.observed_external_order_id=external_id;x.paper_fill_price=paper_price;x.observed_fill_price=observed_price;x.paper_fill_time_utc_msc=paper_time;x.observed_fill_time_utc_msc=observed_time;x.price_delta=observed_price-paper_price;x.latency_delta_milliseconds=observed_time-paper_time;x.volume_delta=observed_volume-paper_volume;x.matched=(MathAbs(x.price_delta)<=price_tolerance&&MathAbs((double)x.latency_delta_milliseconds)<=latency_tolerance&&MathAbs(x.volume_delta)<=volume_tolerance);const string canonical=intent_id+"|"+paper_order_id+"|"+external_id+"|"+SF01_CanonicalDouble(paper_price)+"|"+SF01_CanonicalDouble(observed_price)+"|"+IntegerToString(paper_time)+"|"+IntegerToString(observed_time)+"|"+SF01_CanonicalDouble(x.price_delta)+"|"+IntegerToString(x.latency_delta_milliseconds)+"|"+SF01_CanonicalDouble(x.volume_delta)+"|"+SF01_CanonicalBool(x.matched);x.comparison_id=SF01_StableId("xshd",canonical);x.comparison_hash=x.comparison_id;return x;
}
#endif
