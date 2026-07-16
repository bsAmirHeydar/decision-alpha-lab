#ifndef SAEDV415_QUALITY_GATE_MQH
#define SAEDV415_QUALITY_GATE_MQH
// SAED_V4_15 monotone quality/freshness gate.
double SAEDV415Gate(const double quality,const int age_seconds){ if(quality<=0.0)return 0.0; return quality*MathExp(-((double)age_seconds)/86400.0); }
#endif
