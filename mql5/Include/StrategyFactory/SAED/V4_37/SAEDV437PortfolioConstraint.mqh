#ifndef SAED_V4_37_PORTFOLIOCONSTRAINT_MQH
#define SAED_V4_37_PORTFOLIOCONSTRAINT_MQH
// SAED_V4_37 PortfolioConstraint: research-only static contract mirror.
struct SAEDV437PortfolioConstraint { string object_id; string object_hash; bool research_only; bool production_authorized; };
bool SAEDV437ValidatePortfolioConstraint(const SAEDV437PortfolioConstraint &x){ return x.object_id!="" && x.object_hash!="" && x.research_only && !x.production_authorized; }
#endif
