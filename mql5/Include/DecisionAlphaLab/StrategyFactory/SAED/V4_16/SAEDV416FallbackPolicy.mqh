#ifndef SAEDV416_FALLBACK_MQH
#define SAEDV416_FALLBACK_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
int SAEDV416FailClosedDirective(const bool hash_ok,const bool known_time_ok,const bool calibrated,const bool supported){if(!hash_ok)return 5;if(!known_time_ok)return 5;if(!calibrated)return 3;if(!supported)return 2;return 0;}
#endif
