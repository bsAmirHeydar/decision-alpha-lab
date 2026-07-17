#ifndef SAED_V4_39_MODE_GATE_MQH
#define SAED_V4_39_MODE_GATE_MQH
enum SAEDV439Mode { V439_OFF=0,V439_PAPER=1,V439_SHADOW=2,V439_MICRO_LIVE_QUALIFICATION=3,V439_MICRO_LIVE=4,V439_PRODUCTION=5 };
bool SAEDV439ModeHasBrokerSideEffects(const SAEDV439Mode mode){return false;}
bool SAEDV439CanEnterMicroLive(const bool signed_permit,const bool external_runtime,const bool broker_live,const bool kill_drill){return false;}
#endif
