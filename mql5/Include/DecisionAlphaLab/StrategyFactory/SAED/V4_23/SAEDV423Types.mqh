#property strict
#ifndef SAEDV423TYPES_MQH
#define SAEDV423TYPES_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
enum ENUM_SAED_V4_23_ACTION { SAED_V4_23_SKIP=0, SAED_V4_23_LONG=1, SAED_V4_23_SHORT=2 };
struct SAEDV423PolicyProbability { string state; double skip; double long_p; double short_p; };

#endif
