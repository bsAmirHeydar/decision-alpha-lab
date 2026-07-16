#ifndef SAEDV416_CONFORMANCE_MQH
#define SAEDV416_CONFORMANCE_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416StaticConformance(){double q[3]={-1.0,0.0,1.0};double s[3]={1.0,0.8,0.5};return SAEDV416QuantilesMonotone(q)&&SAEDV416SurvivalCurveValid(s)&&!SAEDV416HasExecutionAuthority();}
#endif
