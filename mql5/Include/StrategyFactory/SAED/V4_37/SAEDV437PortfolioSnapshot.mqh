#ifndef SAED_V4_37_PORTFOLIOSNAPSHOT_MQH
#define SAED_V4_37_PORTFOLIOSNAPSHOT_MQH
// SAED_V4_37 PortfolioSnapshot: research-only static contract mirror.
struct SAEDV437PortfolioSnapshot { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidatePortfolioSnapshot(const SAEDV437PortfolioSnapshot &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
