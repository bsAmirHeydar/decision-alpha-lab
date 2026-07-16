#ifndef SAEDV415_TELEMETRY_MQH
#define SAEDV415_TELEMETRY_MQH
// SAED_V4_15 static telemetry mirror.
struct SAEDV415Telemetry { int available_domain_views; int available_foundation_views; int missing_required_views; double disagreement; double uncertainty; int directive; };
#endif
