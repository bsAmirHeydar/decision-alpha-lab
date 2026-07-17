#ifndef SAEDV436STATICASSERTIONS_MQH
#define SAEDV436STATICASSERTIONS_MQH
// SAED V4-36 static mirror; no experiment, order, capital or production authority.
bool SAED_V4_36_StaticAuthoritySafe(){ return (!SAED_V4_36_AUTOMATIC_EXECUTION && !SAED_V4_36_CAPITAL_AUTHORITY && !SAED_V4_36_PRODUCTION_AUTHORIZATION); }
#endif
