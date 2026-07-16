#ifndef DECISION_ALPHA_LAB_SAED_V424_COVERAGERISK_MQH
#define DECISION_ALPHA_LAB_SAED_V424_COVERAGERISK_MQH
double SAEDV424Coverage(const int accepted,const int total){ return total>0?(double)accepted/(double)total:0.0; }
#endif
