#ifndef SAEDV415_DISAGREEMENT_GUARD_MQH
#define SAEDV415_DISAGREEMENT_GUARD_MQH
// SAED_V4_15 disagreement inflates uncertainty and never grants authority.
double SAEDV415InflateUncertainty(const double u,const double d,const double threshold,const double factor){ return (d>threshold ? u*factor : u); }
#endif
