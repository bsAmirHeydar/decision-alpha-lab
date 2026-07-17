#ifndef SAED_V4_37_LIQUIDITYPROFILE_MQH
#define SAED_V4_37_LIQUIDITYPROFILE_MQH
// SAED_V4_37 LiquidityProfile: research-only static contract mirror.
struct SAEDV437LiquidityProfile { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidateLiquidityProfile(const SAEDV437LiquidityProfile &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
