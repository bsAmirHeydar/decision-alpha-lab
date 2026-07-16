#ifndef SAEDV416_CENSORING_MQH
#define SAEDV416_CENSORING_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416CensoringValid(const bool observed,const int cause,const bool outcome_observed){if(!observed && cause!=7)return false;if(observed && cause==7)return false;if(!observed && outcome_observed)return false;return true;}
#endif
