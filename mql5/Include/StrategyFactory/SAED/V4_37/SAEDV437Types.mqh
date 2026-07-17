#ifndef SAED_V4_37_TYPES_MQH
#define SAED_V4_37_TYPES_MQH
// SAED_V4_37 research-only static mirror.
struct SAEDV437Money { double value; string currency; };
struct SAEDV437Exposure { string instrument_id; double gross_notional; double signed_notional; };
struct SAEDV437Cost { double explicit_bps; double impact_bps; double total_bps; };
struct SAEDV437Capacity { string opportunity_id; double units; double notional; };
#endif
