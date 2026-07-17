#ifndef SAED_V4_38_TYPES_MQH
#define SAED_V4_38_TYPES_MQH
// SAED_V4_38 research-only types.
struct SAEDV438Decision { string decision; string treatment_id; double confidence; double net_edge_bps; double size_fraction; };
struct SAEDV438State { long sequence; int cooldown_bars; double drawdown_state; };
#endif
